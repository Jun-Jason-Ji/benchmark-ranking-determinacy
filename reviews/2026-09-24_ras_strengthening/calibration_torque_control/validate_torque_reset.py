"""Outcome-free half-torque initialization, physical-property and lifetime check."""
from pathlib import Path
import gc,hashlib,importlib.metadata,json,sys,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
RESET=HERE.parent/'calibration_reset_validation'
sys.path.insert(0,str(ROOT/'scripts'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

if __name__=='__main__':
    assert not (HERE/'torque_reset_records.jsonl').exists(),'Never overwrite a technical attempt'
    frozen=json.loads((HERE/'FROZEN_TECHNICAL_PROTOCOL.json').read_text())
    for path,digest in frozen['files'].items():assert sha(ROOT/path)==digest,path
    refs={r['episode_id']:r for r in map(json.loads,(RESET/'reset_records.jsonl').read_text().splitlines())if r['pass_number']==0}
    assert set(refs)==set(range(24))
    import numpy as np
    import controller_sweep as sweep
    import mani_skill.envs
    import sapien
    from ms3_windows_compat import apply_compatibility
    from fresh_reset_torque import fresh_reset_episode,joint_properties,controller_properties
    compat=apply_compatibility();device=sapien.Device('cuda');backend='pci:'+device.pci_string
    rows=[];times=[];started=time.perf_counter()
    for pass_no,condition in enumerate(['nominal','forcehalf']):
        for ep in range(24):
            with fresh_reset_episode('PutSpoonOnTableClothInScene-v1',ep,condition,backend)as(env,obs,audit):
                base=env.unwrapped;arm=base.agent.controller.controllers['arm']
                audit['matches_canonical_state']=audit['state']==refs[ep]['state']
                audit['matches_canonical_image']=audit['image_sha256']==refs[ep]['image_sha256']
                assert audit['matches_canonical_state'] and audit['matches_canonical_image']
                expected=dict(stiffness=sweep.NOMINAL['arm_stiffness'],damping=sweep.NOMINAL['arm_damping'],
                    force_limit=[v*(1. if condition=='nominal'else .5)for v in sweep.NOMINAL['arm_force_limit']])
                for key,value in expected.items():
                    assert np.allclose(audit['built_controller'][key],value,rtol=2e-6,atol=1e-5)
                    assert np.allclose(audit['actual_joints'][key],value,rtol=2e-6,atol=1e-5)
                assert audit['delay_steps']==0
                before=joint_properties(arm);state_before=sweep.to_json(base.get_state_dict())
                base.agent.controller.reset()
                audit['parameters_survive_controller_reset']=joint_properties(arm)==before
                audit['state_survives_controller_reset']=sweep.to_json(base.get_state_dict())==state_before
                assert audit['parameters_survive_controller_reset'] and audit['state_survives_controller_reset']
                audit.update(pass_number=pass_no,source_sha256=sha(HERE/'fresh_reset_torque.py'),
                    policy_requests=0,success_fields_read=False)
            assert audit['closed_scene_and_agent_cleared']
            rows.append(audit);times.append(audit['initialization_seconds'])
            with (HERE/'torque_reset_records.jsonl').open('a',encoding='utf-8')as f:f.write(json.dumps(audit)+'\n')
            print(f'TECHNICAL_RESET_PASS condition={condition} configuration={ep}',flush=True)
            del env,obs,base,arm,audit
            gc.collect()
    report=dict(status='pass',cases=len(rows),configurations=24,conditions=['nominal','forcehalf'],
        exact_prior_full_state_and_rgb=True,unchanged_gripper_contact_mass=True,
        actual_physical_and_config_parameters_verified=True,no_policy_calls=True,no_success_fields_read=True,
        compatibility=compat,versions={p:importlib.metadata.version(p)for p in ['mani_skill','sapien','torch','gymnasium','numpy']},
        render_device=device.name,total_seconds=time.perf_counter()-started,
        initialization_seconds=dict(mean=float(np.mean(times)),median=float(np.median(times)),maximum=max(times)),
        records_sha256=sha(HERE/'torque_reset_records.jsonl'),
        prior_canonical_sha256=sha(RESET/'reset_records.jsonl'),frozen_protocol_sha256=sha(HERE/'FROZEN_TECHNICAL_PROTOCOL.json'))
    (HERE/'RESET_VALIDATION_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2),flush=True)
