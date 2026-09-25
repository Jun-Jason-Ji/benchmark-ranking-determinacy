"""Validate and summarize the complete prospective native ManiSkill grid."""
import hashlib, json, math
from pathlib import Path
import numpy as np
from scipy.stats import beta

HERE=Path(__file__).resolve().parent
TASKS=['PickCube-v1','PushCube-v1']
MODES=['pd_joint_delta_pos','pd_ee_delta_pos']
SETTINGS=['nominal','gain_half','gain_double','force_half','force_double']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def cp(k,n,tail=.0125):
    return (0.0 if k==0 else float(beta.ppf(tail,k,n-k+1)),
            1.0 if k==n else float(beta.ppf(1-tail,k+1,n-k)))
def paired(a,b):
    a,b=np.array(a,dtype=int),np.array(b,dtype=int)
    y=a-b
    n=len(y);plus=int((y==1).sum());minus=int((y==-1).sum())
    lp,up=cp(plus,n);lm,um=cp(minus,n)
    lo,hi=lp-um,up-lm
    return dict(n=n,joint_successes=int(a.sum()),cartesian_successes=int(b.sum()),
                joint_only=plus,cartesian_only=minus,difference=float(y.mean()),
                lower=lo,upper=hi,verdict='joint' if lo>0 else 'cartesian' if hi<0 else 'abstain')

records={};manifest={}
for task in TASKS:
    for mode in MODES:
        for setting in SETTINGS:
            path=HERE/'full_grid'/f'{task}_{mode}_{setting}.json'
            if not path.exists(): raise FileNotFoundError(f'Incomplete grid: {path}')
            rec=json.loads(path.read_text())
            assert len(rec['episodes'])==256
            assert rec['args']['num_envs']==256
            assert rec['args']['seed_start']==2026092500
            assert [r['reset_seed'] for r in rec['episodes']]==list(range(2026092500,2026092756))
            records[(task,mode,setting)]=rec
            manifest[str(path.relative_to(HERE))]=sha(path)

checks=[];source_inventory=[]
for task,tree_name in zip(TASKS,['hf_pickcube_tree.json','hf_pushcube_tree.json']):
    upstream={x['path'].split('/')[-1]:x for x in json.loads((HERE/tree_name).read_text())}
    ref=records[(task,MODES[0],'nominal')]['episodes']
    states=[json.dumps(r['initial_state'],sort_keys=True) for r in ref]
    assert len(set(states))==256, 'Duplicated physical initial states'
    for mode in MODES:
        base_name=f'ppo_{mode}_ckpt.pt'
        local_name=base_name if task==TASKS[0] else 'PushCube_'+base_name
        actual=sha(HERE/local_name)
        expected=upstream[base_name]['lfs']['oid']
        assert actual==expected, 'Checkpoint does not match upstream LFS SHA256'
        source_inventory.append(dict(task=task,mode=mode,path=local_name,sha256=actual,verified_against='official HF LFS'))
        for setting in SETTINGS:
            rec=records[(task,mode,setting)]
            assert rec['checkpoint_sha256']==actual
            assert [json.dumps(r['initial_state'],sort_keys=True) for r in rec['episodes']]==states,'Initial physical states not matched'
            assert rec['success_at_end']==sum(r['success_at_end'] for r in rec['episodes'])
            assert rec['success_once']==sum(r['success_once'] for r in rec['episodes'])
            assert all(not r['success_at_end'] or r['success_once'] for r in rec['episodes'])
    checks.append(dict(task=task,distinct_initial_states=256,all_ten_cells_match_initial_states=True))

def summarize(outcome):
  results={}
  for task in TASKS:
    prefix_results={}
    for n in [32,64,128,256]:
        cells={}
        for setting in SETTINGS:
            a=[r[outcome] for r in records[(task,MODES[0],setting)]['episodes'][:n]]
            b=[r[outcome] for r in records[(task,MODES[1],setting)]['episodes'][:n]]
            cells[setting]=paired(a,b)
        lo=min(c['lower'] for c in cells.values());hi=max(c['upper'] for c in cells.values())
        prefix_results[str(n)]=dict(cells=cells,envelope=dict(lower=lo,upper=hi,
                 verdict='joint' if lo>0 else 'cartesian' if hi<0 else 'abstain'),
                 point_difference_range=[min(c['difference'] for c in cells.values()),max(c['difference'] for c in cells.values())])
    results[task]=prefix_results
  return results
results=summarize('success_at_end')
results_ever=summarize('success_once')

report=dict(status='complete',episodes=5120,scene_sample_size_per_task=256,
            inference='randomized initial-scene distribution under binomial sampling assumptions, conditional on checkpoints/build',
            component_interval='Clopper–Pearson, two-sided 97.5% for each discordance probability',
            combined_interval='[lower(p_plus)-upper(p_minus), upper(p_plus)-lower(p_minus)]',
            per_direction_failure_bound=.025,any_direction_failure_bound=.05,
            distinct_second_benchmark_tasks=True,independent_physics_engine=False,
            calibrated_parameter_set=False,real_robot_validation=False,
            scene_matching=checks,checkpoints=source_inventory,
            evaluator_hashes=sorted({r['script_sha256'] for r in records.values()}),
            outcome_family='final-step success (primary); ever-success (diagnostic only)',
            results=results,results_ever_success=results_ever,raw_file_sha256=manifest,
            measured_episode_execution_seconds=sum(r['elapsed_seconds'] for r in records.values()))
(HERE/'RESULTS.json').write_text(json.dumps(report,indent=2),encoding='utf-8')

lines=['# Native ManiSkill external check: complete results','',
       'This is a workflow portability check on native Franka manipulation tasks. It is not an independent physics-engine replication, a real-robot validation, or a calibration-identifiability experiment. All 20 planned cells were retained.','',
       'The primary difference is joint-space PPO minus Cartesian-position PPO. Counts use final-step success after 50 steps on the same 256 initial scenes. Intervals concern the randomized initial-scene distribution under the stated sampling assumptions; the observed finite sample is not an exhaustive benchmark census.','',
       '| Task | Nominal difference [95% interval] | Five-setting envelope | Verdict |',
       '|---|---:|---:|---|']
for task in TASKS:
    r=results[task]['256'];c=r['cells']['nominal'];e=r['envelope']
    lines.append(f"| {task} | {c['difference']:+.3f} [{c['lower']:+.3f}, {c['upper']:+.3f}] | [{e['lower']:+.3f}, {e['upper']:+.3f}] | {e['verdict']} |")
lines+=['','## Full planned grid','',
        '| Task | Setting | Joint successes / 256 | Cartesian successes / 256 | Paired difference | 95% interval |',
        '|---|---|---:|---:|---:|---:|']
for task in TASKS:
    for setting,c in results[task]['256']['cells'].items():
        lines.append(f"| {task} | {setting} | {c['joint_successes']} | {c['cartesian_successes']} | {c['difference']:+.3f} | [{c['lower']:+.3f}, {c['upper']:+.3f}] |")
lines+=['','## Success-definition sensitivity (recorded diagnostic)','',
        'The prespecified primary outcome is final-step success. Official PPO examples prominently report ever-success. These answer different questions: reaching the goal at least once versus retaining success at step 50. Both were recorded in every cell; the primary outcome was not changed after observing the distinction.','',
        '| Task | Nominal ever-success joint / Cartesian | Difference [95% interval] | Five-setting ever-success envelope | Verdict |',
        '|---|---:|---:|---:|---|']
for task in TASKS:
    r=results_ever[task]['256'];c=r['cells']['nominal'];e=r['envelope']
    lines.append(f"| {task} | {c['joint_successes']}/256 / {c['cartesian_successes']}/256 | {c['difference']:+.3f} [{c['lower']:+.3f}, {c['upper']:+.3f}] | [{e['lower']:+.3f}, {e['upper']:+.3f}] | {e['verdict']} |")
lines+=['','### Complete ever-success diagnostic','',
        '| Task | Setting | Joint successes / 256 | Cartesian successes / 256 | Paired difference | 95% interval |',
        '|---|---|---:|---:|---:|---:|']
for task in TASKS:
    for setting,c in results_ever[task]['256']['cells'].items():
        lines.append(f"| {task} | {setting} | {c['joint_successes']} | {c['cartesian_successes']} | {c['difference']:+.3f} | [{c['lower']:+.3f}, {c['upper']:+.3f}] |")
lines+=['','## Prespecified descriptive prefix budgets','',
        '| Task | Scenes | Nominal verdict | Envelope verdict | Envelope |','|---|---:|---|---|---:|']
for task in TASKS:
    for n,r in results[task].items():
        e=r['envelope'];lines.append(f"| {task} | {n} | {r['cells']['nominal']['verdict']} | {e['verdict']} | [{e['lower']:+.3f}, {e['upper']:+.3f}] |")
lines+=['','## Integrity and interpretation','',
        '- All four checkpoints match their official Hugging Face LFS SHA256. No training was performed.',
        '- Within each task, all ten policy–setting cells share identical recorded initial joint, object and goal states; all 256 states are distinct.',
        '- Initial scenes are paired; actor means are deterministic. There are no additional policy sampling replications or independent training runs.',
        '- Five arm settings were fixed before full evaluation: nominal, half/double common gain, and half/double force limit. These are deliberate robustness interventions, not a real-data-compatible calibration set.',
        '- Published export metadata comes from an earlier ManiSkill build. No equivalence to the original training or published benchmark score is assumed.',
        '- The public ManiSkill support table does not guarantee Windows GPU support. The recorded unchanged native components ran successfully on this local Windows build; operating-system portability remains untested.',
        '- This two-task check broadens embodiment, task, policy family and observation modality, but shares SAPIEN/PhysX lineage with SIMPLER and does not establish universal benchmark generalization.',
        '- Null and abstention results are retained; neither tasks nor intervention magnitudes were selected after the grid outcomes.',
        '', '## Sources','',
        '- Official code: https://github.com/mani-skill/ManiSkill',
        '- Official policy export and demonstrations: https://huggingface.co/datasets/haosulab/ManiSkill_Demonstrations/tree/d674485bbffdd533914e52d272fdda34c0515608/demos',
        '- Native task interface and RNG: https://maniskill.readthedocs.io/en/latest/user_guide/concepts/rng.html',
        '- ManiSkill3 formal publication: https://www.roboticsproceedings.org/rss21/p021.pdf','']
(HERE/'RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')
print('\n'.join(lines[:14]))
