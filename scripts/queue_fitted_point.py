"""Evaluate the policy pair at the operating point the calibration data actually prefer.

Every rate in this project, and every rate the benchmark publishes, is computed at the simulator's
shipped nominal controller setting. analyze_compatible_set_v2.py shows that setting is not the
replay loss minimiser: on both stacks independently the minimum is at (k x2, d x0.5, delay 1), ratio
d/k = 0.25, and nominal is rejected against it. That left the manuscript unable to say whether a
policy ranking computed at nominal would survive at the setting the calibration evidence selects --
the first item in its limitations.

This queue closes that gap. It evaluates both policies at the fitted point and over its full
calibration-invisible fibre -- six conditions mirroring `variants_v1` one for one, so the two fibres
can be compared without an asymmetry to explain away. On eggplant that is 64 configurations under
three seed sets whose bases match census sets A'/C/D; on spoon, 24 configurations under the two the
spoon census has. Because the bases match, every comparison against nominal is PAIRED: same
configurations, same policy seeds episode for episode, only the controller setting differs.

The iso directions in that fibre are measured rather than assumed. The 50-point replay grid samples
ratio 0.25 exactly once, so the common-scale invariance was verified at seven other ratios and not
at this one; the `iso_at_fitted` replay preset sweeps the scale sixteenfold at ratio 0.25 and finds
the loss flat to 5.4 um on ManiSkill3 and 11.1 um on the original stack, against the 1356 um at
which the two stacks disagree at identical nominal parameters.

Ordering puts the primary result first: every seed set of `fitted` completes before any other
condition starts, and all of eggplant before any of spoon, so an interruption costs the least
valuable part. The sweep skips episode ids already present in its target record file, so re-running
this queue after widening the fibre re-does nothing.

Logs the marker FITTED_POINT_DONE to stdout on completion; redirect it to a file to watch for that.
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
# Primary first, then the rest of the invisible fibre through the fitted point. The sweep skips
# episode ids already present in its target record file, so re-listing completed conditions costs
# nothing and the queue is safe to re-run after the fibre was widened.
CONDS = ["fitted", "fitted_force_x0.5",
         "fitted_iso_x0.25", "fitted_iso_x4.0", "fitted_fric_x0.4", "fitted_dens_x0.5"]
# (env, episodes, [(seed base, output dir)]) -- bases and set counts match each task's own nominal
# census, so every comparison is paired. Eggplant has five census sets and we use three; spoon has
# two and we use both. Eggplant runs first: it is the task the headline comparison is on, and
# finishing it before spoon starts means an interruption costs the less valuable half.
TASKS = [
    ("PutEggplantInBasketScene-v1", 64,
     [(20260918, "results/controller_sweep_fitted_A"),
      (20280101, "results/controller_sweep_fitted_C"),
      (20290101, "results/controller_sweep_fitted_D")]),
    ("PutSpoonOnTableClothInScene-v1", 24,
     [(20260918, "results/controller_sweep_fitted_A"),
      (20280101, "results/controller_sweep_fitted_C")]),
]
PORTS = {"octo-small": 8767, "octo-base": 8768}


def worker(policy, port):
    for env, episodes, sets in TASKS:
        short = "egg" if "Eggplant" in env else "spoon"
        for cond in CONDS:
            for base, out in sets:
                tag = f"fitted_{short}_{policy}_{cond}_{base}"
                cmd = [PY, str(ROOT / "scripts/controller_sweep.py"),
                       "--env-id", env, "--policy-url", f"http://127.0.0.1:{port}",
                       "--policy-name", policy, "--preset", "fitted_v1", "--conditions", cond,
                       "--episodes", str(episodes), "--episode-offset", "0",
                       "--policy-seed-base", str(base), "--output-dir", out]
                jl = open(LOGS / "jobs" / f"{tag}.out", "a", encoding="utf-8")
                log(f"start {short} {policy} {cond} base={base}")
                t0 = time.time()
                rc = subprocess.call(cmd, cwd=ROOT, stdout=jl, stderr=subprocess.STDOUT)
                log(f"done rc={rc} {short} {policy} {cond} base={base} "
                    f"({(time.time() - t0) / 60:.1f} min)")
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
