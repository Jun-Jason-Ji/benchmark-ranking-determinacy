"""Read-only CPU reconstruction of Section 7.4's current mechanism scope."""
from pathlib import Path
import argparse
import sys,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import analyze_torque_mechanism as m
import make_figures_v2 as fig
ENV='PutEggplantInBasketScene-v1'
policies=['openvla-7b-4bit','octo-small','octo-base','octo-small@hist1','octo-base@hist1']
results={}
files={}
for p in policies:
    sets=m.DET_SETS if m.is_deterministic(p) else m.OCTO_SETS
    a=fig.merged(sets,p,'nominal');b=fig.merged(sets,p,'force_x0.5')
    ar=fig.runs(sets,p,'nominal');br=fig.runs(sets,p,'force_x0.5')
    na={c:sum(c in r for r in ar) for c in a};nb={c:sum(c in r for r in br) for c in b}
    common=sorted(set(a)&set(b));assert len(common)==64
    changes={c:b[c]-a[c] for c in common}
    orient=[float(np.mean([changes[c] for c in common if c%8==q])) for q in range(8)]
    zero=[c for c in common if a[c]==0]
    results[p]={'configurations':len(common),'nominal_mean':float(np.mean([a[c] for c in common])),
        'force_mean':float(np.mean([b[c] for c in common])),'mean_change':float(np.mean(list(changes.values()))),
        'improved':sum(v>0.01 for v in changes.values()),'degraded':sum(v<-.01 for v in changes.values()),
        'unchanged':sum(-.01<=v<=.01 for v in changes.values()),
        'gain_nominal_correlation':float(np.corrcoef([a[c] for c in common],[changes[c] for c in common])[0,1]),
        'nominal_zero_configs':len(zero),'rescued_configs':sum(b[c]>0 for c in zero),
        'orientation_changes':orient,'positive_orientations':sum(v>0 for v in orient),
        'orientation_range':[min(orient),max(orient)],
        'nominal_run_count_range':[min(na.values()),max(na.values())],
        'force_run_count_range':[min(nb.values()),max(nb.values())]}
    old_a,_=m.merged(p,ENV,'nominal');old_b,_=m.merged(p,ENV,'force_x0.5')
    results[p]['legacy_helper_max_abs_difference_from_figure_estimator']=max(max(abs(a[c]-old_a[c]),abs(b[c]-old_b[c])) for c in common)
    for folder in sets.values():
        for cond in ['nominal','force_x0.5']:
            f=ROOT/folder/p/ENV/(cond+'.jsonl')
            if f.exists():files[f.relative_to(ROOT).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
out={'date':'2026-09-23','method':'Existing Figure3 make_figures_v2.py merged/runs estimator, which removes record-identical whole deterministic runs per Section5.3; per-config >0.01 improved, <-0.01 degraded as in analyze_torque_mechanism.py. Legacy mechanism helper does not remove record-identical whole runs, hence primary results use the current figure estimator consistently.',
     'analysis_scripts':{name:hashlib.sha256((ROOT/'scripts'/name).read_bytes()).hexdigest() for name in ['analyze_torque_mechanism.py','make_figures_v2.py']},
     'octo_seed_sets':list(m.OCTO_SETS),'results':results,'input_sha256':files,
     'historical_values':{'openvla':{'improved':16,'unchanged':42,'degraded':6,'gain_nominal_correlation':-.44,'nominal_zero_configs':51,'rescued_configs':13,'positive_orientations':7,'orientation_range':[-.04,.29]},'octo_small':{'improved':15,'degraded':15,'positive_orientations':2}},
     'no_new_experiment':True}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out', type=Path, required=True, help='New JSON output outside the input snapshot')
args=parser.parse_args()
if args.out.exists(): parser.error('Output already exists; use a new path.')
args.out.parent.mkdir(parents=True, exist_ok=True)
args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(results,indent=2))

