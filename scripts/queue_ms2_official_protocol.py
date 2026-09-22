"""Reproduce the published SIMPLER bridge numbers with the official protocol, on the original stack.

scripts/octo_bridge.sh (SimplerEnv main) evaluates every bridge task as `--obj-episode-range 0 24` under
`for init_rng in 0 2 4`, i.e. **the full 24-configuration census repeated under three policy seeds, 72 episodes**,
with one seed held fixed for a whole run (OctoInference seeds jax.random.PRNGKey(init_rng) at every reset).
Our sweeps instead used policy_seed = base + episode_id, which is a different (finer) scheme, so the numbers were
never directly comparable with the published table. `--policy-seed-fixed` reproduces the official scheme.

Published sim success (simpler_env/utils/metrics.py, SIMPLER_SUCCESS): spoon octo-base 0.125 / octo-small 0.472;
carrot 0.083 / 0.097; stack 0.000 / 0.042; eggplant 0.431 / 0.569 -- all n/72.

Runs after T1_UNION_HIST1_DONE (the last Octo queue) so the GPU is not contended. Two workers (octo-small 8767, octo-base 8768; the
servers are session-isolated, verified 2026-09-19). Output: results/controller_sweep_ms2_official.
Marker MS2_OFFICIAL_DONE."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import log, healthy  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
OUT = "results/controller_sweep_ms2_official"
TASKS = ["widowx_put_eggplant_in_basket", "widowx_spoon_on_towel", "widowx_carrot_on_plate", "widowx_stack_cube"]
SEEDS = [0, 2, 4]  # the official init_rng values
PORTS = {"octo-small": 8767, "octo-base": 8768}
WSL_PREFIX = ("cd /mnt/e/research/the_world && source .venv-linux/bin/activate && source scripts/wsl_render_env.sh && "
              "export LP_NUM_THREADS=4 && export PYTHONUNBUFFERED=1 && ")


def wait_marker(fname, marker, timeout_h=24):
    deadline = time.time() + timeout_h * 3600
    while time.time() < deadline:
        f = LOGS / fname
        if f.exists() and marker in f.read_text(encoding="utf-8", errors="replace"):
            return True
        time.sleep(120)
    log(f"marker {marker} not seen within {timeout_h} h; starting anyway")
    return False


def worker(policy, port):
    for task in TASKS:
        for seed in SEEDS:
            out = f"{OUT}/seed{seed}"
            inner = WSL_PREFIX + " ".join([
                "python", "scripts/controller_sweep_ms2.py", "--policy-name", policy,
                "--policy-url", f"http://127.0.0.1:{port}", "--task", task, "--preset", "variants_v1",
                "--conditions", "nominal", "--episodes", "24", "--episode-offset", "0",
                "--policy-seed-fixed", str(seed), "--output-dir", out]) + " 2>&1 | grep --line-buffered -v 'using WSL'"
            jl = open(LOGS / "jobs" / f"ms2_official_{policy}_{task}_seed{seed}.out", "a", encoding="utf-8")
            log(f"start {policy} {task} seed={seed}")
            rc = subprocess.call(["wsl.exe", "-e", "bash", "-c", inner], cwd=ROOT, stdout=jl, stderr=subprocess.STDOUT)
            log(f"done rc={rc} {policy} {task} seed={seed}")


def main():
    wait_marker("queue_t1_union_hist1.out", "T1_UNION_HIST1_DONE")
    (LOGS / "jobs").mkdir(parents=True, exist_ok=True)
    for policy, port in PORTS.items():
        if not healthy(port, policy):
            log(f"SERVER_NOT_HEALTHY {policy}:{port}")
            return
    import threading
    ts = [threading.Thread(target=worker, args=(p, port)) for p, port in PORTS.items()]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    log("MS2_OFFICIAL_DONE")


if __name__ == "__main__":
    main()
