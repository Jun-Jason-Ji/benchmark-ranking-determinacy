"""OpenVLA sweep runner that assumes the OpenVLA server on 8771 is already (being) started externally:
waits for /health, then runs variants_v1 (24 episodes) on eggplant + spoon and the all-policy analysis.
Replaces the server-start part of queue_openvla.py after its first attempt failed (accelerate mismatch)."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import PY, OUT, log  # noqa: E402
from queue_openvla import health, PORT, POLICY, ENVS, LOGS  # noqa: E402


def main():
    deadline = time.time() + 3600
    while time.time() < deadline:
        h = health(PORT)
        if h and h.get("model") == POLICY:
            log(f"openvla server ready: {str(h)[:300]}")
            break
        time.sleep(30)
    else:
        log("OPENVLA_SERVER_FAILED")
        return
    for env in ENVS:
        cmd = [str(PY), "scripts/controller_sweep.py", "--policy-name", POLICY, "--policy-url", f"http://127.0.0.1:{PORT}",
               "--env-id", env, "--preset", "variants_v1", "--episodes", "24", "--output-dir", OUT]
        (LOGS / "jobs").mkdir(parents=True, exist_ok=True)
        jl = open(LOGS / "jobs" / f"openvla_{env}.out", "a", encoding="utf-8")
        rc = subprocess.call(cmd, cwd=ROOT, stdout=jl, stderr=subprocess.STDOUT)
        log(f"done rc={rc} {POLICY} {env}")
    r = subprocess.run([str(PY), "scripts/analyze_controller_sweep.py", "--root", OUT, "--out", f"{OUT}/analysis_all_policies.md"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    log(f"analysis rc={r.returncode}")
    log("OPENVLA_QUEUE_DONE")


if __name__ == "__main__":
    main()
