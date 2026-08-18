v {xschem version=3.4.8 file_version=1.2}
G {}
V {}
S {}
E {}
T {*** BUILD YOUR DIODE-CONNECTED PMOS HERE ***

Mirror of the NMOS case, referenced to the source instead of ground:

  gate and drain -> g   (held at 0 V by the testbench)
  source and body -> s  (swept from 0 to 1.8 V by the testbench)

so V_SG = v(s) and the device is saturated whenever it conducts.

Size it W = 10, L = 2, the same extraction device as the NMOS.
Enter W and L as unitless microns -- no 'u'.

Do not rename the pins.} -420 -300 0 0 0.3 0.3 {}
C {devices/iopin.sym} 0 -150 0 0 {name=p1 lab=g}
C {devices/iopin.sym} 0 150 0 0 {name=p2 lab=s}
