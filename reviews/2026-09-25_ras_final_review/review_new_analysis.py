"""Read-only independent audit of new descriptive analyses; writes only review outputs."""
from pathlib import Path
import hashlib,json,math,statistics
import numpy as np

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
A=ROOT/'reviews/2026-09-24_ras_strengthening'
TOR=A/'calibration_torque_control';V3=A/'calibration_confirmation_v3'
checks={};inputs={}
def load(p):
    raw=p.read_bytes();inputs[p.relative_to(ROOT).as_posix()]=hashlib.sha256(raw).hexdigest();return json.loads(raw)
def lines(p):
    raw=p.read_bytes();inputs[p.relative_to(ROOT).as_posix()]=hashlib.sha256(raw).hexdigest()
    return [json.loads(s)for s in raw.decode().splitlines()if s.strip()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

reported=load(TOR/'EPISODE_LEVEL_COMPARISON.json')
comparisons=[];byblock={};success_diffs=[];info_diffs=[]
for block in range(1,9):
    b=dict(episodes=0,success_changed=0,flags_changed=0,net_gap_change_numerator=0)
    for policy in ['octo-small','octo-base']:
        task='PutSpoonOnTableClothInScene-v1'
        n=lines(V3/'data'/f'block_{block:02d}'/policy/task/'nominal.jsonl')
        t=lines(TOR/'data'/f'block_{block:02d}'/policy/task/'forcehalf.jsonl')
        assert len(n)==len(t)==24
        nm={x['episode_id']:x for x in n};tm={x['episode_id']:x for x in t}
        assert set(nm)==set(tm)==set(range(24))
        for ep in range(24):
            x=nm[ep];y=tm[ep]
            assert x['policy']==y['policy']==policy and x['env_id']==y['env_id']==task
            assert x['condition']=='nominal'and y['condition']=='forcehalf'
            assert x['policy_seed']==y['policy_seed']and x['steps']==y['steps']==60
            assert isinstance(x['success'],bool)and isinstance(y['success'],bool)
            b['episodes']+=1
            same=x['success']==y['success'];sameinfo=x['info']==y['info']
            comparisons.append(dict(block=block,policy=policy,episode=ep,same_success=same,same_info=sameinfo))
            if not same:
                b['success_changed']+=1;b['net_gap_change_numerator']+=(1 if policy=='octo-small'else -1)*(int(y['success'])-int(x['success']))
                success_diffs.append(dict(block=block,policy=policy,episode_id=ep,nominal=x['success'],half_torque=y['success']))
            if not sameinfo:
                b['flags_changed']+=1
                info_diffs.append(dict(block=block,policy=policy,episode_id=ep,nominal=x['info'],half_torque=y['info']))
    byblock[str(block)]=b
assert reported['episodes']==len(comparisons)==384
assert reported['success_unchanged']==sum(x['same_success']for x in comparisons)==380
assert reported['diagnostic_flags_unchanged']==sum(x['same_info']for x in comparisons)==370
assert reported['success_changed']==success_diffs and reported['diagnostic_flags_changed']==info_diffs
assert reported['per_block']==byblock
assert all(sha(ROOT/rel)==digest for rel,digest in reported['inputs'].items())
checks['episode_level']=dict(pass_=True,episodes=384,success_unchanged=380,diagnostics_unchanged=370,
    success_changed=success_diffs,per_block=byblock,all_32_raw_input_hashes_match=True,
    no_inference_on_trajectory_identity_or_mechanical_cause=True)

provenance=load(A/'MECHANISM_FIGURE_PROVENANCE.json');native={}
fixed_provenance=load(HERE/'FIG4_DESCRIPTIVE_PROVENANCE.json')
for task in ['PickCube-v1','PushCube-v1']:
    for mode in ['pd_joint_delta_pos','pd_ee_delta_pos']:
        seq=[];distance=[];episodes=[];metadata=[]
        for batch in range(4):
            path=A/'confirmatory/raw_v2'/f'{task}_{mode}_nominal_batch{batch}.json'
            d=load(path)
            assert d['task']==task and d['mode']==mode and d['setting']=='nominal'and d['batch']==batch
            assert d['steps']==100 and d['num_scenes']==len(d['episodes'])==256
            assert d['applied_gains']==d['nominal_gains']==dict(stiffness=1000.,damping=100.,force_limit=100.)
            assert d['plan_sha256']==sha(A/'confirmatory/PLAN.md')
            assert d['evaluator_sha256']==sha(A/'confirmatory/run_confirmatory_v2.py')
            assert d['frozen_manifest_sha256']==sha(A/'confirmatory/FROZEN_RUNTIME_AMENDMENT_V2.json')
            assert sorted(e['scene_slot']for e in d['episodes'])==list(range(256))
            metadata.append({k:d[k]for k in ['plan_sha256','evaluator_sha256','checkpoint_sha256','frozen_manifest_sha256']})
            for e in d['episodes']:
                s=e['success_sequence'];assert len(s)==100 and set(s)<={0,1}
                seq.append(s);episodes.append(e)
                c=e['state_at_50']['cube_state'];g=e['state_at_50']['goal_state']
                distance.append(math.hypot(c[0]-g[0],c[1]-g[1]))
        S=np.array(seq,dtype=int);D=np.array(distance);counts=S.sum(0);n=len(S)
        summary=dict(n=n,ever50=int(S[:,:50].any(1).sum()),at50=int(S[:,49].sum()),
            peak_step=int(counts[:50].argmax())+1,peak_fraction=float(counts[:50].max()/n),
            median_xy_distance_at_50=statistics.median(distance),fraction_beyond_0p1_at_50=float((D>.1).mean()))
        want=provenance['summary'][f'{task}/{mode}']
        assert set(summary)==set(want)
        for key,value in summary.items():assert math.isclose(value,want[key],rel_tol=1e-12,abs_tol=1e-12),(task,mode,key,value,want[key])
        first50=[next(i+1 for i,s in enumerate(row[:50])if s) for row in seq if any(row[:50])]
        hit_then_lost50=sum(any(row[:50]) and not row[49]for row in seq)
        hit_then_any_loss50=sum(any(row[i]and not row[j]for i in range(50)for j in range(i+1,50))for row in seq)
        extra=dict(at100=int(S[:,99].sum()),min_fraction_steps50_100=float(counts[49:].min()/n),
            max_fraction_steps50_100=float(counts[49:].max()/n),first_hit_median_among_ever50=statistics.median(first50),
            hit_then_lost_at50=hit_then_lost50,at_least_one_loss_after_hit_by50=hit_then_any_loss50,
            distance_min=float(D.min()),distance_max=float(D.max()),histogram_0_to_0p6_outside_count=int(((D<0)|(D>.6)).sum()))
        if task=='PushCube-v1':
            hist=fixed_provenance['histograms'][mode]
            edges=np.array(hist['finite_bin_edges'])
            # Independently count half-open finite bins and the unbounded tail.
            finite_counts=[int(((D>=lo)&(D<hi)).sum())for lo,hi in zip(edges[:-1],edges[1:])]
            overflow=int((D>=.6).sum())
            assert hist['finite_bin_counts']==finite_counts
            assert hist['overflow_threshold_m']==.6 and hist['overflow_operator']=='>='
            assert hist['overflow_count']==overflow
            assert sum(finite_counts)+overflow==hist['count_accounted_for']==hist['n']==1024
            assert math.isclose(hist['raw_max_m'],float(D.max()),rel_tol=1e-12,abs_tol=1e-12)
            assert fixed_provenance['summary'][f'{task}/{mode}']==provenance['summary'][f'{task}/{mode}']
            dx=[];perp=[];speed=[]
            for e in episodes:
                i=e['initial_state'];q=e['state_at_50'];c0=np.array(i['cube_state'][:2]);g0=np.array(i['goal_state'][:2]);u=(g0-c0)/np.linalg.norm(g0-c0)
                c=np.array(q['cube_state'][:2]);g=np.array(q['goal_state'][:2]);delta=c-g
                dx.append(float(delta@u));perp.append(float(delta@np.array([-u[1],u[0]])))
                speed.append(math.sqrt(sum(v*v for v in q['cube_state'][7:10])))
                assert np.allclose(g,g0,rtol=0,atol=0)
            dx=np.array(dx);perp=np.array(perp)
            extra.update(far_edge_along_initial_push_axis_count=int((dx>.1).sum()),behind_near_edge_count=int((dx<-.1).sum()),
                sideways_beyond_radius_count=int((np.abs(perp)>.1).sum()),
                outside_circle_not_far_edge_count=int(((D>.1)&(dx<=.1)).sum()),
                outside_circle_not_far_edge_and_sideways_count=int(((D>.1)&(dx<=.1)&(np.abs(perp)>.1)).sum()),
                speed_at50_median=statistics.median(speed),speed_at50_max=max(speed))
            heights=np.array([e['state_at_50']['cube_state'][2]for e in episodes])
            predicate=(D<.1)&(heights<.025)
            assert np.array_equal(predicate,S[:,49].astype(bool))
            extra.update(inside_radius_at50=int((D<.1).sum()),
                inside_radius_but_height_condition_failed=int(((D<.1)&(heights>=.025)).sum()),
                full_pushcube_predicate_matches_all_at50=True)
        native[f'{task}/{mode}']=dict(recomputed_summary=summary,extra_diagnostics=extra,step_success_counts=list(map(int,counts)),
            metadata_identity_stable=all(v==metadata[0]for v in metadata),source_metadata=metadata[0])
assert all(sha(ROOT/rel)==digest for rel,digest in provenance['inputs'].items())
assert all(sha(ROOT/rel)==digest for rel,digest in fixed_provenance['inputs'].items())
assert sha(ROOT/fixed_provenance['output'])==fixed_provenance['output_sha256']
assert sha(HERE/'make_mechanism_figure.py')==fixed_provenance['source_generator_sha256']
assert sha(A/'make_mechanism_figure.py')==fixed_provenance['original_generator_sha256']
checks['mechanism_figure']=dict(pass_=True,nominal_files=16,episode_sequences=4096,
    all_100_step_fractions_recomputed=True,all_recorded_summary_values_match=True,all_input_hashes_and_output_hash_match=True,
    fixed_histograms_all_1024_scenes_accounted_for=True,original_generator_unchanged=True,
    overflow_counts={m:h['overflow_count']for m,h in fixed_provenance['histograms'].items()},
    current_figure_provenance='FIG4_DESCRIPTIVE_PROVENANCE.json',
    original_output_hash_verified_before_authorized_figure_repair=provenance['output_sha256'],
    comparisons=native)

out=dict(date='2026-09-25',scope='Read-only independent CPU audit; no scientific input, source, figure or frozen analysis changed.',
    checks=checks,source_sha256=inputs)
(HERE/'NEW_ANALYSIS_RECOMPUTATION.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(episode=checks['episode_level'],native={k:{'summary':v['recomputed_summary'],'extra':v['extra_diagnostics']}for k,v in native.items()}),indent=2))
