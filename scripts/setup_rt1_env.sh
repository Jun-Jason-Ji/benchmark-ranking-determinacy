#!/usr/bin/env bash
# Build the RT-1 inference environment (WSL, CPU TensorFlow).
#
# RT-1 ships as a TF SavedModel loaded through tf_agents' eager policy wrapper, which is a different stack
# from the Octo (jax) and OpenVLA (torch) servers, so it gets its own venv. CPU only, deliberately: RT-1 is
# ~35M parameters, the 8 GB card is already held by the Octo servers, and the fractal sweep is CPU-rendered
# anyway, so the GPU build would buy nothing and cost VRAM we do not have.
#
# Versions are the ones SimplerEnv pins (README + requirements_full_install.txt): tensorflow 2.15.0,
# tf_agents 0.19.0, tensorflow_hub 0.16.0, numpy<2. The SavedModels were exported against that line and
# tf_agents is strict about it.
#
# The language embedding is the Universal Sentence Encoder that RT-1 was trained with. tfhub.dev now 302s
# to Kaggle, which still serves the archive without credentials, so TFHUB_CACHE_DIR is pointed at a local
# directory and the model is fetched once here rather than on the first evaluation episode.
set -euo pipefail
cd /mnt/e/research/the_world
# Log from inside the script: piping through the Windows->WSL command line mangles quoting
# (a bare `numpy<2.0` on that command line becomes a shell redirect).
mkdir -p results/controller_sweep/logs
exec > >(tee -a results/controller_sweep/logs/setup_rt1_env.log) 2>&1
echo "=== setup_rt1_env start $(date -u +%FT%TZ) ==="
VENV="${VENV:-.venv-rt1}"
export TFHUB_CACHE_DIR=/mnt/e/models/tfhub

# WSL only ships python3.12, which tensorflow 2.15 does not support. This project already bootstraps a
# standalone CPython 3.11 under .runtime (no sudo, no system packages), so use that one.
PY311=/mnt/e/research/the_world/.runtime/python/cpython-3.11.16-linux-x86_64-gnu/bin/python3.11
if [ ! -x "$PY311" ]; then echo "missing $PY311"; exit 1; fi
if [ ! -d "$VENV" ]; then
  "$PY311" -m venv "$VENV"
fi
source "$VENV/bin/activate"
python -m pip install --upgrade pip wheel setuptools

pip install "numpy<2.0" "tensorflow==2.15.0" "tf_agents==0.19.0" "tensorflow_hub==0.16.0" transforms3d pillow

mkdir -p "$TFHUB_CACHE_DIR"
python - <<'PY'
import os
import tensorflow as tf, tf_agents, tensorflow_hub as hub, numpy as np
print("tensorflow", tf.__version__, "| tf_agents", tf_agents.__version__, "| numpy", np.__version__)
print("devices:", [d.device_type for d in tf.config.list_physical_devices()])
# Fetch and cache the sentence encoder now, so an evaluation run never blocks on the network.
m = hub.load("https://tfhub.dev/google/universal-sentence-encoder-large/5")
v = m(["pick coke can"])
print("USE ok, embedding shape", tuple(v.shape), "cache", os.environ["TFHUB_CACHE_DIR"])
PY
echo "RT1_ENV_READY"
