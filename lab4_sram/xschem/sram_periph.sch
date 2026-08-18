v {xschem version=3.4.8 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {SRAM periphery -- provided, already built.

Precharge:     `pre` high drives both bit lines to VDD through P3 and P4.
Write drivers: with `write` high, N5/N7 pull `bit` down when data is 0, and
               N6/N8 pull `bit_b` down when data is 1. Only one side pulls at
               a time, which is what makes the write directional.

Press `e` with this symbol selected to look inside it.} -300 -560 0 0 0.3 0.3 {}
C {devices/ipin.sym} -300 -40 0 0 {name=p1 lab=pre}
C {devices/ipin.sym} -300 0 0 0 {name=p2 lab=write}
C {devices/ipin.sym} -300 40 0 0 {name=p3 lab=data}
C {devices/iopin.sym} 500 0 0 0 {name=p4 lab=bit}
C {devices/iopin.sym} 1320 0 0 0 {name=p5 lab=bit_b}
C {devices/iopin.sym} 570 -260 0 0 {name=p6 lab=vdd}
C {devices/iopin.sym} 570 260 0 0 {name=p7 lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 0 -120 0 0 {name=PIP W=8.0 L=0.5 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -20 -120 0 0 {name=l_PIP_pre lab=pre}
C {sky130_fd_pr/nfet_01v8.sym} 0 120 0 0 {name=PIN W=2.667 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -20 120 0 0 {name=l_PIN_pre lab=pre}
N 20 -120 20 -260 {lab=vdd}
N 20 120 20 260 {lab=vss}
N 20 -90 20 90 {lab=pre_b}
C {devices/lab_pin.sym} 20 0 0 0 {name=l_PIN_out lab=pre_b}
C {devices/lab_pin.sym} 20 -260 0 0 {name=l_PIP_v lab=vdd}
C {devices/lab_pin.sym} 20 260 0 0 {name=l_PIN_g lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 300 -120 0 0 {name=PDP W=8.0 L=0.5 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 280 -120 0 0 {name=l_PDP_data lab=data}
C {sky130_fd_pr/nfet_01v8.sym} 300 120 0 0 {name=PDN W=2.667 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 280 120 0 0 {name=l_PDN_data lab=data}
N 320 -120 320 -260 {lab=vdd}
N 320 120 320 260 {lab=vss}
N 320 -90 320 90 {lab=data_b}
C {devices/lab_pin.sym} 320 0 0 0 {name=l_PDN_out lab=data_b}
C {devices/lab_pin.sym} 320 -260 0 0 {name=l_PDP_v lab=vdd}
C {devices/lab_pin.sym} 320 260 0 0 {name=l_PDN_g lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 700 -120 0 0 {name=P3 W=8.0 L=0.5 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 680 -120 0 0 {name=l_P3_pre_b lab=pre_b}
N 720 -120 720 -260 {lab=vdd}
N 720 -90 720 0 {lab=bit}
C {devices/lab_pin.sym} 720 -260 0 0 {name=l_P3_v lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 700 60 0 0 {name=N5 W=8.0 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 680 60 0 0 {name=l_N5_write lab=write}
C {devices/lab_pin.sym} 720 60 0 0 {name=l_N5_vss lab=vss}
C {sky130_fd_pr/nfet_01v8.sym} 700 190 0 0 {name=N7 W=8.0 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 680 190 0 0 {name=l_N7_data_b lab=data_b}
N 720 30 720 0 {lab=bit}
N 720 90 720 160 {lab=n5d}
C {devices/lab_pin.sym} 720 125 0 0 {name=l_n5d lab=n5d}
N 720 190 720 260 {lab=vss}
C {devices/lab_pin.sym} 720 260 0 0 {name=l_N7_g lab=vss}
C {sky130_fd_pr/pfet_01v8.sym} 1100 -120 0 0 {name=P4 W=8.0 L=0.5 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1080 -120 0 0 {name=l_P4_pre_b lab=pre_b}
N 1120 -120 1120 -260 {lab=vdd}
N 1120 -90 1120 0 {lab=bit_b}
C {devices/lab_pin.sym} 1120 -260 0 0 {name=l_P4_v lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 1100 60 0 0 {name=N6 W=8.0 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1080 60 0 0 {name=l_N6_write lab=write}
C {devices/lab_pin.sym} 1120 60 0 0 {name=l_N6_vss lab=vss}
C {sky130_fd_pr/nfet_01v8.sym} 1100 190 0 0 {name=N8 W=8.0 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1080 190 0 0 {name=l_N8_data lab=data}
N 1120 30 1120 0 {lab=bit_b}
N 1120 90 1120 160 {lab=n6d}
C {devices/lab_pin.sym} 1120 125 0 0 {name=l_n6d lab=n6d}
N 1120 190 1120 260 {lab=vss}
C {devices/lab_pin.sym} 1120 260 0 0 {name=l_N8_g lab=vss}
N 720 0 500 0 {lab=bit}
N 1120 0 1320 0 {lab=bit_b}
N 20 -260 1120 -260 {lab=vdd}
N 20 260 1120 260 {lab=vss}
