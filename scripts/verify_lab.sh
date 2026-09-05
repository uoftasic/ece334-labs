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
    # An unbuilt DUT netlists to a subcircuit with no contents. Whether that is
    # caught later depends on whether the .control block happens to reference a
    # net that no longer exists, so check for it directly.
    empty="$(awk '
      /^[.]subckt/ { name=$2; body=0; next }
      /^[.]ends/   { if (name != "" && body == 0) print name; name=""; next }
      { if (name != "" && $0 !~ /^[*]/ && $0 !~ /^[[:space:]]*$/ && $0 !~ /^[+]/) body++ }
    ' "$deck")"
    if [ -n "$empty" ]; then
      echo "FAIL empty subcircuit(s) in $name: $(echo $empty | tr '\n' ' ')"
      echo "     the DUT has not been built yet"
      fail=1; continue
    fi

    # Netlisting cleanly is not enough either: simulate the generated deck and
    # insist it runs without error.
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
    # Skip include-only netlists: a file with no analysis statement is a
    # subcircuit library, not a deck, and ngspice exits non-zero on it.
    # An analysis can be a .tran card at the top level OR a bare `tran` inside
    # a .control block -- decks that drive two analyses have to use the latter,
    # and matching only the dotted form silently stops verifying them.
    if ! grep -qE '^[[:space:]]*\.(tran|dc|ac|op|noise)' "$deck" \
       && ! grep -qE '^[[:space:]]*(tran|dc|ac|op|noise)[[:space:]]' "$deck"; then
      echo "skip include-only: $name"; continue
    fi
    # Decks differ in what directory their relative .include paths assume.
    # lab4's want spice/ as the cwd (.include include/dff.spice); lab2's want
    # the lab root, because the netlists magic extracts land there and the
    # manual runs them as `ngspice -b spice/<deck>`. Try spice/ first, then the
    # lab root, and only fail when neither resolves.
    ran=""
    if (cd "$LABDIR/spice" && timeout 300 ngspice -b "$name" >"$work/$name.log" 2>&1); then
      ran="spice"
    elif grep -q "Could not find include file" "$work/$name.log" 2>/dev/null &&
         (cd "$LABDIR" && timeout 300 ngspice -b "spice/$name" >"$work/$name.log" 2>&1); then
      ran="labroot"
    fi
    if [ -z "$ran" ]; then
      echo "FAIL simulate: $name"; tail -15 "$work/$name.log" | sed 's/^/    /'; fail=1
      continue
    fi
    outdir="$LABDIR/spice"; [ "$ran" = labroot ] && outdir="$LABDIR"

    # Exiting zero is not the same as producing the right data. A deck with two
    # .control blocks is the specific way that goes wrong: `reset` restores the
    # circuit to its FIRST analysis, so the second `run` repeats it and the
    # second output file is a copy of the first. Catch it directly, by checking
    # that the files the deck names are actually different from each other.
    outs="$(grep -oE '^[[:space:]]*(wrdata|write)[[:space:]]+[^[:space:]]+' "$deck" \
            | awk '{print $2}' | sort -u)"
    n_out="$(echo "$outs" | grep -c . || true)"
    if [ "$n_out" -gt 1 ]; then
      dup=""
      for a in $outs; do
        for b in $outs; do
          [ "$a" \< "$b" ] || continue
          [ -f "$outdir/$a" ] && [ -f "$outdir/$b" ] || continue
          cmp -s "$outdir/$a" "$outdir/$b" && dup="$a and $b"
        done
      done
      if [ -n "$dup" ]; then
        echo "FAIL identical outputs in $name: $dup"
        echo "     the deck names two outputs and wrote the same data to both;"
        echo "     check for a second .control block ($(grep -c '^[.]control' "$deck") found)"
        fail=1; continue
      fi
    fi
    echo "ok   simulate: $name"
  done
fi

[ "$fail" -eq 0 ] && echo "PASS $LAB" || echo "FAIL $LAB"
exit "$fail"
