"""Publication-style descriptive plots from saved synthetic results only."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "pilot/outputs"
with (OUT / "evidence_summary.csv").open(newline="", encoding="utf-8") as f:
    evidence = list(csv.DictReader(f))
with (OUT / "mechanism_summary.csv").open(newline="", encoding="utf-8") as f:
    mechanism = list(csv.DictReader(f))
colors = dict(random="#64748b", d_opt="#2563eb", c_opt="#d97706")
labels = dict(random="Random", d_opt="D-optimal", c_opt="c-optimal")
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
fig, axs = plt.subplots(2, 2, figsize=(11.8, 8.5), layout="constrained")

for scenario, color in [("null", "#b91c1c"), ("weak", "#d97706"), ("balanced", "#2563eb")]:
    rows = [r for r in mechanism if r["scenario"] == scenario]
    axs[0, 0].plot([int(r["n"]) for r in rows], [float(r["mean_delta_width"]) for r in rows],
                   "o-", label=scenario, color=color)
axs[0, 0].set(xscale="log", yscale="log", xlabel="Calibration observations",
              ylabel="Mean interval width", title="A. Null and weak excitation differ")
axs[0, 0].legend(frameon=False)

for method in colors:
    rows = [r for r in evidence if r["method"] == method and float(r["alpha"]) == .05
            and r["interval_type"] == "shared_parameter_set"]
    x = np.array([int(r["budget"]) for r in rows])
    y = np.array([float(r["decision_coverage"]) for r in rows])
    lo = np.array([float(r["decision_coverage_wilson95_low"]) for r in rows])
    hi = np.array([float(r["decision_coverage_wilson95_high"]) for r in rows])
    axs[0, 1].plot(x, y, "o-", label=labels[method], color=colors[method])
    axs[0, 1].fill_between(x, lo, hi, color=colors[method], alpha=.10)
axs[0, 1].set(xlabel="Additional evidence budget", ylabel="Decision coverage", ylim=(-.025, .85),
              title="B. Decisions at nominal alpha = 0.05")
axs[0, 1].legend(frameon=False)

for kind, label, color in [("shared_parameter_set", "Shared parameter set", "#2563eb"),
                           ("scalar_wald", "Single-contrast Wald", "#059669")]:
    rows = [r for r in evidence if r["method"] == "d_opt" and float(r["alpha"]) == .05
            and r["interval_type"] == kind]
    axs[1, 0].plot([int(r["budget"]) for r in rows], [float(r["decision_coverage"]) for r in rows],
                   "o-", label=label, color=color)
axs[1, 0].set(xlabel="Additional evidence budget", ylabel="Decision coverage", ylim=(-.025, .85),
              title="C. Strong baseline: one prespecified contrast")
axs[1, 0].legend(frameon=False)

for method in colors:
    rows = [r for r in evidence if r["method"] == method and int(r["budget"]) == 16
            and r["interval_type"] == "shared_parameter_set"]
    rows.sort(key=lambda r: float(r["decision_coverage"]))
    axs[1, 1].plot([float(r["decision_coverage"]) for r in rows],
                   [float(r["selective_risk"]) for r in rows], "o-",
                   label=labels[method], color=colors[method])
axs[1, 1].set(xlabel="Decision coverage", ylabel="Observed selective risk",
              title="D. Risk / coverage at budget 16", ylim=(-.002, .08))
axs[1, 1].legend(frameon=False)
for ax in axs.flat:
    ax.grid(alpha=.18)
fig.suptitle("Synthetic mechanism pilot | 300 trials per condition | NOT robot evidence", fontsize=14)
fig.supxlabel("Panel B bands: pointwise Wilson 95% intervals. Zero observed errors do not imply zero risk.", fontsize=9)
fig.savefig(OUT / "pilot_figure.png", dpi=180)
fig.savefig(OUT / "pilot_figure.pdf")
print(OUT / "pilot_figure.png")
