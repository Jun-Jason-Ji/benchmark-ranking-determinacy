"""Read-only replay-initialization audit; no simulator/policy import or execution."""
from pathlib import Path
from collections import defaultdict
import hashlib,itertools,json
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SCOPES={
 'ms3_grid':'results/replay_sysid_100/grid',
 'ms3_sweep':'results/replay_sysid_100/sweep_v1',
 'ms3_fitted_ratio':'results/replay_sysid_100_fitted_ratio/iso_at_fitted',
 'ms2_grid':'results/replay_sysid_ms2/grid',
 'ms2_sweep':'results/replay_sysid_ms2/sweep_v1',
 'ms2_extended_scale':'results/replay_sysid_ms2/iso_ratio_v1',
 'ms2_fitted_ratio':'results/replay_sysid_ms2_fitted_ratio/iso_at_fitted',
 'ms2_fitted_force':'results/replay_sysid_ms2_force_probe/fitted_force_probe'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files={};outputs={};stack_refs={};frame_mismatch=[]
def register(path):files[path.relative_to(ROOT).as_posix()]=sha(path)
for name,rel in SCOPES.items():
    directory=ROOT/rel;register(directory/'run_meta.json')
    meta=json.loads((directory/'run_meta.json').read_text())
    expected=meta['demo_ids'];assert len(expected)==len(set(expected))==98
    arrays={};all_init=[];bad=[];refs={};first_mismatch=[];condition_means={}
    for condition in meta['conditions']:
        records_path=directory/(condition+'.jsonl');register(records_path)
        records=[json.loads(line)for line in records_path.read_text().splitlines()if line.strip()]
        assert len(records)==98 and {r['episode_id']for r in records}==set(expected)
        condition_means[condition]=float(np.mean([r['mean_total_err']for r in records]))
        for record in records:
            episode=record['episode_id'];path=directory/f'{condition}_ep{episode:03d}.npz';register(path)
            with np.load(path,allow_pickle=False)as data:
                p=data['sim_p'];q=data['sim_q'];gp=data['gt_p'];gq=data['gt_q']
                assert p.shape==(record['steps'],3)and q.shape==(record['steps'],4)
                assert all(np.isfinite(a).all()for a in [p,q,gp,gq])
                assert abs(np.linalg.norm(p[0]-gp[0])-record['init_transl_err'])<1e-12
                first=(p[0].tobytes(),q[0].tobytes());stack_key=(name[:3],episode)
                if episode not in refs:refs[episode]=(first,gp.copy(),gq.copy())
                assert np.array_equal(gp,refs[episode][1])and np.array_equal(gq,refs[episode][2])
                if first!=refs[episode][0]:first_mismatch.append(dict(condition=condition,episode=episode))
                if stack_key not in stack_refs:stack_refs[stack_key]=first
                elif first!=stack_refs[stack_key]:frame_mismatch.append(dict(scope=name,condition=condition,episode=episode))
                arrays[(condition,episode)]=(p.copy(),q.copy())
            all_init.append(record['init_transl_err'])
            if not record['init_ok']:bad.append(dict(condition=condition,episode=episode))
    groups=defaultdict(list)
    for c,params in meta['conditions'].items():
        if params.get('force_scale',1.)!=1.:continue
        groups[(round(params.get('damping_scale',1.)/params.get('stiffness_scale',1.),6),params.get('delay_steps',0))].append(c)
    max_iso=0.;max_meanloss_change=0.;groups_measured=0
    for group in groups.values():
        if len(group)<2:continue
        groups_measured+=1
        for a,b in itertools.combinations(group,2):
            max_meanloss_change=max(max_meanloss_change,abs(condition_means[a]-condition_means[b]))
            for episode in expected:
                max_iso=max(max_iso,float(np.linalg.norm(arrays[(a,episode)][0]-arrays[(b,episode)][0],axis=1).max()))
    torque=[]
    pairs=[('nominal','force_x0.5'),('nominal','nominal_force0.5'),('s2_d0.5_delay1','s2_d0.5_delay1_force0.5')]
    for a,b in pairs:
        if a not in meta['conditions']or b not in meta['conditions']:continue
        exact=0;residuals=[]
        for episode in expected:
            pa,qa=arrays[(a,episode)];pb,qb=arrays[(b,episode)]
            same=pa.dtype==pb.dtype and qa.dtype==qb.dtype and pa.tobytes()==pb.tobytes()and qa.tobytes()==qb.tobytes()
            if same:exact+=1
            else:residuals.append(dict(episode=episode,max_position_difference_m=float(np.linalg.norm(pa-pb,axis=1).max())))
        torque.append(dict(conditions=[a,b],bitwise_position_and_quaternion_equal=exact,total=98,residuals=residuals))
    outputs[name]=dict(directory=rel,n_conditions=len(meta['conditions']),n_demos=98,
        trajectories_checked=len(arrays),initial_ee_frame_mismatches=first_mismatch,
        all_initialization_flags_valid=not bad,bad_initialization_records=bad,
        min_initial_position_error_m=min(all_init),max_initial_position_error_m=max(all_init),
        equal_ratio_groups=groups_measured,max_equal_ratio_euclidean_displacement_m=max_iso,
        max_mean_composite_loss_change_within_equal_ratio_group=max_meanloss_change,
        torque_checks=torque,recorded_array_fields=['sim_p','sim_q','gt_p','gt_q','transl_err','rot_err'],
        recorded_full_initial_joint_or_contact_state=False,
        started_utc=meta['started_utc'],metadata_contains_executed_script_hash=any('sha' in k.lower()or 'hash'in k.lower()for k in meta))
    print(name,outputs[name]['trajectories_checked'],'initial mismatches',len(first_mismatch),flush=True)
sources=['scripts/replay_bridge_sysid.py','scripts/replay_bridge_sysid_ms2.py',
         'scripts/run_replay100.cmd','scripts/run_replay_ms2.sh','scripts/ms3_windows_compat.py']
for source in sources:register(ROOT/source)
report=dict(scope='Read-only source and stored-trajectory audit; no simulator or policy execution',
            scopes=outputs,within_stack_across_scope_initial_frame_mismatches=frame_mismatch,
            total_trajectory_files=sum(x['trajectories_checked']for x in outputs.values()),
            script_sha256=sha(Path(__file__)),input_file_count=len(files))
(HERE/'REPLAY_INITIALIZATION_INPUTS.json').write_text(json.dumps(files,indent=2),encoding='utf-8')
(HERE/'REPLAY_INITIALIZATION_RESULTS.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Total',report['total_trajectory_files'],'cross-scope mismatches',len(frame_mismatch))
