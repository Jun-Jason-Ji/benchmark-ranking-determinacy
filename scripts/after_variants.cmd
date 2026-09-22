@echo off
setlocal
set ROOT=E:\research\the_world
set LOGS=%ROOT%\results\controller_sweep\logs
set PYTHONIOENCODING=utf-8
cd /d %ROOT%
:wait
findstr /c:"VARIANTS_QUEUE_DONE" "%LOGS%\queue_variants.out" >nul 2>&1
if errorlevel 1 (timeout /t 120 /nobreak >nul & goto wait)
"%ROOT%\.venv-windows-ms3\Scripts\python.exe" scripts\analyze_variant_pairs.py --root results\controller_sweep_gpu --out results\controller_sweep_gpu\analysis_variant_pairs.md
echo VARIANT_PAIRS_DONE
