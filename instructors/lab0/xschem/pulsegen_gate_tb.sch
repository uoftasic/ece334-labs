v {xschem version=3.4.8 file_version=1.2}
G {}
V {}
S {}
E {}
T {ECE334 Lab 0 - pulse generator} -900 -420 0 0 0.45 0.45 {}
T {Three inverters delay and invert the input; the NAND compares the input
with that delayed copy. Both NAND inputs are high only during the delay,
so "out" goes low for a short time after each rising edge of "in".

Reference build. Students construct this from the inv and nand2 cells
they made earlier in the lab.} -900 -370 0 0 0.32 0.32 {}
C {devices/code_shown.sym} -900 -150 0 0 {name=MODELS only_toplevel=true value=".lib $PDK_ROOT/sky130A/libs.tech/ngspice/sky130.lib.spice tt"}
C {devices/code_shown.sym} -900 -100 0 0 {name=CONTROL only_toplevel=true value="
.option wnflag=1
.temp 27
.control
save all
set filetype=ascii
tran 1p 25n
write pulsegen_gate_tb.raw v(in) v(n3) v(out)
.endc
"}
C {devices/launcher.sym} -900 200 0 0 {name=h1 descr="Netlist & Simulate"
tclcommand="xschem save; xschem netlist; xschem simulate"}
N -700 0 -450 0 {lab=in}
N -350 0 -250 0 {lab=n1}
N -150 0 -50 0 {lab=n2}
N 50 0 150 0 {lab=n3}
N 150 0 150 120 {lab=n3}
N 150 120 250 120 {lab=n3}
N -600 0 -600 -200 {lab=in}
N -600 -200 200 -200 {lab=in}
N 200 -200 200 80 {lab=in}
N 200 80 250 80 {lab=in}
N 370 100 470 100 {lab=out}
C {devices/lab_pin.sym} 100 0 0 0 {name=ln3 lab=n3}
C {devices/lab_pin.sym} 470 100 0 0 {name=lout lab=out}
C {inv.sym} -400 0 0 0 {name=xi1}
C {inv.sym} -200 0 0 0 {name=xi2}
C {inv.sym} 0 0 0 0 {name=xi3}
C {nand2.sym} 300 100 0 0 {name=xn1}
C {devices/lab_pin.sym} -400 -40 0 0 {name=lv1 lab=vdd}
C {devices/lab_pin.sym} -400 40 0 0 {name=lg1 lab=vss}
C {devices/lab_pin.sym} -200 -40 0 0 {name=lv2 lab=vdd}
C {devices/lab_pin.sym} -200 40 0 0 {name=lg2 lab=vss}
C {devices/lab_pin.sym} 0 -40 0 0 {name=lv3 lab=vdd}
C {devices/lab_pin.sym} 0 40 0 0 {name=lg3 lab=vss}
C {devices/lab_pin.sym} 290 40 0 0 {name=lv4 lab=vdd}
C {devices/lab_pin.sym} 290 160 0 0 {name=lg4 lab=vss}
C {devices/vsource.sym} -820 60 0 0 {name=Vin value="PULSE(0 1.8 1n 0.2n 0.2n 10n 20n)"}
C {devices/lab_pin.sym} -820 30 0 0 {name=l_in lab=in}
C {devices/gnd.sym} -820 90 0 0 {name=g1 lab=0}
C {devices/lab_pin.sym} -700 0 0 0 {name=l_in2 lab=in}
C {devices/vsource.sym} 620 260 0 0 {name=Vdd value=1.8}
C {devices/lab_pin.sym} 620 230 0 0 {name=l_vdd lab=vdd}
C {devices/gnd.sym} 620 290 0 0 {name=g2 lab=0}
C {devices/vsource.sym} 800 260 0 0 {name=Vss value=0}
C {devices/lab_pin.sym} 800 230 0 0 {name=l_vss lab=vss}
C {devices/gnd.sym} 800 290 0 0 {name=g3 lab=0}
