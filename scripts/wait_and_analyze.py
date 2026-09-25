"""Generic waiter: poll until every (policy, env, condition) JSONL under --root has >= --n episodes,
then run analyze_controller_sweep.py on --root and write --out. Detached-friendly (prints progress).

Usage:
  python scripts/wait_and_analyze.py --root results/controller_sweep_gpu --env PutCarrotOnPlateInScene-v1 \
      --policies octo-small,octo-base --conditions iso_x0.25,iso_x0.5,iso_x2.0,iso_x4.0 --n 24 \
      --out results/controller_sweep_gpu/analysis_iso_carrot.md
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = ROOT / ".venv-windows-ms3/Scripts/python.exe"


def count(root, policy, env, cond):
    f = ROOT / root / policy / env / f"{cond}.jsonl"
    if not f.exists():
        return 0
    return sum(1 for l in f.read_text(encoding="utf-8").splitlines() if l.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--env", required=True)
    ap.add_argument("--policies", required=True)
    ap.add_argument("--conditions", required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--poll", type=int, default=60)
    ap.add_argument("--script", default="scripts/analyze_controller_sweep.py")
    ap.add_argument("--extra", default="", help="extra args for the analysis script")
    args = ap.parse_args()
    pols, conds, envs = args.policies.split(","), args.conditions.split(","), args.env.split(",")
    while True:
        status = {p: {f"{e}/{c}": count(args.root, p, e, c) for e in envs for c in conds} for p in pols}
        print(time.strftime("%H:%M:%S"), json.dumps(status), flush=True)
        if all(v >= args.n for p in pols for v in status[p].values()):
            break
        time.sleep(args.poll)
    r = subprocess.run([str(PY), args.script, "--root", args.root, "--out", args.out] + (args.extra.split() if args.extra else []),
                       cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    print("analysis rc", r.returncode, flush=True)
    if r.returncode != 0:
        print(r.stderr[-2000:], flush=True)
    print("WAIT_ANALYZE_DONE", args.out, flush=True)


if __name__ == "__main__":
    main()
