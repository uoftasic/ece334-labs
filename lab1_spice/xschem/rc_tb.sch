v {xschem version=3.4.8 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {ECE334 Lab 1 - RC step response

A voltage step drives R into C. The output settles with time constant
tau = R * C. With R = 1k and C = 1p, tau = 1 ns.

Press "Netlist & Simulate" to write rc_tb.raw (v(in), v(out)),
then open lab1.ipynb to measure tau and the 10-90% rise time.
Try changing R or C and re-running.} -360 -240 0 0 0.4 0.4 {}
C {devices/vsource.sym} -200 30 0 0 {name=Vin value="PULSE(0 1.8 0 1p 1p 50n 100n)"}
C {devices/lab_pin.sym} -200 0 0 0 {name=l_in lab=in}
C {devices/gnd.sym} -200 60 0 0 {name=g1 lab=0}
C {devices/res.sym} 0 30 0 0 {name=R1 value=1k m=1}
C {devices/lab_pin.sym} 0 0 0 0 {name=l_rin lab=in}
C {devices/lab_pin.sym} 0 60 0 0 {name=l_rout lab=out}
C {devices/capa.sym} 0 150 0 0 {name=C1 value=1p m=1}
C {devices/lab_pin.sym} 0 120 0 0 {name=l_cout lab=out}
C {devices/gnd.sym} 0 180 0 0 {name=g2 lab=0}
C {devices/code_shown.sym} -360 40 0 0 {name=CONTROL only_toplevel=true value="
.control
save all
set filetype=ascii
tran 10p 60n
write rc_tb.raw v(in) v(out)
.endc
"}
C {devices/launcher.sym} -360 160 0 0 {name=h1 descr="Netlist & Simulate"
tclcommand="xschem save; xschem netlist; xschem simulate"}
C {devices/launcher.sym} -360 200 0 0 {name=h2 descr="Run analysis notebook"
tclcommand="exec sh -c {cd /foss/designs/lab1_spice && jupyter nbconvert --to notebook --execute --inplace lab1.ipynb} &"}
