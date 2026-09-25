"""Success-state fraction per control step and cube-goal distance at step 50, nominal native settings.
Reads the frozen confirmatory raw records; no refitting."""
from pathlib import Path
import hashlib, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
A = Path(__file__).resolve().parent; R = A.parents[1]
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9.5, 'axes.labelcolor': 'black', 'text.color': 'black',
                     'xtick.color': 'black', 'ytick.color': 'black', 'pdf.fonttype': 42, 'ps.fonttype': 42})
inputs = {}
def load(task, mode):
    seqs, d50 = [], []
    for b in range(4):
        p = A / 'confirmatory' / 'raw_v2' / f'{task}_{mode}_nominal_batch{b}.json'
        raw = p.read_bytes(); inputs[str(p.relative_to(R))] = hashlib.sha256(raw).hexdigest()
        d = json.loads(raw)
        assert d['setting'] == 'nominal' and d['num_scenes'] == 256
        for e in d['episodes']:
            seqs.append(e['success_sequence'])
            c = np.array(e['state_at_50']['cube_state'][:3]); g = np.array(e['state_at_50']['goal_state'][:3])
            d50.append(float(np.linalg.norm((c - g)[:2])))
    return np.array(seqs, dtype=np.uint8), np.array(d50)
fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.7), gridspec_kw={'width_ratios': [1.15, 1.15, 1]})
styles = [('pd_joint_delta_pos', '#0072B2', '-', 'Joint pipeline'), ('pd_ee_delta_pos', '#D55E00', '--', 'Cartesian pipeline')]
summary = {}
for ax, task, title in zip(axs[:2], ['PickCube-v1', 'PushCube-v1'], ['(a) PickCube', '(b) PushCube']):
    for mode, color, ls, label in styles:
        S, d50 = load(task, mode)
        frac = S.mean(0)
        ax.plot(np.arange(1, 101), frac, color=color, ls=ls, lw=1.4, label=label)
        summary[f'{task}/{mode}'] = dict(n=int(len(S)), ever50=int(S[:, :50].any(1).sum()), at50=int(S[:, 49].sum()),
                                         peak_step=int(frac[:50].argmax()) + 1, peak_fraction=float(frac[:50].max()),
                                         median_xy_distance_at_50=float(np.median(d50)),
                                         fraction_beyond_0p1_at_50=float((d50 > 0.1).mean()))
        if task == 'PushCube-v1':
            axs[2].hist(d50, bins=np.linspace(0, 0.6, 31), histtype='step', color=color, ls=ls, lw=1.4, label=label)
    ax.axvline(50, color='black', lw=.85, ls=':')
    ax.set_xlim(0, 100); ax.set_ylim(0, 1); ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_title(title, fontsize=10.5, pad=6); ax.set_xlabel('Control step')
    ax.spines[['top', 'right']].set_visible(False); ax.set_axisbelow(True); ax.grid(axis='y', color='#dddddd', lw=.6)
axs[0].set_ylabel('Fraction in success state')
axs[2].axvline(0.1, color='black', lw=.85, ls=':')
axs[2].set_title('(c) PushCube, step 50', fontsize=10.5, pad=6); axs[2].set_xlabel('Cube–goal distance (m)')
axs[2].set_ylabel('Scenes'); axs[2].spines[['top', 'right']].set_visible(False)
handles, labels = axs[1].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(.5, -.01), ncol=2, frameon=False, fontsize=9)
fig.subplots_adjust(left=.085, right=.99, top=.86, bottom=.32, wspace=.38)
out = R / 'submission' / 'ras' / 'Fig4.pdf'
fig.savefig(out, metadata={'Creator': 'Matplotlib; nominal confirmatory raw records'})
fig.savefig(A / 'mechanism_figure.png', dpi=220)
(A / 'MECHANISM_FIGURE_PROVENANCE.json').write_text(json.dumps({'inputs': inputs, 'output': str(out.relative_to(R)),
    'output_sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'summary': summary}, indent=2) + '\n')
print(json.dumps(summary, indent=1))
