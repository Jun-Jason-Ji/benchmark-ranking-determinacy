"""Additional outcome-blind cross-process check against the frozen 96-reset records."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,sys,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import controller_sweep
import mani_skill.envs
import sapien
from ms3_windows_compat import apply_compatibility
from fresh_reset import fresh_reset_episode
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--condition',choices=['nominal','fitted'],required=True)
    args=ap.parse_args();out=HERE/f'CROSS_PROCESS_{args.condition}.json'
    assert not out.exists()
    frozen=json.loads((HERE/'FROZEN_TECHNICAL_PROTOCOL.json').read_text())
    for name,digest in frozen['files'].items():assert sha(ROOT/name)==digest
    refs={r['episode_id']:r for r in map(json.loads,(HERE/'reset_records.jsonl').read_text().splitlines())if r['pass_number']==0}
    protocol=dict(created_utc=datetime.now(timezone.utc).isoformat(),condition=args.condition,
        scope='Twenty-four resets in a new Python process; exact state and input comparison only',
        adapter_sha256=sha(HERE/'fresh_reset.py'),test_sha256=sha(Path(__file__)),
        canonical_records_sha256=sha(HERE/'reset_records.jsonl'))
    (HERE/f'CROSS_PROCESS_{args.condition}_BEFORE.json').write_text(json.dumps(protocol,indent=2),encoding='utf-8')
    apply_compatibility();device=sapien.Device('cuda');backend='pci:'+device.pci_string
    rows=[];started=time.perf_counter()
    for ep in range(24):
        with fresh_reset_episode('PutSpoonOnTableClothInScene-v1',ep,args.condition,backend)as(env,obs,audit):
            audit['matches_previous_process_state']=audit['state']==refs[ep]['state']
            audit['matches_previous_process_image']=audit['image_sha256']==refs[ep]['image_sha256']
        rows.append(audit)
        del env,obs,audit
    passed=all(r['matches_previous_process_state']and r['matches_previous_process_image']for r in rows)
    report=dict(status='pass'if passed else 'fail',condition=args.condition,cases=24,
        no_policy_calls=True,no_success_fields_read=True,elapsed_seconds=time.perf_counter()-started,
        protocol=protocol,rows=rows)
    out.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items()if k not in ['rows','protocol']}))
    if not passed:raise SystemExit(2)
