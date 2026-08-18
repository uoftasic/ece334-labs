v {xschem version=3.4.8 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Reference solution -- AOI21,  Y = NOT(A + B.C)

Pull-down:  a alone, in parallel with the series pair b-c.
Pull-up:    a in series with the parallel pair b-c -- the dual.

The two networks are duals of each other, which is what makes the output
always driven and never both at once.} -240 -560 0 0 0.3 0.3 {}
C {devices/ipin.sym} -240 -100 0 0 {name=p1 lab=a}
C {devices/ipin.sym} -240 0 0 0 {name=p2 lab=b}
C {devices/ipin.sym} -240 100 0 0 {name=p3 lab=c}
C {devices/opin.sym} 520 0 0 0 {name=p4 lab=y}
C {devices/iopin.sym} 170 -360 0 0 {name=p5 lab=vdd}
C {devices/iopin.sym} 170 360 0 0 {name=p6 lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 0 -280 0 0 {name=MPA W=30 L=0.5 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -20 -280 0 0 {name=l_MPA_a lab=a}
N 20 -280 20 -360 {lab=vdd}
C {sky130_fd_pr/pfet_01v8.sym} 0 -100 0 0 {name=MPB W=30 L=0.5 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -20 -100 0 0 {name=l_MPB_b lab=b}
C {devices/lab_pin.sym} 20 -100 0 0 {name=l_MPB_vdd lab=vdd}
N 20 -130 20 -180 {lab=pmid}
N 20 -70 20 0 {lab=y}
C {sky130_fd_pr/pfet_01v8.sym} 300 -100 0 0 {name=MPC W=30 L=0.5 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 280 -100 0 0 {name=l_MPC_c lab=c}
C {devices/lab_pin.sym} 320 -100 0 0 {name=l_MPC_vdd lab=vdd}
N 320 -130 320 -180 {lab=pmid}
N 320 -70 320 0 {lab=y}
N 20 -250 20 -180 {lab=pmid}
N 20 -180 320 -180 {lab=pmid}
C {devices/lab_pin.sym} 80 -180 0 0 {name=l_pmid lab=pmid}
C {sky130_fd_pr/nfet_01v8.sym} 0 100 0 0 {name=MNA W=5 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -20 100 0 0 {name=l_MNA_a lab=a}
N 20 70 20 0 {lab=y}
N 20 100 20 360 {lab=vss}
C {sky130_fd_pr/nfet_01v8.sym} 300 100 0 0 {name=MNB W=10 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 280 100 0 0 {name=l_MNB_b lab=b}
C {devices/lab_pin.sym} 320 100 0 0 {name=l_MNB_vss lab=vss}
C {sky130_fd_pr/nfet_01v8.sym} 300 280 0 0 {name=MNC W=10 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 280 280 0 0 {name=l_MNC_c lab=c}
N 320 70 320 0 {lab=y}
N 320 130 320 250 {lab=nmid}
C {devices/lab_pin.sym} 320 190 0 0 {name=l_nmid lab=nmid}
N 320 280 320 360 {lab=vss}
N 20 -360 320 -360 {lab=vdd}
N 20 360 320 360 {lab=vss}
N 20 0 520 0 {lab=y}
