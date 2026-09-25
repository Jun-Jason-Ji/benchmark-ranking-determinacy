"""Instrument the unchanged historical evaluator without changing policy actions."""
from pathlib import Path
import hashlib,json,sys,os,time
R=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(R/'scripts'))
import controller_sweep as sweep
import numpy as np
import gymnasium as gym

args=sys.argv[1:]
def arg(name):return args[args.index(name)+1]
out=Path(arg('--output-dir'))/arg('--policy-name')/arg('--env-id')
out.mkdir(parents=True,exist_ok=True)
cond=arg('--conditions');audit=out/(cond+'_audit.jsonl')
def emit(kind,**values):
    with audit.open('a',encoding='utf-8') as f:f.write(json.dumps({'kind':kind,'time_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),**values})+'\n')

reset=sweep.PolicyClient.reset
def checked_reset(self,instruction,seed,config=None):
    response=reset(self,instruction,seed,config)
    assert response.get('ok') and response.get('session')==self.session,response
    assert response.get('rng_mode')=='reseed' and response.get('rng_seed')==seed,response
    emit('policy_reset',requested_seed=seed,session=self.session,response=response)
    return response
sweep.PolicyClient.reset=checked_reset
step=sweep.PolicyClient.step
def checked_step(self,img):
    response=step(self,img)
    assert response.get('session')==self.session,response
    assert np.isfinite(response['action']).all()
    return response
sweep.PolicyClient.step=checked_step
make=gym.make
class RecordedEnvironment(gym.Wrapper):
    def reset(self,**kwargs):
        obs,info=self.env.reset(**kwargs)
        state=sweep.to_json(self.unwrapped.get_state_dict())
        rgb=obs['sensor_data']['3rd_view_camera']['rgb'][0].detach().cpu().numpy()
        emit('environment_reset',seed=kwargs.get('seed'),state=state,
             state_sha256=hashlib.sha256(json.dumps(state,sort_keys=True).encode()).hexdigest(),
             image_sha256=hashlib.sha256(rgb.tobytes()).hexdigest())
        return obs,info
def recorded_make(*args,**kwargs):return RecordedEnvironment(make(*args,**kwargs))
gym.make=recorded_make
emit('cell_start',argv=args,source_sha256={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),R/'scripts/controller_sweep.py',R/'scripts/octo_policy_server.py',R/'scripts/ms3_windows_compat.py']})
sweep.main()
emit('cell_complete')
