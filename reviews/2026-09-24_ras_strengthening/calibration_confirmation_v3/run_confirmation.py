"""Freeze and run the explicitly authorized V3 study using existing servers only."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,concurrent.futures,hashlib,http.client,json,os,subprocess,sys,threading,time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
RESET=HERE.parent/'calibration_reset_validation'
OLD=HERE.parent/'calibration_confirmation'
PY=ROOT/'.venv-windows-ms3/Scripts/python.exe'
SEEDS=[431700100,557900200,683100300,809300400,947500500,1089700600,1231900700,1393100800]
ENV='PutSpoonOnTableClothInScene-v1'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def require(ok,message):
    if not ok:raise RuntimeError(message)
def utc():return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def health(port):
    c=http.client.HTTPConnection('127.0.0.1',port,timeout=8)
    try:
        c.request('GET','/health');r=c.getresponse();require(r.status==200,'Server unavailable')
        return json.loads(r.read())
    finally:c.close()

def freeze():
    validation=json.loads((RESET/'RESULTS.json').read_text())
    require(validation['status']=='pass'and validation['cases']==96 and validation['unique_configurations']==24
            and validation['exact_full_state_and_rgb_across_nominal_fitted']is True and not validation['mismatches'],'Reset validation failed')
    technical=json.loads((RESET/'FROZEN_TECHNICAL_PROTOCOL.json').read_text())
    for rel,digest in technical['files'].items():require(sha(ROOT/rel)==digest,f'Technically validated source changed: {rel}')
    require(sha(RESET/'reset_records.jsonl')==validation['records_sha256'],'Reset validation records changed')
    failed=json.loads((OLD/'V2_UNAVAILABLE_INVENTORY.json').read_text())
    require(failed['status']=='confirmatory_unavailable'and failed['all_attempt_records_excluded_from_confirmation']is True,'Failed attempt must remain excluded')
    paths=[HERE/name for name in ['PLAN.md','execute_cell.py','run_confirmation.py','analyze_confirmation.py','test_analysis.py']]
    paths += [RESET/'RESULTS.json',RESET/'reset_records.jsonl',RESET/'FROZEN_TECHNICAL_PROTOCOL.json',OLD/'V2_UNAVAILABLE_INVENTORY.json']
    paths += [ROOT/rel for rel in technical['files']]
    paths += [ROOT/'scripts/octo_policy_server.py',ROOT/'scripts/task_configs.py']
    filemap={p.relative_to(ROOT).as_posix():sha(p)for p in paths}
    payload=dict(created_utc=utc(),protocol_version='V3-controlled-initialization',seeds=SEEDS,episodes=768,
        independent_blocks_assumed=8,reset_validation_passed=True,reset_validation_sha256=sha(RESET/'RESULTS.json'),
        failed_v2_inventory_sha256=sha(OLD/'V2_UNAVAILABLE_INVENTORY.json'),files=filemap,
        scope_amendment='Canonical nominal-settled initialization before operating-point assignment; historical effects remain protocol contrasts',
        execution_authorization='Coordinating agent explicitly authorized V3 start after passed technical validation and implementation checks')
    plan_path=HERE/'FROZEN_PLAN.json';analysis_path=HERE/'FROZEN_ANALYSIS.json'
    if plan_path.exists():
        old=json.loads(plan_path.read_text());require(old['files']==filemap and old['seeds']==SEEDS,'Existing freeze differs; do not overwrite')
    else:
        require(not(HERE/'data').exists(),'Do not create a pre-execution freeze after data exist')
        plan_path.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    analyzer_hash=sha(HERE/'analyze_confirmation.py')
    if analysis_path.exists():require(json.loads(analysis_path.read_text())['analyzer_sha256']==analyzer_hash,'Analyzer freeze differs')
    else:analysis_path.write_text(json.dumps(dict(created_utc=utc(),analyzer_sha256=analyzer_hash,
        tests_sha256=sha(HERE/'test_analysis.py'),plan_sha256=sha(HERE/'PLAN.md'),protocol_version='V3-controlled-initialization',
        primary='Eight complete seed blocks; exact one-sided binomial/sign test; zeros nonnegative',
        secondary='Block-t working model and bounded-mean interval on [-2,2]'),indent=2)+'\n',encoding='utf-8')
    return json.loads(plan_path.read_text())

def run():
    frozen=freeze();started=time.monotonic();deadline=started+150*60;stop=threading.Event()
    (HERE/'logs').mkdir(exist_ok=True)
    servers={p:health(port)for p,port in [('octo-small',8767),('octo-base',8768)]}
    for p,h in servers.items():require(h.get('model')==p and h.get('session_isolation')is True,'Unexpected policy server')
    (HERE/'SERVER_HEALTH.json').write_text(json.dumps(servers,indent=2)+'\n',encoding='utf-8')
    (HERE/'RUNNING.json').write_text(json.dumps(dict(pid=os.getpid(),started_utc=utc(),deadline_minutes=150,
        protocol_version='V3-controlled-initialization',frozen_plan_sha256=sha(HERE/'FROZEN_PLAN.json')),indent=2)+'\n',encoding='utf-8')
    def worker(policy,port):
        complete=[]
        try:
            for idx,seed in enumerate(SEEDS,1):
                order=['nominal','fitted']if idx%2 else['fitted','nominal']
                for condition in order:
                    require(not stop.is_set(),'Stopped after technical failure in other worker')
                    remaining=deadline-time.monotonic();require(remaining>0,'Fixed wall-time budget exceeded')
                    target=HERE/'data'/f'block_{idx:02d}'
                    command=[str(PY),str(HERE/'execute_cell.py'),'--policy-name',policy,'--policy-url',f'http://127.0.0.1:{port}',
                        '--condition',condition,'--policy-seed-base',str(seed),'--output-dir',str(target)]
                    log=HERE/'logs'/f'block_{idx:02d}_{policy}_{condition}.log'
                    print(f'START block={idx} policy={policy} setting={condition}',flush=True)
                    with log.open('a',encoding='utf-8')as stream:
                        process=subprocess.run(command,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,timeout=remaining)
                    require(process.returncode==0,f'Cell technical failure; inspect {log}')
                    rows=[json.loads(s)for s in (target/policy/ENV/f'{condition}.jsonl').read_text().splitlines()if s.strip()]
                    require(len(rows)==24 and sorted(r['episode_id']for r in rows)==list(range(24)),'Incomplete cell')
                    require(all(r['policy_seed']==seed+r['episode_id']and r['steps']==60 for r in rows),'Record identity/horizon mismatch')
                    complete.append((idx,condition));print(f'DONE block={idx} policy={policy} setting={condition}',flush=True)
            return complete
        except Exception:
            stop.set();raise
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
            futures=[pool.submit(worker,p,port)for p,port in [('octo-small',8767),('octo-base',8768)]]
            jobs=[f.result()for f in futures]
    except Exception as exc:
        (HERE/'TECHNICAL_FAILURE.json').write_text(json.dumps(dict(time_utc=utc(),reason=str(exc),partial_confirmatory_analysis_allowed=False),indent=2)+'\n',encoding='utf-8')
        raise
    (HERE/'COMPLETE.json').write_text(json.dumps(dict(complete=True,elapsed_seconds=time.monotonic()-started,jobs=jobs,
        frozen_plan_sha256=sha(HERE/'FROZEN_PLAN.json'),protocol_version='V3-controlled-initialization'),indent=2)+'\n',encoding='utf-8')
    print('CALIBRATION_V3_COMPLETE: no comparative analysis has been run',flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    action=ap.add_mutually_exclusive_group(required=True)
    action.add_argument('--freeze-only',action='store_true')
    action.add_argument('--execute',action='store_true')
    args=ap.parse_args()
    if args.freeze_only:freeze();print('V3 FROZEN; no policy evaluations executed')
    else:run()
