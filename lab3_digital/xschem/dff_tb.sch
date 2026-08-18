v {xschem version=3.4.8 file_version=1.2}
G {}
V {}
S {}
E {}
T {ECE334 Lab 3 - P3/L3  D flip-flop} -900 -420 0 0 0.45 0.45 {}
T {Stimulus from the legacy handout, rescaled to 1.8 V.

  CL     : 10 ns high, 20 ns period
  DATA   : 20 ns high, 40 ns period, delayed 5 ns
  SETQ   : one 40 ns pulse at 55 ns
  RESETQ : one 40 ns pulse at 175 ns

Writes dff_tb.raw with cl, cl_b, setq, resetq, data, q and q_b.} -900 -380 0 0 0.32 0.32 {}
C {devices/code_shown.sym} -900 -230 0 0 {name=MODELS only_toplevel=true value=".lib $PDK_ROOT/sky130A/libs.tech/ngspice/sky130.lib.spice tt"}
C {devices/code_shown.sym} -900 -180 0 0 {name=CONTROL only_toplevel=true value="
.option wnflag=1
.temp 27
.control
save all
set filetype=ascii
tran 10p 250n
write dff_tb.raw v(cl) v(x1.cl_b) v(setq) v(resetq) v(data) v(q) v(q_b)
.endc
"}
C {devices/launcher.sym} -900 120 0 0 {name=h1 descr="Netlist & Simulate"
tclcommand="xschem save; xschem netlist; xschem simulate"}
C {devices/launcher.sym} -900 160 0 0 {name=h2 descr="Run analysis notebook"
tclcommand="exec sh -c {cd /foss/designs/lab3_digital && jupyter nbconvert --to notebook --execute --inplace lab3.ipynb} &"}
C {dff.sym} 0 0 0 0 {name=x1}
C {devices/lab_pin.sym} -90 -50 0 0 {name=l_d lab=data}
C {devices/lab_pin.sym} -90 -10 0 0 {name=l_cl lab=cl}
C {devices/lab_pin.sym} -90 30 0 0 {name=l_s lab=setq}
C {devices/lab_pin.sym} -90 70 0 0 {name=l_r lab=resetq}
C {devices/lab_pin.sym} 90 -40 0 0 {name=l_q lab=q}
C {devices/lab_pin.sym} 90 40 0 0 {name=l_qb lab=q_b}
C {devices/lab_pin.sym} 0 -100 0 0 {name=l_vdd lab=vdd}
C {devices/lab_pin.sym} 0 100 0 0 {name=l_vss lab=vss}
C {devices/vsource.sym} -600 60 0 0 {name=Vcl value="PULSE(0 1.8 0 0.5n 0.5n 10n 20n)"}
C {devices/lab_pin.sym} -600 30 0 0 {name=lv1 lab=cl}
C {devices/gnd.sym} -600 90 0 0 {name=g1 lab=0}
C {devices/vsource.sym} -440 60 0 0 {name=Vdata value="PULSE(0 1.8 5n 0.5n 0.5n 20n 40n)"}
C {devices/lab_pin.sym} -440 30 0 0 {name=lv2 lab=data}
C {devices/gnd.sym} -440 90 0 0 {name=g2 lab=0}
C {devices/vsource.sym} -600 220 0 0 {name=Vsetq value="PULSE(0 1.8 55n 0.5n 0.5n 40n 1000n)"}
C {devices/lab_pin.sym} -600 190 0 0 {name=lv3 lab=setq}
C {devices/gnd.sym} -600 250 0 0 {name=g3 lab=0}
C {devices/vsource.sym} -440 220 0 0 {name=Vresetq value="PULSE(0 1.8 175n 0.5n 0.5n 40n 1000n)"}
C {devices/lab_pin.sym} -440 190 0 0 {name=lv4 lab=resetq}
C {devices/gnd.sym} -440 250 0 0 {name=g4 lab=0}
C {devices/vsource.sym} -260 220 0 0 {name=Vdd value=1.8}
C {devices/lab_pin.sym} -260 190 0 0 {name=lv5 lab=vdd}
C {devices/gnd.sym} -260 250 0 0 {name=g5 lab=0}
C {devices/vsource.sym} -120 220 0 0 {name=Vss value=0}
C {devices/lab_pin.sym} -120 190 0 0 {name=lv6 lab=vss}
C {devices/gnd.sym} -120 250 0 0 {name=g6 lab=0}
