"""Inspect completed-cell interfaces only; no success aggregation or inference.

This separate diagnostic does not modify the frozen analysis or evaluation.
It never reads a success field, computes a policy gap, or evaluates a p-value.
"""
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path
import sys
import numpy as np
import analyze_confirmation as spec

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import controller_sweep

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(condition,message):
    if not condition:raise ValueError(message)
def readjson(p):return json.loads(p.read_text(encoding='utf-8'))
def readlines(p):return [json.loads(s)for s in p.read_text(encoding='utf-8').splitlines()if s.strip()]

def main():
    frozen=readjson(HERE/'FROZEN_PLAN.json');af=readjson(HERE/'FROZEN_ANALYSIS.json')
    require(sha(HERE/'analyze_confirmation.py')==af['analyzer_sha256'],'Frozen analyzer changed')
    for rel,want in frozen['files'].items():require(sha(ROOT/rel)==want,f'Frozen source changed: {rel}')
    checked=[];issues=[];reference={};fingerprints={};frequencies=set();states=set()
    for summary_path in sorted((HERE/'data').rglob('*_summary.json')):
        directory=summary_path.parent
        condition=summary_path.name.removesuffix('_summary.json')
        if condition not in spec.CONDITIONS:continue
        policy=directory.parent.name;block=int(directory.parents[1].name.removeprefix('block_'))
        audit_path=directory/f'{condition}_audit.jsonl'
        audit=readlines(audit_path)
        if not any(e['kind']=='cell_complete'for e in audit):continue
        name=f'block_{block:02d}/{policy}/{condition}'
        try:
            require(policy in spec.POLICIES and 1<=block<=8,'Scope mismatch')
            base=spec.SEEDS[block-1]
            rows=readlines(directory/f'{condition}.jsonl')
            require(len(rows)==24 and sorted(r['episode_id']for r in rows)==list(range(24)),'Record inventory mismatch')
            for r in rows:
                require(r['policy']==policy and r['env_id']==spec.ENV and r['condition']==condition,'Record scope mismatch')
                require(r['steps']==60 and r['policy_seed']==base+r['episode_id'],'Horizon/seed mismatch')
            # No success field is accessed; only technical metadata is used.
            meta=readjson(directory/f'{condition}_run_meta.json')
            eff=readjson(summary_path)['conditions'][condition]['effective']
            args=meta['args'];variant=meta['variant_config']
            require(args['conditions']==condition and args['policy_seed_base']==base,'Metadata condition/seed mismatch')
            require(variant['history']==2 and variant['ensemble']is True and variant['exec_horizon']==1,'Policy mode mismatch')
            ss,ds,delay=(1.,1.,0)if condition=='nominal'else(2.,.5,1)
            for key,factor,nominal_key in [('built_stiffness',ss,'arm_stiffness'),('built_damping',ds,'arm_damping'),('built_force_limit',1.,'arm_force_limit')]:
                require(np.allclose(eff[key],np.asarray(controller_sweep.NOMINAL[nominal_key])*factor,rtol=2e-6,atol=1e-5),f'Built parameters mismatch: {key}')
            require(eff['delay_steps']==delay and eff['horizon']==60,'Built delay/horizon mismatch')
            require(eff['gripper_force_limit']==controller_sweep.NOMINAL['gripper_force_limit'],'Gripper changed')
            require(eff['obj_friction']==.5 and eff['density_scale']==1.,'Contact parameters changed')
            frequencies.add((eff['control_freq'],eff['sim_freq']))
            health=meta['policy_server']
            require(health['model']==policy and health.get('session_isolation')is True,'Server scope/session isolation mismatch')
            fp={k:health.get(k)for k in ['model','hf_id','jax','flax','tensorflow','numpy','python','action_mean','action_std','rotation_convention','policy_setups']}
            if policy in fingerprints:require(fp==fingerprints[policy],'Server fingerprint changed')
            else:fingerprints[policy]=fp
            resets={};requested=set();session_count=set()
            for event in audit:
                if event['kind']=='cell_start':
                    require(event['time_utc']>=af['created_utc'],'Analysis freeze postdates cell start')
                    for rel,want in event['source_sha256'].items():require(sha(ROOT/rel)==want,f'Executed source mismatch: {rel}')
                if event['kind']=='policy_reset':
                    seed=event['requested_seed'];resp=event['response']
                    require(resp.get('ok')and resp.get('session')==event['session'],'Session mismatch')
                    require(resp.get('rng_mode')=='reseed'and resp.get('rng_seed')==seed,'RNG lifecycle mismatch')
                    requested.add(seed);session_count.add(event['session'])
                if event['kind']=='environment_reset':
                    ep=event['seed'];require(ep in range(24),'Unknown initial scene')
                    spec.check_finite(event['state'])
                    state_sha=hashlib.sha256(json.dumps(event['state'],sort_keys=True).encode()).hexdigest()
                    require(state_sha==event['state_sha256'],'State hash mismatch')
                    pair=(state_sha,event['image_sha256'])
                    if ep in resets:require(pair==resets[ep],'Retry changed initial state/image')
                    resets[ep]=pair;states.add(state_sha)
            require(set(resets)==set(range(24))and requested==set(range(base,base+24)),'Incomplete technical reset records')
            for ep,pair in resets.items():
                if ep in reference:require(pair==reference[ep],f'Initial state/image pairing mismatch at configuration {ep}')
                else:reference[ep]=pair
            checked.append(dict(cell=name,rows=24,source_and_metadata_gate=True,built_parameters_gate=True,
                                session_reseed_gate=True,initial_state_image_pairing_gate=True,sessions=len(session_count),
                                summary_path=summary_path.relative_to(ROOT).as_posix()))
        except (ValueError,KeyError,FileNotFoundError)as exc:issues.append(dict(cell=name,issue=str(exc)))
    if len(frequencies)>1:issues.append(dict(cell='global',issue='Control/physics frequencies changed'))
    result=dict(created_utc=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                scope='Completed-cell technical interfaces only; no outcome aggregation, directional assessment or inference',
                completed_cells_checked=len(checked),passed=not issues,checks=checked,issues=issues,
                unique_initial_state_hashes=len(states),frequencies=[list(x)for x in sorted(frequencies)],
                frozen_analysis_unchanged=True,confirmatory_p_value_computed=False)
    out=HERE/'technical_prechecks';out.mkdir(exist_ok=True)
    path=out/f"precheck_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items()if k!='checks'},indent=2))
    print('report:',path)
    if issues:raise SystemExit(2)

if __name__=='__main__':main()
