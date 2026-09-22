"""Cluster bootstrap by initial configuration.

Episodes that land on the same configuration (`episode_id % n_configs`, see scripts/task_configs.py) are not
independent draws: they share the scene and differ only through policy noise. A task with 24 configurations run
for 96 episodes therefore carries 24 clusters of 4, not 96 independent samples, and an i.i.d. paired bootstrap
understates the interval whenever the configuration effect dominates the policy noise -- which it does here
(success is strongly config-dependent). This script recomputes every Δ both ways so the difference is visible.

Estimand: Δ = mean over configurations of the paired success difference, averaged over policy noise within a
configuration. Cluster bootstrap: resample configurations with replacement, keep all episodes of a drawn config.

Usage:
  python scripts/analyze_cluster_bootstrap.py --root results/controller_sweep_gpu --env PutCarrotOnPlateInScene-v1 \
      --policies octo-small,octo-base --conditions nominal,iso_x0.25,iso_x4.0 --n 96
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

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from task_configs import config_id, n_configs  # noqa: E402


def load(root, policy, env, cond, n):
    f = ROOT / root / policy / env / f"{cond}.jsonl"
    d = {}
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                if n <= 0 or r["episode_id"] < n:
                    d.setdefault(r["episode_id"], int(bool(r["success"])))
    return d


def boot_iid(x, rng, n=20000):
    x = np.asarray(x, float)
    m = x[rng.integers(0, len(x), size=(n, len(x)))].mean(1)
    return float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def boot_cluster(x, clusters, rng, n=20000):
    """x: per-episode values; clusters: same-length config ids. Resample config ids with replacement."""
    x = np.asarray(x, float)
    clusters = np.asarray(clusters)
    uniq = np.unique(clusters)
    groups = [x[clusters == c] for c in uniq]
    sums = np.array([g.sum() for g in groups])
    sizes = np.array([len(g) for g in groups])
    idx = rng.integers(0, len(uniq), size=(n, len(uniq)))
    m = sums[idx].sum(1) / sizes[idx].sum(1)
    return float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def verdict(lo, hi):
    return "+" if lo > 0 else ("−" if hi < 0 else "abstain")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="results/controller_sweep_gpu")
    ap.add_argument("--env", default="PutEggplantInBasketScene-v1")
    ap.add_argument("--policies", default="octo-small,octo-base")
    ap.add_argument("--conditions", default="nominal,iso_x0.25,iso_x4.0,force_x0.5,fric_x0.4,dens_x0.5")
    ap.add_argument("--n", type=int, default=96)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    rng = np.random.default_rng(0)
    pols = args.policies.split(",")
    conds = args.conditions.split(",")
    tot = n_configs(args.env)
    L = [f"# Cluster bootstrap by configuration: `{args.root}`, {args.env}, episodes < {args.n}", "",
         f"The task has **{tot}** distinct initial configurations; episodes beyond that repeat one "
         "(same scene, new policy noise). i.i.d. = the paired bootstrap used so far; cluster = configurations "
         "resampled with replacement. A verdict that holds i.i.d. but not under clustering was resting on "
         "repeated scenes.", "",
         "| pair | condition | eps | configs | reps/config | Δ | i.i.d. 95% | verdict | cluster 95% | verdict | width ratio |",
         "|---|---|---:|---:|---:|---:|---|---|---|---|---:|"]
    changed = []
    for a, b in itertools.combinations(pols, 2):
        for c in conds:
            da, db = load(args.root, a, args.env, c, args.n), load(args.root, b, args.env, c, args.n)
            eps = sorted(set(da) & set(db))
            if not eps:
                continue
            diff = [da[e] - db[e] for e in eps]
            cl = [config_id(args.env, e) for e in eps]
            m, li, hi_ = boot_iid(diff, rng)
            _, lc, hc = boot_cluster(diff, cl, rng)
            vi, vc = verdict(li, hi_), verdict(lc, hc)
            if vi != vc:
                changed.append((a, b, c, vi, vc))
            L.append(f"| {a} vs {b} | {c} | {len(eps)} | {len(set(cl))} | {len(eps) / len(set(cl)):.1f} | {m:+.3f} | "
                     f"[{li:+.2f}, {hi_:+.2f}] | {vi} | [{lc:+.2f}, {hc:+.2f}] | {vc} | {(hc - lc) / (hi_ - li):.2f} |")
    L += ["", "## Verdicts that do not survive clustering", ""]
    L += [f"- {a} vs {b} @ {c}: i.i.d. **{vi}**, clustered **{vc}**" for a, b, c, vi, vc in changed] or ["- none"]
    L.append("")
    text = "\n".join(L)
    if args.out:
        Path(ROOT / args.out).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / args.out).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
