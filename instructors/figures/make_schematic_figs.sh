#!/usr/bin/env bash
# Render every schematic figure in the manual, headlessly.
#
#   docker exec <container> /foss/designs/instructors/figures/make_schematic_figs.sh [OUTDIR]
#
# Unlike scripts/make_figures.sh this needs no X server, no window manager and
# no xdotool: it goes through XSchem's own --pdf export. See
# instructors/README.md for why that is the only export that works headless.
#
# Screenshots still have a job -- figures whose subject is the interface rather
# than the circuit (a menu, a dialog, the Magic window). Those stay in
# scripts/make_figures.sh.
set -uo pipefail
DESIGNS="${DESIGNS:-/foss/designs}"
OUT="${1:-/tmp/schematic-figs}"
EXPORT="${DESIGNS}/instructors/figures/export_schematic.sh"
SOL="${DESIGNS}/instructors"

fail=0
render() {  # render <sch> <lab> <name.png> [density]
  local sch="$1" lab="$2" png="$3" density="${4:-150}"
  mkdir -p "${OUT}/${lab}"
  "$EXPORT" "$sch" "${OUT}/${lab}/${png}" "$density" || fail=1
}

echo "== Lab 0 / Lab 1 cells =="
render "${DESIGNS}/common/xschem/inv.sch"        lab0 03-inverter-wired.png
render "${DESIGNS}/common/xschem/nand2.sch"      lab0 05-nand2-schematic.png
render "${SOL}/lab0/xschem/pulsegen_gate_tb.sch" lab0 06-pulsegen-hierarchy.png 130
render "${DESIGNS}/lab1_spice/xschem/rc_tb.sch"  lab1 01-rc-testbench.png 130

echo "== Lab 2 =="
render "${DESIGNS}/lab2_layout/xschem/nand2_lvs.sch" lab2 05-lvs-wrapper.png

echo "== Lab 3 =="
render "${SOL}/lab3/xschem/dut_aoi21.sch"    lab3 04-aoi21-schematic.png 130
render "${DESIGNS}/common/xschem/dff.sch"    lab3 05-dff-schematic.png   120
render "${DESIGNS}/common/xschem/tgate.sch"  lab3 06-tgate.png
render "${DESIGNS}/common/xschem/nor2.sch"   lab3 07-nor2.png

echo "== Lab 4 =="
render "${SOL}/lab4/xschem/dut_sram6t.sch"           lab4 05-sram6t-cell.png    130
render "${DESIGNS}/lab4_sram/xschem/sram_periph.sch" lab4 06-sram-periphery.png 110
# The testbench itself is deliberately not rendered. Most of its area is the
# thirty-line .control block, which is legible in the tool and illegible in a
# figure; the cell and the periphery carry everything a reader needs.

[ "$fail" -eq 0 ] && echo "done. schematic figures in ${OUT}" || echo "FAILED some renders"
exit "$fail"
