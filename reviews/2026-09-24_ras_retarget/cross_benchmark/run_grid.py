"""Execute the fixed native-task external check, sequentially on one GPU."""
import hashlib, json, subprocess, sys, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
out=HERE/'full_grid'
out.mkdir(exist_ok=True)
plan_sha=hashlib.sha256((HERE/'PLAN.md').read_bytes()).hexdigest()
jobs=[]
for task in ['PickCube-v1','PushCube-v1']:
    for mode in ['pd_joint_delta_pos','pd_ee_delta_pos']:
        for setting in ['nominal','gain_half','gain_double','force_half','force_double']:
            name=f'{task}_{mode}_{setting}'
            dest=out/(name+'.json')
            if dest.exists():
                jobs.append(dict(name=name,status='existing_not_overwritten'))
                continue
            cmd=[sys.executable,str(HERE/'run_native_policies.py'),'--env-id',task,
                 '--mode',mode,'--num-envs','256','--setting',setting,
                 '--seed-start','2026092500','--output','full_grid/'+name+'.json']
            started=time.time()
            with (out/(name+'.log')).open('w',encoding='utf-8') as f:
                p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=180)
            job=dict(name=name,returncode=p.returncode,elapsed=time.time()-started)
            jobs.append(job)
            (HERE/'GRID_PROGRESS.json').write_text(json.dumps(dict(plan_sha256=plan_sha,jobs=jobs),indent=2),encoding='utf-8')
            print(json.dumps(job),flush=True)
            if p.returncode: raise RuntimeError(f'Cell failed: {name}; inspect its log.')
print('All 20 cells completed',flush=True)
