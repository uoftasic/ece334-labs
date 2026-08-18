"""Generate lab4_sram/lab4.ipynb.

Same shape as build_lab1_notebook.py: every section of the manual becomes a
heading, a hand-analysis cell the student fills in, a measurement cell that
runs, and an answer block they write into.

    python3 instructors/build_lab4_notebook.py lab4_sram/lab4.ipynb
"""
import json
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "lab4_sram/lab4.ipynb"


def md(text):
    return {"cell_type": "markdown", "metadata": {},
            "source": text.strip("\n").splitlines(True)}


def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": text.strip("\n").splitlines(True)}


ANSWER = """
### Your answer

*Replace this text.* Give the measured value, what you expected, and one
sentence on the difference.
"""

cells = [
    md("""
# ECE334 Lab 4 — Flip-flop characterization and the 6T SRAM cell

**Name:**
**Student number:**
**Date:**

This notebook is your lab report. Its sections match the manual:
<https://uoftasic.github.io/ece334-docs/labs/lab4/>

Before you start, in the container terminal:

```bash
. /foss/designs/common/.designinit
cd /foss/designs/lab4_sram
jlab
```
"""),
    code("""
import numpy as np
import matplotlib.pyplot as plt

from ece334lib import measure, plot, sim

VDD = 1.8
%matplotlib inline


def value_at(wave, sig, t):
    \"\"\"The value of a signal at one instant, interpolated between samples.\"\"\"
    return float(np.interp(t, wave.x, wave[sig]))


def crossing(wave, sig, level, rising=True, n=1, after=0.0):
    \"\"\"Time of the n-th crossing of `level` after time `after`.

    Both t_PCQ and the read time are measured between two crossings, and
    picking the wrong one is the single most common way to get a negative or
    absurd number out of this lab.\"\"\"
    t, y = wave.x, wave[sig]
    keep = t >= after
    t, y = t[keep], y[keep]
    below = y < level
    idx = np.flatnonzero(below[:-1] & ~below[1:]) if rising else \\
          np.flatnonzero(~below[:-1] & below[1:])
    if len(idx) < n:
        raise ValueError(f"{sig} has only {len(idx)} such crossings of {level}")
    i = idx[n - 1]
    # Linear interpolation between the bracketing samples.
    return float(t[i] + (level - y[i]) * (t[i+1] - t[i]) / (y[i+1] - y[i]))
"""),

    # ---------------------------------------------------------------- P1
    md("""
---
## P1 — Size the SRAM cell

The two stability conditions pull against each other:

$$W_{N1} \\geq 2.7\\,W_{N2} \\quad\\text{(read)} \\qquad
  W_{N2} \\geq 1.2\\,W_{P1} \\quad\\text{(write)}$$

Enter your six widths below. The cell checks both conditions for you — but the
*reasoning* for your choice is what is marked, so write it in the answer block.
"""),
    code("""
# --- P1: your sizing --------------------------------------------------------
W_load   = 0.5    # P1, P2   cell load PMOS
W_access = 0.7    # N2, N4   access
W_driver = 2.0    # N1, N3   driver
L        = 0.5

read_ok  = W_driver >= 2.7 * W_access
write_ok = W_access >= 1.2 * W_load

print(f"read   {W_driver} >= 2.7 * {W_access} = {2.7*W_access:.2f}   "
      f"{'OK' if read_ok else 'VIOLATED'}")
print(f"write  {W_access} >= 1.2 * {W_load} = {1.2*W_load:.2f}   "
      f"{'OK' if write_ok else 'VIOLATED'}")
"""),
    md(ANSWER + """
Say why you chose these six numbers, not just that they satisfy the
inequalities. Which device did you size first, and what set its value?
"""),

    md("""
## P2 — Which device would you change?

1. If the **read** condition were violated, which transistor(s) would you
   resize, and in which direction?
2. If the **write** condition were violated, which transistor(s)?

Answer here *before* running L6 and L7, where you break each one on purpose.
"""),
    md(ANSWER),

    # ---------------------------------------------------------------- L1
    md("""
---
## L1 — Setup time

Setup time is the smallest gap between the data edge and the clock edge for
which the flip-flop still captures. Sweep the gap and find where capture
stops. `DSKEW` is that gap.
"""),
    code("""
# --- L1: sweep the data-to-clock gap ----------------------------------------
skews = ["1000p", "500p", "300p", "260p", "240p", "220p"]

setup = sim.sweep_param(
    "spice/dff_char.spice", "DSKEW", skews,
    lambda w: {"q_after_edge": value_at(w, "q", 38e-9)},
    output="dff_char.raw")

setup["captured"] = setup["q_after_edge"] > VDD / 2
print(setup.to_string(index=False))
"""),
    code("""
# --- L1: report the two values that bracket the boundary --------------------
passed = setup[setup["captured"]]
failed = setup[~setup["captured"]]

if passed.empty or failed.empty:
    # The sweep did not straddle the boundary, so there is nothing to bracket.
    raise SystemExit(
        "Every skew in the sweep gave the same answer, so the boundary is "
        "outside it. Extend `skews` in the direction that still captures "
        "(smaller values) or still fails (larger ones) and run this again.")

t_ok   = min(float(s.rstrip("p")) for s in passed["DSKEW"])
t_fail = max(float(s.rstrip("p")) for s in failed["DSKEW"])
t_setup = (t_ok + t_fail) / 2

print(f"captures down to {t_ok:.0f} ps, fails at {t_fail:.0f} ps")
print(f"t_setup ~ {t_setup:.0f} ps")
"""),
    md(ANSWER + """
Quote the bracketing pair, not a single number. A setup time stated to three
figures from a coarse sweep is a number you cannot defend.
"""),

    # ---------------------------------------------------------------- L2
    md("""
---
## L2 — Clock-to-Q delay

On a cycle that *does* capture, measure from the clock's 50 % point to Q's.
"""),
    code("""
# --- L2: t_PCQ --------------------------------------------------------------
dff = sim.run_deck("spice/dff_char.spice", output="dff_char.raw")

t_clk = crossing(dff, "cl", VDD/2, rising=True, n=1)
t_q   = crossing(dff, "q",  VDD/2, rising=True, n=1, after=t_clk)
t_pcq = t_q - t_clk
print(f"t_PCQ = {t_pcq*1e12:.0f} ps")

plot.transient(dff, ["cl", "data", "q"])
plt.title("L2  Flip-flop capture"); plt.show()
"""),
    md(ANSWER),

    # ---------------------------------------------------------------- L3
    md("""
---
## L3 — Two flip-flops and four inverters

The path is `DFF1 -> inv -> inv -> inv -> inv -> DFF2`, both flip-flops on the
same clock. The maximum clock frequency follows from the max-delay constraint:

$$f_{max} = \\frac{1}{t_{PCQ} + t_{logic} + t_{setup}}$$
"""),
    code("""
# --- L3: logic delay through the four inverters -----------------------------
chain = sim.run_deck("spice/dff_chain.spice", output="dff_chain.raw")

t_q1 = crossing(chain, "q1", VDD/2, rising=True, n=1)
t_d2 = crossing(chain, "d2", VDD/2, rising=True, n=1, after=t_q1)
t_logic = t_d2 - t_q1
print(f"t_logic = {t_logic*1e12:.0f} ps  (rising)")

plot.transient(chain, ["cl", "q1", "d2", "q2"])
plt.title("L3  Flip-flop to flip-flop through four inverters"); plt.show()
"""),
    code("""
# --- L3: predicted maximum clock frequency ----------------------------------
t_period = t_pcq + t_logic + t_setup * 1e-12
f_max = 1 / t_period

print(f"t_PCQ    = {t_pcq*1e12:8.0f} ps")
print(f"t_logic  = {t_logic*1e12:8.0f} ps")
print(f"t_setup  = {t_setup:8.0f} ps")
print(f"-------------------------------")
print(f"period   = {t_period*1e12:8.0f} ps")
print(f"f_max    = {f_max/1e6:8.0f} MHz")
"""),
    code("""
# --- L3: now find it experimentally -----------------------------------------
# Shorten the clock period until the second stage stops tracking the first.
# Each point is a 200 ns transient through two flip-flops, so keep the list
# short: bracket the calculated f_max above and add points until the answer
# stops moving, rather than sweeping a fine grid from the start.
periods = ["10n", "4n", "2.5n", "2n"]

# What fails is not that q2 holds the wrong value at some instant -- q2 always
# lags q1 by a full clock cycle, so comparing the two at the same moment only
# measures that lag. What fails is that q2 stops changing at all, because DFF2
# never gets a settled input in time to capture. So measure the swing.
def swing(w, sig, after=60e-9):
    return float(np.ptp(w[sig][w.x > after]))

chain_sweep = sim.sweep_param(
    "spice/dff_chain.spice", "TCLK", periods,
    lambda w: {"q1_swing": swing(w, "q1"), "q2_swing": swing(w, "q2")},
    output="dff_chain.raw")

# q1 is driven straight from the source, so it keeps swinging whatever the
# clock does; it is the control that tells you the deck still works at all.
chain_sweep["captures"] = chain_sweep["q2_swing"] > 0.9 * VDD
print(chain_sweep.to_string(index=False))
"""),
    md(ANSWER + """
Compare the calculated $f_{max}$ against the simulated one, and say which of
the three terms you trust least and why.
"""),

    # ---------------------------------------------------------------- L5
    md("""
---
## L5 — Write, then read

Build your cell in the DUT of `xschem/sram6t_tb.sch` and press
**Netlist & Simulate**, which writes `sram6t_tb.raw`.

The stimulus writes a 1 between 10 and 19 ns, precharges again, then reads
from 29 ns.
"""),
    code("""
# --- L5: load the result ----------------------------------------------------
# From the schematic testbench. If you ran the deck instead, use:
#     s = sim.run_deck("spice/sram6t.spice", output="sram6t.raw")
s = sim.raw("sram6t_tb.raw")

print(f"after the write:  a = {value_at(s, 'a', 19e-9):.3f} V     "
      f"a_b = {value_at(s, 'a_b', 19e-9):.3f} V")
"""),
    code("""
# --- L5: the two numbers this lab is about ----------------------------------
# Read disturb: after writing a 1, a is high and a_b is low, so a_b is the
# node at risk of being dragged up through its access device during the read.
read_window = s.x >= 29.1e-9
disturb = float(np.max(s["a_b"][read_window]))

# Read time: word line rising to 200 mV of bit-line separation. Take the
# SECOND word rise -- the first belongs to the write, where the driver
# separates the bit lines for an entirely different reason.
t_word = crossing(s, "word", VDD/2, rising=True, n=2)
dbit = s["bit"] - s["bit_b"]
i = np.flatnonzero((s.x > t_word) & (np.abs(dbit) > 0.2))[0]
t_read = float(s.x[i]) - t_word

print(f"read disturb = {disturb*1e3:.0f} mV   (limit 300 mV)")
print(f"read time    = {t_read*1e12:.0f} ps")
"""),
    code("""
# --- L5: waveforms ----------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(9, 6))
for sig in ("pre", "word", "write"):
    ax1.plot(s.x * 1e9, s[sig], label=sig)
ax1.set_ylabel("control (V)"); ax1.legend(loc="upper right"); ax1.grid(alpha=0.3)

for sig in ("bit", "bit_b", "a", "a_b"):
    ax2.plot(s.x * 1e9, s[sig], label=sig)
ax2.axhline(0.3, ls=":", c="r", lw=1)
ax2.set_xlabel("time (ns)"); ax2.set_ylabel("cell (V)")
ax2.legend(loc="upper right"); ax2.grid(alpha=0.3)
fig.suptitle("L5  Write a 1, then read it back"); plt.show()
"""),
    md(ANSWER + """
Report the read time and the read disturb, and say what sets each of them.
"""),

    # ---------------------------------------------------------------- L6/L7
    md("""
---
## L6 — Break read stability

Shrink the driver NMOS so that $W_{N1}$ falls well below $2.7\\,W_{N2}$.
"""),
    code("""
# --- L6: sweep the driver width through the read-stability boundary ---------
drivers = ["2.0", "1.2", "0.9", "0.6"]

read_fail = sim.sweep_param(
    "spice/sram6t.spice", "WDRV", drivers,
    lambda w: {"disturb_mV": 1e3 * float(np.max(w["a_b"][w.x >= 29.1e-9]))},
    output="sram6t.raw")

read_fail["ratio_needed"] = 2.7 * W_access
read_fail["condition"] = [
    "OK" if float(d) >= 2.7 * W_access else "VIOLATED" for d in drivers]
print(read_fail.to_string(index=False))
"""),
    code("""
# --- L6: the failing case, plotted against the working one ------------------
bad = sim.run_deck("spice/sram6t_read_fail.spice", output="sram6t_read_fail.raw")

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(s.x * 1e9,   s["a_b"],   label="a_b, W_driver = 2.0")
ax.plot(bad.x * 1e9, bad["a_b"], label="a_b, W_driver = 0.6")
ax.axhline(0.3, ls=":", c="r", lw=1, label="300 mV limit")
ax.set_xlim(28, 40); ax.set_xlabel("time (ns)"); ax.set_ylabel("V")
ax.legend(); ax.grid(alpha=0.3)
plt.title("L6  Read disturb with the driver weakened"); plt.show()
"""),
    md(ANSWER + """
Compare against your P2 answer: is the device you named the one that mattered?
"""),

    md("""
---
## L7 — Break write stability

Grow the load PMOS and shrink the access NMOS.

Note that violating the inequality by a little is not enough — a PMOS is
roughly three times weaker than an NMOS of the same width, so the stated
1.2 ratio carries real margin. Both devices have to move.
"""),
    code("""
# --- L7: the write that does not take ---------------------------------------
wf = sim.run_deck("spice/sram6t_write_fail.spice", output="sram6t_write_fail.raw")

print(f"working cell, a after the write: {value_at(s,  'a', 19e-9):.3f} V")
print(f"broken  cell, a after the write: {value_at(wf, 'a', 19e-9):.3f} V")

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(s.x * 1e9,  s["a"],  label="a, sized correctly")
ax.plot(wf.x * 1e9, wf["a"], label="a, write condition violated")
ax.set_xlabel("time (ns)"); ax.set_ylabel("V"); ax.legend(); ax.grid(alpha=0.3)
plt.title("L7  The write never takes"); plt.show()
"""),
    md(ANSWER + """
Also say how far past the inequality you had to go before the write actually
failed, and why that margin exists.
"""),

    # ---------------------------------------------------------------- summary
    md("""
---
## Summary

Fill this in from the cells above.

| Quantity | Value |
|---|---|
| $t_{setup}$ (bracketing pair) | |
| $t_{PCQ}$ | |
| $t_{logic}$ | |
| $f_{max}$, calculated | |
| $f_{max}$, simulated | |
| Read time | |
| Read disturb | |
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
