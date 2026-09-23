"""The paper's core table: point calibration vs the compatible-set verdict, on the configuration census.

For every task and policy pair it reports
  * the benchmark-value Δ under the nominal condition with its policy-noise interval (point calibration),
  * the union bound over the calibration-invisible conditions (the compatible-set verdict),
  * whether the two disagree -- the cases where point calibration declares a ranking the calibration data
    cannot support,
and, in the same row, the provenance a reader needs: configurations covered / total, independent runs per
policy, and the variance model (see docs/methods_census_2026-09-19.md §5).

Sources are chosen per policy family. Octo uses only the current inference-server generation (A', B, C): the
pre-fix directory drifts against a re-run of its own seeds
(results/controller_sweep_gpu_replayA/FINDING_platform_drift.md). OpenVLA has run on one unchanged Windows
server throughout, so all three directories are current for it. Pass --legacy-a to add the pre-fix Octo data.

Usage: python scripts/make_core_table.py
"""
import argparse
import itertools
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SETS_MS3 = {}
sys.path.insert(0, str(ROOT / "scripts"))
from task_configs import config_id, is_deterministic, n_configs  # noqa: E402

# The drift that disqualifies the pre-fix directory is specific to the WSL jax/XLA **Octo** server (the
# determinism flags were added between collections). The OpenVLA server is a separate Windows process on one
# unchanged build, so its episodes in results/controller_sweep_gpu -- including tonight's census -- are current
# generation. Sources are therefore chosen per policy family.
# D and E are T2-A (scripts/queue_t2a_seeds.py), which takes the eggplant census to S=5; empty until it runs.
SEED_SETS_OCTO = {"A'": "results/controller_sweep_gpu_replayA", "B": "results/controller_sweep_gpu_rep",
                  "C": "results/controller_sweep_gpu_rep3", "D": "results/controller_sweep_gpu_rep4",
                  "E": "results/controller_sweep_gpu_rep5"}
SEED_SETS_DET = {"A": "results/controller_sweep_gpu", "B": "results/controller_sweep_gpu_rep",
                 "C": "results/controller_sweep_gpu_rep3", "D": "results/controller_sweep_gpu_rep4",
                 "E": "results/controller_sweep_gpu_rep5"}
LEGACY_A = {"A (pre-fix)": "results/controller_sweep_gpu"}
MS2_SETS = {"ms2": "results/controller_sweep_ms2"}
FRACTAL_SETS = {"fractal": "results/fractal_reversal"}
INVISIBLE = ["iso_x0.25", "iso_x4.0", "force_x0.5", "fric_x0.4", "dens_x0.5"]
TASKS = [
    ("eggplant (ms3)", "PutEggplantInBasketScene-v1", None),
    ("spoon (ms3)", "PutSpoonOnTableClothInScene-v1", None),
    ("carrot (ms3)", "PutCarrotOnPlateInScene-v1", None),
    ("eggplant (ms2, original stack)", "PutEggplantInBasketScene-v0", MS2_SETS),
    ("spoon (ms2, original stack)", "PutSpoonOnTableClothInScene-v0", MS2_SETS),
    ("carrot (ms2, original stack)", "PutCarrotOnPlateInScene-v0", MS2_SETS),
    # The real-vs-sim reversal pair. Only force_x0.5 and fric_x0.4 were run here, so this row's union is over
    # a strictly smaller set than the bridge rows -- the footnote below reports each row's condition count so
    # the two are not read as equally strong. Real-robot comparison: analysis_fractal_reversal.md, §8.4.
    ("pick-coke-can (ms2, fractal)", "GraspSingleOpenedCokeCanInScene-v0", FRACTAL_SETS),
]
POLICIES = ["octo-small", "octo-base", "octo-small@hist1", "octo-base@hist1", "openvla-7b-4bit",
            "rt-1-converged", "rt-1-15pct"]


def per_config(root, policy, env, cond, raw=False):
    """Per-configuration outcomes from one directory.

    THE OBSERVATION UNIT. With raw=False each configuration returns the MEAN of that directory's
    episodes at it, so the unit entering the variance is the directory mean and S_c in
    Eq. (eq:var) is the number of directories. With raw=True the individual episode outcomes are
    returned, so the unit is the run and S_c is the number of runs at that configuration -- which is
    what the manuscript's formula actually says.

    The two differ because a directory can hold more than one episode per configuration: seed set B
    and the pre-fix build carry 96 episodes on a 64-configuration grid, so ids 64-95 wrap onto
    configurations 0-31 and give those two episodes, at different policy seeds (policy_seed =
    base + episode_id), from the same directory.

    They are not interchangeable and they change two verdicts (see --unit in main). Neither is
    wrong: the run unit is finer and matches the stated formula, since the episodes really are
    distinct seeds; the directory unit is conservative against any directory-level common effect,
    which the build-drift result shows can exist across generations though these five sets share a
    build. We report the run unit as primary because it is what Eq. (eq:var) defines, and the
    directory unit as a sensitivity -- not the other way round, and not chosen by which one
    declares.
    """
    f = ROOT / root / policy / env / f"{cond}.jsonl"
    acc, seen = {}, set()
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                e = r["episode_id"]
                if e in seen:
                    continue
                seen.add(e)
                acc.setdefault(config_id(env, e), []).append(int(bool(r["success"])))
    if raw:
        return acc
    return {c: float(np.mean(v)) for c, v in acc.items()}


def sets_for(sets, policy):
    """Deterministic policies may also draw on the pre-fix directory (see the note by SEED_SETS_DET)."""
    if is_deterministic(policy) and sets is SETS_MS3:
        return SEED_SETS_DET
    return sets


def runs_for(sets, policy, env, cond):
    """One dict per seed set; record-identical runs of a deterministic policy collapse to one observation."""
    out = []
    for root in sets_for(sets, policy).values():
        d = per_config(root, policy, env, cond)
        if d:
            out.append(d)
    if is_deterministic(policy):
        uniq = []
        for r in out:
            if not any(set(r) == set(u) and all(r[k] == u[k] for k in r) for u in uniq):
                uniq.append(r)
        return uniq
    return out


def raw_by_config(sets, policy, env, cond):
    """{configuration: [every raw episode outcome]} pooled over directories -- the run unit.

    De-duplication for policies labelled deterministic mirrors runs_for: collapse directories whose
    records are IDENTICAL, keep the ones that differ. An earlier version of this function returned
    the first non-empty directory outright and described that as matching runs_for. It does not, and
    the difference is not hypothetical -- OpenVLA's directories are not record-identical. On the
    eggplant census its nominal records differ from the first directory in 6 of 48 shared episodes,
    and under the halved torque limit in 3 and 5. Returning one directory discards that variation
    and sets the unobserved run-to-run term to zero, which understates the interval; it restored a
    third point/set disagreement at S=3 when corrected.

    The label `deterministic` describes the decoder (OpenVLA decodes greedily and ignores the policy
    seed), not the whole pipeline. Something else varies across these collections -- the plausible
    candidates are the inference-stack build and nondeterminism in the quantised kernels -- and
    since we cannot attribute it from the records, we keep the differing collections as
    observations rather than assert they are replicates of one number.
    """
    roots = list(sets_for(sets, policy).values())
    accs = [a for a in (per_config(r, policy, env, cond, raw=True) for r in roots) if a]
    if is_deterministic(policy):
        uniq = []
        for a in accs:
            if not any(set(a) == set(u) and all(a[k] == u[k] for k in a) for u in uniq):
                uniq.append(a)
        accs = uniq
    acc = {}
    for a in accs:
        for c, vals in a.items():
            acc.setdefault(c, []).extend(vals)
    return acc


UNIT = "run"   # "run" (Eq. (eq:var) as written) or "directory" (the earlier implementation)


def delta(sets, a, b, env, cond, unit=None):
    """Benchmark-value Delta with its policy-noise interval, Eq. (eq:var).

    `unit` selects the observation unit and defaults to the module-level UNIT. See per_config for
    what the two mean and why it matters: they disagree on two verdicts out of eighteen.
    """
    if (unit or UNIT) == "run":
        return _delta_run(sets, a, b, env, cond)
    return _delta_dir(sets, a, b, env, cond)


def _delta_run(sets, a, b, env, cond):
    """S_c = the number of runs at configuration c, pooling episodes across directories."""
    ra, rb = raw_by_config(sets, a, env, cond), raw_by_config(sets, b, env, cond)
    if not ra or not rb:
        return None
    cfgs = sorted(set(ra) & set(rb))
    if not cfgs:
        return None
    n = len(cfgs)
    ma = {k: float(np.mean(ra[k])) for k in cfgs}
    mb = {k: float(np.mean(rb[k])) for k in cfgs}

    def terms(acc, policy):
        out, known = {}, []
        for k in cfgs:
            v = float(np.var(acc[k], ddof=1)) if len(acc[k]) > 1 else None
            out[k] = (v, len(acc[k]))
            if v is not None:
                known.append(v)
        if known:
            fill, model = float(np.mean(known)), "empirical"
        elif is_deterministic(policy):
            fill, model = 0.0, "1 run (drift unmeasured)"
        else:
            rate = float(np.mean([float(np.mean(acc[k])) for k in cfgs]))
            fill, model = rate * (1 - rate), "binomial (1 run/config)"
        return {k: ((fill if v is None else v), s) for k, (v, s) in out.items()}, model

    ta, mda = terms(ra, a)
    tb, mdb = terms(rb, b)
    d = float(np.mean([ma[k] - mb[k] for k in cfgs]))
    se = float(np.sqrt(sum(ta[k][0] / ta[k][1] + tb[k][0] / tb[k][1] for k in cfgs) / n ** 2))
    return dict(delta=d, se=se, lo=d - 1.96 * se, hi=d + 1.96 * se, n=n,
                runs=(min(ta[k][1] for k in cfgs), min(tb[k][1] for k in cfgs)),
                runs_max=(max(ta[k][1] for k in cfgs), max(tb[k][1] for k in cfgs)),
                model=f"{mda} / {mdb}", unit="run")


def _delta_dir(sets, a, b, env, cond):
    ra, rb = runs_for(sets, a, env, cond), runs_for(sets, b, env, cond)
    if not ra or not rb:
        return None
    # Configurations are pooled as a union per policy, not intersected across runs: a run that covers fewer
    # configurations still contributes to the ones it has, and the variance term below already divides by the
    # per-configuration run count S_c. Intersecting would have thrown away the 16 configurations that only the
    # completed census covers.
    cfgs = sorted(set().union(*[set(r) for r in ra]) & set().union(*[set(r) for r in rb]))
    if not cfgs:
        return None

    def stats(runs, policy):
        mean, var, cnt = {}, {}, {}
        for k in cfgs:
            vals = [r[k] for r in runs if k in r]
            mean[k], cnt[k] = float(np.mean(vals)), len(vals)
            var[k] = float(np.var(vals, ddof=1)) if len(vals) > 1 else None
        known = [v for v in var.values() if v is not None]
        if known:
            fill, model = float(np.mean(known)), "empirical"
        elif is_deterministic(policy):
            fill, model = 0.0, "1 run (drift unmeasured)"
        else:
            rate = float(np.mean([mean[k] for k in cfgs]))
            fill, model = rate * (1 - rate), "binomial (1 run/config)"
        return mean, {k: (fill if v is None else v) for k, v in var.items()}, cnt, model

    ma, va, sa, mda = stats(ra, a)
    mb, vb, sb, mdb = stats(rb, b)
    n = len(cfgs)
    d = float(np.mean([ma[k] - mb[k] for k in cfgs]))
    se = float(np.sqrt(sum(va[k] / sa[k] + vb[k] / sb[k] for k in cfgs) / n ** 2))
    return dict(delta=d, se=se, lo=d - 1.96 * se, hi=d + 1.96 * se, n=n,
                runs=(len(ra), len(rb)), runs_max=(len(ra), len(rb)),
                model=f"{mda} / {mdb}", unit="directory")


def verdict(lo, hi, a, b):
    return f"{a}>" if lo > 0 else (f"{b}>" if hi < 0 else "abstain")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--legacy-a", action="store_true")
    ap.add_argument("--unit", default="run", choices=["run", "directory"],
                    help="observation unit for Eq. (eq:var). 'run' is what the formula states and "
                         "is the primary analysis; 'directory' was the earlier implementation and "
                         "is reported as a sensitivity. They disagree on two verdicts.")
    ap.add_argument("--out", default="results/CORE_TABLE.md")
    ap.add_argument("--max-sets", type=int, default=0,
                    help="keep only the first N seed-set directories. Sect. 7.2's claim is about "
                         "the EVALUATION BUDGET, so it has to be measurable at the budgets the "
                         "literature uses: --max-sets 3 is the reference protocol's, --max-sets 1 "
                         "a single seed. 0 means use every set collected.")
    args = ap.parse_args()
    global SETS_MS3, UNIT, SEED_SETS_OCTO, SEED_SETS_DET
    UNIT = args.unit
    if args.max_sets:
        SEED_SETS_OCTO = dict(list(SEED_SETS_OCTO.items())[:args.max_sets])
        SEED_SETS_DET = dict(list(SEED_SETS_DET.items())[:args.max_sets])
    SETS_MS3 = dict(SEED_SETS_OCTO)
    if args.legacy_a:
        SETS_MS3.update(LEGACY_A)
    sets_ms3 = SETS_MS3
    L = ["# 核心表：点校准 vs 相容集合判定（构型普查口径）", "",
         "每格的 Δ 为基准值估计量（全构型枚举后构型抽样误差为零，区间只含策略噪声与确定性策略的运行间噪声）。"
         "**点校准** = 仅标称条件；**并集界** = 结论须在全部校准不可见条件上同号，区间取 [min 下界, max 上界]。"
         "两者不一致的行，就是点校准宣布了校准数据无法支撑的排序。仅用当代服务器采集的数据"
         f"（Octo 用种子集 {', '.join(SEED_SETS_OCTO)}；OpenVLA 的服务器自始至终是同一套 Windows 进程，故其数据不受该问题影响，"
         f"沿用 {', '.join(SEED_SETS_DET)}{'；另含修复前的 Octo 数据' if args.legacy_a else ''}）。", "",
         "| 任务 | 策略对 | 构型 | 运行数 | 点校准 Δ [95%] | 判定 | 并集界 | 判定 | 不一致 | 方差模型 |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    disagree = 0
    used_conds = {}
    knife = []
    for label, env, override in TASKS:
        sets = override or sets_ms3
        total = n_configs(env)
        avail = [p for p in POLICIES if any((ROOT / r / p / env).exists() for r in sets.values())]
        for a, b in itertools.combinations(avail, 2):
            nom = delta(sets, a, b, env, "nominal")
            if not nom:
                continue
            got = [(c, delta(sets, a, b, env, c)) for c in INVISIBLE]
            inv = [r for _, r in got if r]
            if not inv:
                continue
            used_conds.setdefault(label, sorted({c for c, r in got if r}, key=INVISIBLE.index))
            # The union runs over nominal as well as the calibration-invisible conditions. The
            # compatible set contains the fitted nominal parameter by construction -- it is the loss
            # minimiser, so it is never rejected -- and a union bound that omitted it would not cover
            # the whole set. It widens no verdict here, but it is what makes the bound a bound.
            env_rs = inv + [nom]
            lo, hi = min(r["lo"] for r in env_rs), max(r["hi"] for r in env_rs)
            pv, uv = verdict(nom["lo"], nom["hi"], a, b), verdict(lo, hi, a, b)
            if pv != uv:
                disagree += 1
            # A declaration whose excluding bound rounds to +0.00 is a knife edge, and printing it
            # at two decimals shows a reader a bound of zero next to a declared ordering. Mark it
            # and report the bound at full precision, rather than let the rounding carry the claim.
            edge_u = uv != "abstain" and min(abs(lo), abs(hi)) < 0.01
            edge_p = pv != "abstain" and min(abs(nom["lo"]), abs(nom["hi"])) < 0.01
            if edge_p or edge_u:
                knife.append((label, f"{a} vs {b}", nom["lo"], nom["hi"], lo, hi, edge_p, edge_u))
            L.append(f"| {label} | {a} vs {b} | {nom['n']}/{total} | {nom['runs'][0]}/{nom['runs'][1]} | "
                     f"{nom['delta']:+.3f} [{nom['lo']:+.2f}, {nom['hi']:+.2f}] | "
                     f"{pv}{'†' if edge_p else ''} | [{lo:+.2f}, {hi:+.2f}] | "
                     f"{uv}{'†' if edge_u else ''} | "
                     f"{'**是**' if pv != uv else '否'} | {nom['model']} |")
    L += ["", f"不一致的策略对共 **{disagree}** 个。", ""]
    if knife:
        L += ["† 打了此标记的判定落在刀口上：把它排除出 0 的那一端界限绝对值小于 0.01，"
              "四舍五入到两位小数即为 0。**这种“宣布”与拒判之间只差数值噪声，不应与稳健的宣布同等看待。**", ""]
        for lab, pair, plo, phi, lo, hi, ep, eu in knife:
            L.append(f"- {lab}，{pair}：点校准 [{plo:+.6f}, {phi:+.6f}]{'（刀口）' if ep else ''}；"
                     f"并集界 [{lo:+.6f}, {hi:+.6f}]{'（刀口）' if eu else ''}")
        L += [""]
    L += [
          "**并集所覆盖的条件数按任务不同，不可横向当作同等强度**（条件越少，并集界越接近点校准）：", ""]
    for label in (t[0] for t in TASKS):
        if label in used_conds:
            cs = used_conds[label]
            L.append(f"- {label}：{len(cs)} 个条件 — {', '.join('`' + c + '`' for c in cs)}")
    L += ["",
          "`pick-coke-can (ms2, fractal)` 一行是真机-仿真反转对：该对的公布真机排序与仿真相反"
          "（真机 0.853 vs 0.920，仿真 0.857 vs 0.710），因此它检验的是"
          "**判据会不会在仿真出错的对上拒判**。结论见 `results/fractal_reversal/analysis_fractal_reversal.md`"
          "与论文 §8.4：不会——并集界在该对上宣布了真机反对的排序。", "",
          f"**观察单位：`{UNIT}`。** Eq. (eq:var) 的 S_c 写的是「构型 c 上的运行次数」，即 `run` 口径；"
          "早期实现先在目录内对同构型的多集取平均，再把目录均值作为观察值（`directory` 口径）。"
          "两者在 18 对中有 2 对判决不同：MS3 eggplant small−base（`directory` 下界 +0.000042 宣布，"
          "`run` 下为 [−0.0079, +0.1173] 拒判）与 MS2 spoon small−base（`directory` 拒判，`run` 宣布）。"
          "**point/set 不一致的总数在两种口径下都是 1。** 主分析用 `run`，因为公式如此定义、且同一目录内不同 "
          "episode 用的是不同策略种子；`directory` 更保守（防目录级共同效应），以 `--unit directory` 复现，"
          "作为敏感性报告。口径不是按哪种更容易得到宣布来选的。", "",
          "口径与限制见 `docs/methods_census_2026-09-19.md`；形式化账本见 `docs/theory_protocol.md §6.1`；"
          "数据来源与风险分级见 `results/PROVENANCE_AUDIT_2026-09-19.md`。", ""]
    text = "\n".join(L)
    (ROOT / args.out).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
