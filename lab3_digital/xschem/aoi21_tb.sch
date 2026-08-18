v {xschem version=3.4.8 file_version=1.2}
G {}
V {}
S {}
E {}
T {ECE334 Lab 3 - P2/L2  AOI21, Y = NOT(A + B.C)} -820 -420 0 0 0.45 0.45 {}
T {Build the gate inside the DUT (double-click it -> dut_aoi21.sch).

Change which input switches and which are held to select the case you are
measuring. As shipped this is the WORST CASE FALL and WORST CASE RISE:
a is held low, c is held high, and b switches, so the only conducting
pull-down path is the series b-c pair and the only pull-up path is a in
series with b.

  worst fall / worst rise : a = 0, c = 1, b switches
  best fall               : a, b and c all switch together
  best rise               : b = c = 0, a switches

Load is 1.5 pF. Writes aoi21_tb.raw with v(a), v(b), v(c) and v(y).} -820 -380 0 0 0.32 0.32 {}
C {devices/code_shown.sym} -820 -160 0 0 {name=MODELS only_toplevel=true value=".lib $PDK_ROOT/sky130A/libs.tech/ngspice/sky130.lib.spice tt"}
C {devices/code_shown.sym} -820 -110 0 0 {name=CONTROL only_toplevel=true value="
.option wnflag=1
.temp 27
.control
save all
set filetype=ascii
tran 10p 30n
write aoi21_tb.raw v(a) v(b) v(c) v(y)
meas tran tfall TRIG v(y) VAL=1.62 FALL=1 TARG v(y) VAL=0.18 FALL=1
meas tran trise TRIG v(y) VAL=0.18 RISE=1 TARG v(y) VAL=1.62 RISE=1
.endc
"}
C {devices/launcher.sym} -820 160 0 0 {name=h1 descr="Netlist & Simulate"
tclcommand="xschem save; xschem netlist; xschem simulate"}
C {dut_aoi21.sym} 0 0 0 0 {name=x1}
C {devices/lab_pin.sym} -80 -30 0 0 {name=l_a lab=a}
C {devices/lab_pin.sym} -80 0 0 0 {name=l_b lab=b}
C {devices/lab_pin.sym} -80 30 0 0 {name=l_c lab=c}
C {devices/lab_pin.sym} 80 0 0 0 {name=l_y lab=y}
C {devices/lab_pin.sym} 0 -75 0 0 {name=l_vdd lab=vdd}
C {devices/lab_pin.sym} 0 75 0 0 {name=l_vss lab=vss}
C {devices/capa.sym} 220 60 0 0 {name=CL value=1.5p m=1}
C {devices/lab_pin.sym} 220 30 0 0 {name=l_cl lab=y}
C {devices/gnd.sym} 220 90 0 0 {name=g0 lab=0}
C {devices/vsource.sym} -400 160 0 0 {name=Va value=0}
C {devices/lab_pin.sym} -400 130 0 0 {name=lv1 lab=a}
C {devices/gnd.sym} -400 190 0 0 {name=g1 lab=0}
C {devices/vsource.sym} -240 160 0 0 {name=Vb value="PULSE(0 1.8 2n 0.1n 0.1n 10n 20n)"}
C {devices/lab_pin.sym} -240 130 0 0 {name=lv2 lab=b}
C {devices/gnd.sym} -240 190 0 0 {name=g2 lab=0}
C {devices/vsource.sym} -80 160 0 0 {name=Vc value=1.8}
C {devices/lab_pin.sym} -80 130 0 0 {name=lv3 lab=c}
C {devices/gnd.sym} -80 190 0 0 {name=g3 lab=0}
C {devices/vsource.sym} 80 160 0 0 {name=Vdd value=1.8}
C {devices/lab_pin.sym} 80 130 0 0 {name=lv4 lab=vdd}
C {devices/gnd.sym} 80 190 0 0 {name=g4 lab=0}
C {devices/vsource.sym} 240 160 0 0 {name=Vss value=0}
C {devices/lab_pin.sym} 240 130 0 0 {name=lv5 lab=vss}
C {devices/gnd.sym} 240 190 0 0 {name=g5 lab=0}
T {Launchers: click the arrow once, then press Ctrl-H.
Ctrl-clicking one usually misses: it fires only if the pointer
does not move at all between press and release. The menubar's
Netlist and Simulate buttons do the same thing and always work.} -830 205 0 0 0.25 0.25 {}
