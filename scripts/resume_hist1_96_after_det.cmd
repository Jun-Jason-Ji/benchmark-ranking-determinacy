@echo off
setlocal
set ROOT=E:\research\the_world
set LOGS=%ROOT%\results\controller_sweep\logs
set MS_ASSET_DIR=%ROOT%\data\maniskill-assets
cd /d %ROOT%
:wait
findstr /c:"DETERMINISM_DONE" "%LOGS%\queue_determinism.out" >nul 2>&1
if errorlevel 1 (timeout /t 60 /nobreak >nul & goto wait)
echo ==== %DATE% %TIME% resuming eggplant near-tied 96 queue
"%ROOT%\.venv-windows-ms3\Scripts\python.exe" scripts\queue_hist1_96.py >> "%LOGS%\queue_hist1_96.out" 2>> "%LOGS%\queue_hist1_96.err"
