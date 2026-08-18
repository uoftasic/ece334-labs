"""Generate lab2_layout/lab2.ipynb. See build_lab1_notebook.py for the shape.

Lab 2 differs from the others: most of its evidence is tool output -- a DRC
count, an extracted netlist, an LVS verdict -- rather than waveforms. The
notebook therefore captures those artefacts as text before it gets to the one
measurement section, so the report holds everything the lab produced.

    python3 instructors/build_lab2_notebook.py lab2_layout/lab2.ipynb
"""
import json
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "lab2_layout/lab2.ipynb"


def md(text):
    return {"cell_type": "markdown", "metadata": {},
            "source": text.strip("\n").splitlines(True)}


def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": text.strip("\n").splitlines(True)}


ANSWER = """
### Your answer

*Replace this text.*
"""

cells = [
    md("""
# ECE334 Lab 2 — NAND2 layout, DRC, LVS and extraction

**Name:**
**Student number:**
**Date:**

This notebook is your lab report. Its sections match the manual:
<https://uoftasic.github.io/ece334-docs/labs/lab2/>

Unlike the other labs, most of what Lab 2 produces is tool output rather than
waveforms. The cells below capture that output into the report, so run them
after you have finished in Magic.

Before you start, in the container terminal:

```bash
. /foss/designs/common/.designinit
cd /foss/designs/lab2_layout
jlab
```
"""),
    code("""
import os
import re
import subprocess

import numpy as np
import matplotlib.pyplot as plt

from ece334lib import measure, plot, sim

VDD = 1.8
%matplotlib inline

LAB = "/foss/designs/lab2_layout"


def show(path, head=None):
    \"\"\"Print a file the tools produced, so it lands in the report.\"\"\"
    if not os.path.exists(path):
        print(f"MISSING: {path}\\n"
              f"Produce it in Magic first -- see the manual's L4.")
        return None
    text = open(path).read()
    lines = text.splitlines()
    print("\\n".join(lines[:head] if head else lines))
    return text
"""),

    # ---------------------------------------------------------------- P2/P3
    md("""
---
## P2 — Stick diagram

Attach or describe your stick diagram here. Say which diffusion strip is NMOS
and which is PMOS, where each poly gate crosses, which diffusion regions are
shared, and where the taps go.

The series NMOS pair shares its middle diffusion region with no contact at all.
Say why that is legal.
"""),
    md(ANSWER),

    md("""
## P3 — Predict the parasitics

Before you measure anything: does layout parasitic capacitance matter more when
the gate drives a **large** load or a **small** one? Why?

Answer here, before running L6.
"""),
    md(ANSWER),

    # ---------------------------------------------------------------- L3
    md("""
---
## L3 — DRC

Get `drc count` to zero in Magic, then record it here.
"""),
    code("""
# --- L3: DRC ----------------------------------------------------------------
# Magic reads commands on stdin even without a GUI, which is the reliable way
# to ask it a question from a script.
def magic(commands, cell="nand2"):
    script = "\\n".join(commands) + "\\nquit -noprompt\\n"
    p = subprocess.run(["magic", "-dnull", "-noconsole", "-T", "sky130A", cell],
                       input=script, capture_output=True, text=True, cwd=LAB)
    return p.stdout + p.stderr


out = magic(["drc check", "drc catchup", 'puts "DRC_COUNT=[drc list count total]"'])
m = re.search(r"DRC_COUNT=(\\d+)", out)
print(f"drc count = {m.group(1) if m else '?'}")
"""),
    md(ANSWER + """
If you had violations along the way, name one rule `drc why` reported and say
what you changed.
"""),

    # ---------------------------------------------------------------- L4
    md("""
---
## L4 — The extracted netlist

Extraction turns geometry back into a circuit. This is the answer to *what did
I actually draw*, as opposed to what you meant to draw.
"""),
    code("""
# --- L4: what the layout actually contains ----------------------------------
netlist = show(f"{LAB}/nand2.lvs.spice")
"""),
    code("""
# --- L4: check the device count and the sizes -------------------------------
if netlist:
    devices = [l for l in netlist.splitlines() if l.strip().lower().startswith("x")]
    print(f"{len(devices)} devices (expected 4)\\n")
    for d in devices:
        w = re.search(r"\\bw=([\\d.]+)", d, re.I)
        l = re.search(r"\\bl=([\\d.]+)", d, re.I)
        kind = "nfet" if "nfet" in d else "pfet"
        print(f"  {d.split()[0]:6} {kind}  W={w.group(1) if w else '?':>4}  "
              f"L={l.group(1) if l else '?'}")
"""),
    md(ANSWER + """
The internal node between the series NMOS devices has a name like `a_400_0#`.
Say where that name came from and why it does not matter.

If any `W` is not 2 or 3, your diffusion is the wrong height. Say what you
changed.
"""),

    # ---------------------------------------------------------------- L5
    md("""
---
## L5 — LVS

Netgen compares the extracted layout against the schematic. Both sides need a
`.subckt` of the same name, which is why the schematic side is netlisted
through `xschem/nand2_lvs.sch` — a wrapper that *instantiates* `nand2.sym`
rather than being the cell itself.
"""),
    code("""
# --- L5: run LVS ------------------------------------------------------------
p = subprocess.run(
    ["/foss/designs/scripts/run_lvs.sh", "nand2.lvs.spice",
     f"{LAB}/xschem/nand2_lvs.sch"],
    capture_output=True, text=True, cwd=LAB)
print(p.stdout[-3000:] or p.stderr[-3000:])
"""),
    md(ANSWER + """
State the verdict. If you hit either of the two documented failures — a pin
mismatch on a topology that otherwise matches, or a device/net count difference
— say which, and what you changed.
"""),

    # ---------------------------------------------------------------- L6
    md("""
---
## L6 — What the parasitics cost

Both netlists come from the same layout, so any difference in the measured
delay is the parasitics and nothing else.
"""),
    code("""
# --- L6: one load, both netlists --------------------------------------------
def compare_at(cload):
    \"\"\"t_pHL from the device-only netlist and from the extracted one.\"\"\"
    out = {}
    for label, inc in (("ideal", "nand2.lvs.spice"), ("extracted", "nand2.pex.spice")):
        deck = open(f"{LAB}/spice/nand2_compare.spice").read()
        deck = re.sub(r"^\\.include\\s+nand2\\.\\w+\\.spice", f".include {inc}",
                      deck, flags=re.M)
        deck = re.sub(r"^(\\.param\\s+CLOAD\\s*=\\s*)\\S+", r"\\g<1>" + str(cload),
                      deck, flags=re.M)
        path = f"{LAB}/_compare_tmp.spice"
        open(path, "w").write(deck)
        try:
            w = sim.run_deck(path, output="nand2_wave.raw", cwd=LAB)
            out[label] = measure.prop_delay(w, "a", "out", vdd=VDD)[0]
            out[label + "_wave"] = w
        finally:
            os.remove(path)
    return out

r = compare_at("0.1p")
print(f"ideal      t_pHL = {r['ideal']*1e12:.1f} ps")
print(f"extracted  t_pHL = {r['extracted']*1e12:.1f} ps")
print(f"difference        {100*(r['extracted']/r['ideal']-1):.1f} %")
"""),
    code("""
# --- L6: the two waveforms on one axis --------------------------------------
fig, ax = plt.subplots(figsize=(9, 4))
for label, style in (("ideal", "-"), ("extracted", "--")):
    w = r[label + "_wave"]
    ax.plot(w.x * 1e9, w["out"], style, label=label)
ax.set_xlabel("time (ns)"); ax.set_ylabel("out (V)")
ax.legend(); ax.grid(alpha=0.3)
plt.title("L6  Same layout, with and without its parasitics"); plt.show()
"""),
    code("""
# --- L6: sweep the load -----------------------------------------------------
# One number at one load says almost nothing. The shape of the difference
# against load is the actual result.
loads = ["0", "1f", "5f", "20f", "100f"]
rows = []
for cl in loads:
    r_cl = compare_at(cl)
    rows.append((cl, r_cl["ideal"] * 1e12, r_cl["extracted"] * 1e12))

print(f"{'C_L':>6} {'ideal':>10} {'extracted':>11} {'change':>9}")
for cl, i, e in rows:
    print(f"{cl:>6} {i:9.1f}p {e:10.1f}p {100*(e/i-1):8.1f} %")
"""),
    code("""
# --- L6: plot the contribution ----------------------------------------------
cl_f = [0, 1, 5, 20, 100]
ideal = [r[1] for r in rows]
extr  = [r[2] for r in rows]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.plot(cl_f, ideal, "o-", label="ideal")
ax1.plot(cl_f, extr,  "s--", label="extracted")
ax1.set_xlabel("$C_L$ (fF)"); ax1.set_ylabel("$t_{pHL}$ (ps)")
ax1.legend(); ax1.grid(alpha=0.3)

ax2.plot(cl_f, [100*(e/i-1) for i, e in zip(ideal, extr)], "d-")
ax2.set_xlabel("$C_L$ (fF)"); ax2.set_ylabel("parasitic contribution (%)")
ax2.grid(alpha=0.3)
fig.suptitle("L6  Parasitics are a roughly fixed additive load"); plt.show()
"""),
    md(ANSWER + """
Answer the question the sweep asks: the absolute penalty barely changes, but
its *share* falls sharply with load. Explain why, and compare against your P3
prediction.
"""),

    # ---------------------------------------------------------------- summary
    md("""
---
## Summary

| Check | Result |
|---|---|
| `drc count` | |
| Extracted device count | |
| Extracted $W_n$ / $W_p$ | |
| LVS verdict | |
| $t_{pHL}$ ideal @ 0.1 pF | |
| $t_{pHL}$ extracted @ 0.1 pF | |
| Parasitic contribution at 0 load | |
| Parasitic contribution at 0.1 pF | |
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
