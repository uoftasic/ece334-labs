#!/usr/bin/env bash
# Start the course docs portal inside the running ECE334 container.
set -euo pipefail

CONTAINER_NAME="${CONTAINER_NAME:-ece334-osic}"
DOCS_PORT="${DOCS_PORT:-8080}"
HOST_PORT="${HOST_PORT:-80}"
VNC_PW="${VNC_PW:-abc123}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Starting course portal inside ${CONTAINER_NAME}..."

ready=0
for _ in $(seq 1 45); do
  if docker exec "${CONTAINER_NAME}" true 2>/dev/null; then
    ready=1
    break
  fi
  sleep 1
done
if [ "${ready}" -ne 1 ]; then
  echo "WARNING: container ${CONTAINER_NAME} not ready — skip docs auto-start."
  exit 0
fi

CONTAINER_NAME="${CONTAINER_NAME}" "${SCRIPT_DIR}/configure_vnc_desktop.sh"

docker exec "${CONTAINER_NAME}" bash -lc "
set -e
for f in /foss/designs/common/.designinit /foss/designs/scripts/*.sh; do
  [ -f \"\$f\" ] && sed -i 's/\r$//' \"\$f\"
done
export DOCS_PORT=8080

portal_running() {
  pgrep -f 'serve_course_portal.py' >/dev/null 2>&1
}

if ! portal_running; then
  nohup python3 /foss/designs/scripts/serve_course_portal.py \
    >>/tmp/ece334-portal.log 2>&1 &
fi
"

echo ""
echo "=== Open in your browser ==="
echo "  Lab manuals (PDF):          http://localhost:${DOCS_PORT}/"
echo "  EDA desktop (XSchem, Magic):  http://localhost:${HOST_PORT}/  (password: ${VNC_PW})"
echo "  Copy/paste: use the clipboard icon in the noVNC sidebar, or Ctrl+Shift+V to paste into the VM."
echo ""
