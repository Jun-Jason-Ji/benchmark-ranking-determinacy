"""After HIST1_96_DONE: bring the spoon-task pair octo-small vs octo-small@hist1 to 96 episodes on all
variants_v1 conditions (the pair shows a point-estimate sign change: nominal +0.125, friction 0.2 −0.21,
iso x0.25 −0.08 at 24 episodes), then analyze the pair."""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import run_phase, PY, OUT, log  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
ENV = "PutSpoonOnTableClothInScene-v1"


def main():
    while "HIST1_96_DONE" not in (LOGS / "queue_hist1_96.out").read_text(encoding="utf-8", errors="replace"):
        time.sleep(120)
    conds = ["nominal", "iso_x0.25", "iso_x4.0", "force_x0.5", "fric_x0.4", "dens_x0.5"]
    jobs = [dict(policy="octo-small@hist1", env=ENV, preset="variants_v1", conds=c, offset=24, episodes=72) for c in conds]
    jobs += [dict(policy="octo-small", env=ENV, preset="variants_v1", conds=c, offset=48, episodes=48) for c in ("nominal", "iso_x0.25", "iso_x4.0", "force_x0.5")]
    jobs += [dict(policy="octo-small", env=ENV, preset="variants_v1", conds=c, offset=24, episodes=72) for c in ("fric_x0.4", "dens_x0.5")]
    run_phase("spoon_hist1_96", jobs)
    # pair analysis
    import numpy as np
    rng = np.random.default_rng(0)

    def load(p, c):
        f = ROOT / OUT / p / ENV / f"{c}.jsonl"
        d = {}
        for l in f.read_text(encoding="utf-8").splitlines():
            if l.strip():
                r = json.loads(l)
                d.setdefault(r["episode_id"], int(bool(r["success"])))  # first record wins on duplicates
        return d

    def boot(d):
        d = np.asarray(d, float); m = d[rng.integers(0, len(d), size=(20000, len(d)))].mean(1)
        return d.mean(), np.percentile(m, 2.5), np.percentile(m, 97.5)

    lines = ["# Spoon: octo-small vs octo-small@hist1 at 96 episodes", "", "| condition | n | small | small@hist1 | Δ | 95% |", "|---|---:|---:|---:|---:|---|"]
    res = {}
    for c in ["nominal", "iso_x0.25", "iso_x4.0", "force_x0.5", "fric_x0.4", "dens_x0.5"]:
        A, B = load("octo-small", c), load("octo-small@hist1", c); e = sorted(set(A) & set(B))
        m, lo, hi = boot([A[i] - B[i] for i in e]); res[c] = (m, lo, hi)
        lines.append(f"| {c} | {len(e)} | {sum(A[i] for i in e)} | {sum(B[i] for i in e)} | {m:+.3f} | [{lo:+.2f}, {hi:+.2f}] |")
    A0, B0, A1, B1 = load("octo-small", "nominal"), load("octo-small@hist1", "nominal"), load("octo-small", "fric_x0.4"), load("octo-small@hist1", "fric_x0.4")
    e = sorted(set(A0) & set(B0) & set(A1) & set(B1)); m, lo, hi = boot([(A1[i] - B1[i]) - (A0[i] - B0[i]) for i in e])
    lines += ["", f"Δ(fric_x0.4) − Δ(nominal) = {m:+.3f} [{lo:+.2f}, {hi:+.2f}] (n={len(e)})"]
    (ROOT / OUT / "analysis_spoon_hist1_96.md").write_text("\n".join(lines), encoding="utf-8")
    log("SPOON_HIST1_96_DONE")


if __name__ == "__main__":
    main()
