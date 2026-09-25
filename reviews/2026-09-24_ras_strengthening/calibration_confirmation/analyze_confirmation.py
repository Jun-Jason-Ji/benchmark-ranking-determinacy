"""Analyse the frozen eight-block direction-repeatability study, or fail closed.

The confirmatory estimand is P(D_block < 0), not E[D_block]. No partial-design
p-value, sample-size adaptation, or reconstruction of missing audit data.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import sys
import numpy as np
from scipy import stats

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SEEDS=[431700100,557900200,683100300,809300400,947500500,1089700600,1231900700,1393100800]
POLICIES=['octo-small','octo-base']
CONDITIONS=['nominal','fitted']
ENV='PutSpoonOnTableClothInScene-v1'
N_CONFIG=24
ALPHA=.05
INPUTS={}

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):
    path=Path(path);data=path.read_bytes()
    INPUTS[path.relative_to(ROOT).as_posix()]={'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
    return data.decode('utf-8')
def json_file(path):return json.loads(read(path))
def json_lines(path):return [json.loads(s)for s in read(path).splitlines()if s.strip()]
def require(condition,message):
    if not condition:raise ValueError(message)

def check_finite(value):
    if isinstance(value,float):require(math.isfinite(value),'Nonfinite audited state')
    elif isinstance(value,dict):
        for v in value.values():check_finite(v)
    elif isinstance(value,list):
        for v in value:check_finite(v)

def validate_rows(rows,policy,condition,base):
    require(len(rows)==24,'A cell must contain exactly 24 completed records')
    require(sorted(r['episode_id']for r in rows)==list(range(24)),'Missing/duplicate configuration IDs')
    for r in rows:
        require(r['policy']==policy and r['env_id']==ENV and r['condition']==condition,'Episode scope mismatch')
        require(isinstance(r['success'],bool),'Success must be an explicit Boolean')
        require(r['steps']==60,'Unexpected outcome horizon')
        require(r['policy_seed']==base+r['episode_id'],'Wrong per-configuration seed')
    return {r['episode_id']:int(r['success'])for r in rows}

def primary_inference(block_numerators):
    require(len(block_numerators)==8,'Incomplete eight-block primary design')
    require(all(isinstance(v,int) and -48<=v<=48 for v in block_numerators),'Invalid exact block contrast numerator')
    k=sum(v<0 for v in block_numerators)
    p=float(stats.binom.sf(k-1,8,.5))
    lower=0. if k==0 else float(stats.beta.ppf(ALPHA,k,8-k+1))
    return dict(target='P(D_block < 0) under independent identically sampled seed blocks',
                null='P(D_block < 0) <= 0.5',alternative='P(D_block < 0) > 0.5',
                negative_blocks=k,nonnegative_blocks=8-k,zero_blocks=sum(v==0 for v in block_numerators),
                n_blocks=8,one_sided_exact_binomial_p=p,one_sided_exact_95_lower_bound=lower,
                reject_at_005=p<=ALPHA,zero_rule='Zeros count as nonnegative; no observations are discarded')

def secondary_inference(block_numerators):
    x=np.asarray(block_numerators,dtype=float)/N_CONFIG
    n=len(x);mean=float(x.mean());sd=float(x.std(ddof=1));se=sd/math.sqrt(n)
    model=dict(target='Mean block shift E[D_block]',mean=mean,sd=sd,se=se,df=n-1,
               scope='Secondary Student-t working model for independent approximately normal block differences')
    if se==0:
        model.update(interval_available=False,reason='Zero observed block variance; no empirical estimate of nonzero variance')
    else:
        r=float(stats.t.ppf(.975,n-1))*se
        model.update(interval_available=True,lower=max(-2.,mean-r),upper=min(2.,mean+r))
    # D is a difference of two policy gaps, so its support is [-2,2], width FOUR.
    radius=math.sqrt(8*math.log(2/ALPHA)/n)
    bounded=dict(target='Mean block shift E[D_block]',mean=mean,block_range=[-2,2],radius=radius,
                 lower=max(-2.,mean-radius),upper=min(2.,mean+radius),
                 scope='Secondary Hoeffding 95% interval; independent blocks, no Gaussian or within-block independence assumption')
    return dict(t_working_model=model,bounded_mean=bounded)

def main():
    analysis_freeze=json_file(HERE/'FROZEN_ANALYSIS.json')
    require(sha(Path(__file__))==analysis_freeze['analyzer_sha256'],'Analysis source changed after its freeze')
    frozen=json_file(HERE/'FROZEN_PLAN.json')
    require(frozen['seeds']==SEEDS and frozen['episodes']==768,'Unexpected frozen design')
    for rel,want in frozen['files'].items():
        require(sha(ROOT/rel)==want,f'Frozen source changed: {rel}')
        read(ROOT/rel)
    complete=json_file(HERE/'COMPLETE.json')
    require(complete.get('complete') is True,'Run did not complete')
    require(complete['frozen_plan_sha256']==sha(HERE/'FROZEN_PLAN.json'),'Completion belongs to a different freeze')
    # Import contains constants only; no evaluator is run.
    sys.path.insert(0,str(ROOT/'scripts'))
    import controller_sweep
    expected_nominal=controller_sweep.NOMINAL
    by_cell={};cells=[];physical_reference={};image_reference={};server_fingerprint={};frequency_reference=None
    for index,base in enumerate(SEEDS,1):
        for policy in POLICIES:
            for condition in CONDITIONS:
                directory=HERE/'data'/f'block_{index:02d}'/policy/ENV
                rows=json_lines(directory/f'{condition}.jsonl')
                outcomes=validate_rows(rows,policy,condition,base)
                meta=json_file(directory/f'{condition}_run_meta.json')
                summary=json_file(directory/f'{condition}_summary.json')
                args=meta['args'];variant=meta['variant_config']
                require(args['policy_name']==policy and args['env_id']==ENV and args['policy_seed_base']==base,'Metadata scope mismatch')
                require(args['conditions']==condition and args['episodes']==24 and args['episode_offset']==0,'Metadata cell inventory mismatch')
                require(variant['history']==2 and variant['ensemble'] is True and variant['exec_horizon']==1,'Policy configuration changed')
                eff=summary['conditions'][condition]['effective']
                ss,ds,delay=(1.,1.,0)if condition=='nominal'else(2.,.5,1)
                for key,factor,nominal_key in [('built_stiffness',ss,'arm_stiffness'),('built_damping',ds,'arm_damping'),('built_force_limit',1.,'arm_force_limit')]:
                    expected=np.asarray(expected_nominal[nominal_key])*factor
                    require(np.allclose(np.asarray(eff[key]),expected,rtol=2e-6,atol=1e-5),f'Built controller mismatch: {policy} {condition} {key}')
                require(eff['delay_steps']==delay and eff['horizon']==60,'Actual delay or horizon mismatch')
                require(eff['control_freq']>0 and eff['sim_freq']>=eff['control_freq'],'Invalid frequencies')
                frequency=(eff['control_freq'],eff['sim_freq'])
                if frequency_reference is None:frequency_reference=frequency
                else:require(frequency==frequency_reference,'Control/physics frequencies changed')
                require(eff['gripper_force_limit']==expected_nominal['gripper_force_limit'],'Gripper force changed')
                require(eff['obj_friction']==.5 and eff['density_scale']==1.,'Unplanned contact-parameter perturbation')
                require(summary['conditions'][condition]['episodes']==24 and summary['conditions'][condition]['successes']==sum(outcomes.values()),'Summary does not match raw outcomes')
                health=meta['policy_server']
                require(health['model']==policy and health.get('session_isolation') is True,'Wrong or unisolated policy server')
                fingerprint={k:health.get(k)for k in ['model','hf_id','jax','flax','tensorflow','numpy','python','action_mean','action_std','rotation_convention','policy_setups']}
                if policy in server_fingerprint:require(fingerprint==server_fingerprint[policy],'Policy server metadata drift')
                else:server_fingerprint[policy]=fingerprint
                audit=json_lines(directory/f'{condition}_audit.jsonl')
                require(any(e['kind']=='cell_complete'for e in audit),'Missing completed audit event')
                resets={}
                for event in audit:
                    if event['kind']=='cell_start':
                        require(event['time_utc']>=analysis_freeze['created_utc'],'Analysis was not frozen before the first cell started')
                        for rel,want in event['source_sha256'].items():require(sha(ROOT/rel)==want,f'Executed source differs: {rel}')
                    if event['kind']=='policy_reset':
                        seed=event['requested_seed'];response=event['response']
                        require(response.get('ok')and response.get('session')==event['session'],'Policy reset session mismatch')
                        require(response.get('rng_mode')=='reseed'and response.get('rng_seed')==seed,'Policy RNG lifecycle mismatch')
                        require(seed in range(base,base+24),'Unknown requested seed')
                    if event['kind']=='environment_reset':
                        ep=event['seed'];require(ep in range(24),'Unknown scene seed')
                        check_finite(event['state'])
                        encoded=json.dumps(event['state'],sort_keys=True).encode()
                        require(hashlib.sha256(encoded).hexdigest()==event['state_sha256'],'Corrupt state digest')
                        if ep in resets:require(resets[ep]==(event['state_sha256'],event['image_sha256']),'Technical retry changed initial state/image')
                        resets[ep]=(event['state_sha256'],event['image_sha256'])
                require(set(resets)==set(range(24)),'Missing initial-state audit')
                requested={e['requested_seed']for e in audit if e['kind']=='policy_reset'}
                require(requested==set(range(base,base+24)),'Missing policy reseed audit')
                for ep,(state_hash,image_hash)in resets.items():
                    if ep in physical_reference:require(state_hash==physical_reference[ep],f'Physical-state pairing failed: block{index} {policy} {condition} config{ep}')
                    else:physical_reference[ep]=state_hash
                    if ep in image_reference:require(image_hash==image_reference[ep],f'Initial-image pairing failed: block{index} {policy} {condition} config{ep}')
                    else:image_reference[ep]=image_hash
                by_cell[index,policy,condition]=outcomes
                cells.append(dict(block=index,seed_base=base,policy=policy,condition=condition,successes=sum(outcomes.values()),n=24,
                                  built_parameters=eff,configuration_state_digests={str(k):v[0]for k,v in resets.items()}))
    require(len(cells)==32,'Incomplete 32-cell design')
    require(len(set(physical_reference.values()))==24,'Configuration states not distinct')
    blocks=[];numerators=[]
    for b in range(1,9):
        totals={f'{policy}_{condition}':sum(by_cell[b,policy,condition].values())for policy in POLICIES for condition in CONDITIONS}
        nominal=totals['octo-small_nominal']-totals['octo-base_nominal']
        fitted=totals['octo-small_fitted']-totals['octo-base_fitted']
        diff=fitted-nominal;numerators.append(diff)
        blocks.append(dict(block=b,seed_base=SEEDS[b-1],success_totals=totals,denominator=24,
                           nominal_gap=nominal/24,fitted_gap=fitted/24,shift_numerator=diff,shift=diff/24))
    result=dict(status='complete',raw_rollouts=768,n_independent_blocks_assumed=8,configurations_per_block=24,
        primary=primary_inference(numerators),secondary=secondary_inference(numerators),blocks=blocks,cells=cells,
        integrity=dict(all_32_cells_complete=True,all_24_initial_states_and_images_match_across_policies_settings_blocks=True,
                       all_built_parameters_checked=True,all_policy_resets_verified=True,server_metadata_stable=True),
        scope='Independent identically sampled policy-seed blocks are assumed; within-block dependence is unrestricted. Fixed finite scene population, fixed pipelines/build, final-success horizon 60.',
        exclusions='Not a test of E[D]=0; not a six-setting envelope confirmation, real-world or cross-engine validation.',
        input_sha256=INPUTS,analysis_sha256=sha(Path(__file__)),frozen_analysis_sha256=sha(HERE/'FROZEN_ANALYSIS.json'))
    (HERE/'ANALYSIS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    p=result['primary'];secondary=result['secondary'];t=secondary['t_working_model'];h=secondary['bounded_mean']
    lines=['# Prospective spoon operating-point repeatability','',
        f"All 768 planned rollouts completed. Negative block shifts: {p['negative_blocks']}/8; zeros: {p['zero_blocks']}/8.",
        f"Prespecified one-sided exact binomial p = {p['one_sided_exact_binomial_p']:.8f}; one-sided 95% lower bound on P(D_block < 0) = {p['one_sided_exact_95_lower_bound']:.6f}.",
        'This tests directional repeatability across the specified seed-block sampling model, not a population mean shift.','',
        '| Block | Small nominal | Base nominal | Small fitted | Base fitted | Nominal gap | Fitted gap | Change |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for b in blocks:
        v=b['success_totals'];lines.append(f"| {b['block']} | {v['octo-small_nominal']}/24 | {v['octo-base_nominal']}/24 | {v['octo-small_fitted']}/24 | {v['octo-base_fitted']}/24 | {b['nominal_gap']:+.4f} | {b['fitted_gap']:+.4f} | {b['shift']:+.4f} |")
    lines+=['',f"Secondary mean change: {t['mean']:+.6f}."]
    if t['interval_available']:lines.append(f"Secondary t working-model 95% interval (7 df): [{t['lower']:+.6f}, {t['upper']:+.6f}].")
    else:lines.append('Secondary t interval unavailable: zero empirical block variance.')
    lines.append(f"Secondary distribution-free bounded-mean interval: [{h['lower']:+.6f}, {h['upper']:+.6f}], using D in [-2,2].")
    lines+=['','All initial states/images, parameter assignments, reseeding responses and source hashes passed the fixed integrity checks. Statistical independence of blocks remains an assumption; unique seed numbers do not prove it.','',result['exclusions']]
    (HERE/'ANALYSIS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (HERE/'ANALYSIS_STATUS.json').write_text(json.dumps({'status':'complete','primary_available':True})+'\n')
    print('\n'.join(lines[:7]))

if __name__=='__main__':
    try:main()
    except (ValueError,AssertionError,KeyError,FileNotFoundError)as exc:
        status={'status':'unavailable','primary_available':False,'reason':str(exc),'partial_p_value_computed':False}
        (HERE/'ANALYSIS_STATUS.json').write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(status),file=sys.stderr)
        raise SystemExit(2)
