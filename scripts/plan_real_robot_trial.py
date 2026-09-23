"""Magnitude check on the real-robot validation plan of Sect. 9: power, not interval half-width.

The plan in the limitations section names a trial count, and an earlier version of it sized the
experiment by asking when the expected 95% interval half-width falls below the hypothesised gap.
That is the wrong quantity. An expected half-width of 0.062 against a gap of 0.067 does not make the
observed interval exclude zero -- it makes it a coin flip, because the estimate itself is random.
The quantity that answers "how many trials" is the power of the test at the hypothesised gap.

Assumptions, all of them optimistic, and the table is a magnitude check rather than a formal sample
size:
  * the published rates 0.853 (rt-1-converged) and 0.920 (rt-1-15pct) are the true rates;
  * trials are independent Bernoulli draws, no scene clustering;
  * equal allocation to the two policies;
  * no protocol drift between the two arms of the comparison;
  * a two-sided normal-approximation test at alpha = 0.05, with the standard error computed under
    the alternative rather than pooled under the null.

A paired design over a shared scene grid -- which is what this paper argues for everywhere else --
would need fewer trials than this, and clustering by scene would need more. Either way the point
stands: per-policy n and total n are not the same number, and half-width is not power.

Usage: python scripts/plan_real_robot_trial.py [--p1 0.853 --p2 0.920] [--n 200 400 800]
"""
import argparse
import math

Z = 1.959963985                       # two-sided 95%


def phi(x):
    """Standard normal CDF."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def row(p1, p2, n):
    se = math.sqrt(p1 * (1 - p1) / n + p2 * (1 - p2) / n)
    gap = abs(p2 - p1)
    half = Z * se
    # Two-sided power at the alternative: both rejection tails, the far one negligible but kept.
    power = phi(gap / se - Z) + phi(-gap / se - Z)
    return se, half, power


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--p1", type=float, default=0.853)
    ap.add_argument("--p2", type=float, default=0.920)
    ap.add_argument("--n", type=int, nargs="+", default=[200, 400, 800])
    args = ap.parse_args()
    gap = abs(args.p2 - args.p1)
    print(f"published rates {args.p1} and {args.p2}, hypothesised gap {gap:.3f}")
    print(f"{'per policy':>10} {'total':>7} {'se':>8} {'half-width':>11} {'power':>7}")
    for n in args.n:
        se, half, power = row(args.p1, args.p2, n)
        print(f"{n:>10} {2 * n:>7} {se:>8.4f} {half:>11.4f} {power:>7.3f}")
    print("\nHalf-width is not power: at n = 200 per policy the expected half-width (0.062) is "
          "already below the gap (0.067) while the power is about 0.57.")


if __name__ == "__main__":
    main()
