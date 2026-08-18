v {xschem version=3.4.8 file_version=1.2}
G {}
V {}
S {}
E {}
T {2-input NOR} -320 -340 0 0 0.4 0.4 {}
T {PMOS in series, NMOS in parallel.
Series PMOS pair is doubled in width so the worst-case pull-up
matches a single device.
Gates connect by net name -- the a and b labels.} -320 -302 0 0 0.28 0.28 {}
N -40 -190 -40 -240 {lab=vdd}
N -40 -240 60 -240 {lab=vdd}
N -40 -130 -40 -70 {lab=mid}
N -40 -10 -40 40 {lab=out}
N -40 40 160 40 {lab=out}
N 160 40 160 -10 {lab=out}
N 160 100 160 160 {lab=vss}
N 160 160 20 160 {lab=vss}
N 20 160 20 100 {lab=vss}
N 60 40 60 -10 {lab=out}
N 20 -10 20 40 {lab=out}
C {sky130_fd_pr/pfet_01v8.sym} -60 -160 0 0 {name=MPA W=18 L=0.5 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} -60 -40 0 0 {name=MPB W=18 L=0.5 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet_01v8.sym} 0 70 0 0 {name=MNA W=3 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet_01v8.sym} 140 70 0 0 {name=MNB W=3 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -80 -160 0 0 {name=la1 lab=a}
C {devices/lab_pin.sym} -80 -40 0 0 {name=lb1 lab=b}
C {devices/lab_pin.sym} -20 70 0 0 {name=la2 lab=a}
C {devices/lab_pin.sym} 120 70 0 0 {name=lb2 lab=b}
C {devices/lab_pin.sym} -40 -160 0 0 {name=lv1 lab=vdd}
C {devices/lab_pin.sym} -40 -40 0 0 {name=lv2 lab=vdd}
C {devices/lab_pin.sym} 20 70 0 0 {name=lg1 lab=vss}
C {devices/lab_pin.sym} 160 70 0 0 {name=lg2 lab=vss}
C {devices/ipin.sym} -320 -160 0 0 {name=pa lab=a}
C {devices/ipin.sym} -320 -120 0 0 {name=pb lab=b}
C {devices/opin.sym} 260 40 0 0 {name=py lab=out}
C {devices/iopin.sym} 60 -240 0 0 {name=pv lab=vdd}
C {devices/iopin.sym} 20 160 0 0 {name=pg lab=vss}
N 160 40 260 40 {lab=out}
