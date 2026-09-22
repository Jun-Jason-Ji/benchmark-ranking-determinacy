@echo off
rem Relaunch the three schedulers on the hardened queue_v2 (busy_ports regex; skip complete/running jobs).
setlocal
set ROOT=E:\research\the_world
set LOGS=%ROOT%\results\controller_sweep\logs
set MS_ASSET_DIR=%ROOT%\data\maniskill-assets
cd /d %ROOT%
echo ==== %DATE% %TIME% restarted scheduler after busy_ports crash (%1) >> "%LOGS%\%1.out"
"%ROOT%\.venv-windows-ms3\Scripts\python.exe" scripts\%1.py >> "%LOGS%\%1.out" 2>> "%LOGS%\%1.err"
