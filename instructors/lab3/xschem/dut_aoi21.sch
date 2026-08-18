v {xschem version=3.4.8 file_version=1.2}
G {}
V {}
S {}
E {}
T {Reference solution -- AOI21, Y = NOT(A + B.C).
Pull-down: a alone, in parallel with the series pair b-c.
Pull-up:   a in series with the parallel pair b-c.} -520 -340 0 0 0.3 0.3 {}
C {sky130_fd_pr/pfet_01v8.sym} -200 -200 0 0 {name=MPA W=30 L=0.5 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} -60 -80 0 0 {name=MPB W=30 L=0.5 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} 100 -80 0 0 {name=MPC W=30 L=0.5 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet_01v8.sym} -200 100 0 0 {name=MNA W=5 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet_01v8.sym} 60 60 0 0 {name=MNB W=10 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet_01v8.sym} 60 180 0 0 {name=MNC W=10 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -180 -230 0 0 {name=x1 lab=vdd}
C {devices/lab_pin.sym} -180 -200 0 0 {name=x2 lab=vdd}
C {devices/lab_pin.sym} -180 -170 0 0 {name=x3 lab=pmid}
C {devices/lab_pin.sym} -220 -200 0 0 {name=x4 lab=a}
C {devices/lab_pin.sym} -40 -110 0 0 {name=x5 lab=pmid}
C {devices/lab_pin.sym} -40 -80 0 0 {name=x6 lab=vdd}
C {devices/lab_pin.sym} -40 -50 0 0 {name=x7 lab=y}
C {devices/lab_pin.sym} -80 -80 0 0 {name=x8 lab=b}
C {devices/lab_pin.sym} 120 -110 0 0 {name=x9 lab=pmid}
C {devices/lab_pin.sym} 120 -80 0 0 {name=x10 lab=vdd}
C {devices/lab_pin.sym} 120 -50 0 0 {name=x11 lab=y}
C {devices/lab_pin.sym} 80 -80 0 0 {name=x12 lab=c}
C {devices/lab_pin.sym} -180 70 0 0 {name=x13 lab=y}
C {devices/lab_pin.sym} -180 100 0 0 {name=x14 lab=vss}
C {devices/lab_pin.sym} -180 130 0 0 {name=x15 lab=vss}
C {devices/lab_pin.sym} -220 100 0 0 {name=x16 lab=a}
C {devices/lab_pin.sym} 80 30 0 0 {name=x17 lab=y}
C {devices/lab_pin.sym} 80 60 0 0 {name=x18 lab=vss}
C {devices/lab_pin.sym} 80 90 0 0 {name=x19 lab=nmid}
C {devices/lab_pin.sym} 40 60 0 0 {name=x20 lab=b}
C {devices/lab_pin.sym} 80 150 0 0 {name=x21 lab=nmid}
C {devices/lab_pin.sym} 80 180 0 0 {name=x22 lab=vss}
C {devices/lab_pin.sym} 80 210 0 0 {name=x23 lab=vss}
C {devices/lab_pin.sym} 40 180 0 0 {name=x24 lab=c}
C {devices/ipin.sym} -520 -30 0 0 {name=p1 lab=a}
C {devices/ipin.sym} -520 0 0 0 {name=p2 lab=b}
C {devices/ipin.sym} -520 30 0 0 {name=p3 lab=c}
C {devices/opin.sym} 420 0 0 0 {name=p4 lab=y}
C {devices/iopin.sym} 0 -300 0 0 {name=p5 lab=vdd}
C {devices/iopin.sym} 0 300 0 0 {name=p6 lab=vss}
