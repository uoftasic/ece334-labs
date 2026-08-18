v {xschem version=3.4.8 file_version=1.2}
G {}
V {}
S {}
E {}
T {Transmission-gate D flip-flop} -980 -320 0 0 0.45 0.45 {}
T {Master-slave. Each latch is two NOR gates in a loop, closed by a
transmission gate when the other gate is open.

cl low  : TG1 passes data into the master; the slave holds through TG4.
cl high : TG1 opens, TG2 closes the master loop, TG3 passes the stored
          value into the slave. q updates on the rising edge.

setq forces q high and resetq forces q low, both through the NOR gates.
Connections are made by net name.} -980 -284 0 0 0.28 0.28 {}
C {inv.sym} -820 300 0 0 {name=xclk}
C {devices/lab_pin.sym} -870 300 0 0 {name=l_xclk_in lab=cl}
C {devices/lab_pin.sym} -770 300 0 0 {name=l_xclk_out lab=cl_b}
C {devices/lab_pin.sym} -820 260 0 0 {name=l_xclk_vdd lab=vdd}
C {devices/lab_pin.sym} -820 340 0 0 {name=l_xclk_vss lab=vss}
C {tgate.sym} -560 0 0 0 {name=xtg1}
C {devices/lab_pin.sym} -610 0 0 0 {name=l_xtg1_in lab=data}
C {devices/lab_pin.sym} -510 0 0 0 {name=l_xtg1_out lab=m1}
C {devices/lab_pin.sym} -560 -60 0 0 {name=l_xtg1_ctrl lab=cl_b}
C {devices/lab_pin.sym} -560 -85 0 0 {name=l_xtg1_vdd lab=vdd}
C {devices/lab_pin.sym} -560 85 0 0 {name=l_xtg1_vss lab=vss}
C {nor2.sym} -360 0 0 0 {name=xna}
C {devices/lab_pin.sym} -410 -20 0 0 {name=l_xna_a lab=m1}
C {devices/lab_pin.sym} -410 20 0 0 {name=l_xna_b lab=setq}
C {devices/lab_pin.sym} -290 0 0 0 {name=l_xna_out lab=m2}
C {devices/lab_pin.sym} -370 -58 0 0 {name=l_xna_vdd lab=vdd}
C {devices/lab_pin.sym} -370 58 0 0 {name=l_xna_vss lab=vss}
C {nor2.sym} -140 0 0 0 {name=xnb}
C {devices/lab_pin.sym} -190 -20 0 0 {name=l_xnb_a lab=m2}
C {devices/lab_pin.sym} -190 20 0 0 {name=l_xnb_b lab=resetq}
C {devices/lab_pin.sym} -70 0 0 0 {name=l_xnb_out lab=m3}
C {devices/lab_pin.sym} -150 -58 0 0 {name=l_xnb_vdd lab=vdd}
C {devices/lab_pin.sym} -150 58 0 0 {name=l_xnb_vss lab=vss}
C {tgate.sym} -360 240 0 0 {name=xtg2}
C {devices/lab_pin.sym} -410 240 0 0 {name=l_xtg2_in lab=m3}
C {devices/lab_pin.sym} -310 240 0 0 {name=l_xtg2_out lab=m1}
C {devices/lab_pin.sym} -360 180 0 0 {name=l_xtg2_ctrl lab=cl}
C {devices/lab_pin.sym} -360 155 0 0 {name=l_xtg2_vdd lab=vdd}
C {devices/lab_pin.sym} -360 325 0 0 {name=l_xtg2_vss lab=vss}
C {tgate.sym} 90 0 0 0 {name=xtg3}
C {devices/lab_pin.sym} 40 0 0 0 {name=l_xtg3_in lab=m3}
C {devices/lab_pin.sym} 140 0 0 0 {name=l_xtg3_out lab=s1}
C {devices/lab_pin.sym} 90 -60 0 0 {name=l_xtg3_ctrl lab=cl}
C {devices/lab_pin.sym} 90 -85 0 0 {name=l_xtg3_vdd lab=vdd}
C {devices/lab_pin.sym} 90 85 0 0 {name=l_xtg3_vss lab=vss}
C {nor2.sym} 290 0 0 0 {name=xnc}
C {devices/lab_pin.sym} 240 -20 0 0 {name=l_xnc_a lab=s1}
C {devices/lab_pin.sym} 240 20 0 0 {name=l_xnc_b lab=setq}
C {devices/lab_pin.sym} 360 0 0 0 {name=l_xnc_out lab=q_b}
C {devices/lab_pin.sym} 280 -58 0 0 {name=l_xnc_vdd lab=vdd}
C {devices/lab_pin.sym} 280 58 0 0 {name=l_xnc_vss lab=vss}
C {nor2.sym} 510 0 0 0 {name=xnd}
C {devices/lab_pin.sym} 460 -20 0 0 {name=l_xnd_a lab=q_b}
C {devices/lab_pin.sym} 460 20 0 0 {name=l_xnd_b lab=resetq}
C {devices/lab_pin.sym} 580 0 0 0 {name=l_xnd_out lab=q}
C {devices/lab_pin.sym} 500 -58 0 0 {name=l_xnd_vdd lab=vdd}
C {devices/lab_pin.sym} 500 58 0 0 {name=l_xnd_vss lab=vss}
C {tgate.sym} 290 240 0 0 {name=xtg4}
C {devices/lab_pin.sym} 240 240 0 0 {name=l_xtg4_in lab=q}
C {devices/lab_pin.sym} 340 240 0 0 {name=l_xtg4_out lab=s1}
C {devices/lab_pin.sym} 290 180 0 0 {name=l_xtg4_ctrl lab=cl_b}
C {devices/lab_pin.sym} 290 155 0 0 {name=l_xtg4_vdd lab=vdd}
C {devices/lab_pin.sym} 290 325 0 0 {name=l_xtg4_vss lab=vss}
C {devices/ipin.sym} -980 -60 0 0 {name=p_data lab=data}
C {devices/ipin.sym} -980 -20 0 0 {name=p_cl lab=cl}
C {devices/ipin.sym} -980 20 0 0 {name=p_setq lab=setq}
C {devices/ipin.sym} -980 60 0 0 {name=p_resetq lab=resetq}
C {devices/opin.sym} 720 -40 0 0 {name=p_q lab=q}
C {devices/opin.sym} 720 40 0 0 {name=p_q_b lab=q_b}
C {devices/iopin.sym} -980 -140 0 0 {name=p_vdd lab=vdd}
C {devices/iopin.sym} -980 -100 0 0 {name=p_vss lab=vss}
