v {xschem version=3.4.8 file_version=1.2}
G {}
V {}
S {}
E {}
T {ECE334 Lab 1 - P4/L4  Pulse generator} -700 -420 0 0 0.45 0.45 {}
T {Three inverters delay the input; the NAND compares the input with the
delayed, inverted copy. Both NAND inputs are high only during that delay,
so "out" carries a narrow LOW-going pulse once per rising input edge.

Build the circuit inside the DUT (double-click it -> dut_pulsegen.sch).
Required net names: in  n3  out  vdd  vss.

Writes pulsegen_tb.raw with v(in), v(n3), v(out).} -700 -370 0 0 0.32 0.32 {}
C {devices/code_shown.sym} -700 -130 0 0 {name=MODELS only_toplevel=true value=".lib $PDK_ROOT/sky130A/libs.tech/ngspice/sky130.lib.spice tt"}
C {devices/code_shown.sym} -700 -80 0 0 {name=CONTROL only_toplevel=true value="
.option wnflag=1
.temp 27
.control
save all
set filetype=ascii
tran 1p 25n
write pulsegen_tb.raw v(in) v(n3) v(out)
.endc
"}
C {devices/launcher.sym} -700 190 0 0 {name=h1 descr="Netlist & Simulate"
tclcommand="xschem save; xschem netlist; xschem simulate"}
C {devices/launcher.sym} -700 230 0 0 {name=h2 descr="Annotate OP"
tclcommand="set show_hidden_texts 1; xschem annotate_op"}
C {devices/launcher.sym} -700 270 0 0 {name=h3 descr="Run analysis notebook"
tclcommand="exec sh -c {cd /foss/designs/lab1_spice && jupyter nbconvert --to notebook --execute --inplace lab1.ipynb} &"}
N -240 0 -85 0 {lab=in}
N 85 0 200 0 {lab=out}
C {devices/vsource.sym} -320 60 0 0 {name=Vin value="PULSE(0 1.8 1n 0.2n 0.2n 10n 20n)"}
C {devices/lab_pin.sym} -320 30 0 0 {name=l_in lab=in}
C {devices/gnd.sym} -320 90 0 0 {name=g1 lab=0}
C {devices/lab_pin.sym} -240 0 0 0 {name=l_in2 lab=in}
C {dut_pulsegen.sym} 0 0 0 0 {name=x1}
C {devices/lab_pin.sym} 0 -65 0 0 {name=l_vdd lab=vdd}
C {devices/lab_pin.sym} 0 65 0 0 {name=l_vss lab=vss}
C {devices/lab_pin.sym} 200 0 0 0 {name=l_out lab=out}
C {devices/lab_pin.sym} 85 -30 0 0 {name=l_n3 lab=n3}
C {devices/vsource.sym} 340 190 0 0 {name=Vdd value=1.8}
C {devices/lab_pin.sym} 340 160 0 0 {name=l_vddsrc lab=vdd}
C {devices/gnd.sym} 340 220 0 0 {name=g2 lab=0}
C {devices/vsource.sym} 500 190 0 0 {name=Vss value=0}
C {devices/lab_pin.sym} 500 160 0 0 {name=l_vsssrc lab=vss}
C {devices/gnd.sym} 500 220 0 0 {name=g3 lab=0}
