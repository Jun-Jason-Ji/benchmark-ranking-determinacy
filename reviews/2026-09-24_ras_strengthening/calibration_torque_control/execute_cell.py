"""Independent secondary half-torque control; one fresh environment per episode.

This file executes only within a separately frozen, reset-validated secondary study. It leaves
installed packages, earlier attempts, and inference-server configuration alone.
"""
from collections import deque
from pathlib import Path
import argparse,gc,hashlib,importlib.metadata,json,sys,time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
RESET=HERE.parent/'calibration_reset_validation'
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(HERE))

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def check(value,message):
    if not value:raise RuntimeError(message)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--policy-name',required=True,choices=['octo-small','octo-base'])
    ap.add_argument('--policy-url',required=True)
    ap.add_argument('--condition',required=True,choices=['forcehalf'])
    ap.add_argument('--policy-seed-base',type=int,required=True)
    ap.add_argument('--output-dir',required=True)
    args=ap.parse_args()
    frozen=json.loads((HERE/'FROZEN_PLAN.json').read_text())
    check(frozen.get('protocol_version')=='SECONDARY-controlled-initialization-half-torque'and frozen.get('reset_validation_passed')is True,'Secondary torque study is not validated/frozen')
    for rel,digest in frozen['files'].items():check(sha(ROOT/rel)==digest,f'Frozen file changed: {rel}')
    check(args.policy_seed_base in frozen['seeds'],'Unplanned policy seed base')

    import numpy as np
    import torch
    import sapien
    import mani_skill.envs
    import controller_sweep as sweep
    from ms3_windows_compat import apply_compatibility
    from fresh_reset_torque import fresh_reset_episode,joint_properties,controller_properties,contact_properties
    compatibility=apply_compatibility()
    env_id='PutSpoonOnTableClothInScene-v1'
    device=sapien.Device('cuda');render_backend='pci:'+device.pci_string
    out=Path(args.output_dir)/args.policy_name/env_id;out.mkdir(parents=True,exist_ok=True)
    condition=args.condition;audit_path=out/f'{condition}_audit.jsonl'
    def emit(kind,**values):
        with audit_path.open('a',encoding='utf-8')as f:
            f.write(json.dumps({'kind':kind,'time_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),**values})+'\n')
    source_paths=[Path(__file__),HERE/'fresh_reset_torque.py',ROOT/'scripts/controller_sweep.py',ROOT/'scripts/octo_policy_server.py',ROOT/'scripts/ms3_windows_compat.py']
    emit('cell_start',argv=sys.argv[1:],source_sha256={p.relative_to(ROOT).as_posix():sha(p)for p in source_paths},
         frozen_plan_sha256=sha(HERE/'FROZEN_PLAN.json'))
    client=sweep.PolicyClient(args.policy_url);health=client.health()
    check(health.get('model')==args.policy_name and health.get('session_isolation')is True,'Wrong or unisolated server')
    variant=dict(sweep.VARIANTS['default'])
    metadata=dict(started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
       protocol_version='SECONDARY-controlled-initialization-half-torque',
       args=dict(policy_name=args.policy_name,env_id=env_id,policy_url=args.policy_url,
                 policy_seed_base=args.policy_seed_base,conditions=condition,episodes=24,episode_offset=0),
       variant_config=variant,policy_server=health,compatibility_adapter=compatibility,
       versions={p:importlib.metadata.version(p)for p in ['sapien','mani_skill','torch','gymnasium','numpy']},
       nominal=sweep.NOMINAL,initialization='fresh environment; nominal settling; then arm force limits halved without physics advance',
       render_device=device.name,sim_backend='cpu',render_backend=render_backend,
       source_sha256={p.relative_to(ROOT).as_posix():sha(p)for p in source_paths})
    (out/f'{condition}_run_meta.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
    validation_records=[json.loads(s)for s in (RESET/'reset_records.jsonl').read_text().splitlines()if s.strip()]
    canonical={r['episode_id']:(r['state_sha256'],r['image_sha256'])for r in validation_records if r['pass_number']==0}
    check(set(canonical)==set(range(24)),'Incomplete validated canonical-scene inventory')
    raw=out/f'{condition}.jsonl'
    old=[json.loads(s)for s in raw.read_text().splitlines()if s.strip()]if raw.exists()else[]
    done={r['episode_id']for r in old};check(len(done)==len(old),'Duplicate stored episode IDs')
    check(all(r['policy_seed']==args.policy_seed_base+r['episode_id']for r in old),'Retry would alter existing seed identities')
    effective=None
    for ep in range(24):
        if ep in done:continue
        started=time.perf_counter();seed=args.policy_seed_base+ep
        with fresh_reset_episode(env_id,ep,condition,render_backend)as(env,obs,initial):
            emit('environment_reset',**initial)
            check((initial['state_sha256'],initial['image_sha256'])==canonical[ep],'Initial state/image differs from validated canonical scene; no policy action allowed')
            base=env.unwrapped;arm=base.agent.controller.controllers['arm'];gripper=base.agent.controller.controllers['gripper']
            instruction=base.get_language_instruction()[0]
            response=client.reset(instruction,seed,variant)
            check(response.get('ok')and response.get('session')==client.session,'Policy reset session mismatch')
            check(response.get('rng_mode')=='reseed'and response.get('rng_seed')==seed,'Policy did not reseed correctly')
            emit('policy_reset',requested_seed=seed,session=client.session,response=response)
            delay=0
            check(initial['delay_steps']==delay,'Adapter delay mismatch')
            check(initial['force_limit_scale']==.5,'Adapter force limit scale mismatch')
            for key,expected in [('stiffness',sweep.NOMINAL['arm_stiffness']),('damping',sweep.NOMINAL['arm_damping']),('force_limit',[v*.5 for v in sweep.NOMINAL['arm_force_limit']])]:
                check(np.allclose(initial['built_controller'][key],expected,rtol=2e-6,atol=1e-5),'Unexpected controller parameter: '+key)
                check(np.allclose(initial['actual_joints'][key],expected,rtol=2e-6,atol=1e-5),'Unexpected physical drive parameter: '+key)
            queue=deque([np.array([0,0,0,0,0,0,1.],dtype=np.float32)]*delay)if delay else None
            inference_seconds=sim_seconds=0.;last_info=None
            for step in range(60):
                rgb=obs['sensor_data']['3rd_view_camera']['rgb'][0].detach().cpu().numpy().astype(np.uint8)
                response=client.step(rgb)
                check(response.get('session')==client.session,'Action came from a different policy session')
                action=np.asarray(response['action'],dtype=np.float32)
                check(action.shape==(7,)and np.isfinite(action).all(),'Invalid action')
                inference_seconds+=float(response['inference_seconds'])
                if queue is not None:queue.append(action);action=np.asarray(queue.popleft(),dtype=np.float32)
                tick=time.perf_counter()
                obs,reward,terminated,truncated,info=env.step(torch.as_tensor(action)[None])
                sim_seconds+=time.perf_counter()-tick;last_info=info
                if bool(truncated.any()):
                    check(step==59,'Unexpected early time truncation')
                    break
            check(step+1==60,'Incomplete endpoint horizon')
            check(bool(truncated.all()),'Registered episode horizon did not truncate at step 60')
            check(joint_properties(arm)==initial['actual_joints'],'Arm physical gains changed during the episode')
            check(controller_properties(arm)==initial['built_controller'],'Controller config changed during the episode')
            check(joint_properties(gripper)==initial['gripper'],'Gripper properties changed')
            check(contact_properties(base)==initial['object_contact'],'Object mass/material properties changed')
            info=sweep.to_json(last_info)
            flat={k:(v[0]if isinstance(v,list)and len(v)==1 else v)for k,v in info.items()}
            check('success'in flat,'Missing final success criterion')
            rec=dict(policy=args.policy_name,env_id=env_id,condition=condition,episode_id=ep,policy_seed=seed,
                     instruction=instruction,steps=60,success=bool(flat['success']),info=flat,
                     inference_seconds=inference_seconds,sim_seconds=sim_seconds,
                     episode_seconds=time.perf_counter()-started,protocol_version='SECONDARY-controlled-initialization-half-torque')
            effective=dict(arm_stiffness=initial['built_controller']['stiffness'],arm_damping=initial['built_controller']['damping'],
                arm_force_limit=initial['built_controller']['force_limit'],built_stiffness=initial['built_controller']['stiffness'],
                built_damping=initial['built_controller']['damping'],built_force_limit=initial['built_controller']['force_limit'],
                gripper_force_limit=sweep.NOMINAL['gripper_force_limit'],delay_steps=delay,obj_friction=.5,density_scale=1.,
                control_freq=initial['control_freq'],sim_freq=initial['sim_freq'],horizon=60,
                actual_joints=initial['actual_joints'],initialization_protocol='fresh_nominal_settled_then_half_torque')
        check(initial.get('closed_scene_and_agent_cleared')is True,'Environment failed to close completely')
        emit('episode_closed',episode_id=ep,closed_scene_and_agent_cleared=True,active_parameters_unchanged=True)
        with raw.open('a',encoding='utf-8')as f:f.write(json.dumps(rec)+'\n')
        del base,arm,gripper,env,obs
        gc.collect()
        print(f'TECHNICALLY_COMPLETE policy={args.policy_name} setting={condition} episode={ep} steps=60',flush=True)
    rows=[json.loads(s)for s in raw.read_text().splitlines()if s.strip()]
    check(len(rows)==24 and sorted(r['episode_id']for r in rows)==list(range(24)),'Cell inventory incomplete')
    if effective is None:
        # Completed resumed cells retain the original immutable per-condition summary.
        check((out/f'{condition}_summary.json').exists(),'Completed records lack technical summary')
    else:
        summary=dict(run_meta=metadata,conditions={condition:dict(effective=effective,episodes=24,
            successes=sum(r['success']for r in rows),episode_ids=list(range(24)))})
        (out/f'{condition}_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    emit('cell_complete',episodes=24)

if __name__=='__main__':main()
