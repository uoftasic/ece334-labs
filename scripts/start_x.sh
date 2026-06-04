#!/usr/bin/env bash
# Launch IIC-OSIC-TOOLS with local X11 (Linux / macOS + XQuartz). Faster than noVNC.
set -euo pipefail

DOCKER_TAG="${DOCKER_TAG:-2026.04}"
IMAGE="hpretl/iic-osic-tools:${DOCKER_TAG}"
CONTAINER_NAME="${CONTAINER_NAME:-ece334-osic-x11}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

: "${DISPLAY:?Set DISPLAY (e.g. :0 or host.docker.internal:0 on Mac)}"

docker pull "${IMAGE}"
docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true

docker run -it --rm --name "${CONTAINER_NAME}" \
  -e DISPLAY="${DISPLAY}" \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v "${REPO_ROOT}:/foss/designs" \
  "${IMAGE}"
