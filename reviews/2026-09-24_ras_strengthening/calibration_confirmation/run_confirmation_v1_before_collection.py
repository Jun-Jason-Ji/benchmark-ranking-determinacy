"""Run the fixed eight-block study; never launch or reconfigure a service."""
from pathlib import Path
import concurrent.futures,hashlib,http.client,json,subprocess,time,sys
HERE=Path(__file__).resolve().parent;R=HERE.parents[2]
PY=R/'.venv-windows-ms3/Scripts/python.exe'
SEEDS=[431700100,557900200,683100300,809300400,947500500,1089700600,1231900700,1393100800]
ENV='PutSpoonOnTableClothInScene-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def health(port):
    c=http.client.HTTPConnection('127.0.0.1',port,timeout=8);c.request('GET','/health');r=c.getresponse();assert r.status==200
    data=json.loads(r.read());c.close();return data
def freeze():
    files=[HERE/'PLAN.md',HERE/'execute_cell.py',Path(__file__),R/'scripts/controller_sweep.py',R/'scripts/octo_policy_server.py',R/'scripts/ms3_windows_compat.py',R/'scripts/task_configs.py']
    payload={'created_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'seeds':SEEDS,'episodes':768,'files':{p.relative_to(R).as_posix():sha(p) for p in files}}
    p=HERE/'FROZEN_PLAN.json'
    if p.exists():
        old=json.loads(p.read_text());assert old['files']==payload['files'] and old['seeds']==SEEDS
    else:p.write_text(json.dumps(payload,indent=2)+'\n')
def run():
    freeze();start=time.monotonic();deadline=start+150*60
    (HERE/'logs').mkdir(exist_ok=True)
    servers={p:health(port) for p,port in [('octo-small',8767),('octo-base',8768)]}
    for p,h in servers.items():assert h['model']==p and h.get('session_isolation')
    (HERE/'SERVER_HEALTH.json').write_text(json.dumps(servers,indent=2)+'\n')
    def worker(policy,port):
        done=[]
        for idx,seed in enumerate(SEEDS):
            for cond in (['nominal','fitted'] if idx%2==0 else ['fitted','nominal']):
                assert time.monotonic()<deadline,'Fixed evaluation time budget exceeded; do not infer from partial design.'
                target=HERE/'data'/f'block_{idx+1:02d}'
                command=[str(PY),str(HERE/'execute_cell.py'),'--env-id',ENV,'--policy-url',f'http://127.0.0.1:{port}',
                         '--policy-name',policy,'--preset','fitted_v1' if cond=='fitted' else 'sweep_v1','--conditions',cond,
                         '--episodes','24','--episode-offset','0','--policy-seed-base',str(seed),'--output-dir',str(target)]
                log=HERE/'logs'/f'block_{idx+1:02d}_{policy}_{cond}.log'
                print(f'START block={idx+1} policy={policy} setting={cond}',flush=True)
                with log.open('a',encoding='utf-8') as f:r=subprocess.run(command,cwd=R,stdout=f,stderr=subprocess.STDOUT)
                assert r.returncode==0,(policy,idx,cond,str(log))
                records=[json.loads(x) for x in (target/policy/ENV/(cond+'.jsonl')).read_text().splitlines()]
                assert len(records)==24 and sorted(x['episode_id'] for x in records)==list(range(24))
                assert all(x['policy_seed']==seed+x['episode_id'] and x['steps']==60 for x in records)
                done.append((idx+1,cond));print(f'DONE block={idx+1} policy={policy} setting={cond}',flush=True)
        return done
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(worker,p,port) for p,port in [('octo-small',8767),('octo-base',8768)]]
        result=[f.result() for f in futures]
    (HERE/'COMPLETE.json').write_text(json.dumps({'complete':True,'elapsed_seconds':time.monotonic()-start,'jobs':result,'frozen_plan_sha256':sha(HERE/'FROZEN_PLAN.json')},indent=2)+'\n')
    print('CALIBRATION_CONFIRMATION_COMPLETE',flush=True)
if __name__=='__main__':
    if '--freeze-only' in sys.argv:freeze();print('FROZEN; no evaluations executed')
    else:run()
