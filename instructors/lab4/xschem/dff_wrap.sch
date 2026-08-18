v {xschem version=3.4.8 file_version=1.2}
G {}
V {}
S {}
E {}
T {Wrapper that makes XSchem emit ".subckt dff ..." for the Lab 4 decks to
include. Netlisting dff.sch on its own emits its devices at the top level
with no subcircuit around them.} -400 -240 0 0 0.3 0.3 {}
C {dff.sym} 0 0 0 0 {name=x1}
C {devices/lab_pin.sym} -90 -50 0 0 {name=a lab=data}
C {devices/lab_pin.sym} -90 -10 0 0 {name=b lab=cl}
C {devices/lab_pin.sym} -90 30 0 0 {name=c lab=setq}
C {devices/lab_pin.sym} -90 70 0 0 {name=d lab=resetq}
C {devices/lab_pin.sym} 90 -40 0 0 {name=e lab=q}
C {devices/lab_pin.sym} 90 40 0 0 {name=f lab=q_b}
C {devices/lab_pin.sym} 0 -100 0 0 {name=g lab=vdd}
C {devices/lab_pin.sym} 0 100 0 0 {name=h lab=vss}
