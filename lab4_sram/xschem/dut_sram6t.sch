v {xschem version=3.4.8 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {*** BUILD YOUR 6T SRAM CELL HERE ***

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
  bit  bit_b  word  a  a_b  vdd  vss} -540 -400 0 0 0.3 0.3 {}
C {devices/iopin.sym} -160 120 0 0 {name=p1 lab=bit}
C {devices/iopin.sym} 500 120 0 0 {name=p2 lab=bit_b}
C {devices/ipin.sym} -380 0 0 0 {name=p3 lab=word}
C {devices/iopin.sym} -160 -120 0 0 {name=p4 lab=a}
C {devices/iopin.sym} 500 -120 0 0 {name=p5 lab=a_b}
C {devices/iopin.sym} 170 -260 0 0 {name=p6 lab=vdd}
C {devices/iopin.sym} 170 260 0 0 {name=p7 lab=vss}
