"""Rebuild the calibration-compatible set from the replay grid, with the search domain made explicit.

This exists because the set was never actually computed the way the manuscript defines it.
analyze_compatible_set.py fixed `nominal` as the reference, read the 40-demonstration directory, and
took a 2.5% quantile while the text says 5%. The definition in the appendix instead says: find the
loss-minimising point on the search grid, then test every candidate against THAT point with a
one-sided paired bootstrap, and keep the candidates the test does not reject.

Those two procedures do not agree, and the difference is not cosmetic: on the 98-demonstration grid
the loss minimiser is not nominal, so testing against the true minimiser can reject nominal itself.
This script computes it both ways and prints the full candidate table, so the question is settled by
the data rather than by which script was run.

Definitions, all switchable, because the answer depends on them and the manuscript has to state
which it uses:

  --loss           per-demonstration scalar loss; default mean_total_err, the field the replay
                   records carry.
  --ref            best  : test against the grid's loss minimiser (the appendix's definition)
                   nominal: test against the nominal setting (what the old script did)
  --alpha          one-sided level; 0.05 means the 5th percentile of the bootstrap distribution.
  --tol            engineering-equivalence tolerance t >= 0: keep candidate c when the lower bound of
                   mean(loss_c - loss_ref) is <= t rather than <= 0. Default 0, which is the rule the
                   manuscript states. A nonzero value must be justified on its own terms, not chosen
                   to retain a conclusion.
  --split          SELECTION BIAS. With --ref best the reference is the argmin of the SAME
                   demonstrations the test then uses, and that invalidates the coverage
                   interpretation: the reference is the luckiest point in this sample, so near-tied
                   candidates are rejected too often. Under a null of K equal-risk candidates with
                   M=98 demonstrations, retention of a nominated true minimiser is about 53% against
                   a nominal 95% (scripts/check_selection_bias.py). --split fixes it the simple way:
                   choose the reference on one half of the demonstrations and run the test on the
                   other half, so selection and inference use disjoint data. The cost is power --
                   half the demonstrations for each job -- and the benefit is that the level means
                   something. --split-seed permutes the halves.

Paired by demonstration throughout: the demonstrations differ enormously in difficulty, and an
unpaired test compares the between-demonstration spread against the parameter effect instead of
against itself.

Usage:
  python scripts/rebuild_compatible_set.py --stack ms3
  python scripts/rebuild_compatible_set.py --stack ms2 --ref nominal
"""
import argparse
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
STACKS = {"ms3": "results/replay_sysid_100/grid",
          "ms2": "results/replay_sysid_ms2/grid",
          "ms3_40": "results/replay_sysid/grid"}
# The grid names the shipped controller setting s1_d1_delay0; "nominal" is the sweep-side name.
NOMINAL = "s1_d1_delay0"


def load(d, loss):
    """{condition: {episode_id: loss}} over the grid directory."""
    out = {}
    for f in sorted(d.glob("*.jsonl")):
        per = {}
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if loss not in r or r[loss] is None:
                continue
            per.setdefault(r["episode_id"], float(r[loss]))
        if per:
            out[f.stem] = per
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stack", default="ms3", choices=sorted(STACKS))
    ap.add_argument("--loss", default="mean_total_err")
    ap.add_argument("--ref", default="best", choices=["best", "nominal"])
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--tol", type=float, default=0.0)
    ap.add_argument("--boot", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--top", type=int, default=12, help="how many rows of the candidate table to print")
    ap.add_argument("--split", action="store_true",
                    help="select the reference on one half of the demonstrations and test on the "
                         "other, so selection and inference use disjoint data")
    ap.add_argument("--split-seed", type=int, default=0)
    args = ap.parse_args()

    d = ROOT / STACKS[args.stack]
    per = load(d, args.loss)
    if not per:
        raise SystemExit(f"no records with field {args.loss!r} under {d}")
    # Common demonstrations: the paired test is only defined on demos every candidate ran.
    ids = sorted(set.intersection(*[set(v) for v in per.values()]))
    conds = sorted(per)
    if args.split:
        # Disjoint halves: pick the reference on A, test on B. Without this the reference is the
        # argmin of the very sample the test uses, and the level is not what it says.
        perm = np.random.default_rng(args.split_seed).permutation(len(ids))
        half = len(ids) // 2
        sel_ids = [ids[i] for i in sorted(perm[:half])]
        ids = [ids[i] for i in sorted(perm[half:])]
        sel_means = {c: float(np.mean([per[c][i] for i in sel_ids])) for c in conds}
        best = min(sel_means, key=sel_means.get)
        means = {c: float(np.mean([per[c][i] for i in ids])) for c in conds}
    else:
        means = {c: float(np.mean([per[c][i] for i in ids])) for c in conds}
        best = min(means, key=means.get)
    ref = best if args.ref == "best" else NOMINAL
    if ref not in means:
        raise SystemExit(f"reference {ref!r} absent; conditions are {conds[:5]}...")

    print(f"# Compatible set, rebuilt   stack={args.stack}  dir={STACKS[args.stack]}")
    print(f"search domain: {len(conds)} grid points; paired on {len(ids)} demonstrations"
          + (f" (reference selected on a disjoint {len(sel_ids)}, split seed {args.split_seed})"
             if args.split else " (reference selected on the SAME demonstrations -- see --split)"))
    print(f"loss={args.loss}  reference={args.ref} ({ref})  alpha={args.alpha}  tol={args.tol}  "
          f"B={args.boot}  seed={args.seed}")
    print(f"\nloss minimiser on the grid: {best}  (mean {means[best]:.8f})")
    print(f"nominal mean loss: {means.get(NOMINAL, float('nan')):.8f}   "
          f"nominal - best = {means.get(NOMINAL, float('nan')) - means[best]:+.8f}")

    rng = np.random.default_rng(args.seed)
    ridx = rng.integers(0, len(ids), size=(args.boot, len(ids)))
    rvals = np.array([per[ref][i] for i in ids])
    rows = []
    for c in conds:
        dv = np.array([per[c][i] for i in ids]) - rvals
        if c == ref:
            rows.append((c, 0.0, 0.0, True))
            continue
        bs = dv[ridx].mean(axis=1)
        lo = float(np.percentile(bs, 100 * args.alpha))
        rows.append((c, float(dv.mean()), lo, lo <= args.tol))
    rows.sort(key=lambda r: r[1])

    keep = [r for r in rows if r[3]]
    print(f"\nkept: {len(keep)} of {len(rows)} grid points")
    print(f"\n| condition | mean(loss_c - loss_ref) | {args.alpha:.0%} lower bound | in set |")
    print("|---|---:|---:|---|")
    shown = rows[:args.top]
    if NOMINAL not in [r[0] for r in shown]:
        shown = shown + [r for r in rows if r[0] == NOMINAL]
    for c, m, lo, k in shown:
        mark = "**nominal**" if c == NOMINAL else c
        print(f"| {mark} | {m:+.8f} | {lo:+.8f} | {'yes' if k else '**NO**'} |")
    if len(rows) > len(shown):
        print(f"\n({len(rows) - len(shown)} further grid points omitted; all have larger mean loss)")

    nom = next(r for r in rows if r[0] == NOMINAL)
    print(f"\nnominal: mean diff {nom[1]:+.8f}, lower bound {nom[2]:+.8f} -> "
          f"{'IN the set' if nom[3] else 'EXCLUDED from the set'} at tol={args.tol}")
    if not nom[3]:
        # The smallest tolerance that would retain nominal. Reported so that any engineering
        # equivalence margin is chosen against a stated number rather than reverse-engineered.
        print(f"  the smallest tolerance that would retain nominal is t = {nom[2]:.8f} "
              f"({nom[2] * 1000:.4f} mm if the loss is in metres)")
    print("\nkept set:", ", ".join(r[0] for r in keep) if keep else "(empty)")


if __name__ == "__main__":
    main()
