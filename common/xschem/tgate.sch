v {xschem version=3.4.8 file_version=1.2}
G {}
V {}
S {}
E {}
T {Transmission gate} -380 -300 0 0 0.4 0.4 {}
T {NMOS and PMOS in parallel. The internal inverter derives the PMOS gate
from ctrl, so one control signal opens and closes both devices.
Conducting when ctrl is high.

Wn = 3, Wp = 9. Terminals connect by net name: a transmission gate has no
fixed source, so drawing it with wires would suggest a direction it does
not have. Bodies go to the rails, never to the passed signal.} -380 -262 0 0 0.28 0.28 {}
C {sky130_fd_pr/pfet_01v8.sym} 0 -60 0 0 {name=MP W=9 L=0.5 nf=1 mult=1 model=pfet_01v8 spiceprefix=X}
C {sky130_fd_pr/nfet_01v8.sym} 0 60 0 0 {name=MN W=3 L=0.5 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 20 -30 0 0 {name=lp_in lab=in}
C {devices/lab_pin.sym} 20 -90 0 0 {name=lp_out lab=out}
C {devices/lab_pin.sym} -20 -60 0 0 {name=lp_cb lab=ctrl_b}
C {devices/lab_pin.sym} 20 -60 0 0 {name=lp_vb lab=vdd}
C {devices/lab_pin.sym} 20 30 0 0 {name=ln_in lab=in}
C {devices/lab_pin.sym} 20 90 0 0 {name=ln_out lab=out}
C {devices/lab_pin.sym} -20 60 0 0 {name=ln_c lab=ctrl}
C {devices/lab_pin.sym} 20 60 0 0 {name=ln_gb lab=vss}
C {inv.sym} -220 -180 0 0 {name=xinv}
C {devices/lab_pin.sym} -270 -180 0 0 {name=lci lab=ctrl}
C {devices/lab_pin.sym} -170 -180 0 0 {name=lcb lab=ctrl_b}
C {devices/lab_pin.sym} -220 -220 0 0 {name=lv0 lab=vdd}
C {devices/lab_pin.sym} -220 -140 0 0 {name=lg0 lab=vss}
C {devices/ipin.sym} -380 0 0 0 {name=p1 lab=in}
C {devices/opin.sym} 200 0 0 0 {name=p2 lab=out}
C {devices/ipin.sym} -380 60 0 0 {name=p3 lab=ctrl}
C {devices/iopin.sym} -380 -180 0 0 {name=p4 lab=vdd}
C {devices/iopin.sym} -380 -140 0 0 {name=p5 lab=vss}
