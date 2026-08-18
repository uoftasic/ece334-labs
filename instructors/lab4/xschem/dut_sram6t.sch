v {xschem version=3.4.8 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Reference 6T cell. Sizing from Lab 4 P1:
  read   2.0 >= 2.7 * 0.7 = 1.89   OK
  write  0.7 >= 1.2 * 0.5 = 0.60   OK} -380 -400 0 0 0.3 0.3 {}
C {devices/iopin.sym} -160 120 0 0 {name=p1 lab=bit}
C {devices/iopin.sym} 500 120 0 0 {name=p2 lab=bit_b}
C {devices/ipin.sym} -380 0 0 0 {name=p3 lab=word}
C {devices/iopin.sym} -160 -120 0 0 {name=p4 lab=a}
C {devices/iopin.sym} 500 -120 0 0 {name=p5 lab=a_b}
C {devices/iopin.sym} 170 -260 0 0 {name=p6 lab=vdd}
C {devices/iopin.sym} 170 260 0 0 {name=p7 lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 0 -120 0 0 {name=P1 W=0.5 L=0.5 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -20 -120 0 0 {name=l_P1_a_b lab=a_b}
C {sky130_fd_pr/nfet_01v8.sym} 0 120 0 0 {name=N1 W=2.0 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -20 120 0 0 {name=l_N1_a_b lab=a_b}
N 20 -120 20 -260 {lab=vdd}
N 20 120 20 260 {lab=vss}
N 20 -90 20 90 {lab=a}
C {devices/lab_pin.sym} 20 0 0 0 {name=l_N1_out lab=a}
C {sky130_fd_pr/pfet_01v8.sym} 300 -120 0 0 {name=P2 W=0.5 L=0.5 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 280 -120 0 0 {name=l_P2_a lab=a}
C {sky130_fd_pr/nfet_01v8.sym} 300 120 0 0 {name=N3 W=2.0 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 280 120 0 0 {name=l_N3_a lab=a}
N 320 -120 320 -260 {lab=vdd}
N 320 120 320 260 {lab=vss}
N 320 -90 320 90 {lab=a_b}
C {devices/lab_pin.sym} 320 0 0 0 {name=l_N3_out lab=a_b}
C {sky130_fd_pr/nfet_01v8.sym} -180 0 0 0 {name=N2 W=0.7 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -200 0 0 0 {name=l_N2_word lab=word}
C {devices/lab_pin.sym} -160 0 0 0 {name=l_N2_vss lab=vss}
N -160 -30 -160 -120 {lab=a}
N -160 30 -160 120 {lab=bit}
C {sky130_fd_pr/nfet_01v8.sym} 480 0 0 0 {name=N4 W=0.7 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 460 0 0 0 {name=l_N4_word lab=word}
C {devices/lab_pin.sym} 500 0 0 0 {name=l_N4_vss lab=vss}
N 500 -30 500 -120 {lab=a_b}
N 500 30 500 120 {lab=bit_b}
N 20 -260 320 -260 {lab=vdd}
N 20 260 320 260 {lab=vss}
