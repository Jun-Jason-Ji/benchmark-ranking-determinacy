"""The benchmark-value estimator: what a SIMPLER task actually measures once its config grid is enumerated.

A SIMPLER task defines a finite set of initial configurations (scripts/task_configs.py). Define the estimand as
the benchmark's own value: the mean success over ALL of its configurations, averaged over policy noise. Then

  * a deterministic policy (OpenVLA) run over the full grid gives that value EXACTLY -- no sampling error at all,
    only run-to-run GPU nondeterminism, which is measured separately by re-running;
  * a stochastic policy (Octo) has only policy noise left, which shrinks with the number of seed sets and is
    estimated here from the spread across seed sets, not from an episode bootstrap.

So the benchmark's own statistical error can be driven to zero, while the simulator-parameter ambiguity (the
compatible set) cannot. That is the sharpest form of the paper's claim: with sampling error removed by
construction, a calibration-invisible parameter still changes whether the ranking can be declared.

Reports per condition: each policy's benchmark value per seed set, the seed-averaged value, coverage of the grid,
and Δ = Octo − OpenVLA per seed set with the across-seed range. A decision is declared only when every seed set
agrees in sign on the full census.

Usage: python scripts/analyze_benchmark_value.py --env PutEggplantInBasketScene-v1 --conditions nominal,force_x0.5
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
sys.path.insert(0, str(ROOT / "scripts"))
from task_configs import config_id, is_deterministic, n_configs  # noqa: E402

# Seed sets, current server generation only. The original "A" (results/controller_sweep_gpu, 2026-09-18 16:46)
# predates the XLA determinism flags and drifts against a re-run of its own seeds (see
# results/controller_sweep_gpu_replayA/FINDING_platform_drift.md), so A' replaces it; pass --legacy-a to
# include the old directory for comparison.
SEED_SETS = {"A'": "results/controller_sweep_gpu_replayA", "B": "results/controller_sweep_gpu_rep",
             "C": "results/controller_sweep_gpu_rep3",
             # T2-A (scripts/queue_t2a_seeds.py) takes the eggplant census to S=5; empty until it runs.
             "D": "results/controller_sweep_gpu_rep4", "E": "results/controller_sweep_gpu_rep5"}
# The drift that disqualifies the pre-fix directory is specific to the WSL jax/XLA **Octo** server. OpenVLA has
# run on one unchanged Windows process throughout, so for it the original directory is current generation --
# and it is the only place its completed 64-configuration, six-condition census lives. Sources are therefore
# chosen per policy family, as in scripts/make_core_table.py; the first column is A' for Octo and A for OpenVLA.
SEED_SETS_DET = dict(SEED_SETS, **{"A'": "results/controller_sweep_gpu"})
LEGACY_A = {"A (pre-fix)": "results/controller_sweep_gpu"}


def sets_for(policy):
    return SEED_SETS_DET if is_deterministic(policy) else SEED_SETS
OPENVLA = "openvla-7b-4bit"
OCTO = ["octo-small", "octo-base", "octo-small@hist1", "octo-base@hist1"]


def per_config(root, policy, env, cond):
    """config_id -> mean success over the episodes that landed on it (first record per episode wins)."""
    f = ROOT / root / policy / env / f"{cond}.jsonl"
    acc = {}
    if f.exists():
        seen = set()
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                e = r["episode_id"]
                if e in seen:
                    continue
                seen.add(e)
                acc.setdefault(config_id(env, e), []).append(int(bool(r["success"])))
    return {c: float(np.mean(v)) for c, v in acc.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default="PutEggplantInBasketScene-v1")
    ap.add_argument("--conditions", default="nominal,force_x0.5")
    ap.add_argument("--legacy-a", action="store_true",
                    help="also include the pre-fix seed set A (results/controller_sweep_gpu)")
    ap.add_argument("--out", default="results/controller_sweep_gpu_rep3/analysis_benchmark_value.md")
    args = ap.parse_args()
    if args.legacy_a:
        SEED_SETS.update(LEGACY_A)
        SEED_SETS_DET.update(LEGACY_A)
    env, conds = args.env, args.conditions.split(",")
    total = n_configs(env)
    L = [f"# Benchmark value over the full configuration grid: {env}", "",
         f"The task has **{total}** initial configurations. A policy's benchmark value is its mean success over all of them. "
         "OpenVLA is deterministic, so a complete census is exact; Octo is stochastic, so its remaining error is policy noise, "
         "read off the spread across seed sets rather than from an episode bootstrap. A decision is declared only when every "
         "seed set agrees in sign on a complete census.", "",
         "Sources are chosen per policy family: Octo uses the post-fix inference-server generation "
         "(A′ = `controller_sweep_gpu_replayA`, B, C), while OpenVLA, whose server is one unchanged Windows "
         "process throughout, uses its original directory in the first column (A = `controller_sweep_gpu`), "
         "where its complete census lives.", ""]
    data = {}
    for label in SEED_SETS:
        for p in [OPENVLA] + OCTO:
            for c in conds:
                d = per_config(sets_for(p)[label], p, env, c)
                if d:
                    data[(label, p, c)] = d
    L += ["## Coverage and benchmark values", "", "| policy | condition | " + " | ".join(f"{l}" for l in SEED_SETS) + " |",
          "|---|---|" + "---|" * len(SEED_SETS)]
    for p in [OPENVLA] + OCTO:
        for c in conds:
            cells = []
            for label in SEED_SETS:
                d = data.get((label, p, c))
                cells.append("–" if not d else f"{np.mean(list(d.values())):.3f} ({len(d)}/{total}{'' if len(d) == total else ' partial'})")
            L.append(f"| {p} | {c} | " + " | ".join(cells) + " |")
    L.append("")
    L += ["## Δ = Octo − OpenVLA on the shared configurations", "",
          "| pair | condition | seed set | configs compared | census | Δ |", "|---|---|---|---:|---|---:|"]
    summary = {}
    for o in OCTO:
        for c in conds:
            for label in SEED_SETS:
                do, dv = data.get((label, o, c)), data.get((label, OPENVLA, c)) or next((data[(l, OPENVLA, c)] for l in SEED_SETS if (l, OPENVLA, c) in data), None)
                if not do or not dv:
                    continue
                common = sorted(set(do) & set(dv))
                if not common:
                    continue
                delta = float(np.mean([do[k] - dv[k] for k in common]))
                summary.setdefault((o, c), []).append((label, delta, len(common)))
                L.append(f"| {o} vs OpenVLA | {c} | {label} | {len(common)} | {'complete' if len(common) == total else 'partial'} | {delta:+.3f} |")
    L.append("")

    # Census estimator: with every configuration enumerated there is no config-sampling error left, so the only
    # variance is the policy noise averaged within each configuration (and the deterministic policy's run-to-run
    # noise). Var(Δ̂) = (1/N²) Σ_c [ s²_octo(c)/S_c + s²_vla(c)/R_c ], with per-config variances pooled across
    # configurations when a configuration has a single run (S_c = 1 gives no variance estimate of its own).
    def dedup(runs, policy):
        """Re-runs of a deterministic policy that came out identical are one observation, not several: seed sets
        B and C of OpenVLA are record-identical, and counting them twice would halve the variance for free."""
        if not is_deterministic(policy):
            return runs
        uniq = []
        for r in runs:
            if not any(set(r) == set(u) and all(r[k] == u[k] for k in r) for u in uniq):
                uniq.append(r)
        return uniq

    def census_delta(o, c):
        runs_o = dedup([data[(l, o, c)] for l in SEED_SETS if (l, o, c) in data], o)
        runs_v = dedup([data[(l, OPENVLA, c)] for l in SEED_SETS if (l, OPENVLA, c) in data], OPENVLA)
        if not runs_o or not runs_v:
            return None
        # union per policy, intersect across the pair: a shorter run still contributes the configurations
        # it covers, and the variance term divides by the per-configuration run count.
        cfgs = sorted(set().union(*[set(r) for r in runs_o]) & set().union(*[set(r) for r in runs_v]))
        if not cfgs:
            return None

        def stats(runs, policy):
            """Per-config mean and the variance of that mean's noise.

            With two or more runs of a configuration the variance is estimated empirically. With a single run
            there is nothing in the data to estimate it from: for a stochastic policy we fall back to the
            binomial model var = p(1-p) at the policy's observed rate (which reproduces the ordinary binomial
            interval, the honest answer for one draw per configuration), and for a deterministic policy the
            value is exact up to run-to-run GPU noise, which a single run cannot measure -- reported as 0 and
            flagged, never as a claim that there is none."""
            mean, var, cnt = {}, {}, {}
            for k in cfgs:
                vals = [r[k] for r in runs if k in r]
                mean[k] = float(np.mean(vals))
                cnt[k] = len(vals)
                var[k] = float(np.var(vals, ddof=1)) if len(vals) > 1 else None
            known = [v for v in var.values() if v is not None]
            if known:
                fill, model = float(np.mean(known)), "empirical"
            elif is_deterministic(policy):
                fill, model = 0.0, "single run (run-to-run noise unmeasured)"
            else:
                rate = float(np.mean([mean[k] for k in cfgs]))
                fill, model = rate * (1 - rate), "binomial fallback (1 run/config)"
            return mean, {k: (fill if v is None else v) for k, v in var.items()}, cnt, model

        mo, vo, so, model_o = stats(runs_o, o)
        mv, vv, sv, model_v = stats(runs_v, OPENVLA)
        n = len(cfgs)
        delta = float(np.mean([mo[k] - mv[k] for k in cfgs]))
        var = sum(vo[k] / so[k] + vv[k] / sv[k] for k in cfgs) / n ** 2
        se = float(np.sqrt(var))
        return dict(delta=delta, se=se, lo=delta - 1.96 * se, hi=delta + 1.96 * se, n=n,
                    runs=(len(runs_o), len(runs_v)), complete=(n == total), model=f"{model_o} / {model_v}")

    L += ["## Census estimator: Δ with policy-noise interval only", "",
          "With every configuration enumerated, the configuration-sampling error is zero by construction; the interval below "
          "covers only the policy noise of the stochastic policy and the run-to-run noise of the deterministic one, and it "
          "shrinks as 1/sqrt(runs). Anything that survives it is not a sampling artefact.", "",
          "| pair | condition | configs | census | Octo runs / OpenVLA runs | Δ | 95% (policy noise) | decision | variance model |",
          "|---|---|---:|---|---|---:|---|---|---|"]
    verdicts = {}
    for o in OCTO:
        for c in conds:
            r = census_delta(o, c)
            if not r:
                continue
            dec = "Octo>" if r["lo"] > 0 else ("OpenVLA>" if r["hi"] < 0 else "abstain")
            verdicts[(o, c)] = dec
            L.append(f"| {o} vs OpenVLA | {c} | {r['n']} | {'**complete**' if r['complete'] else 'partial'} | "
                     f"{r['runs'][0]} / {r['runs'][1]} | {r['delta']:+.3f} | [{r['lo']:+.3f}, {r['hi']:+.3f}] | {dec} | {r['model']} |")
    L.append("")

    # Union bound over the calibration-invisible conditions, computed on the census intervals: the compatible set
    # contains every one of these conditions, so a ranking may only be declared when the interval holds for all
    # of them -- i.e. over [min lo, max hi]. Nominal is the point-calibration comparison and stays out of the union.
    inv = [c for c in conds if c != "nominal"]
    if inv:
        L += ["## Point calibration vs union bound over the compatible set (census intervals)", "",
              "Point = the nominal condition alone, the usual practice. Union = the ranking must hold at every "
              "calibration-invisible condition, so the interval is [min lower bound, max upper bound] over " +
              ", ".join(f"`{c}`" for c in inv) + ". A pair where the two disagree is one where point calibration "
              "declares a ranking the calibration data cannot support.", "",
              "| pair | point Δ | point verdict | union interval | union verdict | disagreement |",
              "|---|---:|---|---|---|---|"]
        for o in OCTO:
            rn = census_delta(o, "nominal") if "nominal" in conds else None
            rows = [census_delta(o, c) for c in inv]
            rows = [r for r in rows if r]
            if not rn or not rows:
                continue
            lo, hi = min(r["lo"] for r in rows), max(r["hi"] for r in rows)
            pv = "Octo>" if rn["lo"] > 0 else ("OpenVLA>" if rn["hi"] < 0 else "abstain")
            uv = "Octo>" if lo > 0 else ("OpenVLA>" if hi < 0 else "abstain")
            L.append(f"| {o} vs OpenVLA | {rn['delta']:+.3f} | {pv} | [{lo:+.3f}, {hi:+.3f}] | {uv} | "
                     f"{'**yes**' if pv != uv else 'no'} |")
        L.append("")

    L += ["## Decision change per pair", "", "| pair | " + " | ".join(f"{c}" for c in conds) + " | change | sign agreement across runs |",
          "|---|" + "---|" * (len(conds) + 2)]
    for o in OCTO:
        decs = [verdicts.get((o, c), "–") for c in conds]
        agree = []
        for c in conds:
            ds = [d for _, d, _ in summary.get((o, c), [])]
            agree.append("same sign" if ds and (min(ds) > 0 or max(ds) < 0) else ("mixed" if ds else "–"))
        L.append(f"| {o} vs OpenVLA | " + " | ".join(decs) + " | " + " → ".join(decs) + " | " + " / ".join(agree) + " |")
    L.append("")
    text = "\n".join(L)
    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
