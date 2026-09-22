"""After REPLICATION_DONE: rerun eggplant nominal episodes 0-23 for both policies with the ORIGINAL policy
seed base (20260918) on the restarted servers into a separate root, and compare per-episode outcomes with
the original run. Identical outcomes => no code-path drift after the server restart; the replication
difference is then attributable to policy seeds alone."""
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import run_phase, log  # noqa: E402
import queue_v2  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
ENV = "PutEggplantInBasketScene-v1"
OUT_DET = "results/controller_sweep_gpu_det"


def main():
    while "REPLICATION_DONE" not in (LOGS / "queue_replication.out").read_text(encoding="utf-8", errors="replace"):
        time.sleep(60)
    queue_v2.OUT = OUT_DET  # run_phase reads the module global
    jobs = [dict(policy=p, env=ENV, preset="sweep_v1", conds="nominal", offset=0, episodes=24) for p in ("octo-small", "octo-base")]
    run_phase("determinism_check", jobs)
    lines = ["# Determinism check: original seeds re-run on restarted servers (eggplant nominal, episodes 0-23)", "",
             "| policy | n | original successes | rerun successes | identical episodes |", "|---|---:|---:|---:|---:|"]
    for p in ("octo-small", "octo-base"):
        def load(root):
            f = ROOT / root / p / ENV / "nominal.jsonl"
            return {json.loads(l)["episode_id"]: int(bool(json.loads(l)["success"])) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()}
        A, B = load("results/controller_sweep_gpu"), load(OUT_DET)
        e = sorted(set(A) & set(B))
        lines.append(f"| {p} | {len(e)} | {sum(A[i] for i in e)} | {sum(B[i] for i in e)} | {sum(A[i] == B[i] for i in e)} |")
    (ROOT / OUT_DET / "analysis_determinism.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)
    log("DETERMINISM_DONE")


if __name__ == "__main__":
    main()
