"""Time per-step inference latency of a running policy server with a real frame.

Usage: python scripts/time_policy_server.py --port 8767 --steps 30 [--image path.png]
Reports mean/median/min of server-side inference seconds and client round-trip.
"""
import argparse
import json
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from controller_sweep import PolicyClient  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--steps", type=int, default=30)
    ap.add_argument("--image", default="results/controller_sweep_smoke/octo-small/PutCarrotOnPlateInScene-v1/nominal_ep000_first.png")
    args = ap.parse_args()
    import imageio.v2 as imageio
    import numpy as np
    img = np.asarray(imageio.imread(args.image))[..., :3].astype(np.uint8)
    c = PolicyClient(f"http://127.0.0.1:{args.port}")
    h = c.health()
    c.reset("put carrot on plate", 20260918)
    server, rtt, first = [], [], None
    for i in range(args.steps):
        t = time.perf_counter()
        r = c.step(img)
        dt = time.perf_counter() - t
        if i == 0:
            first = (r["inference_seconds"], dt)
        else:
            server.append(r["inference_seconds"])
            rtt.append(dt)
    out = dict(port=args.port, model=h.get("model"), backend=h.get("jax_backend"), steps=args.steps,
               first_step_server_s=first[0], first_step_rtt_s=first[1],
               server_mean_s=statistics.mean(server), server_median_s=statistics.median(server),
               server_min_s=min(server), rtt_mean_s=statistics.mean(rtt), image_shape=list(img.shape),
               action_last=r["action"])
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
