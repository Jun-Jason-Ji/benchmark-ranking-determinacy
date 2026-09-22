"""Strengthen the replicated OpenVLA torque finding on the OpenVLA server (8771), sequentially:
  1. third independent seed set (20280101), eggplant nominal + force_x0.5, episodes 0-47 -> results/controller_sweep_gpu_rep3
  2. extend seed set A (20260918) to episodes 48-95 -> results/controller_sweep_gpu
  3. extend seed set B (20270101) to episodes 48-95 -> results/controller_sweep_gpu_rep
Each block ~2 h at 147 s/episode. Marker OPENVLA_STRENGTHEN_DONE."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import PY, OUT, log  # noqa: E402
from queue_openvla import health, PORT, POLICY, LOGS  # noqa: E402

ENV = "PutEggplantInBasketScene-v1"
JOBS = [dict(seed=20280101, offset=0, episodes=48, out="results/controller_sweep_gpu_rep3"),
        dict(seed=20260918, offset=48, episodes=48, out=OUT),
        dict(seed=20270101, offset=48, episodes=48, out="results/controller_sweep_gpu_rep")]


def main():
    h = health(PORT)
    if not (h and h.get("model") == POLICY):
        log("OPENVLA_SERVER_NOT_HEALTHY")
        return
    for j in JOBS:
        cmd = [str(PY), "scripts/controller_sweep.py", "--policy-name", POLICY, "--policy-url", f"http://127.0.0.1:{PORT}", "--env-id", ENV,
               "--preset", "variants_v1", "--conditions", "nominal,force_x0.5", "--episode-offset", str(j["offset"]), "--episodes", str(j["episodes"]),
               "--policy-seed-base", str(j["seed"]), "--output-dir", j["out"]]
        (LOGS / "jobs").mkdir(parents=True, exist_ok=True)
        jl = open(LOGS / "jobs" / f"openvla_strengthen_{j['seed']}_{j['offset']}.out", "a", encoding="utf-8")
        rc = subprocess.call(cmd, cwd=ROOT, stdout=jl, stderr=subprocess.STDOUT)
        log(f"done rc={rc} openvla strengthen seed={j['seed']} off={j['offset']}")
    log("OPENVLA_STRENGTHEN_DONE")


if __name__ == "__main__":
    main()
