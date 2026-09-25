"""Known-null synthetic stress test using frozen observed observation inventories.

No estimate of the actual study's false-declaration rate is made. Outcomes are
new Bernoulli(.5) simulations, not bootstrap resamples or new robot trials.
"""
import json
import math
from pathlib import Path
import numpy as np
from scipy import stats
import reanalyze_statistics as audit

HERE=Path(__file__).resolve().parent
N_SIM=20000
BATCH=500
SEED=20260924

def design(rows,N):
    blocks=sorted(set(r['block']for r in rows))
    block_index=np.array([blocks.index(r['block'])for r in rows])
    config_index=np.array([r['config']for r in rows])
    n=np.bincount(config_index,minlength=N)
    cfg=np.eye(N)[config_index]
    weights=(1/n[config_index])/N
    grid=np.zeros((len(rows),len(blocks)*N))
    for i,r in enumerate(rows):grid[i,blocks.index(r['block'])*N+r['config']]=1
    counts=grid.sum(axis=0).reshape(len(blocks),N)
    if (counts==0).any():raise ValueError('Complete nominal census blocks required')
    grid=grid/counts.reshape(-1)
    return dict(blocks=blocks,index=block_index,cfg=cfg,n=n,weights=weights,grid=grid,N=N)

def evaluate(y,z,dsg):
    N=dsg['N'];n=dsg['n'];B=len(dsg['blocks'])
    sy=y@dsg['cfg'];sz=z@dsg['cfg']
    delta=((sy-sz)/n).mean(axis=1)
    vy=(sy-sy**2/n)/(n-1);vz=(sz-sz**2/n)/(n-1)
    se=np.sqrt(((vy+vz)/n).sum(axis=1))/N
    pnorm=2*stats.norm.sf(np.divide(np.abs(delta),se,out=np.zeros_like(delta),where=se>0))
    gy=(y@dsg['grid']).reshape(-1,B,N);gz=(z@dsg['grid']).reshape(-1,B,N)
    dd=(gy-gz).mean(axis=(1,2))
    dse=np.sqrt((gy.var(axis=1,ddof=1)+gz.var(axis=1,ddof=1)).sum(axis=1)/B)/N
    pdir=2*stats.norm.sf(np.divide(np.abs(dd),dse,out=np.zeros_like(dd),where=dse>0))
    bd=(gy-gz).mean(axis=2);bdelta=bd.mean(axis=1);bse=bd.std(axis=1,ddof=1)/math.sqrt(B)
    pt=2*stats.t.sf(np.divide(np.abs(bdelta),bse,out=np.zeros_like(bdelta),where=bse>0),B-1)
    ranges_episode=2*np.sum(dsg['weights']**2)
    ph=np.minimum(1.,2*np.exp(-2*delta**2/ranges_episode))
    # Same-directory policies are allowed to depend arbitrarily, so range is total |weight|.
    group_weights=np.bincount(dsg['index'],weights=2*dsg['weights'])
    ranges_block=np.sum(group_weights**2)
    pb=np.minimum(1.,2*np.exp(-2*delta**2/ranges_block))
    return dict(episode_normal=pnorm,directory_normal=pdir,complete_block_t=pt,
                episode_hoeffding=ph,directory_cluster_hoeffding=pb)

def main():
    rng=np.random.default_rng(SEED)
    audit.legacy.SETS_MS3=dict(audit.legacy.SEED_SETS_OCTO)
    records=[]
    for task,env in [('eggplant','PutEggplantInBasketScene-v1'),('spoon','PutSpoonOnTableClothInScene-v1')]:
        N=audit.n_configs(env)
        ra=audit.read_policy(audit.legacy.SETS_MS3,'octo-small',env,'nominal')
        rb=audit.read_policy(audit.legacy.SETS_MS3,'octo-base',env,'nominal')
        # Both policies have exactly the same nominal record inventory in these examples.
        assert [(r['block'],r['episode_id'])for r in ra]==[(r['block'],r['episode_id'])for r in rb]
        dsg=design(ra,N)
        for rho in [0.,.05,.20]:
            counters={}
            for start in range(0,N_SIM,BATCH):
                size=min(BATCH,N_SIM-start);B=len(dsg['blocks']);M=len(ra)
                latent=rng.standard_normal((2,size,B))
                innovations=rng.standard_normal((2,size,M))
                zz=np.sqrt(rho)*latent[:,:,dsg['index']]+np.sqrt(1-rho)*innovations
                yy=(zz>0).astype(float)
                ps=evaluate(yy[0],yy[1],dsg)
                for method,pvalues in ps.items():
                    counters[method]=counters.get(method,0)+int(np.sum(pvalues<=.05))
            for method,k in counters.items():
                lo=0. if k==0 else stats.beta.ppf(.025,k,N_SIM-k+1)
                hi=1. if k==N_SIM else stats.beta.ppf(.975,k+1,N_SIM-k)
                records.append(dict(task=task,N=N,episodes_per_policy=len(ra),blocks=len(dsg['blocks']),
                    latent_correlation=rho,binary_within_block_correlation=2/math.pi*math.asin(rho),method=method,
                    false_declarations=k,trials=N_SIM,rate=k/N_SIM,monte_carlo_95_interval=[lo,hi]))
                print(task,rho,method,k/N_SIM,flush=True)
    output={'seed':SEED,'simulations_per_design_scenario':N_SIM,
      'null':'Each observation marginally Bernoulli(0.5); each policy true finite-configuration mean 0.5; true gap exactly zero.',
      'dependence':'Independent policy-specific block Gaussian shocks and observation innovations; threshold at zero; latent rho=0,.05,.20. Blocks independent. Same observation inventory as frozen nominal runs.',
      'scope':'Synthetic per-pair, single-setting falsification check. Not an estimate of actual dependence, actual error rate, or 17-pair family-wise error. Perfectly shared setting outcomes would make a null IUT identical to this test; no simulated setting independence is assumed.',
      'results':records}
    (HERE/'NULL_STRESS.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
