"""Experiment B (first instantiation): build the calibration-compatible controller set from the demo
replay residuals, propagate it to policy differences, and compare point-calibrated vs set-calibrated
ranking verdicts per task.

Compatible set (model-confidence-set style, one-sided, alpha=0.05): a replay condition c is compatible
if its per-demo total error is not significantly worse than the best (nominal) condition, i.e. the
paired bootstrap 95% lower bound of mean(err_c - err_nominal) <= 0. Conditions the free-space replay
cannot see at all (common stiffness/damping scale, force limit, object friction/density) are compatible
by construction and are flagged.

Sweep conditions are mapped to replay conditions by their (k/d ratio, delay). Verdict per policy pair:
  point  : sign of the nominal-condition CI
  set    : L = min over compatible conditions of CI lower, U = max of CI upper; decide if L>0 or U<0.
Two set variants: controller-only, and controller + contact (friction/density) parameters.

Usage: python scripts/analyze_compatible_set.py --out results/controller_sweep_gpu/analysis_compatible_set.md
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
REPLAY = ROOT / "results/replay_sysid"
SWEEP = ROOT / "results/controller_sweep_gpu"
ENVS = {"carrot": "PutCarrotOnPlateInScene-v1", "spoon": "PutSpoonOnTableClothInScene-v1", "eggplant": "PutEggplantInBasketScene-v1"}
# sweep condition -> (replay condition in grid, class)
MAP = {
    "nominal": ("s1_d1_delay0", "ctrl"),
    "stiff_x0.5": ("s0.5_d1_delay0", "ctrl"), "stiff_x2.0": ("s2_d1_delay0", "ctrl"),
    "damp_x0.5": ("s1_d0.5_delay0", "ctrl"), "damp_x2.0": ("s1_d2_delay0", "ctrl"),
    "delay_1": ("s1_d1_delay1", "ctrl"),
    "stiff_x0.25": (None, "ctrl_untested"), "stiff_x4.0": (None, "ctrl_untested"),
    "damp_x0.25": (None, "ctrl_untested"), "damp_x4.0": (None, "ctrl_untested"), "delay_2": (None, "ctrl_untested"),
    "iso_x0.25": ("s0.5_d0.5_delay0", "ctrl_invisible"), "iso_x0.5": ("s0.5_d0.5_delay0", "ctrl_invisible"),
    "iso_x2.0": ("s2_d2_delay0", "ctrl_invisible"), "iso_x4.0": ("s2_d2_delay0", "ctrl_invisible"),
    "force_x0.5": ("s1_d1_delay0", "ctrl_invisible"),
    "fric_x0.4": (None, "contact_invisible"), "fric_x2.5": (None, "contact_invisible"),
    "dens_x0.5": (None, "contact_invisible"), "dens_x2.0": (None, "contact_invisible"),
}


def boot(d, n=10000, seed=0):
    d = np.asarray(d, float)
    if len(d) == 0:
        return float("nan"), float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    m = d[rng.integers(0, len(d), size=(n, len(d)))].mean(axis=1)
    return float(d.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def replay_errors(cond):
    f = REPLAY / "grid" / f"{cond}.jsonl"
    return {json.loads(l)["episode_id"]: json.loads(l)["mean_total_err"] for l in f.read_text(encoding="utf-8").splitlines() if l.strip()}


def sweep_success(policy, env, cond):
    f = SWEEP / policy / env / f"{cond}.jsonl"
    if not f.exists():
        return {}
    return {json.loads(l)["episode_id"]: int(bool(json.loads(l)["success"])) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(SWEEP / "analysis_compatible_set.md"))
    ap.add_argument("--alpha", type=float, default=0.05)
    args = ap.parse_args()
    nom = replay_errors("s1_d1_delay0")
    L = ["# Compatible-set calibration vs point calibration (Experiment B, first instantiation)", "",
         "Replay residuals: 40 BridgeData V2 demos, ManiSkill3 free-space replay (results/replay_sysid/grid). "
         "Compatibility rule: paired bootstrap 95% lower bound of mean(err_c − err_nominal) ≤ 0 (not significantly worse than nominal). "
         "Sweep data: results/controller_sweep_gpu (all available episodes per condition; n shown).", "",
         "## Replay compatibility of sweep conditions", "", "| sweep condition | replay condition | class | mean Δerr vs nominal | 95% | compatible |", "|---|---|---|---:|---|---|"]
    compat = {}
    for sc, (rc, cls) in MAP.items():
        if cls in ("ctrl_invisible", "contact_invisible"):
            compat[sc] = True
            L.append(f"| {sc} | {rc or '—'} | {cls} | 0 (invisible) | — | yes (by construction) |")
            continue
        if rc is None:
            compat[sc] = False
            L.append(f"| {sc} | — | {cls} | untested | — | excluded (untested) |")
            continue
        e = replay_errors(rc)
        common = sorted(set(e) & set(nom))
        m, lo, hi = boot([e[i] - nom[i] for i in common])
        ok = lo <= 0
        compat[sc] = ok
        L.append(f"| {sc} | {rc} | {cls} | {m:+.4f} | [{lo:+.4f}, {hi:+.4f}] | {'yes' if ok else 'no'} |")
    L.append("")
    L += ["## Verdicts per task: point (nominal) vs compatible-set (controller-only) vs compatible-set (controller + contact)", "",
          "Δ = rate(octo-small) − rate(octo-base), paired by episode. Set verdict uses L = min CI-lower, U = max CI-upper over compatible conditions.", ""]
    summary = {}
    for name, env in ENVS.items():
        rows = []
        for sc in MAP:
            S, B = sweep_success("octo-small", env, sc), sweep_success("octo-base", env, sc)
            common = sorted(set(S) & set(B))
            if not common:
                continue
            m, lo, hi = boot([S[i] - B[i] for i in common])
            rows.append((sc, MAP[sc][1], compat[sc], len(common), m, lo, hi))
        L += [f"### {name}", "", "| condition | class | in set | n | Δ | 95% |", "|---|---|---|---:|---:|---|"]
        for sc, cls, ok, n, m, lo, hi in rows:
            L.append(f"| {sc} | {cls} | {'yes' if ok else 'no'} | {n} | {m:+.3f} | [{lo:+.2f}, {hi:+.2f}] |")

        def verdict(lo, hi):
            return "small better" if lo > 0 else ("base better" if hi < 0 else "abstain")

        nomrow = next((r for r in rows if r[0] == "nominal"), None)
        pv = verdict(nomrow[5], nomrow[6]) if nomrow else "n/a"
        ctrl = [r for r in rows if r[2] and r[1].startswith("ctrl")]
        both = [r for r in rows if r[2]]
        sv_c = verdict(min(r[5] for r in ctrl), max(r[6] for r in ctrl)) if ctrl else "n/a"
        sv_b = verdict(min(r[5] for r in both), max(r[6] for r in both)) if both else "n/a"
        L += ["", f"**{name}: point = {pv}; set (controller) = {sv_c}; set (controller + contact) = {sv_b}.**", ""]
        summary[name] = dict(point=pv, set_controller=sv_c, set_controller_contact=sv_b,
                             set_controller_bounds=[min(r[5] for r in ctrl), max(r[6] for r in ctrl)] if ctrl else None,
                             set_all_bounds=[min(r[5] for r in both), max(r[6] for r in both)] if both else None)
    L += ["## Summary", "", "| task | point verdict | set verdict (controller) | set verdict (controller + contact) |", "|---|---|---|---|"]
    for name, s in summary.items():
        L.append(f"| {name} | {s['point']} | {s['set_controller']} | {s['set_controller_contact']} |")
    L += ["", "Reading: where the set verdict abstains while the point verdict decides, the ranking conclusion depends on parameters the "
          "calibration data cannot constrain. Where both agree, the conclusion is robust to calibration ambiguity within the tested ranges."]
    text = "\n".join(L)
    Path(args.out).write_text(text, encoding="utf-8")
    (Path(args.out).with_suffix(".json")).write_text(json.dumps(dict(compatible=compat, summary=summary), indent=2), encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
