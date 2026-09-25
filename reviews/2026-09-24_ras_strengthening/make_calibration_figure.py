"""Plot all frozen controlled-study blocks after both studies are complete."""
from pathlib import Path
import hashlib,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
A=Path(__file__).resolve().parent;R=A.parents[1]
vp=A/'calibration_confirmation_v3/ANALYSIS.json';tp=A/'calibration_torque_control/ANALYSIS.json'
v=json.loads(vp.read_text());t=json.loads(tp.read_text())
assert v['status']==t['status']=='complete' and len(v['blocks'])==len(t['blocks'])==8
panels=[(v['blocks'],v['secondary']['t_working_model'],'(a) Replay-preferred − nominal','#0072B2','o'),
        (t['blocks'],t['mean_sensitivity']['t_working_model'],'(b) Half torque − nominal','#D55E00','s')]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.labelcolor':'black',
                    'text.color':'black','xtick.color':'black','ytick.color':'black','pdf.fonttype':42})
fig,axes=plt.subplots(1,2,figsize=(7.2,3.7),sharex=True,sharey=True)
extent=.15
for blocks,model,_,_,_ in panels:
    extent=max(extent,*[abs(b['shift']) for b in blocks])
    if model['interval_available']:extent=max(extent,abs(model['lower']),abs(model['upper']))
limit=math.ceil((extent+.045)*10)/10
for ax,(blocks,model,title,color,marker) in zip(axes,panels):
    assert [b['block'] for b in blocks]==list(range(1,9))
    ax.scatter([b['shift'] for b in blocks],np.arange(8),color=color,marker=marker,s=27,zorder=3)
    ax.axvline(0,color='black',lw=.8,ls='--')
    ax.axhline(7.7,color='#888888',lw=.6)
    if model['interval_available']:
        ax.errorbar(model['mean'],9,xerr=[[model['mean']-model['lower']],[model['upper']-model['mean']]],
                    fmt='D',color='black',markersize=4,capsize=3,lw=1.1,zorder=4)
    else:ax.scatter(model['mean'],9,color='black',marker='D',s=25)
    ax.set_title(title,fontsize=10,pad=11)
    ax.set_xlim(-limit,limit);ax.set_ylim(10,-.6)
    ax.set_xticks(np.linspace(-limit,limit,5))
    ax.set_axisbelow(True);ax.grid(axis='x',color='#dddddd',lw=.6)
    ax.spines[['top','right']].set_visible(False)
axes[0].set_yticks([*range(8),9],[str(i) for i in range(1,9)]+['Mean with\n95% t interval'])
axes[0].set_ylabel('Policy-seed block',labelpad=7)
fig.supxlabel('Change in Small − Base success-rate difference',x=.59,y=.02,fontsize=10)
fig.subplots_adjust(left=.19,right=.955,top=.88,bottom=.18,wspace=.20)
for ext in ['pdf','png']:fig.savefig(A/('calibration_figure.'+ext),dpi=220)
dest=R/'submission/ras/Fig8.pdf';dest.write_bytes((A/'calibration_figure.pdf').read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(A/'CALIBRATION_FIGURE_PROVENANCE.json').write_text(json.dumps({
    'inputs':{p.relative_to(A).as_posix():sha(p) for p in [vp,tp]},'source_sha256':sha(Path(__file__)),
    'output_sha256':sha(dest),'display':'Every prespecified block; mean and unadjusted secondary t working intervals; bounded-mean sensitivities reported in S2, not omitted from inference.'},indent=2)+'\n')
print(dest)
