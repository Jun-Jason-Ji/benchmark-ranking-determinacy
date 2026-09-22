"""Deployment-variant policy pairs: find near-tied pairs at nominal and check whether any
calibration-invisible condition flips or un-decides them.

Usage: python scripts/analyze_variant_pairs.py --root results/controller_sweep_gpu --out results/controller_sweep_gpu/analysis_variant_pairs.md
Policies = every directory under root that has the env; conditions = variants_v1 set.
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

ENVS = ["PutEggplantInBasketScene-v1", "PutSpoonOnTableClothInScene-v1"]
CONDS = ["nominal", "iso_x0.25", "iso_x4.0", "force_x0.5", "fric_x0.4", "dens_x0.5"]


DEDUPE = "first"  # duplicate episode_id records (two writers on one file): keep the first completed record


def load(root, policy, env, cond, n_max=24):
    f = Path(root) / policy / env / f"{cond}.jsonl"
    if not f.exists():
        return {}
    d = {}
    for line in f.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            if r["episode_id"] < n_max:
                if DEDUPE == "first" and r["episode_id"] in d:
                    continue
                d[r["episode_id"]] = int(bool(r["success"]))
    return d


def boot(d, n=10000, seed=0):
    d = np.asarray(d, float)
    if len(d) == 0:
        return float("nan"), float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    m = d[rng.integers(0, len(d), size=(n, len(d)))].mean(axis=1)
    return float(d.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="results/controller_sweep_gpu")
    ap.add_argument("--out", default="results/controller_sweep_gpu/analysis_variant_pairs.md")
    ap.add_argument("--tie", type=float, default=0.10, help="|Δ| threshold for 'near-tied' at nominal")
    ap.add_argument("--n", type=int, default=24, help="use episode_ids < n")
    ap.add_argument("--dedupe", choices=["first", "last"], default="first", help="rule for duplicate episode_id records")
    args = ap.parse_args()
    global DEDUPE
    DEDUPE = args.dedupe
    policies = sorted(p.name for p in Path(args.root).iterdir() if p.is_dir() and (p / ENVS[0]).exists())
    L = [f"# Deployment-variant policy pairs (same {args.n} episode_ids per condition; duplicate records: keep {args.dedupe})", "",
         f"Policies: {', '.join(policies)}. Near-tied = |Δ| ≤ {args.tie} at nominal with both rates in [0.2, 0.8].", ""]
    for env in ENVS:
        data = {p: {c: load(args.root, p, env, c, args.n) for c in CONDS} for p in policies}
        L += [f"## {env}", "", "### Nominal success rates", "", "| policy | n | rate |", "|---|---:|---:|"]
        for p in policies:
            d = data[p]["nominal"]
            if d:
                L.append(f"| {p} | {len(d)} | {np.mean(list(d.values())):.3f} |")
        L += ["", "### All pairs at nominal (Δ = rate(A) − rate(B), paired)", "", "| A | B | n | Δ | 95% | near-tied |", "|---|---|---:|---:|---|---|"]
        tied = []
        for a, b in itertools.combinations(policies, 2):
            da, db = data[a]["nominal"], data[b]["nominal"]
            common = sorted(set(da) & set(db))
            if len(common) < 12:
                continue
            m, lo, hi = boot([da[e] - db[e] for e in common])
            ra, rb = np.mean([da[e] for e in common]), np.mean([db[e] for e in common])
            nt = abs(m) <= args.tie and 0.2 <= ra <= 0.8 and 0.2 <= rb <= 0.8
            if nt:
                tied.append((a, b))
            L.append(f"| {a} | {b} | {len(common)} | {m:+.3f} | [{lo:+.2f}, {hi:+.2f}] | {'yes' if nt else ''} |")
        L += ["", f"### Near-tied pairs under calibration-invisible conditions ({len(tied)} pairs)", ""]
        flips = []
        for a, b in tied:
            L += [f"#### {a} vs {b}", "", "| condition | n | Δ | 95% | sign |", "|---|---:|---:|---|---|"]
            signs = {}
            for c in CONDS:
                da, db = data[a][c], data[b][c]
                common = sorted(set(da) & set(db))
                if not common:
                    continue
                m, lo, hi = boot([da[e] - db[e] for e in common])
                s = "+" if lo > 0 else ("−" if hi < 0 else "0")
                signs[c] = (m, s)
                L.append(f"| {c} | {len(common)} | {m:+.3f} | [{lo:+.2f}, {hi:+.2f}] | {s} |")
            L.append("")
            ss = {s for _, s in signs.values() if s != "0"}
            if len(ss) == 2:
                flips.append((env, a, b, {c: v[0] for c, v in signs.items()}))
            elif any(v[0] > 0 for v in signs.values()) and any(v[0] < 0 for v in signs.values()):
                L.append(f"point-estimate sign change across conditions for {a} vs {b}: {{ {', '.join(f'{c}: {v[0]:+.2f}' for c, v in signs.items())} }}")
                L.append("")
        L += ["### CI-supported sign flips among near-tied pairs", ""]
        L += [f"- {e}: {a} vs {b}: {s}" for e, a, b, s in flips] if flips else ["None."]
        L.append("")
    text = "\n".join(L)
    Path(args.out).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
