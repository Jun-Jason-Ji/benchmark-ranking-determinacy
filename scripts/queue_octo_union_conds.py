"""Union-bound conditions on the current server generation, so the compatible-set verdict does not rest on
pre-fix data.

The union bound over the calibration-invisible conditions (iso x0.25, iso x4.0, fric x0.4, dens x0.5) currently
uses Octo data from seed set A, collected before the XLA determinism flags were added -- the generation that was
shown to drift (results/controller_sweep_gpu_replayA/FINDING_platform_drift.md). This queue re-collects those
four conditions on today's servers over the full 64-configuration census, under two seeds (A's base 20260918 ->
results/controller_sweep_gpu_replayA, and C's base 20280101 -> results/controller_sweep_gpu_rep3), for the two
headline policies. 2 policies x 4 conditions x 64 configs x 2 seeds = 1024 episodes, ~4 h on two servers.

Runs after OPENVLA_CENSUS_DONE. Marker UNION_CONDS_DONE."""
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
POLICIES = ["octo-small", "octo-base"]
CONDS = ["iso_x0.25", "iso_x4.0", "fric_x0.4", "dens_x0.5"]
SEEDS = [("20260918", "results/controller_sweep_gpu_replayA"), ("20280101", "results/controller_sweep_gpu_rep3")]


def wait_marker(fname, marker, timeout_h=18):
    deadline = time.time() + timeout_h * 3600
    while time.time() < deadline:
        f = LOGS / fname
        if f.exists() and marker in f.read_text(encoding="utf-8", errors="replace"):
            return True
        time.sleep(120)
    log(f"marker {marker} not seen within {timeout_h} h; starting anyway")
    return False


def main():
    wait_marker("queue_openvla_census.out", "OPENVLA_CENSUS_DONE")
    jobs = [dict(policy=p, conds=c, seed=s, out=o) for s, o in SEEDS for p in POLICIES for c in CONDS]
    log(f"=== octo_union_conds: {len(jobs)} jobs")
    pending, running = list(jobs), {}
    while pending or running:
        for port, (proc, job) in list(running.items()):
            if proc.poll() is not None:
                log(f"done rc={proc.returncode} {job['policy']} {job['conds']} seed={job['seed']} on {port}")
                running.pop(port)
        taken = busy_ports() | set(running)
        active = running_jobs()
        for job in list(pending):
            full = dict(policy=job["policy"], env=ENV, conds=job["conds"], offset=0, episodes=64)
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
                   "--episodes", "64", "--policy-seed-base", job["seed"], "--output-dir", job["out"]]
            (LOGS / "jobs").mkdir(parents=True, exist_ok=True)
            lf = open(LOGS / "jobs" / f"union_{job['seed']}_{job['policy']}_{job['conds']}.out", "a", encoding="utf-8")
            running[port] = (subprocess.Popen(cmd, cwd=ROOT, stdout=lf, stderr=subprocess.STDOUT), job)
            taken.add(port)
            pending.remove(job)
            log(f"launched {job['policy']} {job['conds']} seed={job['seed']} on {port}")
        time.sleep(20)
    log("UNION_CONDS_DONE")


if __name__ == "__main__":
    main()
