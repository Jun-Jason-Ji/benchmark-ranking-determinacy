"""Publication figure from the frozen confirmatory intervals, without refitting."""
from pathlib import Path
import hashlib,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
A=Path(__file__).resolve().parent;R=A.parents[1]
data=json.loads((A/'confirmatory/RESULTS.json').read_text())
assert data['status']=='complete' and data['family_differences']==20
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9.5,'axes.labelcolor':'black','text.color':'black','xtick.color':'black','ytick.color':'black','pdf.fonttype':42,'ps.fonttype':42})
settings=['nominal','gain_half','gain_double','force_half','force_double']
labels=['Nominal','Gain × 0.5','Gain × 2','Force limit × 0.5','Force limit × 2']
fig,axs=plt.subplots(1,2,figsize=(7.2,3.5),sharex=True,sharey=True)
for ax,task,title in zip(axs,['PickCube-v1','PushCube-v1'],['(a) PickCube','(b) PushCube']):
    for endpoint,offset,color,marker,label in [('ever50',-.12,'#0072B2','o','Success at any step 1–50'),('at50',.12,'#D55E00','s','Success at step 50')]:
        cells=data['results'][task][endpoint]['cells'];means=np.array([cells[s]['difference'] for s in settings]);lo=np.array([cells[s]['lower'] for s in settings]);hi=np.array([cells[s]['upper'] for s in settings])
        ax.errorbar(means,np.arange(5)+offset,xerr=np.stack([means-lo,hi-means]),fmt=marker,markersize=4.5,capsize=2.7,lw=1.25,color=color,label=label)
    ax.axvline(0,color='black',lw=.85,ls='--');ax.set_title(title,fontsize=11,pad=10)
    ax.set_xlim(-.52,.52);ax.set_xticks([-.4,-.2,0,.2,.4]);ax.set_ylim(4.6,-.6)
    ax.set_axisbelow(True);ax.grid(axis='x',color='#dddddd',lw=.6)
    ax.spines[['top','right']].set_visible(False)
axs[0].set_yticks(range(5),labels)
handles,legend=axs[0].get_legend_handles_labels()
fig.legend(handles,legend,loc='lower center',bbox_to_anchor=(.57,.015),ncol=2,frameon=False,fontsize=9)
fig.supxlabel('Joint − Cartesian success-rate difference',x=.60,y=.13,fontsize=10)
fig.subplots_adjust(left=.19,right=.985,top=.86,bottom=.26,wspace=.17)
for suffix in ['pdf','png']:
    fig.savefig(A/('confirmation_figure.'+suffix),dpi=220,metadata={'Creator':'Matplotlib; frozen primary 20-comparison family'} if suffix=='pdf' else None)
pdf=R/'submission/ras/Fig7.pdf';pdf.write_bytes((A/'confirmation_figure.pdf').read_bytes())
(A/'FIGURE_PROVENANCE.json').write_text(json.dumps({'input':'confirmatory/RESULTS.json','input_sha256':hashlib.sha256((A/'confirmatory/RESULTS.json').read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'source':'prespecified simultaneous paired-discordance intervals, all 20 comparisons'},indent=2)+'\n')
print(pdf)
