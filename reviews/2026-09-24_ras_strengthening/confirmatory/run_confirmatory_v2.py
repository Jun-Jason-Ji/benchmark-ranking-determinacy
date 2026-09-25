"""Frozen confirmatory native-task protocol; writes only its own output directory."""
import argparse,ctypes,hashlib,importlib.metadata,json,os,platform,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OLD=ROOT/'reviews/2026-09-24_ras_retarget/cross_benchmark'
parser=argparse.ArgumentParser()
parser.add_argument('--task',choices=['PickCube-v1','PushCube-v1'],required=True)
parser.add_argument('--mode',choices=['pd_joint_delta_pos','pd_ee_delta_pos'],required=True)
args=parser.parse_args()
PLAN_SHA=hashlib.sha256((HERE/'PLAN.md').read_bytes()).hexdigest()
SOURCE_SHA=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
FROZEN=json.loads((HERE/'FROZEN_RUNTIME_AMENDMENT_V2.json').read_text())
assert FROZEN['files']['PLAN.md']==PLAN_SHA
assert FROZEN['files']['run_confirmatory_v2.py']==SOURCE_SHA
os.environ['MS_ASSET_DIR']=str(HERE/'assets')
import numpy as np
import torch
import torch.nn as nn
import gymnasium as gym
import mani_skill.envs
import sapien.physx
torch.set_num_threads(2)
DLL_DIRECTORY=os.add_dll_directory(str(OLD/'physx_runtime'))
ctypes.CDLL('nvcuda.dll');ctypes.CDLL(str(OLD/'physx_runtime/PhysXGpu_64.dll'))
sapien.physx._enable_gpu()

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def to_json(x):
    if isinstance(x,dict):return {str(k):to_json(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [to_json(v) for v in x]
    if isinstance(x,torch.Tensor):return x.detach().cpu().tolist()
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    return x
def state(base):
    obj=base.cube if hasattr(base,'cube') else base.obj
    target=base.goal_site if hasattr(base,'goal_site') else base.goal_region
    return dict(qpos=base.agent.robot.get_qpos().clone(),qvel=base.agent.robot.get_qvel().clone(),
                cube_state=obj.get_state().clone(),goal_state=target.get_state().clone())

task_short=args.task.split('-')[0]
name=f'ppo_{args.mode}_ckpt.pt'
ckpt=OLD/(name if task_short=='PickCube' else 'PushCube_'+name)
official={x['path'].split('/')[-1]:x for x in json.loads((OLD/('hf_pickcube_tree.json' if task_short=='PickCube' else 'hf_pushcube_tree.json')).read_text())}
assert sha(ckpt)==official[name]['lfs']['oid']
weights=torch.load(ckpt,map_location='cuda',weights_only=True)
d=[weights[f'actor_mean.{i}.weight'].shape for i in [0,2,4,6]]
actor=nn.Sequential(nn.Linear(d[0][1],d[0][0]),nn.Tanh(),nn.Linear(d[1][1],d[1][0]),nn.Tanh(),
                    nn.Linear(d[2][1],d[2][0]),nn.Tanh(),nn.Linear(d[3][1],d[3][0])).cuda()
actor.load_state_dict({k[len('actor_mean.'):]:v for k,v in weights.items() if k.startswith('actor_mean.')},strict=True)
actor.eval()
env=gym.make(args.task,num_envs=256,obs_mode='state',control_mode=args.mode,
             sim_backend='gpu',render_backend='cpu',enhanced_determinism=True,
             reconfiguration_freq=0,max_episode_steps=100)
base=env.unwrapped
assert base.control_freq==20 and base.sim_freq==100
arm=base.agent.controller.controllers['arm']
nominal={k:float(getattr(arm.config,k)) for k in ['stiffness','damping','force_limit']}
assert nominal==dict(stiffness=1000.0,damping=100.0,force_limit=100.0)
out=HERE/'raw_v2';out.mkdir(exist_ok=True)
for batch,seed_start in enumerate([731250001,893460001,1135790001,1579130001]):
    for setting in ['nominal','gain_half','gain_double','force_half','force_double']:
        output=out/f'{args.task}_{args.mode}_{setting}_batch{batch}.json'
        if output.exists():raise FileExistsError(output)
        started=time.time()
        # Assign from the original constants, never multiply an already changed value.
        for k,v in nominal.items():setattr(arm.config,k,v)
        arm.set_drive_property()
        obs,_=env.reset(seed=list(range(seed_start,seed_start+256)))
        initial=state(base)
        full_initial=to_json(base.get_state_dict())
        initial_obs=obs.detach().cpu().tolist()
        gain=.5 if setting=='gain_half' else 2.0 if setting=='gain_double' else 1.0
        force=.5 if setting=='force_half' else 2.0 if setting=='force_double' else 1.0
        arm.config.stiffness=nominal['stiffness']*gain
        arm.config.damping=nominal['damping']*gain
        arm.config.force_limit=nominal['force_limit']*force
        arm.set_drive_property()
        sequences=[];at50=None;at100=None
        with torch.no_grad():
            for step in range(1,101):
                obs,_,terminated,truncated,info=env.step(actor(obs))
                if not bool(torch.isfinite(obs).all()):raise ValueError('Non-finite observation')
                sequences.append(info['success'].detach().cpu().numpy().astype(np.uint8))
                if step==50:at50=to_json(state(base))
                if step<100 and bool(truncated.any()):raise AssertionError('Early timeout')
        assert bool(truncated.all()) and int(base.elapsed_steps.min())==100 and int(base.elapsed_steps.max())==100
        at100=to_json(state(base))
        seq=np.stack(sequences,axis=1)
        initial=to_json(initial)
        report=dict(experiment='native_confirmatory_holdout',task=args.task,mode=args.mode,
            batch=batch,setting=setting,scene_seed_vector_start=seed_start,num_scenes=256,
            plan_sha256=PLAN_SHA,evaluator_sha256=SOURCE_SHA,checkpoint_sha256=sha(ckpt),
            frozen_manifest_sha256=sha(HERE/'FROZEN_RUNTIME_AMENDMENT_V2.json'),
            versions={k:importlib.metadata.version(k) for k in ['mani_skill','sapien','torch','numpy','gymnasium']},
            platform=platform.platform(),sim_freq=base.sim_freq,control_freq=base.control_freq,steps=100,
            nominal_gains=nominal,applied_gains={k:float(getattr(arm.config,k)) for k in nominal},
            initial_state_dict=full_initial,initial_observations=initial_obs,
            episodes=[dict(scene_slot=i,requested_reset_seed=seed_start+i,
                initial_state={k:v[i] for k,v in initial.items()},
                success_sequence=seq[i].tolist(),state_at_50={k:v[i] for k,v in at50.items()},
                state_at_100={k:v[i] for k,v in at100.items()}) for i in range(256)],
            elapsed_seconds=time.time()-started)
        output.write_text(json.dumps(report,separators=(',',':'),allow_nan=False),encoding='utf-8')
        print(json.dumps(dict(cell=output.name,seconds=report['elapsed_seconds'],completed=True)),flush=True)
env.close()
