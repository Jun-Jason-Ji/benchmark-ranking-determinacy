"""Reanalyse frozen public SIMPLER summaries, without inventing trial records.

Standard-library implementation. No simulator or policy code is executed.
The output is descriptive plus explicitly conditional counts-only sensitivity.
Run this file from any directory; all inputs/outputs are next to the script.
"""
from __future__ import annotations

import ast
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
from statistics import NormalDist

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "sources"
COMMIT = "06accaca93535902d408da4855f21cece12bceb7"
ALPHA = 0.05


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def literal_assignment(tree, name, function=None):
    nodes = tree.body
    if function:
        nodes = next(n.body for n in nodes if isinstance(n, ast.FunctionDef) and n.name == function)
    for n in nodes:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets):
            return ast.literal_eval(n.value)
    raise KeyError((name, function))


def pearson(x, y, source_epsilon=False):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    dx, dy = [v - mx for v in x], [v - my for v in y]
    denom = math.sqrt(sum(v * v for v in dx) * sum(v * v for v in dy))
    if source_epsilon:
        if dx == dy:
            return 1.0
        return sum(a * b for a, b in zip(dx, dy)) / (denom + 1e-8)
    if denom == 0:
        return None
    return sum(a * b for a, b in zip(dx, dy)) / denom


def mmrv(sim, real):
    return sum(max([0.0] + [abs(real[i] - real[j]) for j in range(len(sim))
                           if (sim[i] > sim[j]) != (real[i] > real[j])])
               for i in range(len(sim))) / len(sim)


def sign(x):
    return 0 if abs(x) < 1e-12 else (1 if x > 0 else -1)


def wilson(k, n, alpha=ALPHA):
    p = k / n
    z = NormalDist().inv_cdf(1 - alpha / 2)
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0., centre - half), min(1., centre + half)


def newcombe(k1, n1, k2, n2, alpha=ALPHA):
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1, alpha)
    l2, u2 = wilson(k2, n2, alpha)
    return (p1 - p2 - math.hypot(p1 - l1, u2 - p2),
            p1 - p2 + math.hypot(u1 - p1, p2 - l2))


def binom_cdf(k, n, p):
    return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k + 1))


def solve_cdf(k, n, target):
    low, high = 0., 1.
    for _ in range(90):
        mid = (low + high) / 2
        if binom_cdf(k, n, mid) > target:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def clopper_pearson(k, n, alpha=ALPHA):
    return (0. if k == 0 else solve_cdf(k - 1, n, 1 - alpha / 2),
            1. if k == n else solve_cdf(k, n, alpha / 2))


def exact_mcnemar_p(n10, n01):
    total = n10 + n01
    if total == 0:
        return 1.
    return min(1., 2 * binom_cdf(min(n10, n01), total, .5))


def pair_status(real, sim, policies):
    pairs = []
    for a, b in itertools.combinations(policies, 2):
        dr, ds = real[a] - real[b], sim[a] - sim[b]
        status = "tied_in_at_least_one_domain" if not sign(dr) or not sign(ds) else (
            "opposite_mean_directions" if sign(dr) != sign(ds) else "same_mean_direction")
        pairs.append(dict(policy_a=a, policy_b=b, real_difference=dr,
                          sim_difference=ds, status=status))
    return pairs


def write_csv(name, rows):
    with (ROOT / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    tree = ast.parse((SOURCES / "metrics.py").read_text(encoding="utf-8"))
    eval_tree = ast.parse((SOURCES / "calc_metrics_evaluation_videos.py").read_text(encoding="utf-8"))
    real = literal_assignment(tree, "REAL_PERF")
    sim = literal_assignment(tree, "SIMPLER_PERF")
    coke_strata = literal_assignment(eval_tree, "coke_can_real_success", "calc_pick_coke_can_stats")
    n_orientation = literal_assignment(eval_tree, "n_trials_per_ckpt_per_orientation", "calc_pick_coke_can_stats")
    budgets = {
        "google_robot_pick_coke_can": n_orientation * len(coke_strata),
        "google_robot_move_near": literal_assignment(eval_tree, "n_trials_per_ckpt", "calc_move_near_stats"),
        "google_robot_open_drawer": literal_assignment(eval_tree, "n_trials_per_ckpt_per_task", "calc_drawer_stats"),
        "google_robot_close_drawer": literal_assignment(eval_tree, "n_trials_per_ckpt_per_task", "calc_drawer_stats"),
        "google_robot_place_apple_in_closed_top_drawer": literal_assignment(eval_tree, "n_trials_per_ckpt_per_task", "calc_long_horizon_apple_in_drawer_stats"),
    }
    # Name varies across commits; identify the function by its literal real-success table.
    bridge_function = next(n.name for n in eval_tree.body if isinstance(n, ast.FunctionDef)
                           and any(isinstance(x, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "real_success_dict"
                                                                 for t in x.targets) for x in n.body))
    bridge_n = literal_assignment(eval_tree, "n_trials_per_ckpt", bridge_function)
    for task in real:
        if task.startswith("widowx_"):
            budgets[task] = bridge_n

    cells, counts = [], {}
    for task in real:
        assert set(real[task]) == set(sim[task])
        n = budgets[task]
        counts[task] = {}
        for policy, p in real[task].items():
            candidates = [k for k in range(n + 1) if abs(k / n - p) <= .0005000001]
            k = candidates[0] if len(candidates) == 1 else None
            counts[task][policy] = k
            cells.append(dict(task=task, policy=policy, published_real_rate=p,
                              published_sim_rate=sim[task][policy], public_budget=n,
                              compatible_success_count=k, integer_count_status="unique_rounding_compatible" if k is not None else "not_compatible_do_not_round",
                              interval_status="conditional_on_budget_cohort_and_sampling_model" if k is not None else "excluded"))

    correlation, all_pair_rows, deletion_rows = [], [], []
    for scope in ("all_published_policies", "public_checkpoint_subset"):
        for task in real:
            policies = [p for p in real[task] if scope == "all_published_policies" or p != "rt-2-x"]
            r, s = [real[task][p] for p in policies], [sim[task][p] for p in policies]
            pairs = pair_status(real[task], sim[task], policies)
            lopo = []
            for omitted in policies:
                retained = [p for p in policies if p != omitted]
                rr, ss = [real[task][p] for p in retained], [sim[task][p] for p in retained]
                item = dict(scope=scope, task=task, omitted_policy=omitted, n_retained=len(retained),
                            pearson=pearson(ss, rr), mmrv=mmrv(ss, rr),
                            interpretation="two_points_or_constant_not_inferential" if len(retained) <= 2 else "deterministic_deletion_sensitivity")
                lopo.append(item)
                deletion_rows.append(item)
            valid_lopo = [v["pearson"] for v in lopo if v["pearson"] is not None]
            correlation.append(dict(scope=scope, task=task, n_policies=len(policies), pearson=pearson(s, r),
                                    source_pearson=pearson(s, r, True), mmrv=mmrv(s, r), n_pairs=len(pairs),
                                    opposite_pairs=sum(p["status"] == "opposite_mean_directions" for p in pairs),
                                    tied_pairs=sum(p["status"] == "tied_in_at_least_one_domain" for p in pairs),
                                    deletion_r_min=min(valid_lopo) if valid_lopo else None,
                                    deletion_r_max=max(valid_lopo) if valid_lopo else None,
                                    deletion_r_undefined=sum(v["pearson"] is None for v in lopo)))
            for pair in pairs:
                all_pair_rows.append(dict(scope=scope, task=task, **pair))

    # Counts-only sensitivity: no reconstructed trial arrays, no pseudo-pairing.
    pair_intervals = []
    for task in real:
        compatible = [p for p in real[task] if counts[task][p] is not None]
        # Per-task simultaneous marginal intervals imply simultaneous pair-difference bounds.
        # Bonferroni does not require independence BETWEEN policies.
        task_cp = {p: clopper_pearson(counts[task][p], budgets[task], ALPHA / len(compatible)) for p in compatible}
        for a, b in itertools.combinations(compatible, 2):
            ka, kb, n = counts[task][a], counts[task][b], budgets[task]
            lo, hi = newcombe(ka, n, kb, n)
            simultaneous = (task_cp[a][0] - task_cp[b][1], task_cp[a][1] - task_cp[b][0])
            pair_intervals.append(dict(task=task, policy_a=a, policy_b=b, count_a=ka, count_b=kb, n_each=n,
                                       difference=(ka-kb)/n, newcombe_low=lo, newcombe_high=hi,
                                       simultaneous_cp_low=simultaneous[0], simultaneous_cp_high=simultaneous[1],
                                       publicly_rerunnable_pair=(a != "rt-2-x" and b != "rt-2-x"),
                                       opposite_published_means=sign(real[task][a]-real[task][b])*sign(sim[task][a]-sim[task][b]) == -1))

    # Six marginal binomial intervals: 2 policies x 3 orientations, alpha/6 each.
    # Equal stratum weights. Cross-policy/stratum independence is unnecessary for the union bound;
    # the binomial model within EACH policy/orientation cell is still required.
    a, b = "rt-1-converged", "rt-1-15pct"
    strata_rows, strat_low, strat_high, d10_ranges = [], 0., 0., []
    for orientation, rates in coke_strata.items():
        ka, kb = round(rates[a] * n_orientation), round(rates[b] * n_orientation)
        assert abs(ka / n_orientation - rates[a]) < 1e-12
        assert abs(kb / n_orientation - rates[b]) < 1e-12
        ia = clopper_pearson(ka, n_orientation, ALPHA / 6)
        ib = clopper_pearson(kb, n_orientation, ALPHA / 6)
        strat_low += (ia[0] - ib[1]) / 3
        strat_high += (ia[1] - ib[0]) / 3
        # Hypothetical one-to-one pairing on 25 common trials, not an observed design.
        possibilities = []
        for both in range(max(0, ka + kb - n_orientation), min(ka, kb) + 1):
            possibilities.append((ka-both, kb-both))
        d10_ranges.append(possibilities)
        strata_rows.append(dict(orientation=orientation, count_converged=ka, count_15pct=kb,
                                n_each=n_orientation, difference=(ka-kb)/n_orientation))
    paired_possibilities = []
    for combo in itertools.product(*d10_ranges):
        n10, n01 = sum(v[0] for v in combo), sum(v[1] for v in combo)
        row = dict(converged_only=n10, checkpoint15_only=n01, exact_two_sided_p=exact_mcnemar_p(n10,n01))
        if row not in paired_possibilities:
            paired_possibilities.append(row)
    # Independent, non-identically distributed Bernoulli trials within each policy are enough
    # for this conservative finite-planned-evaluation-average bound. Cross-policy dependence allowed.
    # Two one-policy two-sided Hoeffding bounds (alpha/2 each), then a union bound.
    hoeffding_half = 2 * math.sqrt(math.log(4 / ALPHA) / (2 * 75))
    coke = dict(orientation_counts=strata_rows, aggregate_counts=[64,69], n_each=75,
                difference=-5/75, independent_iid_newcombe95=newcombe(64,75,69,75),
                orientation_stratified_bonferroni_cp95=[strat_low,strat_high],
                independent_trials_nonidentical_hoeffding95=[max(-1.,-5/75-hoeffding_half),min(1.,-5/75+hoeffding_half)],
                hypothetical_paired_tables=paired_possibilities,
                hypothetical_exact_mcnemar_p_range=[min(r["exact_two_sided_p"] for r in paired_possibilities),max(r["exact_two_sided_p"] for r in paired_possibilities)],
                limitations="Actual trial pairing, batch dependence, exclusions and cohort mapping remain unverified. These are sensitivity models, not design-validated intervals or a held-out test.")

    tests = []
    def check(name, condition):
        assert condition, name
        tests.append(dict(name=name, passed=True))
    check("source tables contain 42 matched cells", len(cells) == 42)
    check("41 cells have unique counts; eggplant-small excluded", sum(x["compatible_success_count"] is not None for x in cells) == 41 and counts["widowx_put_eggplant_in_basket"]["octo-small"] is None)
    public_pairs = [p for p in all_pair_rows if p["scope"] == "public_checkpoint_subset"]
    check("existing 62 pairs / 5 opposite / 3 tied reproduced", len(public_pairs) == 62 and sum(p["status"] == "opposite_mean_directions" for p in public_pairs) == 5 and sum(p["status"] == "tied_in_at_least_one_domain" for p in public_pairs) == 3)
    check("coke stratum counts reproduce table to published rounding", all(abs(sum(coke_strata[s][p] for s in coke_strata)/3-real["google_robot_pick_coke_can"][p]) <= .00050001 for p in real["google_robot_pick_coke_can"]))
    check("Newcombe previously crosschecked reference example", abs(coke["independent_iid_newcombe95"][0] + .172863) < 1e-6 and abs(coke["independent_iid_newcombe95"][1]-.037981) < 1e-6)
    check("CP zero and all-success exact boundary cases", abs(clopper_pearson(0,24)[1]-(1-(.025)**(1/24))) < 1e-12 and abs(clopper_pearson(24,24)[0]-(.025)**(1/24)) < 1e-12)
    check("pair-difference CI antisymmetry", all(abs(newcombe(p["count_b"],p["n_each"],p["count_a"],p["n_each"])[0]+p["newcombe_high"])<1e-12 for p in pair_intervals))
    check("stratified conservative interval contains pooled point", strat_low < -5/75 < strat_high)
    check("every compatible coke pairing is unresolved at 5 percent", min(x["exact_two_sided_p"] for x in paired_possibilities) > .05)
    check("constant correlation explicitly undefined", pearson([0,0],[0,0]) is None)
    check("MMRV zero for identical strict ordering", mmrv([0,.2,.9],[.1,.3,.8]) == 0)

    output = dict(schema_version=1, source_commit=COMMIT, alpha=ALPHA,
                  interpretation="Descriptive aggregates and conditional sampling-model sensitivity, not new hardware data and not a held-out validation.",
                  sources=[dict(file=f.name, sha256=sha(f)) for f in sorted(SOURCES.iterdir()) if f.is_file()],
                  cells=cells, correlations=correlation, policy_deletions=deletion_rows,
                  published_pairs=all_pair_rows, count_pair_intervals=pair_intervals,
                  coke_sensitivity=coke, verification=tests)
    (ROOT / "analysis.json").write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    write_csv("public_cells.csv",cells)
    write_csv("task_correlations.csv",correlation)
    write_csv("policy_deletion_sensitivity.csv",deletion_rows)
    write_csv("count_pair_intervals.csv",pair_intervals)
    print(json.dumps(dict(cells=len(cells),counts_compatible=41,tests=len(tests),coke=coke,correlations=correlation),indent=2))


if __name__ == "__main__":
    main()
