"""Independent, CPU-only mechanical checks; no new experimental endpoint claims."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy.stats import binomtest
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OLD=ROOT/'reviews/2026-09-24_ras_retarget/cross_benchmark'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
results=json.loads((HERE/'RESULTS.json').read_text())
assert results['status']=='complete'
# Check that the runtime change did not alter any saved state or success bit in
# the one technically repeated cell, without counting the repeat as new evidence.
old=json.loads(next((HERE/'raw').glob('*.json')).read_text())
new=json.loads((HERE/'raw_v2'/next((HERE/'raw').glob('*.json')).name).read_text())
assert old['initial_state_dict']==new['initial_state_dict']
assert old['initial_observations']==new['initial_observations']
assert old['episodes']==new['episodes']
environment=json.loads((OLD/'ENVIRONMENT.json').read_text())
source_checks={}
for name,rec in environment['source_files'].items():
    source_checks[name]=sha(ROOT/name)==rec['sha256']
assert all(source_checks.values())
predicate_checks=0
for path in (HERE/'raw_v2').glob('*.json'):
    rec=json.loads(path.read_text())
    expected_gains=dict(stiffness=1000.,damping=100.,force_limit=100.)
    if rec['setting'].startswith('gain_'):
        multiple=.5 if rec['setting']=='gain_half' else 2.
        expected_gains['stiffness']*=multiple;expected_gains['damping']*=multiple
    if rec['setting'].startswith('force_'):
        expected_gains['force_limit']*=.5 if rec['setting']=='force_half' else 2.
    assert rec['applied_gains']==expected_gains
    task=rec['task']
    for episode in rec['episodes']:
        for step in [50,100]:
            state=episode['state_at_'+str(step)]
            cube=np.asarray(state['cube_state'][:3],dtype=np.float32)
            goal=np.asarray(state['goal_state'][:3],dtype=np.float32)
            if task=='PushCube-v1':
                success=bool(np.linalg.norm(cube[:2]-goal[:2])<.1 and cube[2]<.025)
            else:
                qvel=np.asarray(state['qvel'][:-2],dtype=np.float32)
                success=bool(np.linalg.norm(cube-goal)<=.025 and np.max(np.abs(qvel))<=.2)
            assert success==bool(episode['success_sequence'][step-1]),(path,step,episode['scene_slot'])
            predicate_checks+=1
# Recompute all 20 intervals through scipy's independent binomtest exact API.
tail=.05/80
ci_checks=0
for task,endpoints in results['results'].items():
    for endpoint,res in endpoints.items():
        for setting,cell in res['cells'].items():
            ip=binomtest(cell['joint_only'],cell['n']).proportion_ci(1-2*tail,method='exact')
            im=binomtest(cell['cartesian_only'],cell['n']).proportion_ci(1-2*tail,method='exact')
            assert abs(cell['lower']-(ip.low-im.high))<1e-10
            assert abs(cell['upper']-(ip.high-im.low))<1e-10
            assert sum(row['joint'] for row in cell['batch_counts'])==cell['joint_successes']
            assert sum(row['cartesian'] for row in cell['batch_counts'])==cell['cartesian_successes']
            ci_checks+=1
assert ci_checks==20 and predicate_checks==40960
record=dict(status='pass',
    unchanged_plan_sha256=sha(HERE/'PLAN.md'),
    runtime_repeat=dict(cells=1,episodes=256,initial_observations_identical=True,
        full_initial_states_identical=True,all_100_success_bits_and_50_100_states_identical=True,
        used_as_extra_evidence=False),
    source_and_binary_hashes_match_original_environment=source_checks,
    independent_endpoint_predicate_checks=predicate_checks,
    independent_binomtest_interval_checks=ci_checks,
    all_parameter_assignments_match_fixed_settings=True,
    result_sha256=sha(HERE/'RESULTS.json'))
(HERE/'AUDIT.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps(record,indent=2))
