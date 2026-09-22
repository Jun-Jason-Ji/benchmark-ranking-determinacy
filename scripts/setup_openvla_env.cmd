@echo off
setlocal
set ROOT=E:\research\the_world
set UV_LINK_MODE=copy
set UV_HTTP_TIMEOUT=600
cd /d %ROOT%
if not exist "%ROOT%\.venv-openvla\Scripts\python.exe" uv venv .venv-openvla --python "%ROOT%\.runtime\python-win\cpython-3.11-windows-x86_64-none\python.exe" --seed
set /a TRY=0
:retry
set /a TRY+=1
echo ==== attempt %TRY% %DATE% %TIME%
uv pip install --python "%ROOT%\.venv-openvla\Scripts\python.exe" --index-url https://download.pytorch.org/whl/cu128 "torch==2.7.1"
if errorlevel 1 (if %TRY% LSS 6 (timeout /t 60 /nobreak >nul & goto retry) else (echo OPENVLA_ENV_FAILED_TORCH & exit /b 1))
uv pip install --python "%ROOT%\.venv-openvla\Scripts\python.exe" "transformers==4.40.1" "tokenizers==0.19.1" "timm==0.9.10" "accelerate" "bitsandbytes==0.50.2" "huggingface_hub" "pillow" "numpy<2" "transforms3d" "sentencepiece" "protobuf" "einops"
if errorlevel 1 (if %TRY% LSS 6 (timeout /t 60 /nobreak >nul & goto retry) else (echo OPENVLA_ENV_FAILED_DEPS & exit /b 1))
"%ROOT%\.venv-openvla\Scripts\python.exe" -c "import torch, transformers, bitsandbytes as bnb; print('OPENVLA_ENV_OK', torch.__version__, torch.cuda.is_available(), transformers.__version__, bnb.__version__)"
