v {xschem version=3.4.8 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Transmission gate} -600 -380 0 0 0.4 0.4 {}
T {NMOS and PMOS in parallel. The internal inverter derives the PMOS gate
from ctrl, so one control signal opens and closes both devices.
Conducting when ctrl is high.

Wn = 3, Wp = 9. Terminals connect by net name: a transmission gate has no
fixed source, so drawing it with wires would suggest a direction it does
not have. Bodies go to the rails, never to the passed signal.} -600 -340 0 0 0.28 0.28 {}
C {sky130_fd_pr/pfet_01v8.sym} 0 -160 0 0 {name=MP W=9 L=0.5 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 20 -190 0 0 {name=l_MP_out lab=out}
C {devices/lab_pin.sym} -20 -160 0 0 {name=l_MP_ctrl_b lab=ctrl_b}
C {devices/lab_pin.sym} 20 -130 0 0 {name=l_MP_in lab=in}
C {devices/lab_pin.sym} 20 -160 0 0 {name=l_MP_vdd lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 0 160 0 0 {name=MN W=3 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 20 130 0 0 {name=l_MN_in lab=in}
C {devices/lab_pin.sym} -20 160 0 0 {name=l_MN_ctrl lab=ctrl}
C {devices/lab_pin.sym} 20 190 0 0 {name=l_MN_out lab=out}
C {devices/lab_pin.sym} 20 160 0 0 {name=l_MN_vss lab=vss}
C {inv.sym} -350 300 0 0 {name=xinv}
C {devices/lab_pin.sym} -400 300 0 0 {name=l_ci lab=ctrl}
C {devices/lab_pin.sym} -300 300 0 0 {name=l_cb lab=ctrl_b}
C {devices/lab_pin.sym} -350 260 0 0 {name=l_iv lab=vdd}
C {devices/lab_pin.sym} -350 340 0 0 {name=l_ig lab=vss}
C {devices/ipin.sym} -600 0 0 0 {name=p1 lab=in}
C {devices/opin.sym} 600 0 0 0 {name=p2 lab=out}
C {devices/ipin.sym} -600 160 0 0 {name=p3 lab=ctrl}
C {devices/iopin.sym} -900 -300 0 0 {name=p4 lab=vdd}
C {devices/iopin.sym} -900 300 0 0 {name=p5 lab=vss}
