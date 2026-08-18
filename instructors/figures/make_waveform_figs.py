"""Generate the Lab 0 and Lab 1 waveform figures for the manual.

Waveform figures are drawn with matplotlib rather than screen-grabbed, so the
axes are labelled, the measured quantity is annotated on the plot, and the whole
set can be regenerated after a tool or model update.

    python3 instructors/figures/make_waveform_figs.py <rawdir> <outdir>
"""
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from ece334lib import measure, sim  # noqa: E402

VDD = 1.8
RAW = sys.argv[1] if len(sys.argv) > 1 else "/tmp/M"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/figs"
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "figure.figsize": (7.2, 4.0),
    "figure.dpi": 150,
    "font.size": 10,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "legend.frameon": False,
    "savefig.bbox": "tight",
})


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path)
    plt.close(fig)
    print("wrote", path)


def mark_span(ax, t0, t1, y, label, side="right"):
    """Draw a horizontal measurement span, labelled clear of the arrow."""
    ax.annotate("", xy=(t0, y), xytext=(t1, y),
                arrowprops=dict(arrowstyle="<->", color="0.25", lw=1.2))
    if side == "right":
        ax.text(t1, y, f"  {label}", ha="left", va="center", fontsize=9,
                color="0.15")
    else:
        ax.text(t0, y, f"{label}  ", ha="right", va="center", fontsize=9,
                color="0.15")


# --- Lab 1 P1: RC divider step response -------------------------------------
rc = sim.raw(f"{RAW}/rc_tb.raw")
t = rc.x * 1e9
fig, ax = plt.subplots()
ax.plot(t, rc["in"], label="$V_{in}$", lw=1.4)
ax.plot(t, rc["out"], label="$V_{out}$", lw=1.8)
tr, _ = measure.edges_10_90(rc, "out", vdd=1.2)
xs, dirs = measure._crossings(rc.x, rc["out"], 0.1 * 1.2)
t10 = xs[dirs == 1][0] * 1e9
xs, dirs = measure._crossings(rc.x, rc["out"], 0.9 * 1.2)
t90 = xs[dirs == 1][0] * 1e9
ax.axhline(1.2, color="0.6", ls=":", lw=1)
ax.text(0.985, 0.66, "1.200 V final", transform=ax.transAxes, ha="right",
        va="bottom", fontsize=9, color="0.35")
for lev in (0.12, 1.08):
    ax.axhline(lev, color="0.8", ls=":", lw=0.8)
mark_span(ax, t10, t90, 1.32, f"$t_r$ = {tr * 1e12:.0f} ps (10-90 %)")
ax.set_xlim(0, 8)
ax.set_xlabel("time (ns)")
ax.set_ylabel("voltage (V)")
ax.set_title("P1  RC divider step response: $R_1$=1 k, $R_2$=2 k, $C_1$=0.7 pF")
ax.legend(loc="lower right")
save(fig, "02-rc-waves.png")

# --- Lab 1 P2: square-law fit ------------------------------------------------
d = sim.raw(f"{RAW}/diode_nmos.raw")
vg, idd = d["g"], d["id"]
res = measure.extract_square_law(vg, idd, wl=10 / 2, vmin=1.0, vmax=1.7)
fig, ax = plt.subplots()
ax.plot(vg, np.sqrt(np.clip(idd, 0, None)) * 1e3, lw=1.8,
        label=r"$\sqrt{I_D}$  (simulated)")
vfit = np.array([res["Vt"], 1.8])
ax.plot(vfit, (res["slope"] * vfit + res["intercept"]) * 1e3, "--", lw=1.4,
        color="0.35", label="fit over 1.0-1.7 V")
ax.axvspan(1.0, 1.7, color="0.85", alpha=0.5, zorder=0)
ax.plot([res["Vt"]], [0], "o", ms=6, color="0.2")
ax.annotate(f"$V_t$ = {res['Vt']:.3f} V",
            xy=(res["Vt"], 0), xytext=(res["Vt"] + 0.12, 4),
            arrowprops=dict(arrowstyle="->", color="0.3"), fontsize=10)
ax.text(0.03, 0.95, f"$K_P$ = {res['KP'] * 1e6:.1f} $\\mu$A/V$^2$",
        transform=ax.transAxes, va="top", fontsize=10)
ax.set_xlabel("$V_{GS}$ (V)")
ax.set_ylabel(r"$\sqrt{I_D}$  (mA$^{1/2}$)")
ax.set_title("P2  Diode-connected NMOS: slope gives $K_P$, intercept gives $V_t$")
ax.legend(loc="lower right")
save(fig, "04-sqrt-id-fit.png")

# --- Lab 1 P3: inverter VTC --------------------------------------------------
v = sim.raw(f"{RAW}/inv_tb_vtc.raw")
nm = measure.noise_margins(v, "in", "out")
fig, ax = plt.subplots()
vi = v["in"]
ax.plot(vi, v["out"], lw=1.8, label="VTC")
ax.plot(vi, vi, "k--", lw=0.8, alpha=0.5, label="$V_{out}=V_{in}$")
ax.axvline(nm["VM"], color="0.5", ls=":", lw=1)
ax.annotate(f"$V_M$ = {nm['VM']:.3f} V", xy=(nm["VM"], nm["VM"]),
            xytext=(nm["VM"] + 0.25, 1.35),
            arrowprops=dict(arrowstyle="->", color="0.3"), fontsize=10)
for lab, key in (("$V_{IL}$", "VIL"), ("$V_{IH}$", "VIH")):
    if key in nm:
        ax.axvline(nm[key], color="0.8", ls=":", lw=0.8)
        ax.text(nm[key], 1.02 * VDD, lab, ha="center", va="bottom", fontsize=9,
                color="0.35")
ax.text(0.03, 0.10,
        f"$NM_H$ = {nm['NMH']:.3f} V\n$NM_L$ = {nm['NML']:.3f} V",
        transform=ax.transAxes, fontsize=10)
ax.set_xlim(0, VDD)
ax.set_ylim(-0.05, VDD + 0.16)
ax.set_xlabel("$V_{in}$ (V)")
ax.set_ylabel("$V_{out}$ (V)")
ax.set_title("P3  Inverter transfer characteristic (Wn=1, Wp=3, L=0.5)")
ax.legend(loc="upper right")
save(fig, "06-inv-vtc.png")

# --- Lab 1 P3: inverter transient -------------------------------------------
tr_w = sim.raw(f"{RAW}/inv_tb_tran.raw")
t = tr_w.x * 1e9
fig, ax = plt.subplots()
ax.plot(t, tr_w["in"], label="$V_{in}$", lw=1.3)
ax.plot(t, tr_w["out"], label="$V_{out}$", lw=1.8)
t_rise, t_fall = measure.edges_10_90(tr_w, "out", vdd=VDD)
tpd = measure.prop_delay(tr_w, "in", "out", vdd=VDD)
ax.text(0.02, 0.5,
        f"$t_r$ = {t_rise * 1e12:.0f} ps\n$t_f$ = {t_fall * 1e12:.0f} ps\n"
        f"$t_{{pd}}$ = {tpd * 1e12:.0f} ps",
        transform=ax.transAxes, fontsize=10, va="center")
for lev, s in ((0.1 * VDD, "10 %"), (0.9 * VDD, "90 %"), (0.5 * VDD, "50 %")):
    ax.axhline(lev, color="0.85", ls=":", lw=0.8)
ax.set_ylim(-0.1, 2.35)
ax.set_xlabel("time (ns)")
ax.set_ylabel("voltage (V)")
ax.set_title("P3  Inverter transient, $C_L$ = 0.2 pF")
ax.legend(loc="upper right", ncol=2)
save(fig, "07-inv-transient.png")

# --- Lab 1 P4 / Lab 0: pulse generator --------------------------------------
p = sim.raw(f"{RAW}/pulsegen_tb.raw")
t = p.x * 1e9
pw = measure.pulse_width(p, "out", vdd=VDD, polarity="low")
xs, dirs = measure._crossings(p.x, p["out"], 0.5 * VDD)
tf = xs[dirs == -1][0] * 1e9
trr = xs[(dirs == 1) & (xs > xs[dirs == -1][0])][0] * 1e9
fig, ax = plt.subplots(figsize=(7.2, 4.6))
ax.plot(t, p["in"], label="in", lw=1.3)
ax.plot(t, p["n3"] + 2.2, label="n3 (chain output, offset)", lw=1.3)
ax.plot(t, p["out"] + 4.4, label="out (offset)", lw=1.8)
ax.axvspan(tf, trr, color="0.88", zorder=0)
mark_span(ax, tf, trr, 6.45, f"{pw * 1e12:.0f} ps")
ax.set_yticks([0, 0.9, 1.8, 2.2, 3.1, 4.0, 4.4, 5.3, 6.2])
ax.set_yticklabels(["0", "0.9", "1.8", "0", "0.9", "1.8", "0", "0.9", "1.8"])
ax.set_xlim(0.5, 4)
ax.set_xlabel("time (ns)")
ax.set_ylabel("voltage (V), traces offset")
ax.set_title("P4  Pulse generator: out is low while in and n3 are both high")
ax.legend(loc="lower right")
save(fig, "09-pulsegen-waves.png")

print("\nall waveform figures written to", OUT)
