"""Preserve the failed v1, record a narrow runtime fix, and freeze v2 before use."""
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert len(list((HERE/'raw').glob('*.json')))==1
assert not (HERE/'raw_v2').exists()
src=(HERE/'run_confirmatory.py').read_text()
src=src.replace("FROZEN=json.loads((HERE/'FROZEN_BEFORE_EXECUTION.json').read_text())","FROZEN=json.loads((HERE/'FROZEN_RUNTIME_AMENDMENT_V2.json').read_text())")
src=src.replace("FROZEN['files']['run_confirmatory.py']","FROZEN['files']['run_confirmatory_v2.py']")
src=src.replace("out=HERE/'raw';", "out=HERE/'raw_v2';")
src=src.replace('with torch.inference_mode():','with torch.no_grad():')
src=src.replace("sha(HERE/'FROZEN_BEFORE_EXECUTION.json')","sha(HERE/'FROZEN_RUNTIME_AMENDMENT_V2.json')")
(HERE/'run_confirmatory_v2.py').write_text(src,encoding='utf-8')
runner=(HERE/'run_all.py').read_text().replace('1500-','1440-').replace("'run_confirmatory.py'","'run_confirmatory_v2.py'").replace("name+'.log'","name+'_v2.log'").replace("'PROGRESS.json'","'PROGRESS_V2.json'")
(HERE/'run_all_v2.py').write_text(runner,encoding='utf-8')
analysis=(HERE/'analyze_confirmatory.py').read_text().replace("'FROZEN_BEFORE_EXECUTION.json'","'FROZEN_RUNTIME_AMENDMENT_V2.json'").replace("'run_confirmatory.py'","'run_confirmatory_v2.py'").replace("HERE/'raw'/","HERE/'raw_v2'/")
(HERE/'analyze_confirmatory_v2.py').write_text(analysis,encoding='utf-8')
note='''# Runtime amendment, version 2

The locally frozen protocol, seeds, endpoints, sample size, setting grid,
confidence family and decision criteria are unchanged. The first evaluator
completed one cell (PickCube, joint controller, nominal, batch 0) and then failed
at the next environment reset. Its traceback reports PyTorch's prohibition on
an in-place update to an inference tensor outside InferenceMode. Reusing a
controller after a rollout in `torch.inference_mode()` caused this incompatibility.

The version-2 executor changes this context to `torch.no_grad()`, preserving
deterministic actor evaluation without inference-tensor restrictions. Paths and
source-hash validation are updated to separate version-2 outputs. A fresh full
run uses exactly the same prespecified scenes; the original successful cell and
failed execution are retained. The repeated first cell will be compared for
identical physical states and success sequences. No primary outcome summaries
were computed or inspected before this correction. This correction is not
described as an independently preregistered study or hidden by overwriting the
original frozen record. It is a technical amendment after one cell was generated.

The original failed executor consumed 53.38 seconds. The replacement run has a
fixed 1440-second execution limit, keeping combined process runtime below the
original 1500-second compute allocation. Both failures and completed results
remain in the evidence package. The new analysis is the original frozen analysis
with only raw-directory and evaluator/manifest filename substitutions; no
statistical formulas or result-selection logic changed.
'''
(HERE/'RUNTIME_AMENDMENT_V2.md').write_text(note,encoding='utf-8')
files=['PLAN.md','run_confirmatory_v2.py','run_all_v2.py','analyze_confirmatory_v2.py','RUNTIME_AMENDMENT_V2.md']
record=dict(recorded_at_utc=datetime.now(timezone.utc).isoformat(),
    status='runtime_amendment_after_one_saved_cell_before_any_primary_analysis',
    original_frozen_manifest_sha256=sha(HERE/'FROZEN_BEFORE_EXECUTION.json'),
    files={p:sha(HERE/p) for p in files},
    retained_original_raw={p.name:sha(p) for p in (HERE/'raw').glob('*.json')},
    original_failed_execution_sha256=sha(HERE/'PickCube-v1_pd_joint_delta_pos.log'))
(HERE/'FROZEN_RUNTIME_AMENDMENT_V2.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps(record,indent=2))
