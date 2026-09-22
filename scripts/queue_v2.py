"""GPU job queue v2 (replaces queue_next_gpu.py mid-run). Reprioritised:
  Phase A: carrot iso-scale extremes (iso_x0.25, iso_x0.5, iso_x4.0) episodes 48-95, both policies
  Phase B: remaining iso_ratio_v1 to 48 (spoon/eggplant/stack; resume-safe, done ids skipped)
  Phase C: wide_v1 episodes 0-23, four tasks
Then runs the carrot equivalent-pairs analysis at 96 and writes NEXT_GPU_QUEUE_DONE.

A server is considered busy if any controller_sweep.py process (from any scheduler) targets its port,
so jobs orphaned by the previous queue are respected. Servers: octo-small 8767/8769, octo-base 8768/8770.
"""
import http.client
import json
import re
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


def healthy(port, policy):
    try:
        c = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
        c.request("GET", "/health")
        r = json.loads(c.getresponse().read())
        c.close()
        return r.get("model") == policy
    except Exception:
        return False


def _sweep_cmdlines():
    try:
        out = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command",
             "(Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' -and $_.CommandLine -like '*scripts/controller_sweep.py*' }).CommandLine"],
            text=True, timeout=60)
    except Exception:
        return []
    return [l for l in out.splitlines() if l.strip()]


_PORT_RE = re.compile(r"--policy-url\s+http://127\.0\.0\.1:(\d+)")


def busy_ports():
    """Ports targeted by any running controller_sweep.py process on this machine (robust to foreign command lines)."""
    ports = set()
    for line in _sweep_cmdlines():
        m = _PORT_RE.search(line)
        if m:
            ports.add(int(m.group(1)))
    return ports


def running_jobs():
    """(policy, env, condition-or-None) triples of running controller_sweep.py processes."""
    def arg(line, name):
        m = re.search(name + r"\s+(\S+)", line)
        return m.group(1) if m else None
    return {(arg(l, "--policy-name"), arg(l, "--env-id"), arg(l, "--conditions")) for l in _sweep_cmdlines()}


def job_complete(job, out_dir):
    """True when the job targets a single condition whose jsonl already holds every requested episode_id."""
    if not job["conds"] or "," in job["conds"]:
        return False
    f = ROOT / out_dir / job["policy"] / job["env"] / f"{job['conds']}.jsonl"
    if not f.exists():
        return False
    have = set()
    for line in f.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                have.add(json.loads(line)["episode_id"])
            except Exception:
                pass
    return set(range(job["offset"], job["offset"] + job["episodes"])) <= have


def phases():
    A = [dict(policy=p, env=ENVS[0], preset="iso_ratio_v1", conds="iso_x0.25,iso_x0.5,iso_x4.0", offset=48, episodes=48) for p in SERVERS]
    B = [dict(policy=p, env=e, preset="iso_ratio_v1", conds=None, offset=24, episodes=24) for e in ENVS[1:] for p in SERVERS]
    C = [dict(policy=p, env=e, preset="wide_v1", conds=None, offset=0, episodes=24) for e in ENVS for p in SERVERS]
    return [("phaseA_carrot_iso96", A), ("phaseB_iso_to48", B), ("phaseC_wide_v1", C)]


def run_phase(name, jobs):
    log(f"=== {name}: {len(jobs)} jobs")
    pending, running = list(jobs), {}
    while pending or running:
        for port, (proc, job) in list(running.items()):
            if proc.poll() is not None:
                log(f"done rc={proc.returncode} {job['policy']} {job['env']} {job['preset']} off={job['offset']} on {port}")
                running.pop(port)
        taken = busy_ports() | set(running)
        active = running_jobs()
        for job in list(pending):
            if job_complete(job, OUT):
                log(f"skip complete {job['policy']} {job['env']} {job['conds']} off={job['offset']}")
                pending.remove(job)
                continue
            if (job["policy"], job["env"], job["conds"]) in active:
                continue  # same condition already being written by another process; wait (avoids duplicate records)
            base = job["policy"].split("@")[0]
            free = [p for p in SERVERS[base] if p not in taken and healthy(p, base)]
            if not free:
                continue
            port = free[0]
            cmd = [str(PY), "scripts/controller_sweep.py", "--policy-name", job["policy"], "--policy-url", f"http://127.0.0.1:{port}",
                   "--env-id", job["env"], "--preset", job["preset"], "--episode-offset", str(job["offset"]),
                   "--episodes", str(job["episodes"]), "--output-dir", OUT]
            if job["conds"]:
                cmd += ["--conditions", job["conds"]]
            JOBLOGS.mkdir(parents=True, exist_ok=True)
            lf = open(JOBLOGS / f"{name}_{job['policy']}_{job['env']}_{job['preset']}_{job['offset']}.out", "a", encoding="utf-8")
            running[port] = (subprocess.Popen(cmd, cwd=ROOT, stdout=lf, stderr=subprocess.STDOUT), job)
            taken.add(port)
            pending.remove(job)
            log(f"launched {job['policy']} {job['env']} {job['preset']} off={job['offset']} on {port}")
        time.sleep(20)
    log(f"=== {name} complete")


def main():
    for name, jobs in phases():
        run_phase(name, jobs)
        if name == "phaseA_carrot_iso96":
            r = subprocess.run([str(PY), "scripts/analyze_equiv_pairs.py", "--root", OUT, "--envs=PutCarrotOnPlateInScene-v1",
                                "--out", f"{OUT}/analysis_equiv_pairs_iso96_carrot.md"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
            log(f"ISO96_ANALYSIS rc={r.returncode}")
    log("NEXT_GPU_QUEUE_DONE")


if __name__ == "__main__":
    main()
