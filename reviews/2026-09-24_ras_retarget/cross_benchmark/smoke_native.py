"""Native ManiSkill task availability probe; NOT a policy or scientific result."""
import argparse, importlib.metadata, json, os, time, traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--backend', default='cpu')
parser.add_argument('--project-physx', action='store_true')
args = parser.parse_args()
os.environ['MS_ASSET_DIR'] = str(HERE / 'assets')
started = time.time()
report = dict(purpose='technical smoke test only', backend=args.backend)
env = None
try:
    import gymnasium as gym
    import numpy as np
    import torch
    import mani_skill.envs
    if args.project_physx:
        import ctypes, sapien.physx
        os.add_dll_directory(str(HERE / 'physx_runtime'))
        ctypes.CDLL('nvcuda.dll')
        ctypes.CDLL(str(HERE / 'physx_runtime/PhysXGpu_64.dll'))
        sapien.physx._enable_gpu()
        report['gpu_library_location'] = 'audit-directory-only; official unchanged library'
    report['versions'] = {x: importlib.metadata.version(x) for x in ['torch','mani_skill','sapien','gymnasium']}
    report['torch_cuda'] = torch.cuda.is_available()
    env = gym.make('PickCube-v1', num_envs=1, obs_mode='state', control_mode='pd_joint_delta_pos', sim_backend=args.backend, render_backend='cpu')
    obs, info = env.reset(seed=20260924)
    report['observation_shape'] = list(obs.shape)
    report['action_shape'] = list(env.action_space.shape)
    step_started = time.time()
    for i in range(50):
        obs, reward, terminated, truncated, info = env.step(np.zeros(env.action_space.shape, dtype=np.float32))
    report['step_seconds'] = time.time() - step_started
    report['finite'] = bool(torch.isfinite(obs).all())
    report['status'] = 'passed'
except Exception as e:
    report.update(status='failed', error=repr(e), traceback=traceback.format_exc())
finally:
    report['elapsed_seconds'] = time.time()-started
    (HERE / ('smoke_'+args.backend+'.json')).write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))
    if env is not None:
        env.close()
