"""Evaluate the policy pair at the operating point the calibration data actually prefer.

Every rate in this project, and every rate the benchmark publishes, is computed at the simulator's
shipped nominal controller setting. analyze_compatible_set_v2.py shows that setting is not the
replay loss minimiser: on both stacks independently the minimum is at (k x2, d x0.5, delay 1), ratio
d/k = 0.25, and nominal is rejected against it. That left the manuscript unable to say whether a
policy ranking computed at nominal would survive at the setting the calibration evidence selects --
the first item in its limitations.

This queue closes that gap. It runs the complete 64-configuration eggplant census for octo-small and
octo-base at the fitted point, under three seed sets whose bases match three of the existing census
sets (20260918, 20280101, 20290101), so the comparison against nominal is PAIRED: same
configurations, same policy seeds, only the controller setting differs. It also runs the halved
torque limit at the fitted point, which is the one calibration-invisible direction that carries over
to this operating point without new replay evidence (see the fitted_v1 preset comment).

2 conditions x 64 configurations x 2 policies x 3 seed sets = 1,536 episodes; about 13 s each,
two workers in parallel, so roughly two hours.

Conditions are ordered so the primary result lands first: all three seed sets of `fitted` complete
before any `fitted_force_x0.5` starts. The sweep skips episode ids already present in its target
record file, so an interruption costs only the episode in flight.

Marker FITTED_POINT_DONE in results/controller_sweep/logs/queue_fitted_point.out.
"""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import log, healthy  # noqa: E402

PY = str(ROOT / ".venv-windows-ms3/Scripts/python.exe")
LOGS = ROOT / "results/controller_sweep/logs"
ENV = "PutEggplantInBasketScene-v1"
EPISODES = 64
# base -> output directory. Bases match census sets A', C and D so the pairing is exact.
SETS = [(20260918, "results/controller_sweep_fitted_A"),
        (20280101, "results/controller_sweep_fitted_C"),
        (20290101, "results/controller_sweep_fitted_D")]
CONDS = ["fitted", "fitted_force_x0.5"]     # primary first
PORTS = {"octo-small": 8767, "octo-base": 8768}


def worker(policy, port):
    for cond in CONDS:
        for base, out in SETS:
            tag = f"fitted_{policy}_{cond}_{base}"
            cmd = [PY, str(ROOT / "scripts/controller_sweep.py"),
                   "--env-id", ENV, "--policy-url", f"http://127.0.0.1:{port}",
                   "--policy-name", policy, "--preset", "fitted_v1", "--conditions", cond,
                   "--episodes", str(EPISODES), "--episode-offset", "0",
                   "--policy-seed-base", str(base), "--output-dir", out]
            jl = open(LOGS / "jobs" / f"{tag}.out", "a", encoding="utf-8")
            log(f"start {policy} {cond} base={base}")
            t0 = time.time()
            rc = subprocess.call(cmd, cwd=ROOT, stdout=jl, stderr=subprocess.STDOUT)
            log(f"done rc={rc} {policy} {cond} base={base} ({(time.time() - t0) / 60:.1f} min)")
            if rc != 0:
                log(f"NONZERO_RC {tag} -- see results/controller_sweep/logs/jobs/{tag}.out")


def main():
    (LOGS / "jobs").mkdir(parents=True, exist_ok=True)
    for policy, port in PORTS.items():
        if not healthy(port, policy):
            log(f"SERVER_NOT_HEALTHY {policy}:{port}")
            return
    import threading
    ts = [threading.Thread(target=worker, args=(p, port)) for p, port in PORTS.items()]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    log("FITTED_POINT_DONE")


if __name__ == "__main__":
    main()
