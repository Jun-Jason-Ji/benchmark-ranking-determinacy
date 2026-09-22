"""Re-run the two second-seed-set jobs whose records were quarantined after the shared-server contamination
(results/contaminated_2026-09-19/README.md): octo-base dens_x0.5 and octo-base@hist1 iso_x0.25, eggplant, 48 eps,
seed base 20270101, on the Octo-base servers. Uses the same run() as queue_replication_neartied.py."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_replication_neartied import run, log  # noqa: E402

if __name__ == "__main__":
    run("rep_recontam_base", [dict(policy="octo-base", conds="dens_x0.5"), dict(policy="octo-base@hist1", conds="iso_x0.25")], [8768, 8770])
    log("REP_RECONTAM_DONE")
