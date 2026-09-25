"""Freeze and execute the fixed 384-rollout secondary study using existing servers.

Only --execute collects data. It requires the preceding V3 collection complete.
No server starts, restarts or auto-start configuration changes are performed.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,concurrent.futures,hashlib,http.client,json,os,subprocess,threading,time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
V3=HERE.parent/'calibration_confirmation_v3'
RESET=HERE.parent/'calibration_reset_validation'
PY=ROOT/'.venv-windows-ms3/Scripts/python.exe'
SEEDS=[431700100,557900200,683100300,809300400,947500500,1089700600,1231900700,1393100800]
ENV='PutSpoonOnTableClothInScene-v1'
PROTOCOL='SECONDARY-controlled-initialization-half-torque'

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
    hyp=json.loads((HERE/'HYPOTHESIS_FREEZE.json').read_text())
    require(hyp['v3_outcomes_analyzed']is False and hyp['additional_rollouts']==384,'Hypothesis freeze mismatch')
    require(sha(HERE/'PLAN.md')==hyp['plan_sha256'],'Hypothesis plan changed')
    require(sha(V3/'FROZEN_PLAN.json')==hyp['v3_frozen_plan_sha256'],'V3 freeze changed')
    validation=json.loads((HERE/'RESET_VALIDATION_RESULTS.json').read_text())
    require(validation['status']=='pass'and validation['cases']==48 and validation['configurations']==24
        and validation['exact_prior_full_state_and_rgb']is True
        and validation['unchanged_gripper_contact_mass']is True
        and validation['actual_physical_and_config_parameters_verified']is True,'Secondary reset validation failed')
    require(sha(HERE/'torque_reset_records.jsonl')==validation['records_sha256'],'Validation records changed')
    technical=json.loads((HERE/'FROZEN_TECHNICAL_PROTOCOL.json').read_text())
    require(sha(HERE/'FROZEN_TECHNICAL_PROTOCOL.json')==validation['frozen_protocol_sha256'],'Technical freeze changed')
    for rel,digest in technical['files'].items():require(sha(ROOT/rel)==digest,'Validated technical source changed: '+rel)
    v3freeze=json.loads((V3/'FROZEN_PLAN.json').read_text())
    for rel,digest in v3freeze['files'].items():require(sha(ROOT/rel)==digest,'A frozen V3 dependency changed: '+rel)
    paths=[HERE/name for name in ['PLAN.md','HYPOTHESIS_FREEZE.json','execute_cell.py','fresh_reset_torque.py','run_torque_control.py','analyze_torque.py','test_analysis.py','RESET_VALIDATION_RESULTS.json','torque_reset_records.jsonl','FROZEN_TECHNICAL_PROTOCOL.json','validate_torque_reset.py']]
    paths+=[V3/'FROZEN_PLAN.json',V3/'FROZEN_ANALYSIS.json',RESET/'reset_records.jsonl']
    paths+=[ROOT/rel for rel in v3freeze['files']]
    filemap={p.relative_to(ROOT).as_posix():sha(p)for p in paths}
    payload=dict(created_utc=utc(),protocol_version=PROTOCOL,seeds=SEEDS,episodes=384,
        independent_blocks_assumed=8,reset_validation_passed=True,shared_v3_nominal_rollouts=384,
        hypothesis_freeze_sha256=sha(HERE/'HYPOTHESIS_FREEZE.json'),files=filemap,
        execution_authorization='Coordinating agent authorized fixed 384-rollout secondary study after full V3 collection, no outcome-dependent continuation')
    path=HERE/'FROZEN_PLAN.json';af=HERE/'FROZEN_ANALYSIS.json'
    if path.exists():require(json.loads(path.read_text())['files']==filemap,'Existing freeze differs; do not overwrite')
    else:
        require(not(HERE/'data').exists(),'No pre-collection source freeze after data exist')
        path.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    digest=sha(HERE/'analyze_torque.py')
    if af.exists():require(json.loads(af.read_text())['analyzer_sha256']==digest,'Analysis freeze changed')
    else:af.write_text(json.dumps(dict(created_utc=utc(),analyzer_sha256=digest,tests_sha256=sha(HERE/'test_analysis.py'),
        hypothesis_freeze_sha256=sha(HERE/'HYPOTHESIS_FREEZE.json'),protocol_version=PROTOCOL,
        secondary_test='Two-sided majority-direction binomial test, all eight blocks retained; zeros match neither sign',
        joint_family='Holm over original V3 one-sided p and secondary two-sided p; shared baseline explicitly retained'),indent=2)+'\n',encoding='utf-8')
    return payload

def run():
    freeze()
    previous=json.loads((V3/'COMPLETE.json').read_text())
    require(previous.get('complete')is True and previous['frozen_plan_sha256']==sha(V3/'FROZEN_PLAN.json'),'V3 collection must finish before secondary collection')
    require(not(HERE/'RUNNING.json').exists()and not(HERE/'data').exists(),'Do not overwrite or silently resume a prior collection attempt')
    started=time.monotonic();deadline=started+75*60;stop=threading.Event()
    (HERE/'logs').mkdir(exist_ok=True)
    servers={p:health(port)for p,port in [('octo-small',8767),('octo-base',8768)]}
    for p,h in servers.items():require(h.get('model')==p and h.get('session_isolation')is True,'Unexpected policy server')
    (HERE/'SERVER_HEALTH.json').write_text(json.dumps(servers,indent=2)+'\n',encoding='utf-8')
    (HERE/'RUNNING.json').write_text(json.dumps(dict(pid=os.getpid(),started_utc=utc(),deadline_minutes=75,
        protocol_version=PROTOCOL,frozen_plan_sha256=sha(HERE/'FROZEN_PLAN.json')),indent=2)+'\n',encoding='utf-8')
    child_env=os.environ.copy();child_env['MS_ASSET_DIR']=str(ROOT/'data/maniskill-assets')
    def worker(policy,port):
        jobs=[]
        try:
            for block,seed in enumerate(SEEDS,1):
                require(not stop.is_set(),'Other worker failed technical gate')
                remaining=deadline-time.monotonic();require(remaining>0,'Fixed wall-time budget exceeded')
                target=HERE/'data'/f'block_{block:02d}'
                command=[str(PY),str(HERE/'execute_cell.py'),'--policy-name',policy,'--policy-url',f'http://127.0.0.1:{port}',
                    '--condition','forcehalf','--policy-seed-base',str(seed),'--output-dir',str(target)]
                log=HERE/'logs'/f'block_{block:02d}_{policy}_forcehalf.log'
                print(f'START block={block} policy={policy} setting=forcehalf',flush=True)
                with log.open('a',encoding='utf-8')as stream:
                    process=subprocess.run(command,cwd=ROOT,env=child_env,stdout=stream,stderr=subprocess.STDOUT,timeout=remaining)
                require(process.returncode==0,'Technical failure; inspect '+str(log))
                rows=[json.loads(s)for s in (target/policy/ENV/'forcehalf.jsonl').read_text().splitlines()if s.strip()]
                require(len(rows)==24 and sorted(r['episode_id']for r in rows)==list(range(24)),'Incomplete cell')
                require(all(r['policy_seed']==seed+r['episode_id']and r['steps']==60 for r in rows),'Identity/horizon mismatch')
                jobs.append((block,'forcehalf'));print(f'DONE block={block} policy={policy} setting=forcehalf',flush=True)
            return jobs
        except Exception:stop.set();raise
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
            futures=[pool.submit(worker,p,port)for p,port in [('octo-small',8767),('octo-base',8768)]]
            jobs=[f.result()for f in futures]
    except Exception as exc:
        (HERE/'TECHNICAL_FAILURE.json').write_text(json.dumps(dict(time_utc=utc(),reason=str(exc),partial_analysis_allowed=False),indent=2)+'\n')
        raise
    (HERE/'COMPLETE.json').write_text(json.dumps(dict(complete=True,elapsed_seconds=time.monotonic()-started,jobs=jobs,
        frozen_plan_sha256=sha(HERE/'FROZEN_PLAN.json'),protocol_version=PROTOCOL),indent=2)+'\n',encoding='utf-8')
    print('SECONDARY_TORQUE_COMPLETE: no comparative analysis has been run',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--freeze-only',action='store_true');group.add_argument('--execute',action='store_true')
    args=parser.parse_args()
    if args.freeze_only:freeze();print('SECONDARY TORQUE FROZEN; no policy evaluations executed')
    else:run()
