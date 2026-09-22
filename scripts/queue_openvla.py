"""Second model family: OpenVLA-7B (4-bit) sweep. Waits for SPOON_HIST1_96_DONE (all Octo queues done),
stops the two extra Octo servers (8769/8770) to free VRAM, starts the OpenVLA server on 8771, waits for
READY, then runs variants_v1 (nominal + 5 calibration-invisible conditions, 24 episodes) on eggplant and
spoon, followed by the all-policy pairwise analysis."""
import http.client
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import PY, OUT, log, busy_ports  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
ENVS = ["PutEggplantInBasketScene-v1", "PutSpoonOnTableClothInScene-v1"]
PORT = 8771
POLICY = "openvla-7b-4bit"


def health(port):
    try:
        c = http.client.HTTPConnection("127.0.0.1", port, timeout=5); c.request("GET", "/health")
        r = json.loads(c.getresponse().read()); c.close(); return r
    except Exception:
        return None


def main():
    while "SPOON_HIST1_96_DONE" not in (LOGS / "queue_spoon_hist1_96.out").read_text(encoding="utf-8", errors="replace"):
        time.sleep(120)
    while busy_ports():
        log(f"waiting for sweep jobs on {sorted(busy_ports())}"); time.sleep(60)
    log("stopping Octo servers 8769/8770 to free VRAM")
    subprocess.run(["wsl.exe", "-e", "bash", "-c", "pkill -f 'port 8769'; pkill -f 'port 8770'; sleep 3"], timeout=60)
    lf = open(LOGS / "server_openvla_8771.log", "a", encoding="utf-8")
    subprocess.Popen([str(ROOT / ".venv-openvla/Scripts/python.exe"), "scripts/openvla_policy_server.py", "--port", str(PORT)],
                     cwd=ROOT, stdout=lf, stderr=subprocess.STDOUT, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    deadline = time.time() + 1800
    while time.time() < deadline:
        h = health(PORT)
        if h and h.get("model") == POLICY:
            log(f"openvla server ready: {json.dumps(h)[:300]}"); break
        time.sleep(30)
    else:
        log("OPENVLA_SERVER_FAILED"); return
    for env in ENVS:
        cmd = [str(PY), "scripts/controller_sweep.py", "--policy-name", POLICY, "--policy-url", f"http://127.0.0.1:{PORT}",
               "--env-id", env, "--preset", "variants_v1", "--episodes", "24", "--output-dir", OUT]
        jl = open(LOGS / "jobs" / f"openvla_{env}.out", "a", encoding="utf-8")
        rc = subprocess.call(cmd, cwd=ROOT, stdout=jl, stderr=subprocess.STDOUT)
        log(f"done rc={rc} {POLICY} {env}")
    r = subprocess.run([str(PY), "scripts/analyze_controller_sweep.py", "--root", OUT, "--out", f"{OUT}/analysis_all_policies.md"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    log(f"analysis rc={r.returncode}")
    log("OPENVLA_QUEUE_DONE")


if __name__ == "__main__":
    main()
