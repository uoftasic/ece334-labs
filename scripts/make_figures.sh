#!/usr/bin/env bash
# Regenerate the tool screenshots for the Lab 0 and Lab 1 manuals.
#
#   docker exec -e DISPLAY=:1 <container> /foss/designs/scripts/make_figures.sh
#
# Staff-only. Needs xdotool and ImageMagick: scripts/install_capture_deps.sh.
# Waveform figures are NOT made here -- they come from matplotlib via
# instructors/figures/make_waveform_figs.py so they carry real axes and
# annotations.
#
# Dialogs are opened with `xschem --command`, never synthetic mouse events:
# clicking at guessed coordinates selects the wrong object, and a stray drag
# silently edits the schematic being photographed.
set -uo pipefail
DESIGNS="${DESIGNS:-/foss/designs}"
OUT="${1:-/tmp/figs}"
CAP="${DESIGNS}/scripts/capture.sh"
SOL="${DESIGNS}/instructors"
export DISPLAY="${DISPLAY:-:1}"

mkdir -p "$OUT"

# A scratch lab holding the student files with the reference solutions laid on
# top, so the figures show completed circuits. Named lab0_* so that it sorts
# ahead of the real labs on XSCHEM_LIBRARY_PATH and therefore wins.
SCRATCH="${DESIGNS}/lab0_figures"
# Remove a stale scratch left by a killed run: it would otherwise sit on
# XSCHEM_LIBRARY_PATH and shadow the real labs.
rm -rf "$SCRATCH"
rm -rf "$SCRATCH"; mkdir -p "$SCRATCH/xschem"
cp -a "${DESIGNS}/lab1_spice/xschem/." "$SCRATCH/xschem/"
cp -a "${SOL}/lab1/xschem/."           "$SCRATCH/xschem/"
cp -a "${SOL}/lab0/xschem/."           "$SCRATCH/xschem/"
cp -a "${DESIGNS}/common/xschem/."     "$SCRATCH/xschem/"
trap 'rm -rf "$SCRATCH"' EXIT

kill_xschem() { pkill -x xschem 2>/dev/null; sleep 1; }
kill_magic()  { pkill -x magic  2>/dev/null; sleep 1; }

# shot <file.sch> <out.png> [WxH] [extra xdotool keys...]
shot() {
  local sch="$1" png="$2" size="${3:-1200x820}"; shift 3 || true
  kill_xschem
  ( cd "$SCRATCH/xschem" && nohup xschem "$sch" >/dev/null 2>&1 & )
  sleep 9
  local id
  id="$(xdotool search --name "^xschem - ${sch}$" | tail -1)"
  if [ -z "$id" ]; then echo "MISS window for $sch" >&2; return 1; fi
  xdotool windowsize "$id" "${size%x*}" "${size#*x}"; sleep 1
  xdotool windowactivate "$id"; sleep 1
  xdotool key --window "$id" f; sleep 2          # zoom to fit
  for k in "$@"; do xdotool key --window "$id" "$k"; sleep 1; done
  import -window "$id" "${OUT}/${png}"
  echo "wrote ${OUT}/${png}"
}

echo "== Lab 1 schematics =="
shot rc_tb.sch        01-rc-testbench.png  1250x820
shot dut_diode.sch    03-diode-dut.png     1100x780
shot dut_inv.sch      05-inv-dut.png       1000x780
shot pulsegen_tb.sch  08-pulsegen-tb.png   1350x850

echo "== Lab 0 cells =="
shot inv.sch          L0-07-inverter-wired.png  950x740
shot nand2.sch        L0-09-nand2-schematic.png 1000x800
shot pulsegen_gate_tb.sch L0-10-pulsegen-hierarchy.png 1400x860

# dlg <out.png> <window-regex> <WxH> -- capture a dialog already on screen
dlg() {
  local png="$1" name="$2" size="$3" id
  id="$(xdotool search --name "$name" | tail -1)"
  [ -n "$id" ] || { echo "MISS dialog $name" >&2; return 1; }
  xdotool windowsize "$id" "${size%x*}" "${size#*x}" 2>/dev/null
  sleep 1; xdotool windowactivate "$id"; sleep 1
  import -window "$id" "${OUT}/${png}"
  echo "wrote ${OUT}/${png}"
}

echo "== Lab 0 tool interface =="
# Blank canvas: what the student sees on first launch.
kill_xschem
( cd "$SCRATCH/xschem" && nohup xschem >/dev/null 2>&1 & )
sleep 10
BLANK="$(xdotool search --name "^xschem - " | tail -1)"
if [ -n "$BLANK" ]; then
  xdotool windowsize "$BLANK" 1150x780; sleep 1; xdotool windowactivate "$BLANK"; sleep 2
  import -window "$BLANK" "${OUT}/L0-03-xschem-window.png"
  echo "wrote ${OUT}/L0-03-xschem-window.png"
  # The "Choose symbol" browser is deliberately not captured: its file pane
  # only populates after a real click on a library row, and synthetic clicks do
  # not register on that widget. A screenshot of the empty pane would mislead.
fi

# Instance property editor, opened without touching the mouse.
kill_xschem
( cd "$SCRATCH/xschem" && nohup xschem --command \
    "xschem select instance 0; xschem edit_prop" inv.sch >/dev/null 2>&1 & )
sleep 12
dlg L0-06-edit-properties.png "^Edit Properties$" 900x300 || true

# The inverter's symbol view -- what the cell looks like once it has one.
shot inv.sym L0-08-inverter-symbol.png 900x700 || true

kill_xschem
kill_magic
echo "done. tool screenshots in ${OUT}"
