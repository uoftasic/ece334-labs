@echo off
REM Start course docs portal inside the ECE334 container (Windows).
setlocal
if not defined CONTAINER_NAME set CONTAINER_NAME=ece334-osic
if not defined DOCS_PORT set DOCS_PORT=8080
if not defined HOST_PORT set HOST_PORT=80
if not defined VNC_PW set VNC_PW=abc123
set SCRIPT_DIR=%~dp0

echo Starting course portal inside %CONTAINER_NAME%...
timeout /t 3 /nobreak >nul

bash "%SCRIPT_DIR%configure_vnc_desktop.sh" 2>nul

REM Windows Git often checks out CRLF; strip before bash sources these files in the container.
docker exec %CONTAINER_NAME% bash -lc "for f in /foss/designs/common/.designinit /foss/designs/scripts/*.sh; do [ -f \"\$f\" ] && sed -i 's/\r$//' \"\$f\"; done"

docker exec %CONTAINER_NAME% bash -lc "export DOCS_PORT=8080; portal_running() { pgrep -f serve_course_portal.py >/dev/null 2>&1; }; if ! portal_running; then nohup python3 /foss/designs/scripts/serve_course_portal.py >>/tmp/ece334-portal.log 2>&1 & fi"

echo.
echo === Open in your browser ===
echo   Lab manuals (PDF):          http://localhost:%DOCS_PORT%/
echo   EDA desktop (XSchem, Magic):  http://localhost:%HOST_PORT%/  (password: %VNC_PW%)
echo   Copy/paste: use the clipboard icon in the noVNC sidebar, or Ctrl+Shift+V to paste into the VM.
echo.
endlocal
