"""Recheck all reset evidence without initializing a simulator or reading outcomes."""
from pathlib import Path
import hashlib,json
import numpy as np
import imageio.v2 as imageio
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
frozen=json.loads((HERE/'FROZEN_TECHNICAL_PROTOCOL.json').read_text())
assert all(sha(ROOT/name)==digest for name,digest in frozen['files'].items())
rows=[json.loads(line)for line in (HERE/'reset_records.jsonl').read_text().splitlines()]
assert len(rows)==96
assert {(r['pass_number'],r['episode_id'])for r in rows}=={(p,e)for p in range(4)for e in range(24)}
references={r['episode_id']:r for r in rows if r['pass_number']==0}
for row in rows:
    reference=references[row['episode_id']]
    assert row['condition']==['nominal','fitted','fitted','nominal'][row['pass_number']]
    assert row['state']==reference['state']
    assert hashlib.sha256(json.dumps(row['state'],sort_keys=True).encode()).hexdigest()==row['state_sha256']
    rgb=imageio.imread(HERE/'canonical_images'/f"spoon_{row['episode_id']:02d}.png")
    assert hashlib.sha256(rgb.tobytes()).hexdigest()==row['image_sha256']
    assert row['object_contact']==reference['object_contact']
    assert row['gripper']==reference['gripper']
    assert row['gains_survive_controller_reset'] and row['state_survives_controller_reset']
    assert row['closed_scene_and_agent_cleared'] and row['active_controller_references_new_scene']
    assert row['nominal_settling_completed_before_condition'] and row['physics_steps_after_condition']==0
    assert row['success_fields_read']is False and row['policy_requests']==0
    for key in ['stiffness','damping','force_limit']:
        factor=2 if row['condition']=='fitted'and key=='stiffness'else .5 if row['condition']=='fitted'and key=='damping'else 1.
        want=np.asarray(reference['built_controller'][key])*factor
        assert np.allclose(row['built_controller'][key],want,rtol=1e-12,atol=0)
        assert np.allclose(row['actual_joints'][key],want,rtol=2e-6,atol=1e-5)
report=dict(status='pass',verified_records=96,verified_canonical_pngs=24,
    exact_full_state_dict_comparisons=96,decoded_image_hash_comparisons=96,
    scope='CPU-only verification of reset states, inputs, applied parameters and source/lifetime records',
    no_policy_outcomes=True,frozen_sources_unchanged=True,
    records_sha256=sha(HERE/'reset_records.jsonl'))
(HERE/'AUDIT.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
