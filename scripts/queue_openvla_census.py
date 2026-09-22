"""OpenVLA evidence, rebuilt around the config census (replaces queue_openvla_strengthen / queue_openvla_more,
both stopped on 2026-09-19 once the seed sets were found to be non-independent for a deterministic policy).

OpenVLA-7B is deterministic (do_sample=False, per-episode seed ignored), and each task has a finite grid of
initial configurations (scripts/task_configs.py): ms3 eggplant 64, ms3 spoon/carrot 24, ms2 eggplant 24.
Running the full grid therefore measures OpenVLA's success rate on the benchmark exactly -- there is no
sampling error left to shrink -- and any remaining variation is (a) simulator parameters, which is the object
of study, and (b) run-to-run GPU nondeterminism, quantified separately from the A/B/C re-runs.

Jobs (sequential; the OpenVLA server has process-global state, one client at a time). Waits for
OCTO_RECOLLECT_DONE (the last Octo queue) so the two Octo servers are not competing for the GPU (OpenVLA drops from ~70 s to
~280 s per episode under three-way contention).
  1. ms3 eggplant, episodes 0-63, nominal + force_x0.5        -> completes the 64-config census of the core case
  2. ms3 eggplant, episodes 0-63, iso_x0.25, iso_x4.0, fric_x0.4, dens_x0.5 -> the other calibration-invisible axes
  3. ms3 carrot,   episodes 0-23, variants_v1                 -> third task, full census
  4. ms2 eggplant, episodes 0-23, nominal + force_x0.5        -> original SIMPLER stack, full census (cross-stack)
(ms3 spoon is already a complete 24-config census for all six conditions.)
Marker OPENVLA_CENSUS_DONE."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import PY, OUT, log  # noqa: E402
from queue_openvla import health, PORT, POLICY, LOGS  # noqa: E402

SEED = "20260918"  # seed set A; the value is irrelevant for a deterministic policy, kept for record compatibility
WSL_PREFIX = ("cd /mnt/e/research/the_world && source .venv-linux/bin/activate && source scripts/wsl_render_env.sh && "
              "export LP_NUM_THREADS=4 && export PYTHONUNBUFFERED=1 && ")
JOBS = [
    dict(kind="ms3", env="PutEggplantInBasketScene-v1", conds="nominal,force_x0.5", episodes=64, out=OUT),
    dict(kind="ms3", env="PutEggplantInBasketScene-v1", conds="iso_x0.25,iso_x4.0,fric_x0.4,dens_x0.5", episodes=64, out=OUT),
    dict(kind="ms3", env="PutCarrotOnPlateInScene-v1", conds="nominal,force_x0.5,iso_x0.25,iso_x4.0,fric_x0.4,dens_x0.5", episodes=24, out=OUT),
    dict(kind="ms2", task="widowx_put_eggplant_in_basket", conds="nominal,force_x0.5", episodes=24, out="results/controller_sweep_ms2"),
]


def wait_marker(fname, marker, timeout_h=12):
    deadline = time.time() + timeout_h * 3600
    while time.time() < deadline:
        f = LOGS / fname
        if f.exists() and marker in f.read_text(encoding="utf-8", errors="replace"):
            return True
        time.sleep(120)
    log(f"marker {marker} not seen within {timeout_h} h; starting anyway")
    return False


def main():
    wait_marker("queue_octo_recollect.out", "OCTO_RECOLLECT_DONE")
    log("starting OpenVLA census jobs")
    (LOGS / "jobs").mkdir(parents=True, exist_ok=True)
    for j in JOBS:
        h = health(PORT)
        if not (h and h.get("model") == POLICY):
            log("OPENVLA_SERVER_NOT_HEALTHY")
            return
        common = ["--policy-name", POLICY, "--policy-url", f"http://127.0.0.1:{PORT}", "--preset", "variants_v1",
                  "--conditions", j["conds"], "--episode-offset", "0", "--episodes", str(j["episodes"]),
                  "--policy-seed-base", SEED, "--output-dir", j["out"]]
        if j["kind"] == "ms3":
            cmd = [str(PY), "scripts/controller_sweep.py", "--env-id", j["env"]] + common
            tag = f"ms3_{j['env']}_{j['conds'].split(',')[0]}"
        else:
            inner = WSL_PREFIX + " ".join(["python", "scripts/controller_sweep_ms2.py", "--task", j["task"]] + common) + " 2>&1 | grep --line-buffered -v 'using WSL'"
            cmd = ["wsl.exe", "-e", "bash", "-c", inner]
            tag = f"ms2_{j['task']}"
        log(f"start {tag} ({j['conds']}, {j['episodes']} eps)")
        jl = open(LOGS / "jobs" / f"openvla_census_{tag}.out", "a", encoding="utf-8")
        rc = subprocess.call(cmd, cwd=ROOT, stdout=jl, stderr=subprocess.STDOUT)
        log(f"done rc={rc} {tag}")
    log("OPENVLA_CENSUS_DONE")


if __name__ == "__main__":
    main()
