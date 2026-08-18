#!/usr/bin/env bash
# Netgen LVS: the extracted layout against the XSchem schematic.
#
#   ./scripts/run_lvs.sh [layout.spice] [schematic.spice] [report]
#
# Both netlists must define a .subckt of the same name. Magic produces one
# once the layout has ports (see the manual, L4). XSchem produces one only for
# a schematic that INSTANTIATES the cell -- netlisting nand2.sch directly emits
# its devices at the top level with no .subckt, and netgen then reports
# "Cannot find cell nand2".
set -euo pipefail
cd "$(dirname "$0")/.."
: "${PDK_ROOT:?source /foss/designs/common/.designinit first}"

LAYOUT="${1:-nand2.lvs.spice}"
SCHEM="${2:-nand2_lvs.spice}"
REPORT="${3:-nand2.lvs.report}"

for f in "$LAYOUT" "$SCHEM"; do
  [ -f "$f" ] || { echo "missing netlist: $f" >&2; exit 2; }
done

netgen -batch lvs \
  "${LAYOUT} nand2" \
  "${SCHEM} nand2" \
  "$PDK_ROOT/sky130A/libs.tech/netgen/sky130A_setup.tcl" \
  "$REPORT" >/dev/null 2>&1 || true

echo "report: $REPORT"
grep -E "Netlists match|Mismatch|Final result" "$REPORT" || tail -20 "$REPORT"

if grep -q "Circuits match uniquely" "$REPORT"; then
  exit 0
fi
echo
echo "LVS did not match. Usual causes, in order of likelihood:"
echo "  * a missing or misspelled port label in the layout"
echo "  * a port present in one netlist but not the other"
echo "  * inputs swapped -- netgen matches the topology but reports a pin"
echo "    mismatch, because a NAND is symmetric in its inputs"
exit 1
