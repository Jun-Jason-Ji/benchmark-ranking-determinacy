"""After the spoon re-run queue and the replication re-run queue finish: restart the two long-lived Octo
servers (8767 octo-small, 8768 octo-base) on the session-isolated server code, wait for health with
session_isolation=True, then launch the original-stack (ms2) sweep in WSL. 8769/8770 are left to the
OpenVLA queue (which stops them to free VRAM). Logs to results/controller_sweep/logs/orchestrate_session_restart.out."""
import http.client
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import busy_ports, log  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
RESTART = {"octo-small": 8767, "octo-base": 8768}


def health(port):
    try:
        c = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
        c.request("GET", "/health")
        r = json.loads(c.getresponse().read())
        c.close()
        return r
    except Exception:
        return None


def text(name):
    f = LOGS / name
    return f.read_text(encoding="utf-8", errors="replace") if f.exists() else ""


def main():
    while not (text("queue_spoon_hist1_96.out").count("SPOON_HIST1_96_DONE") >= 2 and "REP_RECONTAM_DONE" in text("queue_recontam_rep.out")):
        time.sleep(60)
    log("re-run queues finished")
    while busy_ports():
        log(f"waiting for sweep jobs on {sorted(busy_ports())}")
        time.sleep(30)
    for model, port in RESTART.items():
        log(f"restarting {model} on {port} with session-isolated server code")
        subprocess.run(["wsl.exe", "-e", "bash", "-c", f"pkill -f 'octo_policy_server.py --model {model} --port {port} '; sleep 3"], timeout=60)
        lf = open(LOGS / f"server_wsl_{model}_{port}.restart.log", "a", encoding="utf-8")
        subprocess.Popen(["wsl.exe", "-e", "bash", "/mnt/e/research/the_world/scripts/run_wsl_server.sh", model, str(port)],
                         stdout=lf, stderr=subprocess.STDOUT, cwd=ROOT, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
        time.sleep(20)
    deadline = time.time() + 1200
    while time.time() < deadline:
        hs = {p: health(p) for p in RESTART.values()}
        ok = {p: bool(h and h.get("session_isolation")) for p, h in hs.items()}
        log(f"health session_isolation: {ok}")
        if all(ok.values()):
            break
        time.sleep(30)
    else:
        log("SESSION_RESTART_FAILED")
        return
    log("SESSION_RESTART_DONE")
    subprocess.Popen(["wsl.exe", "-e", "bash", "/mnt/e/research/the_world/scripts/queue_ms2_sweep.sh"], cwd=ROOT,
                     creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    log("MS2_SWEEP_LAUNCHED")


if __name__ == "__main__":
    main()
