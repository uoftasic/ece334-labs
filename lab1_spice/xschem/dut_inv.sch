v {xschem version=3.4.8 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {*** BUILD YOUR CMOS INVERTER HERE ***

This is the cell behind the `dut_inv` symbol used by inv_tb.sch.
Place one PMOS and one NMOS from the sky130_fd_pr library and wire them:

  PMOS (pfet_01v8):  source -> vdd,  drain -> out,  gate -> in,  body -> vdd
  NMOS (nfet_01v8):  source -> vss,  drain -> out,  gate -> in,  body -> vss

Teaching sizes:  Wn = 1, Wp = 3, L = 0.5

>>> Enter W and L as UNITLESS MICRONS (W=1, L=0.5) -- do NOT add 'u'.
    The sky130 device models bin on plain micron numbers; "W=1u" lands
    outside every bin and ngspice reports "could not find a valid modelname".

DO NOT rename the four pins. The testbench and the analysis notebook rely on
the net names:  in, out, vdd, vss.} -180 -230 0 0 0.3 0.3 {}
C {devices/ipin.sym} -280 0 0 0 {name=p1 lab=in}
C {devices/opin.sym} 280 0 0 0 {name=p2 lab=out}
C {devices/iopin.sym} 0 -120 0 0 {name=p3 lab=vdd}
C {devices/iopin.sym} 0 120 0 0 {name=p4 lab=vss}
