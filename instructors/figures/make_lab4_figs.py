"""Lab 4 figures: SRAM write/read, the two stability violations, setup time.

    python3 instructors/figures/make_lab4_figs.py <rawdir> <outdir>
"""
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from ece334lib import sim  # noqa: E402

RAW = sys.argv[1] if len(sys.argv) > 1 else "/tmp/l4"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/figs"
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"figure.dpi": 150, "font.size": 9, "axes.grid": True,
                     "grid.alpha": 0.3, "legend.frameon": False,
                     "savefig.bbox": "tight"})


def sram_panels(raw, title, outfile, note=None):
    w = sim.raw(raw)
    t = w.x * 1e9
    fig, axes = plt.subplots(3, 1, figsize=(8.6, 6.2), sharex=True)
    axes[0].plot(t, w["pre"], label="precharge")
    axes[0].plot(t, w["word"], label="word")
    axes[0].plot(t, w["write"], label="write")
    axes[0].set_ylabel("control")
    axes[1].plot(t, w["bit"], label="bit")
    axes[1].plot(t, w["bit_b"], label="bit_b")
    axes[1].set_ylabel("bit lines")
    axes[2].plot(t, w["a"], label="A")
    axes[2].plot(t, w["a_b"], label="A_b")
    axes[2].axhline(0.3, color="0.5", ls=":", lw=1)
    axes[2].text(50, 0.33, "0.3 V read-stability limit", ha="right", fontsize=8,
                 color="0.35")
    axes[2].set_ylabel("cell nodes")
    for ax in axes:
        ax.set_ylim(-0.15, 2.05)
        ax.legend(loc="upper right", ncol=3, fontsize=8)
        ax.axvspan(10, 19, color="0.92", zorder=0)
        ax.axvspan(29, 50, color="0.96", zorder=0)
    axes[0].set_title(title)
    axes[0].text(14.5, 1.9, "WRITE '1'", ha="center", fontsize=8, color="0.3")
    axes[0].text(39, 1.9, "READ", ha="center", fontsize=8, color="0.3")
    if note:
        axes[2].text(0.015, 0.62, note, transform=axes[2].transAxes, fontsize=9,
                     family="monospace", color="0.15")
    axes[-1].set_xlabel("time (ns)")
    axes[-1].set_xlim(0, 50)
    fig.savefig(os.path.join(OUT, outfile))
    plt.close(fig)
    print("wrote", outfile)


sram_panels(f"{RAW}/sram6t.raw",
            "L5  6T SRAM, working cell: write a 1, then read it back",
            "L4-01-sram-nominal.png",
            "A reaches 1.8 V on the write.\nA_b peaks at 144 mV during the read.")
sram_panels(f"{RAW}/sram6t_read_fail.raw",
            "L6  Read stability violated: driver 0.6 instead of 2.0",
            "L4-02-sram-read-fail.png",
            "A_b is dragged to 351 mV during\nthe read, past the 300 mV limit.")
sram_panels(f"{RAW}/sram6t_write_fail.raw",
            "L7  Write stability violated: load 6.0, access 0.36",
            "L4-03-sram-write-fail.png",
            "The write never takes: A stays\nat 0.075 V instead of 1.8 V.")

# --- setup time -------------------------------------------------------------
skews = [3000, 2000, 1500, 1000, 800, 600, 500, 400, 300, 290, 280, 260, 240,
         220, 210, 200, 100]
captured = [s >= 240 for s in skews]
fig, ax = plt.subplots(figsize=(7.2, 3.6))
ax.plot([s for s, c in zip(skews, captured) if c],
        [1.8] * sum(captured), "o", ms=7, label="captured")
ax.plot([s for s, c in zip(skews, captured) if not c],
        [0.0] * (len(skews) - sum(captured)), "x", ms=9, label="failed")
ax.axvspan(220, 240, color="0.88", zorder=0)
ax.text(230, 0.9, " $t_{setup}$ lies here\n ≈ 230 ps", fontsize=9, ha="left")
ax.set_xscale("log")
ax.set_xlabel("data edge placed this many ps before the clock edge")
ax.set_ylabel("Q after the edge (V)")
ax.set_ylim(-0.3, 2.1)
ax.set_title("L1  Setup time: sweep the data edge toward the clock until capture fails")
ax.legend(loc="center left")
fig.savefig(os.path.join(OUT, "L4-04-setup-time.png"))
plt.close(fig)
print("wrote L4-04-setup-time.png")
