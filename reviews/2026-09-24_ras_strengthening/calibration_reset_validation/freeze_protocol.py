from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
assert not (HERE/'reset_records.jsonl').exists()
assert not (HERE/'FROZEN_TECHNICAL_PROTOCOL.json').exists()
paths=[HERE/'PLAN.md',HERE/'fresh_reset.py',HERE/'validate_fresh_reset.py',
       ROOT/'scripts/controller_sweep.py',ROOT/'scripts/ms3_windows_compat.py',
       ROOT/'reviews/2026-09-24_ras_strengthening/calibration_confirmation/INITIAL_STATE_FAILURE.md',
       ROOT/'reviews/2026-09-24_ras_strengthening/calibration_confirmation/INITIAL_STATE_FAILURE.json']
pkg=ROOT/'.venv-windows-ms3/Lib/site-packages/mani_skill'
paths += [pkg/p for p in ['envs/sapien_env.py','agents/base_agent.py',
    'agents/controllers/pd_joint_pos.py','agents/controllers/pd_ee_pose.py',
    'envs/tasks/digital_twins/bridge_dataset_eval/base_env.py',
    'envs/tasks/digital_twins/bridge_dataset_eval/put_on_in_scene.py']]
report=dict(created_utc=datetime.now(timezone.utc).isoformat(),
    purpose='Outcome-blind reset implementation validation; no policy outcomes',
    files={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in paths})
(HERE/'FROZEN_TECHNICAL_PROTOCOL.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(report['created_utc'])
