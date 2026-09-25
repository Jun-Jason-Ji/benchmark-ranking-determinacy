"""Independent completed-data numerical and pairing review; no simulator runs."""
from pathlib import Path
from fractions import Fraction
import hashlib,json,math,statistics,sys
import numpy as np
import scipy
from scipy.stats import t
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
V3=HERE.parent/'calibration_confirmation_v3'
SEEDS=[431700100,557900200,683100300,809300400,947500500,1089700600,1231900700,1393100800]
ENV='PutSpoonOnTableClothInScene-v1'
POLICIES=['octo-small','octo-base']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def same(a,b):return math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-10)
def jsonlines(p):return [json.loads(x)for x in p.read_text().splitlines()if x.strip()]

def main():
    for folder in [V3,HERE]:
        complete=json.loads((folder/'COMPLETE.json').read_text());assert complete['complete']is True
        assert complete['frozen_plan_sha256']==sha(folder/'FROZEN_PLAN.json')
        for rel,digest in json.loads((folder/'FROZEN_PLAN.json').read_text())['files'].items():assert sha(ROOT/rel)==digest,rel
    published=json.loads((HERE/'ANALYSIS.json').read_text());primary=json.loads((V3/'ANALYSIS.json').read_text())
    assert published['status']==primary['status']=='complete'
    totals={};raw_hashes={};technical_hashes={};episode_keys=set();technical=0;cells=[]
    for b,seed in enumerate(SEEDS,1):
      for policy in POLICIES:
        baseline_audit=V3/'data'/f'block_{b:02d}'/policy/ENV/'nominal_audit.jsonl'
        nominal_reset={e['episode_id']:e for e in jsonlines(baseline_audit)if e['kind']=='environment_reset'}
        assert set(nominal_reset)==set(range(24))
        technical_hashes[baseline_audit.relative_to(ROOT).as_posix()]=sha(baseline_audit)
        for condition,folder in [('nominal',V3),('fitted',V3),('forcehalf',HERE)]:
            directory=folder/'data'/f'block_{b:02d}'/policy/ENV
            path=directory/(condition+'.jsonl');rows=jsonlines(path)
            raw_hashes[path.relative_to(ROOT).as_posix()]=sha(path)
            assert len(rows)==24 and sorted(r['episode_id']for r in rows)==list(range(24))
            for row in rows:
                assert row['policy']==policy and row['condition']==condition and row['env_id']==ENV
                assert row['steps']==60 and row['policy_seed']==seed+row['episode_id'] and type(row['success'])is bool
                key=(b,policy,condition,row['episode_id']);assert key not in episode_keys;episode_keys.add(key)
            totals[b,policy,condition]=sum(int(r['success'])for r in rows)
            cells.append(dict(block=b,policy=policy,condition=condition,successes=totals[b,policy,condition],n=24))
            if condition!='forcehalf':continue
            meta=json.loads((directory/'forcehalf_run_meta.json').read_text())
            refmeta=json.loads((V3/'data'/f'block_{b:02d}'/policy/ENV/'nominal_run_meta.json').read_text())
            for key in ['model','hf_id','jax','flax','tensorflow','numpy','python','action_mean','action_std','rotation_convention','policy_setups']:
                assert meta['policy_server'].get(key)==refmeta['policy_server'].get(key)
            audit_path=directory/'forcehalf_audit.jsonl';events=jsonlines(audit_path)
            technical_hashes[audit_path.relative_to(ROOT).as_posix()]=sha(audit_path)
            resets={};requested=set();closed=set()
            for event in events:
                if event['kind']=='cell_start':
                    assert event['frozen_plan_sha256']==sha(HERE/'FROZEN_PLAN.json')
                    for rel,digest in event['source_sha256'].items():assert sha(ROOT/rel)==digest
                if event['kind']=='policy_reset':
                    requested.add(event['requested_seed']);response=event['response']
                    assert response['ok']and response['session']==event['session']
                    assert response['rng_mode']=='reseed'and response['rng_seed']==event['requested_seed']
                if event['kind']=='episode_closed':
                    assert event['closed_scene_and_agent_cleared']and event['active_parameters_unchanged']
                    closed.add(event['episode_id'])
                if event['kind']!='environment_reset':continue
                ep=event['episode_id'];ref=nominal_reset[ep]
                assert event['state']==ref['state']
                assert event['state_sha256']==ref['state_sha256']and event['image_sha256']==ref['image_sha256']
                assert hashlib.sha256(json.dumps(event['state'],sort_keys=True).encode()).hexdigest()==event['state_sha256']
                assert event['gripper']==ref['gripper']and event['object_contact']==ref['object_contact']
                assert event['actual_joints']['friction']==ref['actual_joints']['friction']
                assert event['delay_steps']==0 and event['force_limit_scale']==.5
                assert event['physics_steps_after_condition']==0 and event['nominal_settling_completed_before_condition']
                assert event['active_controller_references_new_scene']
                for key in ['stiffness','damping','force_limit']:
                    expected=np.array(ref['built_controller'][key])*(.5 if key=='force_limit'else 1.)
                    assert np.allclose(event['built_controller'][key],expected,rtol=2e-6,atol=1e-5)
                    assert np.allclose(event['actual_joints'][key],expected,rtol=2e-6,atol=1e-5)
                if ep in resets:assert resets[ep]==event['state_sha256']
                resets[ep]=event['state_sha256']
            assert set(resets)==closed==set(range(24))and requested==set(range(seed,seed+24))
            assert any(e['kind']=='cell_complete'for e in events);technical+=24
    assert len(episode_keys)==1152 and len(cells)==48 and technical==384
    blocks=[];nums=[];v3nums=[]
    for b in range(1,9):
        counts={f'{p}_{c}':totals[b,p,c]for p in POLICIES for c in ['nominal','fitted','forcehalf']}
        gap=lambda c:counts['octo-small_'+c]-counts['octo-base_'+c]
        num=gap('forcehalf')-gap('nominal');v3num=gap('fitted')-gap('nominal');nums.append(num);v3nums.append(v3num)
        assert published['blocks'][b-1]['shift_numerator']==num
        assert primary['blocks'][b-1]['shift_numerator']==v3num
        blocks.append(dict(block=b,counts=counts,torque_shift_numerator=num,v3_shift_numerator=v3num,denominator=24))
    neg=sum(x<0 for x in nums);pos=sum(x>0 for x in nums);zeros=sum(x==0 for x in nums)
    tail=lambda k:Fraction(sum(math.comb(8,j)for j in range(k,9)),256)
    torque_p=min(Fraction(1),2*min(tail(neg),tail(pos)));v3_p=tail(sum(x<0 for x in v3nums))
    pvals=[v3_p,torque_p];order=sorted(range(2),key=lambda k:pvals[k]);adjusted=[None,None];running=Fraction(0)
    for rank,k in enumerate(order):running=max(running,(2-rank)*pvals[k]);adjusted[k]=min(Fraction(1),running)
    exactmean=sum((Fraction(x,24)for x in nums),Fraction())/8
    x=[num/24 for num in nums];sd=statistics.stdev(x);se=sd/math.sqrt(8);r=float(t.ppf(.975,7))*se
    ti=[max(-2,float(exactmean)-r),min(2,float(exactmean)+r)]
    hr=math.sqrt(16/(2*8)*math.log(40));hi=[max(-2,float(exactmean)-hr),min(2,float(exactmean)+hr)]
    sign=published['secondary_sign_test'];tm=published['mean_sensitivity']['t_working_model'];hm=published['mean_sensitivity']['bounded_mean']
    assert [neg,pos,zeros]==[sign['negative_blocks'],sign['positive_blocks'],sign['zero_blocks']]
    assert float(torque_p)==sign['two_sided_p']
    assert same(float(exactmean),tm['mean'])and same(sd,tm['sd'])and same(se,tm['se'])and tm['df']==7
    assert all(same(tm[k],v)for k,v in zip(['lower','upper'],ti))
    assert all(same(hm[k],v)for k,v in zip(['lower','upper'],hi))
    assert list(map(float,adjusted))==published['two_claim_family']['holm_adjusted_p']
    assert published['two_claim_family']['reject']==[False,False]
    report=dict(status='passed',total_unique_rollouts=1152,new_torque_rollouts=384,shared_nominal_rollouts=384,
        raw_cells_checked=48,torque_episodes_technically_rechecked=technical,blocks=blocks,cells=cells,
        torque_numerators=nums,v3_numerators=v3nums,torque_signs=dict(negative=neg,positive=pos,zero=zeros),
        exact_torque_p=str(torque_p),two_sided_torque_p=float(torque_p),exact_mean_fraction=str(exactmean),
        mean=float(exactmean),t_df=7,t95=ti,bounded95=hi,
        joint_family=dict(raw_p=list(map(float,pvals)),holm_adjusted_p=list(map(float,adjusted)),reject=[False,False]),
        all_reported_arithmetic_matches=True,all_paired_states_images_and_declared_parameters_match=True,
        frozen_sources_unchanged=True,comparison_tolerance=dict(absolute=1e-10,relative=1e-9,integer_counts='exact'),
        interpretation='Neither directional claim passes the planned two-test Holm family. Torque non-rejection does not demonstrate equivalence or invariance. V3 original unadjusted direction result and secondary mean intervals must keep their distinct scope.',
        independent_runtime=dict(python=sys.version,scipy=scipy.__version__),raw_sha256=raw_hashes,technical_sha256=technical_hashes,
        staged_manuscript_sha256={p.name:sha(p)for p in sorted((HERE/'MANUSCRIPT_INSERTS').glob('*.tex'))},
        analysis_sha256=sha(HERE/'ANALYSIS.json'),v3_analysis_sha256=sha(V3/'ANALYSIS.json'),independent_script_sha256=sha(Path(__file__)))
    (HERE/'TORQUE_FINAL_NUMERICAL_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n')
    lines=['# Final independent numerical and technical review','',
        'Passed: all 48 complete cells (1,152 unique rollouts) were independently counted. The 384 new half-torque episodes were individually checked against their shared V3 nominal initial state/image, actual/configured parameters, gripper/contact/mass/friction, policy reseeding and clean lifecycle records. Frozen source hashes agree.',
        '',f'Torque block numerators: {nums}, each divided by 24. There are {neg} negative, {pos} positive and {zeros} zero shifts. Exact direction-adjusted two-sided p = {torque_p}.',
        f'Mean torque shift = {exactmean} = {float(exactmean):+.9f}; secondary t-model 95% interval = [{ti[0]:+.9f}, {ti[1]:+.9f}] (7 df); independent bounded-mean interval = [{hi[0]:+.9f}, {hi[1]:+.9f}].',
        f'Joint Holm-adjusted p values: V3={float(adjusted[0]):.8f}, torque={float(adjusted[1]):.8f}. Neither directional claim passes the planned two-test family at 0.05.',
        '', '| Block | Nominal S/B | Fitted S/B | Half torque S/B | Fitted numerator | Torque numerator |',
        '|---|---:|---:|---:|---:|---:|']
    for b in blocks:
        c=b['counts'];pair=lambda name:f"{c['octo-small_'+name]}/{c['octo-base_'+name]}"
        lines.append(f"| {b['block']} | {pair('nominal')} | {pair('fitted')} | {pair('forcehalf')} | {b['v3_shift_numerator']}/24 | {b['torque_shift_numerator']}/24 |")
    lines+=['','## Interpretation','',
        'Do not state that the controlled studies confirm either directional claim after joint correction. V3 retains its original unadjusted p=0.03515625, but its joint adjusted p is 0.0703125. Report both with their explicitly distinct scope; do not select the unadjusted result after seeing the secondary result.',
        'The two small negative torque contrasts and six zeros do not establish equivalence, parameter invariance, or inactive torque saturation. The secondary t interval and the much wider bounded-mean interval include zero. There was no prespecified equivalence margin or equivalence test.',
        'These are conditional simulation-pipeline comparisons on one fixed task and 24 fixed scenes, under an independent identically sampled seed-block working model. Shared nominal data are counted once. The controls do not validate a historical six-setting envelope, isolate the historical reset-confounded effect, or establish real-world/cross-engine policy rankings.',
        '', '## Staged manuscript check','',
        'The staged combined count table, eight signs, denominators, three-decimal changes and interval values agree with the independently recounted data. Its table note correctly identifies 24 as the per-policy denominator and explains baseline sharing. The narrative correctly states that neither claim passes the two-test family and that torque non-rejection is not equivalence.',
        'One prose cleanup is advisable: replace the awkward phrase "negative in 7 of eight blocks, including 0 zero changes among the remaining blocks" with "negative in seven blocks and positive in one". This is stylistic and changes no scientific claim. No frozen source or manuscript file was edited during this review.']
    (HERE/'TORQUE_FINAL_NUMERICAL_REVIEW.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k]for k in ['status','torque_numerators','torque_signs','two_sided_torque_p','mean','t95','bounded95','joint_family']},indent=2))

if __name__=='__main__':main()
