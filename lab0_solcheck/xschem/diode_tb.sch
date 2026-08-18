v {xschem version=3.4.8 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {ECE334 Lab 1 - diode-connected device extraction

Build a diode-connected FET inside the DUT (gate AND drain -> g, source AND
body -> s). Vsweep ramps the gate/drain 0 -> 1.8 V; the bench records the
drain current vs gate voltage.

Press "Netlist & Simulate" to write diode_nmos.raw (v(g), id),
then run the extraction section of lab1.ipynb to fit KP and Vt.} -470 -360 0 0 0.4 0.4 {}
C {dut_diode.sym} 0 0 0 0 {name=x1}
C {devices/lab_pin.sym} 0 -50 0 0 {name=l_g lab=g}
C {devices/vsource.sym} -200 30 0 0 {name=Vsweep value=0}
C {devices/lab_pin.sym} -200 0 0 0 {name=l_vs lab=g}
C {devices/gnd.sym} -200 60 0 0 {name=g1 lab=0}
C {devices/gnd.sym} 0 50 0 0 {name=g2 lab=0}
C {devices/code_shown.sym} -470 -200 0 0 {name=MODELS only_toplevel=true value=".lib $PDK_ROOT/sky130A/libs.tech/ngspice/sky130.lib.spice tt"}
C {devices/code_shown.sym} -470 -120 0 0 {name=CONTROL only_toplevel=true value="
.control
save all
set filetype=ascii
dc Vsweep 0 1.8 0.01
let id = -i(Vsweep)
write diode_nmos.raw v(g) id
.endc
"}
C {devices/launcher.sym} -470 40 0 0 {name=h1 descr="Netlist & Simulate"
tclcommand="xschem save; xschem netlist; xschem simulate"}
C {devices/launcher.sym} -470 80 0 0 {name=h2 descr="Run analysis notebook"
tclcommand="exec sh -c {cd /foss/designs/lab1_spice && jupyter nbconvert --to notebook --execute --inplace lab1.ipynb} &"}
