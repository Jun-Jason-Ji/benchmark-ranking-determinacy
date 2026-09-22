"""After CONTACT_QUEUE_DONE: extend eggplant nominal / fric_x0.4 / dens_x0.5 to 96 episodes for both
policies (the low-friction condition lifted octo-base from 6/24 to 11/24 while octo-small stayed at 12/24),
then re-run the equivalent-pairs analysis for eggplant."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import run_phase, SERVERS, PY, OUT, log  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
ENV = "PutEggplantInBasketScene-v1"


def main():
    while "CONTACT_QUEUE_DONE" not in (LOGS / "queue_contact.out").read_text(encoding="utf-8", errors="replace"):
        log("waiting for CONTACT_QUEUE_DONE")
        time.sleep(120)
    jobs = [dict(policy=p, env=ENV, preset="contact_v1", conds="fric_x0.4,dens_x0.5", offset=24, episodes=72) for p in SERVERS]
    jobs += [dict(policy=p, env=ENV, preset="sweep_v1", conds="nominal", offset=48, episodes=48) for p in SERVERS]
    run_phase("eggplant_contact_96", jobs)
    r = subprocess.run([str(PY), "scripts/analyze_equiv_pairs.py", "--root", OUT, f"--envs={ENV}",
                        "--out", f"{OUT}/analysis_equiv_pairs_eggplant_contact96.md"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    log(f"analysis rc={r.returncode}")
    log("CONTACT_EXT_DONE")


if __name__ == "__main__":
    main()
