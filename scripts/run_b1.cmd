@echo off
REM Experiment B-1 driver: wait for 40 Bridge demos, then replay under sweep_v1 conditions and the
REM stiffness x damping x delay grid. CPU only; safe to run alongside the GPU policy sweeps.
setlocal
set ROOT=E:\research\the_world
set MS_ASSET_DIR=%ROOT%\data\maniskill-assets
set PYTHONIOENCODING=utf-8
cd /d %ROOT%
:wait
set /a N=0
for %%F in (data\bridge_sysid\ep_*.npz) do set /a N+=1
if %N% LSS 40 (
  echo %TIME% waiting for demos: %N%/40
  timeout /t 30 /nobreak >nul
  goto wait
)
echo ==== %DATE% %TIME% B1 sweep_v1 start
"%ROOT%\.venv-windows-ms3\Scripts\python.exe" scripts\replay_bridge_sysid.py --episodes 40 --preset sweep_v1 --output-dir results\replay_sysid
echo ==== %DATE% %TIME% B1 sweep_v1 end exit %ERRORLEVEL%
echo ==== %DATE% %TIME% B1 grid start
"%ROOT%\.venv-windows-ms3\Scripts\python.exe" scripts\replay_bridge_sysid.py --episodes 40 --grid --output-dir results\replay_sysid
echo ==== %DATE% %TIME% B1 grid end exit %ERRORLEVEL%
echo B1_DONE
