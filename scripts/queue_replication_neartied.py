"""Second seed set for the eggplant near-tied policy set {octo-small, octo-base, octo-small@hist1, octo-base@hist1}:
variants_v1 (nominal + 5 calibration-invisible conditions), episodes 0-47, policy seed base 20270101, output
root results/controller_sweep_gpu_rep. Any "decidable / flip" claim needs >= 2 seed sets (FINDING_eggplant_friction.md).

Scheduling (fills otherwise idle servers without delaying the user-approved queues):
  phase 1 (after HIST1_96_DONE): octo-base, octo-base@hist1 on 8768/8770 -- the spoon queue only uses octo-small servers.
  phase 2 (after the OpenVLA server is up and its sweep is running): octo-small, octo-small@hist1 on 8767 only.
Port/condition contention is handled by queue_v2.busy_ports / running_jobs (respects other schedulers).
"""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import PY, log, healthy, busy_ports, running_jobs, job_complete  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
OUT2 = "results/controller_sweep_gpu_rep"
ENV = "PutEggplantInBasketScene-v1"
CONDS = ["nominal", "iso_x0.25", "iso_x4.0", "force_x0.5", "fric_x0.4", "dens_x0.5"]
SEED_BASE = "20270101"


def wait_marker(fname, marker):
    while True:
        f = LOGS / fname
        if f.exists() and marker in f.read_text(encoding="utf-8", errors="replace"):
            return
        time.sleep(120)


def run(name, jobs, ports):
    """jobs: dicts(policy, conds); ports: allowed server ports (all for one base model)."""
    log(f"=== {name}: {len(jobs)} jobs on {ports}")
    pending, running = list(jobs), {}
    while pending or running:
        for port, (proc, job) in list(running.items()):
            if proc.poll() is not None:
                log(f"done rc={proc.returncode} {job['policy']} {job['conds']} on {port}")
                running.pop(port)
        taken = busy_ports() | set(running)
        active = running_jobs()
        for job in list(pending):
            full = dict(policy=job["policy"], env=ENV, conds=job["conds"], offset=0, episodes=48)
            if job_complete(full, OUT2):
                log(f"skip complete {job['policy']} {job['conds']}")
                pending.remove(job)
                continue
            if (job["policy"], ENV, job["conds"]) in active:
                continue
            base = job["policy"].split("@")[0]
            free = [p for p in ports if p not in taken and healthy(p, base)]
            if not free:
                continue
            port = free[0]
            cmd = [str(PY), "scripts/controller_sweep.py", "--policy-name", job["policy"], "--policy-url", f"http://127.0.0.1:{port}",
                   "--env-id", ENV, "--preset", "variants_v1", "--conditions", job["conds"], "--episode-offset", "0", "--episodes", "48",
                   "--policy-seed-base", SEED_BASE, "--output-dir", OUT2]
            (LOGS / "jobs").mkdir(parents=True, exist_ok=True)
            lf = open(LOGS / "jobs" / f"repnt_{job['policy']}_{job['conds']}.out", "a", encoding="utf-8")
            running[port] = (subprocess.Popen(cmd, cwd=ROOT, stdout=lf, stderr=subprocess.STDOUT), job)
            taken.add(port)
            pending.remove(job)
            log(f"launched {job['policy']} {job['conds']} on {port}")
        time.sleep(20)
    log(f"=== {name} complete")


def main():
    wait_marker("queue_hist1_96.out", "HIST1_96_DONE")
    run("rep_neartied_base", [dict(policy=p, conds=c) for p in ("octo-base", "octo-base@hist1") for c in CONDS], [8768, 8770])
    log("REP_NEARTIED_BASE_DONE")
    # phase 2 must not delay the OpenVLA start: wait until its server is up (or the queue gave up)
    while True:
        t = (LOGS / "queue_openvla.out").read_text(encoding="utf-8", errors="replace") if (LOGS / "queue_openvla.out").exists() else ""
        if "openvla server ready" in t or "OPENVLA_SERVER_FAILED" in t or "OPENVLA_QUEUE_DONE" in t:
            break
        time.sleep(120)
    run("rep_neartied_small", [dict(policy=p, conds=c) for p in ("octo-small", "octo-small@hist1") for c in CONDS], [8767])
    log("REP_NEARTIED_SMALL_DONE")
    r = subprocess.run([str(PY), "scripts/analyze_seed_replication_pairs.py"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    log(f"analysis rc={r.returncode} {r.stderr[-300:] if r.returncode else ''}")
    log("REP_NEARTIED_DONE")


if __name__ == "__main__":
    main()
