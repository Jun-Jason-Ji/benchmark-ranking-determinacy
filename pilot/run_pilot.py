"""Run the preregistered synthetic mechanism experiment using NumPy only."""
from __future__ import annotations

import csv
from collections import defaultdict
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
import time
from xml.sax.saxutils import escape

import numpy as np

from model import (D, DIRECTIONS, G, S, classify, confidence_interval,
                   contains, contrast_wald, fit, linear_extrema, select_order)


ROOT = Path(__file__).resolve().parent


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def wilson(success, total):
    if not total:
        return None
    z = 1.959963984540054
    p = success / total
    den = 1 + z * z / total
    center = (p + z * z / (2 * total)) / den
    half = z * math.sqrt(p * (1-p) / total + z * z / (4*total*total)) / den
    return [center-half, center+half]


def decision_fields(interval, truth, delta):
    if interval is None or interval[0] > interval[1]:
        return {"empty": 1, "lower": "", "upper": "", "width": "",
                "delta_covered": 0, "decision": 0,
                "incorrect_claim": 0, "sign_error": 0}
    lower, upper = interval[:2]
    decision = classify(lower, upper, delta)
    return {"empty": 0, "lower": lower, "upper": upper, "width": upper-lower,
            "delta_covered": int(lower-1e-9 <= truth <= upper+1e-9),
            "decision": decision,
            "incorrect_claim": int(decision != 0 and decision*truth <= delta),
            "sign_error": int(decision != 0 and decision*truth <= 0)}


def aggregate(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[(row["method"], row["interval_type"], row["budget"], row["alpha"])].append(row)
    output = []
    for (method, interval_type, budget, alpha), group in groups.items():
        n = len(group)
        claims = sum(r["decision"] != 0 for r in group)
        errors = sum(r["incorrect_claim"] for r in group)
        covered = sum(r["delta_covered"] for r in group)
        widths = [r["width"] for r in group if r["width"] != ""]
        output.append({
            "method": method, "interval_type": interval_type, "budget": budget,
            "alpha": alpha, "trials": n,
            "parameter_coverage": sum(r["parameter_covered"] for r in group)/n,
            "delta_coverage": covered/n,
            "delta_coverage_wilson95_low": wilson(covered, n)[0],
            "delta_coverage_wilson95_high": wilson(covered, n)[1],
            "decision_coverage": claims/n,
            "decision_coverage_wilson95_low": wilson(claims, n)[0],
            "decision_coverage_wilson95_high": wilson(claims, n)[1],
            "claims": claims, "incorrect_claims": errors,
            "unconditional_incorrect_claim_rate": errors/n,
            "selective_risk": errors/claims if claims else "",
            "selective_risk_wilson95_low": wilson(errors, claims)[0] if claims else "",
            "selective_risk_wilson95_high": wilson(errors, claims)[1] if claims else "",
            "sign_errors": sum(r["sign_error"] for r in group),
            "empty_sets": sum(r["empty"] for r in group),
            "mean_interval_width_nonempty": float(np.mean(widths)) if widths else "",
            "point_ranking_error_rate": sum(r["point_sign_error"] for r in group)/n,
        })
    return output


def run_evidence(config):
    root_rng = np.random.SeedSequence(config["master_seed"])
    seeds = root_rng.spawn(config["trials"])
    initial_x = np.tile(S, (config["initial_samples"], 1))
    pool_x = np.repeat(DIRECTIONS, config["pool_repetitions_per_direction"], axis=0)
    deterministic_order = {
        method: select_order(method, pool_x, initial_x, None, config["selection_ridge"])
        for method in config["methods"] if method != "random"
    }
    rows = []
    designs = []
    for trial, seed in enumerate(seeds):
        rng = np.random.default_rng(seed)
        theta = rng.uniform(*config["sampling_box"], size=2)
        initial_y = initial_x @ theta + rng.normal(0, config["noise_sigma"], len(initial_x))
        # Shared finite pool: response draws are made once and hidden from selectors.
        pool_y = pool_x @ theta + rng.normal(0, config["noise_sigma"], len(pool_x))
        truth = float(G @ theta)
        for method in config["methods"]:
            order = (select_order(method, pool_x, initial_x, rng, config["selection_ridge"])
                     if method == "random" else deterministic_order[method])
            if trial == 0:
                designs.append({"method": method, "first_trial_selection_ids": order,
                                "selected_input_vectors": pool_x[order].tolist()})
            for budget in config["budgets"]:
                ids = order[:budget]
                x = np.vstack([initial_x, pool_x[ids]])
                y = np.concatenate([initial_y, pool_y[ids]])
                a, center, rank = fit(x, y)
                estimate = float(G @ center)
                # Forced point ranking uses pi1 for an exact/numerical tie.
                point_decision = 1 if estimate >= -1e-10 else -1
                for alpha in config["alphas"]:
                    radius2, interval = confidence_interval(a, center, rank, config["noise_sigma"], alpha)
                    parameter_covered = int(contains(a, center, radius2, theta))
                    base = {"trial": trial, "method": method, "budget": budget,
                            "alpha": alpha, "rank": rank,
                            "theta1": theta[0], "theta2": theta[1], "true_delta": truth,
                            "delta_hat": estimate, "parameter_covered": parameter_covered,
                            "point_sign_error": int(point_decision*truth <= 0)}
                    rows.append({**base, "interval_type": "shared_parameter_set",
                                 **decision_fields(interval, truth, config["delta"])})
                    wald = contrast_wald(a, center, config["noise_sigma"], alpha)
                    rows.append({**base, "interval_type": "scalar_wald",
                                 **decision_fields(wald, truth, config["delta"])})
    return rows, designs


def run_mechanism(config):
    rng = np.random.default_rng(config["master_seed"] + 1)
    theta = np.array(config["mechanism_theta"])
    rows = []
    for scenario in ("null", "weak", "balanced"):
        for n in config["mechanism_samples"]:
            if scenario == "null":
                x = np.tile(S, (n, 1))
            elif scenario == "weak":
                eps = config["weak_excitation"]
                x = (S + np.where(np.arange(n)[:, None] % 2 == 0, eps, -eps)*D) / math.sqrt(1+eps**2)
            else:
                x = np.where(np.arange(n)[:, None] % 2 == 0, S, D)
            a = x.T @ x
            rank = int(np.linalg.matrix_rank(a, tol=1e-10))
            eigvals, eigvecs = np.linalg.eigh(np.linalg.pinv(a, rcond=1e-12))
            # Exact distribution of the sufficient statistic; avoids materializing
            # 300 repeated long trajectories and is not a surrogate approximation.
            mean_center = np.linalg.pinv(a, rcond=1e-12) @ a @ theta
            factor = eigvecs @ np.diag(np.sqrt(np.maximum(eigvals, 0)))
            for trial in range(config["trials"]):
                center = mean_center + config["noise_sigma"] * factor @ rng.normal(size=2)
                radius2, interval = confidence_interval(a, center, rank, config["noise_sigma"], config["main_alpha"])
                aligned_interval = linear_extrema(a, center, radius2, S)
                row = {"scenario": scenario, "n": n, "trial": trial,
                       "rank": rank, "lambda_min_information": max(float(np.linalg.eigvalsh(a).min()), 0),
                       "parameter_covered": int(contains(a, center, radius2, theta)),
                       "aligned_sum_width": aligned_interval[1]-aligned_interval[0] if aligned_interval else "",
                       **decision_fields(interval, float(G@theta), config["delta"])}
                rows.append(row)
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["scenario"], row["n"]].append(row)
    aggregates = []
    for (scenario, n), group in grouped.items():
        aggregates.append({
            "scenario": scenario, "n": n, "rank": group[0]["rank"],
            "parameter_coverage": float(np.mean([r["parameter_covered"] for r in group])),
            "delta_coverage": float(np.mean([r["delta_covered"] for r in group])),
            "decision_coverage": float(np.mean([r["decision"] != 0 for r in group])),
            "mean_delta_width": float(np.mean([r["width"] for r in group if r["width"] != ""])),
            "mean_aligned_sum_width": float(np.mean([r["aligned_sum_width"] for r in group if r["aligned_sum_width"] != ""])),
        })
    return rows, aggregates


def make_figure(path, aggregates, mechanisms, config):
    colors = {"random": "#64748b", "d_opt": "#007f8b", "c_opt": "#c55334",
              "null": "#64748b", "weak": "#c55334", "balanced": "#007f8b"}
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="880" viewBox="0 0 1200 880">',
             '<rect width="1200" height="880" fill="#f9fafb"/>',
             '<style>text{font-family:Arial,sans-serif;fill:#18212b} .small{font-size:13px} .axis{font-size:14px}</style>',
             '<text x="50" y="38" font-size="23" font-weight="bold">Synthetic mechanism pilot: identifiability and policy ranking</text>',
             '<text x="50" y="64" font-size="14">300 trials | known Gaussian noise | two gain parameters | no robot or real-world evidence</text>']

    def panel(px, py, title, xlabel, ylabel, series, xmin, xmax, ymin, ymax, xticks, yticks):
        width, height = 455, 255
        ox, oy = px+58, py+38
        parts.append(f'<text x="{px}" y="{py+10}" font-size="17" font-weight="bold">{escape(title)}</text>')
        parts.append(f'<rect x="{ox}" y="{oy}" width="{width}" height="{height}" fill="white" stroke="#cbd5e1"/>')
        def sx(v): return ox+(v-xmin)/(xmax-xmin)*width
        def sy(v): return oy+height-(v-ymin)/(ymax-ymin)*height
        for v, label in xticks:
            parts.append(f'<text class="small" text-anchor="middle" x="{sx(v):.2f}" y="{oy+height+20}">{label}</text>')
        for v in yticks:
            parts.append(f'<line x1="{ox}" y1="{sy(v):.2f}" x2="{ox+width}" y2="{sy(v):.2f}" stroke="#e2e8f0"/>')
            parts.append(f'<text class="small" text-anchor="end" x="{ox-8}" y="{sy(v)+4:.2f}">{v:g}</text>')
        for label, points, color, dash in series:
            coordinates = ' '.join(f'{sx(x):.3f},{sy(y):.3f}' for x,y in points)
            parts.append(f'<polyline points="{coordinates}" stroke="{color}" stroke-width="2.6" fill="none" stroke-dasharray="{dash}"/>')
            for x,y in points:
                parts.append(f'<circle cx="{sx(x):.3f}" cy="{sy(y):.3f}" r="3.2" fill="{color}"/>')
        parts.append(f'<text class="axis" text-anchor="middle" x="{ox+width/2}" y="{oy+height+45}">{escape(xlabel)}</text>')
        parts.append(f'<text class="axis" transform="translate({px+13},{oy+height/2}) rotate(-90)" text-anchor="middle">{escape(ylabel)}</text>')
        for idx,(label, _, color, dash) in enumerate(series):
            lx=ox+(idx%3)*155
            ly=oy+height+70+(idx//3)*19
            parts.append(f'<line x1="{lx}" y1="{ly-4}" x2="{lx+18}" y2="{ly-4}" stroke="{color}" stroke-width="2.5" stroke-dasharray="{dash}"/>')
            parts.append(f'<text class="small" x="{lx+24}" y="{ly}">{escape(label)}</text>')

    main = [r for r in aggregates if r["alpha"]==config["main_alpha"] and r["interval_type"]=="shared_parameter_set"]
    series = [(m, [(r["budget"],r["decision_coverage"]) for r in main if r["method"]==m], colors[m], "") for m in config["methods"]]
    ticks=[(x,str(x)) for x in config["budgets"]]
    panel(35,95,"A. Decision coverage (alpha = 0.05)","Additional revealed observations","Fraction making a claim",series,0,32,0,1,ticks,[0,.25,.5,.75,1])
    series = [(m, [(r["budget"],r["mean_interval_width_nonempty"]) for r in main if r["method"]==m], colors[m], "") for m in config["methods"]]
    panel(625,95,"B. Shared-set interval width","Additional revealed observations","Mean width",series,0,32,0,2,ticks,[0,.5,1,1.5,2])
    risk = [r for r in aggregates if r["budget"]==8 and r["interval_type"]=="shared_parameter_set" and r["selective_risk"]!=""]
    series = [(m, sorted([(r["decision_coverage"],r["selective_risk"]) for r in risk if r["method"]==m]),colors[m], "") for m in config["methods"]]
    panel(35,500,"C. Risk vs coverage (budget = 8)","Fraction making a claim","Incorrect claims / all claims",series,0,1,0,.25,[(0,'0'),(.25,'.25'),(.5,'.5'),(.75,'.75'),(1,'1')],[0,.05,.1,.15,.2,.25])
    series = [(m,[(math.log2(r["n"]),r["mean_delta_width"]) for r in mechanisms if r["scenario"]==m], colors[m], "") for m in ("null","weak","balanced")]
    panel(625,500,"D. Null vs weak vs balanced excitation","Calibration sample count (log scale)","Mean contrast interval width",series,3,13,0,2,[(math.log2(n),str(n)) for n in config["mechanism_samples"]],[0,.5,1,1.5,2])
    parts.append('</svg>')
    path.write_text('\n'.join(parts), encoding="utf-8")


def main():
    started = time.perf_counter()
    raw_config = (ROOT / "config.json").read_bytes()
    config = json.loads(raw_config)
    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    rows, designs = run_evidence(config)
    aggregates = aggregate(rows)
    mechanisms, mechanism_summary = run_mechanism(config)
    write_csv(out / "evidence_trials.csv", rows)
    write_csv(out / "evidence_summary.csv", aggregates)
    write_csv(out / "mechanism_trials.csv", mechanisms)
    write_csv(out / "mechanism_summary.csv", mechanism_summary)
    make_figure(out / "pilot_figure.svg", aggregates, mechanism_summary, config)
    witness = {"theta_a": [.25,.65], "theta_b": [.65,.25],
               "calibration_input": S.tolist(),
               "mean_observation_both": float(S@np.array([.25,.65])),
               "delta_a": -.4, "delta_b": .4,
               "status": "Exact analytical witness fixed independently of stochastic trials; not a prevalence result."}
    summary = {
        "protocol": config["protocol_version"],
        "config_sha256": hashlib.sha256(raw_config).hexdigest(),
        "source_sha256": {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                          for name in ("model.py", "run_pilot.py", "test_model.py")},
        "environment": {"python": sys.version, "numpy": np.__version__, "platform": platform.platform()},
        "runtime_seconds": time.perf_counter()-started,
        "trials": config["trials"], "evidence_trial_rows": len(rows),
        "mechanism_trial_rows": len(mechanisms),
        "exact_ambiguity_witness": witness,
        "example_selection_orders": designs,
        "main_results": [r for r in aggregates if r["alpha"]==config["main_alpha"] and r["interval_type"]=="shared_parameter_set"],
        "scalar_wald_results": [r for r in aggregates if r["alpha"]==config["main_alpha"] and r["interval_type"]=="scalar_wald"],
        "mechanism_summary": mechanism_summary,
        "limitations": [
            "Synthetic correct linear model with known observation noise; not robot or real-world evidence.",
            "Classical D-opt and c-opt only; no novel identifiability utility is implemented.",
            "Coverage is marginal at each response-independent fixed-design budget; not across stopping times.",
            "Unconditional incorrect-claim probability is bounded by set miscoverage; selective risk is not bounded by alpha.",
            "Box is a known assumption, not a prior estimated from these observations.",
            "One prespecified policy pair; a scalar Wald interval may be more efficient than a shared parameter set.",
            "Finite-pool acquisition means revealing synthetic outcomes, not saving real robot data collection.",
            "Only 300 trials per condition; report uncertainty and do not claim uniform superiority."
        ]
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"runtime_seconds":summary["runtime_seconds"],"outputs":str(out),
                      "config_sha256":summary["config_sha256"],"trial_rows":len(rows)}, indent=2))


if __name__ == "__main__":
    main()
