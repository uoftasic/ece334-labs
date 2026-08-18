"""Shared helpers for generating XSchem schematics and symbols.

Anything with more than a handful of instances is generated rather than drawn.
A schematic wired by name is netlisted, simulated, and silently wrong when a
terminal coordinate is off by ten units; declaring the pin offsets once and
computing every position from them removes that whole class of mistake, and
makes the result reviewable as a diff.

Two rules encoded here, both learned the hard way:

* A wire's ``lab=`` field is only XSchem's cached display value. It does NOT
  name the net. A wire takes its name from a ``lab_pin`` or a port sitting on
  it; a wire with neither is netlisted as ``net1``, ``net2``, ... Every wire
  drawn through :func:`wire` should be paired with a :func:`name` or a port.
* A ``gnd`` symbol and a ``lab_pin`` cannot share a point. XSchem keeps the
  ``lab_pin`` name and the ground connection is silently lost, which leaves the
  supplies floating. Use a 0 V source instead.
"""
import os

HDR = "v {xschem version=3.4.8 file_version=1.2}\nG {}\nK {}\nV {}\nS {}\nE {}\n"

# Terminal offsets from the instance origin, rotation 0, for both sky130
# 1.8 V devices. Read straight out of the B lines of the PDK symbols.
#   nfet: D (20,-30)  G (-20,0)  S (20,30)  B (20,0)
#   pfet: S (20,-30)  G (-20,0)  D (20,30)  B (20,0)
# Both put the terminal that normally faces the supply rail at the top for a
# PMOS and at the bottom for an NMOS, so a PMOS above an NMOS needs no flipping.
TOP, GATE, BOT, BODY = (20, -30), (-20, 0), (20, 30), (20, 0)


def dev(kind, name, x, y, w, l, top, gate, bot, body):
    """One transistor. A terminal given as None is left for a wire to reach;
    any other terminal gets a lab_pin dropped exactly on it, which is how
    XSchem connects by name."""
    # model= is the BARE name: the symbol prepends the sky130_fd_pr__ prefix
    # itself, and passing the full name yields sky130_fd_pr__sky130_fd_pr__nfet.
    out = ['C {sky130_fd_pr/%s_01v8.sym} %d %d 0 0 {name=%s W=%s L=%s nf=1 mult=1 '
           'model=%s_01v8 spiceprefix=X}' % (kind, x, y, name, w, l, kind)]
    for (dx, dy), net in ((TOP, top), (GATE, gate), (BOT, bot), (BODY, body)):
        if net is None:
            continue
        out.append('C {devices/lab_pin.sym} %d %d 0 0 {name=l_%s_%s lab=%s}'
                   % (x + dx, y + dy, name, net, net))
    return out


def wire(x1, y1, x2, y2, net):
    """A wire segment. The lab= field here is only XSchem's cached display
    value -- it does NOT name the net. A wire takes its name from a lab_pin or
    a port sitting on it, and a wire with neither is netlisted as net1, net2,
    ... So every wire this file draws is paired with a name() below."""
    return 'N %d %d %d %d {lab=%s}' % (x1, y1, x2, y2, net)


def name(x, y, net, tag):
    """Name the wire passing through (x, y)."""
    return ('C {devices/lab_pin.sym} %d %d 0 0 {name=l_%s lab=%s}' % (x, y, tag, net))


# Rail heights. Every inverter drops a single vertical wire from its PMOS body
# pin up to VDD and from its NMOS body pin down to VSS; because the body pin
# and the source pin share a column, one wire carries both.
VDD_Y, VSS_Y, DEV_Y = -260, 260, 120


def inverter(pname, nname, x, vin, vout, wp, wn, l="0.5", label_rails=True):
    """A CMOS inverter drawn the way one is drawn by hand: PMOS above NMOS,
    a supply wire out of each, and the output as the column between them."""
    out = dev("pfet", pname, x, -DEV_Y, wp, l, None, vin, None, None)
    out += dev("nfet", nname, x, DEV_Y, wn, l, None, vin, None, None)
    out += [wire(x + 20, -DEV_Y, x + 20, VDD_Y, "vdd"),   # body + source
            wire(x + 20, DEV_Y, x + 20, VSS_Y, "vss"),
            wire(x + 20, -DEV_Y + 30, x + 20, DEV_Y - 30, vout),
            name(x + 20, 0, vout, "%s_out" % nname)]
    if label_rails:
        out += [name(x + 20, VDD_Y, "vdd", "%s_v" % pname),
                name(x + 20, VSS_Y, "vss", "%s_g" % nname)]
    return out


def ports(pins):
    """ipin/opin/iopin placements. Their order here sets the .subckt port
    order, which must match the order of the B lines in the symbol."""
    out = []
    for i, (name, direction, x, y) in enumerate(pins):
        sym = {"in": "ipin", "out": "opin", "inout": "iopin"}[direction]
        out.append('C {devices/%s.sym} %d %d 0 0 {name=p%d lab=%s}'
                   % (sym, x, y, i + 1, name))
    return out


def symbol(cellname, label, pins, half_w=80, half_h=90):
    """A rectangular subcircuit symbol. Pin B-line order follows `pins`, which
    is the same list the schematic's ports are generated from."""
    L = ['v {xschem version=3.4.8 file_version=1.2}',
         'G {type=subcircuit', 'format="@name @pinlist @symname"',
         'template="name=x1"', '}', 'V {}', 'S {}', 'E {}']
    L += ['L 4 %d %d %d %d {}' % c for c in (
        (-half_w, -half_h, half_w, -half_h), (half_w, -half_h, half_w, half_h),
        (half_w, half_h, -half_w, half_h), (-half_w, half_h, -half_w, -half_h))]
    B, T = [], ['T {@name} %d %d 0 0 0.3 0.3 {}' % (-half_w + 2, -half_h - 14),
                'T {%s} %d -10 0 0 0.4 0.4 {}' % (label, -len(label) * 8)]
    for name, direction, side, off in pins:
        if side == "L":
            px, py, sx, sy = -half_w - 20, off, -half_w, off
            T.append('T {%s} %d %d 0 0 0.22 0.22 {}' % (name, -half_w + 6, off - 10))
        elif side == "R":
            px, py, sx, sy = half_w + 20, off, half_w, off
            T.append('T {%s} %d %d 0 0 0.22 0.22 {}'
                     % (name, half_w - 6 - len(name) * 9, off - 10))
        elif side == "T":
            px, py, sx, sy = off, -half_h - 15, off, -half_h
            T.append('T {%s} %d %d 0 0 0.2 0.2 {}' % (name, off + 4, -half_h + 2))
        else:
            px, py, sx, sy = off, half_h + 15, off, half_h
            T.append('T {%s} %d %d 0 0 0.2 0.2 {}' % (name, off + 4, half_h - 12))
        L.append('L 4 %d %d %d %d {}' % (px, py, sx, sy))
        B.append('B 5 %.1f %.1f %.1f %.1f {name=%s dir=%s}'
                 % (px - 2.5, py - 2.5, px + 2.5, py + 2.5, name, direction))
    return "\n".join(L + B + T) + "\n"


# The repository root, used only to print tidy relative paths.
LABS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(text)
    print("wrote %s" % os.path.relpath(path, LABS))


