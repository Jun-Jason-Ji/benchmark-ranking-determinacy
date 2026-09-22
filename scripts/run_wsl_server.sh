#!/usr/bin/env bash
# Usage (from WSL): bash /mnt/e/research/the_world/scripts/run_wsl_server.sh <octo-small|octo-base> <port>
# Runs the Octo policy server on the GPU inside WSL2 using the ~/venvs/octo-gpu environment.
set -euo pipefail
MODEL="${1:-octo-small}"
PORT="${2:-8767}"
cd /mnt/e/research/the_world
source "$HOME/venvs/${OCTO_VENV:-octo-gpu2}/bin/activate"   # octo-gpu2: jax 0.5.3 CUDA (Blackwell-capable); octo-gpu (jax 0.4.30) fails with sm_90a ptxas error
export JAX_PLATFORMS=cuda
export XLA_PYTHON_CLIENT_PREALLOCATE=false
# Overridable so an extra short-lived server (e.g. a fractal validation run alongside a queue that
# already holds two servers) can be given a smaller slice of the 8 GB card.
export XLA_PYTHON_CLIENT_MEM_FRACTION=${XLA_MEM_FRACTION:-0.35}
export HF_HOME=/mnt/e/models/hf
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1   # WSL outbound network is flaky; weights + t5-base tokenizer are already in the Windows-side cache
export TF_CPP_MIN_LOG_LEVEL=2
export PYTHONUNBUFFERED=1
# deterministic GPU numerics across server restarts (autotuning otherwise picks different conv algorithms per process)
export XLA_FLAGS="--xla_gpu_deterministic_ops=true --xla_gpu_autotune_level=0"
echo "run_wsl_server.sh start model=$MODEL port=$PORT $(date -u +%FT%TZ)"
exec python scripts/octo_policy_server.py --model "$MODEL" --port "$PORT" --host 0.0.0.0
