v {xschem version=3.4.8 file_version=1.2}
G {}
V {}
S {}
E {}
T {*** BUILD YOUR PULSE GENERATOR HERE ***

This is the cell behind the dut_pulsegen symbol used by pulsegen_tb.sch.

Wire three inverters in a chain, then feed a NAND2 with the chain output
and the original input:

    in ---+--[inv]--[inv]--[inv]--> n3 ---> NAND2.b
          |                                NAND2.a
          +--------------------------------^

    NAND2.out -> out

Both cells are already in this folder: place inv.sym three times and
nand2.sym once (Shift-I opens the symbol browser).

Connect vdd and vss of every cell to the vdd and vss pins below.

DO NOT rename the four pins. The testbench and lab1.ipynb rely on the net
names:  in, out, vdd, vss.  Wire the last chain node to the n3 port so the notebook can plot it
beside in and out.} -420 -330 0 0 0.3 0.3 {}
C {devices/ipin.sym} -420 0 0 0 {name=p1 lab=in}
C {devices/opin.sym} 420 -120 0 0 {name=p2 lab=n3}
C {devices/opin.sym} 420 0 0 0 {name=p3 lab=out}
C {devices/iopin.sym} 0 -120 0 0 {name=p4 lab=vdd}
C {devices/iopin.sym} 0 120 0 0 {name=p5 lab=vss}
