"""One process per task/pipeline; fixed 25-minute execution budget."""
import json,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
started=time.time();jobs=[]
for task in ['PickCube-v1','PushCube-v1']:
    for mode in ['pd_joint_delta_pos','pd_ee_delta_pos']:
        remaining=1440-(time.time()-started)
        if remaining<=0:raise TimeoutError('Fixed execution budget exhausted')
        name=f'{task}_{mode}'
        t=time.time()
        with (HERE/(name+'_v2.log')).open('w',encoding='utf-8') as stream:
            proc=subprocess.run([sys.executable,str(HERE/'run_confirmatory_v2.py'),'--task',task,'--mode',mode],
                                stdout=stream,stderr=subprocess.STDOUT,timeout=remaining)
        item=dict(job=name,returncode=proc.returncode,elapsed=time.time()-t)
        jobs.append(item)
        (HERE/'PROGRESS_V2.json').write_text(json.dumps(dict(jobs=jobs,elapsed=time.time()-started),indent=2),encoding='utf-8')
        print(json.dumps(item),flush=True)
        if proc.returncode:raise RuntimeError('Failed job: '+name)
print('All 80 cells complete',flush=True)
