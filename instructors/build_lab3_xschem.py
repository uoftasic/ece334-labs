#!/usr/bin/env python3
"""Regenerate the Lab 3 AOI21 reference solution.

The point of Lab 3 P2 is the *shape* of the network -- one NMOS in parallel
with a series pair, and the dual of that on top. A schematic wired purely by
net name is electrically correct and shows none of that, so this one is drawn
with wires: the series pairs read as series, the parallel pairs as parallel.

    python3 instructors/build_lab3_xschem.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from xschemgen import HDR, dev, name, ports, wire, write

HERE = os.path.dirname(os.path.abspath(__file__))
SOL = os.path.join(HERE, "lab3", "xschem")

# Widths from the manual's P2 table.
WA_N, WBC_N = "5", "10"      # NMOS: a alone; b and c in series
WA_P, WBC_P = "30", "30"     # PMOS: a in series with the parallel b-c pair

VDD_Y, VSS_Y = -360, 360
PMID_Y, Y_Y = -180, 0        # the two internal rails
COL_L, COL_R = 0, 300        # the two device columns
XL, XR = COL_L + 20, COL_R + 20   # their terminal columns

# (name, direction, x, y) -- this order is the .subckt port order and must
# match the B-line order in dut_aoi21.sym.
PORTS = [("a", "in", -240, -100), ("b", "in", -240, 0), ("c", "in", -240, 100),
         ("y", "out", 520, Y_Y),
         ("vdd", "inout", 170, VDD_Y), ("vss", "inout", 170, VSS_Y)]


def build():
    body = ["""T {Reference solution -- AOI21,  Y = NOT(A + B.C)

Pull-down:  a alone, in parallel with the series pair b-c.
Pull-up:    a in series with the parallel pair b-c -- the dual.

The two networks are duals of each other, which is what makes the output
always driven and never both at once.} -240 -560 0 0 0.3 0.3 {}"""]
    body += ports(PORTS)

    # ---- pull-up ---------------------------------------------------------
    # MPA carries the whole pull-up current, so it sits alone between VDD and
    # pmid. Its body and source share a column, so one wire ties both to VDD.
    body += dev("pfet", "MPA", COL_L, -280, WA_P, "0.5", None, "a", None, None)
    body += [wire(XL, -280, XL, VDD_Y, "vdd")]
    # MPB and MPC in parallel from pmid down to y. Their sources are on pmid,
    # not VDD, so their bodies have to be tied separately.
    for tag, col, gate in (("MPB", COL_L, "b"), ("MPC", COL_R, "c")):
        x = col + 20
        body += dev("pfet", tag, col, -100, WBC_P, "0.5", None, gate, None, "vdd")
        body += [wire(x, -130, x, PMID_Y, "pmid"),   # source up to pmid
                 wire(x, -70, x, Y_Y, "y")]          # drain down to the output
    body += [wire(XL, -250, XL, PMID_Y, "pmid"),     # MPA drain down to pmid
             wire(XL, PMID_Y, XR, PMID_Y, "pmid"),
             name(XL + 60, PMID_Y, "pmid", "pmid")]

    # ---- pull-down -------------------------------------------------------
    # MNA on its own from y to VSS; body and source share a column again.
    body += dev("nfet", "MNA", COL_L, 100, WA_N, "0.5", None, "a", None, None)
    body += [wire(XL, 70, XL, Y_Y, "y"), wire(XL, 100, XL, VSS_Y, "vss")]
    # MNB above MNC in series, joined at nmid.
    body += dev("nfet", "MNB", COL_R, 100, WBC_N, "0.5", None, "b", None, "vss")
    body += dev("nfet", "MNC", COL_R, 280, WBC_N, "0.5", None, "c", None, None)
    body += [wire(XR, 70, XR, Y_Y, "y"),
             wire(XR, 130, XR, 250, "nmid"), name(XR, 190, "nmid", "nmid"),
             wire(XR, 280, XR, VSS_Y, "vss")]

    # ---- rails and the output node --------------------------------------
    body += [wire(XL, VDD_Y, XR, VDD_Y, "vdd"),
             wire(XL, VSS_Y, XR, VSS_Y, "vss"),
             wire(XL, Y_Y, 520, Y_Y, "y")]
    return HDR + "\n".join(body) + "\n"


# --------------------------------------------------------------- the tgate
# Regenerated only to lay it out with room around it. Every connection is by
# net name, exactly as before, so the netlist is unchanged -- confirm that with
# scripts/verify_solutions.sh lab3_digital lab3 after touching this.
TG_TEXT = """T {Transmission gate} -600 -380 0 0 0.4 0.4 {}
T {NMOS and PMOS in parallel. The internal inverter derives the PMOS gate
from ctrl, so one control signal opens and closes both devices.
Conducting when ctrl is high.

Wn = 3, Wp = 9. Terminals connect by net name: a transmission gate has no
fixed source, so drawing it with wires would suggest a direction it does
not have. Bodies go to the rails, never to the passed signal.} -600 -340 0 0 0.28 0.28 {}"""


def build_tgate():
    body = [TG_TEXT]
    # PMOS above, NMOS below, in the same column. Terminal order on both is
    # top / gate / bottom / body; for the PMOS the top terminal is the source
    # and for the NMOS it is the drain, which is why `out` is the top net on
    # one and the bottom net on the other.
    body += dev("pfet", "MP", 0, -160, "9", "0.5", "out", "ctrl_b", "in", "vdd")
    body += dev("nfet", "MN", 0,  160, "3", "0.5", "in", "ctrl", "out", "vss")
    # The internal inverter that derives ctrl_b. inv.sym's pins sit at
    # (-50, 0) (50, 0) (0, -40) (0, 40) relative to the instance.
    body += ['C {inv.sym} -350 300 0 0 {name=xinv}',
             name(-400, 300, "ctrl", "ci"), name(-300, 300, "ctrl_b", "cb"),
             name(-350, 260, "vdd", "iv"), name(-350, 340, "vss", "ig")]
    # The supply ports sit out at x = -900, clear of the note. They also set
    # the left edge of the bounding box that xschem's --pdf page fit uses, and
    # the note has to fall inside that box or the figure crops it.
    body += ports([("in", "in", -600, 0), ("out", "out", 600, 0),
                   ("ctrl", "in", -600, 160), ("vdd", "inout", -900, -300),
                   ("vss", "inout", -900, 300)])
    return HDR + "\n".join(body) + "\n"


COMMON = os.path.join(os.path.dirname(HERE), "common", "xschem")

if __name__ == "__main__":
    write(os.path.join(SOL, "dut_aoi21.sch"), build())
    write(os.path.join(COMMON, "tgate.sch"), build_tgate())


