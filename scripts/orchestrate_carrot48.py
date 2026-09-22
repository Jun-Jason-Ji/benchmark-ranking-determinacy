"""Unattended orchestration: bring the carrot task to 48 episodes per condition for both
policies, then run the analysis. Safe to re-run (idempotent, resume-aware).

Logic per policy:
  1. wait until the main sweep has finished episodes 0-23 for all 7 conditions
     (so no concurrent writes to those JSONL files);
  2. wait until the part-1 extension (nominal, stiff_x0.5, stiff_x2.0; eps 24-47) is done,
     because it uses the same extra policy server;
  3. run the part-2 extension (damp_x0.5, damp_x2.0, force_x0.5, delay_1; eps 24-47)
     on the extra server (octo-small: 8769, octo-base: 8770);
When both policies have >= 48 episodes in all 7 conditions, run analyze_controller_sweep.py
and write results/controller_sweep_gpu/analysis_carrot48.md.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/controller_sweep_gpu"
ENV = "PutCarrotOnPlateInScene-v1"
CONDS = ["nominal", "stiff_x0.5", "stiff_x2.0", "damp_x0.5", "damp_x2.0", "force_x0.5", "delay_1"]
PART1 = ["nominal", "stiff_x0.5", "stiff_x2.0"]
PART2 = ["damp_x0.5", "damp_x2.0", "force_x0.5", "delay_1"]
PORTS = {"octo-small": 8769, "octo-base": 8770}
PY = ROOT / ".venv-windows-ms3/Scripts/python.exe"


def ids(policy, cond):
    f = OUT / policy / ENV / f"{cond}.jsonl"
    if not f.exists():
        return set()
    s = set()
    for line in f.read_text(encoding="utf-8").splitlines():
        try:
            s.add(json.loads(line)["episode_id"])
        except Exception:
            pass
    return s


def log(msg):
    print(f"{time.strftime('%H:%M:%S')} {msg}", flush=True)


def main():
    launched = {}
    while True:
        status = {}
        for policy in PORTS:
            main_done = all(set(range(24)) <= ids(policy, c) for c in CONDS)
            part1_done = all(set(range(48)) <= ids(policy, c) for c in PART1)
            part2_done = all(set(range(48)) <= ids(policy, c) for c in PART2)
            status[policy] = (main_done, part1_done, part2_done)
            if main_done and part1_done and not part2_done and policy not in launched:
                cmd = [str(PY), "scripts/controller_sweep.py", "--policy-name", policy,
                       "--policy-url", f"http://127.0.0.1:{PORTS[policy]}", "--env-id", ENV,
                       "--preset", "sweep_v1", "--conditions", ",".join(PART2),
                       "--episode-offset", "24", "--episodes", "24", "--output-dir", "results/controller_sweep_gpu"]
                logf = open(ROOT / f"results/controller_sweep/logs/extend_gpu_{policy}_part2.out", "a", encoding="utf-8")
                launched[policy] = subprocess.Popen(cmd, cwd=ROOT, stdout=logf, stderr=subprocess.STDOUT)
                log(f"launched part-2 extension for {policy} (pid {launched[policy].pid})")
        log("status " + json.dumps({p: dict(main=s[0], part1=s[1], part2=s[2]) for p, s in status.items()}))
        for policy, proc in list(launched.items()):
            rc = proc.poll()
            if rc is not None:
                log(f"part-2 extension {policy} exited rc={rc}")
                if rc != 0:
                    launched.pop(policy)  # allow relaunch on next loop
        if all(s[0] and s[1] and s[2] for s in status.values()):
            break
        time.sleep(60)
    log("all 48 episodes present for both policies; running analysis")
    r = subprocess.run([str(PY), "scripts/analyze_controller_sweep.py", "--root", "results/controller_sweep_gpu",
                        "--out", "results/controller_sweep_gpu/analysis_carrot48.md"], cwd=ROOT,
                       capture_output=True, text=True, encoding="utf-8")
    log(f"analysis rc={r.returncode}")
    if r.returncode != 0:
        log(r.stderr[-2000:])
    log("ORCHESTRATE_DONE")


if __name__ == "__main__":
    main()
