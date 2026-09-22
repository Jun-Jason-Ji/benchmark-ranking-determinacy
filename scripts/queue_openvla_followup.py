"""After OPENVLA_QUEUE_DONE: extend the OpenVLA eggplant candidate (torque x0.5 lifts OpenVLA from 0.125 to 0.50,
24 episodes, single seed set) with (a) episodes 24-47 under the original seeds and (b) a second seed set
(20270101) episodes 0-47, for nominal and force_x0.5 only; then re-run the pair analysis at 48 episodes on
both seed sets. Runs on the OpenVLA server (8771) sequentially."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import PY, OUT, log  # noqa: E402
from queue_openvla import health, PORT, POLICY, LOGS  # noqa: E402

ENV = "PutEggplantInBasketScene-v1"
OUT2 = "results/controller_sweep_gpu_rep"


def main():
    while "OPENVLA_QUEUE_DONE" not in (LOGS / "queue_openvla_run.out").read_text(encoding="utf-8", errors="replace"):
        time.sleep(120)
    h = health(PORT)
    if not (h and h.get("model") == POLICY):
        log("OPENVLA_SERVER_NOT_HEALTHY")
        return
    jobs = [dict(conds="nominal,force_x0.5", offset=24, episodes=24, seed=20260918, out=OUT),
            dict(conds="nominal,force_x0.5", offset=0, episodes=48, seed=20270101, out=OUT2)]
    for j in jobs:
        cmd = [str(PY), "scripts/controller_sweep.py", "--policy-name", POLICY, "--policy-url", f"http://127.0.0.1:{PORT}", "--env-id", ENV,
               "--preset", "variants_v1", "--conditions", j["conds"], "--episode-offset", str(j["offset"]), "--episodes", str(j["episodes"]),
               "--policy-seed-base", str(j["seed"]), "--output-dir", j["out"]]
        jl = open(LOGS / "jobs" / f"openvla_followup_{j['seed']}.out", "a", encoding="utf-8")
        rc = subprocess.call(cmd, cwd=ROOT, stdout=jl, stderr=subprocess.STDOUT)
        log(f"done rc={rc} openvla followup seed={j['seed']} off={j['offset']}")
    log("OPENVLA_FOLLOWUP_DONE")


if __name__ == "__main__":
    main()
