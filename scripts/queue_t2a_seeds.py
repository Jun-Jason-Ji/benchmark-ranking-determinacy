"""T2-A: take the eggplant census from S=3 to S=5 seed sets, so that a persisting point-vs-union
disagreement can no longer be explained by evaluation budget.

Why this is the decisive experiment. As the evaluation half-width h shrinks, the union bound converges to
[min_c delta_c, max_c delta_c] over the calibration-invisible conditions, and that span does NOT shrink with
budget. So at infinite budget a union abstention means the per-condition deltas genuinely disagree in sign --
a fact about the simulator parameters. At finite budget an abstention can instead mean the intervals are
merely wide -- a fact about our noise. More seed sets is the only way to separate the two.

Two of the three disagreeing pairs are internal to Octo (octo-small vs octo-base@hist1, octo-base vs
octo-base@hist1); the third, octo-base@hist1 vs OpenVLA, hangs on torque x0.5 where the census interval is
+0.068 [-0.000, +0.135] -- grazing zero. All three are tightened by Octo seed sets alone: OpenVLA is
deterministic and its census is already exact.

4 policies x 6 conditions x 64 configurations x 2 new seed sets = 3072 episodes, ~5 h on the two servers.
Seeds: 20290101 -> results/controller_sweep_gpu_rep4 (D), 20300101 -> results/controller_sweep_gpu_rep5 (E),
continuing the existing bases (A' 20260918, B 20270101, C 20280101).

Runs after T1B_NEARTIED_DONE. Marker T2A_SEEDS_DONE."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import PY, log, healthy, busy_ports, running_jobs, job_complete  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
ENV = "PutEggplantInBasketScene-v1"
CONDS = ["nominal", "force_x0.5", "iso_x0.25", "iso_x4.0", "fric_x0.4", "dens_x0.5"]
POLICIES = ["octo-small", "octo-base", "octo-small@hist1", "octo-base@hist1"]
PORTS = {"octo-small": [8767], "octo-base": [8768]}
SEEDS = [("20290101", "results/controller_sweep_gpu_rep4"), ("20300101", "results/controller_sweep_gpu_rep5")]
EPISODES = 64


def wait_marker(fname, marker, timeout_h=24):
    deadline = time.time() + timeout_h * 3600
    while time.time() < deadline:
        f = LOGS / fname
        if f.exists() and marker in f.read_text(encoding="utf-8", errors="replace"):
            return True
        time.sleep(120)
    log(f"marker {marker} not seen within {timeout_h} h; starting anyway")
    return False


def main():
    wait_marker("queue_t1_neartied.out", "T1B_NEARTIED_DONE")
    # Conditions that bind the union bound first, so that a night cut short still answers the question the
    # queue was launched for: torque is where the cross-family pair grazes zero, density is where the one
    # genuine per-condition sign reversal sits.
    order = {"force_x0.5": 0, "dens_x0.5": 1, "nominal": 2, "fric_x0.4": 3, "iso_x0.25": 4, "iso_x4.0": 5}
    jobs = [dict(policy=p, conds=c, seed=s, out=o) for s, o in SEEDS for c in sorted(CONDS, key=order.get) for p in POLICIES]
    log(f"=== t2a_seeds: {len(jobs)} jobs")
    pending, running = list(jobs), {}
    while pending or running:
        for port, (proc, job) in list(running.items()):
            if proc.poll() is not None:
                log(f"done rc={proc.returncode} {job['policy']} {job['conds']} seed={job['seed']} on {port}")
                running.pop(port)
        taken = busy_ports() | set(running)
        active = running_jobs()
        for job in list(pending):
            full = dict(policy=job["policy"], env=ENV, conds=job["conds"], offset=0, episodes=EPISODES)
            if job_complete(full, job["out"]):
                log(f"skip complete {job['policy']} {job['conds']} seed={job['seed']}")
                pending.remove(job)
                continue
            if (job["policy"], ENV, job["conds"]) in active:
                continue
            base = job["policy"].split("@")[0]
            free = [p for p in PORTS[base] if p not in taken and healthy(p, base)]
            if not free:
                continue
            port = free[0]
            cmd = [str(PY), "scripts/controller_sweep.py", "--policy-name", job["policy"], "--policy-url", f"http://127.0.0.1:{port}",
                   "--env-id", ENV, "--preset", "variants_v1", "--conditions", job["conds"], "--episode-offset", "0",
                   "--episodes", str(EPISODES), "--policy-seed-base", job["seed"], "--output-dir", job["out"]]
            (LOGS / "jobs").mkdir(parents=True, exist_ok=True)
            lf = open(LOGS / "jobs" / f"t2a_{job['seed']}_{job['policy']}_{job['conds']}.out", "a", encoding="utf-8")
            running[port] = (subprocess.Popen(cmd, cwd=ROOT, stdout=lf, stderr=subprocess.STDOUT), job)
            taken.add(port)
            pending.remove(job)
            log(f"launched {job['policy']} {job['conds']} seed={job['seed']} on {port}")
        time.sleep(20)
    log("T2A_SEEDS_DONE")


if __name__ == "__main__":
    main()
