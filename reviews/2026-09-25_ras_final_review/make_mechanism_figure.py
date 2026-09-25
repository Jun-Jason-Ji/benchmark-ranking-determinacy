"""Descriptive success-state fractions and complete terminal-distance histogram.
Reads frozen nominal confirmation records; no new evaluation or inferential test.
The last displayed distance group aggregates all values >= 0.6 m; no observations
are omitted. The original September 24 generator and its outputs are preserved.
"""
from pathlib import Path
import hashlib, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
A = Path(__file__).resolve().parent; R = A.parents[1]
SOURCE = R / 'reviews' / '2026-09-24_ras_strengthening'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9.5, 'axes.labelcolor': 'black', 'text.color': 'black',
                     'xtick.color': 'black', 'ytick.color': 'black', 'pdf.fonttype': 42, 'ps.fonttype': 42})
inputs = {}
def load(task, mode):
    seqs, d50 = [], []
    for b in range(4):
        p = SOURCE / 'confirmatory' / 'raw_v2' / f'{task}_{mode}_nominal_batch{b}.json'
        raw = p.read_bytes(); inputs[str(p.relative_to(R))] = hashlib.sha256(raw).hexdigest()
        d = json.loads(raw)
        assert d['task'] == task and d['mode'] == mode and d['batch'] == b
        assert d['setting'] == 'nominal' and d['num_scenes'] == len(d['episodes']) == 256
        assert sorted(e['scene_slot'] for e in d['episodes']) == list(range(256))
        for e in d['episodes']:
            assert len(e['success_sequence']) == 100 and set(e['success_sequence']) <= {0, 1}
            seqs.append(e['success_sequence'])
            c = np.array(e['state_at_50']['cube_state'][:3]); g = np.array(e['state_at_50']['goal_state'][:3])
            d50.append(float(np.linalg.norm((c - g)[:2])))
    distances = np.array(d50)
    assert np.isfinite(distances).all() and (distances >= 0).all()
    return np.array(seqs, dtype=np.uint8), distances
fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.7), gridspec_kw={'width_ratios': [1.15, 1.15, 1]})
styles = [('pd_joint_delta_pos', '#0072B2', '-', 'Joint pipeline'), ('pd_ee_delta_pos', '#D55E00', '--', 'Cartesian pipeline')]
summary = {}
histograms = {}
axs[2].axvspan(0.6, 0.66, color='#eeeeee', zorder=0)
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
            finite_edges = np.linspace(0, 0.6, 31)
            finite_counts, _ = np.histogram(d50[d50 < 0.6], bins=finite_edges)
            overflow = int((d50 >= 0.6).sum())
            display_counts = np.append(finite_counts, overflow)
            display_edges = np.append(finite_edges, 0.66)
            assert int(display_counts.sum()) == len(d50) == 1024
            histograms[mode] = dict(n=1024, finite_bin_edges=finite_edges.tolist(),
                finite_bin_counts=finite_counts.tolist(), overflow_threshold_m=0.6,
                overflow_operator='>=', overflow_count=overflow,
                count_accounted_for=int(display_counts.sum()),
                raw_min_m=float(d50.min()), raw_max_m=float(d50.max()),
                overflow_display_interval=[0.6, 0.66],
                interpretation='Last shaded group is categorical overflow, not a 0.06-m bin or a density estimate')
            axs[2].stairs(display_counts, display_edges, color=color, ls=ls, lw=1.4, label=label)
    ax.axvline(50, color='black', lw=.85, ls=':')
    ax.set_xlim(0, 100); ax.set_ylim(0, 1); ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_title(title, fontsize=10.5, pad=6); ax.set_xlabel('Control step')
    ax.spines[['top', 'right']].set_visible(False); ax.set_axisbelow(True); ax.grid(axis='y', color='#dddddd', lw=.6)
axs[0].set_ylabel('Fraction in success state')
axs[2].axvline(0.1, color='black', lw=.85, ls=':')
axs[2].set_title('(c) PushCube, step 50', fontsize=10, pad=6); axs[2].set_xlabel('Planar goal distance (m)', fontsize=9)
axs[2].set_ylabel('Scenes'); axs[2].spines[['top', 'right']].set_visible(False)
axs[2].set_xlim(0, 0.675)
axs[2].set_xticks([0, 0.2, 0.4, 0.63], ['0.0', '0.2', '0.4', r'$\geq$0.6'])
axs[2].axvline(0.6, color='#999999', lw=0.7)
overflow_label = (f"Overflow counts\nJoint: {histograms['pd_joint_delta_pos']['overflow_count']}"
                  f"\nCartesian: {histograms['pd_ee_delta_pos']['overflow_count']}")
axs[2].text(0.975, 0.97, overflow_label,
            transform=axs[2].transAxes, ha='right', va='top', fontsize=7.5,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.95, pad=1.5))
handles, labels = axs[1].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(.5, -.01), ncol=2, frameon=False, fontsize=9)
fig.subplots_adjust(left=.085, right=.955, top=.86, bottom=.32, wspace=.40)
out = R / 'submission' / 'ras' / 'Fig4.pdf'
fig.savefig(out, metadata={'Creator': 'Matplotlib; complete nominal confirmation diagnostics; explicit distance overflow'})
fig.savefig(A / 'descriptive_success_distance.png', dpi=220)
(A / 'FIG4_DESCRIPTIVE_PROVENANCE.json').write_text(json.dumps({'inputs': inputs, 'output': str(out.relative_to(R)),
    'output_sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'summary': summary,
    'histograms': histograms, 'analysis_scope': 'Post-confirmation descriptive diagnostics; no mechanism identification',
    'source_generator_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'original_generator': str((SOURCE / 'make_mechanism_figure.py').relative_to(R)),
    'original_generator_sha256': hashlib.sha256((SOURCE / 'make_mechanism_figure.py').read_bytes()).hexdigest()}, indent=2) + '\n')
print(json.dumps(summary, indent=1))
