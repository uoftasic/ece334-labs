v {xschem version=3.4.8 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {ECE334 Lab 4 - 6T SRAM cell testbench

Build your cell inside the DUT (select it and press `e` -> dut_sram6t.sch).
Required net names:  bit  bit_b  word  a  a_b  vdd  vss

The periphery is provided. Press `e` on it to see the precharge devices and
the write drivers.

Writes sram6t_tb.raw. Open lab4.ipynb to analyse it.} -1600 -1260 0 0 0.4 0.4 {}
C {sram_periph.sym} -800 0 0 0 {name=x2}
C {devices/lab_pin.sym} -900 -40 0 0 {name=l_per_pre lab=pre}
C {devices/lab_pin.sym} -900 0 0 0 {name=l_per_write lab=write}
C {devices/lab_pin.sym} -900 40 0 0 {name=l_per_data lab=data}
C {devices/lab_pin.sym} -700 -40 0 0 {name=l_per_bit lab=bit}
C {devices/lab_pin.sym} -700 40 0 0 {name=l_per_bit_b lab=bit_b}
C {devices/lab_pin.sym} -800 -105 0 0 {name=l_per_vdd lab=vdd}
C {devices/lab_pin.sym} -800 105 0 0 {name=l_per_vss lab=vss}
C {dut_sram6t.sym} 200 0 0 0 {name=x1}
C {devices/lab_pin.sym} 100 -40 0 0 {name=l_cell_bit lab=bit}
C {devices/lab_pin.sym} 100 40 0 0 {name=l_cell_bit_b lab=bit_b}
C {devices/lab_pin.sym} 100 0 0 0 {name=l_cell_word lab=word}
C {devices/lab_pin.sym} 300 -40 0 0 {name=l_cell_a lab=a}
C {devices/lab_pin.sym} 300 40 0 0 {name=l_cell_a_b lab=a_b}
C {devices/lab_pin.sym} 200 -105 0 0 {name=l_cell_vdd lab=vdd}
C {devices/lab_pin.sym} 200 105 0 0 {name=l_cell_vss lab=vss}
C {devices/vsource.sym} -1600 -300 0 0 {name=Vpre value="PWL(0 0  1n 0  1.05n 1.8  9n 1.8  9.05n 0  20n 0  20.05n 1.8  29n 1.8  29.05n 0  50n 0)"}
C {devices/lab_pin.sym} -1600 -330 0 0 {name=l_Vpre lab=pre}
C {devices/gnd.sym} -1600 -270 0 0 {name=g_Vpre lab=0}
C {devices/vsource.sym} -1600 -160 0 0 {name=Vword value="PWL(0 0  10n 0  10.05n 1.8  19n 1.8  19.05n 0  29n 0  29.05n 1.8  50n 1.8)"}
C {devices/lab_pin.sym} -1600 -190 0 0 {name=l_Vword lab=word}
C {devices/gnd.sym} -1600 -130 0 0 {name=g_Vword lab=0}
C {devices/vsource.sym} -1600 -20 0 0 {name=Vwrite value="PWL(0 0  10n 0  10.05n 1.8  19n 1.8  19.05n 0  50n 0)"}
C {devices/lab_pin.sym} -1600 -50 0 0 {name=l_Vwrite lab=write}
C {devices/gnd.sym} -1600 10 0 0 {name=g_Vwrite lab=0}
C {devices/vsource.sym} -1600 120 0 0 {name=Vdata value="1.8"}
C {devices/lab_pin.sym} -1600 90 0 0 {name=l_Vdata lab=data}
C {devices/gnd.sym} -1600 150 0 0 {name=g_Vdata lab=0}
C {devices/vsource.sym} -1600 260 0 0 {name=Vdd value="1.8"}
C {devices/lab_pin.sym} -1600 230 0 0 {name=l_Vdd lab=vdd}
C {devices/gnd.sym} -1600 290 0 0 {name=g_Vdd lab=0}
C {devices/vsource.sym} -1600 400 0 0 {name=Vss value="0"}
C {devices/lab_pin.sym} -1600 370 0 0 {name=l_Vss lab=vss}
C {devices/gnd.sym} -1600 430 0 0 {name=g_Vss lab=0}
C {devices/capa.sym} -300 500 0 0 {name=Cb value=1p}
C {devices/lab_pin.sym} -300 470 0 0 {name=l_Cb lab=bit}
C {devices/gnd.sym} -300 530 0 0 {name=g_Cb lab=0}
C {devices/capa.sym} 600 500 0 0 {name=Cbb value=1p}
C {devices/lab_pin.sym} 600 470 0 0 {name=l_Cbb lab=bit_b}
C {devices/gnd.sym} 600 530 0 0 {name=g_Cbb lab=0}
C {devices/code_shown.sym} -1600 -960 0 0 {name=MODELS only_toplevel=true value=".lib $PDK_ROOT/sky130A/libs.tech/ngspice/sky130.lib.spice tt"}
C {devices/code_shown.sym} -1600 -900 0 0 {name=CONTROL only_toplevel=true value="
.option wnflag=1
.temp 27
* Two stable states, so say which one to start in -- without this the DC
* solution is arbitrary and the write has nothing to overwrite.
.ic v(a)=0 v(a_b)=1.8
.control
save all
set filetype=ascii
tran 10p 50n
write sram6t_tb.raw v(pre) v(word) v(write) v(bit) v(bit_b) v(a) v(a_b)

* After writing a 1, a is high and a_b is low, so a_b is the node at risk
* during the read.
meas tran a_after_write  FIND v(a)   AT=19n
meas tran ab_after_write FIND v(a_b) AT=19n
meas tran ab_read_peak   MAX  v(a_b) FROM=29.1n TO=50n

* Read time: word rising to 200 mV of bit-line separation. RISE=2 on both --
* the first crossing belongs to the write, where the driver separates the bit
* lines for an unrelated reason.
let dbit = v(bit) - v(bit_b)
meas tran t_read TRIG v(word) VAL=0.9 RISE=2 TARG dbit VAL=0.2 RISE=2
.endc
"}
C {devices/launcher.sym} 700 -300 0 0 {name=h1 descr="Netlist & Simulate"
tclcommand="xschem save; xschem netlist; xschem simulate"}
C {devices/launcher.sym} 700 -240 0 0 {name=h2 descr="Run analysis notebook"
tclcommand="exec sh -c {cd /foss/designs/lab4_sram && jupyter nbconvert --to notebook --execute --inplace lab4.ipynb} &"}
