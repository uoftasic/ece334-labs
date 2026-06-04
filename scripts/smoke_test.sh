#!/usr/bin/env bash
# First-run check: tools and SKY130 PDK resolve. Run inside the container.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=/dev/null
[ -f "${REPO_ROOT}/common/.designinit" ] && . "${REPO_ROOT}/common/.designinit"

fail=0
check() {
  if command -v "$1" >/dev/null 2>&1; then
    echo "OK  $1"
  else
    echo "FAIL  $1 not found"
    fail=1
  fi
}

echo "=== ECE334 smoke test ==="
check ngspice
check xschem
check magic
check netgen

if [ -n "${PDK_ROOT:-}" ] && [ -d "${PDK_ROOT}/sky130A" ]; then
  echo "OK  PDK sky130A at ${PDK_ROOT}/sky130A"
else
  echo "FAIL  sky130A not found — run: sak-pdk sky130A"
  fail=1
fi

if ngspice -v >/dev/null 2>&1; then
  ngspice -v | head -1
fi

if [ "$fail" -eq 0 ]; then
  echo "=== All checks passed ==="
else
  echo "=== Some checks failed ==="
  exit 1
fi
