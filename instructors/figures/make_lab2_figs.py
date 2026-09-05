"""Lab 2 waveform figures: ideal devices versus extracted parasitics.

    python3 instructors/figures/make_lab2_figs.py <rawdir> <outdir>

Expects nand2_wave_lvs.raw and nand2_wave_pex.raw, produced by running
spice/nand2_compare.spice once against each extracted netlist.
"""
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from ece334lib import measure, sim  # noqa: E402

VDD = 1.8
RAW = sys.argv[1] if len(sys.argv) > 1 else "/tmp/n3"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/figs"
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "figure.figsize": (7.4, 4.2), "figure.dpi": 150, "font.size": 10,
    "axes.grid": True, "grid.alpha": 0.3, "legend.frameon": False,
    "savefig.bbox": "tight",
})

ideal = sim.raw(f"{RAW}/nand2_wave_lvs.raw")
pex = sim.raw(f"{RAW}/nand2_wave_pex.raw")

fig, ax = plt.subplots()
ax.plot(ideal.x * 1e9, ideal["a"], color="0.55", lw=1.1, label="a (input)")
ax.plot(ideal.x * 1e9, ideal["out"], lw=1.9, label="out, devices only")
ax.plot(pex.x * 1e9, pex["out"], lw=1.9, ls="--", label="out, with parasitics")

t_i = measure.prop_delay(ideal, "a", "out", vdd=VDD)
t_p = measure.prop_delay(pex, "a", "out", vdd=VDD)
ax.text(0.02, 0.42,
        f"$t_{{pd}}$ ideal     = {t_i*1e12:.1f} ps\n"
        f"$t_{{pd}}$ extracted = {t_p*1e12:.1f} ps\n"
        f"difference        = {100*(t_p-t_i)/t_i:+.1f} %",
        transform=ax.transAxes, fontsize=9, family="monospace", va="center")

ax.set_xlim(0.5, 9)
ax.set_ylim(-0.1, 2.3)
ax.set_xlabel("time (ns)")
ax.set_ylabel("voltage (V)")
ax.set_title("L6  NAND2 switching, before and after parasitic extraction "
             "($C_L$ = 0.1 pF)")
ax.legend(loc="upper right", ncol=2)
fig.savefig(os.path.join(OUT, "L2-03-pex-compare.png"))
plt.close(fig)
print("wrote", os.path.join(OUT, "L2-03-pex-compare.png"))

# Where the parasitics actually matter: they add a roughly fixed delay, so their
# share of the total shrinks as the load grows.
loads = np.array([0.0, 1.0, 5.0, 20.0, 100.0])
ideal_ps = np.array([100.0, 104.0, 120.0, 177.1, 467.8])
pex_ps = np.array([106.8, 110.8, 126.7, 183.6, 474.3])   # magic 8.3.681 (image 2026.08)

fig, ax = plt.subplots()
ax.plot(loads, 100 * (pex_ps - ideal_ps) / ideal_ps, "o-", lw=1.8)
for x, y in zip(loads, 100 * (pex_ps - ideal_ps) / ideal_ps):
    ax.annotate(f"{y:.1f} %", (x, y), textcoords="offset points",
                xytext=(6, 6), fontsize=9)
ax.set_xlabel("load capacitance (fF)")
ax.set_ylabel("increase in $t_{pHL}$ from parasitics (%)")
ax.set_title("L6  The parasitics add about 6.6 ps regardless of load")
ax.set_ylim(0, 7)
fig.savefig(os.path.join(OUT, "L2-04-pex-vs-load.png"))
plt.close(fig)
print("wrote", os.path.join(OUT, "L2-04-pex-vs-load.png"))
