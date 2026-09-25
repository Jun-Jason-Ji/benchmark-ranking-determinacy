"""Analyze the complete fixed secondary torque control, including shared baseline.

No partial or adaptive analysis. This file does not modify the V3 protocol.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import numpy as np
from scipy import stats

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
V3=HERE.parent/'calibration_confirmation_v3'
SEEDS=[431700100,557900200,683100300,809300400,947500500,1089700600,1231900700,1393100800]
POLICIES=['octo-small','octo-base']
ENV='PutSpoonOnTableClothInScene-v1'
PROTOCOL='SECONDARY-controlled-initialization-half-torque'
INPUTS={}

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def require(condition,message):
    if not condition:raise ValueError(message)
def read(path):
    data=Path(path).read_bytes();INPUTS[Path(path).relative_to(ROOT).as_posix()]={'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
    return data.decode('utf-8')
def jf(path):return json.loads(read(path))
def jl(path):return [json.loads(s)for s in read(path).splitlines()if s.strip()]

def sign_inference(numerators):
    require(len(numerators)==8,'Exactly eight complete blocks required')
    require(all(isinstance(x,int)and -48<=x<=48 for x in numerators),'Invalid exact contrast numerator')
    neg=sum(x<0 for x in numerators);pos=sum(x>0 for x in numerators)
    pneg=float(stats.binom.sf(neg-1,8,.5));ppos=float(stats.binom.sf(pos-1,8,.5))
    p=min(1.,2*min(pneg,ppos))
    return dict(target='One strict direction has probability greater than one half',
        null='P(T < 0) <= 0.5 and P(T > 0) <= 0.5',n_blocks=8,negative_blocks=neg,
        positive_blocks=pos,zero_blocks=8-neg-pos,negative_one_sided_p=pneg,positive_one_sided_p=ppos,
        two_sided_p=p,reject_at_005=p<=.05,
        zero_rule='Zeros match neither direction and remain among all eight blocks',
        scope='Independent identically sampled seed blocks; not a mean-effect or equivalence test')

def holm_two(pvalues):
    require(len(pvalues)==2 and all(0<=p<=1 for p in pvalues),'Two valid p values required')
    order=sorted(range(2),key=lambda k:pvalues[k]);out=[None,None];running=0.
    for rank,k in enumerate(order):
        running=max(running,(2-rank)*pvalues[k]);out[k]=min(1.,running)
    return out

def mean_inference(numerators):
    require(len(numerators)==8,'Exactly eight complete blocks required')
    x=np.asarray(numerators,dtype=float)/24;mean=float(x.mean());sd=float(x.std(ddof=1));se=sd/math.sqrt(8)
    t=dict(mean=mean,sd=sd,se=se,df=7,interval_available=se>0,
        scope='Secondary independent approximately normal block-difference working model')
    if se>0:
        radius=float(stats.t.ppf(.975,7))*se;t.update(lower=max(-2.,mean-radius),upper=min(2.,mean+radius))
    else:t['reason']='Zero observed variance does not establish zero population variance'
    radius=math.sqrt(math.log(40))
    h=dict(mean=mean,lower=max(-2.,mean-radius),upper=min(2.,mean+radius),radius=radius,
        support=[-2,2],scope='Secondary independent-block Hoeffding 95% interval; unrestricted within-block dependence')
    return dict(t_working_model=t,bounded_mean=h)

def main():
    af=jf(HERE/'FROZEN_ANALYSIS.json');require(sha(__file__)==af['analyzer_sha256'],'Frozen analyzer changed')
    freeze=jf(HERE/'FROZEN_PLAN.json');hyp=jf(HERE/'HYPOTHESIS_FREEZE.json')
    require(freeze['protocol_version']==PROTOCOL and freeze['episodes']==384 and freeze['seeds']==SEEDS,'Frozen design mismatch')
    require(freeze['reset_validation_passed']is True,'Missing passed technical validation')
    require(sha(HERE/'PLAN.md')==hyp['plan_sha256']and hyp['v3_outcomes_analyzed']is False,'Hypothesis freeze changed')
    for rel,digest in freeze['files'].items():require(sha(ROOT/rel)==digest,f'Frozen input changed: {rel}');read(ROOT/rel)
    complete=jf(HERE/'COMPLETE.json');require(complete['complete']is True and complete['frozen_plan_sha256']==sha(HERE/'FROZEN_PLAN.json'),'Secondary collection incomplete or mismatched')
    v3complete=jf(V3/'COMPLETE.json');require(v3complete['complete']is True,'V3 baseline incomplete')
    require(sha(V3/'FROZEN_PLAN.json')==hyp['v3_frozen_plan_sha256'],'V3 freeze changed')
    # Run its existing frozen, fail-closed integrity/analysis code only now, after both collections complete.
    spec=importlib.util.spec_from_file_location('frozen_v3',V3/'analyze_confirmation.py')
    v3=importlib.util.module_from_spec(spec);spec.loader.exec_module(v3);v3.main()
    baseline=jf(V3/'ANALYSIS.json');require(baseline['status']=='complete'and baseline['raw_rollouts']==768,'Invalid V3 analysis')
    sys.path.insert(0,str(ROOT/'scripts'));import controller_sweep
    nominal=controller_sweep.NOMINAL;by_cell={};cells=[]
    expected_params={key:np.asarray(nominal[nkey])*factor for key,factor,nkey in [('stiffness',1.,'arm_stiffness'),('damping',1.,'arm_damping'),('force_limit',.5,'arm_force_limit')]}
    fingerprint_keys=['model','hf_id','jax','flax','tensorflow','numpy','python','action_mean','action_std','rotation_convention','policy_setups']
    for block,seed in enumerate(SEEDS,1):
        for policy in POLICIES:
            directory=HERE/'data'/f'block_{block:02d}'/policy/ENV
            bd=V3/'data'/f'block_{block:02d}'/policy/ENV
            rows=jl(directory/'forcehalf.jsonl');outcomes=v3.validate_rows(rows,policy,'forcehalf',seed)
            require(all(r.get('protocol_version')==PROTOCOL for r in rows),'Record protocol version mismatch')
            meta=jf(directory/'forcehalf_run_meta.json');summary=jf(directory/'forcehalf_summary.json')
            require(meta.get('protocol_version')==PROTOCOL,'Metadata protocol mismatch')
            args=meta['args'];variant=meta['variant_config'];eff=summary['conditions']['forcehalf']['effective']
            require(args['conditions']=='forcehalf'and args['policy_name']==policy and args['env_id']==ENV and args['policy_seed_base']==seed,'Metadata scope mismatch')
            require(args['episodes']==24 and args['episode_offset']==0,'Metadata inventory mismatch')
            require(variant['history']==2 and variant['ensemble']is True and variant['exec_horizon']==1,'Policy mode mismatch')
            for key,expected in expected_params.items():require(np.allclose(eff['built_'+key],expected,rtol=2e-6,atol=1e-5),'Built force/gain mismatch')
            require(eff['delay_steps']==0 and eff['horizon']==60 and eff['control_freq']==5 and eff['sim_freq']==500,'Timing mismatch')
            require(eff['gripper_force_limit']==nominal['gripper_force_limit']and eff['obj_friction']==.5 and eff['density_scale']==1.,'Unplanned gripper/contact change')
            require(summary['conditions']['forcehalf']['episodes']==24 and summary['conditions']['forcehalf']['successes']==sum(outcomes.values()),'Raw/summary mismatch')
            server=meta['policy_server'];base_server=jf(bd/'nominal_run_meta.json')['policy_server']
            require(server['model']==policy and server.get('session_isolation')is True,'Wrong/unisolated server')
            require({k:server.get(k)for k in fingerprint_keys}=={k:base_server.get(k)for k in fingerprint_keys},'Server differs from shared baseline')
            baseline_resets={e['seed']:e for e in jl(bd/'nominal_audit.jsonl')if e['kind']=='environment_reset'}
            audit=jl(directory/'forcehalf_audit.jsonl');require(any(e['kind']=='cell_complete'for e in audit),'Missing complete audit')
            resets={};requested=set()
            for event in audit:
                if event['kind']=='cell_start':
                    require(event['time_utc']>=af['created_utc'],'Analysis freeze postdates data collection')
                    for rel,digest in event['source_sha256'].items():require(sha(ROOT/rel)==digest,'Executed source changed')
                elif event['kind']=='policy_reset':
                    s=event['requested_seed'];response=event['response'];requested.add(s)
                    require(response.get('ok')and response.get('session')==event['session'],'Session reset mismatch')
                    require(response.get('rng_mode')=='reseed'and response.get('rng_seed')==s and s in range(seed,seed+24),'Policy seed mismatch')
                elif event['kind']=='environment_reset':
                    ep=event['seed'];require(ep in range(24),'Unknown configuration')
                    require(event.get('nominal_settling_completed_before_condition')is True and event.get('physics_steps_after_condition')==0,'Condition changed scene settling')
                    require(event.get('active_controller_references_new_scene')is True,'Stale controller')
                    for key,expected in expected_params.items():
                        require(np.allclose(event['built_controller'][key],expected,rtol=2e-6,atol=1e-5),'Reset config mismatch')
                        require(np.allclose(event['actual_joints'][key],expected,rtol=2e-6,atol=1e-5),'Physical drive mismatch')
                    v3.check_finite(event['state']);digest=hashlib.sha256(json.dumps(event['state'],sort_keys=True).encode()).hexdigest()
                    require(digest==event['state_sha256'],'Corrupt state hash')
                    pair=(digest,event['image_sha256']);reference=baseline_resets[ep]
                    require(pair==(reference['state_sha256'],reference['image_sha256']),'Initial state/image differs from paired V3 baseline')
                    require(event['gripper']==reference['gripper']and event['object_contact']==reference['object_contact'],'Gripper/contact/mass differs from shared baseline')
                    require(event['actual_joints']['friction']==reference['actual_joints']['friction'],'Arm joint friction differs from shared baseline')
                    if ep in resets:require(resets[ep]==pair,'Retry changed state/image')
                    resets[ep]=pair
            require(set(resets)==set(range(24))and requested==set(range(seed,seed+24)),'Incomplete technical reset audit')
            closed=[e for e in audit if e['kind']=='episode_closed']
            require({e['episode_id']for e in closed}==set(range(24)),'Missing closure')
            require(all(e.get('closed_scene_and_agent_cleared')is True and e.get('active_parameters_unchanged')is True for e in closed),'Incorrect lifecycle/parameter preservation')
            by_cell[block,policy]=sum(outcomes.values());cells.append(dict(block=block,policy=policy,condition='forcehalf',successes=sum(outcomes.values()),n=24))
    require(len(cells)==16,'Incomplete fixed secondary design')
    blocks=[];numerators=[]
    for b in baseline['blocks']:
        index=b['block'];totals=b['success_totals']
        nominal_gap=totals['octo-small_nominal']-totals['octo-base_nominal']
        small=by_cell[index,'octo-small'];base=by_cell[index,'octo-base'];num=small-base-nominal_gap;numerators.append(num)
        blocks.append(dict(block=index,seed_base=SEEDS[index-1],small_nominal=totals['octo-small_nominal'],base_nominal=totals['octo-base_nominal'],small_forcehalf=small,base_forcehalf=base,denominator=24,shift_numerator=num,shift=num/24))
    sign=sign_inference(numerators);means=mean_inference(numerators)
    original=baseline['primary']['one_sided_exact_binomial_p'];adjusted=holm_two([original,sign['two_sided_p']])
    result=dict(status='complete',additional_unique_rollouts=384,shared_v3_nominal_rollouts=384,joint_unique_rollouts=1152,
        secondary_sign_test=sign,mean_sensitivity=means,blocks=blocks,cells=cells,
        two_claim_family=dict(names=['V3 one-sided direction repeatability','Secondary two-sided torque direction repeatability'],raw_p=[original,sign['two_sided_p']],holm_adjusted_p=adjusted,reject=[p<=.05 for p in adjusted],baseline_shared=True,independence_between_tests_required=False),
        integrity=dict(complete_16_cells=True,all_states_images_match_shared_baseline=True,all_parameters_verified=True,all_reseeds_and_closures_verified=True),
        scope='Fixed finite spoon configurations, fixed build/policy pipelines, final60 and canonical nominal-settled initialization. Independent identically sampled seed blocks assumed. Secondary majority-direction test is not a mean test or equivalence test. Historical effects remain protocol contrasts.',
        input_sha256=INPUTS,v3_input_sha256=baseline['input_sha256'],analyzer_sha256=sha(__file__))
    (HERE/'ANALYSIS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    lines=['# Secondary prospective half-torque control','',f"All 384 additional rollouts complete; 384 V3 nominal rollouts reused. Joint unique count: 1,152.",
        f"Block signs: {sign['negative_blocks']} negative, {sign['positive_blocks']} positive, {sign['zero_blocks']} zero. Direction-adjusted two-sided p={sign['two_sided_p']:.8f}.",
        f"Two-claim Holm adjusted p: V3={adjusted[0]:.8f}; torque={adjusted[1]:.8f}.",'',
        '| Block | Small nominal | Base nominal | Small half torque | Base half torque | Shift |','|---|---:|---:|---:|---:|---:|']
    for b in blocks:lines.append(f"| {b['block']} | {b['small_nominal']} | {b['base_nominal']} | {b['small_forcehalf']} | {b['base_forcehalf']} | {b['shift']:+.6f} |")
    t=means['t_working_model'];h=means['bounded_mean'];lines+=['',f"Mean shift {t['mean']:+.6f}."]
    if t['interval_available']:lines.append(f"Secondary t-model 95% interval [{t['lower']:+.6f}, {t['upper']:+.6f}] (7 df).")
    else:lines.append('Secondary t interval unavailable: zero empirical variance.')
    lines+=[f"Independent-block bounded-mean interval [{h['lower']:+.6f}, {h['upper']:+.6f}].",'',result['scope']]
    (HERE/'ANALYSIS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (HERE/'ANALYSIS_STATUS.json').write_text(json.dumps({'status':'complete','secondary_available':True})+'\n')
    print('\n'.join(lines[:6]))

if __name__=='__main__':
    try:main()
    except (ValueError,AssertionError,KeyError,FileNotFoundError)as exc:
        status=dict(status='unavailable',secondary_available=False,reason=str(exc),partial_p_value_computed=False)
        (HERE/'ANALYSIS_STATUS.json').write_text(json.dumps(status,indent=2)+'\n');print(json.dumps(status),file=sys.stderr);raise SystemExit(2)
