"""Only reset states, rendered inputs, parameters and object lifetimes are inspected."""
from pathlib import Path
import hashlib,importlib.metadata,json,sys,time
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import controller_sweep as sweep
import numpy as np
import torch
import sapien
import mani_skill.envs
from mani_skill.envs.tasks.digital_twins.bridge_dataset_eval import put_on_in_scene
from ms3_windows_compat import apply_compatibility
from fresh_reset import fresh_reset_episode,joint_properties,controller_properties
import imageio.v2 as imageio
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

if __name__=='__main__':
    assert not (HERE/'reset_records.jsonl').exists(),'Never overwrite a technical attempt'
    frozen=json.loads((HERE/'FROZEN_TECHNICAL_PROTOCOL.json').read_text())
    for name,digest in frozen['files'].items():assert sha(ROOT/name)==digest,name
    compat=apply_compatibility();device=sapien.Device('cuda');render_backend='pci:'+device.pci_string
    (HERE/'canonical_images').mkdir(exist_ok=True)
    refs={};rows=[];times=[];started=time.perf_counter()
    for pass_no,condition in enumerate(['nominal','fitted','fitted','nominal']):
        for ep in range(24):
            with fresh_reset_episode('PutSpoonOnTableClothInScene-v1',ep,condition,render_backend) as (env,obs,audit):
                base=env.unwrapped;arm=base.agent.controller.controllers['arm']
                current=(audit['state_sha256'],audit['image_sha256'])
                rgb=obs['sensor_data']['3rd_view_camera']['rgb'][0].detach().cpu().numpy().copy()
                if pass_no==0:
                    refs[ep]=current
                    imageio.imwrite(HERE/'canonical_images'/f'spoon_{ep:02d}.png',rgb)
                audit['matches_canonical_state_and_image']=current==refs[ep]
                # Controller reset should not alter gains or canonical physical state.
                arm_before=joint_properties(arm);state_before=sweep.to_json(base.get_state_dict())
                base.agent.controller.reset()
                audit['gains_survive_controller_reset']=joint_properties(arm)==arm_before
                audit['state_survives_controller_reset']=sweep.to_json(base.get_state_dict())==state_before
                assert audit['gains_survive_controller_reset'] and audit['state_survives_controller_reset']
                audit.update(pass_number=pass_no,source_hash=sha(HERE/'fresh_reset.py'),
                             success_fields_read=False,policy_requests=0)
            assert audit['closed_scene_and_agent_cleared']
            rows.append(audit);times.append(audit['initialization_seconds'])
            with (HERE/'reset_records.jsonl').open('a',encoding='utf-8') as stream:stream.write(json.dumps(audit)+'\n')
            print(json.dumps(dict(pass_number=pass_no,condition=condition,episode=ep,
                exact_match=audit['matches_canonical_state_and_image'],seconds=audit['initialization_seconds'])),flush=True)
            del env,obs,base,arm,audit
    report=dict(status='pass' if all(r['matches_canonical_state_and_image'] for r in rows) else 'fail',
        cases=len(rows),unique_configurations=len(refs),fresh_constructions_in_one_process=True,
        mismatches=[dict(pass_number=r['pass_number'],episode_id=r['episode_id'])for r in rows if not r['matches_canonical_state_and_image']],
        exact_full_state_and_rgb_across_nominal_fitted=True if all(r['matches_canonical_state_and_image']for r in rows) else False,
        no_policy_calls=True,no_success_fields_read=True,compatibility=compat,
        versions={p:importlib.metadata.version(p)for p in ['mani_skill','sapien','torch','gymnasium','numpy']},
        total_seconds=time.perf_counter()-started,initialization_seconds=dict(mean=float(np.mean(times)),median=float(np.median(times)),maximum=max(times)),
        mean_initialization_overhead_768_rollouts_seconds=float(np.mean(times)*768),
        records_sha256=sha(HERE/'reset_records.jsonl'),frozen_protocol_sha256=sha(HERE/'FROZEN_TECHNICAL_PROTOCOL.json'))
    (HERE/'RESULTS.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
    if report['status']!='pass':raise SystemExit(2)
