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
    fig, axes = plt.subplots(1, 3, figsize=(6.85, 2.9))  # 174 mm journal full-column width
    nom = replay_err("s1_d1_delay0")
    # (a) ratio curve at scale 1 (damping 1): s in {0.5,0.7,1,1.4,2}
    ratios, means, los, his = [], [], [], []
    for s in [0.5, 0.7, 1, 1.4, 2]:
        e = replay_err(f"s{s:g}_d1_delay0"); common = sorted(set(e) & set(nom))
        m, lo, hi = boot([e[i] - nom[i] for i in common]); ratios.append(s); means.append(m); los.append(lo); his.append(hi)
    ax = axes[0]
    ax.errorbar(ratios, means, yerr=[np.array(means) - np.array(los), np.array(his) - np.array(means)], fmt="o-", color="#1f77b4", capsize=3)
    ax.axhline(0, color="k", lw=0.8); ax.set_xscale("log"); ax.xaxis.set_major_locator(FixedLocator(ratios)); ax.xaxis.set_major_formatter(FixedFormatter([f"{r:g}" for r in ratios])); ax.xaxis.set_minor_locator(NullLocator())
    ax.set_xlabel(r"ratio $d/k$ ($\times$ nominal)", fontsize=8)
    ax.set_ylabel(r"$\Delta$ replay error vs nominal", fontsize=8)
    ax.set_title("(a) ratio", fontsize=8.5)
    # (b) scale axis at ratio 1: s=d in {0.5,0.7,1,1.4,2}
    ax = axes[1]
    scales, means2, los2, his2 = [], [], [], []
    for s in [0.5, 0.7, 1, 1.4, 2]:
        e = replay_err(f"s{s:g}_d{s:g}_delay0"); common = sorted(set(e) & set(nom))
        m, lo, hi = boot([e[i] - nom[i] for i in common]); scales.append(s); means2.append(m); los2.append(lo); his2.append(hi)
    ax.errorbar(scales, means2, yerr=[np.array(means2) - np.array(los2), np.array(his2) - np.array(means2)], fmt="s-", color="#d62728", capsize=3)
    ax.axhline(0, color="k", lw=0.8); ax.set_xscale("log"); ax.xaxis.set_major_locator(FixedLocator(scales)); ax.xaxis.set_major_formatter(FixedFormatter([f"{r:g}" for r in scales])); ax.xaxis.set_minor_locator(NullLocator())
    ax.set_ylim(axes[0].get_ylim())
    ax.set_xlabel(r"common scale ($\times$ nominal)", fontsize=8)
    ax.set_title("(b) common scale", fontsize=8.5)
    # (c) delay
    ax = axes[2]
    vals = []
    for cond, lab in [("s1_d1_delay1", "delay 1 step")]:
        e = replay_err(cond); common = sorted(set(e) & set(nom)); vals.append((lab,) + boot([e[i] - nom[i] for i in common]))
    lab, m, lo, hi = vals[0]
    ax.bar([0], [m], yerr=[[m - lo], [hi - m]], color="#2ca02c", capsize=4, width=0.5); ax.set_xticks([0]); ax.set_xticklabels([lab])
    ax.axhline(0, color="k", lw=0.8); ax.set_ylim(axes[0].get_ylim())
    ax.set_title("(c) delay", fontsize=8.5)
    # No in-figure title: the journal forbids titles inside figure files, and the caption carries it.
    for a in axes:
        a.tick_params(labelsize=8)
    fig.tight_layout(); fig.savefig(OUT / "fig_replay_identifiability.png", dpi=180, bbox_inches="tight"); plt.close(fig)


# ---------------- Figure 2: Δ by condition per task with compatible-set verdict ----------------
CLASS = {"nominal": "identifiable (nominal)", "stiff_x0.5": "identifiable", "stiff_x2.0": "identifiable", "damp_x0.5": "identifiable", "damp_x2.0": "identifiable",
         "delay_1": "identifiable", "stiff_x0.25": "identifiable", "stiff_x4.0": "identifiable", "damp_x0.25": "identifiable", "damp_x4.0": "identifiable", "delay_2": "identifiable",
         "iso_x0.25": "invisible: controller", "iso_x0.5": "invisible: controller", "iso_x2.0": "invisible: controller", "iso_x4.0": "invisible: controller", "force_x0.5": "invisible: controller",
         "fric_x0.4": "invisible: contact", "fric_x2.5": "invisible: contact", "dens_x0.5": "invisible: contact", "dens_x2.0": "invisible: contact"}
COLORS = {"identifiable (nominal)": "#000000", "identifiable": "#7f7f7f", "invisible: controller": "#d62728", "invisible: contact": "#ff7f0e"}
ORDER = ["nominal", "stiff_x0.5", "stiff_x2.0", "damp_x0.5", "damp_x2.0", "delay_1", "stiff_x0.25", "stiff_x4.0", "damp_x0.25", "damp_x4.0", "delay_2",
         "iso_x0.25", "iso_x0.5", "iso_x2.0", "iso_x4.0", "force_x0.5", "fric_x0.4", "fric_x2.5", "dens_x0.5", "dens_x2.0"]


def fig_delta():
    fig, axes = plt.subplots(1, 3, figsize=(6.85, 4.3), sharey=True)  # 174 mm journal width
    for ax, (name, env) in zip(axes, ENVS.items()):
        ys, labels, cols, Ls, Us, ns = [], [], [], [], [], []
        for c in ORDER:
            S, B = success("octo-small", env, c), success("octo-base", env, c)
            common = sorted(set(S) & set(B))
            if len(common) < 12:
                continue
            m, lo, hi = boot([S[i] - B[i] for i in common]); ys.append(m); Ls.append(lo); Us.append(hi)
            # The per-condition n moves to the caption: at 174 mm the tick labels cannot carry it.
            labels.append(c); ns.append(len(common)); cols.append(COLORS[CLASS[c]])
        x = np.arange(len(ys))
        for xi, m, lo, hi, col in zip(x, ys, Ls, Us, cols):
            ax.errorbar(xi, m, yerr=[[m - lo], [hi - m]], fmt="o", color=col, capsize=2, ms=4)
        ax.axhline(0, color="k", lw=0.8)
        inv = [i for i, c in enumerate(labels) if CLASS[c].startswith("invisible")]
        if inv:
            L_set, U_set = min(Ls[i] for i in inv), max(Us[i] for i in inv)
            ax.axhspan(L_set, U_set, xmin=0, xmax=1, color="#d62728", alpha=0.08, zorder=0)
            verdict = "small better" if L_set > 0 else ("base better" if U_set < 0 else "abstain")
            nom_i = labels.index("nominal")
            pv = "small better" if Ls[nom_i] > 0 else ("base better" if Us[nom_i] < 0 else "abstain")
            # Verdicts, set bounds and per-condition n belong in the caption, not inside the figure
            # file (journal rule). Printed here so the caption cannot drift from the data.
            print(f"  Fig3 {name}: point={pv}, set={verdict}, bounds=[{L_set:+.2f}, {U_set:+.2f}]")
            print(f"    n per condition: " + ", ".join(f"{c}={n}" for c, n in zip(labels, ns)))
        ax.set_title(name, fontsize=9)
        ax.set_xticks(x); ax.set_xticklabels(labels, rotation=90, ha="center", fontsize=8)
        ax.tick_params(axis="y", labelsize=8)
        ax.set_ylim(-0.6, 0.8)
    axes[0].set_ylabel("$\\Delta$ = small $-$ base (paired, 95%)", fontsize=8.5)
    handles = [plt.Line2D([], [], marker="o", ls="", color=c, label=k) for k, c in COLORS.items()]
    axes[-1].legend(handles=handles, loc="upper right", fontsize=8, frameon=False)
    fig.tight_layout(); fig.savefig(OUT / "fig_delta_by_condition.png", dpi=180, bbox_inches="tight"); plt.close(fig)


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
