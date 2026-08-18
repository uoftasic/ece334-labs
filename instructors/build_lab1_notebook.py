"""Generate lab1_spice/lab1.ipynb.

The notebook is the student's report. Each section of the manual maps to four
cells here: a heading, a hand-analysis cell they fill in, a measurement cell
that runs, and an answer block they write into. Generating it from this script
keeps that shape consistent and makes it reviewable as a diff.

    python3 instructors/build_lab1_notebook.py lab1_spice/lab1.ipynb
"""
import json
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "lab1_spice/lab1.ipynb"


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip("\n").splitlines(True)}


def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": text.strip("\n").splitlines(True)}


ANSWER = """
### Your answer

*Replace this text.* State the measured value, the value your hand analysis
predicted, the percentage difference, and one sentence explaining the gap.
"""

cells = [
    md("""
# ECE334 Lab 1 — Basic SPICE simulations

**Name:**
**Student number:**
**Date:**

This notebook is your lab report. Its sections match the manual:
<https://uoftasic.github.io/ece334-docs/labs/lab1/>

For each section: fill in the hand-analysis cell with your own numbers, run the
measurement cell, then write your comparison in the answer block. A section
with no written answer is incomplete, however many plots it contains.

Before you start, in the container terminal:

```bash
. /foss/designs/common/.designinit
cd /foss/designs/lab1_spice
jlab
```
"""),
    code("""
import numpy as np
import matplotlib.pyplot as plt

from ece334lib import measure, plot, sim

VDD = 1.8
%matplotlib inline

# Results are written by the "Netlist & Simulate" button in each testbench.
# sim.raw() finds them by filename, so it does not matter which directory
# XSchem was started from.
"""),

    # ---- P1 ----
    md("""
---
## P1 / L1 — RC divider step response

Open `xschem/rc_tb.sch` and press **Netlist & Simulate**.

$R_1 = 1\\,\\mathrm{k}\\Omega$ into `out`, loaded by $R_2 = 2\\,\\mathrm{k}\\Omega$
in parallel with $C_1 = 0.7\\,\\mathrm{pF}$.
"""),
    code("""
# --- P1 hand analysis -------------------------------------------------------
R1, R2, C1 = 1e3, 2e3, 0.7e-12

Vf_hand   = VDD * R2 / (R1 + R2)
tau_hand  = (R1 * R2 / (R1 + R2)) * C1
tr_hand   = tau_hand * np.log(9)

print(f"Vout(inf) = {Vf_hand:.3f} V")
print(f"tau       = {tau_hand*1e12:.1f} ps")
print(f"t_rise    = {tr_hand*1e12:.1f} ps")
"""),
    code("""
# --- P1 measurement ---------------------------------------------------------
rc = sim.raw("rc_tb.raw")

Vf_sim = float(np.max(rc["out"]))
tr_sim, _ = measure.edges_10_90(rc, "out", vdd=Vf_hand)

# Read tau from the 10-90 % time. The input ramps over 0.2 ns, so the step has
# no single origin and a 63.2 % reading taken from t = 0 is biased high.
tau_sim = tr_sim / np.log(9)

print(f"Vout(inf) = {Vf_sim:.3f} V     (hand {Vf_hand:.3f} V)")
print(f"tau       = {tau_sim*1e12:.1f} ps   (hand {tau_hand*1e12:.1f} ps)")
print(f"t_rise    = {tr_sim*1e12:.1f} ps   (hand {tr_hand*1e12:.1f} ps)")

plot.transient(rc, ["in", "out"])
plt.title("P1  RC divider step response")
plt.show()
"""),
    md(ANSWER),

    # ---- P2 ----
    md("""
---
## P2 / L2 — Extract $K_P$ and $V_t$

Build a diode-connected NMOS in the DUT of `xschem/diode_tb.sch`
(gate and drain to `g`, source and body to `s`, `W=10`, `L=2`), then
**Netlist & Simulate**.

A diode-connected device is saturated whenever it conducts, so

$$I_D = \\tfrac{1}{2}K_P\\tfrac{W}{L}(V_{GS}-V_t)^2
\\;\\Longrightarrow\\;
\\sqrt{I_D}\\ \\text{is linear in}\\ V_{GS}$$

The fitted slope $m$ gives $K_P = 2m^2/(W/L)$ and the x-intercept gives $V_t$.
"""),
    code("""
# --- P2 measurement: NMOS ---------------------------------------------------
dn = sim.raw("diode_nmos.raw")
rn = measure.extract_square_law(dn["g"], dn["id"], wl=10 / 2, vmin=1.0, vmax=1.7)

Vtn, KPn = rn["Vt"], rn["KP"]
print(f"Vtn = {Vtn:.3f} V     KPn = {KPn*1e6:.1f} uA/V^2")

fig, ax = plt.subplots()
ax.plot(dn["g"], np.sqrt(np.clip(dn["id"], 0, None)) * 1e3, label=r"$\\sqrt{I_D}$")
vfit = np.array([Vtn, VDD])
ax.plot(vfit, (rn["slope"] * vfit + rn["intercept"]) * 1e3, "--", label="fit")
ax.axvspan(1.0, 1.7, color="0.9", zorder=0)
ax.set_xlabel("$V_{GS}$ (V)"); ax.set_ylabel(r"$\\sqrt{I_D}$ (mA$^{1/2}$)")
ax.legend(); ax.grid(alpha=0.3)
plt.title("P2  NMOS square-law fit"); plt.show()
"""),
    code("""
# --- P2 measurement: PMOS ---------------------------------------------------
# Build the diode-connected PMOS in the DUT of xschem/diode_pmos_tb.sch and
# press Netlist & Simulate. These are the last two of the four parameters you
# use for the rest of the lab.

dp = sim.raw("diode_pmos.raw")
# The PMOS bench grounds the gate and sweeps the source, so the swept variable
# is V_SG directly and the same square-law fit applies unchanged.
rp = measure.extract_square_law(dp["vsg"], dp["id"], wl=10 / 2, vmin=1.0, vmax=1.7)

Vtp, KPp = abs(rp["Vt"]), rp["KP"]
print(f"|Vtp| = {Vtp:.3f} V    KPp = {KPp*1e6:.1f} uA/V^2")
"""),
    md(ANSWER + """
Also state the fit window you used and why. Report all four parameters:
$V_{tn}$, $K_{Pn}$, $|V_{tp}|$, $K_{Pp}$.
"""),

    # ---- P3 ----
    md("""
---
## P3 / L3 — CMOS inverter

Build the inverter in the DUT of `xschem/inv_tb.sch`: $W_n=1$, $W_p=3$,
$L=0.5$. **Netlist & Simulate** writes `inv_tb_vtc.raw` and `inv_tb_tran.raw`.
"""),
    code("""
# --- P3 measurement: transfer characteristic --------------------------------
vtc = sim.raw("inv_tb_vtc.raw")
nm = measure.noise_margins(vtc, "in", "out")

print(f"V_M  = {nm['VM']:.3f} V")
print(f"NM_H = {nm['NMH']:.3f} V     NM_L = {nm['NML']:.3f} V")

plot.vtc(vtc, "in", "out")
plt.title("P3  Inverter transfer characteristic"); plt.show()
"""),
    code("""
# --- P3 hand analysis: equivalent-resistance timing -------------------------
# Uses YOUR extracted parameters from P2.
WLn, WLp = 1 / 0.5, 3 / 0.5
CL = 0.2e-12

Req_n = VDD / (KPn * WLn * (VDD - Vtn))
Req_p = VDD / (KPp * WLp * (VDD - Vtp))

tf_hand = 2.2 * Req_n * CL
tr_hand = 2.2 * Req_p * CL

print(f"Req_n = {Req_n/1e3:.2f} kOhm    t_fall = {tf_hand*1e12:.0f} ps")
print(f"Req_p = {Req_p/1e3:.2f} kOhm    t_rise = {tr_hand*1e12:.0f} ps")
"""),
    code("""
# --- P3 measurement: transient ----------------------------------------------
tran = sim.raw("inv_tb_tran.raw")

tpd = measure.prop_delay(tran, "in", "out", vdd=VDD)
tr_sim, tf_sim = measure.edges_10_90(tran, "out", vdd=VDD)

print(f"t_rise = {tr_sim*1e12:6.0f} ps   (hand {tr_hand*1e12:.0f} ps)")
print(f"t_fall = {tf_sim*1e12:6.0f} ps   (hand {tf_hand*1e12:.0f} ps)")
print(f"t_pd   = {tpd*1e12:6.0f} ps")

plot.transient(tran, ["in", "out"])
plt.title("P3  Inverter transient, CL = 0.2 pF"); plt.show()
"""),
    md(ANSWER + """
Answer two more things:

1. $V_M$ is not at $V_{DD}/2$. Why, and what would you change to move it there?
2. The hand estimate is optimistic. Name the two effects that account for most
   of the gap.
"""),

    # ---- P4 ----
    md("""
---
## P4 / L4 — Pulse generator

Build the circuit in the DUT of `xschem/pulsegen_tb.sch` from the `inv` and
`nand2` cells in `common/xschem`: three inverters in a chain, the chain output
and the original input into the NAND. Wire the chain output to the `n3` port.
"""),
    code("""
# --- P4 measurement ---------------------------------------------------------
pg = sim.raw("pulsegen_tb.raw")
pw = measure.pulse_width(pg, "out", vdd=VDD, polarity="low")
print(f"pulse width (50-50 %) = {pw*1e12:.1f} ps")

t = pg.x * 1e9
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.plot(t, pg["in"], label="in")
ax.plot(t, pg["n3"] + 2.2, label="n3 (offset)")
ax.plot(t, pg["out"] + 4.4, label="out (offset)")
ax.set_xlabel("time (ns)"); ax.set_ylabel("voltage (V), offset")
ax.legend(); ax.grid(alpha=0.3)
plt.title("P4  Pulse generator"); plt.show()
"""),
    code("""
# --- P4 design task: size the load at n3 for a 1.5 ns pulse -----------------
# Step 1: a first-order estimate. Only the FALLING edge of n3 closes the pulse,
# and that edge is driven by the third inverter's NMOS, so use Req_n.
target = 1.5e-9
C_first_order = (target - pw) / (0.69 * Req_n)
print(f"measured width   = {pw*1e12:.0f} ps")
print(f"first-order C(n3)= {C_first_order*1e15:.0f} fF")

# Step 2: calibrate. Expect the first-order number to be about 3x too LARGE.
# It predicts roughly 2.6 ps of extra width per fF; the circuit actually gives
# about 7.1 ps/fF, so it needs far less capacitance than the model claims.
# Req above is the resistance at full overdrive, while the real device spends
# much of the transition with less gate drive and out of saturation.
# So measure the sensitivity instead of trusting it: simulate at two values of
# C(n3) and interpolate.
#
#   C_a, width_a = 40e-15, <width you measured>   # fill these in
#   C_b, width_b = 80e-15, <width you measured>
#   slope = (width_b - width_a) / (C_b - C_a)     # s/F
#   C_needed = C_a + (target - width_a) / slope
#
# Step 3: put C_needed at n3, re-simulate, and confirm the width.
"""),
    md(ANSWER + """
State the capacitance you predicted, the capacitance you used, and the width you
measured. If the prediction was off by more than about 20 %, say which
assumption broke.
"""),

    md("""
---
## Checklist

- [ ] P1 — $V_{in}$/$V_{out}$ plot; measured $\\tau$ and $t_r$ against hand analysis
- [ ] P2 — NMOS and PMOS fits; all four parameters, with the fit window stated
- [ ] P3 — VTC with $V_M$, $NM_H$, $NM_L$; transient against your own estimate
- [ ] P4 — waveforms and measured width; predicted and achieved 1.5 ns load
- [ ] Every answer block filled in
"""),
]

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

with open(OUT, "w") as fh:
    json.dump(nb, fh, indent=1)
    fh.write("\n")
print(f"wrote {OUT}  ({len(cells)} cells)")
