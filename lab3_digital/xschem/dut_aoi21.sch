v {xschem version=3.4.8 file_version=1.2}
G {}
V {}
S {}
E {}
T {*** BUILD YOUR AOI21 GATE HERE ***

    Y = NOT( A + B.C )

Pull-down (NMOS), conducts when A + B.C is true:
    one device for A, in PARALLEL with a SERIES pair for B and C.

Pull-up (PMOS), conducts when NOT(A + B.C) = (NOT A) AND (NOT B OR NOT C):
    one device for A, in SERIES with a PARALLEL pair for B and C.

Sizing from P2, for the same worst-case edges as the unit inverter at 1.5 pF:
    NMOS  a = 5      b = c = 10   (series pair, doubled)
    PMOS  a = 30     b = c = 30   (a is in series with one of b, c)

Enter W and L as unitless microns. L = 0.5 throughout.
Do not rename the pins: a, b, c, y, vdd, vss.} -420 -340 0 0 0.3 0.3 {}
C {devices/ipin.sym} -420 -30 0 0 {name=p1 lab=a}
C {devices/ipin.sym} -420 0 0 0 {name=p2 lab=b}
C {devices/ipin.sym} -420 30 0 0 {name=p3 lab=c}
C {devices/opin.sym} 420 0 0 0 {name=p4 lab=y}
C {devices/iopin.sym} 0 -140 0 0 {name=p5 lab=vdd}
C {devices/iopin.sym} 0 140 0 0 {name=p6 lab=vss}
