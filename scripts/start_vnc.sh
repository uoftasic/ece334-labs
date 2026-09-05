#!/usr/bin/env bash
# Launch IIC-OSIC-TOOLS with noVNC (browser GUI). Works on Linux and macOS.
set -euo pipefail

DOCKER_TAG="${DOCKER_TAG:-2026.08}"
IMAGE="hpretl/iic-osic-tools:${DOCKER_TAG}"
CONTAINER_NAME="${CONTAINER_NAME:-ece334-osic}"
VNC_PW="${VNC_PW:-abc123}"
# Upstream image defaults to 1680x1050; a smaller desktop fits typical laptop browsers.
VNC_RESOLUTION="${VNC_RESOLUTION:-1280x800}"
HOST_PORT="${HOST_PORT:-80}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "Image:    ${IMAGE}"
echo "Mount:    ${REPO_ROOT} -> /foss/designs"
echo ""
echo "After start, open in your browser:"
echo "  EDA desktop:        http://localhost:${HOST_PORT}/  (password: ${VNC_PW}, ${VNC_RESOLUTION})"
echo "  (override resolution: VNC_RESOLUTION=1920x1080 ./scripts/start_vnc.sh)"
echo ""
echo "Lab manuals & cheatsheets are online: https://uoftasic.com/ece334-docs/"
echo ""
echo "Confirm tag ${DOCKER_TAG} on: https://github.com/iic-jku/IIC-OSIC-TOOLS/releases"

docker pull "${IMAGE}"

docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true

docker run -d --name "${CONTAINER_NAME}" \
  --shm-size=1g \
  --security-opt seccomp=unconfined \
  -p "${HOST_PORT}:80" \
  -e VNC_PW="${VNC_PW}" \
  -e XKB_KEYBOARD_LAYOUT="${XKB_KEYBOARD_LAYOUT:-us}" \
  -e VNC_RESOLUTION="${VNC_RESOLUTION}" \
  -v "${REPO_ROOT}:/foss/designs" \
  -v "${REPO_ROOT}/docker/novnc-index.html:/usr/share/novnc/index.html:ro" \
  "${IMAGE}"

echo "Container ${CONTAINER_NAME} started."
"${SCRIPT_DIR}/post_start_services.sh"
