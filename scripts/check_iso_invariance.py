"""Check whether free-space replay trajectories are invariant to a common scaling of arm stiffness
and damping (same k/d ratio, same delay) across all replayed demos.

Usage: python scripts/check_iso_invariance.py --dir results/replay_sysid/sweep_v1
       python scripts/check_iso_invariance.py --dir results/replay_sysid/grid
Groups conditions by (round(stiffness_scale/damping_scale, 6), delay_steps) using run_meta.json,
then for every pair within a group and every episode computes max |Δp| between simulated EE
trajectories, and also the difference in per-episode mean error. Reports per-group maxima and
contrasts them with the smallest between-group difference.
"""
import argparse
import itertools
import json
import sys
from collections import defaultdict
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--tol-m", type=float, default=1e-3, help="invariance tolerance on max |dp| (m)")
    args = ap.parse_args()
    d = Path(args.dir)
    meta = json.loads((d / "run_meta.json").read_text(encoding="utf-8"))
    conds = meta["conditions"]
    groups = defaultdict(list)
    for name, c in conds.items():
        ss, ds, dl = c.get("stiffness_scale", 1.0), c.get("damping_scale", 1.0), int(c.get("delay_steps", 0))
        if c.get("force_scale", 1.0) != 1.0:
            groups[("force", dl)].append(name)  # force-limit variants: compare to nominal separately
            continue
        groups[(round(ss / ds, 6), dl)].append(name)
    if "nominal" in conds and ("force", 0) in groups:
        groups[("force", 0)].append("nominal")

    def traj(cond, ep):
        f = d / f"{cond}_ep{ep:03d}.npz"
        return np.load(f)["sim_p"] if f.exists() else None

    def episodes(cond):
        f = d / f"{cond}.jsonl"
        return sorted(json.loads(l)["episode_id"] for l in f.read_text(encoding="utf-8").splitlines() if l.strip()) if f.exists() else []

    lines = [f"# Iso-ratio invariance check: {d}", "", "| group (k/d ratio, delay) | conditions | episodes | max |Δp| (mm) | p95 |Δp| (mm) | max |Δ mean err| |", "|---|---|---:|---:|---:|---:|"]
    within_max = 0.0
    for key, names in sorted(groups.items(), key=lambda kv: str(kv[0])):
        if len(names) < 2:
            continue
        eps = sorted(set.intersection(*[set(episodes(n)) for n in names]))
        dps, derr = [], []
        for a, b in itertools.combinations(names, 2):
            ra = {json.loads(l)["episode_id"]: json.loads(l) for l in (d / f"{a}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
            rb = {json.loads(l)["episode_id"]: json.loads(l) for l in (d / f"{b}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
            for e in eps:
                ta, tb = traj(a, e), traj(b, e)
                if ta is None or tb is None:
                    continue
                dps.append(float(np.abs(ta - tb).max()))
                derr.append(abs(ra[e]["mean_total_err"] - rb[e]["mean_total_err"]))
        if dps:
            within_max = max(within_max, max(dps))
            lines.append(f"| {key} | {', '.join(names)} | {len(eps)} | {max(dps)*1000:.3f} | {np.percentile(dps, 95)*1000:.3f} | {max(derr):.2e} |")
    # between-group reference: nominal vs each ratio-changing condition
    ref = "nominal" if "nominal" in conds else None
    between = []
    if ref:
        for name, c in conds.items():
            if name == ref or c.get("force_scale", 1.0) != 1.0:
                continue
            r = round(c.get("stiffness_scale", 1.0) / c.get("damping_scale", 1.0), 6)
            if r == 1.0 and int(c.get("delay_steps", 0)) == 0:
                continue
            eps = sorted(set(episodes(ref)) & set(episodes(name)))
            vals = [float(np.abs(traj(ref, e) - traj(name, e)).max()) for e in eps if traj(ref, e) is not None and traj(name, e) is not None]
            if vals:
                between.append((name, np.median(vals), max(vals)))
    lines += ["", "Between-group reference (nominal vs ratio-changing or delayed conditions): median / max |Δp| over episodes", ""]
    for name, med, mx in sorted(between, key=lambda x: x[1]):
        lines.append(f"- {name}: median {med*1000:.2f} mm, max {mx*1000:.2f} mm")
    verdict = "HOLDS" if within_max < args.tol_m else "VIOLATED"
    lines += ["", f"**Verdict:** within-group max |Δp| = {within_max*1000:.3f} mm vs tolerance {args.tol_m*1000:.1f} mm → invariance {verdict}."]
    text = "\n".join(lines)
    (d / "iso_invariance.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
