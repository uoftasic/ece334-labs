"""Report every Lab 1 number the manual quotes, from the reference solutions.

Run after scripts/verify_solutions.sh has produced the .raw files:

    python3 instructors/measure_lab1.py /tmp/M
"""
import sys

import numpy as np

from ece334lib import measure, sim

VDD = 1.8
d = sys.argv[1] if len(sys.argv) > 1 else "/tmp/M"


def show(label, got, hand=None, unit="ps", scale=1e12):
    line = f"{label:<34} {got * scale:8.1f} {unit}"
    if hand is not None:
        err = 100.0 * (got * scale - hand) / hand
        line += f"   hand {hand:8.1f} {unit}   ({err:+.1f} %)"
    print(line)


print("== P1  RC divider (R1=1k, R2=2k, C1=0.7pF) ==")
rc = sim.raw(f"{d}/rc_tb.raw")
vf = float(np.max(rc["out"]))
print(f"{'final value':<34} {vf:8.3f} V    hand    1.200 V")
tr, _ = measure.edges_10_90(rc, "out", vdd=1.2)
show("t_rise (10-90 %)", tr, 1025.4)
# tau from the 10-90 % time is reference-free. Reading the 63.2 % point instead
# needs a known step origin, and the 0.2 ns input ramp makes that ambiguous.
show("tau = t_rise / ln 9", tr / np.log(9.0), 466.7)

print("\n== P2  Diode-connected devices (W=10, L=2) ==")
dn = sim.raw(f"{d}/diode_nmos.raw")
rn = measure.extract_square_law(dn["g"], dn["id"], wl=10 / 2, vmin=1.0, vmax=1.7)
print(f"{'Vtn':<34} {rn['Vt']:8.3f} V")
print(f"{'KPn':<34} {rn['KP'] * 1e6:8.1f} uA/V^2")

print("\n== P3  CMOS inverter (Wn=1, Wp=3, L=0.5, CL=0.2pF) ==")
v = sim.raw(f"{d}/inv_tb_vtc.raw")
nm = measure.noise_margins(v, "in", "out")
for k in ("VM", "VIL", "VIH", "VOL", "VOH", "NMH", "NML"):
    if k in nm:
        print(f"{k:<34} {nm[k]:8.3f} V")
t = sim.raw(f"{d}/inv_tb_tran.raw")
show("t_pd (50-50 %)", measure.prop_delay(t, "in", "out", vdd=VDD))
trr, tff = measure.edges_10_90(t, "out", vdd=VDD)
show("t_rise (10-90 %)", trr)
show("t_fall (90-10 %)", tff)

print("\n== P4  Pulse generator ==")
p = sim.raw(f"{d}/pulsegen_tb.raw")
show("pulse width (50-50 %, low-going)", measure.pulse_width(p, "out", vdd=VDD,
                                                             polarity="low"))
