"""Redraw historical summary with explicit contrast labels; preserve its calculations."""
from pathlib import Path
import hashlib,importlib.util,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.text import Text
A=Path(__file__).resolve().parent;R=A.parents[1];source=R/'scripts/make_figures_v2.py'
spec=importlib.util.spec_from_file_location('historical_figure_source',source);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
plt.rcParams['pdf.fonttype']=42
source_sha=hashlib.sha256(source.read_bytes()).hexdigest()
out=A/'figure_inspection';out.mkdir(exist_ok=True);m.OUT=out
close=plt.close
mapping={
 'Implementation build\n(shift in Δ)':'Historical build contrast\n(change in Δ)',
 'Calibration-invisible parameter,\ntorque limit (shift in Δ)':'Historical torque-limit contrast\n(change in Δ)',
 'Robot texture variant, no physics\n(span of Δ over 4 settings)':'Robot texture variants\n(span of Δ over 4 variants)',
 'Not reduced by\nadditional\nevaluation runs':'Contrasts across\nconditions; not\nsampling precision',
}
def export(fig=None):
    if hasattr(fig,'findobj'):
        for ax in fig.axes:
            labels=[mapping.get(t.get_text(),t.get_text()).replace('Evaluation noise,','Illustrative noise,') for t in ax.get_yticklabels()]
            ax.set_yticks(ax.get_yticks(),labels)
        for item in fig.findobj(match=Text):
            label=item.get_text();item.set_text(mapping.get(label,label).replace('Evaluation noise,','Illustrative noise,'))
            item.set_color('black');item.set_fontfamily('DejaVu Sans')
        fig.savefig(out/'historical_summary.png',dpi=220)
        fig.savefig(R/'submission/ras/Fig2.pdf')
    close(fig)
plt.close=export
try:values=m.fig_uncertainty_budget()
finally:plt.close=close
assert [round(1.96*values['seed_sd']/n**.5,3)for n in [1,3,10]]==[.132,.076,.042]
assert round(values['drift_max'],3)==.109 and round(values['shift'],3)==.121
assert round(m.texture_variant_delta_span()[0],3)==.160
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_sha
(A/'HISTORICAL_FIGURE_PROVENANCE.json').write_text(json.dumps({'source':source.relative_to(R).as_posix(),'source_sha256':source_sha,'adapter_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'calculation_unchanged':True,'values':values,'output_sha256':hashlib.sha256((R/'submission/ras/Fig2.pdf').read_bytes()).hexdigest(),'scope':'Historical execution-protocol contrasts, not isolated causal parameter effects. Illustrative noise projections retain their working assumptions.'},indent=2)+'\n',encoding='utf-8')
