"""Generate common/xschem/dff.sch -- the transmission-gate D flip-flop.

Placing nine cells and wiring roughly forty pins by hand is where coordinate
mistakes come from, so the pin locations are declared once here and the
schematic is generated. Connections are made by net name, which is how the
other course cells connect their gates.

Topology (positive edge triggered):

    master   TG1(cl_b): data -> m1
             NOR_A(m1, setq)     -> m2
             NOR_B(m2, resetq)   -> m3
             TG2(cl):   m3 -> m1        (hold when the clock is high)
    slave    TG3(cl):   m3 -> s1
             NOR_C(s1, setq)     -> q_b
             NOR_D(q_b, resetq)  -> q
             TG4(cl_b): q  -> s1        (hold when the clock is low)

With cl low the master is transparent and m3 = data. On the rising edge TG1
opens, TG2 closes to hold the master, and TG3 passes m3 into the slave, so q
takes the value data had just before the edge.

setq forces q high, resetq forces q low; both act through the NOR gates.

    python3 instructors/build_dff.py common/xschem/dff.sch
"""
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "common/xschem/dff.sch"

# Pin offsets, taken from each symbol's B lines.
TG = {"in": (-50, 0), "out": (50, 0), "ctrl": (0, -60), "vdd": (0, -85), "vss": (0, 85)}
NOR = {"a": (-50, -20), "b": (-50, 20), "out": (70, 0), "vdd": (-10, -58), "vss": (-10, 58)}
INV = {"in": (-50, 0), "out": (50, 0), "vdd": (0, -40), "vss": (0, 40)}

# instance name, symbol, pin map, origin, {pin: net}
INSTANCES = [
    ("xclk", "inv.sym",   INV, (-820, 300), {"in": "cl",   "out": "cl_b"}),
    ("xtg1", "tgate.sym", TG,  (-560,   0), {"in": "data", "out": "m1", "ctrl": "cl_b"}),
    ("xna",  "nor2.sym",  NOR, (-360,   0), {"a": "m1",    "b": "setq",   "out": "m2"}),
    ("xnb",  "nor2.sym",  NOR, (-140,   0), {"a": "m2",    "b": "resetq", "out": "m3"}),
    ("xtg2", "tgate.sym", TG,  (-360, 240), {"in": "m3",   "out": "m1", "ctrl": "cl"}),
    ("xtg3", "tgate.sym", TG,  (  90,   0), {"in": "m3",   "out": "s1", "ctrl": "cl"}),
    ("xnc",  "nor2.sym",  NOR, ( 290,   0), {"a": "s1",    "b": "setq",   "out": "q_b"}),
    ("xnd",  "nor2.sym",  NOR, ( 510,   0), {"a": "q_b",   "b": "resetq", "out": "q"}),
    ("xtg4", "tgate.sym", TG,  ( 290, 240), {"in": "q",    "out": "s1", "ctrl": "cl_b"}),
]

# Port order here sets the .subckt port order, and must match the B-line order
# in dff.sym or instances wire to the wrong nets.
PORTS = [
    ("ipin",  "data",   (-980,  -60)),
    ("ipin",  "cl",     (-980,  -20)),
    ("ipin",  "setq",   (-980,   20)),
    ("ipin",  "resetq", (-980,   60)),
    ("opin",  "q",      ( 720,  -40)),
    ("opin",  "q_b",    ( 720,   40)),
    ("iopin", "vdd",    (-980, -140)),
    ("iopin", "vss",    (-980, -100)),
]

lines = [
    "v {xschem version=3.4.8 file_version=1.2}",
    "G {}", "V {}", "S {}", "E {}",
    "T {Transmission-gate D flip-flop} -980 -320 0 0 0.45 0.45 {}",
    "T {Master-slave. Each latch is two NOR gates in a loop, closed by a",
    "transmission gate when the other gate is open.",
    "",
    "cl low  : TG1 passes data into the master; the slave holds through TG4.",
    "cl high : TG1 opens, TG2 closes the master loop, TG3 passes the stored",
    "          value into the slave. q updates on the rising edge.",
    "",
    "setq forces q high and resetq forces q low, both through the NOR gates.",
    "Connections are made by net name.} -980 -284 0 0 0.28 0.28 {}",
]

for name, sym, pins, (ox, oy), nets in INSTANCES:
    lines.append(f"C {{{sym}}} {ox} {oy} 0 0 {{name={name}}}")
    for pin, (dx, dy) in pins.items():
        net = nets.get(pin, pin)          # vdd/vss default to their own name
        lines.append(
            f"C {{devices/lab_pin.sym}} {ox+dx} {oy+dy} 0 0 "
            f"{{name=l_{name}_{pin} lab={net}}}"
        )

for kind, net, (x, y) in PORTS:
    lines.append(f"C {{devices/{kind}.sym}} {x} {y} 0 0 {{name=p_{net} lab={net}}}")

with open(OUT, "w") as fh:
    fh.write("\n".join(lines) + "\n")
print(f"wrote {OUT}: {len(INSTANCES)} instances, {len(PORTS)} ports")
