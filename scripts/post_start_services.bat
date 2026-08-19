@echo off
REM Post-start setup inside the ECE334 container (Windows): clipboard sync, line endings.
setlocal
if not defined CONTAINER_NAME set CONTAINER_NAME=ece334-osic
if not defined HOST_PORT set HOST_PORT=80
if not defined VNC_PW set VNC_PW=abc123
set SCRIPT_DIR=%~dp0

echo Configuring %CONTAINER_NAME%...
REM `timeout` needs a console handle and fails when stdin is redirected,
REM which is what happens when this file is run from a script rather than
REM double-clicked. ping is portable and needs no console.
ping -n 4 127.0.0.1 >nul

bash "%SCRIPT_DIR%configure_vnc_desktop.sh" 2>nul

REM Windows Git often checks out CRLF; strip before bash sources these files in the container.
docker exec %CONTAINER_NAME% bash -lc "for f in /foss/designs/common/.designinit /foss/designs/scripts/*.sh; do [ -f \"\$f\" ] && sed -i 's/\r$//' \"\$f\"; done"

echo.
echo === Open in your browser ===
echo   EDA desktop (XSchem, Magic):  http://localhost:%HOST_PORT%/  (password: %VNC_PW%)
echo   Lab manuals ^& cheatsheets:    https://uoftasic.com/ece334-docs/
echo   Copy/paste: use the clipboard icon in the noVNC sidebar, or Ctrl+Shift+V to paste into the VM.
echo.
endlocal
