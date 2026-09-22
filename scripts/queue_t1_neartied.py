"""T1-B: bring the deployment variants into the eggplant census, to widen the set of near-tied pairs.

The point-vs-union disagreement only appears where the margin is comparable to the parameter-induced shift:
on the completed 64-configuration census the pairs with |Delta| >= 0.29 survive both verdicts and those with
|Delta| <= 0.25 do not. With only two such pairs in the cross-family case, the result rests on a thin base.
The deployment variants of the same weights (@noens: no action ensembling, @chunk4: 4-step action chunks)
sit close to their parents by construction and therefore generate more pairs in the interesting margin band,
at a quarter of the cost of a new policy family.

4 policies x 2 conditions (nominal, force x0.5) x 64 configurations x 2 seed sets = 1024 episodes, ~2.1 h.
Seeds: 20260918 -> results/controller_sweep_gpu_replayA, 20280101 -> results/controller_sweep_gpu_rep3, so the
variance is empirical and the new pairs are directly comparable with the existing ones.

Runs after T1A_PROVENANCE_DONE. Marker T1B_NEARTIED_DONE."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import PY, log, healthy, busy_ports, running_jobs, job_complete  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
ENV = "PutEggplantInBasketScene-v1"
CONDS = ["nominal", "force_x0.5"]
POLICIES = ["octo-small@noens", "octo-small@chunk4", "octo-base@noens", "octo-base@chunk4"]
PORTS = {"octo-small": [8767], "octo-base": [8768]}
SEEDS = [("20260918", "results/controller_sweep_gpu_replayA"), ("20280101", "results/controller_sweep_gpu_rep3")]
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
    wait_marker("queue_t1_provenance.out", "T1A_PROVENANCE_DONE")
    jobs = [dict(policy=p, conds=c, seed=s, out=o) for s, o in SEEDS for p in POLICIES for c in CONDS]
    log(f"=== t1b_neartied: {len(jobs)} jobs")
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
            lf = open(LOGS / "jobs" / f"t1b_{job['seed']}_{job['policy']}_{job['conds']}.out", "a", encoding="utf-8")
            running[port] = (subprocess.Popen(cmd, cwd=ROOT, stdout=lf, stderr=subprocess.STDOUT), job)
            taken.add(port)
            pending.remove(job)
            log(f"launched {job['policy']} {job['conds']} seed={job['seed']} on {port}")
        time.sleep(20)
    log("T1B_NEARTIED_DONE")


if __name__ == "__main__":
    main()
