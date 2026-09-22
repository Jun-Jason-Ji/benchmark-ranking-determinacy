@echo off
setlocal
set ROOT=E:\research\the_world
set LOGS=%ROOT%\results\controller_sweep\logs
set PYTHONIOENCODING=utf-8
cd /d %ROOT%
:wait
findstr /c:"B1 grid end" "%LOGS%\b1_replay.out" >nul 2>&1
if errorlevel 1 (timeout /t 60 /nobreak >nul & goto wait)
echo ==== %DATE% %TIME% grid finished; running iso-ratio invariance check on the grid
"%ROOT%\.venv-windows-ms3\Scripts\python.exe" scripts\check_iso_invariance.py --dir results\replay_sysid\grid
echo GRID_CHECK_DONE
