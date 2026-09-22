"""Reproduce the published SIMPLER bridge numbers under the reference RNG lifecycle.

queue_ms2_official_protocol.py matched the reference's *outer* loop -- the full 24-configuration census
repeated under init_rng in {0, 2, 4}, 72 episodes per (task, policy) -- but not its RNG lifecycle. It sent
the seed on every reset, and our server re-seeds whenever it receives one, so the 24 configurations of a
cell all replayed one identical noise realisation instead of being independent draws.

The reference seeds once per process and lets the key advance:
simpler_env/policies/octo/octo_model.py sets self.rng = jax.random.PRNGKey(init_rng) in __init__ (plus five
warm-up splits), advances it at every step, and its reset() restores task, image history, ensembler and
sticky-gripper state while never touching self.rng. One stream therefore runs through every step of every
episode of a run. `--policy-seed-stream S` sends S on the first reset and None afterwards, which our server
answers by carrying the session's key across episode boundaries; the sweep asserts the server echoed the
mode it asked for, so an un-patched server fails loudly instead of quietly re-seeding.

Output: results/controller_sweep_ms2_official_stream/seed{S}, laid out exactly like the `..._official`
directory so scripts/analyze_official_protocol.py reads either. 576 episodes across two workers.
Marker MS2_OFFICIAL_STREAM_DONE."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import log, healthy  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
OUT = "results/controller_sweep_ms2_official_stream"
TASKS = ["widowx_put_eggplant_in_basket", "widowx_spoon_on_towel", "widowx_carrot_on_plate", "widowx_stack_cube"]
SEEDS = [0, 2, 4]  # the official init_rng values
PORTS = {"octo-small": 8767, "octo-base": 8768}
WSL_PREFIX = ("cd /mnt/e/research/the_world && source .venv-linux/bin/activate && source scripts/wsl_render_env.sh && "
              "export LP_NUM_THREADS=4 && export PYTHONUNBUFFERED=1 && ")


def worker(policy, port):
    for task in TASKS:
        for seed in SEEDS:
            out = f"{OUT}/seed{seed}"
            inner = WSL_PREFIX + " ".join([
                "python", "scripts/controller_sweep_ms2.py", "--policy-name", policy,
                "--policy-url", f"http://127.0.0.1:{port}", "--task", task, "--preset", "variants_v1",
                "--conditions", "nominal", "--episodes", "24", "--episode-offset", "0",
                "--policy-seed-stream", str(seed), "--output-dir", out]) + " 2>&1 | grep --line-buffered -v 'using WSL'"
            jl = open(LOGS / "jobs" / f"ms2_stream_{policy}_{task}_seed{seed}.out", "a", encoding="utf-8")
            log(f"start {policy} {task} seed={seed}")
            rc = subprocess.call(["wsl.exe", "-e", "bash", "-c", inner], cwd=ROOT, stdout=jl, stderr=subprocess.STDOUT)
            log(f"done rc={rc} {policy} {task} seed={seed}")
            if rc != 0:
                log(f"NONZERO_RC {policy} {task} seed={seed} -- see the job log; a server without the "
                    f"stream patch raises rather than silently re-seeding")


def main():
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
    log("MS2_OFFICIAL_STREAM_DONE")


if __name__ == "__main__":
    main()
