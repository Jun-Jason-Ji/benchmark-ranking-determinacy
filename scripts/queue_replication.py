"""Seed replication of the key eggplant finding. After VARIANTS_QUEUE_DONE: rerun eggplant nominal and
fric_x0.4 for octo-small and octo-base with a different policy seed base (20270101) into a separate
output root, 96 episodes each, then compare with the original seed set."""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import SERVERS, PY, log, healthy, busy_ports  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
OUT2 = "results/controller_sweep_gpu_rep"
ENV = "PutEggplantInBasketScene-v1"


def main():
    while "VARIANTS_QUEUE_DONE" not in (LOGS / "queue_variants.out").read_text(encoding="utf-8", errors="replace"):
        time.sleep(120)
    jobs = [dict(policy=p, conds=c) for p in SERVERS for c in ("nominal", "fric_x0.4")]
    running = {}
    while jobs or running:
        for port, (proc, job) in list(running.items()):
            if proc.poll() is not None:
                log(f"done rc={proc.returncode} {job}")
                running.pop(port)
        taken = busy_ports() | set(running)
        for job in list(jobs):
            free = [p for p in SERVERS[job["policy"]] if p not in taken and healthy(p, job["policy"])]
            if not free:
                continue
            port = free[0]
            preset = "sweep_v1" if job["conds"] == "nominal" else "contact_v1"
            cmd = [str(PY), "scripts/controller_sweep.py", "--policy-name", job["policy"], "--policy-url", f"http://127.0.0.1:{port}",
                   "--env-id", ENV, "--preset", preset, "--conditions", job["conds"], "--episodes", "96",
                   "--policy-seed-base", "20270101", "--output-dir", OUT2]
            lf = open(LOGS / "jobs" / f"rep_{job['policy']}_{job['conds']}.out", "a", encoding="utf-8")
            running[port] = (subprocess.Popen(cmd, cwd=ROOT, stdout=lf, stderr=subprocess.STDOUT), job)
            taken.add(port)
            jobs.remove(job)
            log(f"launched {job} on {port}")
        time.sleep(20)
    # compare
    import numpy as np
    rng = np.random.default_rng(0)

    def load(root, p, c):
        f = ROOT / root / p / ENV / f"{c}.jsonl"
        return {json.loads(l)["episode_id"]: int(bool(json.loads(l)["success"])) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()}

    def boot(d):
        d = np.asarray(d, float); m = d[rng.integers(0, len(d), size=(20000, len(d)))].mean(1)
        return d.mean(), np.percentile(m, 2.5), np.percentile(m, 97.5)

    lines = ["# Seed replication: eggplant nominal vs fric_x0.4 (policy seeds 20270101+ep)", "", "| seed set | condition | n | small | base | Δ | 95% |", "|---|---|---:|---:|---:|---:|---|"]
    for root, tag in [("results/controller_sweep_gpu", "original"), (OUT2, "replication")]:
        for c in ("nominal", "fric_x0.4"):
            S, B = load(root, "octo-small", c), load(root, "octo-base", c)
            e = sorted(set(S) & set(B)); m, lo, hi = boot([S[i] - B[i] for i in e])
            lines.append(f"| {tag} | {c} | {len(e)} | {sum(S[i] for i in e)} | {sum(B[i] for i in e)} | {m:+.3f} | [{lo:+.2f}, {hi:+.2f}] |")
    S1, B1 = load(OUT2, "octo-small", "fric_x0.4"), load(OUT2, "octo-base", "fric_x0.4")
    S0, B0 = load(OUT2, "octo-small", "nominal"), load(OUT2, "octo-base", "nominal")
    e = sorted(set(S1) & set(B1) & set(S0) & set(B0)); m, lo, hi = boot([(S1[i] - B1[i]) - (S0[i] - B0[i]) for i in e])
    lines += ["", f"Replication: Δ(fric) − Δ(nominal) = {m:+.3f} [{lo:+.2f}, {hi:+.2f}] (n={len(e)})"]
    (ROOT / OUT2 / "analysis_replication.md").write_text("\n".join(lines), encoding="utf-8")
    log("REPLICATION_DONE")


if __name__ == "__main__":
    main()
