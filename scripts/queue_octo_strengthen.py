"""Octo side of the OpenVLA-torque strengthening (runs on the WSL GPU servers 8767 octo-small / 8768 octo-base,
concurrently with the OpenVLA queue on 8771; hist1 variants are served by the same base-model servers).
Eggplant only, conditions nominal + force_x0.5 (the pair that carries the replicated finding).

Config census (2026-09-19 fix): the ManiSkill3 eggplant env maps episode_id -> (position, orientation) as
episode_id % (8*8), so there are exactly 64 distinct initial configurations and episodes 64-95 are repeats of 0-31.
Every seed set is therefore run over episodes 0-63 = the complete config census; extra episodes only resample the
Octo diffusion noise on already-seen configs. Octo genuinely uses the per-episode seed (jax PRNGKey), so seed sets
A/B/C are valid independent replicates for Octo (unlike OpenVLA, which is deterministic — see
results/controller_sweep_gpu_rep3/FINDING_seed_set_bug.md).
  phase C: third seed set 20280101, episodes 0-63, four policies -> results/controller_sweep_gpu_rep3
  phase B: seed set B 20270101 extended 48-63 -> results/controller_sweep_gpu_rep
Seed set A already covers 0-95. Resume-safe (done episode_ids skipped by controller_sweep.py).
Marker OCTO_STRENGTHEN_DONE."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import PY, log, healthy, busy_ports, running_jobs, job_complete  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
ENV = "PutEggplantInBasketScene-v1"
PORTS = {"octo-small": [8767], "octo-base": [8768]}
POLICIES = ["octo-small", "octo-base", "octo-small@hist1", "octo-base@hist1"]


def phase_jobs():
    C = [dict(policy=p, conds=c, offset=0, episodes=64, seed="20280101", out="results/controller_sweep_gpu_rep3")
         for p in POLICIES for c in ("nominal", "force_x0.5")]
    B = [dict(policy=p, conds=c, offset=48, episodes=16, seed="20270101", out="results/controller_sweep_gpu_rep")
         for p in POLICIES for c in ("nominal", "force_x0.5")]
    return [("octo_seedC_census64", C), ("octo_seedB_to64", B)]


def run(name, jobs):
    log(f"=== {name}: {len(jobs)} jobs")
    pending, running = list(jobs), {}
    while pending or running:
        for port, (proc, job) in list(running.items()):
            if proc.poll() is not None:
                log(f"done rc={proc.returncode} {job['policy']} {job['conds']} seed={job['seed']} off={job['offset']} on {port}")
                running.pop(port)
        taken = busy_ports() | set(running)
        active = running_jobs()
        for job in list(pending):
            full = dict(policy=job["policy"], env=ENV, conds=job["conds"], offset=job["offset"], episodes=job["episodes"])
            if job_complete(full, job["out"]):
                log(f"skip complete {job['policy']} {job['conds']} seed={job['seed']} off={job['offset']}")
                pending.remove(job)
                continue
            if (job["policy"], ENV, job["conds"]) in active:
                continue  # same jsonl being written by another process
            base = job["policy"].split("@")[0]
            free = [p for p in PORTS[base] if p not in taken and healthy(p, base)]
            if not free:
                continue
            port = free[0]
            cmd = [str(PY), "scripts/controller_sweep.py", "--policy-name", job["policy"], "--policy-url", f"http://127.0.0.1:{port}",
                   "--env-id", ENV, "--preset", "variants_v1", "--conditions", job["conds"], "--episode-offset", str(job["offset"]),
                   "--episodes", str(job["episodes"]), "--policy-seed-base", job["seed"], "--output-dir", job["out"]]
            (LOGS / "jobs").mkdir(parents=True, exist_ok=True)
            lf = open(LOGS / "jobs" / f"octo_strengthen_{job['seed']}_{job['offset']}_{job['policy']}_{job['conds']}.out", "a", encoding="utf-8")
            running[port] = (subprocess.Popen(cmd, cwd=ROOT, stdout=lf, stderr=subprocess.STDOUT), job)
            taken.add(port)
            pending.remove(job)
            log(f"launched {job['policy']} {job['conds']} seed={job['seed']} off={job['offset']} on {port}")
        time.sleep(20)
    log(f"=== {name} complete")


def main():
    for name, jobs in phase_jobs():
        run(name, jobs)
    log("OCTO_STRENGTHEN_DONE")


if __name__ == "__main__":
    main()
