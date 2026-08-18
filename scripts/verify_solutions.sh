#!/usr/bin/env bash
# Verify that a lab is completable, using the reference solutions.
#
#   scripts/verify_solutions.sh lab1_spice lab1
#
# Student files are never modified. The lab's xschem directory is copied to a
# scratch lab, the matching instructors/<name>/xschem files are laid over the
# copy, and the scratch lab is netlisted and simulated.
#
# The scratch directory is named lab0_solcheck on purpose: common/xschemrc adds
# every /foss/designs/lab*/xschem to XSCHEM_LIBRARY_PATH in sorted order, and an
# earlier entry wins, so this name shadows the real lab rather than the reverse.
set -uo pipefail
LAB="${1:?usage: verify_solutions.sh <labdir> <instructors-subdir>}"
REF="${2:?usage: verify_solutions.sh <labdir> <instructors-subdir>}"
DESIGNS="${DESIGNS:-/foss/designs}"
SCRATCH="${DESIGNS}/lab0_solcheck"
# Remove a stale scratch left by a killed run: it would otherwise sit on
# XSCHEM_LIBRARY_PATH and shadow the real labs.
rm -rf "$SCRATCH"

[ -d "${DESIGNS}/${LAB}/xschem" ]        || { echo "no ${LAB}/xschem" >&2; exit 2; }
[ -d "${DESIGNS}/instructors/${REF}/xschem" ] || { echo "no instructors/${REF}/xschem" >&2; exit 2; }

rm -rf "$SCRATCH"
trap 'rm -rf "$SCRATCH"' EXIT
mkdir -p "$SCRATCH/xschem" "$SCRATCH/spice"
cp -a "${DESIGNS}/${LAB}/xschem/." "$SCRATCH/xschem/"
cp -a "${DESIGNS}/instructors/${REF}/xschem/." "$SCRATCH/xschem/"

echo "verifying ${LAB} with instructors/${REF} solutions laid over it"
"${DESIGNS}/scripts/verify_lab.sh" lab0_solcheck
