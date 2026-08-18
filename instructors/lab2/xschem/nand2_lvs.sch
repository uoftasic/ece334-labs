v {xschem version=3.4.8 file_version=1.2}
G {}
V {}
S {}
E {}
T {LVS wrapper.

Netlisting nand2.sch on its own emits its devices at the top level, with no
.subckt around them, and netgen then reports "Cannot find cell nand2".
Instantiating the symbol here produces a proper .subckt nand2 for the compare.} -400 -300 0 0 0.3 0.3 {}
C {nand2.sym} 0 0 0 0 {name=x1}
C {devices/lab_pin.sym} -50 -20 0 0 {name=la lab=a}
C {devices/lab_pin.sym} -50 20 0 0 {name=lb lab=b}
C {devices/lab_pin.sym} 70 0 0 0 {name=lo lab=out}
C {devices/lab_pin.sym} -10 -60 0 0 {name=lv lab=vdd}
C {devices/lab_pin.sym} -10 60 0 0 {name=lg lab=vss}
