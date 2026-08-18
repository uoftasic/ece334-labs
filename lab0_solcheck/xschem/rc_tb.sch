v {xschem version=3.4.8 file_version=1.2}
G {}
V {}
S {}
E {}
T {ECE334 Lab 1 - P1/L1  RC divider step response} -620 -320 0 0 0.45 0.45 {}
T {A 1.8 V step drives R1 into the R2 || C1 node "out".

  Final value   Vout(inf) = 1.8 * R2/(R1+R2)
  Time constant tau       = (R1 || R2) * C1

Press "Netlist & Simulate". It writes rc_tb.raw (v(in), v(out)).
Then open lab1.ipynb, section P1, and run the measurement cell.

Predict both numbers by hand BEFORE you simulate.} -620 -270 0 0 0.35 0.35 {}
C {devices/code_shown.sym} -620 -80 0 0 {name=CONTROL only_toplevel=true value="
.control
save all
set filetype=ascii
tran 1p 15n
write rc_tb.raw v(in) v(out)
.endc
"}
C {devices/launcher.sym} -620 140 0 0 {name=h1 descr="Netlist & Simulate"
tclcommand="xschem save; xschem netlist; xschem simulate"}
C {devices/launcher.sym} -620 180 0 0 {name=h2 descr="Run analysis notebook"
tclcommand="exec sh -c {cd /foss/designs/lab1_spice && jupyter nbconvert --to notebook --execute --inplace lab1.ipynb} &"}
C {devices/vsource.sym} 0 60 0 0 {name=Vin value="PULSE(0 1.8 0 0.2n 0.2n 3n 6n)"}
C {devices/lab_pin.sym} 0 30 0 0 {name=l_in lab=in}
C {devices/gnd.sym} 0 90 0 0 {name=g1 lab=0}
C {devices/res.sym} 200 60 0 0 {name=R1 value=1k m=1}
C {devices/lab_pin.sym} 200 30 0 0 {name=l_r1a lab=in}
C {devices/lab_pin.sym} 200 90 0 0 {name=l_r1b lab=out}
C {devices/res.sym} 400 60 0 0 {name=R2 value=2k m=1}
C {devices/lab_pin.sym} 400 30 0 0 {name=l_r2a lab=out}
C {devices/gnd.sym} 400 90 0 0 {name=g2 lab=0}
C {devices/capa.sym} 580 60 0 0 {name=C1 value=0.7p m=1}
C {devices/lab_pin.sym} 580 30 0 0 {name=l_c1a lab=out}
C {devices/gnd.sym} 580 90 0 0 {name=g3 lab=0}
