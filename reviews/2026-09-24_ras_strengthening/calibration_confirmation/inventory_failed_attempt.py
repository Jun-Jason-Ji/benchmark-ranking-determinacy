"""Preserve an outcome-blind inventory of the stopped V2 technical attempt."""
import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
import analyze_confirmation as spec

HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def inspect_jsonl(path):
    if not path.exists():return dict(present=False,records=0,episode_ids=[],malformed_lines=[]),[]
    lines=path.read_text(encoding='utf-8').splitlines();records=[];malformed=[]
    for number,line in enumerate(lines,1):
        if not line.strip():continue
        try:records.append(json.loads(line))
        except json.JSONDecodeError:malformed.append(number)
    # Only identity, seed and horizon fields are inspected. No success field is accessed.
    info=dict(present=True,path=path.relative_to(HERE).as_posix(),sha256=sha(path),records=len(records),
              episode_ids=[r['episode_id']for r in records],malformed_lines=malformed,
              steps_present=sorted(set(r['steps']for r in records)))
    return info,records

def main():
    cells=[]
    for block,base in enumerate(spec.SEEDS,1):
        for policy in spec.POLICIES:
            for condition in spec.CONDITIONS:
                d=HERE/'data'/f'block_{block:02d}'/policy/spec.ENV
                info,records=inspect_jsonl(d/f'{condition}.jsonl')
                audit_path=d/f'{condition}_audit.jsonl';complete=False
                if audit_path.exists():
                    events=[]
                    for line in audit_path.read_text(encoding='utf-8').splitlines():
                        try:events.append(json.loads(line))
                        except json.JSONDecodeError:pass
                    complete=any(r.get('kind')=='cell_complete'for r in events)
                identity_ok=all(r['policy']==policy and r['condition']==condition and r['env_id']==spec.ENV and r['policy_seed']==base+r['episode_id']for r in records)
                ids=info['episode_ids']
                status='not_started'if not info['present']else('completed_but_excluded'if complete and sorted(ids)==list(range(24))and not info['malformed_lines']else'partial_technical_attempt_excluded')
                cells.append(dict(block=block,policy=policy,condition=condition,status=status,audit_complete_marker=complete,identity_fields_consistent=identity_ok,**info))
    result=dict(status='confirmatory_unavailable',attempt='V2 with precollection provenance amendment',
                inventory_created_utc=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                reason='Prespecified physical-state/image pairing gate failed; policy-dependent initial states differed materially.',
                all_attempt_records_excluded_from_confirmation=True,outcome_summary_computed=False,sign_count_computed=False,p_value_computed=False,
                frozen_plan_sha256=sha(HERE/'FROZEN_PLAN.json'),frozen_analysis_sha256=sha(HERE/'FROZEN_ANALYSIS.json'),
                initial_state_failure_sha256=sha(HERE/'INITIAL_STATE_FAILURE.json'),
                completed_cells=sum(r['status']=='completed_but_excluded'for r in cells),
                partial_cells=sum(r['status']=='partial_technical_attempt_excluded'for r in cells),
                not_started_cells=sum(r['status']=='not_started'for r in cells),record_count=sum(r['records']for r in cells),cells=cells)
    target=HERE/'V2_UNAVAILABLE_INVENTORY.json'
    if target.exists():raise RuntimeError('Preserved inventory exists; do not overwrite')
    target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items()if k!='cells'},indent=2))

if __name__=='__main__':main()
