v {xschem version=3.4.8 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {*** BUILD YOUR DIODE-CONNECTED DEVICE HERE ***

This is the cell behind the `dut_diode` symbol used by diode_tb.sch.
Place one NMOS (sky130_fd_pr/nfet_01v8) and wire it diode-connected:

  gate  -> g      drain -> g       (gate tied to drain)
  source -> s     body  -> s

Extraction size:  W = 10, L = 2

>>> Enter W and L as UNITLESS MICRONS (W=10, L=2) -- do NOT add 'u'.
    A 'u' suffix lands outside every model bin -> "could not find a valid modelname".

DO NOT rename the two pins (g, s); the bench and notebook rely on them.} -180 -210 0 0 0.3 0.3 {}
C {devices/iopin.sym} 0 -150 0 0 {name=p1 lab=g}
C {devices/iopin.sym} 0 150 0 0 {name=p2 lab=s}
