#!/usr/bin/env bash
# Full B-1 replay on the original SIMPLER main stack (WSL, CPU, headless): sweep_v1 + iso_ratio_v1 + 5x5x2 grid, 98 demos.
set -uo pipefail
cd /mnt/e/research/the_world
source .venv-linux/bin/activate
export PYTHONUNBUFFERED=1
LOG=results/replay_sysid_ms2/run.log
echo "run_replay_ms2 start $(date -u +%FT%TZ)" >> "$LOG"
for spec in "--preset sweep_v1" "--preset iso_ratio_v1" "--grid"; do
  python scripts/replay_bridge_sysid_ms2.py --episodes 100 $spec --output-dir results/replay_sysid_ms2 2>&1 | grep -v -i "using WSL" >> "$LOG"
done
echo "REPLAY_MS2_ALL_DONE $(date -u +%FT%TZ)" >> "$LOG"
