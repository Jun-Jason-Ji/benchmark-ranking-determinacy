"""Aggregate controller_sweep JSONL results into per-condition success rates, pairwise
policy differences with paired bootstrap CIs, and a sign-flip table.

Usage: python scripts/analyze_controller_sweep.py --root results/controller_sweep --out results/controller_sweep/analysis.md
Descriptive only. Episodes share episode_ids across policies/conditions (common random
numbers), so differences are paired by episode_id. Wilson intervals for single rates.
"""
import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

import sys as _sys
try:
    _sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import numpy as np


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def load(root):
    data = defaultdict(dict)  # (policy, env) -> condition -> {episode_id: success}
    meta = {}
    for jsonl in Path(root).rglob("*.jsonl"):
        env = jsonl.parent.name
        policy = jsonl.parent.parent.name
        cond = jsonl.stem
        eps = {}
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                eps[r["episode_id"]] = r
        data[(policy, env)][cond] = eps
        sj = jsonl.parent / "summary.json"
        if sj.exists():
            meta[(policy, env)] = json.loads(sj.read_text(encoding="utf-8"))
    return data, meta


def paired_boot(a, b, n_boot=5000, seed=0):
    rng = np.random.default_rng(seed)
    d = np.asarray(a, float) - np.asarray(b, float)
    if len(d) == 0:
        return float("nan"), (float("nan"), float("nan"))
    idx = rng.integers(0, len(d), size=(n_boot, len(d)))
    means = d[idx].mean(axis=1)
    return float(d.mean()), (float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="results/controller_sweep")
    ap.add_argument("--out", default="results/controller_sweep/analysis.md")
    args = ap.parse_args()
    data, meta = load(args.root)
    lines = ["# Controller sweep: descriptive analysis", "",
             "Exploratory ManiSkill3/Windows platform (torch-Jacobian IK adapter), not original SIMPLER. "
             "Paired by episode_id; Wilson 95% for rates; paired bootstrap 95% for differences.", ""]

    # 1. per policy/env/condition success table
    lines += ["## Success rates", "", "| policy | env | condition | n | success | rate | Wilson 95% | mean steps | mean inference s/step |",
              "|---|---|---|---:|---:|---:|---|---:|---:|"]
    for (policy, env), conds in sorted(data.items()):
        for cond, eps in sorted(conds.items()):
            n = len(eps)
            k = sum(r["success"] for r in eps.values())
            lo, hi = wilson(k, n)
            steps = np.mean([r["steps"] for r in eps.values()]) if n else float("nan")
            inf = np.mean([r["inference_seconds"] / max(r["steps"], 1) for r in eps.values()]) if n else float("nan")
            lines.append(f"| {policy} | {env} | {cond} | {n} | {k} | {k / n if n else float('nan'):.3f} | [{lo:.2f}, {hi:.2f}] | {steps:.1f} | {inf:.2f} |")
    lines.append("")

    # 2. pairwise policy differences per env and condition
    envs = sorted({e for (_, e) in data})
    policies = sorted({p for (p, _) in data})
    lines += ["## Pairwise differences Δ = rate(policy_i) − rate(policy_j), paired by episode", ""]
    flips = []
    for env in envs:
        for i in range(len(policies)):
            for j in range(i + 1, len(policies)):
                pi, pj = policies[i], policies[j]
                ci, cj = data.get((pi, env)), data.get((pj, env))
                if not ci or not cj:
                    continue
                lines += [f"### {env}: {pi} vs {pj}", "", "| condition | paired n | Δ | bootstrap 95% | sign |", "|---|---:|---:|---|---|"]
                signs = {}
                for cond in sorted(set(ci) & set(cj)):
                    common = sorted(set(ci[cond]) & set(cj[cond]))
                    a = [ci[cond][e]["success"] for e in common]
                    b = [cj[cond][e]["success"] for e in common]
                    d, (lo, hi) = paired_boot(a, b)
                    sign = "+" if lo > 0 else ("−" if hi < 0 else "0")
                    signs[cond] = (d, lo, hi, sign)
                    lines.append(f"| {cond} | {len(common)} | {d:+.3f} | [{lo:+.2f}, {hi:+.2f}] | {sign} |")
                lines.append("")
                pts = [v[0] for v in signs.values()]
                if pts and (max(pts) > 0 > min(pts)):
                    flips.append((env, pi, pj, {c: round(v[0], 3) for c, v in signs.items()}))
                # nominal vs each condition, per policy
    lines += ["## Point-estimate sign changes across conditions", ""]
    if flips:
        for env, pi, pj, s in flips:
            lines.append(f"- **{env}** {pi} vs {pj}: Δ by condition {s}")
        lines += ["", "A point-estimate sign change is *not* a confirmed ranking flip: check the bootstrap "
                  "intervals above; with 24 paired episodes most differences will be inconclusive."]
    else:
        lines.append("None observed in the point estimates so far.")
    lines.append("")

    # 3. within-policy sensitivity to conditions (vs nominal)
    lines += ["## Within-policy sensitivity vs nominal (paired)", "", "| policy | env | condition | paired n | rate − nominal | bootstrap 95% |", "|---|---|---|---:|---:|---|"]
    for (policy, env), conds in sorted(data.items()):
        if "nominal" not in conds:
            continue
        for cond in sorted(conds):
            if cond == "nominal":
                continue
            common = sorted(set(conds[cond]) & set(conds["nominal"]))
            a = [conds[cond][e]["success"] for e in common]
            b = [conds["nominal"][e]["success"] for e in common]
            d, (lo, hi) = paired_boot(a, b)
            lines.append(f"| {policy} | {env} | {cond} | {len(common)} | {d:+.3f} | [{lo:+.2f}, {hi:+.2f}] |")
    lines.append("")
    Path(args.out).write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
