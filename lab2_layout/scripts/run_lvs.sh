#!/usr/bin/env bash
# Netgen LVS: layout-extracted vs XSchem schematic netlist
set -euo pipefail
cd "$(dirname "$0")/.."
: "${PDK_ROOT:?Run sak-pdk sky130A first}"

LAYOUT_SPICE="${1:-nand2.lvs.spice}"
SCHEM_SPICE="${2:-nand2_sch.spice}"
REPORT="${3:-nand2.lvs.report}"

netgen -batch lvs \
  "${LAYOUT_SPICE} nand2" \
  "${SCHEM_SPICE} nand2_sch" \
  "$PDK_ROOT/sky130A/libs.tech/netgen/sky130A_setup.tcl" \
  "$REPORT"

echo "Report: $REPORT"
grep -E 'match|Match' "$REPORT" || tail -20 "$REPORT"
