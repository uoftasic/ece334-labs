@echo off
REM Launch IIC-OSIC-TOOLS with noVNC on Windows (Docker Desktop required)
setlocal
if not defined DOCKER_TAG set DOCKER_TAG=2026.04
if not defined CONTAINER_NAME set CONTAINER_NAME=ece334-osic
if not defined VNC_PW set VNC_PW=abc123
if not defined VNC_RESOLUTION set VNC_RESOLUTION=1280x800
if not defined HOST_PORT set HOST_PORT=80
if not defined DOCS_PORT set DOCS_PORT=8080

set IMAGE=hpretl/iic-osic-tools:%DOCKER_TAG%
set REPO_ROOT=%~dp0..
set SCRIPT_DIR=%~dp0

echo Image:    %IMAGE%
echo Mount:    %REPO_ROOT% -^> /foss/designs
echo.
echo After start, open in your browser:
echo   Lab manuals (PDF):  http://localhost:%DOCS_PORT%/
echo   EDA desktop:        http://localhost:%HOST_PORT%/  (password: %VNC_PW%, %VNC_RESOLUTION%)

docker pull %IMAGE%
docker rm -f %CONTAINER_NAME% 2>nul
docker run -d --name %CONTAINER_NAME% --shm-size=1g --security-opt seccomp=unconfined -p %HOST_PORT%:80 -p %DOCS_PORT%:8080 -e VNC_PW=%VNC_PW% -e VNC_RESOLUTION=%VNC_RESOLUTION% -v "%REPO_ROOT%:/foss/designs" -v "%REPO_ROOT%/docker/novnc-index.html:/usr/share/novnc/index.html:ro" %IMAGE%
echo Container %CONTAINER_NAME% started.
call "%SCRIPT_DIR%post_start_services.bat"
endlocal
