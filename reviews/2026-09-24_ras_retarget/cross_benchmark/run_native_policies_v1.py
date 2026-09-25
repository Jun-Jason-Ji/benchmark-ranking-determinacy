"""Evaluate public PPO pipelines on native ManiSkill tasks; no SIMPLER adapter.

Uses unchanged official CPU rendering/GPU PhysX and built-in GPU IK. The only
runtime accommodation is the location of the official PhysX DLL. Runs are saved
per episode, with initial physical states to verify scene matching.
"""
import argparse, ctypes, hashlib, importlib.metadata, json, os, platform, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--env-id', default='PickCube-v1')
parser.add_argument('--mode', required=True, choices=['pd_joint_delta_pos','pd_ee_delta_pos'])
parser.add_argument('--num-envs', type=int, default=16)
parser.add_argument('--setting', default='nominal', choices=['nominal','gain_half','gain_double','force_half','force_double'])
parser.add_argument('--seed-start', type=int, default=2026092400)
parser.add_argument('--output', required=True)
args = parser.parse_args()
os.environ['MS_ASSET_DIR'] = str(HERE/'assets')
import numpy as np
import torch
import torch.nn as nn
import gymnasium as gym
import mani_skill.envs
import sapien.physx
torch.set_num_threads(2)
dll_directory = os.add_dll_directory(str(HERE/'physx_runtime'))
ctypes.CDLL('nvcuda.dll')
ctypes.CDLL(str(HERE/'physx_runtime/PhysXGpu_64.dll'))
sapien.physx._enable_gpu()

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def tensor(x): return x.detach().cpu().numpy()
task_short = args.env_id.split('-')[0]
ckpt = HERE / (f'ppo_{args.mode}_ckpt.pt' if task_short=='PickCube' else f'{task_short}_ppo_{args.mode}_ckpt.pt')
weights = torch.load(ckpt, map_location='cuda', weights_only=True)
dimensions = [weights[f'actor_mean.{i}.weight'].shape for i in [0,2,4,6]]
actor = nn.Sequential(nn.Linear(dimensions[0][1],dimensions[0][0]),nn.Tanh(),
                      nn.Linear(dimensions[1][1],dimensions[1][0]),nn.Tanh(),
                      nn.Linear(dimensions[2][1],dimensions[2][0]),nn.Tanh(),
                      nn.Linear(dimensions[3][1],dimensions[3][0])).cuda()
actor.load_state_dict({k[len('actor_mean.'):]:v for k,v in weights.items() if k.startswith('actor_mean.')}, strict=True)
actor.eval()
env = gym.make(args.env_id, num_envs=args.num_envs, obs_mode='state', control_mode=args.mode,
               sim_backend='gpu', render_backend='cpu', enhanced_determinism=True,
               reconfiguration_freq=0, max_episode_steps=50)
start = time.time()
seeds = list(range(args.seed_start, args.seed_start+args.num_envs))
obs, _ = env.reset(seed=seeds)
base = env.unwrapped
initial = dict(qpos=tensor(base.agent.robot.get_qpos()), cube_pose=tensor(base.cube.pose.raw_pose))
if hasattr(base,'goal_site'): initial['goal_pose']=tensor(base.goal_site.pose.raw_pose)
arm = base.agent.controller.controllers['arm']
nominal = {k:float(getattr(arm.config,k)) for k in ['stiffness','damping','force_limit']}
gain = .5 if args.setting=='gain_half' else 2.0 if args.setting=='gain_double' else 1.0
force = .5 if args.setting=='force_half' else 2.0 if args.setting=='force_double' else 1.0
arm.config.stiffness = nominal['stiffness']*gain
arm.config.damping = nominal['damping']*gain
arm.config.force_limit = nominal['force_limit']*force
arm.set_drive_property()
once = torch.zeros(args.num_envs, dtype=torch.bool, device=obs.device)
with torch.inference_mode():
    for step in range(50):
        action = actor(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        if not bool(torch.isfinite(obs).all()): raise ValueError('Non-finite state')
        once |= info['success']
last = tensor(info['success']).astype(bool)
once = tensor(once).astype(bool)
record = dict(experiment='independent_native_task_pilot', args=vars(args),
              versions={p:importlib.metadata.version(p) for p in ['mani_skill','sapien','torch','gymnasium','numpy']},
              platform=platform.platform(), checkpoint_sha256=sha(ckpt), script_sha256=sha(Path(__file__)),
              nominal_arm_gains=nominal, applied_arm_gains={k:float(getattr(arm.config,k)) for k in nominal},
              policy_execution='deterministic actor mean; no action noise', simulator='native GPU PhysX',
              elapsed_seconds=time.time()-start, success_at_end=int(last.sum()), success_once=int(once.sum()),
              episodes=[dict(scene_id=i,reset_seed=seeds[i],success_at_end=bool(last[i]),success_once=bool(once[i]),
                             initial_state={k:v[i].tolist() for k,v in initial.items()}) for i in range(args.num_envs)])
output=HERE/args.output
output.parent.mkdir(parents=True,exist_ok=True)
if output.exists(): raise FileExistsError(output)
output.write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in record.items() if k!='episodes'},indent=2),flush=True)
env.close()
