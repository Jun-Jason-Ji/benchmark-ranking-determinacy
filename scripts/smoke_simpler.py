"""A zero-action environment smoke test, not a learned-policy evaluation."""
import argparse
import json
import time
from pathlib import Path
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--task", default="widowx_put_eggplant_in_basket")
parser.add_argument("--steps", type=int, default=2)
parser.add_argument("--seed", type=int, default=20260918)
parser.add_argument("--output-dir", default="results/simpler_smoke")
args = parser.parse_args()
out = Path(args.output_dir)
out.mkdir(parents=True, exist_ok=True)
started = time.perf_counter()
record = vars(args).copy()
record.update(status="started", policy="zero_action_debug_only", evidence="simulator_smoke_test")
env = None
try:
    import imageio.v2 as imageio
    import simpler_env
    from simpler_env.utils.env.observation_utils import get_image_from_maniskill2_obs_dict
    env = simpler_env.make(args.task)
    observation, reset_info = env.reset(seed=args.seed)
    image = get_image_from_maniskill2_obs_dict(env, observation)
    imageio.imwrite(out / "initial_frame.png", image)
    record["instruction"] = env.get_language_instruction()
    record["action_shape"] = list(env.action_space.shape)
    record["image_shape"] = list(image.shape)
    for _ in range(args.steps):
        observation, reward, terminated, truncated, info = env.step(np.zeros(env.action_space.shape, dtype=np.float32))
        if terminated or truncated:
            break
    record["status"] = "passed"
except Exception as error:
    record.update(status="failed", error_type=type(error).__name__, error=str(error))
    raise
finally:
    record["elapsed_seconds"] = time.perf_counter() - started
    (out / "result.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(json.dumps(record, indent=2), flush=True)
    if env is not None:
        env.close()
