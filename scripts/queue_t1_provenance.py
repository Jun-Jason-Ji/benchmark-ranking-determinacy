"""T1-A: re-collect the ms3 spoon and carrot Octo data on the current inference-server build.

Those two tasks are the medium-risk rows of results/PROVENANCE_AUDIT_2026-09-19.md: their Octo episodes were
collected before the XLA determinism flags were added, on the build that drifts against a re-run of its own
seeds (results/controller_sweep_gpu_replayA/FINDING_platform_drift.md). Until they are re-collected, every
non-eggplant Octo number in the paper has to carry a "pre-fix platform" caveat.

Both tasks have 24 distinct configurations, so a census is 24 episodes per (policy, condition, seed).
Two seed sets are collected so the policy-noise variance is empirical rather than a binomial fallback:
  seed 20260918 -> results/controller_sweep_gpu_replayA   (the A' set)
  seed 20280101 -> results/controller_sweep_gpu_rep3      (the C set)
2 policies x 6 conditions x 24 configs x 2 seeds = 576 episodes, ~1.2 h on the two servers.

Runs after MS2_OFFICIAL_DONE. Marker T1A_PROVENANCE_DONE."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import PY, log, healthy, busy_ports, running_jobs, job_complete  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
ENVS = ["PutSpoonOnTableClothInScene-v1", "PutCarrotOnPlateInScene-v1"]
CONDS = ["nominal", "iso_x0.25", "iso_x4.0", "force_x0.5", "fric_x0.4", "dens_x0.5"]
POLICIES = ["octo-small", "octo-base"]
PORTS = {"octo-small": [8767], "octo-base": [8768]}
SEEDS = [("20260918", "results/controller_sweep_gpu_replayA"), ("20280101", "results/controller_sweep_gpu_rep3")]
EPISODES = 24  # both tasks have exactly 24 configurations


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
    wait_marker("queue_ms2_official_protocol.out", "MS2_OFFICIAL_DONE")
    jobs = [dict(policy=p, env=e, conds=c, seed=s, out=o)
            for s, o in SEEDS for e in ENVS for p in POLICIES for c in CONDS]
    log(f"=== t1a_provenance: {len(jobs)} jobs")
    pending, running = list(jobs), {}
    while pending or running:
        for port, (proc, job) in list(running.items()):
            if proc.poll() is not None:
                log(f"done rc={proc.returncode} {job['policy']} {job['env']} {job['conds']} seed={job['seed']} on {port}")
                running.pop(port)
        taken = busy_ports() | set(running)
        active = running_jobs()
        for job in list(pending):
            full = dict(policy=job["policy"], env=job["env"], conds=job["conds"], offset=0, episodes=EPISODES)
            if job_complete(full, job["out"]):
                log(f"skip complete {job['policy']} {job['env']} {job['conds']} seed={job['seed']}")
                pending.remove(job)
                continue
            if (job["policy"], job["env"], job["conds"]) in active:
                continue
            base = job["policy"].split("@")[0]
            free = [p for p in PORTS[base] if p not in taken and healthy(p, base)]
            if not free:
                continue
            port = free[0]
            cmd = [str(PY), "scripts/controller_sweep.py", "--policy-name", job["policy"], "--policy-url", f"http://127.0.0.1:{port}",
                   "--env-id", job["env"], "--preset", "variants_v1", "--conditions", job["conds"], "--episode-offset", "0",
                   "--episodes", str(EPISODES), "--policy-seed-base", job["seed"], "--output-dir", job["out"]]
            (LOGS / "jobs").mkdir(parents=True, exist_ok=True)
            lf = open(LOGS / "jobs" / f"t1a_{job['seed']}_{job['policy']}_{job['env'][:12]}_{job['conds']}.out", "a", encoding="utf-8")
            running[port] = (subprocess.Popen(cmd, cwd=ROOT, stdout=lf, stderr=subprocess.STDOUT), job)
            taken.add(port)
            pending.remove(job)
            log(f"launched {job['policy']} {job['env']} {job['conds']} seed={job['seed']} on {port}")
        time.sleep(20)
    log("T1A_PROVENANCE_DONE")


if __name__ == "__main__":
    main()
