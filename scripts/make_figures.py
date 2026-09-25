"""Static figures (PNG, local) for the 2026-09-18 results. Run with .venv-windows-ms3 python.
Outputs results/figures/{fig_replay_identifiability,fig_delta_by_condition,fig_eggplant_contact}.png
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.ticker import FixedLocator, NullLocator, FixedFormatter  # noqa: E402
from paper_labels import condition_label  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/figures"
OUT.mkdir(parents=True, exist_ok=True)
SWEEP = ROOT / "results/controller_sweep_gpu"
GRID = ROOT / "results/replay_sysid_100/grid"  # 98 demos, shards 0-3
ENVS = {"carrot": "PutCarrotOnPlateInScene-v1", "spoon": "PutSpoonOnTableClothInScene-v1", "eggplant": "PutEggplantInBasketScene-v1"}
plt.rcParams.update({"font.family": ["DejaVu Sans", "Arial", "sans-serif"], "font.size": 9, "axes.spines.top": False, "axes.spines.right": False})


def boot(d, n=10000, seed=0):
    d = np.asarray(d, float)
    if len(d) == 0:
        return np.nan, np.nan, np.nan
    rng = np.random.default_rng(seed)
    m = d[rng.integers(0, len(d), size=(n, len(d)))].mean(axis=1)
    return float(d.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def replay_err(cond):
    f = GRID / f"{cond}.jsonl"
    return {json.loads(l)["episode_id"]: json.loads(l)["mean_total_err"] for l in f.read_text(encoding="utf-8").splitlines() if l.strip()}


def success(policy, env, cond):
    f = SWEEP / policy / env / f"{cond}.jsonl"
    if not f.exists():
        return {}
    return {json.loads(l)["episode_id"]: int(bool(json.loads(l)["success"])) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()}


# ---------------- Figure 1: replay identifiability ----------------
def fig_replay():
    # All panels show paired changes, not absolute replay loss. Sharing the y-axis
    # makes the near-insensitivity of common gain scaling directly comparable.
    fig, axes = plt.subplots(1, 3, figsize=(6.85, 2.85), sharey=True)
    nom = replay_err("s1_d1_delay0")

    def paired_change(cond):
        values = replay_err(cond)
        common = sorted(set(values) & set(nom))
        return boot([values[i] - nom[i] for i in common])

    def draw_points(ax, x, stats, color, *, connect=True):
        means, lower, upper = np.asarray(stats).T
        ax.errorbar(x, means, yerr=[means - lower, upper - means],
                    fmt="o-" if connect else "o", color=color,
                    capsize=2.5, markersize=4.5, linewidth=1.2, zorder=3)
        # The reference compared with itself is exactly zero by definition.
        reference_x = 1 if connect else 0
        ax.plot(reference_x, 0, "o", color=color, markerfacecolor="white",
                markersize=4.5, markeredgewidth=1.2, zorder=4)

    # (a) d/k: damping is fixed at 1; stiffness scale s gives d/k = 1/s.
    settings = [0.5, 0.7, 1, 1.4, 2]
    ratio_points = sorted((1 / s, paired_change(f"s{s:g}_d1_delay0")) for s in settings)
    ratios, stats = zip(*ratio_points)
    draw_points(axes[0], ratios, stats, "#1f77b4")
    axes[0].set_xscale("log")
    axes[0].xaxis.set_major_locator(FixedLocator(ratios))
    axes[0].xaxis.set_major_formatter(FixedFormatter([f"{r:.3g}" for r in ratios]))
    axes[0].xaxis.set_minor_locator(NullLocator())
    axes[0].set_xlabel("Ratio $d/k$ ($\\times$ nominal)\nLog scale", fontsize=8)
    axes[0].set_ylabel("Replay-loss change from nominal", fontsize=8)
    axes[0].set_title("(a) Gain ratio", fontsize=8.5)

    # (b) Equal stiffness and damping multipliers leave d/k unchanged.
    scale_stats = [paired_change(f"s{s:g}_d{s:g}_delay0") for s in settings]
    draw_points(axes[1], settings, scale_stats, "#c77400")
    axes[1].set_xscale("log")
    axes[1].xaxis.set_major_locator(FixedLocator(settings))
    axes[1].xaxis.set_major_formatter(FixedFormatter([f"{s:g}" for s in settings]))
    axes[1].xaxis.set_minor_locator(NullLocator())
    axes[1].set_xlabel("Common gain scale ($\\times$ nominal)\nLog scale", fontsize=8)
    axes[1].set_title("(b) Common gain scaling", fontsize=8.5)
    maximum = max(abs(row[0]) for row in scale_stats)
    mantissa, exponent = f"{maximum:.1e}".split("e")
    axes[1].text(0.5, 0.58, "Largest absolute mean change\n"
                 + rf"${mantissa} \times 10^{{{int(exponent)}}}$",
                 transform=axes[1].transAxes, ha="center", va="center", fontsize=8)

    # (c) Include the actual zero-delay reference instead of an isolated bar.
    delay_stats = [paired_change("s1_d1_delay0"), paired_change("s1_d1_delay1")]
    draw_points(axes[2], [0, 1], delay_stats, "#2a8336", connect=False)
    axes[2].set_xticks([0, 1])
    axes[2].set_xlim(-0.3, 1.3)
    axes[2].set_xlabel("Execution delay (steps)", fontsize=8)
    axes[2].set_title("(c) Execution delay", fontsize=8.5)

    for ax in axes:
        ax.axhline(0, color="#777777", linewidth=0.7, zorder=1)
        ax.set_ylim(-0.00065, 0.011)
        ax.tick_params(labelsize=8)
    for ax in axes[1:]:
        ax.tick_params(axis="y", left=False, labelleft=False)
        ax.spines["left"].set_visible(False)
    fig.subplots_adjust(left=0.105, right=0.985, bottom=0.24, top=0.88, wspace=0.26)
    fig.savefig(OUT / "fig_replay_identifiability.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


# ---------------- Figure 2: Δ by condition per task with compatible-set verdict ----------------
CLASS = {"nominal": "identifiable (nominal)", "stiff_x0.5": "identifiable", "stiff_x2.0": "identifiable", "damp_x0.5": "identifiable", "damp_x2.0": "identifiable",
         "delay_1": "identifiable", "stiff_x0.25": "identifiable", "stiff_x4.0": "identifiable", "damp_x0.25": "identifiable", "damp_x4.0": "identifiable", "delay_2": "identifiable",
         "iso_x0.25": "invisible: controller", "iso_x0.5": "invisible: controller", "iso_x2.0": "invisible: controller", "iso_x4.0": "invisible: controller", "force_x0.5": "invisible: controller",
         "fric_x0.4": "invisible: contact", "fric_x2.5": "invisible: contact", "dens_x0.5": "invisible: contact", "dens_x2.0": "invisible: contact"}
COLORS = {"identifiable (nominal)": "#000000", "identifiable": "#7f7f7f", "invisible: controller": "#d62728", "invisible: contact": "#ff7f0e"}
ORDER = ["nominal", "stiff_x0.5", "stiff_x2.0", "damp_x0.5", "damp_x2.0", "delay_1", "stiff_x0.25", "stiff_x4.0", "damp_x0.25", "damp_x4.0", "delay_2",
         "iso_x0.25", "iso_x0.5", "iso_x2.0", "iso_x4.0", "force_x0.5", "fric_x0.4", "fric_x2.5", "dens_x0.5", "dens_x2.0"]


def fig_delta():
    """Delta by simulator condition, computed with the core table's own estimator.

    This figure previously read `results/controller_sweep_gpu` directly through success() and
    bootstrapped per episode. That was wrong in three compounding ways: the directory is the
    pre-fix inference-server generation, which Sect. 5.5 disqualifies from being pooled with
    current data; a per-episode bootstrap targets the generalisation value where the paper's
    standard estimand is the benchmark value (Sect. 5.4); and the union ran over nine invisible
    conditions where the core table uses five, giving a wider band. The result was a figure whose
    caption reported "set abstains" on spoon and eggplant where Table 6 reports the union bound
    declaring -- a contradiction a reader comparing the two would find immediately.

    It now calls make_core_table.delta() on the same seed sets and the same five invisible
    conditions, so figure and table cannot disagree: they are the same computation. Available seed
    sets differ by task (five for eggplant, two for spoon and carrot), which is why Table 6's runs
    column differs by row; the caption states it.
    """
    import make_core_table as mct
    mct.SETS_MS3 = dict(mct.SEED_SETS_OCTO)
    sets = mct.SETS_MS3
    A, B = "octo-small", "octo-base"
    conds = ["nominal"] + list(mct.INVISIBLE)

    fig, axes = plt.subplots(1, 3, figsize=(6.85, 3.9), sharey=True)  # 174 mm journal width
    for ax, (name, env) in zip(axes, ENVS.items()):
        labels, ys, Ls, Us, cols, runs = [], [], [], [], [], []
        for c in conds:
            r = mct.delta(sets, A, B, env, c)
            if not r:
                continue
            labels.append(c); ys.append(r["delta"]); Ls.append(r["lo"]); Us.append(r["hi"])
            cols.append(COLORS[CLASS[c]]); runs.append(r["runs"])
        x = np.arange(len(ys))
        for xi, m, lo, hi, col in zip(x, ys, Ls, Us, cols):
            ax.errorbar(xi, m, yerr=[[m - lo], [hi - m]], fmt="o", color=col, capsize=2, ms=4,
                        zorder=3)
        ax.axhline(0, color="k", lw=0.8)
        # The envelope spans nominal together with the invisible conditions: the compatible set
        # contains the fitted nominal parameter by construction, so a bound that left it out would
        # not cover the set. Same convention as make_core_table, which shares this estimator.
        inv = [i for i, c in enumerate(labels) if CLASS[c].startswith("invisible") or c == "nominal"]
        if inv:
            L_set, U_set = min(Ls[i] for i in inv), max(Us[i] for i in inv)
            # EPS has no alpha channel and the PostScript backend draws a translucent patch as
            # a solid one, which is how the shipped Fig4 came to cover its own points. The fill is
            # therefore the already-blended colour at full opacity, with the two bounds drawn as
            # dashed lines so the envelope reads as an interval and not as a wash.
            ax.axhspan(L_set, U_set, xmin=0, xmax=1, color="#fceeee", zorder=0)
            for yb in (L_set, U_set):
                ax.axhline(yb, color="#d62728", lw=0.6, ls=(0, (3, 2)), zorder=1)
            uv = mct.verdict(L_set, U_set, A, B)
            nom = labels.index("nominal")
            pv = mct.verdict(Ls[nom], Us[nom], A, B)
            # Verdicts and bounds belong in the caption, not inside the figure file (journal rule).
            # Printed so the caption cannot drift, and so any disagreement with Table 6 is visible
            # the moment it appears.
            # Four decimals, not two: one of these bounds sits at +0.000042, and a bound that
            # rounds to +0.00 is a declaration resting on a knife edge. The caption has to be able
            # to say so, which it cannot if the diagnostic hides it.
            print(f"  Fig4 {name}: point={pv}  set={uv}  bounds=[{L_set:+.4f}, {U_set:+.4f}]  "
                  f"runs={runs[nom][0]}/{runs[nom][1]}")
        ax.set_title(name, fontsize=9)
        ax.set_xticks(x)
        ax.set_xticklabels([condition_label(c) for c in labels], rotation=90, ha="center", fontsize=8)
        ax.tick_params(axis="y", labelsize=8)
        ax.set_ylim(-0.35, 0.65)
    axes[0].set_ylabel(r"$\Delta$ (S $-$ B; probability points)", fontsize=8.5)
    handles = [plt.Line2D([], [], marker="o", ls="", color=c, label=k) for k, c in COLORS.items()
               if k in {CLASS[c] for c in conds}]
    axes[-1].legend(handles=handles, loc="upper right", fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "fig_delta_by_condition.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


# ---------------- Figure 3: eggplant contact 96 ----------------
def fig_eggplant():
    env = ENVS["eggplant"]
    conds = ["nominal", "fric_x0.4", "dens_x0.5"]
    labels = ["nominal\n(friction 0.5)", "friction 0.2", "density ×0.5"]
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    w = 0.36
    for j, (pol, col) in enumerate([("octo-small", "#1f77b4"), ("octo-base", "#ff7f0e")]):
        rates, lo, hi = [], [], []
        for c in conds:
            d = success(pol, env, c); k, n = sum(d.values()), len(d)
            r = k / n; a, b = wilson(k, n); rates.append(r); lo.append(r - a); hi.append(b - r)
        ax.bar(np.arange(3) + (j - 0.5) * w, rates, width=w, yerr=[lo, hi], color=col, capsize=3, label=pol)
    ax.set_xticks(np.arange(3)); ax.set_xticklabels(labels); ax.set_ylabel("success rate (96 episodes, Wilson 95%)"); ax.set_ylim(0, 0.8)
    ax.legend(frameon=False)
    ax.set_title("Eggplant: object contact parameters (invisible to free-space calibration)\nΔ(small−base): +0.21 [+0.08,+0.32] → +0.05 [−0.07,+0.18] (friction), +0.07 [−0.04,+0.19] (density)", fontsize=8)
    fig.tight_layout(); fig.savefig(OUT / "fig_eggplant_contact.png", dpi=180, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    fig_replay(); fig_delta(); fig_eggplant()
    print("figures written to", OUT)
