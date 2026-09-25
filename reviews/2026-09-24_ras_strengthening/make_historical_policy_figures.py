"""Preserve historical plot data while correcting legend and decoder semantics."""
from pathlib import Path
import hashlib,importlib.util,json,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.text import Text
A=Path(__file__).resolve().parent;R=A.parents[1];sys.path.insert(0,str(R/'scripts'))
out=A/'figure_inspection';out.mkdir(exist_ok=True)
labels={'identifiable (nominal)':'Nominal reference','invisible: controller':'Controller change',
'invisible: contact':'Contact/mass change','OpenVLA (7B, deterministic)':'OpenVLA (greedy decoding)',
'Octo-Small (stochastic)':'Octo-Small (sampled actions)'}
close=plt.close;records=[]
def coordinates(fig):
    values=[]
    for ax in fig.axes:
        for line in ax.lines:values.append([line.get_xdata().tolist() if hasattr(line.get_xdata(),'tolist') else list(line.get_xdata()),line.get_ydata().tolist() if hasattr(line.get_ydata(),'tolist') else list(line.get_ydata())])
        for collection in ax.collections:
            values.append(collection.get_offsets().tolist())
            if hasattr(collection,'get_segments'):values.append([v.tolist() for v in collection.get_segments()])
    return hashlib.sha256(json.dumps(values,sort_keys=True,default=lambda value:value.item()).encode()).hexdigest()
for script,fun,name in [('make_figures_v2.py','fig_torque_by_orientation','Fig3'),('make_figures.py','fig_delta','Fig4')]:
    source=R/'scripts'/script;digest=hashlib.sha256(source.read_bytes()).hexdigest()
    spec=importlib.util.spec_from_file_location('historical_'+name,source);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.OUT=out
    plt.rcParams.update({'pdf.fonttype':42,'font.family':'DejaVu Sans'})
    def export(fig=None):
        if hasattr(fig,'findobj'):
            before=coordinates(fig)
            for item in fig.findobj(match=Text):
                item.set_text(labels.get(item.get_text(),item.get_text()))
                item.set_color('black');item.set_fontfamily('DejaVu Sans')
            assert coordinates(fig)==before
            fig.savefig(out/(name+'_corrected.png'),dpi=220)
            dest=R/'submission/ras'/(name+'.pdf');fig.savefig(dest)
            records.append({'figure':name,'source':source.relative_to(R).as_posix(),'source_sha256':digest,'numeric_artist_coordinates_sha256':before,'numeric_coordinates_unchanged':True,'output_sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
        close(fig)
    plt.close=export
    try:
        function=getattr(m,fun)
        getattr(function,'__wrapped__',function)()
    finally:plt.close=close
    assert hashlib.sha256(source.read_bytes()).hexdigest()==digest
(A/'HISTORICAL_POLICY_FIGURE_PROVENANCE.json').write_text(json.dumps({'adapter_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'figures':records,'scope':'Historical protocol contrasts. Nominal is a reference, not an identified parameter. Greedy decoding does not imply execution determinism.'},indent=2)+'\n',encoding='utf-8')
