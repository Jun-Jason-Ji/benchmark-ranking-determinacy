"""Configuration-level mechanism of the torque-limit effect: is it broad, or driven by a few scenes?

The headline shift in section 6.3 is a mean over the configuration grid, and a mean can be produced either by
a small uniform gain everywhere or by a handful of configurations flipping. This script separates the two on
the complete census: per-orientation means, the improve/unchanged/degrade counts over configurations, the
correlation between gain and nominal success, and how many outright failures are rescued.

The counts quoted in FINDING_estimand_matters.md 2d were computed on 48 of the 64 configurations; this script
exists so they can be refreshed from whatever the census now holds, and so the paper never quotes a
partial-census count again.

Sources follow the per-policy-family rule of make_core_table.py: OpenVLA's server never changed, so its
original directory is current generation and holds its complete census.

Usage: python scripts/analyze_torque_mechanism.py [--env ...] [--policy openvla-7b-4bit] [--out PATH]
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
sys.path.insert(0, str(ROOT / "scripts"))
from task_configs import config_id, is_deterministic, n_configs  # noqa: E402

OCTO_SETS = {"A'": "results/controller_sweep_gpu_replayA", "B": "results/controller_sweep_gpu_rep",
             "C": "results/controller_sweep_gpu_rep3", "D": "results/controller_sweep_gpu_rep4",
             "E": "results/controller_sweep_gpu_rep5"}
DET_SETS = dict(OCTO_SETS, **{"A'": "results/controller_sweep_gpu"})
ORIENT = [-45, 0, 45, 90, 135, 180, 225, 270]


def per_config(root, policy, env, cond):
    f = ROOT / root / policy / env / f"{cond}.jsonl"
    acc, seen = {}, set()
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                if r["episode_id"] in seen:
                    continue
                seen.add(r["episode_id"])
                acc.setdefault(config_id(env, r["episode_id"]), []).append(int(bool(r["success"])))
    return {c: float(np.mean(v)) for c, v in acc.items()}


def merged(policy, env, cond):
    """Mean success per configuration, pooled over the runs that cover it."""
    sets = DET_SETS if is_deterministic(policy) else OCTO_SETS
    acc = {}
    for root in sets.values():
        for c, v in per_config(root, policy, env, cond).items():
            acc.setdefault(c, []).append(v)
    return {c: float(np.mean(v)) for c, v in acc.items()}, {c: len(v) for c, v in acc.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default="PutEggplantInBasketScene-v1")
    ap.add_argument("--policy", default="openvla-7b-4bit")
    ap.add_argument("--control", default="octo-small", help="policy shown alongside as a negative control")
    ap.add_argument("--condition", default="force_x0.5")
    ap.add_argument("--out", default="results/controller_sweep_gpu_rep3/analysis_torque_mechanism.md")
    args = ap.parse_args()
    env, total = args.env, n_configs(args.env)
    L = [f"# Configuration-level mechanism of `{args.condition}`: {env}", "",
         f"The grid has **{total}** configurations. Per-configuration success is pooled over every run that "
         "covers it (sources chosen per policy family, as in `make_core_table.py`). A configuration counts as "
         "improved/degraded when the pooled rate moves by more than 0.01.", ""]
    for policy in [args.policy, args.control]:
        nom, nruns = merged(policy, env, "nominal")
        frc, fruns = merged(policy, env, args.condition)
        common = sorted(set(nom) & set(frc))
        if not common:
            L += [f"## {policy}", "", "no overlapping data", ""]
            continue
        gain = {c: frc[c] - nom[c] for c in common}
        up = sum(1 for c in common if gain[c] > 0.01)
        down = sum(1 for c in common if gain[c] < -0.01)
        same = len(common) - up - down
        a = float(np.mean([nom[c] for c in common]))
        b = float(np.mean([frc[c] for c in common]))
        zero = [c for c in common if nom[c] == 0.0]
        rescued = [c for c in zero if frc[c] > 0.0]
        r = float(np.corrcoef([nom[c] for c in common], [gain[c] for c in common])[0, 1]) if len(common) > 2 else float("nan")
        census = "**complete**" if len(common) == total else f"{len(common)}/{total} partial"
        L += [f"## {policy}", "",
              f"- configurations compared: {len(common)}/{total} ({census}); "
              f"runs per configuration: {min(nruns.get(c, 0) for c in common)}–{max(nruns.get(c, 0) for c in common)} nominal, "
              f"{min(fruns.get(c, 0) for c in common)}–{max(fruns.get(c, 0) for c in common)} {args.condition}",
              f"- benchmark value: {a:.3f} → {b:.3f} (**{b - a:+.3f}**)",
              f"- per configuration: **{up} improve / {same} unchanged / {down} degrade**",
              f"- correlation of gain with nominal success: **r = {r:+.2f}**",
              f"- configurations failing outright at nominal: {len(zero)}; of these **{len(rescued)} rescued**", ""]
        if len(ORIENT) and total % len(ORIENT) == 0:
            L += ["| orientation | " + " | ".join(f"{o}°" for o in ORIENT) + " |",
                  "|---|" + "---:|" * len(ORIENT)]
            for name, d in (("nominal", nom), (args.condition, frc), ("change", gain)):
                cells = []
                for q in range(len(ORIENT)):
                    ks = [c for c in common if c % len(ORIENT) == q]
                    cells.append("–" if not ks else f"{np.mean([d[c] for c in ks]):+.2f}" if name == "change"
                                 else f"{np.mean([d[c] for c in ks]):.2f}")
                L.append(f"| {name} | " + " | ".join(cells) + " |")
            L.append("")
            signs = [np.mean([gain[c] for c in common if c % len(ORIENT) == q]) for q in range(len(ORIENT))
                     if any(c % len(ORIENT) == q for c in common)]
            L += [f"Orientations with a positive mean change: **{sum(1 for v in signs if v > 0)}/{len(signs)}** "
                  f"(range {min(signs):+.2f} to {max(signs):+.2f}).", ""]
    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
