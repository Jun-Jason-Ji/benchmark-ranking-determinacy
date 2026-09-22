"""Core case, N seed sets: torque limit x0.5 (calibration-invisible) vs nominal, OpenVLA-7B (4-bit) against the Octo
eggplant policy set. For every seed set (and optionally the original SIMPLER stack) report
  (1) the paired single-policy change  rate(force_x0.5) - rate(nominal)  per policy,
  (2) per pair Octo - OpenVLA: Δ under nominal and under force_x0.5, the decision (CI excludes 0 -> decidable), and the
      paired change of Δ with its CI,
  (3) across-set verdicts: decision pattern replicated in k/N sets; Δ-change CI-supported in k/N sets; pooled estimate.
Paired bootstrap on common episode_ids, first record wins for duplicates. Sets are compared at the same n (--n) so a set
with fewer episodes truncates the others; --n 0 uses each set's full common range.

Usage: python scripts/analyze_openvla_torque_sets.py --n 48
       python scripts/analyze_openvla_torque_sets.py --n 96 --sets A=results/controller_sweep_gpu B=results/controller_sweep_gpu_rep
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
OPENVLA = "openvla-7b-4bit"
OCTO = ["octo-small", "octo-base", "octo-small@hist1", "octo-base@hist1"]
CONDS = ("nominal", "force_x0.5")
DEFAULT_SETS = ["A=results/controller_sweep_gpu", "B=results/controller_sweep_gpu_rep", "C=results/controller_sweep_gpu_rep3",
                "A-ms2=results/controller_sweep_ms2"]
ENV_BY_ROOT = {"results/controller_sweep_ms2": "PutEggplantInBasketScene-v0"}


def load(root, policy, cond, env, n):
    """episode_id -> success, truncated to episode_id < n (n <= 0 keeps all). For a deterministic policy the
    episodes beyond the config grid repeat earlier configurations bit-for-bit, so they are dropped: keeping
    them would count the same configuration twice and shrink the bootstrap interval for free."""
    f = ROOT / root / policy / env / f"{cond}.jsonl"
    d = {}
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                if n <= 0 or r["episode_id"] < n:
                    d.setdefault(r["episode_id"], int(bool(r["success"])))
    if is_deterministic(policy):
        seen, keep = set(), {}
        for e in sorted(d):
            c = config_id(env, e)
            if c not in seen:
                seen.add(c)
                keep[e] = d[e]
        return keep
    return d


def boot(x, rng, n=20000):
    x = np.asarray(x, float)
    if len(x) == 0:
        return float("nan"), float("nan"), float("nan")
    m = x[rng.integers(0, len(x), size=(n, len(x)))].mean(1)
    return float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def decision(lo, hi):
    return "Octo>" if lo > 0 else ("OpenVLA>" if hi < 0 else "abstain")


def fmt(m, lo, hi):
    return f"{m:+.3f} [{lo:+.2f}, {hi:+.2f}]"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sets", nargs="*", default=DEFAULT_SETS, help="label=root entries")
    ap.add_argument("--n", type=int, default=48)
    ap.add_argument("--env", default="PutEggplantInBasketScene-v1")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    rng = np.random.default_rng(0)
    sets = [s.split("=", 1) for s in args.sets]
    data = {}  # (label, policy, cond) -> {ep: succ}
    for label, root in sets:
        env = ENV_BY_ROOT.get(root, args.env)
        for p in [OPENVLA] + OCTO:
            for c in CONDS:
                data[(label, p, c)] = load(root, p, c, env, args.n)
    L = [f"# Torque x0.5 × OpenVLA: {len(sets)} runs / stacks, episodes < {args.n or 'all'}", "",
         "Sets: " + "; ".join(f"{l} = `{r}`" for l, r in sets) + ". Paired bootstrap (20000) on common episode_ids; first record wins. "
         "Decision = 95% CI of Δ excludes 0. 'n' = paired episodes actually available (a cell is skipped if any side is missing).", "",
         f"**Config census.** `{args.env}` has {n_configs(args.env)} distinct initial configurations "
         f"(`{ENV_BY_ROOT.get('results/controller_sweep_ms2')}`: {n_configs(ENV_BY_ROOT['results/controller_sweep_ms2'])}); "
         "episode_id beyond that repeats a configuration exactly. OpenVLA is deterministic (`do_sample=False`, the per-episode "
         "seed is ignored), so for it the labelled sets are **re-runs of one configuration, not independent seed sets**, and "
         "repeated configs are dropped here; Octo samples its diffusion head from the per-episode seed, so its sets are genuine "
         "replicates. See `FINDING_seed_set_bug.md`.", "",
         "## 0. Coverage", "",
         "| set | policy | condition | episodes kept | distinct configs | census |", "|---|---|---|---:|---:|---|"]
    for label, root in sets:
        env = ENV_BY_ROOT.get(root, args.env)
        tot = n_configs(env)
        for p in [OPENVLA] + OCTO:
            for c in CONDS:
                d = data[(label, p, c)]
                if not d:
                    continue
                cfgs = {config_id(env, e) for e in d}
                L.append(f"| {label} | {p} | {c} | {len(d)} | {len(cfgs)} | {len(cfgs)}/{tot}"
                         f"{' **complete**' if tot and len(cfgs) == tot else ''} |")
    L.append("")

    # (1) single-policy effects
    L += ["## 1. Single-policy paired change, force_x0.5 − nominal", "",
          "| policy | " + " | ".join(f"{l} nominal | {l} force | {l} change [95%]" for l, _ in sets) + " |",
          "|---|" + "---:|---:|---|" * len(sets)]
    single_support = {}
    for p in [OPENVLA] + OCTO:
        row = [p]
        for label, _ in sets:
            a, b = data[(label, p, "nominal")], data[(label, p, "force_x0.5")]
            eps = sorted(set(a) & set(b))
            if not eps:
                row += ["–", "–", "–"]
                continue
            m, lo, hi = boot([b[e] - a[e] for e in eps], rng)
            single_support[(label, p)] = (lo > 0) - (hi < 0)
            row += [f"{np.mean([a[e] for e in eps]):.3f} ({sum(a[e] for e in eps)}/{len(eps)})",
                    f"{np.mean([b[e] for e in eps]):.3f} ({sum(b[e] for e in eps)}/{len(eps)})", fmt(m, lo, hi)]
        L.append("| " + " | ".join(row) + " |")
    L.append("")

    # (2) pairs
    L += ["## 2. Pairs Δ = Octo − OpenVLA", "", "| pair | set | n | Δ nominal [95%] | decision | Δ force_x0.5 [95%] | decision | Δ change [95%] | change supported |",
          "|---|---|---:|---|---|---|---|---|---|"]
    verdicts = []
    for o in OCTO:
        pattern, supported, pooled_change, n_sets = [], [], [], 0
        for label, _ in sets:
            av, af = data[(label, OPENVLA, "nominal")], data[(label, OPENVLA, "force_x0.5")]
            ov, of = data[(label, o, "nominal")], data[(label, o, "force_x0.5")]
            eps = sorted(set(av) & set(af) & set(ov) & set(of))
            if not eps:
                L.append(f"| {o} vs OpenVLA | {label} | 0 | – | – | – | – | – | – |")
                continue
            dn = [ov[e] - av[e] for e in eps]
            df = [of[e] - af[e] for e in eps]
            dc = [df[i] - dn[i] for i in range(len(eps))]
            mn, ln, hn = boot(dn, rng)
            mf, lf, hf = boot(df, rng)
            mc, lc, hc = boot(dc, rng)
            decn, decf = decision(ln, hn), decision(lf, hf)
            sup = "yes" if (lc > 0 or hc < 0) else "no"
            pattern.append((label, decn, decf))
            supported.append(sup == "yes")
            pooled_change += dc
            n_sets += 1
            L.append(f"| {o} vs OpenVLA | {label} | {len(eps)} | {fmt(mn, ln, hn)} | {decn} | {fmt(mf, lf, hf)} | {decf} | {fmt(mc, lc, hc)} | {sup} |")
        if n_sets:
            mp, lp, hp = boot(pooled_change, rng)
            L.append(f"| {o} vs OpenVLA | pooled | {len(pooled_change)} | | | | | {fmt(mp, lp, hp)} | {'yes' if (lp > 0 or hp < 0) else 'no'} |")
            verdicts.append((o, pattern, supported, (mp, lp, hp)))
    L.append("")

    # (3) verdicts
    L += ["## 3. Across-set verdicts", ""]
    for o, pattern, supported, (mp, lp, hp) in verdicts:
        k_dec = sum(1 for _, dn, df in pattern if dn == "Octo>" and df == "abstain")
        k_flip = sum(1 for _, dn, df in pattern if dn == "Octo>" and df == "OpenVLA>")
        L.append(f"- **{o} vs OpenVLA** ({len(pattern)} sets): decidable→abstain in {k_dec}/{len(pattern)} "
                 f"[{', '.join(f'{l}: {dn}→{df}' for l, dn, df in pattern)}]; sign flip in {k_flip}/{len(pattern)}; "
                 f"Δ-change CI-supported in {sum(supported)}/{len(supported)}; pooled Δ change {fmt(mp, lp, hp)}.")
    ks = [(l, s) for (l, p), s in single_support.items() if p == OPENVLA]
    L.append(f"- **OpenVLA single-policy torque effect**: CI-supported positive in {sum(1 for _, s in ks if s > 0)}/{len(ks)} sets "
             f"({', '.join(l for l, s in ks if s > 0)}); Octo policies CI-supported in "
             f"{sum(1 for (l, p), s in single_support.items() if p != OPENVLA and s != 0)}/{sum(1 for (l, p), s in single_support.items() if p != OPENVLA)} cells.")
    L.append("")

    # (4) run-to-run nondeterminism of the deterministic policy: pairwise agreement between labelled sets
    det_sets = [l for l, _ in sets if all(data[(l, OPENVLA, c)] for c in CONDS)]
    if len(det_sets) > 1:
        L += ["## 4. Run-to-run nondeterminism (OpenVLA, identical configuration)", "",
              "Same env configs, same deterministic policy: any disagreement is GPU/run nondeterminism, not sampling.", "",
              "| condition | run pair | common eps | success agreement | rate difference |", "|---|---|---:|---:|---:|"]
        for c in CONDS:
            for i, x in enumerate(det_sets):
                for y in det_sets[i + 1:]:
                    a, b = data[(x, OPENVLA, c)], data[(y, OPENVLA, c)]
                    eps = sorted(set(a) & set(b))
                    if not eps:
                        continue
                    agree = sum(a[e] == b[e] for e in eps)
                    L.append(f"| {c} | {x} vs {y} | {len(eps)} | {agree}/{len(eps)} ({agree / len(eps):.3f}) | "
                             f"{np.mean([a[e] for e in eps]) - np.mean([b[e] for e in eps]):+.3f} |")
        L.append("")
    text = "\n".join(L)
    out = Path(args.out) if args.out else ROOT / "results/controller_sweep_gpu_rep3" / f"analysis_openvla_torque_sets_n{args.n}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
