v {xschem version=3.4.8 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {ECE334 Lab 1 - CMOS inverter testbench

Build your inverter inside the DUT (select it and press `e` -> dut_inv.sch).
Required net names:  in  out  vdd  vss   (do not rename them).

Outputs written by the buttons below:
  inv_tb_tran.raw  - transient (v(in), v(out))
  inv_tb_vtc.raw   - DC transfer curve (v(in), v(out))
Open lab1.ipynb to analyse them.} -470 -470 0 0 0.4 0.4 {}
C {dut_inv.sym} 0 0 0 0 {name=x1}
C {devices/lab_pin.sym} -60 0 0 0 {name=l_in lab=in}
C {devices/lab_pin.sym} 60 0 0 0 {name=l_out lab=out}
C {devices/lab_pin.sym} 0 -50 0 0 {name=l_vdd lab=vdd}
C {devices/vsource.sym} -200 30 0 0 {name=Vin value="PULSE(0 1.8 2n 0.1n 0.1n 8n 16n)"}
C {devices/lab_pin.sym} -200 0 0 0 {name=l_vin lab=in}
C {devices/gnd.sym} -200 60 0 0 {name=g1 lab=0}
C {devices/capa.sym} 200 30 0 0 {name=Cload value=0.2p}
C {devices/lab_pin.sym} 200 0 0 0 {name=l_cl lab=out}
C {devices/gnd.sym} 200 60 0 0 {name=g2 lab=0}
C {devices/vsource.sym} 320 0 0 0 {name=Vdd value=1.8}
C {devices/lab_pin.sym} 320 -30 0 0 {name=l_vdd2 lab=vdd}
C {devices/gnd.sym} 320 30 0 0 {name=g3 lab=0}
C {devices/gnd.sym} 0 50 0 0 {name=g4 lab=0}
C {devices/code_shown.sym} -470 -200 0 0 {name=MODELS only_toplevel=true value=".lib $PDK_ROOT/sky130A/libs.tech/ngspice/sky130.lib.spice tt"}
C {devices/code_shown.sym} -470 -100 0 0 {name=CONTROL only_toplevel=true value="
.option wnflag=1
.temp 27
.control
save all
set filetype=ascii
tran 1p 20n
write inv_tb_tran.raw v(in) v(out)
reset
dc Vin 0 1.8 0.01
write inv_tb_vtc.raw v(in) v(out)
.endc
"}
C {devices/launcher.sym} -470 120 0 0 {name=h1 descr="Netlist & Simulate"
tclcommand="xschem save; xschem netlist; xschem simulate"}
C {devices/launcher.sym} -470 160 0 0 {name=h2 descr="Annotate OP"
tclcommand="set show_hidden_texts 1; xschem annotate_op"}
C {devices/launcher.sym} -470 200 0 0 {name=h3 descr="Run analysis notebook"
tclcommand="exec sh -c {cd /foss/designs/lab1_spice && jupyter nbconvert --to notebook --execute --inplace lab1.ipynb} &"}
T {Launchers: click the arrow once, then press Ctrl-H.
Ctrl-clicking one usually misses: it fires only if the pointer
does not move at all between press and release. The menubar's
Netlist and Simulate buttons do the same thing and always work.} -480 245 0 0 0.25 0.25 {}
