"""After REPLICATION_DONE: bring the mid-success near-tied policy set {octo-small, octo-base,
octo-small@hist1, octo-base@hist1} to 96 episodes on eggplant for all variants_v1 conditions, then
re-run the near-tied pair analysis."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import run_phase, PY, OUT, log  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
ENV = "PutEggplantInBasketScene-v1"


def main():
    while "REPLICATION_DONE" not in (LOGS / "queue_replication.out").read_text(encoding="utf-8", errors="replace"):
        time.sleep(120)
    # fine-grained jobs (one condition each) so the two servers per policy stay balanced
    conds = ["nominal", "iso_x0.25", "iso_x4.0", "force_x0.5", "fric_x0.4", "dens_x0.5"]
    jobs = [dict(policy=f"{m}@hist1", env=ENV, preset="variants_v1", conds=c, offset=24, episodes=72) for m in ("octo-small", "octo-base") for c in conds]
    jobs += [dict(policy=m, env=ENV, preset="variants_v1", conds=c, offset=48, episodes=48) for m in ("octo-small", "octo-base") for c in ("iso_x0.25", "iso_x4.0", "force_x0.5")]
    run_phase("eggplant_neartied_96", jobs)
    for dd in ("first", "last"):
        suffix = "" if dd == "first" else "_dedupe_last"
        r = subprocess.run([str(PY), "scripts/analyze_variant_pairs.py", "--root", OUT, "--n", "96", "--dedupe", dd,
                            "--out", f"{OUT}/analysis_variant_pairs_eggplant96{suffix}.md"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        log(f"analysis ({dd}) rc={r.returncode}")
    log("HIST1_96_DONE")


if __name__ == "__main__":
    main()
