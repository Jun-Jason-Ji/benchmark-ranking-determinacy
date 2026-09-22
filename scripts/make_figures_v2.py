"""Paper figures for the census-era results (2026-09-20).

  fig_uncertainty_budget.png     the four sources of uncertainty that survive a configuration census:
                                 evaluation noise at 1/3/10 seeds, implementation-build drift, the shift
                                 caused by a calibration-invisible parameter, and the robot texture variant
                                 the benchmark averages over. The point of the figure is that only the
                                 first shrinks with budget. The bars are three different KINDS of quantity
                                 (a 95% half-width, a paired shift, a range over four settings); they share
                                 the unit of Δ but not a scale, each label says which, and their lengths
                                 must not be ranked against one another.
  fig_torque_by_orientation.png  the torque-limit effect decomposed over the eggplant orientation grid, for
                                 the deterministic policy (OpenVLA) and a stochastic one (Octo-small).

Every number is computed from the episode records, not typed in, so the figures cannot drift from the tables.
Colors are slots 1/7/2/3 of the validated categorical palette (checked with the dataviz validator, light mode).

Run with .venv-windows-ms3 python. Outputs to results/figures/.
"""
import itertools
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from task_configs import config_id, is_deterministic, n_configs  # noqa: E402

OUT = ROOT / "results/figures"
OUT.mkdir(parents=True, exist_ok=True)
EGG = "PutEggplantInBasketScene-v1"
NC = n_configs(EGG)
OCTO_SETS = {"A'": "results/controller_sweep_gpu_replayA", "B": "results/controller_sweep_gpu_rep",
             "C": "results/controller_sweep_gpu_rep3", "D": "results/controller_sweep_gpu_rep4",
             "E": "results/controller_sweep_gpu_rep5"}
DET_SETS = dict(OCTO_SETS, **{"A'": "results/controller_sweep_gpu"})
PRE_FIX = "results/controller_sweep_gpu"
OCTO = ["octo-small", "octo-base", "octo-small@hist1", "octo-base@hist1"]
OPENVLA = "openvla-7b-4bit"

BLUE, VIOLET, ORANGE, AQUA = "#2a78d6", "#4a3aa7", "#eb6834", "#1baf7a"
# Categorical slots 1/7/2/3 of the validated palette; slots 1,7,2,3 pass every hard gate on the
# adjacent pairlist in light mode (worst adjacent CVD dE 9.2, normal-vision 16.3). Aqua sits below
# 3:1 contrast on a white surface, so the relief rule applies -- every bar carries a direct value
# label and a named y-tick, so identity is never colour-alone.
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#b8b7b1"
plt.rcParams.update({"font.family": ["DejaVu Sans", "Arial", "sans-serif"], "font.size": 9,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": INK2, "axes.labelcolor": INK, "text.color": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "figure.facecolor": "white"})


def episode_ids(root, policy, cond, env=EGG):
    """The episode ids a directory actually holds. Needed because the directories differ in scope:
    seed set B and the pre-fix directory hold 96 episodes, the rest 64, and with 64 configurations
    ids 64-95 wrap back onto configs 0-31. Averaging each directory over its own full contents
    therefore compares different effective scopes -- see analyze_platform_drift_paired.py."""
    f = ROOT / root / policy / env / f"{cond}.jsonl"
    out = set()
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.add(json.loads(line)["episode_id"])
    return out


def common_ids(roots, policy, cond, env=EGG):
    """Episode ids present in every directory under comparison: the only scope on which an
    across-build or across-seed difference is a paired quantity."""
    sets = [episode_ids(r, policy, cond, env) for r in roots]
    sets = [s for s in sets if s]
    return set.intersection(*sets) if sets else set()


def per_config(root, policy, cond, env=EGG, ids=None):
    f = ROOT / root / policy / env / f"{cond}.jsonl"
    acc, seen = {}, set()
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                e = r["episode_id"]
                if e in seen or (ids is not None and e not in ids):
                    continue
                seen.add(e)
                acc.setdefault(config_id(env, e), []).append(int(bool(r["success"])))
    return {c: float(np.mean(v)) for c, v in acc.items()}


def runs(sets, policy, cond):
    out = [d for d in (per_config(r, policy, cond) for r in sets.values()) if d]
    if is_deterministic(policy):
        uniq = []
        for r in out:
            if not any(set(r) == set(u) and all(r[k] == u[k] for k in r) for u in uniq):
                uniq.append(r)
        return uniq
    return out


def merged(sets, policy, cond):
    rs = runs(sets, policy, cond)
    if not rs:
        return {}
    keys = set().union(*[set(r) for r in rs])
    return {k: float(np.mean([r[k] for r in rs if k in r])) for k in keys}


def seed_sd():
    """Median sd of Δ across same-generation seed sets, over Octo pairs and the two core conditions.

    Restricted to the episode ids every seed set holds. Seed set B carries 96 episodes against 64
    elsewhere, so without this the sd mixes one-observation-per-configuration draws with
    two-observations-for-half-the-grid draws and is not a pure across-seed quantity.
    """
    sds = []
    roots = list(OCTO_SETS.values())
    for a, b in itertools.combinations(OCTO, 2):
        for cond in ("nominal", "force_x0.5"):
            ids = common_ids(roots, a, cond) & common_ids(roots, b, cond)
            if not ids:
                continue
            ds = []
            for root in roots:
                da, db = per_config(root, a, cond, ids=ids), per_config(root, b, cond, ids=ids)
                cfgs = sorted(set(da) & set(db))
                if len(cfgs) == NC:
                    ds.append(float(np.mean([da[k] - db[k] for k in cfgs])))
            if len(ds) >= 2:
                sds.append(float(np.std(ds, ddof=1)))
    return float(np.median(sds)) if sds else float("nan")


def build_drift():
    """Effect of the implementation build on the POLICY DIFFERENCE, same seeds, different server build.

    Returns (max |change in Delta|, mean |change in Delta|, per-condition detail).

    This used to return max |rate(pre-fix) - rate(A')| over policy x condition -- the largest change
    in a *single policy's* success rate, which was 0.078125. That is the wrong quantity for this
    paper twice over: it is not a difference between policies, so it does not belong on a Delta axis
    or in a table of effects on Delta; and a maximum over four cells is not an effect size. What the
    argument needs is how much the build moves Delta = rate(small) - rate(base), which is larger:
    -0.109 at nominal and -0.063 under the halved torque limit.

    Paired on the episode ids the two builds share. The pre-fix directory holds 96 episodes against
    A's 64, and ids 64-95 wrap onto configs 0-31, so an unpaired comparison mixes different effective
    scopes (scripts/analyze_platform_drift_paired.py).
    """
    detail = {}
    for cond in ("nominal", "force_x0.5"):
        rates = {}
        for p in ("octo-small", "octo-base"):
            ids = common_ids([PRE_FIX, OCTO_SETS["A'"]], p, cond)
            if not ids:
                continue
            a = per_config(PRE_FIX, p, cond, ids=ids)
            b = per_config(OCTO_SETS["A'"], p, cond, ids=ids)
            cfgs = sorted(set(a) & set(b))
            if len(cfgs) != NC:
                continue
            rates[p] = (float(np.mean([a[k] for k in cfgs])), float(np.mean([b[k] for k in cfgs])))
        if len(rates) == 2:
            pre = rates["octo-small"][0] - rates["octo-base"][0]
            post = rates["octo-small"][1] - rates["octo-base"][1]
            detail[cond] = post - pre
    if not detail:
        return float("nan"), float("nan"), {}
    v = np.abs(list(detail.values()))
    return float(v.max()), float(v.mean()), detail


def parameter_shift():
    """mean over Octo policies of Δ(nominal) - Δ(force x0.5) against OpenVLA: the calibration-invisible shift."""
    shifts = []
    for o in OCTO:
        vals = {}
        for cond in ("nominal", "force_x0.5"):
            mo, mv = merged(OCTO_SETS, o, cond), merged(DET_SETS, OPENVLA, cond)
            cfgs = sorted(set(mo) & set(mv))
            if cfgs:
                vals[cond] = float(np.mean([mo[k] - mv[k] for k in cfgs]))
        if len(vals) == 2:
            shifts.append(vals["nominal"] - vals["force_x0.5"])
    return float(np.mean(shifts)) if shifts else float("nan")


def texture_variant_range():
    """Range of one policy's benchmark value across the four urdf_version recolourings of the robot model.

    The fractal grid is urdf_version x can orientation x xy, so the variant index is (ep % 300) // 75
    (scripts/controller_sweep_ms2.py). urdf_version changes texture colour only and carries no physics, which
    is why this bar belongs in the same budget as the physical parameters: it is invisible to replay
    calibration for the same reason the torque limit is (paper_draft_s4_s5.md §5.5).
    """
    path = ROOT / "results/fractal_validation/octo-base/GraspSingleOpenedCokeCanInScene-v0/nominal.jsonl"
    per_variant = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            per_variant.setdefault((r["episode_id"] % 300) // 75, []).append(float(r["success"]))
    rates = [float(np.mean(v)) for _, v in sorted(per_variant.items())]
    return (float(max(rates) - min(rates)), rates) if rates else (float("nan"), [])


def texture_variant_delta_span():
    """Span of the policy DIFFERENCE across the four urdf_version recolourings, on the fractal pair.

    texture_variant_range() above is the span of a single policy's rate, which is the right number
    for "how much does the published rate depend on a parameter carrying no physics" but the wrong
    one for a figure whose axis is Delta: a rate and a difference of rates are not the same object,
    and putting one on the other's axis is the error this function exists to avoid. Here we take
    Delta = rate(rt-1-converged) - rate(rt-1-15pct) within each variant, over the 300-configuration
    census, and report its span across the four variants.
    """
    base = ROOT / "results/fractal_reversal"
    env = "GraspSingleOpenedCokeCanInScene-v0"
    per = {}
    for pol in ("rt-1-converged", "rt-1-15pct"):
        f = base / pol / env / "nominal.jsonl"
        if not f.exists():
            return float("nan"), []
        seen, acc = set(), {}
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            e = r["episode_id"]
            if e in seen:
                continue
            seen.add(e)
            acc.setdefault((e % 300) // 75, {})[e % 75] = int(bool(r["success"]))
        per[pol] = acc
    deltas = []
    for v in sorted(set(per["rt-1-converged"]) & set(per["rt-1-15pct"])):
        a, b = per["rt-1-converged"][v], per["rt-1-15pct"][v]
        cfgs = sorted(set(a) & set(b))
        if cfgs:
            deltas.append(float(np.mean([a[c] - b[c] for c in cfgs])))
    return (float(max(deltas) - min(deltas)), deltas) if deltas else (float("nan"), [])


def fig_uncertainty_budget():
    sd = seed_sd()
    drift_max, drift_mean, drift_detail = build_drift()
    shift = parameter_shift()
    tex_range, tex_rates = texture_variant_range()
    tex_span, tex_deltas = texture_variant_delta_span()
    # EVERY bar is now a quantity in units of Delta, the policy difference. That was not true
    # before: the build bar was a single policy's rate change and the texture bar a single policy's
    # rate range, and neither is a difference between policies, so neither belonged on this axis.
    # They remain three different KINDS of Delta-quantity -- a 95% half-width, a shift, and a span
    # across settings -- so each label says which, and the caption says not to rank them by length.
    rows = [("Evaluation noise, 1 seed\n(95% half-width of $\\Delta$)", 1.96 * sd, BLUE, 0.45),
            ("Evaluation noise, 3 seeds\n(95% half-width of $\\Delta$)", 1.96 * sd / np.sqrt(3), BLUE, 0.70),
            ("Evaluation noise, 10 seeds\n(95% half-width of $\\Delta$)", 1.96 * sd / np.sqrt(10), BLUE, 0.95),
            ("Implementation build\n(shift in $\\Delta$)", drift_max, VIOLET, 1.0),
            ("Calibration-invisible parameter,\ntorque limit (shift in $\\Delta$)", shift, ORANGE, 1.0),
            ("Robot texture variant, no physics\n(span of $\\Delta$ over 4 settings)", tex_span, AQUA, 1.0)]
    print("  texture variant per-urdf rates (single policy): "
          + ", ".join(f"{r:.3f}" for r in tex_rates) + f"  range {tex_range:.4f}")
    print("  texture variant per-urdf Delta: " + ", ".join(f"{d:+.4f}" for d in tex_deltas)
          + f"  span {tex_span:.4f}")
    print("  build: shift in Delta per condition: "
          + ", ".join(f"{k} {v:+.4f}" for k, v in drift_detail.items())
          + f"   -> max |shift| {drift_max:.4f}, mean |shift| {drift_mean:.4f}")
    fig, ax = plt.subplots(figsize=(6.85, 3.5))  # 174 mm: the journal full-column width, so no rescale
    y = np.arange(len(rows))[::-1]
    vmax = max(r[1] for r in rows)
    for yi, (lab, v, col, alpha) in zip(y, rows):
        ax.barh(yi, v, height=0.52, color=col, alpha=alpha, edgecolor="white", linewidth=1.2, zorder=3)
        ax.text(v + vmax * 0.02, yi, f"{v:.3f}", va="center", ha="left", fontsize=8.5, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels([r[0] for r in rows], fontsize=8.5)
    ax.set_xlabel("effect on the success-rate difference $\\Delta$ (probability points).\n"
                  "Three different quantities; see each label.", fontsize=8.5)
    ax.set_xlim(0, vmax * 1.95)  # room for the right-hand brackets and their labels
    ax.grid(axis="x", color=MUTED, alpha=0.45, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    # right-hand brackets: what a bigger evaluation budget can and cannot buy
    bx = vmax * 1.26
    ax.plot([bx, bx], [y[0] + 0.3, y[2] - 0.3], color=BLUE, lw=1.4, solid_capstyle="round", clip_on=False, zorder=5)
    ax.text(bx + vmax * 0.03, y[1], "reducible:\n$\\propto 1/\\sqrt{\\mathrm{seeds}}$", va="center", ha="left",
            fontsize=8, color=BLUE)
    # the texture variant is irreducible for the same reason as the torque limit, so one bracket spans both
    ax.plot([bx, bx], [y[4] + 0.3, y[5] - 0.3], color=ORANGE, lw=1.4, solid_capstyle="round", clip_on=False, zorder=5)
    ax.text(bx + vmax * 0.03, (y[4] + y[5]) / 2, "irreducible without\nnew calibration evidence", va="center",
            ha="left", fontsize=8, color=ORANGE)
    fig.tight_layout()
    # bbox_inches="tight": the bracket labels sit outside the axes with clip_on=False, so a
    # default bbox crops them (and the two-line xlabel) at the canvas edge.
    fig.savefig(OUT / "fig_uncertainty_budget.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    return dict(seed_sd=sd, drift_max=drift_max, drift_mean=drift_mean, shift=shift,
                drift_detail=drift_detail)


ORIENT = ["-45", "0", "45", "90", "135", "180", "225", "270"]


def fig_torque_by_orientation():
    panels = [(OPENVLA, DET_SETS, "OpenVLA-7B (deterministic)"),
              ("octo-small", OCTO_SETS, "Octo-small (stochastic)")]
    fig, axes = plt.subplots(1, 2, figsize=(6.85, 3.1), sharex=True, sharey=True)  # 174 mm full-column
    for ax, (policy, sets, title) in zip(axes, panels):
        nom, frc = merged(sets, policy, "nominal"), merged(sets, policy, "force_x0.5")
        common = sorted(set(nom) & set(frc))
        y = np.arange(len(ORIENT))[::-1]
        for yi, q in zip(y, range(len(ORIENT))):
            ks = [k for k in common if k % len(ORIENT) == q]
            if not ks:
                continue
            a = float(np.mean([nom[k] for k in ks]))
            b = float(np.mean([frc[k] for k in ks]))
            ax.plot([a, b], [yi, yi], color=MUTED, lw=1.6, solid_capstyle="round", zorder=2)
            ax.plot(a, yi, "o", ms=6, color="white", mec=BLUE, mew=1.8, zorder=3)
            ax.plot(b, yi, "o", ms=6, color=ORANGE, mec="white", mew=1.2, zorder=4)
            ax.text(1.02, yi, f"{b - a:+.2f}", va="center", ha="left", fontsize=8,
                    color=ORANGE if b - a > 0.02 else INK2, transform=ax.get_yaxis_transform())
        ax.set_yticks(y)
        ax.set_yticklabels([f"{o}°" for o in ORIENT], fontsize=8.5)
        ax.set_title(title, fontsize=9.5, color=INK, pad=6)
        ax.set_xlim(-0.02, 1.0)
        ax.grid(axis="x", color=MUTED, alpha=0.45, linewidth=0.6)
        ax.set_axisbelow(True)
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
    axes[0].set_ylabel("eggplant orientation", fontsize=9)
    for ax in axes:
        ax.set_xlabel("success rate", fontsize=9)
    h = [plt.Line2D([], [], marker="o", ls="", ms=6, mfc="white", mec=BLUE, mew=1.8, label="nominal"),
         plt.Line2D([], [], marker="o", ls="", ms=6, color=ORANGE, mec="white", label="torque limit ×0.5")]
    fig.legend(handles=h, loc="lower center", ncol=2, frameon=False, fontsize=8.5, bbox_to_anchor=(0.5, 0.0))
    fig.tight_layout()
    fig.subplots_adjust(right=0.90, bottom=0.24)
    fig.savefig(OUT / "fig_torque_by_orientation.png", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    stats = fig_uncertainty_budget()
    print("uncertainty budget:", {k: round(v, 4) for k, v in stats.items()})
    fig_torque_by_orientation()
    print("wrote", OUT / "fig_uncertainty_budget.png", "and", OUT / "fig_torque_by_orientation.png")
