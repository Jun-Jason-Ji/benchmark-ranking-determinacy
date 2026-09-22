"""Queue the contact_v1 sweep (object friction x0.4/x2.5, density x0.5/x2.0) on carrot, spoon, eggplant
for both policies, then run the pairwise and equivalent-pairs analyses. Reuses queue_v2's scheduler."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import run_phase, SERVERS, PY, OUT, log  # noqa: E402

ENVS = ["PutEggplantInBasketScene-v1", "PutSpoonOnTableClothInScene-v1", "PutCarrotOnPlateInScene-v1"]


def main():
    jobs = [dict(policy=p, env=e, preset="contact_v1", conds=None, offset=0, episodes=24) for e in ENVS for p in SERVERS]
    run_phase("contact_v1_24", jobs)
    for script, out in [("scripts/analyze_controller_sweep.py", f"{OUT}/analysis_contact.md"),
                        ("scripts/analyze_equiv_pairs.py", f"{OUT}/analysis_equiv_pairs_contact.md")]:
        r = subprocess.run([str(PY), script, "--root", OUT, "--out", out], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        log(f"analysis {script} rc={r.returncode}")
    log("CONTACT_QUEUE_DONE")


if __name__ == "__main__":
    main()
