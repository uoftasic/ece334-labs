#!/usr/bin/env python3
"""Generate the Lab 4 XSchem tree: the 6T cell stub, its symbol, the provided
periphery cell, and the testbench.

Written as a generator rather than drawn by hand for the same reason
build_dff.py is: every connection here is made by NAME, by dropping a lab_pin
exactly on a device terminal, and a terminal coordinate that is off by ten
units produces a schematic that still netlists, still simulates, and is wired
wrongly. Declaring the pin offsets once and computing every position from them
removes that whole class of mistake.

    python3 instructors/build_lab4_xschem.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
LABS = os.path.dirname(HERE)
LAB4 = os.path.join(LABS, "lab4_sram", "xschem")
SOL = os.path.join(HERE, "lab4", "xschem")

from xschemgen import (HDR, TOP, GATE, BOT, BODY, VDD_Y, VSS_Y, DEV_Y,
                       dev, wire, name, inverter, ports, symbol, write)

# ---------------------------------------------------------------- the 6T cell
# (name, direction, symbol side, offset along that side). The ORDER of this
# list is the .subckt port order and the symbol's B-line order at once, which
# is the point of deriving both from it.
SRAM6T_PINS = [
    ("bit",   "inout", "L", -40),
    ("bit_b", "inout", "L",  40),
    ("word",  "in",    "L",   0),
    ("a",     "inout", "R", -40),
    ("a_b",   "inout", "R",  40),
    ("vdd",   "inout", "T",   0),
    ("vss",   "inout", "B",   0),
]
# Where those ports sit in the schematic. Same order, again.
SRAM6T_PORT_XY = [(-160, 120), (500, 120), (-380, 0), (-160, -120), (500, -120),
                  (170, VDD_Y), (170, VSS_Y)]

STUB_TEXT = """*** BUILD YOUR 6T SRAM CELL HERE ***

This is the cell behind the `dut_sram6t` symbol used by sram6t_tb.sch.
Six transistors, from your P1 sizing:

  P1  pfet  vdd -> a     gate a_b      load
  N1  nfet  a   -> vss   gate a_b      driver
  P2  pfet  vdd -> a_b   gate a        load
  N3  nfet  a_b -> vss   gate a        driver
  N2  nfet  bit   <-> a     gate word  access
  N4  nfet  bit_b <-> a_b   gate word  access

P1/N1 and P2/N3 are two inverters, each driving the other's input. That is
the whole storage mechanism: whichever state it is in, it holds itself there.

Your sizes must satisfy both conditions from P1:
  read  :  W(driver) >= 2.7 * W(access)
  write :  W(access) >= 1.2 * W(load)

>>> Enter W and L as UNITLESS MICRONS (W=2, L=0.5) -- do NOT add 'u'.

`a` and `a_b` are the two internal storage nodes. They are brought out as
ports so the testbench can apply the initial condition and plot them; a cell
in a real array would not expose them.

DO NOT rename the pins. The testbench and lab4.ipynb rely on the net names:
  bit  bit_b  word  a  a_b  vdd  vss"""


def build_sram6t_stub():
    body = ["T {%s} -540 -400 0 0 0.3 0.3 {}" % STUB_TEXT]
    body += ports([(n, d, x, y) for (n, d, _, _), (x, y)
                   in zip(SRAM6T_PINS, SRAM6T_PORT_XY)])
    return HDR + "\n".join(body) + "\n"


def access(name_, x, storage, bitline, w, l, label_ends=True):
    """An access transistor, drawn with its two ends carried away vertically so
    the body tap sits alone between them instead of crowded against them."""
    out = dev("nfet", name_, x, 0, w, l, None, "word", None, "vss")
    out += [wire(x + 20, -30, x + 20, -DEV_Y, storage),
            wire(x + 20, 30, x + 20, DEV_Y, bitline)]
    if label_ends:
        out += [name(x + 20, -DEV_Y, storage, "%s_st" % name_),
                name(x + 20, DEV_Y, bitline, "%s_bl" % name_)]
    return out


def build_sram6t_solution(wload="0.5", wacc="0.7", wdrv="2.0", l="0.5"):
    # The title is anchored INSIDE the geometry, not above it: xschem's --pdf
    # page fit computes its bounding box from symbols and wires only, so a
    # title floating above the drawing is silently cropped in the figure.
    body = ["""T {Reference 6T cell. Sizing from Lab 4 P1:
  read   2.0 >= 2.7 * 0.7 = 1.89   OK
  write  0.7 >= 1.2 * 0.5 = 0.60   OK} -380 -230 0 0 0.3 0.3 {}"""]
    body += ports([(n, d, x, y) for (n, d, _, _), (x, y)
                   in zip(SRAM6T_PINS, SRAM6T_PORT_XY)])
    # Cross-coupled pair: each inverter's input is the other's output. That is
    # the whole storage mechanism.
    body += inverter("P1", "N1",   0, "a_b", "a",   wload, wdrv, l, label_rails=False)
    body += inverter("P2", "N3", 300, "a",   "a_b", wload, wdrv, l, label_rails=False)
    body += access("N2", -180, "a",   "bit",   wacc, l, label_ends=False)
    body += access("N4",  480, "a_b", "bit_b", wacc, l, label_ends=False)
    # The two supply rails, joining the drops from both inverters.
    body += [wire(20, VDD_Y, 320, VDD_Y, "vdd"),
             wire(20, VSS_Y, 320, VSS_Y, "vss")]
    return HDR + "\n".join(body) + "\n"


# ------------------------------------------------------------- the periphery
PERIPH_PINS = [
    ("pre",   "in",    "L", -40),
    ("write", "in",    "L",   0),
    ("data",  "in",    "L",  40),
    ("bit",   "inout", "R", -40),
    ("bit_b", "inout", "R",  40),
    ("vdd",   "inout", "T",   0),
    ("vss",   "inout", "B",   0),
]
PERIPH_PORT_XY = [(-300, -40), (-300, 0), (-300, 40), (500, 0), (1320, 0),
                  (570, VDD_Y), (570, VSS_Y)]


def build_periph(wper="8.0", l="0.5"):
    """Precharge devices and write drivers. Provided built: the design
    exercise in this lab is the six cell transistors, not this."""
    wn = "%.4g" % (float(wper) / 3.0)   # an NMOS matched to a PMOS of W=wper
    body = ["""T {SRAM periphery -- provided, already built.

Precharge:     `pre` high drives both bit lines to VDD through P3 and P4.
Write drivers: with `write` high, N5/N7 pull `bit` down when data is 0, and
               N6/N8 pull `bit_b` down when data is 1. Only one side pulls at
               a time, which is what makes the write directional.

Press `e` with this symbol selected to look inside it.} -300 -560 0 0 0.3 0.3 {}"""]
    body += ports([(n, d, x, y) for (n, d, _, _), (x, y)
                   in zip(PERIPH_PINS, PERIPH_PORT_XY)])

    # Local inverters generating the active-low precharge and the data
    # complement. These name their own supply drops, so the rails below are
    # drawn for the reader rather than for connectivity.
    body += inverter("PIP", "PIN",   0, "pre",  "pre_b",  wper, wn, l)
    body += inverter("PDP", "PDN", 300, "data", "data_b", wper, wn, l)

    # One bit-line column per side: the precharge pull-up above, the two-high
    # write-driver stack below, meeting on the bit line at y = 0.
    for tag_p, tag_a, tag_b, col, bl, dat in (
            ("P3", "N5", "N7",  700, "bit",   "data_b"),
            ("P4", "N6", "N8", 1100, "bit_b", "data")):
        x = col + 20
        mid = tag_a.lower() + "d"          # n5d / n6d, the series-pair midpoint
        body += dev("pfet", tag_p, col, -DEV_Y, wper, l, None, "pre_b", None, None)
        body += [wire(x, -DEV_Y, x, VDD_Y, "vdd"),      # body + source to VDD
                 wire(x, -DEV_Y + 30, x, 0, bl),        # drain down to the bit line
                 name(x, VDD_Y, "vdd", "%s_v" % tag_p)]
        # N5/N6 sit between the bit line and the midpoint, so their body pin is
        # boxed in by the two terminals and has to be tied by name.
        body += dev("nfet", tag_a, col, 60, wper, l, None, "write", None, "vss")
        body += dev("nfet", tag_b, col, 190, wper, l, None, dat, None, None)
        body += [wire(x, 30, x, 0, bl),
                 wire(x, 90, x, 160, mid), name(x, 125, mid, mid),
                 wire(x, 190, x, VSS_Y, "vss"),
                 name(x, VSS_Y, "vss", "%s_g" % tag_b)]

    # The bit lines run out sideways, in opposite directions, so the two
    # columns never cross.
    body += [wire(720, 0, 500, 0, "bit"), wire(1120, 0, 1320, 0, "bit_b")]
    # Rails, drawn so the supplies read as rails rather than as scattered labels.
    body += [wire(20, VDD_Y, 1120, VDD_Y, "vdd"),
             wire(20, VSS_Y, 1120, VSS_Y, "vss")]
    return HDR + "\n".join(body) + "\n"


# -------------------------------------------------------------- the testbench
# Pin coordinates on a symbol built by symbol() with half_w=80, half_h=90.
SYM_L, SYM_R, SYM_T, SYM_B = -100, 100, -105, 105


def hookup(inst_x, inst_y, pins, nets, tag):
    """Drop a lab_pin on each pin of a placed symbol, naming the net there."""
    out = []
    for (name, _, side, off) in pins:
        px, py = {"L": (SYM_L, off), "R": (SYM_R, off),
                  "T": (off, SYM_T), "B": (off, SYM_B)}[side]
        out.append('C {devices/lab_pin.sym} %d %d 0 0 {name=l_%s_%s lab=%s}'
                   % (inst_x + px, inst_y + py, tag, name, nets[name]))
    return out


def vsource(name, x, y, value, net):
    """A source with its top terminal on `net` and its bottom on ground."""
    return ['C {devices/vsource.sym} %d %d 0 0 {name=%s value="%s"}' % (x, y, name, value),
            'C {devices/lab_pin.sym} %d %d 0 0 {name=l_%s lab=%s}' % (x, y - 30, name, net),
            'C {devices/gnd.sym} %d %d 0 0 {name=g_%s lab=0}' % (x, y + 30, name)]


def cap(name, x, y, value, net):
    return ['C {devices/capa.sym} %d %d 0 0 {name=%s value=%s}' % (x, y, name, value),
            'C {devices/lab_pin.sym} %d %d 0 0 {name=l_%s lab=%s}' % (x, y - 30, name, net),
            'C {devices/gnd.sym} %d %d 0 0 {name=g_%s lab=0}' % (x, y + 30, name)]


# Stimulus from the handout's Figure 3, in ns. Precharge is high while
# precharging; the word line is high for the write and again for the read.
STIM = {
    "pre":   "PWL(0 0  1n 0  1.05n 1.8  9n 1.8  9.05n 0  20n 0  "
             "20.05n 1.8  29n 1.8  29.05n 0  50n 0)",
    "word":  "PWL(0 0  10n 0  10.05n 1.8  19n 1.8  19.05n 0  29n 0  29.05n 1.8  50n 1.8)",
    "write": "PWL(0 0  10n 0  10.05n 1.8  19n 1.8  19.05n 0  50n 0)",
    "data":  "1.8",
}

CONTROL = """
.option wnflag=1
.temp 27
* Two stable states, so say which one to start in -- without this the DC
* solution is arbitrary and the write has nothing to overwrite.
.ic v(a)=0 v(a_b)=1.8
.control
save all
set filetype=ascii
tran 10p 50n
write sram6t_tb.raw v(pre) v(word) v(write) v(bit) v(bit_b) v(a) v(a_b)

* After writing a 1, a is high and a_b is low, so a_b is the node at risk
* during the read.
meas tran a_after_write  FIND v(a)   AT=19n
meas tran ab_after_write FIND v(a_b) AT=19n
meas tran ab_read_peak   MAX  v(a_b) FROM=29.1n TO=50n

* Read time: word rising to 200 mV of bit-line separation. RISE=2 on both --
* the first crossing belongs to the write, where the driver separates the bit
* lines for an unrelated reason.
let dbit = v(bit) - v(bit_b)
meas tran t_read TRIG v(word) VAL=0.9 RISE=2 TARG dbit VAL=0.2 RISE=2
.endc
"""


def build_tb():
    # Laid out in three columns so the CONTROL block, which is thirty lines
    # tall, does not land on top of the title or the stimulus sources.
    TX = -1600                      # text and stimulus column
    body = ["""T {ECE334 Lab 4 - 6T SRAM cell testbench

Build your cell inside the DUT (select it and press `e` -> dut_sram6t.sch).
Required net names:  bit  bit_b  word  a  a_b  vdd  vss

The periphery is provided. Press `e` on it to see the precharge devices and
the write drivers.

Writes sram6t_tb.raw. Open lab4.ipynb to analyse it.} %d -1260 0 0 0.4 0.4 {}"""
            % TX]

    periph_nets = {"pre": "pre", "write": "write", "data": "data",
                   "bit": "bit", "bit_b": "bit_b", "vdd": "vdd", "vss": "vss"}
    cell_nets = {"bit": "bit", "bit_b": "bit_b", "word": "word",
                 "a": "a", "a_b": "a_b", "vdd": "vdd", "vss": "vss"}
    body += ['C {sram_periph.sym} -800 0 0 0 {name=x2}']
    body += hookup(-800, 0, PERIPH_PINS, periph_nets, "per")
    body += ['C {dut_sram6t.sym} 200 0 0 0 {name=x1}']
    body += hookup(200, 0, SRAM6T_PINS, cell_nets, "cell")

    for i, (net, value) in enumerate(STIM.items()):
        body += vsource("V" + net, TX, -300 + i * 140, value, net)
    body += vsource("Vdd", TX, 260, "1.8", "vdd")
    # A 0 V source rather than a bare gnd symbol on the vss net. A gnd symbol
    # and a lab_pin cannot share a point -- XSchem keeps the lab_pin name and
    # the ground connection is silently lost, which leaves every supply
    # floating and the cell sitting at mid-rail.
    body += vsource("Vss", TX, 400, "0", "vss")

    # 1 pF on each bit line, as specified in the conventions table.
    body += cap("Cb",  -300, 500, "1p", "bit")
    body += cap("Cbb",  600, 500, "1p", "bit_b")

    body += ['C {devices/code_shown.sym} %d -960 0 0 {name=MODELS only_toplevel=true '
             'value=".lib $PDK_ROOT/sky130A/libs.tech/ngspice/sky130.lib.spice tt"}' % TX,
             'C {devices/code_shown.sym} %d -900 0 0 {name=CONTROL only_toplevel=true '
             'value="%s"}' % (TX, CONTROL)]
    body += ['C {devices/launcher.sym} 700 -300 0 0 {name=h1 descr="Netlist & Simulate"\n'
             'tclcommand="xschem save; xschem netlist; xschem simulate"}',
             'C {devices/launcher.sym} 700 -240 0 0 {name=h2 descr="Run analysis notebook"\n'
             'tclcommand="exec sh -c {cd /foss/designs/lab4_sram && jupyter nbconvert '
             '--to notebook --execute --inplace lab4.ipynb} &"}']
    return HDR + "\n".join(body) + "\n"


if __name__ == "__main__":
    write(os.path.join(LAB4, "dut_sram6t.sym"),
          symbol("dut_sram6t", "6T CELL", SRAM6T_PINS))
    write(os.path.join(LAB4, "dut_sram6t.sch"), build_sram6t_stub())
    write(os.path.join(LAB4, "sram_periph.sym"),
          symbol("sram_periph", "PERIPHERY", PERIPH_PINS))
    write(os.path.join(LAB4, "sram_periph.sch"), build_periph())
    write(os.path.join(LAB4, "sram6t_tb.sch"), build_tb())
    write(os.path.join(SOL, "dut_sram6t.sch"), build_sram6t_solution())
