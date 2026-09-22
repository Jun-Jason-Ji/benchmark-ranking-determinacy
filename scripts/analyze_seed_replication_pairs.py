"""Two seed sets for the eggplant near-tied policy set: compare every pair x condition between the original
seed set (policy seeds 20260918+ep, results/controller_sweep_gpu) and the replication set (20270101+ep,
results/controller_sweep_gpu_rep) on the same episode_ids (0..N-1). Duplicate records: first record wins.

Reports, per pair and condition: Δ with 95% paired-bootstrap CI in each seed set, the pooled estimate
(both sets, 2N paired observations), and whether the CI-supported sign agrees across sets.
A claim is marked "replicated" only when both seed sets give a CI excluding zero with the same sign.
"""
import argparse
import itertools
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np

ENV = "PutEggplantInBasketScene-v1"
CONDS = ["nominal", "iso_x0.25", "iso_x4.0", "force_x0.5", "fric_x0.4", "dens_x0.5"]
POLICIES = ["octo-small", "octo-base", "octo-small@hist1", "octo-base@hist1"]


def load(root, policy, cond, n):
    f = Path(root) / policy / ENV / f"{cond}.jsonl"
    d = {}
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                if r["episode_id"] < n:
                    d.setdefault(r["episode_id"], int(bool(r["success"])))
    return d


def boot(x, rng, n=10000):
    x = np.asarray(x, float)
    if len(x) == 0:
        return float("nan"), float("nan"), float("nan")
    m = x[rng.integers(0, len(x), size=(n, len(x)))].mean(1)
    return float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def sign(lo, hi):
    return "+" if lo > 0 else ("−" if hi < 0 else "0")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--orig", default="results/controller_sweep_gpu")
    ap.add_argument("--rep", default="results/controller_sweep_gpu_rep")
    ap.add_argument("--n", type=int, default=48)
    ap.add_argument("--out", default="results/controller_sweep_gpu_rep/analysis_seed_replication_pairs.md")
    args = ap.parse_args()
    rng = np.random.default_rng(0)
    L = [f"# Eggplant near-tied set: two seed sets (episodes 0-{args.n - 1})", "",
         f"Original seeds 20260918+ep (`{args.orig}`), replication seeds 20270101+ep (`{args.rep}`). Δ = rate(A) − rate(B), paired by episode_id, 95% paired bootstrap. "
         "Sign column: CI-supported sign. 'replicated' = both sets CI-supported with the same sign. Duplicate records: first wins.", ""]
    L += ["## Single-policy rates", "", "| policy | condition | n_orig | orig | n_rep | rep |", "|---|---|---:|---:|---:|---:|"]
    data = {}
    for p in POLICIES:
        for c in CONDS:
            data[(p, c)] = (load(args.orig, p, c, args.n), load(args.rep, p, c, args.n))
            o, r = data[(p, c)]
            L.append(f"| {p} | {c} | {len(o)} | {np.mean(list(o.values())) if o else float('nan'):.3f} | {len(r)} | {np.mean(list(r.values())) if r else float('nan'):.3f} |")
    L += ["", "## Pairs", ""]
    replicated, disagreements = [], []
    for a, b in itertools.combinations(POLICIES, 2):
        L += [f"### {a} vs {b}", "", "| condition | n | Δ orig | 95% | sign | Δ rep | 95% | sign | Δ pooled | 95% | verdict |", "|---|---:|---:|---|---|---:|---|---|---:|---|---|"]
        for c in CONDS:
            (ao, ar), (bo, br) = data[(a, c)], data[(b, c)]
            eo, er = sorted(set(ao) & set(bo)), sorted(set(ar) & set(br))
            if not eo or not er:
                L.append(f"| {c} | {min(len(eo), len(er))} | | | | | | | | | incomplete |")
                continue
            do, dr = [ao[e] - bo[e] for e in eo], [ar[e] - br[e] for e in er]
            mo, lo_o, hi_o = boot(do, rng)
            mr, lo_r, hi_r = boot(dr, rng)
            mp, lo_p, hi_p = boot(do + dr, rng)
            so, sr = sign(lo_o, hi_o), sign(lo_r, hi_r)
            if so != "0" and so == sr:
                verdict = "replicated"
                replicated.append((a, b, c, mo, mr))
            elif so != "0" and sr != "0":
                verdict = "SIGN CONFLICT"
                disagreements.append((a, b, c, mo, mr))
            elif so != "0" or sr != "0":
                verdict = "one set only"
            else:
                verdict = "undecided in both"
            L.append(f"| {c} | {len(eo)}+{len(er)} | {mo:+.3f} | [{lo_o:+.2f}, {hi_o:+.2f}] | {so} | {mr:+.3f} | [{lo_r:+.2f}, {hi_r:+.2f}] | {sr} | {mp:+.3f} | [{lo_p:+.2f}, {hi_p:+.2f}] | {verdict} |")
        L.append("")
    L += ["## Summary", "",
          f"- CI-supported and replicated (same sign in both seed sets): {len(replicated)}",
          *[f"  - {a} vs {b} @ {c}: orig {mo:+.3f}, rep {mr:+.3f}" for a, b, c, mo, mr in replicated],
          f"- CI-supported in both sets with opposite signs: {len(disagreements)}",
          *[f"  - {a} vs {b} @ {c}: orig {mo:+.3f}, rep {mr:+.3f}" for a, b, c, mo, mr in disagreements], ""]
    text = "\n".join(L)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
