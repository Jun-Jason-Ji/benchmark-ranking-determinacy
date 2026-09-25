"""Independent official-Agent/vector-wrapper parity check on the same frozen scenes.

No main grid outputs are overwritten. Source definitions are restricted to the
reviewed historical PPO Agent/layer initializer and observation flattening method.
"""
import ast, ctypes, hashlib, json, os, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MS_ASSET_DIR']=str(HERE/'assets')
import numpy as np
import torch
import torch.nn as nn
from torch.distributions.normal import Normal
import gymnasium as gym
import mani_skill.envs
from mani_skill.utils.common import to_tensor
from mani_skill.vector.wrappers.gymnasium import ManiSkillVectorEnv
import sapien.physx
torch.set_num_threads(2)
dll_directory=os.add_dll_directory(str(HERE/'physx_runtime'))
ctypes.CDLL('nvcuda.dll');ctypes.CDLL(str(HERE/'physx_runtime/PhysXGpu_64.dll'))
sapien.physx._enable_gpu()

class StripAnnotations(ast.NodeTransformer):
    def visit_FunctionDef(self,node):
        node.returns=None
        for arg in node.args.args+node.args.kwonlyargs: arg.annotation=None
        return self.generic_visit(node)

def defs(path,names):
    tree=ast.parse(path.read_text())
    selected=[]
    for node in ast.walk(tree):
        if isinstance(node,(ast.FunctionDef,ast.ClassDef)) and node.name in names:
            selected.append(node)
    module=ast.fix_missing_locations(StripAnnotations().visit(ast.Module(body=selected,type_ignores=[])))
    ns=dict(torch=torch,np=np,nn=nn,Normal=Normal,to_tensor=to_tensor)
    exec(compile(module,str(path),'exec'),ns)
    return ns

ppo=defs(HERE/'export_commit_ppo_fast.py',{'layer_init','Agent'})
old_flat=defs(HERE/'export_commit_common.py',{'flatten_state_dict'})['flatten_state_dict']
old_extra=defs(HERE/'export_commit_push_cube.py',{'_get_obs_extra'})['_get_obs_extra']
old_agent=defs(HERE/'export_commit_base_agent.py',{'get_proprioception'})['get_proprioception']
records=[]
for mode in ['pd_joint_delta_pos','pd_ee_delta_pos']:
    started=time.time()
    weights=torch.load(HERE/f'PushCube_ppo_{mode}_ckpt.pt',map_location='cuda',weights_only=True)
    agent=ppo['Agent'](weights['actor_mean.0.weight'].shape[1],weights['actor_mean.6.weight'].shape[0],device='cuda')
    agent.load_state_dict(weights,strict=True);agent.eval()
    raw=gym.make('PushCube-v1',num_envs=256,obs_mode='state',control_mode=mode,
                 sim_backend='gpu',render_backend='cpu',enhanced_determinism=True,
                 reconfiguration_freq=0,max_episode_steps=50)
    env=ManiSkillVectorEnv(raw,num_envs=256,ignore_terminations=True,record_metrics=True,auto_reset=False)
    obs,info=env.reset(seed=list(range(2026092500,2026092756)))
    base=raw.unwrapped
    cfg=base.agent.controller.controllers['arm'].config
    before=dict(control_freq=base.control_freq,sim_freq=base.sim_freq,
                obs_shape=list(obs.shape),action_shape=list(env.single_action_space.shape),
                arm_gains={k:float(getattr(cfg,k)) for k in ['stiffness','damping','force_limit']},
                arm_action_lower=cfg.lower if hasattr(cfg,'lower') else cfg.pos_lower,
                arm_action_upper=cfg.upper if hasattr(cfg,'upper') else cfg.pos_upper)
    max_obs_diff=0.0;manual_matches=True
    with torch.inference_mode():
        for step in range(50):
            historical=old_flat(dict(agent=old_agent(base.agent),extra=old_extra(base,base.get_info())),use_torch=True,device=base.device)
            max_obs_diff=max(max_obs_diff,float((historical-obs).abs().max()))
            obs,rew,term,trunc,info=env.step(agent.actor_mean(obs))
            xy=torch.linalg.norm(base.obj.pose.p[:,:2]-base.goal_region.pose.p[:,:2],dim=1)
            height=base.obj.pose.p[:,2]
            manual=(xy<base.goal_radius)&(height<base.cube_half_size+.005)
            manual_matches &= bool((manual==info['success']).all())
    end=info['episode']['success_at_end'].cpu().numpy().astype(bool)
    ever=info['episode']['success_once'].cpu().numpy().astype(bool)
    prior=json.loads((HERE/'full_grid'/f'PushCube-v1_{mode}_nominal.json').read_text())
    expected=np.array([e['success_at_end'] for e in prior['episodes']],dtype=bool)
    expected_ever=np.array([e['success_once'] for e in prior['episodes']],dtype=bool)
    rec=dict(mode=mode,configuration=before,success_at_end=int(end.sum()),success_once=int(ever.sum()),
             initial_and_each_step_historical_observation_max_abs_diff=max_obs_diff,
             manual_success_agrees_at_all_steps=manual_matches,
             original_loop_vs_official_wrapper_episode_disagreements=int((end!=expected).sum()),
             original_loop_vs_official_wrapper_ever_disagreements=int((ever!=expected_ever).sum()),
             final_truncations=int(trunc.sum()),final_episode_lengths=sorted(set(info['episode']['episode_len'].cpu().tolist())),
             final_xy_in_goal=int((xy<base.goal_radius).sum()),
             final_old_height_criterion_success=int(((xy<base.goal_radius)&(height<base.cube_half_size+.001)).sum()),
             final_cube_height_quantiles=np.quantile(height.cpu().numpy(),[0,.25,.5,.75,1]).tolist(),
             elapsed_seconds=time.time()-started)
    assert max_obs_diff==0 and manual_matches
    assert np.array_equal(end,expected) and np.array_equal(ever,expected_ever)
    assert rec['final_episode_lengths']==[50] and rec['final_truncations']==256
    records.append(rec)
    env.close()
    print(json.dumps(rec,indent=2),flush=True)
report=dict(status='passed',purpose='evaluator parity; not additional independent outcome evidence',
            checked_export_commit='baab60ede2e89167c1b7aaed41a9aa8e690a9d1e',runs=records,
            limitation='This rules out the checked local inference/observation/termination mistakes; it does not prove equality of old and current simulator dynamics.')
(HERE/'INTERFACE_AUDIT.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
