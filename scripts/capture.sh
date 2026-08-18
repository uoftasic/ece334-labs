#!/usr/bin/env bash
# Capture one X window to a PNG. Runs inside the container with DISPLAY set.
#
#   capture.sh --window '^xschem - inv_tb' --out /tmp/f.png --size 1200x820
#
# Requires xdotool and ImageMagick's `import`. Both are installed by
# scripts/install_capture_deps.sh if the image does not already carry them.
set -euo pipefail
WIN=""; OUT=""; SIZE=""; SETTLE=2
while [ $# -gt 0 ]; do
  case "$1" in
    --window) WIN="$2"; shift 2 ;;
    --out)    OUT="$2"; shift 2 ;;
    --size)   SIZE="$2"; shift 2 ;;
    --settle) SETTLE="$2"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done
: "${WIN:?--window required}" "${OUT:?--out required}"
export DISPLAY="${DISPLAY:-:1}"

for cmd in xdotool import; do
  command -v "$cmd" >/dev/null 2>&1 || {
    echo "capture.sh: $cmd not found; run scripts/install_capture_deps.sh" >&2
    exit 3
  }
done

id=""
for _ in $(seq 1 40); do
  id="$(xdotool search --name "$WIN" 2>/dev/null | tail -1 || true)"
  [ -n "$id" ] && break
  sleep 0.5
done
[ -n "$id" ] || { echo "capture.sh: window not found: $WIN" >&2; exit 1; }

if [ -n "$SIZE" ]; then
  xdotool windowsize "$id" "${SIZE%x*}" "${SIZE#*x}"
fi
xdotool windowactivate "$id" 2>/dev/null || true
xdotool windowraise "$id" 2>/dev/null || true
sleep "$SETTLE"
mkdir -p "$(dirname "$OUT")"
import -window "$id" "$OUT"
identify "$OUT"
