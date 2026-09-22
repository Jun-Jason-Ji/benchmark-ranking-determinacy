@echo off
REM After the follow-up GPU queue finishes (NEXT_GPU_QUEUE_DONE), extend the carrot iso-scale extremes
REM (iso_x0.25, iso_x0.5, iso_x4.0) to 96 episodes for both policies on servers 8769/8770.
setlocal
set ROOT=E:\research\the_world
set LOGS=%ROOT%\results\controller_sweep\logs
set MS_ASSET_DIR=%ROOT%\data\maniskill-assets
cd /d %ROOT%
:wait
findstr /c:"NEXT_GPU_QUEUE_DONE" "%LOGS%\queue_next_gpu.out" >nul 2>&1
if errorlevel 1 (timeout /t 120 /nobreak >nul & goto wait)
echo ==== %DATE% %TIME% launching carrot iso-extreme extension to 96 episodes
start "" /b cmd /c ""%ROOT%\.venv-windows-ms3\Scripts\python.exe" scripts\controller_sweep.py --policy-name octo-small --policy-url http://127.0.0.1:8769 --env-id PutCarrotOnPlateInScene-v1 --preset iso_ratio_v1 --conditions iso_x0.25,iso_x0.5,iso_x4.0 --episode-offset 48 --episodes 48 --output-dir results\controller_sweep_gpu > "%LOGS%\extend_iso96_octo-small.out" 2>&1"
"%ROOT%\.venv-windows-ms3\Scripts\python.exe" scripts\controller_sweep.py --policy-name octo-base --policy-url http://127.0.0.1:8770 --env-id PutCarrotOnPlateInScene-v1 --preset iso_ratio_v1 --conditions iso_x0.25,iso_x0.5,iso_x4.0 --episode-offset 48 --episodes 48 --output-dir results\controller_sweep_gpu > "%LOGS%\extend_iso96_octo-base.out" 2>&1
:wait2
findstr /c:"== iso_x4.0" "%LOGS%\extend_iso96_octo-small.out" >nul 2>&1
if errorlevel 1 (timeout /t 60 /nobreak >nul & goto wait2)
"%ROOT%\.venv-windows-ms3\Scripts\python.exe" scripts\analyze_equiv_pairs.py --root results\controller_sweep_gpu --envs=PutCarrotOnPlateInScene-v1 --out results\controller_sweep_gpu\analysis_equiv_pairs_iso96_carrot.md > "%LOGS%\iso96_analysis.out" 2>&1
echo ISO96_DONE
