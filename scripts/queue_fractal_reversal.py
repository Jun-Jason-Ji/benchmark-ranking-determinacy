"""The reversal pair on fractal: rt-1-converged vs rt-1-15pct on pick-coke-can, under the calibration-
invisible conditions.

Why this pair. `simpler_env/utils/metrics.py` publishes both real-robot and simulated success rates for the
same policies. On pick-coke-can the two orderings disagree on three of fifteen pairs, all among policies whose
real-world margins are 0.013-0.067. Of those three, this is the only one whose checkpoints are both public
(rt-2-x has none):

    rt-1-converged vs rt-1-15pct     real  0.853 vs 0.920  =  -0.067
                                     sim   0.857 vs 0.710  =  +0.147

So the benchmark declares an ordering the real robot reverses. The question this queue answers is whether the
compatible-set verdict abstains on that pair -- i.e. whether the criterion would have refused to make the
claim the simulator got wrong. A union bound that *declares* it would be evidence against the method, and is
the outcome most worth knowing early.

Scope (as scoped 2026-09-21): 2 policies x 3 conditions x 300 configurations = 1800 episodes. Conditions are
nominal plus the two that moved verdicts on bridge: the torque limit (exactly invisible to replay calibration,
section 4.2) and object friction. At ~30 s/episode this is ~15 h.

Servers are started and stopped here, one checkpoint at a time: each RT-1 server holds a SavedModel plus the
sentence encoder, and this machine has already hit two low-memory kills. Resumable throughout --
controller_sweep_ms2.py skips episode_ids already in the jsonl, so a kill costs only the episode in flight.

Runs after the rt-1-x validation gate. Marker FRACTAL_REVERSAL_DONE."""
import http.client
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import log  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
OUT = "results/fractal_reversal"
TASK = "google_pick_coke_can"
ENV_ID = "GraspSingleOpenedCokeCanInScene-v0"
POLICIES = ["rt-1-converged", "rt-1-15pct"]
CONDS = ["nominal", "force_x0.5", "fric_x0.4"]
EPISODES = 300
PORT = 8774
PY_WIN = ROOT / ".venv-rt1-win/Scripts/python.exe"


def health(port):
    try:
        c = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
        c.request("GET", "/health")
        r = json.loads(c.getresponse().read())
        c.close()
        return r
    except Exception:
        return None


def start_server(checkpoint, port):
    lf = open(LOGS / f"server_rt1_{checkpoint}_{port}.log", "a", encoding="utf-8")
    p = subprocess.Popen([str(PY_WIN), "scripts/rt1_policy_server.py", "--checkpoint", checkpoint,
                          "--port", str(port)], cwd=ROOT, stdout=lf, stderr=subprocess.STDOUT,
                         creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    deadline = time.time() + 900
    while time.time() < deadline:
        h = health(port)
        if h and h.get("model") == checkpoint:
            log(f"server up: {checkpoint} on {port} (startup {h.get('startup_seconds', 0):.0f}s)")
            return p
        if p.poll() is not None:
            log(f"server for {checkpoint} exited rc={p.returncode}")
            return None
        time.sleep(15)
    log(f"server for {checkpoint} did not become healthy")
    return None


def stop_server(proc, port):
    if proc is None:
        return
    try:
        proc.terminate()
        proc.wait(timeout=60)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass
    log(f"server on {port} stopped")


def episodes_done(policy, cond):
    f = ROOT / OUT / policy / ENV_ID / f"{cond}.jsonl"
    if not f.exists():
        return 0
    return len({json.loads(l)["episode_id"] for l in f.read_text(encoding="utf-8").splitlines() if l.strip()})


def run_condition(policy, cond, port):
    """One sweep process in WSL; it resumes from the jsonl, so a retry after a kill is cheap."""
    cmd = ["wsl.exe", "-e", "bash", "-lc",
           "cd /mnt/e/research/the_world && source .venv-linux/bin/activate && "
           "source scripts/wsl_render_env.sh && export LP_NUM_THREADS=4 && "
           f"python scripts/controller_sweep_ms2.py --policy-name {policy} "
           f"--policy-url http://127.0.0.1:{port} --task {TASK} --preset variants_v1 "
           f"--conditions {cond} --episodes {EPISODES} --output-dir {OUT}"]
    lf = open(LOGS / "jobs" / f"fractal_{policy}_{cond}.out", "a", encoding="utf-8")
    return subprocess.run(cmd, cwd=ROOT, stdout=lf, stderr=subprocess.STDOUT).returncode


def wait_gate(timeout_h=8):
    """The rt-1-x census must reproduce the published 0.567 before any of this is worth running."""
    f = ROOT / "results/fractal_validation/rt-1-x" / ENV_ID / "nominal.jsonl"
    deadline = time.time() + timeout_h * 3600
    while time.time() < deadline:
        if f.exists():
            rows = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
            if len({r["episode_id"] for r in rows}) >= 300:
                rate = sum(r["success"] for r in rows) / len(rows)
                log(f"gate: rt-1-x census {rate:.3f} vs published 0.567 (diff {rate - 0.567:+.3f})")
                if abs(rate - 0.567) > 0.12:
                    log("GATE FAILED: reproduction is too far from the published value; not starting the sweep")
                    return False
                return True
        time.sleep(120)
    log("gate: rt-1-x census did not finish in time; not starting the sweep")
    return False


def free_validation_server(port=8773):
    """The rt-1-x server is idle once its census is done, and it holds a SavedModel plus the sentence
    encoder. This machine has already lost two processes to low memory, so reclaim it before starting."""
    if health(port) is None:
        return
    subprocess.run(["powershell", "-NoProfile", "-Command",
                    "Get-CimInstance Win32_Process -Filter \"Name like 'python%'\" | "
                    "Where-Object { $_.CommandLine -like '*rt1_policy_server*--port " + str(port) + "*' } | "
                    "ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"],
                   cwd=ROOT, capture_output=True)
    log(f"released the idle validation server on {port}")


def main():
    (LOGS / "jobs").mkdir(parents=True, exist_ok=True)
    if not wait_gate():
        return
    free_validation_server()
    for policy in POLICIES:
        todo = [c for c in CONDS if episodes_done(policy, c) < EPISODES]
        if not todo:
            log(f"{policy}: all conditions complete")
            continue
        proc = start_server(policy, PORT)
        if proc is None:
            log(f"{policy}: no server, skipping")
            continue
        try:
            for cond in todo:
                have = episodes_done(policy, cond)
                log(f"start {policy} {cond} ({have}/{EPISODES} already done)")
                rc = run_condition(policy, cond, PORT)
                log(f"done rc={rc} {policy} {cond} -> {episodes_done(policy, cond)}/{EPISODES}")
        finally:
            stop_server(proc, PORT)
    log("FRACTAL_REVERSAL_DONE")


if __name__ == "__main__":
    main()
