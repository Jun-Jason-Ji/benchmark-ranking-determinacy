#!/usr/bin/env bash
# Validation gate for the fractal / google-robot pipeline: reproduce the published SIMPLER value for
# octo-base on pick-coke-can (0.170) over the full 300-configuration visual-matching grid.
# Nothing else on this suite is trusted until this matches. Resumable: controller_sweep_ms2.py skips
# episode_ids already in the jsonl.
set -uo pipefail
cd /mnt/e/research/the_world
source .venv-linux/bin/activate
source scripts/wsl_render_env.sh
export LP_NUM_THREADS=4
POLICY="${1:-octo-base}"
PORT="${2:-8772}"
LOG=results/fractal_validation/validation.log
mkdir -p results/fractal_validation
echo "start $POLICY $(date -u +%FT%TZ)" >> "$LOG"
python scripts/controller_sweep_ms2.py --policy-name "$POLICY" --policy-url "http://127.0.0.1:$PORT" \
  --task google_pick_coke_can --preset quick2 --conditions nominal --episodes 300 \
  --output-dir results/fractal_validation >> "$LOG" 2>&1
echo "done rc=$? $POLICY $(date -u +%FT%TZ)" >> "$LOG"
echo "FRACTAL_VALIDATION_DONE $POLICY" >> "$LOG"
