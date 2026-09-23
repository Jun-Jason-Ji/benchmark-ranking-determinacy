"""Why the compatible set carries no 1-alpha coverage claim, and what does.

The construction in the appendix picks the loss-minimising grid point on the demonstration set and
then tests every candidate against that point with a one-sided paired bootstrap. Each test is valid
*for a fixed reference*. The reference here is not fixed: it is the argmin of the same sample the
test then uses, so it is the luckiest candidate in this draw, and candidates close to it are
rejected more often than the nominal level allows. Inverting a test does not by itself handle the
selection.

This script demonstrates the failure and measures the fix.

PART 1, the null. K candidates with identical risk, M independent demonstrations, non-negative
bounded loss. Every candidate is a true minimiser, so a procedure claiming 1-alpha coverage for the
set of minimisers should retain a nominated one about 1-alpha of the time. It does not: retention is
roughly 53% against a nominal 95% at K=50, M=98. Raising the bootstrap count does not help, because
the problem is the reference, not the resampling.

PART 2, the fix. Select the reference on one half of the demonstrations and run the test on the
other half. Selection and inference then use disjoint data and the level means what it says. The
cost is power. On the project's own replay grids this is enough to keep the substantive conclusion:
nominal remains excluded on both stacks across split seeds (rebuild_compatible_set.py --split).

What this does NOT show: it is not an estimate of the coverage of the procedure on the robot data,
and it does not establish that the nominal exclusion reported in the manuscript is wrong. It shows
that the general coverage claim was unearned, which is why the manuscript now states the
same-sample construction as an empirical compatibility rule and reports the split-sample variant
alongside it.

Usage: python scripts/check_selection_bias.py [--reps 1000] [--boot 1000]
"""
import argparse
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np


def retention(k, m, boot, reps, alpha, split, seed=0):
    """How often candidate 0 -- a true risk minimiser -- is retained."""
    rng = np.random.default_rng(seed)
    kept = 0
    for _ in range(reps):
        loss = rng.uniform(0.0, 1.0, size=(m, k))      # identical risk, non-negative, bounded
        if split:
            perm = rng.permutation(m)
            sel, test = perm[: m // 2], perm[m // 2:]
            best = int(np.argmin(loss[sel].mean(axis=0)))
            dv = loss[test, 0] - loss[test, best]
        else:
            best = int(np.argmin(loss.mean(axis=0)))    # reference chosen on the test data
            dv = loss[:, 0] - loss[:, best]
        if best == 0:
            kept += 1
            continue
        idx = rng.integers(0, len(dv), size=(boot, len(dv)))
        kept += int(np.percentile(dv[idx].mean(axis=1), 100 * alpha) <= 0)
    return kept / reps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", type=int, default=50, help="K; the replay grid has 50 points")
    ap.add_argument("--demos", type=int, default=98, help="M; the project has 98 demonstrations")
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--reps", type=int, default=1000)
    ap.add_argument("--alpha", type=float, default=0.05)
    args = ap.parse_args()
    print(f"K={args.candidates} equal-risk candidates, M={args.demos} demonstrations, "
          f"B={args.boot}, {args.reps} repetitions, alpha={args.alpha}")
    print(f"nominal retention of a true minimiser: {1 - args.alpha:.1%}\n")
    print("| reference chosen on | retention | MC std. err. | verdict |")
    print("|---|---:|---:|---|")
    for label, split in (("the same demonstrations (as published)", False),
                         ("a disjoint half (--split)", True)):
        p = retention(args.candidates, args.demos, args.boot, args.reps, args.alpha, split)
        se = (p * (1 - p) / args.reps) ** 0.5
        ok = p >= 1 - args.alpha - 3 * se
        print(f"| {label} | {p:.1%} | {se:.1%} | {'at nominal' if ok else '**below nominal**'} |")
    print("\nThe same-sample column is the construction as published. It is not a valid "
          "1-alpha procedure, and no increase in the bootstrap count changes that.")
    print("The split column removes the selection effect but does not land exactly on nominal: at "
          "M/2 ~ 49 demonstrations the one-sided percentile bootstrap is itself approximate, and a "
          "few points of shortfall remain. We report it as a large improvement with a residual "
          "approximation error, not as an exact procedure -- an exact one would need a studentised "
          "or calibrated bootstrap, or a model confidence set with its own conditions.")


if __name__ == "__main__":
    main()
