"""After OPENVLA_STRENGTHEN_DONE (OpenVLA server 8771 free), sequentially (one OpenVLA client at a time):
  1. original SIMPLER stack (ms2, WSL, llvmpipe render; WSL reaches the Windows server via mirrored 127.0.0.1):
     eggplant nominal + force_x0.5, episodes 0-47, seed set A -> results/controller_sweep_ms2   (cross-stack check of the core case)
  2. ms3 spoon, seed set A, nominal + force_x0.5 extended 24 -> 48                              (second task, same seeds)
  3. ms3 spoon, seed set B (20270101), episodes 0-47                                            (second task replication)
  4. ms3 carrot, seed set A, episodes 0-47                                                       (third task)
  5. ms2 spoon, seed set A, episodes 0-47                                                        (cross-stack, second task)
Marker OPENVLA_MORE_DONE. Each ms3 episode ~70 s, ms2 ~80 s on this machine."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import PY, OUT, log  # noqa: E402
from queue_openvla import health, PORT, POLICY, LOGS  # noqa: E402

CONDS = "nominal,force_x0.5"
WSL_PREFIX = ("cd /mnt/e/research/the_world && source .venv-linux/bin/activate && source scripts/wsl_render_env.sh && "
              "export LP_NUM_THREADS=4 && export PYTHONUNBUFFERED=1 && ")
JOBS = [
    dict(kind="ms2", task="widowx_put_eggplant_in_basket", seed="20260918", offset=0, episodes=48, out="results/controller_sweep_ms2"),
    dict(kind="ms3", env="PutSpoonOnTableClothInScene-v1", seed="20260918", offset=0, episodes=48, out=OUT),
    dict(kind="ms3", env="PutSpoonOnTableClothInScene-v1", seed="20270101", offset=0, episodes=48, out="results/controller_sweep_gpu_rep"),
    dict(kind="ms3", env="PutCarrotOnPlateInScene-v1", seed="20260918", offset=0, episodes=48, out=OUT),
    dict(kind="ms2", task="widowx_spoon_on_towel", seed="20260918", offset=0, episodes=48, out="results/controller_sweep_ms2"),
]


def wait_marker(fname, marker):
    while True:
        f = LOGS / fname
        if f.exists() and marker in f.read_text(encoding="utf-8", errors="replace"):
            return
        time.sleep(120)


def main():
    wait_marker("queue_openvla_strengthen.out", "OPENVLA_STRENGTHEN_DONE")
    log("strengthen done; starting OpenVLA follow-on jobs")
    (LOGS / "jobs").mkdir(parents=True, exist_ok=True)
    for j in JOBS:
        h = health(PORT)
        if not (h and h.get("model") == POLICY):
            log("OPENVLA_SERVER_NOT_HEALTHY")
            return
        common = ["--policy-name", POLICY, "--policy-url", f"http://127.0.0.1:{PORT}", "--preset", "variants_v1", "--conditions", CONDS,
                  "--episode-offset", str(j["offset"]), "--episodes", str(j["episodes"]), "--policy-seed-base", j["seed"], "--output-dir", j["out"]]
        if j["kind"] == "ms3":
            cmd = [str(PY), "scripts/controller_sweep.py", "--env-id", j["env"]] + common
            tag = f"ms3_{j['env']}_{j['seed']}"
        else:
            inner = WSL_PREFIX + " ".join(["python", "scripts/controller_sweep_ms2.py", "--task", j["task"]] + common) + " 2>&1 | grep --line-buffered -v 'using WSL'"
            cmd = ["wsl.exe", "-e", "bash", "-c", inner]
            tag = f"ms2_{j['task']}_{j['seed']}"
        log(f"start {tag}")
        jl = open(LOGS / "jobs" / f"openvla_more_{tag}.out", "a", encoding="utf-8")
        rc = subprocess.call(cmd, cwd=ROOT, stdout=jl, stderr=subprocess.STDOUT)
        log(f"done rc={rc} {tag}")
    log("OPENVLA_MORE_DONE")


if __name__ == "__main__":
    main()
