"""Outcome-blind diagnosis of the first completed cells' initial-state gate."""
import hashlib,json,math
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BASE=HERE/'data/block_01'
ENV='PutSpoonOnTableClothInScene-v1'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load(policy,condition):
    path=BASE/policy/ENV/f'{condition}_audit.jsonl'
    all_events=[json.loads(s)for s in path.read_text().splitlines()if s.strip()]
    assert any(r['kind']=='cell_complete'for r in all_events)
    return path,{r['seed']:r for r in all_events if r['kind']=='environment_reset'}

def main():
    pairs=[(('octo-base','nominal'),('octo-small','nominal')),
           (('octo-small','nominal'),('octo-small','fitted'))]
    outputs=[];sources={}
    for aa,bb in pairs:
        pa,a=load(*aa);pb,b=load(*bb)
        for p in [pa,pb]:sources[p.relative_to(ROOT).as_posix()]=sha(p)
        rows=[]
        for ep in range(24):
            ea,eb=a[ep],b[ep]
            for actor in ea['state']['actors']:
                x=np.asarray(ea['state']['actors'][actor],dtype=float).reshape(-1)
                y=np.asarray(eb['state']['actors'][actor],dtype=float).reshape(-1)
                assert x.shape==y.shape==(13,)
                qx=x[3:7]/np.linalg.norm(x[3:7]);qy=y[3:7]/np.linalg.norm(y[3:7])
                angle=2*math.acos(min(1.,abs(float(qx@qy))))
                rows.append(dict(config=ep,actor=actor,position_distance_mm=float(np.linalg.norm(x[:3]-y[:3])*1000),
                    rotation_distance_degrees=angle*180/math.pi,
                    linear_velocity_difference_m_per_s=float(np.linalg.norm(x[7:10]-y[7:10])),
                    angular_velocity_difference_rad_per_s=float(np.linalg.norm(x[10:13]-y[10:13])),
                    state_identical=ea['state_sha256']==eb['state_sha256'],image_identical=ea['image_sha256']==eb['image_sha256']))
        outputs.append(dict(a=aa,b=bb,rows=rows,
            matched_initial_states=sum(a[ep]['state_sha256']==b[ep]['state_sha256']for ep in range(24)),
            matched_initial_images=sum(a[ep]['image_sha256']==b[ep]['image_sha256']for ep in range(24)),
            maximum_position_distance_mm=max(x['position_distance_mm']for x in rows),
            maximum_rotation_distance_degrees=max(x['rotation_distance_degrees']for x in rows)))
    for rel in ['.venv-windows-ms3/Lib/site-packages/mani_skill/agents/base_agent.py',
                '.venv-windows-ms3/Lib/site-packages/mani_skill/envs/sapien_env.py',
                '.venv-windows-ms3/Lib/site-packages/mani_skill/envs/tasks/digital_twins/bridge_dataset_eval/base_env.py']:
        sources[rel]=sha(ROOT/rel)
    result=dict(scope='Outcome-blind technical failure diagnosis: only initial reset states and implementation sources',
                success_fields_read=False,direction_or_p_value_computed=False,comparisons=outputs,input_sha256=sources)
    (HERE/'INITIAL_STATE_FAILURE.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    for row in outputs:print(json.dumps({k:v for k,v in row.items()if k!='rows'}))

if __name__=='__main__':main()
