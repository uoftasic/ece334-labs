#!/usr/bin/env bash
# Install the screenshot tooling used by scripts/capture.sh.
#
# Only needed by course staff regenerating the manual figures; students never
# run this. The IIC-OSIC-TOOLS image does not ship xdotool or ImageMagick.
#
#   docker exec -u 0 <container> /foss/designs/scripts/install_capture_deps.sh
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "install_capture_deps.sh: must run as root (docker exec -u 0 ...)" >&2
  exit 1
fi

apt-get update -qq
apt-get install -y -qq xdotool imagemagick x11-utils wmctrl
echo "capture dependencies installed:"
for c in xdotool import identify wmctrl; do
  printf '  %-10s %s\n' "$c" "$(command -v "$c" || echo MISSING)"
done
