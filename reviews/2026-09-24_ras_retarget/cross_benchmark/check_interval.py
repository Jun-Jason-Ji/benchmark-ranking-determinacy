"""Exact small-n coverage check, independent of the robot outcome files."""
import json, math
from pathlib import Path
import numpy as np
from scipy.special import gammaln, xlogy
from scipy.stats import beta
HERE=Path(__file__).resolve().parent
n=16
states=[]
for kp in range(n+1):
    for km in range(n-kp+1):
        p_lo=0 if kp==0 else beta.ppf(.0125,kp,n-kp+1)
        p_hi=1 if kp==n else beta.ppf(.9875,kp+1,n-kp)
        m_lo=0 if km==0 else beta.ppf(.0125,km,n-km+1)
        m_hi=1 if km==n else beta.ppf(.9875,km+1,n-km)
        k=np.array([kp,km,n-kp-km])
        states.append((k,float(p_lo-m_hi),float(p_hi-m_lo)))
worst=dict(coverage=1.0)
max_false_direction=dict(probability=0.0)
cases=0
for ip in range(21):
    for im in range(21-ip):
        probs=np.array([ip/20,im/20,1-(ip+im)/20])
        delta=probs[0]-probs[1]
        covered=false=total=0.0
        for k,lo,hi in states:
            mass=float(np.exp(gammaln(n+1)-gammaln(k+1).sum()+xlogy(k,probs).sum()))
            total+=mass
            if lo-1e-12<=delta<=hi+1e-12: covered+=mass
            if (delta<=0 and lo>0) or (delta>=0 and hi<0): false+=mass
        assert abs(total-1)<1e-10
        if covered<worst['coverage']: worst=dict(coverage=covered,p_plus=probs[0],p_minus=probs[1])
        if false>max_false_direction['probability']: max_false_direction=dict(probability=false,p_plus=probs[0],p_minus=probs[1])
        cases+=1
assert worst['coverage']>=.95-1e-10
assert max_false_direction['probability']<=.05+1e-10
report=dict(status='passed',n=n,probability_grid_cases=cases,
            outcome_multinomial_states=len(states),worst_grid_coverage=worst,
            maximum_false_direction_on_grid=max_false_direction,
            limitation='Finite numerical verification is not a replacement for the Clopper–Pearson union-bound argument.')
(HERE/'INTERVAL_CHECK.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
