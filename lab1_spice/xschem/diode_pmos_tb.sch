v {xschem version=3.4.8 file_version=1.2}
G {}
V {}
S {}
E {}
T {ECE334 Lab 1 - P2/L2  PMOS parameter extraction} -620 -400 0 0 0.45 0.45 {}
T {The gate and drain sit at 0 V; the source and body are swept from 0 to 1.8 V,
so V_SG is exactly the swept voltage and the same square-law fit applies.

Build a diode-connected PMOS in the DUT (double-click it), W = 10, L = 2.
Writes diode_pmos.raw with vsg and id.} -620 -350 0 0 0.32 0.32 {}
C {devices/code_shown.sym} -620 -230 0 0 {name=MODELS only_toplevel=true value=".lib $PDK_ROOT/sky130A/libs.tech/ngspice/sky130.lib.spice tt"}
C {devices/code_shown.sym} -620 -180 0 0 {name=CONTROL only_toplevel=true value="
.control
save all
dc Vsweep 0 1.8 0.01
let vsg = v(s)
let id = -i(Vsweep)
set filetype=ascii
write diode_pmos.raw vsg id
.endc
"}
C {devices/launcher.sym} -620 120 0 0 {name=h1 descr="Netlist & Simulate"
tclcommand="xschem save; xschem netlist; xschem simulate"}
C {devices/launcher.sym} -620 160 0 0 {name=h2 descr="Run analysis notebook"
tclcommand="exec sh -c {cd /foss/designs/lab1_spice && jupyter nbconvert --to notebook --execute --inplace lab1.ipynb} &"}
C {dut_diodep.sym} 100 0 0 0 {name=x1}
C {devices/lab_pin.sym} 100 50 0 0 {name=l_s lab=s}
C {devices/gnd.sym} 100 -110 0 0 {name=g1 lab=0}
N 100 -50 100 -110 {lab=g}
C {devices/vsource.sym} 320 60 0 0 {name=Vsweep value=0}
C {devices/lab_pin.sym} 320 30 0 0 {name=l_vs lab=s}
C {devices/gnd.sym} 320 90 0 0 {name=g2 lab=0}
T {Launchers: click the arrow once, then press Ctrl-H.
Ctrl-clicking one usually misses: it fires only if the pointer
does not move at all between press and release. The menubar's
Netlist and Simulate buttons do the same thing and always work.} -630 205 0 0 0.25 0.25 {}
