@echo off
REM Usage: run_extend.cmd <policy-name> <port> <env-id> <episode-offset> <episodes> [outdir]
REM Appends extra episode_ids to an existing sweep directory (resume-safe: done ids are skipped).
setlocal
set POLICY=%1
set PORT=%2
set ENVID=%3
set OFFSET=%4
set EPISODES=%5
set OUTDIR=%6
if "%OUTDIR%"=="" set OUTDIR=results\controller_sweep_gpu
set ROOT=E:\research\the_world
set MS_ASSET_DIR=%ROOT%\data\maniskill-assets
cd /d %ROOT%
echo ==== %DATE% %TIME% extend %POLICY% %ENVID% offset=%OFFSET% n=%EPISODES%
"%ROOT%\.venv-windows-ms3\Scripts\python.exe" scripts\controller_sweep.py --policy-name %POLICY% --policy-url http://127.0.0.1:%PORT% --env-id %ENVID% --preset sweep_v1 --episode-offset %OFFSET% --episodes %EPISODES% --output-dir %OUTDIR%
echo ==== %DATE% %TIME% extend end %POLICY% %ENVID% exit %ERRORLEVEL%
echo EXTEND_DONE %POLICY% %ENVID%
