@echo off
REM Queue the iso_ratio_v1 policy sweep: wait until B-1 replay is done (B1_DONE) and the carrot-48
REM orchestrator has finished (ORCHESTRATE_DONE, which frees servers 8769/8770), then run the
REM iso-ratio sweep for both policies in parallel on those servers, tasks sequentially.
setlocal
set ROOT=E:\research\the_world
set LOGS=%ROOT%\results\controller_sweep\logs
cd /d %ROOT%
:wait
findstr /c:"B1_DONE" "%LOGS%\b1_replay.out" >nul 2>&1
if errorlevel 1 (echo %TIME% waiting for B1_DONE & timeout /t 60 /nobreak >nul & goto wait)
findstr /c:"ORCHESTRATE_DONE" "%LOGS%\orchestrate_carrot48.out" >nul 2>&1
if errorlevel 1 (echo %TIME% waiting for ORCHESTRATE_DONE & timeout /t 60 /nobreak >nul & goto wait)
echo ==== %DATE% %TIME% launching iso_ratio_v1 sweeps on 8769/8770
start "" /b cmd /c ""%ROOT%\scripts\run_sweep_octo.cmd" octo-small 8769 iso_ratio_v1 24 results\controller_sweep_gpu > "%LOGS%\sweep_gpu_iso_octo-small.out" 2>&1"
call "%ROOT%\scripts\run_sweep_octo.cmd" octo-base 8770 iso_ratio_v1 24 results\controller_sweep_gpu > "%LOGS%\sweep_gpu_iso_octo-base.out" 2>&1
echo ==== %DATE% %TIME% octo-base iso sweep finished; waiting for octo-small
:wait2
findstr /c:"SWEEP_DONE" "%LOGS%\sweep_gpu_iso_octo-small.out" >nul 2>&1
if errorlevel 1 (timeout /t 60 /nobreak >nul & goto wait2)
echo ISO_QUEUE_DONE
