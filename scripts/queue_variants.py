"""Deployment-variant policy study. Waits for CONTACT_EXT_DONE, restarts the four WSL GPU servers so
they run the current octo_policy_server.py (variant support), then runs variants_v1 (nominal + 5
calibration-invisible perturbations, 24 episodes) for octo-{small,base}@{noens,chunk4,hist1} on
eggplant and spoon, and finally the pairwise analysis over all 8 policies."""
import http.client
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import run_phase, SERVERS, PY, OUT, log  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
ENVS = ["PutEggplantInBasketScene-v1", "PutSpoonOnTableClothInScene-v1"]
VARIANTS = ["noens", "chunk4", "hist1"]


def health(port):
    try:
        c = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
        c.request("GET", "/health")
        r = json.loads(c.getresponse().read())
        c.close()
        return r
    except Exception:
        return None


def restart_servers():
    log("stopping WSL policy servers")
    subprocess.run(["wsl.exe", "-e", "bash", "-c", "pkill -f octo_policy_server; sleep 2"], timeout=60)
    for model, ports in SERVERS.items():
        for port in ports:
            lf = open(LOGS / f"server_wsl_{model}_{port}.restart.log", "a", encoding="utf-8")
            subprocess.Popen(["wsl.exe", "-e", "bash", "/mnt/e/research/the_world/scripts/run_wsl_server.sh", model, str(port)],
                             stdout=lf, stderr=subprocess.STDOUT, cwd=ROOT,
                             creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
            log(f"launched server {model} on {port}")
            time.sleep(20)  # stagger GPU/JIT warm-up
    deadline = time.time() + 900
    while time.time() < deadline:
        ok = {p: (h or {}).get("variants") is not None for p in [8767, 8768, 8769, 8770] for h in [health(p)]}
        log(f"server health (variant-capable): {ok}")
        if all(ok.values()):
            return True
        time.sleep(30)
    return False


def main():
    while "CONTACT_EXT_DONE" not in (LOGS / "queue_contact_ext.out").read_text(encoding="utf-8", errors="replace"):
        log("waiting for CONTACT_EXT_DONE")
        time.sleep(120)
    from queue_v2 import busy_ports
    while busy_ports():
        log(f"waiting for running sweep jobs to finish on ports {sorted(busy_ports())}")
        time.sleep(60)
    if not restart_servers():
        log("SERVER_RESTART_FAILED")
        return
    jobs = [dict(policy=f"{m}@{v}", env=e, preset="variants_v1", conds=None, offset=0, episodes=24)
            for e in ENVS for m in SERVERS for v in VARIANTS]
    run_phase("variants_v1_24", jobs)
    r = subprocess.run([str(PY), "scripts/analyze_controller_sweep.py", "--root", OUT, "--out", f"{OUT}/analysis_variants.md"],
                       cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    log(f"analysis rc={r.returncode}")
    log("VARIANTS_QUEUE_DONE")


if __name__ == "__main__":
    main()
