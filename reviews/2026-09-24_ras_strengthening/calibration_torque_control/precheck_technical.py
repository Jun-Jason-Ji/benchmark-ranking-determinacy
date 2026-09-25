"""Outcome-blind technical check of completed secondary cells and V3 pairing."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
import numpy as np
import analyze_torque as a

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import controller_sweep
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def rows(p):return [json.loads(s)for s in p.read_text(encoding='utf-8').splitlines()if s.strip()]
def main():
    freeze=read(HERE/'FROZEN_PLAN.json')
    for rel,digest in freeze['files'].items():a.require(a.sha(ROOT/rel)==digest,'Frozen source changed: '+rel)
    completed=[];issues=[]
    for path in sorted((HERE/'data').rglob('forcehalf_audit.jsonl')):
        audit=rows(path)
        if not any(e['kind']=='cell_complete'for e in audit):continue
        d=path.parent;policy=d.parent.name;block=int(d.parents[1].name.removeprefix('block_'));base=a.SEEDS[block-1]
        try:
            records=rows(d/'forcehalf.jsonl')
            a.require(len(records)==24 and sorted(r['episode_id']for r in records)==list(range(24)),'Incomplete configurations')
            a.require(all(r['steps']==60 and r['policy_seed']==base+r['episode_id']and r['protocol_version']==a.PROTOCOL for r in records),'Horizon/seed/protocol mismatch')
            eff=read(d/'forcehalf_summary.json')['conditions']['forcehalf']['effective']
            for key,factor,nkey in [('stiffness',1.,'arm_stiffness'),('damping',1.,'arm_damping'),('force_limit',.5,'arm_force_limit')]:
                a.require(np.allclose(eff['built_'+key],np.asarray(controller_sweep.NOMINAL[nkey])*factor,rtol=2e-6,atol=1e-5),'Built controller mismatch')
            a.require(eff['delay_steps']==0 and eff['horizon']==60 and eff['control_freq']==5 and eff['sim_freq']==500,'Timing mismatch')
            baseline=rows(a.V3/'data'/f'block_{block:02d}'/policy/a.ENV/'nominal_audit.jsonl')
            ref={e['seed']:e for e in baseline if e['kind']=='environment_reset'}
            resets={e['seed']:e for e in audit if e['kind']=='environment_reset'}
            a.require(set(resets)==set(range(24)),'Missing reset records')
            for ep,e in resets.items():
                a.require((e['state_sha256'],e['image_sha256'])==(ref[ep]['state_sha256'],ref[ep]['image_sha256']),'Physical state/image mismatch')
                a.require(e['gripper']==ref[ep]['gripper']and e['object_contact']==ref[ep]['object_contact'],'Gripper/contact mismatch')
                a.require(e['actual_joints']['friction']==ref[ep]['actual_joints']['friction'],'Joint friction changed')
            pr=[e for e in audit if e['kind']=='policy_reset']
            a.require({e['requested_seed']for e in pr}==set(range(base,base+24)),'Missing reseeds')
            a.require(all(e['response'].get('rng_mode')=='reseed'and e['response'].get('rng_seed')==e['requested_seed']and e['response'].get('session')==e['session']for e in pr),'Bad policy RNG lifecycle')
            closed=[e for e in audit if e['kind']=='episode_closed']
            a.require({e['episode_id']for e in closed}==set(range(24))and all(e['closed_scene_and_agent_cleared']and e['active_parameters_unchanged']for e in closed),'Incomplete lifecycle')
            completed.append(dict(block=block,policy=policy,episodes=24))
        except (ValueError,KeyError,FileNotFoundError)as exc:issues.append(dict(block=block,policy=policy,issue=str(exc)))
    result=dict(created_utc=datetime.now(timezone.utc).isoformat(),completed_cells=len(completed),passed=not issues,
        checks=completed,issues=issues,success_fields_accessed=False,comparative_analysis_computed=False)
    out=HERE/'technical_prechecks';out.mkdir(exist_ok=True)
    (out/('check_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k!='checks'},indent=2))
    if issues:raise SystemExit(2)
if __name__=='__main__':main()
