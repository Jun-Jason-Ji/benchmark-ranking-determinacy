"""Cross-stack comparison: original SIMPLER main (ManiSkill2 + SAPIEN 2, results/controller_sweep_ms2, env ids *-v0)
vs the ManiSkill3/Windows platform (results/controller_sweep_gpu, env ids *-v1), same policies, same episode_ids,
same policy seeds, same calibration-invisible conditions (variants_v1).

Per task and condition: success rates of both policies on both stacks, Δ = small − base with paired bootstrap 95% CI
on each stack, and the point / union-bound verdicts per stack. Also the per-episode agreement between stacks.
Usage: python scripts/analyze_cross_stack.py [--n 48] [--tasks eggplant,spoon,carrot]"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from task_configs import GRIDS  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
ROOT = Path(__file__).resolve().parents[1]
MS2 = ROOT / "results/controller_sweep_ms2"
MS3 = ROOT / "results/controller_sweep_gpu"
TASKS = {"eggplant": ("PutEggplantInBasketScene-v0", "PutEggplantInBasketScene-v1"),
         "spoon": ("PutSpoonOnTableClothInScene-v0", "PutSpoonOnTableClothInScene-v1"),
         "carrot": ("PutCarrotOnPlateInScene-v0", "PutCarrotOnPlateInScene-v1")}
CONDS = ["nominal", "iso_x0.25", "iso_x4.0", "force_x0.5", "fric_x0.4", "dens_x0.5"]
POL = ("octo-small", "octo-base")
RNG = np.random.default_rng(0)


def load(root, policy, env, cond, n):
    f = root / policy / env / f"{cond}.jsonl"
    d = {}
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                if r["episode_id"] < n:
                    d.setdefault(r["episode_id"], int(bool(r["success"])))
    return d


def boot(x, nb=10000):
    x = np.asarray(x, float)
    if len(x) == 0:
        return float("nan"), float("nan"), float("nan")
    m = x[RNG.integers(0, len(x), size=(nb, len(x)))].mean(1)
    return float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def verdict(lo, hi):
    return "small" if lo > 0 else ("base" if hi < 0 else "abstain")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=48)
    ap.add_argument("--tasks", default="eggplant,spoon,carrot")
    ap.add_argument("--out", default=str(MS2 / "analysis_cross_stack.md"))
    args = ap.parse_args()
    L = [f"# Cross-stack comparison: original SIMPLER main (ms2/SAPIEN2, WSL CPU render) vs ManiSkill3/Windows, episodes 0-{args.n - 1}", "",
         "Same policies (Octo-small / Octo-base via the same HTTP servers), same episode_ids and policy seeds, variants_v1 conditions. "
         "Δ = small − base, paired bootstrap 95%. Union bound = min/max of per-condition CI over the 5 calibration-invisible conditions.", "",
         "**Config grids.** An episode_id means the same initial state on both stacks only when the two envs share the configuration grid. "
         "Spoon and carrot do (12 positions x 2 orientations); **eggplant does not** (ManiSkill3 8 x 8 vs original 8 x 3, different quaternions), "
         "so per-episode agreement is not computed there and the rates compare different initial-pose distributions. "
         "See results/controller_sweep_gpu_rep3/FINDING_seed_set_bug.md.", ""]
    for task in args.tasks.split(","):
        e2, e3 = TASKS[task]
        rows, present = [], False
        for c in CONDS:
            s2, b2 = load(MS2, POL[0], e2, c, args.n), load(MS2, POL[1], e2, c, args.n)
            s3, b3 = load(MS3, POL[0], e3, c, args.n), load(MS3, POL[1], e3, c, args.n)
            i2, i3 = sorted(set(s2) & set(b2)), sorted(set(s3) & set(b3))
            if not i2 or not i3:
                rows.append((c, None)); continue
            present = True
            d2 = boot([s2[i] - b2[i] for i in i2]); d3 = boot([s3[i] - b3[i] for i in i3])
            grid_match = GRIDS.get(e2) == GRIDS.get(e3)
            common = sorted(set(i2) & set(i3)) if grid_match else []
            agree_s = np.mean([s2[i] == s3[i] for i in common]) if common else float("nan")
            agree_b = np.mean([b2[i] == b3[i] for i in common]) if common else float("nan")
            rows.append((c, dict(n2=len(i2), n3=len(i3), rs2=np.mean(list(s2.values())), rb2=np.mean(list(b2.values())), rs3=np.mean(list(s3.values())), rb3=np.mean(list(b3.values())),
                                 d2=d2, d3=d3, agree_s=agree_s, agree_b=agree_b)))
        if not present:
            continue
        L += [f"## {task}", "", "| condition | n (ms2/ms3) | small ms2 / ms3 | base ms2 / ms3 | Δ ms2 [95%] | Δ ms3 [95%] | verdict ms2 / ms3 | per-episode agreement small / base |",
              "|---|---:|---|---|---|---|---|---|"]
        lo2, hi2, lo3, hi3 = [], [], [], []
        for c, r in rows:
            if r is None:
                L.append(f"| {c} | incomplete | | | | | | |"); continue
            m2, l2, h2 = r["d2"]; m3, l3, h3 = r["d3"]
            if c != "nominal":
                lo2.append(l2); hi2.append(h2); lo3.append(l3); hi3.append(h3)
            agree = "n/a (grids differ)" if np.isnan(r["agree_s"]) else f"{r['agree_s']:.2f} / {r['agree_b']:.2f}"
            L.append(f"| {c} | {r['n2']}/{r['n3']} | {r['rs2']:.3f} / {r['rs3']:.3f} | {r['rb2']:.3f} / {r['rb3']:.3f} | {m2:+.3f} [{l2:+.2f}, {h2:+.2f}] | {m3:+.3f} [{l3:+.2f}, {h3:+.2f}] | {verdict(l2, h2)} / {verdict(l3, h3)} | {agree} |")
        nom = dict(rows).get("nominal")
        if nom and lo2:
            L += ["", f"Point calibration (nominal): ms2 **{verdict(nom['d2'][1], nom['d2'][2])}**, ms3 **{verdict(nom['d3'][1], nom['d3'][2])}**. "
                  f"Union bound over the invisible conditions: ms2 [{min(lo2):+.2f}, {max(hi2):+.2f}] → **{verdict(min(lo2), max(hi2))}**; ms3 [{min(lo3):+.2f}, {max(hi3):+.2f}] → **{verdict(min(lo3), max(hi3))}**.", ""]
    text = "\n".join(L)
    Path(args.out).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
