"""T1-0: the invisible conditions for the @hist1 variants, which carry three of the four disagreements.

Checking the per-condition deltas of the four pairs where point calibration and the union bound disagree on the
completed eggplant census showed that three of them abstain only because one condition's interval grazes zero,
and in every such case that condition has a single run:

  octo-small@hist1 vs OpenVLA   all six deltas positive (+0.115 .. +0.438); iso_x0.25 [-0.01, +0.26], 1 run
  octo-base@hist1  vs OpenVLA   all six positive (+0.068 .. +0.312);        iso_x0.25 [-0.02, +0.23], 1 run
  octo-small vs octo-base@hist1 all six positive;                           fric/dens graze zero, 1 run
  octo-base  vs octo-base@hist1 dens_x0.5 delta = -0.021                    <- a genuine sign disagreement

As the evaluation half-width goes to zero the union interval converges to [min_c delta_c, max_c delta_c], which
does not shrink: an abstention is then a fact about the parameters. With one run per condition an abstention can
equally be a fact about the budget. Separating the two is exactly what a second seed buys, so without this queue
the headline "four disagreements" is partly an artefact of our own power.

queue_octo_union_conds covers octo-small and octo-base only; this queue adds the two @hist1 variants over the
same four conditions, 64 configurations and two seed sets: 2 x 4 x 64 x 2 = 1024 episodes, ~2.1 h.

Runs after UNION_CONDS_DONE. Marker T1_UNION_HIST1_DONE."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import PY, log, healthy, busy_ports, running_jobs, job_complete  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
ENV = "PutEggplantInBasketScene-v1"
CONDS = ["iso_x0.25", "iso_x4.0", "fric_x0.4", "dens_x0.5"]
POLICIES = ["octo-small@hist1", "octo-base@hist1"]
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
    wait_marker("queue_octo_union_conds.out", "UNION_CONDS_DONE")
    jobs = [dict(policy=p, conds=c, seed=s, out=o) for s, o in SEEDS for p in POLICIES for c in CONDS]
    log(f"=== t1_union_hist1: {len(jobs)} jobs")
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
            lf = open(LOGS / "jobs" / f"t1u_{job['seed']}_{job['policy']}_{job['conds']}.out", "a", encoding="utf-8")
            running[port] = (subprocess.Popen(cmd, cwd=ROOT, stdout=lf, stderr=subprocess.STDOUT), job)
            taken.add(port)
            pending.remove(job)
            log(f"launched {job['policy']} {job['conds']} seed={job['seed']} on {port}")
        time.sleep(20)
    log("T1_UNION_HIST1_DONE")


if __name__ == "__main__":
    main()
