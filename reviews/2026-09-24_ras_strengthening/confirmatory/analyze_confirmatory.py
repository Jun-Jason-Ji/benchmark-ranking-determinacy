"""Analyze every fixed cell and the predeclared 20-contrast confidence family."""
import hashlib,json,math
from pathlib import Path
import numpy as np
from scipy.stats import beta
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OLD=ROOT/'reviews/2026-09-24_ras_retarget/cross_benchmark'
TASKS=['PickCube-v1','PushCube-v1']
MODES=['pd_joint_delta_pos','pd_ee_delta_pos']
SETTINGS=['nominal','gain_half','gain_double','force_half','force_double']
STARTS=[731250001,893460001,1135790001,1579130001]
ENDPOINTS=['ever50','at50']
TAIL=.05/(20*4)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cp(k,n):
    return (0. if k==0 else float(beta.ppf(TAIL,k,n-k+1)),
            1. if k==n else float(beta.ppf(1-TAIL,k+1,n-k)))
def longest(row):
    best=run=0
    for value in row:
        run=run+1 if value else 0;best=max(best,run)
    return best
def endpoints(rec,key):
    s=np.array([e['success_sequence'] for e in rec['episodes']],dtype=int)
    if key=='ever50':return s[:,:50].max(1)
    if key=='at50':return s[:,49]
    if key=='ever100':return s.max(1)
    if key=='at100':return s[:,99]
    if key=='dwell10_by50':return np.array([longest(row[:50])>=10 for row in s],dtype=int)
    if key=='dwell10_by100':return np.array([longest(row)>=10 for row in s],dtype=int)
    raise KeyError(key)
def compare(a,b):
    y=np.array(a,dtype=int)-np.array(b,dtype=int);n=len(y)
    kp=int((y==1).sum());km=int((y==-1).sum())
    lp,up=cp(kp,n);lm,um=cp(km,n)
    lo=lp-um;hi=up-lm;estimate=float(y.mean())
    radius=math.sqrt(2*math.log(2*20/.05)/n)
    return dict(n=n,joint_successes=int(np.sum(a)),cartesian_successes=int(np.sum(b)),
                joint_only=kp,cartesian_only=km,difference=estimate,lower=lo,upper=hi,
                verdict='joint' if lo>0 else 'cartesian' if hi<0 else 'abstain',
                hoeffding_lower=max(-1.,estimate-radius),hoeffding_upper=min(1.,estimate+radius))
def old_projection(new):
    return dict(qpos=new['qpos'],cube_pose=new['cube_state'][:7],goal_pose=new['goal_state'][:7])
frozen=json.loads((HERE/'FROZEN_BEFORE_EXECUTION.json').read_text())
assert sha(HERE/'PLAN.md')==frozen['files']['PLAN.md']
records={};raw_hashes={};gates=[]
for task in TASKS:
  seen=[];old_states=set()
  for p in (OLD/'full_grid').glob(task+'*.json'):
    old_states.update(json.dumps(e['initial_state'],sort_keys=True) for e in json.loads(p.read_text())['episodes'])
  if task=='PickCube-v1':
    for name in ['pilot_joint_nominal.json','pilot_ee_nominal.json']:
      old_states.update(json.dumps(e['initial_state'],sort_keys=True) for e in json.loads((OLD/name).read_text())['episodes'])
  for batch in range(4):
    reference=None;reference_full=None
    for mode in MODES:
      for setting in SETTINGS:
        p=HERE/'raw'/f'{task}_{mode}_{setting}_batch{batch}.json'
        rec=json.loads(p.read_text())
        assert rec['steps']==100 and rec['num_scenes']==256
        assert rec['plan_sha256']==frozen['files']['PLAN.md']
        assert rec['evaluator_sha256']==frozen['files']['run_confirmatory.py']
        assert rec['scene_seed_vector_start']==STARTS[batch]
        assert rec['sim_freq']==100 and rec['control_freq']==20
        assert len(rec['episodes'])==256
        assert all(len(e['success_sequence'])==100 and set(e['success_sequence'])<={0,1} for e in rec['episodes'])
        current=[json.dumps(e['initial_state'],sort_keys=True) for e in rec['episodes']]
        full=json.dumps(rec['initial_state_dict'],sort_keys=True)
        if reference is None:
          reference=current;reference_full=full
          seen.extend(json.dumps(old_projection(e['initial_state']),sort_keys=True) for e in rec['episodes'])
        assert current==reference,'Physical state mismatch'
        assert full==reference_full,'Full simulator state mismatch'
        records[(task,mode,setting,batch)]=rec;raw_hashes[p.name]=sha(p)
    assert len(set(reference))==256
  assert len(seen)==1024 and len(set(seen))==1024
  assert not set(seen)&old_states,'Overlap with exploratory data'
  gates.append(dict(task=task,distinct_scenes=1024,old_scene_overlap=0,
                    all_physical_states_and_full_state_dictionaries_match=True))
assert len(records)==80
results={}
for task in TASKS:
  task_results={}
  for endpoint in ENDPOINTS:
    cells={}
    for setting in SETTINGS:
      a=np.concatenate([endpoints(records[(task,MODES[0],setting,b)],endpoint) for b in range(4)])
      c=np.concatenate([endpoints(records[(task,MODES[1],setting,b)],endpoint) for b in range(4)])
      row=compare(a,c)
      row['batch_counts']=[dict(batch=b,joint=int(endpoints(records[(task,MODES[0],setting,b)],endpoint).sum()),
                                  cartesian=int(endpoints(records[(task,MODES[1],setting,b)],endpoint).sum())) for b in range(4)]
      cells[setting]=row
    lo=min(x['lower'] for x in cells.values());hi=max(x['upper'] for x in cells.values())
    hl=min(x['hoeffding_lower'] for x in cells.values());hu=max(x['hoeffding_upper'] for x in cells.values())
    task_results[endpoint]=dict(cells=cells,envelope=dict(lower=lo,upper=hi,
        verdict='joint' if lo>0 else 'cartesian' if hi<0 else 'abstain'),
        hoeffding_envelope=dict(lower=hl,upper=hu,verdict='joint' if hl>0 else 'cartesian' if hu<0 else 'abstain'))
  results[task]=task_results
diagnostics={}
for task in TASKS:
  diagnostics[task]={}
  for setting in SETTINGS:
    diagnostics[task][setting]={}
    for mode in MODES:
      rr=[records[(task,mode,setting,b)] for b in range(4)]
      seq=np.concatenate([np.array([e['success_sequence'] for e in q['episodes']],dtype=int) for q in rr])
      first=[int(np.flatnonzero(row)[0])+1 for row in seq if row.any()]
      diagnostics[task][setting][mode]=dict(
        **{key:int(sum(endpoints(q,key).sum() for q in rr)) for key in ENDPOINTS+['ever100','at100','dwell10_by50','dwell10_by100']},
        longest_success_run_median=float(np.median([longest(row) for row in seq])),
        first_success_step_median_among_successes=float(np.median(first)) if first else None,
        reached_by50_not_successful_at50=int(((seq[:,:50].max(1)==1)&(seq[:,49]==0)).sum()))
report=dict(status='complete',primary_rollouts=20480,steps_per_rollout=100,
            independent_scene_pairs_per_task_setting=1024,batches=4,
            family_alpha=.05,family_differences=20,component_tail_probability=TAIL,
            intervals='simultaneous exact-discordance union-bound family under the independent-scene model',
            iid_assumption='Four distinct seeded pseudorandom streams and no observed state overlap; stochastic independence is an assumption, not established by distinct states.',
            checks=gates,results=results,diagnostics_descriptive_only=diagnostics,
            pushcube_reversal_confirmed=results['PushCube-v1']['ever50']['envelope']['lower']>0 and results['PushCube-v1']['at50']['envelope']['upper']<0,
            pickcube_positive_both_confirmed=all(results['PickCube-v1'][e]['envelope']['lower']>0 for e in ENDPOINTS),
            raw_sha256=raw_hashes,freeze_sha256=sha(HERE/'FROZEN_BEFORE_EXECUTION.json'))
(HERE/'RESULTS.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
lines=['# Confirmatory native-task results','',
       'All 80 prespecified cells completed: 20480 rollouts, 1024 new paired initial scenes per task/setting. The 20-difference primary family uses exact paired-discordance intervals with Bonferroni/union-bound simultaneous coverage at least 95% under the independent-scene binomial sampling assumptions.','',
       '| Task | Primary endpoint | Nominal difference | Simultaneous nominal interval | Five-setting envelope | Decision |','|---|---|---:|---:|---:|---|']
for task in TASKS:
  for endpoint,x in results[task].items():
    n=x['cells']['nominal'];e=x['envelope']
    lines.append(f"| {task} | {endpoint} | {n['difference']:+.3f} | [{n['lower']:+.3f}, {n['upper']:+.3f}] | [{e['lower']:+.3f}, {e['upper']:+.3f}] | {e['verdict']} |")
lines+=['',f"Prespecified PushCube reversal conjunction: **{report['pushcube_reversal_confirmed']}**.",
        f"Prespecified PickCube positive-ordering contrast: **{report['pickcube_positive_both_confirmed']}**.",'',
        'These results are conditional on the fixed checkpoints, build, endpoints, five settings and sampling assumptions. They are not cross-engine or real-world confirmation. Distinct PRNG stream seeds and unique states do not empirically prove stochastic independence.','',
        '## Complete family','',
        '| Task | Endpoint | Setting | Joint / 1024 | Cartesian / 1024 | Difference | Simultaneous interval |','|---|---|---|---:|---:|---:|---:|']
for task in TASKS:
  for endpoint,x in results[task].items():
    for setting,c in x['cells'].items():lines.append(f"| {task} | {endpoint} | {setting} | {c['joint_successes']} | {c['cartesian_successes']} | {c['difference']:+.3f} | [{c['lower']:+.3f}, {c['upper']:+.3f}] |")
lines+=['','## Predetermined concentration-bound sensitivity','',
       'For independent bounded paired outcomes in [-1,1], a simultaneous Hoeffding family uses radius sqrt(2 log(40/0.05)/1024). It does not require normally distributed paired outcomes; independence remains an assumption.','',
       '| Task | Endpoint | Hoeffding envelope | Decision |','|---|---|---:|---|']
for task in TASKS:
  for endpoint,x in results[task].items():
    e=x['hoeffding_envelope'];lines.append(f"| {task} | {endpoint} | [{e['lower']:+.3f}, {e['upper']:+.3f}] | {e['verdict']} |")
lines+=['','## Predetermined diagnostics','',
       'Dwell, step-100 outcomes and first-hit times are descriptive diagnostics only. They are not additional confirmatory claims. Full batch counts, success sequences and initial/final states are preserved.','',
       '| Task | Setting | Pipeline | Ever50 | At50 | Ever100 | At100 | Dwell10 by50 | Dwell10 by100 |','|---|---|---|---:|---:|---:|---:|---:|---:|']
for task in TASKS:
  for setting,rr in diagnostics[task].items():
    for mode,c in rr.items():lines.append(f"| {task} | {setting} | {mode} | {c['ever50']} | {c['at50']} | {c['ever100']} | {c['at100']} | {c['dwell10_by50']} | {c['dwell10_by100']} |")
(HERE/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines[:17]))
