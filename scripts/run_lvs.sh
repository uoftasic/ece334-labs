#!/usr/bin/env bash
# Compare an extracted layout against its schematic with netgen.
#
#   scripts/run_lvs.sh <layout.spice> <schematic.sch|schematic.spice> [cellname]
#
# The schematic argument may be an XSchem schematic, in which case it is
# netlisted first. Give it a schematic that INSTANTIATES the cell, not the
# cell's own schematic: netlisting a cell directly emits its devices at the top
# level with no .subckt around them, and netgen then reports "Cannot find cell".
#
# The cell name defaults to the layout netlist's basename with .lvs/.spice
# stripped, which is what `ext2spice -o nand2.lvs.spice` produces.
set -uo pipefail
layout="${1:?usage: run_lvs.sh <layout.spice> <schematic.sch|.spice> [cell]}"
sch="${2:?usage: run_lvs.sh <layout.spice> <schematic.sch|.spice> [cell]}"
DESIGNS="${DESIGNS:-/foss/designs}"
PDK_ROOT="${PDK_ROOT:?PDK_ROOT is not set -- run . ${DESIGNS}/common/.designinit}"

[ -f "$layout" ] || { echo "no such layout netlist: $layout" >&2; exit 2; }
[ -f "$sch" ]    || { echo "no such schematic: $sch" >&2; exit 2; }

cell="${3:-$(basename "$layout" | sed -e 's/\.spice$//' -e 's/\.lvs$//')}"
setup="${PDK_ROOT}/sky130A/libs.tech/netgen/sky130A_setup.tcl"
[ -f "$setup" ] || { echo "no netgen setup at $setup" >&2; exit 2; }

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

# Netlist the schematic side if we were handed a .sch.
case "$sch" in
  *.sch)
    timeout 180 xschem -n -s -q -x -o "$work" "$sch" >"$work/xschem.log" 2>&1
    sch_net="$work/$(basename "$sch" .sch).spice"
    if [ ! -f "$sch_net" ]; then
      echo "FAIL: xschem produced no netlist for $sch" >&2
      tail -5 "$work/xschem.log" >&2; exit 1
    fi
    if grep -q 'IS MISSING' "$sch_net"; then
      echo "FAIL: unresolved symbols in $sch -- re-run .designinit" >&2
      grep 'IS MISSING' "$sch_net" >&2; exit 1
    fi
    ;;
  *) sch_net="$sch" ;;
esac

if ! grep -qi "^\.subckt[[:space:]]\+${cell}\b" "$sch_net"; then
  echo "FAIL: $sch_net has no '.subckt ${cell}'." >&2
  echo "      Netlist a wrapper that instantiates ${cell}.sym, not ${cell}.sch." >&2
  exit 1
fi

netgen -batch lvs "$layout $cell" "$sch_net $cell" "$setup" "$work/lvs.out" \
  >"$work/netgen.log" 2>&1

if [ -f "$work/lvs.out" ]; then
  sed -n '/Subcircuit summary/,$p' "$work/lvs.out" | head -40
  cp "$work/lvs.out" "./$(basename "$layout" .spice).lvs.log"
fi

if grep -q "Circuits match uniquely" "$work/lvs.out" 2>/dev/null; then
  echo "PASS LVS: $cell"; exit 0
fi
echo "FAIL LVS: $cell"
echo "  full report: ./$(basename "$layout" .spice).lvs.log"
tail -20 "$work/netgen.log" | sed 's/^/    /'
exit 1
