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
import sys
from pathlib import Path

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


def complete(sets, cond, env, n_cfg):
    """The delta for this condition, or None unless it is a complete census at every seed set.

    An envelope is a min/max, so ONE partial condition can move the bound with nothing to show it
    did. Configurations are covered in a deterministic order (config_id is a function of
    episode_id), so a partial condition is a systematic slice of object poses rather than a random
    sample of them. A partial run of this analysis once produced a set bound of [+0.0000, +0.1920]
    and the opposite conclusion to the complete data, which is why this gate exists.
    """
    r = mct.delta(sets, A, B, env, cond)
    if not r or r["n"] != n_cfg or min(r["runs"]) != len(sets):
        return None
    return r


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/FITTED_POINT.md")
    args = ap.parse_args()

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
            raw = mct.delta(fit_sets, A, B, env, FIT_POINT)
            got = f"{raw['n']}/{n_cfg} configs at {min(raw['runs'])}/{len(keys)} runs" if raw \
                else "no records"
            L += [f"**Incomplete: {got}.** No verdict reported; configurations are covered in a "
                  f"deterministic order, so a partial slice is a systematic subset of object poses "
                  f"rather than a random one.", ""]
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
