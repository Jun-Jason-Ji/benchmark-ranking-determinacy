"""Frozen-record sensitivity analyses; no GPU jobs, no historical output writes.

Requires numpy and scipy. Independent source parsing; legacy scripts are imported
only to compare their frozen working-model estimates and family inventory.
"""
from __future__ import annotations
import csv
import hashlib
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path
import sys
import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import make_core_table as legacy
import analyze_multiplicity as multiplicity
from task_configs import n_configs, is_deterministic

ALPHA = .05
CONDS = ['nominal', *legacy.INVISIBLE]
FILES = {}
CACHE = {}

def pinned(path):
    path = Path(path)
    data = path.read_bytes()
    FILES[path.relative_to(ROOT).as_posix()] = {
        'sha256': hashlib.sha256(data).hexdigest(), 'bytes':len(data)}
    return data

def tails(d, se, df=None):
    if se <= 0:
        return [1., 1.]  # no false certainty from an unestimated/zero variance
    if df is None:
        return [float(stats.norm.sf(d/se)), float(stats.norm.cdf(d/se))]
    return [float(stats.t.sf(d/se,df)),float(stats.t.cdf(d/se,df))]

def h_tails(d, sum_range_sq):
    if sum_range_sq <= 0:
        raise ValueError('Positive bounded-sum range required')
    return [min(1.,math.exp(-2*max(d,0.)**2/sum_range_sq)),
            min(1.,math.exp(-2*max(-d,0.)**2/sum_range_sq))]

def iut(tail_pairs):
    if not tail_pairs:
        return 1.
    return min(1.,2*min(max(t[0] for t in tail_pairs),max(t[1] for t in tail_pairs)))

def holm(ps):
    out=[False]*len(ps)
    for rank, idx in enumerate(sorted(range(len(ps)),key=lambda i:ps[i])):
        if ps[idx] > ALPHA/(len(ps)-rank):
            break
        out[idx]=True
    return out

def read_policy(sets, policy, env, condition):
    key=(tuple(sets.items()),policy,env,condition)
    if key in CACHE:return CACHE[key]
    use = legacy.sets_for(sets,policy)
    out=[]
    for label, directory in use.items():
        path=ROOT/directory/policy/env/f'{condition}.jsonl'
        if not path.exists():continue
        rows=[json.loads(line) for line in pinned(path).decode('utf-8').splitlines() if line.strip()]
        seen=set()
        for r in rows:
            eid=r['episode_id']
            if eid in seen:raise ValueError(f'Duplicate episode id: {path}:{eid}')
            seen.add(eid)
            if not isinstance(r['success'],bool):raise ValueError(f'Nonboolean success: {path}')
            if r['policy']!=policy or r['env_id']!=env or r['condition']!=condition:
                raise ValueError(f'Record scope mismatch: {path}')
            out.append(dict(config=eid%n_configs(env),episode_id=eid,
                            seed=r.get('policy_seed'),success=int(r['success']),
                            block=label.replace("'",''),source=path.relative_to(ROOT).as_posix()))
        for meta in ('run_meta.json','run_meta_variants_v1.json'):
            if (path.parent/meta).exists():pinned(path.parent/meta)
    CACHE[key]=out
    return out

def group_config(rows,N):
    out=defaultdict(list)
    for row in rows:out[row['config']].append(row)
    if set(out)!=set(range(N)):
        raise ValueError('Complete configuration inventory required; no intersection permitted')
    return out

def empirical(rows,N,zero_if_unrepeated=False):
    cfg=group_config(rows,N)
    means=np.array([np.mean([r['success'] for r in cfg[c]]) for c in range(N)])
    variances=[np.var([r['success'] for r in cfg[c]],ddof=1) if len(cfg[c])>=2 else None for c in range(N)]
    known=[v for v in variances if v is not None]
    fill=float(np.mean(known)) if known else (0. if zero_if_unrepeated else float(np.mean(means)*(1-np.mean(means))))
    v=sum((fill if variances[c] is None else variances[c])/len(cfg[c]) for c in range(N))/N**2
    return float(means.mean()),float(v),sum(x is None for x in variances),min(map(len,cfg.values())),max(map(len,cfg.values()))

def weighted(rows,N,sign):
    cfg=group_config(rows,N)
    return [(r,sign/(N*len(cfg[c]))) for c in range(N) for r in cfg[c]]

def bounded_result(ra,rb,N,mode,stochastic):
    records=weighted(ra,N,1)+weighted(rb,N,-1)
    d=sum(r['success']*w for r,w in records)
    groups=defaultdict(float)
    if mode=='seed' and not stochastic:
        return dict(delta=d,supported=False,reason='Greedy decoder ignores the nominal seed; independent seed clusters not justified',tails=[1.,1.])
    for j,(r,w) in enumerate(records):
        key=j if mode=='episode' else (r['seed'] if mode=='seed' else r['block'])
        if key is None:raise ValueError('Missing required random-seed identifier')
        groups[key]+=abs(w)
    R2=sum(v*v for v in groups.values())
    width=math.sqrt(.5*R2*math.log(2/ALPHA))
    return dict(delta=d,supported=True,clusters=len(groups),sum_range_sq=R2,
                lo=max(-1.,d-width),hi=min(1.,d+width),tails=h_tails(d,R2))

def complete_blocks(ra,rb,N,block_labels=None):
    pa,pb=defaultdict(list),defaultdict(list)
    for r in ra:pa[r['block']].append(r)
    for r in rb:pb[r['block']].append(r)
    labels=sorted(set(pa)&set(pb)) if block_labels is None else block_labels
    diffs=[]; used=[]
    for label in labels:
        if set(r['config'] for r in pa[label])!=set(range(N)) or set(r['config'] for r in pb[label])!=set(range(N)):
            continue
        a=group_config(pa[label],N);b=group_config(pb[label],N)
        diffs.append(float(np.mean([np.mean([r['success'] for r in a[c]])-np.mean([r['success'] for r in b[c]]) for c in range(N)])))
        used.append(label)
    return used,diffs

def block_t(diffs):
    if len(diffs)<2:return dict(supported=False,reason='Fewer than two complete blocks',tails=[1.,1.],n_blocks=len(diffs))
    d=float(np.mean(diffs));se=float(np.std(diffs,ddof=1)/math.sqrt(len(diffs)))
    if se==0:return dict(supported=False,reason='Zero observed block variance does not justify point certainty',tails=[1.,1.],n_blocks=len(diffs),delta=d)
    df=len(diffs)-1;width=stats.t.ppf(.975,df)*se
    return dict(supported=True,delta=d,se=se,df=df,lo=max(-1.,d-width),hi=min(1.,d+width),tails=tails(d,se,df),n_blocks=len(diffs))

def main():
    for file in ('scripts/make_core_table.py','scripts/analyze_multiplicity.py','scripts/task_configs.py','scripts/controller_sweep.py','scripts/controller_sweep_ms2.py','scripts/octo_policy_server.py','scripts/openvla_policy_server.py'):
        pinned(ROOT/file)
    legacy.SETS_MS3=dict(legacy.SEED_SETS_OCTO)
    results=[]; inventory=[]
    for label,env,override in legacy.TASKS:
        if 'CokeCan' in env:continue
        sets=override or legacy.SETS_MS3;N=n_configs(env)
        available=[p for p in legacy.POLICIES if any((ROOT/r/p/env).exists() for r in sets.values())]
        for a,b in itertools.combinations(available,2):
            expected_conditions=(['nominal','force_x0.5'] if env.endswith('-v0') and (is_deterministic(a)or is_deterministic(b)) else CONDS)
            cell=[]
            for condition in expected_conditions:
                old=legacy.delta(sets,a,b,env,condition)
                if old is None:continue
                ra=read_policy(sets,a,env,condition);rb=read_policy(sets,b,env,condition)
                if not ra or not rb:raise ValueError('One-sided scope')
                if old['n']!=N:raise ValueError('Historical incomplete configuration grid')
                ma,va,ia,mna,mxa=empirical(ra,N);mb,vb,ib,mnb,mxb=empirical(rb,N)
                d=ma-mb;se=math.sqrt(va+vb)
                _,va0,*_=empirical(ra,N,is_deterministic(a));_,vb0,*_=empirical(rb,N,is_deterministic(b))
                se0=math.sqrt(va0+vb0)
                block_labels,diffs=complete_blocks(ra,rb,N)
                methods={
                  'legacy_normal':dict(supported=True,delta=old['delta'],se=old['se'],lo=old['lo'],hi=old['hi'],tails=multiplicity.directional_pvalues(old['delta'],old['se'])),
                  'raw_legacy_variance_normal':dict(supported=True,delta=d,se=se0,lo=d-1.96*se0,hi=d+1.96*se0,tails=tails(d,se0)),
                  'raw_execution_normal':dict(supported=True,delta=d,se=se,lo=d-1.96*se,hi=d+1.96*se,tails=tails(d,se)),
                  'episode_hoeffding':bounded_result(ra,rb,N,'episode',True),
                  'seed_cluster_hoeffding':bounded_result(ra,rb,N,'seed',not(is_deterministic(a)or is_deterministic(b))),
                  'directory_cluster_hoeffding':bounded_result(ra,rb,N,'directory',True),
                }
                cell.append(dict(condition=condition,methods=methods,complete_blocks=block_labels,block_differences=diffs,
                    n_raw=[len(ra),len(rb)],n_imputed_variances=[ia,ib],per_config_counts=[[mna,mxa],[mnb,mxb]],
                    n_historical_after_outcome_dedup=[sum(map(len,legacy.raw_by_config(sets,a,env,condition).values())),sum(map(len,legacy.raw_by_config(sets,b,env,condition).values()))]))
                for policy,records in ((a,ra),(b,rb)):
                    for block in sorted(set(r['block']for r in records)):
                        rr=[r for r in records if r['block']==block]
                        inventory.append(dict(task=label,env=env,policy=policy,condition=condition,block=block,
                          episodes=len(rr),configurations=len(set(r['config']for r in rr)),expected_configurations=N,
                          distinct_seeds=len(set(r['seed']for r in rr)),sources=sorted(set(r['source']for r in rr))))
            if not cell:continue
            if len(cell)!=len(expected_conditions):raise ValueError(f'Missing declared condition: {label} {a} {b}')
            # The same complete blocks must support every condition; no outcome-based retention.
            common=sorted(set.intersection(*(set(c['complete_blocks'])for c in cell)))
            for c in cell:
                diff=dict(zip(c['complete_blocks'],c['block_differences']))
                c['methods']['complete_block_t']=block_t([diff[k]for k in common])
            results.append(dict(task=label,env=env,a=a,b=b,N=N,conditions=cell,complete_blocks_all_conditions=common))
    assert len(results)==17
    names=list(results[0]['conditions'][0]['methods'])
    comparisons=[]
    for method in names:
        row=[]
        for pair in results:
            cc=pair['conditions'];nom=next(c for c in cc if c['condition']=='nominal')['methods'][method]
            tails_all=[c['methods'][method]['tails']for c in cc]
            row.append(dict(task=pair['task'],a=pair['a'],b=pair['b'],p_point=iut([nom['tails']]),p_envelope=iut(tails_all),
                            complete_support=all(c['methods'][method]['supported']for c in cc),nominal_delta=nom.get('delta'),
                            lo=nom.get('lo'),hi=nom.get('hi'),complete_blocks=pair['complete_blocks_all_conditions']))
        hp=holm([r['p_point']for r in row]);he=holm([r['p_envelope']for r in row])
        for i,r in enumerate(row):r.update(holm_point=hp[i],holm_envelope=he[i])
        comparisons.append(dict(method=method,n_pairs=17,n_supported=sum(r['complete_support']for r in row),
          unadjusted_point=sum(r['p_point']<=.05 for r in row),unadjusted_envelope=sum(r['p_envelope']<=.05 for r in row),
          holm_point=sum(hp),holm_envelope=sum(he),rows=row))
    assert (comparisons[0]['holm_point'],comparisons[0]['holm_envelope'])==(9,5)
    dedup_inventory={json.dumps(r,sort_keys=True):r for r in inventory}
    output={'schema_version':1,'family':'Frozen family of 17 bridge pairs; six evaluated conditions except the two original-stack OpenVLA pairs (nominal and half torque); full configuration coverage required',
      'analysis_scope':'Frozen-record sensitivity; independent random seeds/runs remain assumptions, not measured facts',
      'method_comparisons':comparisons,'pairs':results,'scope_inventory':list(dedup_inventory.values())}
    (HERE/'ANALYSIS.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    with (HERE/'METHOD_COMPARISON.csv').open('w',encoding='utf-8',newline='')as f:
        writer=csv.DictWriter(f,fieldnames=[k for k in comparisons[0]if k!='rows']);writer.writeheader()
        writer.writerows({k:v for k,v in c.items()if k!='rows'}for c in comparisons)
    with (HERE/'PAIR_RESULTS.csv').open('w',encoding='utf-8',newline='')as f:
        writer=csv.DictWriter(f,fieldnames=['method',*comparisons[0]['rows'][0]]);writer.writeheader()
        for c in comparisons:writer.writerows(dict(method=c['method'],**r)for r in c['rows'])
    manifest={'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'files':FILES,'file_count':len(FILES)}
    (HERE/'INPUT_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    for r in comparisons:print({k:v for k,v in r.items()if k!='rows'},flush=True)
    print('complete-block counts',[(r['task'],r['a'],r['b'],r['complete_blocks_all_conditions'])for r in results],flush=True)

if __name__=='__main__':main()
