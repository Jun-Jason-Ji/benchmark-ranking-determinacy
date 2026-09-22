"""Re-collect seed set A on the current servers, so that all three Octo seed sets come from one platform generation.

Seed set A (results/controller_sweep_gpu) was collected on 2026-09-18 16:46 local, before the XLA determinism flags
(--xla_gpu_deterministic_ops / --xla_gpu_autotune_level=0) were added to run_wsl_server.sh; sets B (09-18 23:05) and
C (09-19 20:34) came after. On the eggplant census A disagrees with both later sets -- Δ(small−base) nominal
+0.250 vs −0.031 and −0.047, octo-base 0.297 vs 0.516 and 0.500 -- and an earlier determinism check (results/
controller_sweep_gpu_det) already showed the same seeds giving octo-base 6/24 before and 9/24 after a server
restart. "Seed set" and "server generation" are therefore confounded in the existing data.

This queue re-runs A's seeds (policy_seed_base 20260918) over the full 64-configuration census on today's servers
for the core-case conditions, giving a seed set A' that is comparable with B and C. Output:
results/controller_sweep_gpu_replayA (the two nominal jobs may already be there from the manual replay; they are
skipped when complete). Marker OCTO_RECOLLECT_DONE."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import PY, log, healthy, busy_ports, running_jobs, job_complete  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
ENV = "PutEggplantInBasketScene-v1"
OUT = "results/controller_sweep_gpu_replayA"
SEED = "20260918"
PORTS = {"octo-small": [8767], "octo-base": [8768]}
POLICIES = ["octo-small", "octo-base", "octo-small@hist1", "octo-base@hist1"]
CONDS = ["nominal", "force_x0.5"]


def wait_marker(fname, marker, timeout_h=6):
    deadline = time.time() + timeout_h * 3600
    while time.time() < deadline:
        f = LOGS / fname
        if f.exists() and marker in f.read_text(encoding="utf-8", errors="replace"):
            return True
        time.sleep(60)
    log(f"marker {marker} not seen within {timeout_h} h; starting anyway")
    return False


def main():
    wait_marker("queue_octo_strengthen.out", "OCTO_STRENGTHEN_DONE")
    jobs = [dict(policy=p, conds=c) for p in POLICIES for c in CONDS]
    log(f"=== octo_recollect_A: {len(jobs)} jobs")
    pending, running = list(jobs), {}
    while pending or running:
        for port, (proc, job) in list(running.items()):
            if proc.poll() is not None:
                log(f"done rc={proc.returncode} {job['policy']} {job['conds']} on {port}")
                running.pop(port)
        taken = busy_ports() | set(running)
        active = running_jobs()
        for job in list(pending):
            full = dict(policy=job["policy"], env=ENV, conds=job["conds"], offset=0, episodes=64)
            if job_complete(full, OUT):
                log(f"skip complete {job['policy']} {job['conds']}")
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
                   "--episodes", "64", "--policy-seed-base", SEED, "--output-dir", OUT]
            (LOGS / "jobs").mkdir(parents=True, exist_ok=True)
            lf = open(LOGS / "jobs" / f"recollectA_{job['policy']}_{job['conds']}.out", "a", encoding="utf-8")
            running[port] = (subprocess.Popen(cmd, cwd=ROOT, stdout=lf, stderr=subprocess.STDOUT), job)
            taken.add(port)
            pending.remove(job)
            log(f"launched {job['policy']} {job['conds']} on {port}")
        time.sleep(20)
    log("OCTO_RECOLLECT_DONE")


if __name__ == "__main__":
    main()
