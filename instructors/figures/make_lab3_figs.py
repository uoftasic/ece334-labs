"""Lab 3 figures: DFF operation, AOI21 worst/best case, unit inverter.

    python3 instructors/figures/make_lab3_figs.py <rawdir> <outdir>
"""
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from ece334lib import measure, sim  # noqa: E402

VDD = 1.8
RAW = sys.argv[1] if len(sys.argv) > 1 else "/tmp/l3"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/figs"
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"figure.dpi": 150, "font.size": 9, "axes.grid": True,
                     "grid.alpha": 0.3, "legend.frameon": False,
                     "savefig.bbox": "tight"})

# --- DFF, four panels, as the handout asks for ------------------------------
d = sim.raw(f"{RAW}/dff_tb.raw")
t = d.x * 1e9
panels = [
    ("CL", [("cl", "CL"), ("x1.cl_b", r"$\overline{CL}$")]),
    ("set / reset", [("setq", "SETQ"), ("resetq", "RESETQ")]),
    ("data", [("data", "DATA")]),
    ("outputs", [("q", "Q"), ("q_b", r"$\overline{Q}$")]),
]
fig, axes = plt.subplots(4, 1, figsize=(9, 7), sharex=True)
for ax, (title, sigs) in zip(axes, panels):
    for name, lab in sigs:
        if name in d:
            ax.plot(t, d[name], lw=1.3, label=lab)
    ax.set_ylabel(title, fontsize=8)
    ax.set_ylim(-0.2, 2.0)
    ax.legend(loc="upper right", ncol=2, fontsize=8)
for x in (20, 40, 140, 220):
    for ax in axes:
        ax.axvline(x, color="0.75", ls=":", lw=0.8)
axes[0].set_title("L3  D flip-flop: capture on the rising edge, "
                  "asynchronous set at 55 ns and reset at 175 ns")
axes[-1].set_xlabel("time (ns)")
axes[-1].set_xlim(0, 250)
fig.savefig(os.path.join(OUT, "L3-01-dff-panels.png"))
plt.close(fig)
print("wrote L3-01-dff-panels.png")

# --- AOI21 worst versus best case -------------------------------------------
a = sim.raw(f"{RAW}/aoi21_cases.raw")
t = a.x * 1e9
fig, ax = plt.subplots(figsize=(7.4, 4.2))
ax.plot(t, a["yw"], lw=1.9, label="worst case (series b-c path)")
ax.plot(t, a["ybf"], lw=1.5, ls="--", label="best case fall (all paths)")
ax.plot(t, a["ybr"], lw=1.5, ls=":", label="best case rise (both PMOS)")
ax.text(0.02, 0.45,
        "worst  $t_f$ = 2078 ps   $t_r$ = 4150 ps\n"
        "best   $t_f$ = 1092 ps   $t_r$ = 3231 ps",
        transform=ax.transAxes, fontsize=9, family="monospace")
ax.set_xlabel("time (ns)")
ax.set_ylabel("$V_{out}$ (V)")
ax.set_ylim(-0.1, 2.4)
ax.set_title("L2  AOI21 at $C_L$ = 1.5 pF: input pattern sets the edge rate")
ax.legend(loc="upper right", fontsize=8)
fig.savefig(os.path.join(OUT, "L3-02-aoi21-cases.png"))
plt.close(fig)
print("wrote L3-02-aoi21-cases.png")

# --- unit inverter ----------------------------------------------------------
u = sim.raw(f"{RAW}/unit_inv.raw")
t = u.x * 1e9
tr, tf = measure.edges_10_90(u, "out", vdd=VDD)
fig, ax = plt.subplots(figsize=(7.4, 4.0))
ax.plot(t, u["in"], lw=1.2, label="$V_{in}$")
ax.plot(t, u["out"], lw=1.9, label="$V_{out}$")
ax.text(0.03, 0.5, f"$t_r$ = {tr*1e12:.0f} ps\n$t_f$ = {tf*1e12:.0f} ps",
        transform=ax.transAxes, fontsize=10)
ax.set_xlabel("time (ns)")
ax.set_ylabel("voltage (V)")
ax.set_ylim(-0.1, 2.3)
ax.set_title("L1  Unit inverter (Wn = 1, Wp = 3) at $C_L$ = 0.3 pF")
ax.legend(loc="upper right", ncol=2)
fig.savefig(os.path.join(OUT, "L3-03-unit-inv.png"))
plt.close(fig)
print("wrote L3-03-unit-inv.png")
