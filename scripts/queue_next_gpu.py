"""GPU job queue for the controller sweeps after the initial runs finish.

Waits for: SWEEP_DONE in both main sweep logs and ISO_QUEUE_DONE in the iso queue log, then runs
three phases, each a list of controller_sweep.py jobs scheduled onto per-policy servers
(octo-small: 8767, 8769; octo-base: 8768, 8770). A server never serves two clients at once.

Phase 1: sweep_v1 episodes 24-47 for spoon, eggplant, stack (both policies)
Phase 2: iso_ratio_v1 episodes 24-47 for all four tasks
Phase 3: wide_v1 episodes 0-23 for all four tasks
Resume-safe: controller_sweep.py skips episode_ids already present in the JSONL.
Log: results/controller_sweep/logs/queue_next_gpu.out (per-job logs in logs/jobs/).
"""
import http.client
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / "results/controller_sweep/logs"
JOBLOGS = LOGS / "jobs"
PY = ROOT / ".venv-windows-ms3/Scripts/python.exe"
OUT = "results/controller_sweep_gpu"
ENVS = ["PutCarrotOnPlateInScene-v1", "PutSpoonOnTableClothInScene-v1", "PutEggplantInBasketScene-v1",
        "StackGreenCubeOnYellowCubeBakedTexInScene-v1"]
SERVERS = {"octo-small": [8767, 8769], "octo-base": [8768, 8770]}


def log(msg):
    print(f"{time.strftime('%H:%M:%S')} {msg}", flush=True)


def marker(path, text):
    p = LOGS / path
    return p.exists() and text in p.read_text(encoding="utf-8", errors="replace")


def healthy(port, policy):
    try:
        c = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
        c.request("GET", "/health")
        r = json.loads(c.getresponse().read())
        c.close()
        return r.get("model") == policy
    except Exception:
        return False


def phases():
    p1 = [dict(policy=p, env=e, preset="sweep_v1", offset=24, episodes=24) for e in ENVS[1:] for p in SERVERS]
    p2 = [dict(policy=p, env=e, preset="iso_ratio_v1", offset=24, episodes=24) for e in ENVS for p in SERVERS]
    p3 = [dict(policy=p, env=e, preset="wide_v1", offset=0, episodes=24) for e in ENVS for p in SERVERS]
    return [("phase1_sweep_v1_to48", p1), ("phase2_iso_to48", p2), ("phase3_wide_v1", p3)]


def run_phase(name, jobs):
    log(f"=== {name}: {len(jobs)} jobs")
    pending = list(jobs)
    running = {}  # port -> (Popen, job)
    while pending or running:
        for port, (proc, job) in list(running.items()):
            rc = proc.poll()
            if rc is not None:
                log(f"done rc={rc} {job['policy']} {job['env']} {job['preset']} off={job['offset']} on {port}")
                running.pop(port)
        for job in list(pending):
            free = [p for p in SERVERS[job["policy"]] if p not in running and healthy(p, job["policy"])]
            if not free:
                continue
            port = free[0]
            cmd = [str(PY), "scripts/controller_sweep.py", "--policy-name", job["policy"], "--policy-url", f"http://127.0.0.1:{port}",
                   "--env-id", job["env"], "--preset", job["preset"], "--episode-offset", str(job["offset"]),
                   "--episodes", str(job["episodes"]), "--output-dir", OUT]
            JOBLOGS.mkdir(parents=True, exist_ok=True)
            lf = open(JOBLOGS / f"{name}_{job['policy']}_{job['env']}_{job['preset']}_{job['offset']}.out", "a", encoding="utf-8")
            running[port] = (subprocess.Popen(cmd, cwd=ROOT, stdout=lf, stderr=subprocess.STDOUT), job)
            pending.remove(job)
            log(f"launched {job['policy']} {job['env']} {job['preset']} off={job['offset']} on {port}")
        time.sleep(20)
    log(f"=== {name} complete")


def main():
    while not (marker("sweep_gpu_octo-small.out", "SWEEP_DONE") and marker("sweep_gpu_octo-base.out", "SWEEP_DONE")
               and marker("queue_iso_ratio.out", "ISO_QUEUE_DONE")):
        log("waiting for main sweeps and iso queue to finish")
        time.sleep(120)
    for name, jobs in phases():
        run_phase(name, jobs)
    log("NEXT_GPU_QUEUE_DONE")


if __name__ == "__main__":
    main()
