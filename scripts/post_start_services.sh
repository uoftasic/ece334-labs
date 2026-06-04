#!/usr/bin/env bash
# Post-start setup inside the running ECE334 container (clipboard sync, line endings).
set -euo pipefail

CONTAINER_NAME="${CONTAINER_NAME:-ece334-osic}"
HOST_PORT="${HOST_PORT:-80}"
VNC_PW="${VNC_PW:-abc123}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Configuring ${CONTAINER_NAME}..."

ready=0
for _ in $(seq 1 45); do
  if docker exec "${CONTAINER_NAME}" true 2>/dev/null; then
    ready=1
    break
  fi
  sleep 1
done
if [ "${ready}" -ne 1 ]; then
  echo "WARNING: container ${CONTAINER_NAME} not ready — skip post-start setup."
  exit 0
fi

CONTAINER_NAME="${CONTAINER_NAME}" "${SCRIPT_DIR}/configure_vnc_desktop.sh"

docker exec "${CONTAINER_NAME}" bash -lc "
set -e
for f in /foss/designs/common/.designinit /foss/designs/scripts/*.sh; do
  [ -f \"\$f\" ] && sed -i 's/\r$//' \"\$f\"
done
"

echo ""
echo "=== Open in your browser ==="
echo "  EDA desktop (XSchem, Magic):  http://localhost:${HOST_PORT}/  (password: ${VNC_PW})"
echo "  Lab manuals & cheatsheets:    https://ece334.github.io/ece334-docs/"
echo "  Copy/paste: use the clipboard icon in the noVNC sidebar, or Ctrl+Shift+V to paste into the VM."
echo ""
