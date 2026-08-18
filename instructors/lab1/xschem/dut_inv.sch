v {xschem version=3.4.8 file_version=1.2}
G {}
V {}
S {}
E {}
T {Reference solution -- CMOS inverter.  Wn = 1, Wp = 3, L = 0.5.} -320 -260 0 0 0.3 0.3 {}
N 20 -100 20 -160 {lab=vdd}
N 20 -160 70 -160 {lab=vdd}
N 70 -160 70 -70 {lab=vdd}
N 70 -70 20 -70 {lab=vdd}
N 20 -40 20 40 {lab=out}
N 20 0 140 0 {lab=out}
N 20 100 20 160 {lab=vss}
N 20 160 70 160 {lab=vss}
N 70 160 70 70 {lab=vss}
N 70 70 20 70 {lab=vss}
N -20 -70 -20 70 {lab=in}
N -140 0 -20 0 {lab=in}
C {sky130_fd_pr/pfet_01v8.sym} 0 -70 0 0 {name=M2 W=3 L=0.5 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet_01v8.sym} 0 70 0 0 {name=M1 W=1 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/ipin.sym} -140 0 0 0 {name=p1 lab=in}
C {devices/opin.sym} 140 0 0 0 {name=p2 lab=out}
C {devices/iopin.sym} 20 -160 0 0 {name=p3 lab=vdd}
C {devices/iopin.sym} 20 160 0 0 {name=p4 lab=vss}
