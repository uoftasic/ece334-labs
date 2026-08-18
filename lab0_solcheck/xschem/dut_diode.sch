v {xschem version=3.4.8 file_version=1.2}
G {}
V {}
S {}
E {}
T {Reference solution -- diode-connected NMOS.

Gate tied to drain, so the device is saturated whenever it conducts.
Source and body tied together at s.
W = 10, L = 2: a long channel stays close to the square law.} -420 -300 0 0 0.3 0.3 {}
N 20 -30 20 -110 {lab=g}
N 20 -110 -60 -110 {lab=g}
N -60 -110 -60 0 {lab=g}
N -60 0 -20 0 {lab=g}
N 20 -110 20 -150 {lab=g}
N 20 0 20 150 {lab=s}
C {sky130_fd_pr/nfet_01v8.sym} 0 0 0 0 {name=M1 W=10 L=2 nf=1 mult=1 model=nfet_01v8 spiceprefix=X}
C {devices/iopin.sym} 20 -150 0 0 {name=p1 lab=g}
C {devices/iopin.sym} 20 150 0 0 {name=p2 lab=s}
