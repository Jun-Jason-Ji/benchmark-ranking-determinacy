"""Audit the torque-limit invariance claim at the level it is stated: bitwise equality per episode.

The manuscript says the halved torque limit leaves the replay trajectory unchanged "bitwise exactly"
on two independent stacks. check_iso_invariance.py reports max |dp| in millimetres, which is the
right diagnostic for the iso-ratio result but cannot support a bitwise claim: a difference of 1e-12 m
prints as 0.000 mm. This script counts episodes whose sim_p arrays are bitwise identical between
nominal and force_x0.5, and reports the residual for every episode that is not, so the claim can be
stated as what the data show rather than as an absolute.
"""
import argparse
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DIRS = {"ManiSkill3 / SAPIEN 3": "results/replay_sysid_100/sweep_v1",
        "ManiSkill2 / SAPIEN 2.2.2": "results/replay_sysid_ms2/sweep_v1"}


def episodes(d, cond):
    f = d / f"{cond}.jsonl"
    if not f.exists():
        return []
    return sorted(json.loads(l)["episode_id"] for l in f.read_text(encoding="utf-8").splitlines() if l.strip())


def traj(d, cond, ep):
    f = d / f"{cond}_ep{ep:03d}.npz"
    return np.load(f)["sim_p"] if f.exists() else None


def audit(label, rel, a="nominal", b="force_x0.5"):
    d = ROOT / rel
    eps = sorted(set(episodes(d, a)) & set(episodes(d, b)))
    exact, resid = 0, []
    for e in eps:
        ta, tb = traj(d, a, e), traj(d, b, e)
        if ta is None or tb is None:
            continue
        if ta.shape != tb.shape:
            resid.append((e, float("nan"), "shape mismatch %s vs %s" % (ta.shape, tb.shape)))
            continue
        if np.array_equal(ta, tb):
            exact += 1
        else:
            resid.append((e, float(np.abs(ta - tb).max()), ""))
    n = exact + len(resid)
    print(f"\n## {label}  ({rel})")
    print(f"episodes compared: {n}")
    print(f"bitwise identical: {exact}/{n}" + (f"  ({exact / n:.3%})" if n else ""))
    if resid:
        mags = [r[1] for r in resid if np.isfinite(r[1])]
        print(f"not identical    : {len(resid)}/{n}")
        for e, m, note in resid:
            print(f"   episode {e:3d}: max |dp| = {m:.3e} m = {m * 1e3:.3e} mm {note}")
        if mags:
            print(f"   largest residual: {max(mags):.3e} m = {max(mags) * 1e3:.3e} mm "
                  f"({max(mags) * 1e6:.3f} um)")
    return label, exact, n, [r[1] for r in resid if np.isfinite(r[1])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", default="nominal")
    ap.add_argument("--b", default="force_x0.5")
    args = ap.parse_args()
    print(f"# Bitwise audit of the torque-limit invariance: {args.a} vs {args.b}")
    out = [audit(k, v, args.a, args.b) for k, v in DIRS.items()]
    print("\n## How this should be stated")
    for label, exact, n, mags in out:
        if exact == n:
            print(f"- {label}: bitwise identical on all {n} episodes.")
        else:
            worst = max(mags) if mags else float("nan")
            print(f"- {label}: bitwise identical on {exact} of {n} episodes; the remaining "
                  f"{n - exact} differ by at most {worst * 1e6:.3f} um "
                  f"({worst:.1e} m), which is {'far below' if worst < 1e-4 else 'near'} "
                  f"the 0.14--0.21 mm calibration residual.")


if __name__ == "__main__":
    main()
