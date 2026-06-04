#!/usr/bin/env bash
# Enable VNC clipboard sync inside a running IIC-OSIC-TOOLS container.
# TigerVNC needs vncconfig; Xfce often needs autocutsel for PRIMARY/CLIPBOARD.
set -euo pipefail

CONTAINER_NAME="${CONTAINER_NAME:-ece334-osic}"
DISPLAY_NUM="${VNC_DISPLAY:-:1}"

if ! docker exec "${CONTAINER_NAME}" true 2>/dev/null; then
  echo "WARNING: container ${CONTAINER_NAME} not running — skip VNC desktop setup."
  exit 0
fi

if ! docker exec "${CONTAINER_NAME}" bash -lc "command -v autocutsel >/dev/null 2>&1"; then
  docker exec -u root "${CONTAINER_NAME}" bash -lc \
    "DEBIAN_FRONTEND=noninteractive apt-get update -qq \
     && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq autocutsel" \
    2>/dev/null || true
fi

docker exec "${CONTAINER_NAME}" bash -lc "
set -e
export DISPLAY='${DISPLAY_NUM}'

start_if_missing() {
  local pattern=\$1
  shift
  if pgrep -f \"\$pattern\" >/dev/null 2>&1; then
    return 0
  fi
  \"\$@\" >/dev/null 2>&1 &
}

if command -v vncconfig >/dev/null 2>&1; then
  start_if_missing 'vncconfig' vncconfig -iconic -display '${DISPLAY_NUM}'
fi

if command -v autocutsel >/dev/null 2>&1; then
  start_if_missing 'autocutsel.*CLIPBOARD' autocutsel -fork
  start_if_missing 'autocutsel.*PRIMARY' autocutsel -fork -s PRIMARY
fi
" 2>/dev/null || echo "WARNING: VNC clipboard helpers could not be started."
