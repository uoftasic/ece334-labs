#!/usr/bin/env bash
# Strip Windows CRLF from course shell/config files bind-mounted from a Windows host.
# Safe to run repeatedly; no-op when files already use LF.
set -euo pipefail

DESIGNS="${1:-/foss/designs}"

fix_file() {
  local f="$1"
  [ -f "$f" ] || return 0
  if grep -q $'\r' "$f" 2>/dev/null; then
    sed -i 's/\r$//' "$f"
    echo "fixed CRLF: $f"
  fi
}

while IFS= read -r -d '' f; do
  fix_file "$f"
done < <(find "$DESIGNS" -type f \( \
  -name '*.sh' \
  -o -name '.designinit' \
  -o -name '.magicrc' \
  -o -name 'xschemrc' \
  \) -print0 2>/dev/null)
