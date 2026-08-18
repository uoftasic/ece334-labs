# Reference NAND2 layout, drawn with Magic paint commands.
#
# Sized to match common/xschem/nand2.sch exactly -- Wn = 2, Wp = 3, L = 0.5 --
# so LVS compares the layout against the same cell the student built in Lab 1.
# That is also the legacy handout's 24:16 device ratio, at this lab's L.
#
# Layout style: horizontal diffusion, vertical poly.
#   NMOS pair in series  : vss -- [a] -- mid -- [b] -- out
#   PMOS pair in parallel: vdd -- [a] -- out,  vdd -- [b] -- out
#
#   magic -dnull -noconsole -T sky130A < build_nand2.tcl

# Every contact needs local interconnect overhanging the cut by >= 0.08 um
# (rule li.5). Painting li over the full footprint and insetting the contact by
# 0.1 um satisfies that without having to size each cut by hand.
proc contact {type x0 y0 x1 y1} {
    box ${x0}um ${y0}um ${x1}um ${y1}um
    paint li
    box [expr {$x0 + 0.1}]um [expr {$y0 + 0.1}]um \
        [expr {$x1 - 0.1}]um [expr {$y1 - 0.1}]um
    paint $type
}

proc rect {layer x0 y0 x1 y1} {
    box ${x0}um ${y0}um ${x1}um ${y1}um
    paint $layer
}

drc off
load nand2 -silent
# Start from an empty cell. Without this the script paints on top of whatever
# nand2.mag already held, and a previous run's geometry shows up as spurious
# DRC errors that do not exist in a fresh build.
box -60um -60um 60um 60um
select area
delete
box 0 0 0 0

# ---- wells --------------------------------------------------------------
rect nwell -0.8 4.2 8.4 9.0

# ---- NMOS: series pair, W = 2 -------------------------------------------
rect ndiff 0 0 6.0 2.0
contact ndc 0.3 0.3 1.2 1.7
contact ndc 4.3 0.3 5.7 1.7

# ---- PMOS: parallel pair, W = 3 -----------------------------------------
rect pdiff 0 5.0 6.0 8.0
contact pdc 0.3 5.3 1.2 7.7
contact pdc 2.3 5.3 3.2 7.7
contact pdc 4.3 5.3 5.7 7.7

# ---- poly gates ---------------------------------------------------------
# One stripe per input, crossing both diffusions. L = 0.5 um.
rect poly 1.5 -1.6 2.0 8.6
rect poly 3.5 -1.6 4.0 8.6
# Landing pads. Kept clear of the vss interconnect column at x = 1.2 by more
# than the 0.17 um li spacing rule (li.3).
rect poly 1.45 -1.7 2.35 -0.8
rect poly 3.45 -1.7 4.35 -0.8
contact polyc 1.5 -1.65 2.3 -0.85
contact polyc 3.5 -1.65 4.3 -0.85

# ---- substrate and well taps -------------------------------------------
rect ptap 6.8 0 7.8 2.0
contact ptapc 6.9 0.2 7.7 1.8
rect ntap 6.8 5.0 7.8 8.0
contact ntapc 6.9 5.2 7.7 7.8

# ---- supply rails -------------------------------------------------------
rect m1 -0.8 -3.4 8.4 -2.4
rect m1 -0.8 9.4 8.4 10.4

# ---- local interconnect down to the rails -------------------------------
# NMOS source -> vss
rect li 0.3 -3.2 1.2 1.7
rect mcon 0.55 -3.1 0.95 -2.7
# substrate tap -> vss
rect li 6.9 -3.2 7.7 1.8
rect mcon 7.1 -3.1 7.5 -2.7
# PMOS sources -> vdd
rect li 0.3 5.3 1.2 9.9
rect mcon 0.55 9.5 0.95 9.9
rect li 4.3 5.3 5.7 9.9
rect mcon 4.9 9.5 5.3 9.9
# well tap -> vdd
rect li 6.9 5.2 7.7 9.9
rect mcon 7.1 9.5 7.5 9.9

# ---- output net: NMOS drain up to the PMOS shared drain -----------------
rect li 4.6 0.3 5.4 3.6
rect li 2.5 3.0 5.4 3.6
rect li 2.5 3.0 3.2 7.7

# ---- labels -------------------------------------------------------------
# The schematic drives the series NMOS nearest "out" from a, so the RIGHT poly
# stripe is a and the left one is b. Netgen matches the topology either way --
# a NAND is symmetric -- but reports a pin mismatch if the names are permuted.
box 1.6um -1.55um 2.2um -0.95um
label b
box 3.6um -1.55um 4.2um -0.95um
label a
box 2.6um 3.1um 3.1um 3.5um
label out
box 3.0um 9.6um 3.6um 10.2um
label vdd
box 3.0um -3.2um 3.6um -2.6um
label vss

# ---- check --------------------------------------------------------------
drc on
drc euclidean on
box -2um -5um 10um 12um
drc check
drc catchup
puts "DRC_COUNT=[drc list count total]"
foreach {rule areas} [drc listall why] {
    puts "RULE ([llength $areas]): $rule"
    puts "   first at [lindex $areas 0]"
}
# ---- ports --------------------------------------------------------------
# Explicit indices, so the extracted .subckt port order does not depend on the
# order the labels happen to be painted in.
select cell
port makeall
foreach {p i} {a 1 b 2 out 3 vdd 4 vss 5} { port $p index $i }
save nand2

# ---- extraction ---------------------------------------------------------
extract do local
extract all
# Device-level netlist for LVS: no parasitics.
ext2spice lvs
ext2spice -o nand2.lvs.spice
# Parasitic netlist: cthresh 0 keeps every coupling capacitance. Without it the
# small ones are dropped and the pre/post comparison shows almost no difference.
ext2spice cthresh 0
ext2spice -o nand2.pex.spice
puts "PORTS=[exec grep -m1 {^.subckt} nand2.lvs.spice]"
puts "SAVED"
quit -noprompt
