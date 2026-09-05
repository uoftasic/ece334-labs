#!/usr/bin/env python3
"""Re-measure every number the manuals publish, and print them in a stable,
diffable form.

This is the regression oracle for a toolchain change. Run it on the old image,
run it on the new one, diff the two outputs: anything that moves is either a
manual that now lies to students or a real behavioural change to explain.

    python3 instructors/golden_numbers.py > /tmp/golden-<tag>.txt

Everything here is deck-driven, so it needs no schematic the student has to
draw and no GUI. Lab 2 rebuilds the reference layout from build_nand2.tcl.
"""
import os
import re
import subprocess
import sys

import numpy as np

sys.path.insert(0, "/foss/designs/common")
from ece334lib import measure, sim  # noqa: E402

DESIGNS = os.environ.get("DESIGNS", "/foss/designs")
VDD = 1.8
OUT = {}


def rec(key, value, unit="", nd=1):
    OUT[key] = "n/a" if value is None else ("%.*f %s" % (nd, value, unit)).strip()


def ps(x):
    """Scale to ps, tolerating a measurement that found no such edge."""
    return None if x is None else x * 1e12


def at(w, sig, t):
    return float(np.interp(t, w.x, w[sig]))


def crossing(w, sig, level, rising=True, n=1, after=0.0):
    t, y = w.x, w[sig]
    k = t >= after
    t, y = t[k], y[k]
    below = y < level
    idx = np.flatnonzero(below[:-1] & ~below[1:]) if rising else \
          np.flatnonzero(~below[:-1] & below[1:])
    if len(idx) < n:
        return None
    i = idx[n - 1]
    return float(t[i] + (level - y[i]) * (t[i+1] - t[i]) / (y[i+1] - y[i]))


def sh(cmd, cwd=None):
    return subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)


# ------------------------------------------------------------------ Lab 1
def lab1():
    d = os.path.join(DESIGNS, "lab1_spice")
    # rc.spice writes a rawfile, not a wrdata table.
    w = sim.run_deck(os.path.join(d, "spice/rc.spice"), output="rc.raw")
    tr, _ = measure.edges_10_90(w, "out", vdd=float(np.max(w["out"])))
    rec("lab1.rc.Vfinal", float(np.max(w["out"])), "V", 3)
    rec("lab1.rc.t_rise_10_90", ps(tr), "ps")

    dn = sim.run_deck(os.path.join(d, "spice/nmos_diode.spice"),
                      output="nmos_iv.txt", fmt="wrdata", names=["id"])
    rn = measure.extract_square_law(dn.x, dn["id"], wl=10/2, vmin=1.0, vmax=1.7)
    rec("lab1.Vtn", rn["Vt"], "V", 4)
    rec("lab1.KPn_uA_V2", rn["KP"] * 1e6, "", 1)

    dp = sim.run_deck(os.path.join(d, "spice/pmos_diode.spice"),
                      output="pmos_iv.txt", fmt="wrdata", names=["vsg", "id"])
    rp = measure.extract_square_law(dp["vsg"], dp["id"], wl=10/2, vmin=1.0, vmax=1.7)
    rec("lab1.Vtp_abs", abs(rp["Vt"]), "V", 4)
    rec("lab1.KPp_uA_V2", rp["KP"] * 1e6, "", 1)

    sim.run_deck(os.path.join(d, "spice/inverter_tb.spice"), output="inv_tran.txt",
                 fmt="wrdata", names=["vi", "vo"])
    tran = sim.run(os.path.join(d, "spice/inv_tran.txt"), fmt="wrdata", names=["vi", "vo"])
    dc = sim.run(os.path.join(d, "spice/inv_dc.txt"), fmt="wrdata", names=["vi", "vo"])
    rec("lab1.inv.dc_rows", float(len(dc.x)), "", 0)
    rec("lab1.inv.Vm", measure.vtc_trip(dc, "vi", "vo"), "V", 4)
    nm = measure.noise_margins(dc, "vi", "vo")
    rec("lab1.inv.NMH", nm["NMH"], "V", 3)
    rec("lab1.inv.NML", nm["NML"], "V", 3)
    # The hand deck starts its pulse at td=0, so the output is already high at
    # t=0 and edges_10_90 finds no first RISING edge. That is a property of the
    # deck, identical on both images -- not something to chase.
    tr, tf = measure.edges_10_90(tran, "vo", vdd=VDD)
    rec("lab1.inv.t_rise", ps(tr), "ps")
    rec("lab1.inv.t_fall", ps(tf), "ps")

    pg = sim.run_deck(os.path.join(d, "spice/pulsegen.spice"), output="pulsegen.raw")
    rec("lab1.pulsegen.width", ps(measure.pulse_width(pg, "out", vdd=VDD)), "ps")


# ------------------------------------------------------------------ Lab 2
def lab2():
    d = os.path.join(DESIGNS, "lab2_layout")
    sh('echo "source $PDK_ROOT/sky130A/libs.tech/magic/sky130A.magicrc" > .magicrc', cwd=d)
    r = sh("timeout 600 magic -dnull -noconsole -T sky130A < %s/instructors/lab2/build_nand2.tcl"
           % DESIGNS, cwd=d)
    m = re.search(r"DRC_COUNT=(\d+)", r.stdout + r.stderr)
    rec("lab2.drc_count", float(m.group(1)) if m else None, "", 0)

    lvs = os.path.join(d, "nand2.lvs.spice")
    if os.path.exists(lvs):
        txt = open(lvs).read()
        rec("lab2.extracted_devices",
            float(len([l for l in txt.splitlines() if l.strip().lower().startswith("x")])), "", 0)
        ws = sorted(set(re.findall(r"\bw=([\d.]+)", txt, re.I)))
        OUT["lab2.extracted_widths"] = ",".join(ws)
    r = sh("%s/scripts/run_lvs.sh nand2.lvs.spice %s/lab2_layout/xschem/nand2_lvs.sch"
           % (DESIGNS, DESIGNS), cwd=d)
    OUT["lab2.lvs"] = "match" if "Circuits match uniquely" in (r.stdout + r.stderr) else "MISMATCH"

    tmpl = open(os.path.join(d, "spice/nand2_compare.spice")).read()
    for cl in ["0", "1f", "5f", "20f", "100f"]:
        for label, inc in (("ideal", "nand2.lvs.spice"), ("pex", "nand2.pex.spice")):
            deck = re.sub(r"^\.include\s+nand2\.\w+\.spice", ".include " + inc, tmpl, flags=re.M)
            deck = re.sub(r"^(\.param\s+CLOAD\s*=\s*)\S+", r"\g<1>" + cl, deck, flags=re.M)
            p = os.path.join(d, "_golden_tmp.spice")
            open(p, "w").write(deck)
            try:
                w = sim.run_deck(p, output="nand2_wave.raw", cwd=d)
                rec("lab2.tpHL.%s.%s" % (cl, label),
                    measure.prop_delays(w, "a", "out", vdd=VDD)[0] * 1e12, "ps")
            finally:
                if os.path.exists(p):
                    os.remove(p)


# ------------------------------------------------------------------ Lab 3
def lab3():
    d = os.path.join(DESIGNS, "lab3_digital")
    inv = sim.run_deck(os.path.join(d, "spice/unit_inv.spice"), output="unit_inv.raw")
    tr, tf = measure.edges_10_90(inv, "out", vdd=VDD)
    thl, tlh = measure.prop_delays(inv, "in", "out", vdd=VDD)
    rec("lab3.uinv.t_rise", tr * 1e12, "ps"); rec("lab3.uinv.t_fall", tf * 1e12, "ps")
    rec("lab3.uinv.t_pHL", thl * 1e12, "ps"); rec("lab3.uinv.t_pLH", tlh * 1e12, "ps")

    a = sim.run_deck(os.path.join(d, "spice/aoi21_cases.spice"), output="aoi21_cases.raw")
    trw, tfw = measure.edges_10_90(a, "yw", vdd=VDD)
    _, tfb = measure.edges_10_90(a, "ybf", vdd=VDD)
    trb, _ = measure.edges_10_90(a, "ybr", vdd=VDD)
    rec("lab3.aoi21.tf_worst", tfw * 1e12, "ps"); rec("lab3.aoi21.tr_worst", trw * 1e12, "ps")
    rec("lab3.aoi21.tf_best", tfb * 1e12, "ps");  rec("lab3.aoi21.tr_best", trb * 1e12, "ps")


# ------------------------------------------------------------------ Lab 4
def lab4():
    d = os.path.join(DESIGNS, "lab4_sram")
    df = sim.sweep_param(os.path.join(d, "spice/dff_char.spice"), "DSKEW",
                         ["1000p", "500p", "300p", "260p", "240p", "220p", "200p"],
                         lambda w: {"q": at(w, "q", 38e-9)}, output="dff_char.raw")
    ok = [s for s, q in zip(df["DSKEW"], df["q"]) if q > VDD/2]
    bad = [s for s, q in zip(df["DSKEW"], df["q"]) if q <= VDD/2]
    OUT["lab4.setup.captures_to"] = min(ok, key=lambda s: float(s.rstrip("p"))) if ok else "none"
    OUT["lab4.setup.fails_at"] = max(bad, key=lambda s: float(s.rstrip("p"))) if bad else "none"

    ch = sim.run_deck(os.path.join(d, "spice/dff_char.spice"), output="dff_char.raw")
    tc = crossing(ch, "cl", VDD/2, True, 1)
    rec("lab4.t_PCQ", (crossing(ch, "q", VDD/2, True, 1, after=tc) - tc) * 1e12, "ps")

    cn = sim.run_deck(os.path.join(d, "spice/dff_chain.spice"), output="dff_chain.raw")
    t1 = crossing(cn, "q1", VDD/2, True, 1)
    rec("lab4.t_logic", (crossing(cn, "d2", VDD/2, True, 1, after=t1) - t1) * 1e12, "ps")

    sw = sim.sweep_param(os.path.join(d, "spice/dff_chain.spice"), "TCLK",
                         ["8n", "4n", "3n", "2.5n"],
                         lambda w: {"q2": float(np.ptp(w["q2"][w.x > 60e-9]))},
                         output="dff_chain.raw")
    cap = [t for t, s in zip(sw["TCLK"], sw["q2"]) if s > 0.9 * VDD]
    OUT["lab4.fmax.captures_at"] = ",".join(cap) if cap else "none"

    for tag, deck in (("nominal", "sram6t.spice"),
                      ("read_fail", "sram6t_read_fail.spice"),
                      ("write_fail", "sram6t_write_fail.spice")):
        w = sim.run_deck(os.path.join(d, "spice", deck),
                         output=deck.replace(".spice", ".raw"))
        rec("lab4.sram.%s.a_after_write" % tag, at(w, "a", 19e-9), "V", 3)
        rec("lab4.sram.%s.disturb_mV" % tag,
            1e3 * float(np.max(w["a_b"][w.x >= 29.1e-9])), "mV", 0)
        if tag == "nominal":
            tw = crossing(w, "word", VDD/2, True, 2)
            db = w["bit"] - w["bit_b"]
            i = np.flatnonzero((w.x > tw) & (np.abs(db) > 0.2))
            rec("lab4.sram.read_time", (float(w.x[i[0]]) - tw) * 1e12 if len(i) else None, "ps")


for name, fn in (("lab1", lab1), ("lab2", lab2), ("lab3", lab3), ("lab4", lab4)):
    if len(sys.argv) > 1 and name not in sys.argv[1:]:
        continue
    try:
        fn()
    except Exception as exc:                                    # noqa: BLE001
        OUT["%s.ERROR" % name] = "%s: %s" % (type(exc).__name__, exc)

for k in sorted(OUT):
    print("%-34s %s" % (k, OUT[k]))
