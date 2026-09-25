import datetime,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OLD=ROOT/'reviews/2026-09-24_ras_retarget/cross_benchmark'
target=HERE/'FROZEN_BEFORE_EXECUTION.json'
if target.exists():raise FileExistsError(target)
if (HERE/'raw').exists() and any((HERE/'raw').iterdir()):raise RuntimeError('Cannot freeze after raw data exist')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files={name:sha(HERE/name) for name in ['PLAN.md','run_confirmatory.py','run_all.py','analyze_confirmatory.py']}
checkpoint_hashes={p.name:sha(p) for p in OLD.glob('*_ckpt.pt')}
report=dict(recorded_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            status='locally_frozen_before_new_data_not_external_preregistration',files=files,
            checkpoint_hashes=checkpoint_hashes,prior_source_environment_sha256=sha(OLD/'ENVIRONMENT.json'),
            previous_outcomes_not_used_for_new_sample_selection=True,
            seed_vector_starts=[731250001,893460001,1135790001,1579130001],batch_size=256,
            intended_primary_family=20,alpha=.05,confirmation_rule='PushCube: all five ever50 gaps positive AND all five at50 gaps negative; PickCube: both positive over all five settings.')
target.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
