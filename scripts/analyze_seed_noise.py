"""How much of the run-to-run instability is policy noise, and how many seeds does a conclusion need?

With the configuration grid enumerated, the same 64 eggplant configurations are evaluated under several policy
seed sets. Holding the configurations fixed, the spread of Δ across seed sets is *pure policy noise* -- no
configuration sampling is involved. That gives three practically useful numbers per policy pair and condition:

  sd_seed  : the standard deviation of Δ across seed sets (policy noise at one seed)
  se(S)    : sd_seed / sqrt(S), the standard error after averaging S seeds
  S*       : the number of seeds needed for the half-width 1.96*se(S) to fall below |Δ|, i.e. for the sign of Δ
             to be resolvable at 95% -- infinite when Δ is zero within noise

and it can be compared against the ordinary i.i.d. episode bootstrap on a single seed set, which mixes the
configuration variance into the interval and therefore answers a different question (see
docs/methods_census_2026-09-19.md).

Usage: python scripts/analyze_seed_noise.py --env PutEggplantInBasketScene-v1 --conditions nominal,force_x0.5
"""
import argparse
import itertools
import json
import math
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

# Seed sets, current server generation only. The original "A" (results/controller_sweep_gpu, 2026-09-18 16:46)
# predates the XLA determinism flags and drifts against a re-run of its own seeds (see
# results/controller_sweep_gpu_replayA/FINDING_platform_drift.md), so A' replaces it; pass --legacy-a to
# include the old directory for comparison.
SEED_SETS = {"A'": "results/controller_sweep_gpu_replayA", "B": "results/controller_sweep_gpu_rep",
             "C": "results/controller_sweep_gpu_rep3",
             # T2-A (scripts/queue_t2a_seeds.py) takes the eggplant census to S=5; empty until it runs.
             "D": "results/controller_sweep_gpu_rep4", "E": "results/controller_sweep_gpu_rep5"}
LEGACY_A = {"A (pre-fix)": "results/controller_sweep_gpu"}
POLICIES = ["octo-small", "octo-base", "octo-small@hist1", "octo-base@hist1"]


def per_config(root, policy, env, cond, limit):
    f = ROOT / root / policy / env / f"{cond}.jsonl"
    acc, seen = {}, set()
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                e = r["episode_id"]
                if e in seen or e >= limit:
                    continue
                seen.add(e)
                acc.setdefault(config_id(env, e), []).append(int(bool(r["success"])))
    return {c: float(np.mean(v)) for c, v in acc.items()}


def boot(x, rng, n=20000):
    x = np.asarray(x, float)
    m = x[rng.integers(0, len(x), size=(n, len(x)))].mean(1)
    return float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default="PutEggplantInBasketScene-v1")
    ap.add_argument("--conditions", default="nominal,force_x0.5")
    ap.add_argument("--legacy-a", action="store_true",
                    help="also include the pre-fix seed set A (results/controller_sweep_gpu)")
    ap.add_argument("--out", default="results/controller_sweep_gpu_rep3/analysis_seed_noise.md")
    args = ap.parse_args()
    if args.legacy_a:
        SEED_SETS.update(LEGACY_A)
    env, conds = args.env, args.conditions.split(",")
    total = n_configs(env)
    rng = np.random.default_rng(0)
    data = {(l, p, c): per_config(r, p, env, c, total) for l, r in SEED_SETS.items() for p in POLICIES for c in conds}

    L = [f"# Policy noise across seed sets on a fixed configuration census: {env}", "",
         f"All seed sets are restricted to the same {total} configurations, so the spread of Δ across them is policy "
         "noise alone. `sd_seed` is that spread (sample sd over seed sets); `half-width at S seeds` is 1.96·sd_seed/√S; "
         "`S*` is the smallest number of seeds whose half-width falls below |Δ|. The last column is the ordinary i.i.d. "
         "episode bootstrap on the first listed seed set, which also carries the configuration variance and answers a different question.", "",
         "| pair | condition | seeds | Δ per seed | mean Δ | sd_seed | half-width @1 / @3 / @10 | S* | i.i.d. bootstrap 95% (one set) |",
         "|---|---|---:|---|---:|---:|---|---:|---|"]
    for a, b in itertools.combinations(POLICIES, 2):
        for c in conds:
            deltas, labels = [], []
            for l in SEED_SETS:
                da, db = data[(l, a, c)], data[(l, b, c)]
                cfgs = sorted(set(da) & set(db))
                if len(cfgs) < total:
                    continue
                deltas.append(float(np.mean([da[k] - db[k] for k in cfgs])))
                labels.append(l)
            if len(deltas) < 2:
                continue
            sd = float(np.std(deltas, ddof=1))
            mean = float(np.mean(deltas))
            hw = [1.96 * sd / math.sqrt(s) for s in (1, 3, 10)]
            star = "∞" if abs(mean) < 1e-9 or sd == 0 and abs(mean) == 0 else (
                "1" if 1.96 * sd < abs(mean) else str(int(math.ceil((1.96 * sd / abs(mean)) ** 2))) if mean else "∞")
            ref = labels[0]  # the first seed set that covers the census; the bootstrap is shown for one set only
            da, db = data[(ref, a, c)], data[(ref, b, c)]
            cfgs = sorted(set(da) & set(db))
            m, lo, hi = boot([da[k] - db[k] for k in cfgs], rng) if cfgs else (float("nan"),) * 3
            L.append(f"| {a} vs {b} | {c} | {len(deltas)} ({','.join(labels)}) | "
                     f"{', '.join(f'{d:+.3f}' for d in deltas)} | {mean:+.3f} | {sd:.3f} | "
                     f"{hw[0]:.3f} / {hw[1]:.3f} / {hw[2]:.3f} | {star} | [{lo:+.2f}, {hi:+.2f}] |")
    L.append("")
    sds = []
    for row in L:
        parts = row.split("|")
        if len(parts) > 7 and parts[6].strip().replace(".", "").isdigit():
            sds.append(float(parts[6]))
    if sds:
        L += ["## Practical reading", "",
              f"- Policy noise at one seed on this task: sd_seed = {np.median(sds):.3f} (median over pairs and conditions), "
              f"so a single-seed Δ carries a ±{1.96 * np.median(sds):.3f} uncertainty from the policy alone, "
              "before any configuration sampling.",
              f"- Averaging 3 seeds (the official SIMPLER protocol) cuts that to ±{1.96 * np.median(sds) / math.sqrt(3):.3f}; "
              f"10 seeds to ±{1.96 * np.median(sds) / math.sqrt(10):.3f}.",
              "- Compare with the parameter-induced shift measured on this task (torque ×0.5: ≈0.23): the ambiguity is "
              "larger than the policy noise at any realistic seed budget, which is why more evaluation cannot settle it.", ""]
    text = "\n".join(L)
    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
