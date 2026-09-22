@echo off
REM Usage: run_sweep_octo.cmd <policy-name> <port> [preset] [episodes]
REM Runs the controller sweep sequentially over Bridge tasks against a running policy server.
setlocal
set POLICY=%1
set PORT=%2
set PRESET=%3
if "%PRESET%"=="" set PRESET=sweep_v1
set EPISODES=%4
if "%EPISODES%"=="" set EPISODES=24
set OUTDIR=%5
if "%OUTDIR%"=="" set OUTDIR=results\controller_sweep
set ROOT=E:\research\the_world
set MS_ASSET_DIR=%ROOT%\data\maniskill-assets
cd /d %ROOT%
for %%E in (PutCarrotOnPlateInScene-v1 PutSpoonOnTableClothInScene-v1 PutEggplantInBasketScene-v1 StackGreenCubeOnYellowCubeBakedTexInScene-v1) do (
  echo ==== %DATE% %TIME% start %POLICY% %%E
  "%ROOT%\.venv-windows-ms3\Scripts\python.exe" scripts\controller_sweep.py --policy-name %POLICY% --policy-url http://127.0.0.1:%PORT% --env-id %%E --preset %PRESET% --episodes %EPISODES% --output-dir %OUTDIR%
  echo ==== %DATE% %TIME% end %POLICY% %%E exit %ERRORLEVEL%
)
echo SWEEP_DONE %POLICY%
