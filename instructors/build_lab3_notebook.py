"""Generate lab3_digital/lab3.ipynb. See build_lab1_notebook.py for the shape.

    python3 instructors/build_lab3_notebook.py lab3_digital/lab3.ipynb
"""
import json
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "lab3_digital/lab3.ipynb"


def md(text):
    return {"cell_type": "markdown", "metadata": {},
            "source": text.strip("\n").splitlines(True)}


def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": text.strip("\n").splitlines(True)}


ANSWER = """
### Your answer

*Replace this text.* Give the measured value, what your hand analysis
predicted, the percentage difference, and one sentence explaining the gap.
"""

cells = [
    md("""
# ECE334 Lab 3 — Digital building blocks

**Name:**
**Student number:**
**Date:**

This notebook is your lab report. Its sections match the manual:
<https://uoftasic.github.io/ece334-docs/labs/lab3/>

Before you start, in the container terminal:

```bash
. /foss/designs/common/.designinit
cd /foss/designs/lab3_digital
jlab
```
"""),
    code("""
import numpy as np
import matplotlib.pyplot as plt

from ece334lib import measure, plot, sim

VDD = 1.8
%matplotlib inline

# Your four extracted parameters from Lab 1 P2. Use YOUR numbers, not these.
Vtn, KPn = 0.75, 130e-6      # V, A/V^2
Vtp, KPp = 0.85, 45e-6
"""),

    # ---------------------------------------------------------------- P1/L1
    md("""
---
## P1 / L1 — The unit inverter

$W_n = 1$, $W_p = 3$, $L = 0.5$, driving $C_L = 0.3$ pF.

Model each conducting device as an equivalent resistance:

$$R_{eq} = \\frac{V_{DD}}{K_P\\frac{W}{L}(V_{DD}-|V_t|)},
\\qquad t_f \\approx 2.2\\,R_{eq,n}C_L,
\\qquad t_r \\approx 2.2\\,R_{eq,p}C_L$$
"""),
    code("""
# --- P1 hand analysis -------------------------------------------------------
WLn, WLp = 1 / 0.5, 3 / 0.5
CL = 0.3e-12

Req_n = VDD / (KPn * WLn * (VDD - Vtn))
Req_p = VDD / (KPp * WLp * (VDD - Vtp))

tf_hand = 2.2 * Req_n * CL
tr_hand = 2.2 * Req_p * CL

print(f"Req_n = {Req_n/1e3:6.2f} kOhm    t_fall = {tf_hand*1e12:6.0f} ps")
print(f"Req_p = {Req_p/1e3:6.2f} kOhm    t_rise = {tr_hand*1e12:6.0f} ps")
"""),
    code("""
# --- L1 measurement ---------------------------------------------------------
inv = sim.run_deck("spice/unit_inv.spice", output="unit_inv.raw")

tr_sim, tf_sim = measure.edges_10_90(inv, "out", vdd=VDD)
tphl, tplh = measure.prop_delays(inv, "in", "out", vdd=VDD)

print(f"t_rise = {tr_sim*1e12:6.0f} ps   (hand {tr_hand*1e12:.0f} ps)")
print(f"t_fall = {tf_sim*1e12:6.0f} ps   (hand {tf_hand*1e12:.0f} ps)")
print(f"t_pHL  = {tphl*1e12:6.0f} ps")
print(f"t_pLH  = {tplh*1e12:6.0f} ps")

plot.transient(inv, ["in", "out"])
plt.title("L1  Unit inverter into 0.3 pF"); plt.show()
"""),
    md(ANSWER + """
The rise is slower than the fall even though the PMOS is three times wider.
Say what that tells you about the two carrier mobilities.
"""),

    # ---------------------------------------------------------------- P2/L2
    md("""
---
## P2 / L2 — The complex gate

$$Y = \\overline{A + B\\cdot C}$$

The pull-down network conducts when $A + BC$ is true: one NMOS for $A$ in
**parallel** with a **series** pair for $B$ and $C$. The pull-up is the dual.

Four input patterns matter. Fill in your P2 answer for each before you look at
the numbers.

| Case | Hold | Switch | Conducting path |
|---|---|---|---|
| Worst fall | $a=0$, $c=1$ | $b$: 0→1 | series $b$–$c$ only |
| Worst rise | $c=1$ | $b$: 1→0 | $a$ in series with $b$ alone |
| Best fall | — | $a$, $b$, $c$ together 0→1 | every pull-down path |
| Best rise | $b=c=0$ | $a$: 1→0 | both parallel PMOS |
"""),
    code("""
# --- P2 hand analysis: what should the ratio be? ----------------------------
# The worst-case fall drives C_L through TWO series NMOS; the best case has
# every pull-down path on at once. Predict the ratio before measuring it.
worst_fall_paths = 1     # the series b-c branch, on its own
best_fall_paths  = 2     # a's branch in parallel with the b-c branch

print(f"expected t_f(worst) / t_f(best) ~ "
      f"{best_fall_paths/worst_fall_paths:.1f}x")
"""),
    code("""
# --- L2 measurement: all four cases in one deck -----------------------------
# yw  = worst case, ybf = best-case fall, ybr = best-case rise.
aoi = sim.run_deck("spice/aoi21_cases.spice", output="aoi21_cases.raw")

tr_w, tf_w = measure.edges_10_90(aoi, "yw",  vdd=VDD)
_,    tf_b = measure.edges_10_90(aoi, "ybf", vdd=VDD)
tr_b, _    = measure.edges_10_90(aoi, "ybr", vdd=VDD)

print(f"          {'t_f (ps)':>10} {'t_r (ps)':>10}")
print(f"worst     {tf_w*1e12:10.0f} {tr_w*1e12:10.0f}")
print(f"best      {tf_b*1e12:10.0f} {tr_b*1e12:10.0f}")
print(f"ratio     {tf_w/tf_b:10.2f} {tr_w/tr_b:10.2f}")
"""),
    code("""
# --- L2: the three output waveforms together --------------------------------
fig, ax = plt.subplots(figsize=(9, 4))
for sig, lbl in (("yw", "worst case"), ("ybf", "best-case fall"),
                 ("ybr", "best-case rise")):
    ax.plot(aoi.x * 1e9, aoi[sig], label=lbl)
ax.set_xlabel("time (ns)"); ax.set_ylabel("Y (V)")
ax.legend(); ax.grid(alpha=0.3)
plt.title("L2  AOI21 output for each input pattern"); plt.show()
"""),
    md(ANSWER + """
Compare the AOI21 against the unit inverter of L1. It drives five times the
load with much wider devices — did the delay go up or down, and does that match
what the $R_{eq}$ model says it should?
"""),

    # ---------------------------------------------------------------- P3/L3
    md("""
---
## P3 / L3 — The flip-flop

A master–slave pair. Each latch is two NOR gates in a loop that a transmission
gate closes when the input gate is open:

```
master   TG1 (CL_b) : data -> m1
         NOR_A (m1, SETQ)      -> m2
         NOR_B (m2, RESETQ)    -> m3
         TG2 (CL)   : m3 -> m1        hold while the clock is high
slave    TG3 (CL)   : m3 -> s1
         NOR_C (s1, SETQ)      -> Q_b
         NOR_D (Q_b, RESETQ)   -> Q
         TG4 (CL_b) : Q  -> s1        hold while the clock is low
```

Build it in `xschem/dff_tb.sch` and press **Netlist & Simulate**.
"""),
    code("""
# --- L3: the four-panel plot ------------------------------------------------
d = sim.raw("dff_tb.raw")

panels = [(["cl", "x1.cl_b"], "clock"),
          (["setq", "resetq"], "set / reset"),
          (["data"],           "data"),
          (["q", "q_b"],       "outputs")]

fig, axes = plt.subplots(len(panels), 1, sharex=True, figsize=(10, 8))
for ax, (sigs, title) in zip(axes, panels):
    for s in sigs:
        ax.plot(d.x * 1e9, d[s], label=s)
    ax.set_ylabel("V"); ax.set_title(title, loc="left", fontsize=9)
    ax.legend(loc="upper right", fontsize=8); ax.grid(alpha=0.3)
axes[-1].set_xlabel("time (ns)")
fig.suptitle("L3  Master-slave flip-flop"); fig.tight_layout(); plt.show()
"""),
    code("""
# --- L3: check the capture behaviour numerically ----------------------------
# Q should take the value DATA held just before each rising clock edge. Ignore
# everything before the first rising edge at 20 ns: the feedback loops start
# from an arbitrary state and take a cycle to settle.
def rising_edges(wave, sig, level=VDD/2, after=0.0):
    t, y = wave.x, wave[sig]
    below = y < level
    idx = np.flatnonzero(below[:-1] & ~below[1:])
    return t[idx][t[idx] >= after]

edges = rising_edges(d, "cl", after=20e-9)
print(f"{'clock edge':>12} {'DATA before':>12} {'Q after':>9}  captured")
for te in edges[:8]:
    before = float(np.interp(te - 1e-9, d.x, d["data"]))
    after  = float(np.interp(te + 4e-9, d.x, d["q"]))
    ok = (before > VDD/2) == (after > VDD/2)
    print(f"{te*1e9:10.1f} ns {before:11.2f} V {after:8.2f} V  "
          f"{'yes' if ok else 'NO'}")
"""),
    md("""
### Your truth table

Fill this in from the plot. Cover, at minimum: what Q does on a rising clock
edge, what it does between edges, and what SETQ and RESETQ do irrespective of
the clock.

| CL | SETQ | RESETQ | DATA | Q | Comment |
|---|---|---|---|---|---|
| ↑ | 0 | 0 | 0 | | |
| ↑ | 0 | 0 | 1 | | |
| 0 or 1 | 0 | 0 | X | | |
| X | 1 | 0 | X | | |
| X | 0 | 1 | X | | |

Also explain why the two transmission gates in each latch are driven by
opposite clock phases. What would happen if they were driven by the same one?
"""),
    md(ANSWER),

    # ---------------------------------------------------------------- summary
    md("""
---
## Summary

| Quantity | Hand | Simulated |
|---|---|---|
| Unit inverter $t_r$ | | |
| Unit inverter $t_f$ | | |
| AOI21 worst-case $t_f$ | | |
| AOI21 best-case $t_f$ | | |
| AOI21 worst-case $t_r$ | | |
| AOI21 best-case $t_r$ | | |

Carry the unit inverter numbers into Lab 4 — the flip-flop path there is built
from these same cells.
"""),
]

# nbformat 4.5 requires a stable id on every cell; without one, jupyter warns
# on every execution and will eventually refuse the notebook outright.
for _i, _c in enumerate(cells):
    _c["id"] = "c%03d" % _i

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python",
                       "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

with open(OUT, "w") as fh:
    json.dump(nb, fh, indent=1)
    fh.write("\n")
print(f"wrote {OUT}  ({len(cells)} cells)")
