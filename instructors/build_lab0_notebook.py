"""Generate lab0_setup/lab0.ipynb -- the onboarding notebook.

Labs 1 to 4 are all reported through a notebook, and none of them stop to
explain the notebook itself. This one does, in the first session, while a
demonstrator is in the room. It is not marked.

It is deliberately self-contained: every cell runs against a deck that ships
with the lab, so a student whose schematic is not finished can still get to the
end and see what the workflow feels like.

    python3 instructors/build_lab0_notebook.py lab0_setup/lab0.ipynb
"""
import json
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "lab0_setup/lab0.ipynb"


def md(text):
    return {"cell_type": "markdown", "metadata": {},
            "source": text.strip("\n").splitlines(True)}


def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": text.strip("\n").splitlines(True)}


cells = [
    md("""
# ECE334 Lab 0 — the notebook

**Name:**
**Student number:**

Labs 1 to 4 are reported through a notebook like this one. This lab is where
you learn to drive it. Nothing here is marked. Work through it in the session,
with a demonstrator in the room, so that the first time something breaks is not
the night before Lab 1 is due.

Manual: <https://uoftasic.github.io/ece334-docs/labs/lab0/>

## How a notebook works

A notebook is a column of **cells**. A grey cell holds Python; a plain one holds
text you write.

| Action | Key |
|---|---|
| Run the current cell and move on | `Shift-Enter` |
| Run the current cell and stay | `Ctrl-Enter` |
| Add a cell below | `Esc` then `b` |
| Delete a cell | `Esc` then `d` `d` |
| Interrupt a cell that is taking too long | `Esc` then `i` `i` |

Two things about notebooks catch people out every year:

**Order matters, and it is the order you *ran* them, not the order they appear
in.** A variable defined in a cell exists only after that cell has run. If you
skip a cell and the next one says `NameError`, that is why.

**The kernel keeps everything until you restart it.** If you edit a cell and
re-run only that one, the old values from other cells are still there. When
results stop making sense, use **Kernel → Restart Kernel and Run All Cells**.
Do that once before you submit, always: it proves your notebook runs top to
bottom on someone else's machine.
"""),

    md("""
---
## 1. Does everything work?

Run the cell below. It checks the four things the rest of the term depends on.
If any line says **MISSING**, fix it now — ask a demonstrator. Nearly always the
answer is that `.designinit` was not sourced in the terminal you started
JupyterLab from:

```bash
. /foss/designs/common/.designinit
cd /foss/designs/lab0_setup
jlab
```
"""),
    code("""
import os
import shutil

ok = True

def check(label, condition, hint):
    global ok
    print(f"{'ok     ' if condition else 'MISSING'}  {label}")
    if not condition:
        ok = False
        print(f"         -> {hint}")

check("ngspice on PATH", shutil.which("ngspice") is not None,
      "source /foss/designs/common/.designinit, then restart the kernel")
check("xschem on PATH", shutil.which("xschem") is not None,
      "source /foss/designs/common/.designinit, then restart the kernel")
check("PDK_ROOT is set", bool(os.environ.get("PDK_ROOT")),
      "source /foss/designs/common/.designinit, then restart the kernel")

try:
    from ece334lib import measure, plot, sim, waves
    check("ece334lib imports", True, "")
except ImportError as exc:
    check("ece334lib imports", False, f"{exc}; check PYTHONPATH in .designinit")

print()
print("all good -- carry on" if ok else "fix the lines above before continuing")
"""),

    md("""
!!! note "If you fixed something, restart the kernel"
    The environment is read when the kernel starts. Sourcing `.designinit`
    afterwards does not reach a kernel that is already running. **Kernel →
    Restart Kernel**, then run the cell again.
"""),

    md("""
---
## 2. Your first simulation

`spice/inv_demo.spice` is the CMOS inverter you draw in L1.3, written out as a
plain deck. Open it in the file browser and read it — every testbench in this
course has the same five parts: models, supplies, stimulus, circuit, analysis.

`sim.run_deck` runs ngspice on a deck and hands you back the results.
"""),
    code("""
import numpy as np
import matplotlib.pyplot as plt

from ece334lib import measure, plot, sim

VDD = 1.8
%matplotlib inline

# run_deck(deck, output=...) -- `output` is the file the deck's .control block
# writes. Look at the `write inv_demo.raw ...` line in the deck.
inv = sim.run_deck("spice/inv_demo.spice", output="inv_demo.raw")
print(inv)
"""),

    md("""
That printed a `Wave`: a set of named signals sharing one time axis. Get a
signal by name, the way you would from a dictionary. Names are forgiving —
`inv["out"]`, `inv["v(out)"]` and `inv["V(OUT)"]` all work.
"""),
    code("""
print("signals available:", inv.names)
print("time runs from", inv.x[0], "to", inv.x[-1], "seconds")
print("out starts at %.3f V and ends at %.3f V" % (inv["out"][0], inv["out"][-1]))
"""),

    md("""
---
## 3. Plotting

`plot.transient` draws named signals against time with the axes already
labelled. It is a convenience, not a requirement — `inv.x` and `inv["out"]` are
plain numpy arrays, so anything matplotlib can do, you can do.
"""),
    code("""
plot.transient(inv, ["in", "out"])
plt.title("Lab 0 -- CMOS inverter, 0.2 pF load")
plt.show()
"""),
    code("""
# The same thing by hand, to show there is nothing hidden in plot.transient.
fig, ax = plt.subplots(figsize=(9, 3))
ax.plot(inv.x * 1e9, inv["in"], label="in")
ax.plot(inv.x * 1e9, inv["out"], label="out")
ax.set_xlabel("time (ns)"); ax.set_ylabel("V")
ax.legend(); ax.grid(alpha=0.3)
plt.show()
"""),

    md("""
---
## 4. Measuring

Reading a number off a plot is not a measurement. `ece334lib.measure` has the
definitions this course uses, so that everyone's numbers mean the same thing.

- `edges_10_90(wave, sig, vdd)` → `(t_rise, t_fall)`, 10 % to 90 %
- `prop_delays(wave, vin, vout, vdd)` → `(t_pHL, t_pLH)`, 50 % in to 50 % out
- `noise_margins(wave, vin, vout)` → `V_M`, `NM_H`, `NM_L` from a DC sweep

Every one takes the wave and the *names* of the signals.
"""),
    code("""
t_rise, t_fall = measure.edges_10_90(inv, "out", vdd=VDD)
t_pHL, t_pLH   = measure.prop_delays(inv, "in", "out", vdd=VDD)

print(f"t_rise = {t_rise*1e12:7.1f} ps")
print(f"t_fall = {t_fall*1e12:7.1f} ps")
print(f"t_pHL  = {t_pHL*1e12:7.1f} ps")
print(f"t_pLH  = {t_pLH*1e12:7.1f} ps")
"""),
    md("""
The rise is slower than the fall even though the PMOS is three times the width
of the NMOS. Hold on to that; Lab 1 asks you to explain it.

### Try it

Change `CL` in `spice/inv_demo.spice` from `0.2p` to `1p`, save the file, and
re-run the two cells above. Note what happens to the four numbers, and whether
the change is roughly proportional. Nothing is submitted — the point is to see
that editing a deck and re-running is a two-second loop.
"""),

    md("""
---
## 5. Results from the XSchem buttons

Most of the time you will not run a deck from Python. You will press
**Netlist** and **Simulate** in XSchem, and read what they wrote.

Those land in one shared directory, `/foss/designs/.xschem/simulations`, so
`sim.raw()` takes a **bare filename** and does not care which directory you
started XSchem from.

```python
rc = sim.raw("rc_tb.raw")      # Lab 1
```

!!! warning "Firing a launcher"
    The green arrows in each testbench are **launchers**. Click the arrow once
    so it is selected, then press **`Ctrl-H`**. Ctrl-clicking one is XSchem's
    documented shortcut and it fires only if the pointer does not move between
    press and release — a few pixels of hand movement loses it, silently. The
    menubar **Netlist** and **Simulate** buttons always work.

The cell below looks for anything you have produced so far. Early in Lab 0 it
will be empty, and that is fine.
"""),
    code("""
import glob

sim_dir = sim.SIM_DIR
print("results directory:", sim_dir)
found = sorted(glob.glob(os.path.join(sim_dir, "*.raw")))
if found:
    for f in found:
        print("  ", os.path.basename(f))
    print()
    print('load one with, e.g.:  w = sim.raw("%s")' % os.path.basename(found[0]))
else:
    print("  (nothing yet -- press Netlist then Simulate in a testbench)")
"""),

    md("""
---
## 6. How a lab report is written

Labs 1 to 4 repeat one shape for every section:

1. a **hand-analysis** cell, where you compute what you expect *before* looking;
2. a **measurement** cell, which runs and measures;
3. an **answer** block, where you write the comparison.

The third is the one that carries the marks. A section with plots and no
written answer is incomplete. Practise the shape now on a question you can
already answer.

### Hand analysis

The load capacitor is charged through the PMOS and discharged through the NMOS.
Model each as a resistor and the rise and fall times are $2.2 R_{eq} C_L$. You
do not have $R_{eq}$ yet — you extract it in Lab 1 — so predict only the
**ratio** $t_{rise}/t_{fall}$, from the fact that the two devices have the same
length and widths of 3 and 1.
"""),
    code("""
# --- hand analysis -----------------------------------------------------------
# Replace this guess with your own reasoning before you run the next cell.
ratio_predicted = 1.0

print(f"predicted t_rise / t_fall = {ratio_predicted:.2f}")
"""),
    code("""
# --- measurement -------------------------------------------------------------
ratio_measured = t_rise / t_fall
print(f"measured  t_rise / t_fall = {ratio_measured:.2f}")
print(f"difference                = {100*(ratio_measured/ratio_predicted - 1):+.0f} %")
"""),
    md("""
### Your answer

*Replace this text.* What ratio did you predict, what did you measure, and what
does the gap tell you about the two devices? Three sentences is plenty.

Most people predict 1.0, reasoning that making the PMOS three times wider
cancels its three-times-lower mobility. That reasoning is sound as far as it
goes, and the measurement still comes out well above 1. So mobility and width
are not the only things setting $R_{eq}$ — name one more quantity in

$$R_{eq} = \frac{V_{DD}}{K_P\frac{W}{L}(V_{DD}-|V_t|)}$$

that differs between an NMOS and a PMOS, and say which way it pushes. You
measure it yourself in Lab 1. Being wrong for a stated reason is worth marks;
being silent is not.
"""),

    md("""
---
## 7. When a cell goes wrong

You will hit all of these. They are not signs that anything is broken.

| What you see | What it means |
|---|---|
| `NameError: name 'inv' is not defined` | You skipped the cell that defines it. Run the cells above, in order. |
| `FileNotFoundError: ... .raw` | The simulation has not been run yet, or it wrote a different filename. Check the `write` line in the deck. |
| `ngspice failed (exit 1)` | The deck has an error. The message underneath is ngspice's own — read it. |
| `could not find a valid modelname` | A `u` suffix on `W` or `L`. Write `W=1`, not `W=1u`. |
| `KeyError: signal 'foo' not found` | That name is not in the file. `wave.names` lists what is. |
| A cell hangs with `[*]` beside it | Still running. `Esc` then `i` `i` interrupts it. |

Cause one on purpose, so you recognise it later:
"""),
    code("""
try:
    inv["does_not_exist"]
except KeyError as exc:
    print("KeyError, as expected:")
    print(" ", exc)

print()
print("what this wave actually holds:", inv.names)
"""),

    md("""
---
## Before you leave

- [ ] Section 1 reports no **MISSING** lines
- [ ] Section 2 ran a simulation and printed a `Wave`
- [ ] Section 4 printed four timing numbers
- [ ] You wrote something in the answer block in section 6
- [ ] **Kernel → Restart Kernel and Run All Cells** completes with no errors

The last one is the habit worth forming. Every notebook you submit this term
should survive it.
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
