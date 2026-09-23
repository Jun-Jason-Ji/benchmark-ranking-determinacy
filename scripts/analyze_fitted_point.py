"""Does the policy ranking survive a move to the operating point the calibration data prefer?

Every rate this project reports, and every rate the benchmark publishes, is computed at the
simulator's shipped nominal controller setting. analyze_compatible_set_v2.py shows nominal is not
the replay loss minimiser: on both stacks the minimum is at (k x2, d x0.5, delay 1) and nominal is
rejected against it. So the manuscript's verdicts were conditional on an operating point the
calibration evidence does not select, and it could not say whether they would hold at the point it
does.

queue_fitted_point.py answers that by measurement. It evaluates both policies at the fitted point
and over its full calibration-invisible fibre -- six conditions mirroring the nominal fibre one for
one -- on two tasks, under seed sets whose bases match each task's own nominal census. The
comparison is therefore PAIRED in every respect that can be held fixed: same configurations, same
policy seeds episode for episode, same policies, same build, same estimator. Only the controller
setting differs.

The two fibres are the same size, which took an extra measurement to earn. The 50-point replay grid
samples ratio 0.25 exactly once, so the common-scale invariance was verified at seven other ratios
and not at the fitted one; an earlier version of this script reported a two-condition fitted fibre
for that reason. The `iso_at_fitted` replay preset closes it: sixteenfold scale sweep at ratio 0.25,
loss flat to 5.4 um on ManiSkill3 and 11.1 um on the original stack, against the 1356 um at which
the two stacks disagree at identical nominal parameters. Friction and density need no ratio-specific
argument, being unobserved by free-space replay at any ratio.

Both sides use make_core_table.delta, i.e. Eq. (eq:var) of the manuscript, so this is not a new
estimator. Nominal is restricted to the same seed sets as the fitted run on each task, because
comparing against a larger-budget interval would confound the operating point with the budget.

Usage: python scripts/analyze_fitted_point.py [--out results/FITTED_POINT.md]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import make_core_table as mct  # noqa: E402

A, B = "octo-small", "octo-base"
NOM_DIRS = {"A'": "results/controller_sweep_gpu_replayA",
            "C": "results/controller_sweep_gpu_rep3",
            "D": "results/controller_sweep_gpu_rep4"}
FIT_DIRS = {"A'": "results/controller_sweep_fitted_A",
            "C": "results/controller_sweep_fitted_C",
            "D": "results/controller_sweep_fitted_D"}
# task -> (env, n configs, which seed-set keys that task's census has)
TASKS = [("eggplant", "PutEggplantInBasketScene-v1", 64, ["A'", "C", "D"]),
         ("spoon", "PutSpoonOnTableClothInScene-v1", 24, ["A'", "C"])]
NOM_POINT = "nominal"
NOM_FIBRE = ["iso_x0.25", "iso_x4.0", "force_x0.5", "fric_x0.4", "dens_x0.5"]
FIT_POINT = "fitted"
FIT_FIBRE = ["fitted_iso_x0.25", "fitted_iso_x4.0", "fitted_force_x0.5",
             "fitted_fric_x0.4", "fitted_dens_x0.5"]


def census_status(sets, cond, env, n_cfg):
    """Per seed set and per policy: which of the expected episode ids are present.

    Returns (ok, detail). This checks the records directly rather than inferring completeness from
    the estimator's summary, because the summary cannot distinguish the cases. An earlier version
    tested `delta()['n'] == 64 and min(runs) == 3`, which a partial design can satisfy: the
    configuration count is a UNION across seed sets, so one complete set plus two sets holding a
    single configuration each still reports n=64, and the run count is a per-configuration minimum
    that the complete set can supply on its own. The expected ids here are 0..n_cfg-1, which is
    what the queue runs with --episodes n_cfg --episode-offset 0.
    """
    want = set(range(n_cfg))
    detail, ok = {}, True
    for key, root in sets.items():
        for pol in (A, B):
            f = ROOT / root / pol / env / f"{cond}.jsonl"
            have = set()
            if f.exists():
                for line in f.read_text(encoding="utf-8").splitlines():
                    if line.strip():
                        have.add(json.loads(line)["episode_id"])
            detail[(key, pol)] = len(have & want)
            if have & want != want:
                ok = False
    return ok, detail


def complete(sets, cond, env, n_cfg):
    """The delta for this condition, or None unless every seed set and policy has the full census.

    An envelope is a min/max, so ONE partial condition can move the bound with nothing to show it
    did. Configurations are covered in a deterministic order (config_id is a function of
    episode_id), so a partial condition is a systematic slice of object poses rather than a random
    sample of them. A partial run of this analysis once produced a set bound of [+0.0000, +0.1920]
    and the opposite conclusion to the complete data, which is why this gate exists -- and why it
    now verifies the records rather than the estimator's summary.
    """
    ok, _ = census_status(sets, cond, env, n_cfg)
    if not ok:
        return None
    return mct.delta(sets, A, B, env, cond)


def envelope(sets, point, others, env, n_cfg):
    """Union bound over {point} + others. The base point belongs to its own fibre by construction,
    so an envelope omitting it would not cover the fibre (Sect. 4.4)."""
    used, skipped = [], []
    for c in [point] + list(others):
        r = complete(sets, c, env, n_cfg)
        (used if r else skipped).append(r if r else c)
    if not used:
        return None
    return min(r["lo"] for r in used), max(r["hi"] for r in used), len(used), skipped


def paired_shift(nom_sets, fit_sets, env, n_cfg):
    """The change in Delta between the two operating points, on three explicit sampling models.

    D = Delta_fitted - Delta_nominal, paired per configuration. Which interval belongs around it is
    a question about what is random, and the paper's own estimand answers it: the 64 configurations
    are a FIXED, fully enumerated population, so they are not a sampling unit. What remains random
    is the policy seed within a configuration.

    The primary model therefore holds the grid fixed and keeps the pairing intact. Each seed set k
    supplies all four arms at configuration c, so it yields one complete shift

        d_c^(k) = [p_A,fit(c,k) - p_B,fit(c,k)] - [p_A,nom(c,k) - p_B,nom(c,k)],

    and the variance of the mean is N^-2 * sum_c Var_k(d_c^(k)) / K. This never assumes the four
    arms are independent -- any common effect of seed set k cancels inside d_c^(k) before the
    variance is taken, which is the point of pairing.

    Two sensitivities are reported beside it. Summing the four arms' run variances separately
    discards that pairing and treats the arms as independent, so it is wider. Treating whole seed
    sets as blocks with df = 2 is wider still. An earlier version of this paper reported the
    configuration-as-sampling-unit interval as primary; that answers a different question -- a fresh
    draw of configurations from a superpopulation -- which is the estimand Sect. 5 argues is not the
    benchmark's. All four contain zero, so the conclusion does not depend on the choice, and none of
    them is an exact finite-sample guarantee.

    Returns {model: (D, lo, hi)} or None if any arm is not a complete census.
    """
    arms = {}
    for tag, sets, cond in (("fit", fit_sets, FIT_POINT), ("nom", nom_sets, NOM_POINT)):
        for pol in (A, B):
            ok, _ = census_status(sets, cond, env, n_cfg)
            if not ok:
                return None
            arms[(tag, pol)] = mct.raw_by_config(sets, pol, env, cond)
    cfgs = sorted(set.intersection(*[set(v) for v in arms.values()]))
    if len(cfgs) != n_cfg:
        return None

    def mean(tag, pol, c):
        return float(np.mean(arms[(tag, pol)][c]))

    d_c = {c: (mean("fit", A, c) - mean("fit", B, c)) - (mean("nom", A, c) - mean("nom", B, c))
           for c in cfgs}
    D = float(np.mean([d_c[c] for c in cfgs]))
    out = {}

    # (1) fixed census, pairing kept inside each seed set -- primary.
    keys = sorted(set(nom_sets) & set(fit_sets))
    per_set = []
    for k in keys:
        one = {}
        for tag, sets, cond in (("fit", {k: fit_sets[k]}, FIT_POINT),
                                ("nom", {k: nom_sets[k]}, NOM_POINT)):
            for pol in (A, B):
                one[(tag, pol)] = mct.raw_by_config(sets, pol, env, cond)
        if not all(set(cfgs) <= set(v) for v in one.values()):
            per_set = []
            break
        per_set.append({c: (float(np.mean(one[("fit", A)][c])) - float(np.mean(one[("fit", B)][c])))
                        - (float(np.mean(one[("nom", A)][c])) - float(np.mean(one[("nom", B)][c])))
                        for c in cfgs})
    if len(per_set) >= 2:
        tot = sum(float(np.var([d[c] for d in per_set], ddof=1)) / len(per_set) for c in cfgs)
        se = float(np.sqrt(tot)) / len(cfgs)
        out["fixed census, pairing kept within seed set"] = (D, D - 1.96 * se, D + 1.96 * se)

    # (2) the same fixed census with the four arms treated as independent.
    tot = 0.0
    for c in cfgs:
        for key in arms:
            v = arms[key][c]
            var = float(np.var(v, ddof=1)) if len(v) > 1 else 0.0
            tot += var / len(v)
    se = float(np.sqrt(tot)) / len(cfgs)
    out["fixed census, four arms independent"] = (D, D - 1.96 * se, D + 1.96 * se)

    # (3) configurations as the sampling unit -- a superpopulation reading.
    sd = float(np.std([d_c[c] for c in cfgs], ddof=1)) / np.sqrt(len(cfgs))
    out["configurations as sampling unit"] = (D, D - 1.96 * sd, D + 1.96 * sd)

    # (4) whole seed sets as blocks, df = 2.
    per = []
    for k in keys:
        one_n, one_f = {k: nom_sets[k]}, {k: fit_sets[k]}
        rn, rf = mct.delta(one_n, A, B, env, NOM_POINT), mct.delta(one_f, A, B, env, FIT_POINT)
        if rn and rf:
            per.append(rf["delta"] - rn["delta"])
    if len(per) >= 2:
        m = float(np.mean(per))
        seb = float(np.std(per, ddof=1)) / np.sqrt(len(per))
        # Student t, two-sided 97.5%. df = 1 matters: spoon has two seed sets, and an earlier
        # version of this dict started at df = 2 and fell back to the normal quantile 1.96, which
        # understated that task's block half-width by a factor of six.
        t = {1: 12.706205, 2: 4.302653, 3: 3.182446, 4: 2.776445,
             5: 2.570582, 6: 2.446912}.get(len(per) - 1)
        if t is None:
            raise RuntimeError(f"no t quantile for df={len(per) - 1}; add it rather than "
                               "falling back to the normal quantile")
        out[f"seed sets as blocks, df={len(per) - 1}"] = (m, m - t * seb, m + t * seb)
        out["_per_set"] = per
    return out


def selftest():
    """Regression check on the completeness gate, using the real records.

    The pattern that used to slip through: one seed set holding the full census and the others
    holding a single configuration each. The configuration count is a union, so the estimator
    reported n=64 with runs=(3,3) and the old gate passed it. Anything that reports a complete
    design must fail here.
    """
    import shutil
    import tempfile
    env, n_cfg = "PutEggplantInBasketScene-v1", 64
    ok, det = census_status(FIT_DIRS, FIT_POINT, env, n_cfg)
    print(f"real census complete: {ok}  (per set/policy: {sorted(set(det.values()))})")
    assert ok, "the real fitted census should pass"
    tmp = Path(tempfile.mkdtemp())
    try:
        for key, keep_all in (("A", True), ("C", False)):
            src = FIT_DIRS["A'" if keep_all else "C"]
            for pol in (A, B):
                d = tmp / key / pol / env
                d.mkdir(parents=True)
                lines = (ROOT / src / pol / env / f"{FIT_POINT}.jsonl").read_text(
                    encoding="utf-8").splitlines()
                (d / f"{FIT_POINT}.jsonl").write_text(
                    "\n".join(lines if keep_all else lines[:1]), encoding="utf-8")
        bad, det2 = census_status({"A": str(tmp / "A"), "C": str(tmp / "C")},
                                  FIT_POINT, env, n_cfg)
        counts = {f"{k}/{p.split('-')[-1]}": v for (k, p), v in det2.items()}
        print(f"[64, 1] pattern rejected: {not bad}  (counts: {counts})")
        assert not bad, "a seed set with one configuration must not count as a census"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("selftest passed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/FITTED_POINT.md")
    ap.add_argument("--selftest", action="store_true",
                    help="regression-check the completeness gate and exit")
    args = ap.parse_args()
    if args.selftest:
        selftest()
        return

    L = ["# The ranking at the calibration-preferred operating point", "",
         "Complete configuration censuses, octo-small vs octo-base, evaluated at the benchmark's "
         "shipped controller setting and at the replay loss minimiser "
         "$(k\\times2, d\\times0.5, \\text{delay } 1)$. Seed-set bases match each task's own nominal "
         "census, so each comparison is paired on configuration and on policy seed. Estimator is "
         "Eq. (eq:var) via `make_core_table.delta`. Generated by "
         "`scripts/analyze_fitted_point.py`.", ""]
    summary = []

    for name, env, n_cfg, keys in TASKS:
        nom_sets = {k: NOM_DIRS[k] for k in keys}
        fit_sets = {k: FIT_DIRS[k] for k in keys}
        L += [f"## {name} ({n_cfg} configurations, {len(keys)} seed sets)", ""]

        nom_pt = complete(nom_sets, NOM_POINT, env, n_cfg)
        fit_pt = complete(fit_sets, FIT_POINT, env, n_cfg)
        if not fit_pt:
            _, det = census_status(fit_sets, FIT_POINT, env, n_cfg)
            got = ", ".join(f"{k}/{pol.split('-')[-1]} {v}/{n_cfg}" for (k, pol), v in det.items())
            L += [f"**Incomplete.** Episodes present per seed set and policy: {got}. No verdict "
                  f"reported; configurations are covered in a deterministic order, so a partial "
                  f"slice is a systematic subset of object poses rather than a random one.", ""]
            continue

        nom_env = envelope(nom_sets, NOM_POINT, NOM_FIBRE, env, n_cfg)
        fit_env = envelope(fit_sets, FIT_POINT, FIT_FIBRE, env, n_cfg)
        L += ["| operating point | $\\Delta$ | point 95% | point verdict | "
              "set bound | conditions | set verdict |", "|---|---:|---|---|---|---:|---|"]
        rows = [("nominal (shipped)", nom_pt, nom_env), ("fitted (minimiser)", fit_pt, fit_env)]
        for label, pt, ev in rows:
            if not pt:
                continue
            pv = mct.verdict(pt["lo"], pt["hi"], A, B)
            if ev:
                lo, hi, k, sk = ev
                sv, kn = mct.verdict(lo, hi, A, B), str(k) + ("*" if sk else "")
                sb = f"[{lo:+.4f}, {hi:+.4f}]"
            else:
                sb, kn, sv = "--", "0", "--"
            L.append(f"| {label} | {pt['delta']:+.4f} | [{pt['lo']:+.4f}, {pt['hi']:+.4f}] | {pv} | "
                     f"{sb} | {kn} | {sv} |")
        skipped = sorted({c for _, _, ev in rows if ev for c in ev[3]})
        if skipped:
            L += ["", f"\\* incomplete and excluded: {', '.join(skipped)}. The affected envelope is "
                  f"over fewer conditions than the design calls for and can only be narrower than "
                  f"the final one.", ""]

        if nom_pt and fit_pt:
            pflip = mct.verdict(nom_pt["lo"], nom_pt["hi"], A, B) != \
                mct.verdict(fit_pt["lo"], fit_pt["hi"], A, B)
            sflip = (nom_env and fit_env
                     and mct.verdict(nom_env[0], nom_env[1], A, B)
                     != mct.verdict(fit_env[0], fit_env[1], A, B))
            L += ["", f"- $\\Delta$ shifts by **{fit_pt['delta'] - nom_pt['delta']:+.4f}** "
                  f"between the two operating points.",
                  f"- Point verdict {'**flips**' if pflip else 'holds'}; "
                  f"set verdict {'**flips**' if sflip else 'holds'}"
                  + (" (provisional, a condition is still running)" if skipped else "") + ".", ""]
            summary.append((name, fit_pt["delta"] - nom_pt["delta"], pflip, sflip, bool(skipped)))

            ps = paired_shift(nom_sets, fit_sets, env, n_cfg)
            if ps:
                per = ps.pop("_per_set", None)
                L += ["The shift itself, paired per configuration, under each sampling model. The "
                      "first is the primary one because it matches this paper's estimand: the "
                      "configuration grid is enumerated and fixed, so what is random is the policy "
                      "seed within a configuration.", "",
                      "| sampling model | $D$ | 95% | resolved? |", "|---|---:|---|---|"]
                for i, (k, (d, lo, hi)) in enumerate(ps.items()):
                    tag = k + (" **(primary)**" if i == 0 else " (sensitivity)")
                    L.append(f"| {tag} | {d:+.4f} | [{lo:+.4f}, {hi:+.4f}] | "
                             f"{'yes' if lo > 0 or hi < 0 else 'no'} |")
                L.append("")
                if per:
                    same = all(v > 0 for v in per) or all(v < 0 for v in per)
                    ivs = [(d, lo, hi) for (d, lo, hi) in ps.values()]
                    n_zero = sum(1 for _, lo, hi in ivs if lo <= 0 <= hi)
                    if n_zero == len(ivs):
                        res = ("Every model above contains zero: the change in $\\Delta$ is not "
                               "resolved at this budget under any of them")
                    elif n_zero == 0:
                        res = ("No model above contains zero: the change in $\\Delta$ is resolved "
                               "under every sampling model we report")
                    else:
                        res = (f"{len(ivs) - n_zero} of the {len(ivs)} models above exclude zero "
                               "and the rest do not, so whether the change is resolved depends on "
                               "the sampling model")
                    L += ["Per seed set the shift is "
                          + ", ".join(f"${v:+.3f}$" for v in per)
                          + (", and the sets agree on its direction. " if same else
                             ", so the sets do not agree on its direction. ")
                          + res + ", and none of these intervals is an exact finite-sample "
                            "guarantee.", ""]

    if summary:
        L += ["## Across tasks", "",
              "| task | $\\Delta$ shift | point verdict | set verdict |", "|---|---:|---|---|"]
        for name, sh, pf, sf, prov in summary:
            L.append(f"| {name} | {sh:+.4f} | {'flips' if pf else 'holds'} | "
                     f"{'flips' if sf else 'holds'}{' (prov.)' if prov else ''} |")
        L += ["", "The union bound cannot protect against a change of operating point, and it is "
              "worth being clear that this is structural rather than a shortcoming of the "
              "particular fibre. The bound ranges over the directions the calibration data leave "
              "\\emph{unconstrained}; nominal and the minimiser differ in the gain ratio and the "
              "execution delay, which the data \\emph{identify}. A union over the invisible "
              "directions is silent about a move along an identified one by construction.", ""]
    text = "\n".join(L)
    (ROOT / args.out).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
