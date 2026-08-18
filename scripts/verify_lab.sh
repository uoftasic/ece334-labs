#!/usr/bin/env bash
# Netlist and simulate everything in a lab directory. Exit non-zero on any failure.
# Usage (inside the container):  scripts/verify_lab.sh lab1_spice
set -uo pipefail
LAB="${1:?usage: verify_lab.sh <labdir>}"
DESIGNS="${DESIGNS:-/foss/designs}"
LABDIR="${DESIGNS}/${LAB}"
[ -d "$LABDIR" ] || { echo "no such lab: $LABDIR" >&2; exit 2; }

fail=0
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

if [ -d "$LABDIR/xschem" ]; then
  for sch in "$LABDIR"/xschem/*_tb.sch; do
    [ -e "$sch" ] || continue
    name="$(basename "$sch" .sch)"
    out="$work/$name"; mkdir -p "$out"
    # xschem's exit status is not a reliable success signal in batch netlist mode
    # (a schematic carrying a multi-command .control block exits 10 while writing
    # a perfectly good deck). The deck itself is the oracle: it must exist and
    # contain no unresolved symbols.
    timeout 180 xschem -n -s -q -x -o "$out" "$sch" >"$out/log" 2>&1
    rc=$?
    deck="$out/$name.spice"
    if [ ! -f "$deck" ]; then
      echo "FAIL netlist(no deck, xschem exit $rc): $name"
      tail -5 "$out/log" | sed 's/^/    /'
      fail=1; continue
    fi
    n_missing="$(grep -c 'IS MISSING' "$deck" || true)"
    if [ "$n_missing" -ne 0 ]; then
      echo "FAIL netlist($n_missing missing symbols): $name"
      grep 'IS MISSING' "$deck" | sed 's/^/    /'
      fail=1; continue
    fi
    # Netlisting cleanly is not enough: a DUT whose schematic is an empty stub
    # netlists without complaint and then fails at 'write' with "no writable
    # vector found". Simulate the generated deck and insist it produces output.
    if ! (cd "$out" && timeout 300 ngspice -b "$name.spice" >sim.log 2>&1); then
      echo "FAIL simulate(netlisted): $name"; tail -12 "$out/sim.log" | sed 's/^/    /'
      fail=1; continue
    fi
    if grep -qiE "^Error|Error during|could not find a valid modelname" "$out/sim.log"; then
      echo "FAIL simulate(netlisted, errors): $name"
      grep -iE "^Error|Error during|could not find a valid modelname" "$out/sim.log" \
        | head -5 | sed 's/^/    /'
      fail=1; continue
    fi
    echo "ok   netlist+sim: $name"
  done
fi

if [ -d "$LABDIR/spice" ]; then
  for deck in "$LABDIR"/spice/*.spice; do
    [ -e "$deck" ] || continue
    name="$(basename "$deck")"
    if (cd "$LABDIR/spice" && timeout 300 ngspice -b "$name" >"$work/$name.log" 2>&1); then
      echo "ok   simulate: $name"
    else
      echo "FAIL simulate: $name"; tail -15 "$work/$name.log" | sed 's/^/    /'; fail=1
    fi
  done
fi

[ "$fail" -eq 0 ] && echo "PASS $LAB" || echo "FAIL $LAB"
exit "$fail"
