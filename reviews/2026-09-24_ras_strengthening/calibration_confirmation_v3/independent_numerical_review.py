"""Independent arithmetic audit of completed V3 only; never reads torque data."""
from pathlib import Path
from fractions import Fraction
import hashlib,json,math,statistics,sys
import scipy
from scipy.stats import beta,t

HERE=Path(__file__).resolve().parent
SEEDS=[431700100,557900200,683100300,809300400,947500500,1089700600,1231900700,1393100800]
ENV='PutSpoonOnTableClothInScene-v1'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def same(a,b):return math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-10)

def main():
    completed=json.loads((HERE/'COMPLETE.json').read_text())
    freeze=json.loads((HERE/'FROZEN_PLAN.json').read_text())
    assert completed['complete']is True and completed['frozen_plan_sha256']==sha(HERE/'FROZEN_PLAN.json')
    assert freeze['episodes']==768 and freeze['seeds']==SEEDS
    frozen_result=json.loads((HERE/'ANALYSIS.json').read_text())
    assert frozen_result['status']=='complete'
    hashes={};cells=[];blocks=[];nums=[];total=0
    for b,seed in enumerate(SEEDS,1):
        counts={}
        for policy in ['octo-small','octo-base']:
            for condition in ['nominal','fitted']:
                path=HERE/'data'/f'block_{b:02d}'/policy/ENV/f'{condition}.jsonl'
                data=path.read_bytes();hashes[path.relative_to(HERE).as_posix()]=hashlib.sha256(data).hexdigest()
                rows=[json.loads(x)for x in data.decode().splitlines()if x.strip()]
                assert len(rows)==24 and sorted(r['episode_id']for r in rows)==list(range(24))
                for r in rows:
                    assert r['policy']==policy and r['condition']==condition and r['env_id']==ENV
                    assert r['policy_seed']==seed+r['episode_id'] and r['steps']==60
                    assert type(r['success'])is bool and r['protocol_version']=='V3-controlled-initialization'
                k=sum(int(r['success'])for r in rows);counts[policy+'_'+condition]=k;total+=len(rows)
                cells.append(dict(block=b,policy=policy,condition=condition,successes=k,n=24))
        nominal=counts['octo-small_nominal']-counts['octo-base_nominal']
        fitted=counts['octo-small_fitted']-counts['octo-base_fitted']
        num=fitted-nominal;nums.append(num)
        original=frozen_result['blocks'][b-1]
        assert original['block']==b and original['success_totals']==counts and original['shift_numerator']==num
        assert same(original['shift'],num/24)
        blocks.append(dict(block=b,counts=counts,nominal_gap_numerator=nominal,fitted_gap_numerator=fitted,
                           shift_numerator=num,denominator=24,shift=num/24))
    assert total==768 and len(cells)==32
    negative=sum(n<0 for n in nums);positive=sum(n>0 for n in nums);zero=sum(n==0 for n in nums)
    # Combinatorial tail is independent of the original analyzer's scipy.binom implementation.
    p_fraction=Fraction(sum(math.comb(8,k)for k in range(negative,9)),256)
    lower=float(beta.ppf(.05,negative,9-negative))if negative else 0.
    exact_mean=sum((Fraction(n,24)for n in nums),Fraction())/8
    shifts=[n/24 for n in nums];sd=statistics.stdev(shifts);se=sd/math.sqrt(8)
    t_radius=float(t.ppf(.975,7))*se
    t_interval=[max(-2.,float(exact_mean)-t_radius),min(2.,float(exact_mean)+t_radius)]
    h_radius=math.sqrt((4.**2)/(2*8)*math.log(2/.05))
    h_interval=[max(-2.,float(exact_mean)-h_radius),min(2.,float(exact_mean)+h_radius)]
    primary=frozen_result['primary'];tm=frozen_result['secondary']['t_working_model'];hm=frozen_result['secondary']['bounded_mean']
    assert primary['negative_blocks']==negative and primary['zero_blocks']==zero
    assert same(primary['one_sided_exact_binomial_p'],float(p_fraction))
    assert same(primary['one_sided_exact_95_lower_bound'],lower)
    assert same(tm['mean'],float(exact_mean))and same(tm['sd'],sd)and same(tm['se'],se)and tm['df']==7
    assert all(same(tm[k],v)for k,v in zip(['lower','upper'],t_interval))
    assert same(hm['radius'],h_radius)and all(same(hm[k],v)for k,v in zip(['lower','upper'],h_interval))
    plan=(HERE/'PLAN.md').read_text()
    assert 'P(D_b < 0)'in plan or 'P(D_block < 0)'in plan or 'P(D < 0)'in plan
    report=dict(status='passed',scope='Completed V3 only; no torque outcome access',
        raw_rollouts=total,complete_cells=len(cells),blocks=blocks,cells=cells,
        exact_shift_numerators=nums,negative_blocks=negative,positive_blocks=positive,zero_blocks=zero,
        primary=dict(target='P(D_block < 0) > 0.5',one_sided_p=float(p_fraction),
            exact_p_fraction=str(p_fraction),one_sided_95_lower_bound=lower,unadjusted_reject_at_005=float(p_fraction)<=.05),
        secondary=dict(exact_mean_fraction=str(exact_mean),mean=float(exact_mean),sd=sd,se=se,
            t_df=7,t_95_interval=t_interval,hoeffding_radius=h_radius,hoeffding_95_interval=h_interval),
        joint_holm_status='Pending completion and frozen analysis of the separate secondary torque study',
        interpretation='Majority-direction repeatability under independent identically sampled seed blocks. The t interval concerns the mean under its separate working model; the bounded mean interval includes zero. No historical causal effect, rank reversal, full six-setting envelope, real-world or cross-engine validation is established.',
        all_frozen_report_arithmetic_matches=True,torque_outcomes_read=False,
        comparison_tolerance=dict(absolute=1e-10,relative=1e-9,integer_counts='exact'),
        runtime=dict(python=sys.version,scipy=scipy.__version__),
        t_endpoint_max_absolute_difference=max(abs(tm[k]-v)for k,v in zip(['lower','upper'],t_interval)),
        input_sha256=hashes,completed_sha256=sha(HERE/'COMPLETE.json'),plan_sha256=sha(HERE/'PLAN.md'),
        frozen_plan_sha256=sha(HERE/'FROZEN_PLAN.json'),analyzer_output_sha256=sha(HERE/'ANALYSIS.json'),
        independent_script_sha256=sha(Path(__file__)))
    (HERE/'V3_FINAL_NUMERICAL_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n')
    lines=['# Independent final numerical review of V3','',
        'The completed 768 raw outcomes in 32 cells reproduce every count and statistic in the frozen analysis. This review imports no original analyzer functions and reads no partial torque data.',
        'Integer counts and contrast numerators match exactly. Floating computations are compared with absolute tolerance 1e-10 and relative tolerance 1e-9; the independent t endpoints differ from the archived values by only about 3e-11, without changing any reported digit or conclusion.',
        '',f'Exact fitted-minus-nominal Small-minus-Base gap-shift numerators (denominator 24): {nums}.',
        f'Signs: {negative} negative, {positive} positive, {zero} zero. The prespecified one-sided binomial tail is {p_fraction} = {float(p_fraction):.8f}. The one-sided 95% lower bound on the negative-shift probability is {lower:.9f}.',
        f'The exact average shift is {exact_mean} = {float(exact_mean):+.9f}. The secondary t interval, using 7 df, is [{t_interval[0]:+.9f}, {t_interval[1]:+.9f}]. The independent bounded-block interval is [{h_interval[0]:+.9f}, {h_interval[1]:+.9f}].',
        '', '| Block | Small nominal | Base nominal | Small fitted | Base fitted | Exact shift |',
        '|---|---:|---:|---:|---:|---:|']
    for b in blocks:
        c=b['counts'];lines.append(f"| {b['block']} | {c['octo-small_nominal']} | {c['octo-base_nominal']} | {c['octo-small_fitted']} | {c['octo-base_fitted']} | {b['shift_numerator']}/24 |")
    lines+=['','## Interpretation and target consistency','',
        'The plan and frozen analyzer retain the originally specified one-sided direction target. No mean-effect test, post-hoc two-sided replacement, or configuration-level independence assumption was substituted. Seven of eight negative blocks support the prespecified majority-direction claim at unadjusted 0.05 under the stated independent, identically sampled seed-block model. Distinct seeds do not empirically prove this model.',
        'The negative mean and t-model interval are separate, model-dependent summaries. The bounded mean interval includes zero, so these results do not establish a distribution-free negative mean effect. The policy gaps themselves need not reverse sign when their difference decreases.',
        'The joint two-claim Holm result remains pending the complete secondary torque experiment. The V3 value above is the original unadjusted p value and must not yet be labelled the final two-claim family decision. The secondary study was frozen and launched before V3 aggregation; this review does not inspect its partial results or make any adaptive continuation decision.',
        'The result applies to the corrected nominal-settled initialization, eight seed blocks, two fixed pipelines, one task, 24 fixed configurations and final success at step 60. It does not retroactively isolate the cause of historical unmatched-reset effects, establish a six-setting envelope, identify torque saturation, or validate real-world/cross-engine performance.']
    (HERE/'V3_FINAL_NUMERICAL_REVIEW.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items()if k in ['status','exact_shift_numerators','primary','secondary','joint_holm_status']},indent=2))

if __name__=='__main__':main()
