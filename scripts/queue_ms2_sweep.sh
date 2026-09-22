#!/usr/bin/env bash
# Original-SIMPLER-stack verification sweep (WSL). Two workers: octo-small on 8767, octo-base on 8768.
# Tasks in priority order; variants_v1 (nominal + 5 calibration-invisible conditions); episodes 0-47.
set -uo pipefail
cd /mnt/e/research/the_world
source .venv-linux/bin/activate
source scripts/wsl_render_env.sh
export LP_NUM_THREADS=4   # bound llvmpipe threads so the ManiSkill3 jobs keep their CPU share
LOG=results/controller_sweep_ms2/queue.log
echo "queue_ms2_sweep start $(date -u +%FT%TZ)" >> "$LOG"
worker() {  # policy port
  for task in widowx_put_eggplant_in_basket widowx_spoon_on_towel widowx_carrot_on_plate; do
    echo "$(date -u +%T) start $1 $task" >> "$LOG"
    python scripts/controller_sweep_ms2.py --policy-name "$1" --policy-url "http://127.0.0.1:$2" --task "$task" --preset variants_v1 --episodes 48 --output-dir results/controller_sweep_ms2 2>&1 | grep --line-buffered -v "using WSL" > "results/controller_sweep_ms2/job_$1_${task}.log"
    echo "$(date -u +%T) done rc=${PIPESTATUS[0]} $1 $task" >> "$LOG"
  done
}
worker octo-small 8767 &
worker octo-base 8768 &
wait
echo "MS2_SWEEP_DONE $(date -u +%FT%TZ)" >> "$LOG"
