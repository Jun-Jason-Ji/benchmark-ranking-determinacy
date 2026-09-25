"""Episode-level comparison of the half-torque control with the shared nominal cells.
Same block, policy, configuration index and policy seed; compares the stored success flag and
the full task diagnostic dictionary. Trajectories and commanded torques were not stored, so this
is an outcome-level check, not a bitwise trajectory comparison."""
from pathlib import Path
import hashlib, json
HERE = Path(__file__).resolve().parent; R = HERE.parents[2]
NOM = R / 'reviews/2026-09-24_ras_strengthening/calibration_confirmation_v3/data'
TASK = 'PutSpoonOnTableClothInScene-v1'
def load(p): return [json.loads(l) for l in p.read_text(encoding='utf8').splitlines() if l.strip()]
inputs, per_block, diffs, flagdiffs = {}, {}, [], []
tot = same_success = same_flags = 0
for b in range(1, 9):
    blk = dict(episodes=0, success_changed=0, flags_changed=0, net_gap_change_numerator=0)
    for pol in ['octo-small', 'octo-base']:
        pt = HERE / 'data' / f'block_{b:02d}' / pol / TASK / 'forcehalf.jsonl'
        pn = NOM / f'block_{b:02d}' / pol / TASK / 'nominal.jsonl'
        for p in (pt, pn): inputs[str(p.relative_to(R))] = hashlib.sha256(p.read_bytes()).hexdigest()
        t, n = load(pt), load(pn)
        nom = {e['episode_id']: e for e in n}
        assert len(t) == 24 and len(n) == 24
        for e in t:
            o = nom[e['episode_id']]
            assert o['policy_seed'] == e['policy_seed'] and o['steps'] == e['steps'] == 60
            tot += 1; blk['episodes'] += 1
            if o['success'] == e['success']: same_success += 1
            else:
                blk['success_changed'] += 1
                sign = (1 if pol == 'octo-small' else -1) * ((1 if e['success'] else 0) - (1 if o['success'] else 0))
                blk['net_gap_change_numerator'] += sign
                diffs.append(dict(block=b, policy=pol, episode_id=e['episode_id'], nominal=o['success'], half_torque=e['success']))
            if o['info'] == e['info']: same_flags += 1
            else:
                blk['flags_changed'] += 1
                flagdiffs.append(dict(block=b, policy=pol, episode_id=e['episode_id'], nominal=o['info'], half_torque=e['info']))
    per_block[b] = blk
out = dict(scope='Half-torque control versus shared nominal cells; same block, policy, configuration and policy seed.',
           episodes=tot, success_unchanged=same_success, diagnostic_flags_unchanged=same_flags,
           success_changed=diffs, diagnostic_flags_changed=flagdiffs, per_block=per_block,
           note='Outcome-level check only; trajectories and commanded torques were not stored.', inputs=inputs)
(HERE / 'EPISODE_LEVEL_COMPARISON.json').write_text(json.dumps(out, indent=1) + '\n', encoding='utf8')
print(json.dumps({k: out[k] for k in ['episodes', 'success_unchanged', 'diagnostic_flags_unchanged']}), '\nper block:', json.dumps(per_block))
