#!/usr/bin/env bash
# Render an XSchem schematic to a PNG figure for the manual. Runs headless.
#
#   instructors/figures/export_schematic.sh <cell.sch> <out.png> [density]
#
# Why this and not a screenshot: the export is vector, on white, already
# zoomed to fit, and carries no window chrome or dark canvas. It is also the
# student's own schematic rather than a redrawing of it, so a figure cannot
# drift away from the cell it documents.
set -euo pipefail
sch="${1:?usage: export_schematic.sh <cell.sch> <out.png> [density]}"
out="${2:?usage: export_schematic.sh <cell.sch> <out.png> [density]}"
density="${3:-150}"
DESIGNS="${DESIGNS:-/foss/designs}"

[ -f "$sch" ] || { echo "no such schematic: $sch" >&2; exit 2; }
sch="$(realpath "$sch")"   # xschem runs from $work below, so fix the path now

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

# xschem writes plot.pdf into the current directory, so give it one of its own.
( cd "$work" && timeout 180 xschem --pdf -c -q -x \
    --rcfile "${DESIGNS}/common/xschem/exportrc" "$sch" ) >"$work/log" 2>&1 || true

if [ ! -s "$work/plot.pdf" ]; then
  echo "FAIL export: $sch" >&2; tail -5 "$work/log" >&2; exit 1
fi

mkdir -p "$(dirname "$out")"
convert -density "$density" -background white -alpha remove -alpha off \
        -trim +repage -bordercolor white -border 20 "$work/plot.pdf" "$out"
echo "ok $sch -> $out ($(identify -format '%wx%h' "$out"))"
