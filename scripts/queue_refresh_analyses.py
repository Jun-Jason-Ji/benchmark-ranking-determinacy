"""Refresh the analysis tables as each stage of the overnight chain completes.

Only generated `analysis_*.md` tables are rewritten; hand-written `FINDING_*.md` narratives are never
touched (an earlier version of this queue overwrote one).

The chain is: OCTO_RECOLLECT_DONE -> OPENVLA_CENSUS_DONE -> UNION_CONDS_DONE -> MS2_OFFICIAL_DONE. After each
marker the analyses that the new data affects are re-run, so the tables on disk always reflect everything
collected so far (CPU only; no GPU contention). Every stage writes a stamped copy under
results/analysis_refresh/<marker>/ as well, so the progression stays auditable.

Marker REFRESH_DONE."""
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_v2 import PY, log  # noqa: E402

LOGS = ROOT / "results/controller_sweep/logs"
SNAP = ROOT / "results/analysis_refresh"
EGG = "PutEggplantInBasketScene-v1"

# (marker file, marker text, [(script, args, output path relative to ROOT), ...])
STAGES = [
    ("queue_octo_recollect.out", "OCTO_RECOLLECT_DONE", [
        ("analyze_platform_drift.py", [], "results/controller_sweep_gpu_replayA/analysis_platform_drift.md"),
        ("analyze_seed_noise.py", [], "results/controller_sweep_gpu_rep3/analysis_seed_noise.md"),
        ("analyze_benchmark_value.py", [], "results/controller_sweep_gpu_rep3/analysis_benchmark_value.md"),
        ("analyze_cluster_bootstrap.py", ["--env", EGG, "--policies", "octo-small,octo-base,octo-small@hist1,octo-base@hist1",
                                          "--n", "64", "--out", "results/controller_sweep_gpu/analysis_cluster_bootstrap_eggplant.md"],
         "results/controller_sweep_gpu/analysis_cluster_bootstrap_eggplant.md"),
    ]),
    ("queue_openvla_census.out", "OPENVLA_CENSUS_DONE", [
        ("analyze_benchmark_value.py", [], "results/controller_sweep_gpu_rep3/analysis_benchmark_value.md"),
        ("analyze_openvla_torque_sets.py", ["--n", "64", "--out", "results/controller_sweep_gpu_rep3/analysis_openvla_torque_census.md"],
         "results/controller_sweep_gpu_rep3/analysis_openvla_torque_census.md"),
        ("analyze_benchmark_value.py", ["--env", "PutCarrotOnPlateInScene-v1",
                                        "--conditions", "nominal,force_x0.5,iso_x0.25,iso_x4.0,fric_x0.4,dens_x0.5",
                                        "--out", "results/controller_sweep_gpu_rep3/analysis_benchmark_value_carrot.md"],
         "results/controller_sweep_gpu_rep3/analysis_benchmark_value_carrot.md"),
        ("analyze_cross_stack.py", ["--n", "24"], "results/controller_sweep_ms2/analysis_cross_stack.md"),
    ]),
    ("queue_octo_union_conds.out", "UNION_CONDS_DONE", [
        ("analyze_benchmark_value.py", ["--conditions", "nominal,force_x0.5,iso_x0.25,iso_x4.0,fric_x0.4,dens_x0.5",
                                        "--out", "results/controller_sweep_gpu_rep3/analysis_benchmark_value_union.md"],
         "results/controller_sweep_gpu_rep3/analysis_benchmark_value_union.md"),
        ("analyze_seed_noise.py", ["--conditions", "nominal,force_x0.5,iso_x0.25,iso_x4.0,fric_x0.4,dens_x0.5",
                                   "--out", "results/controller_sweep_gpu_rep3/analysis_seed_noise_union.md"],
         "results/controller_sweep_gpu_rep3/analysis_seed_noise_union.md"),
    ]),
    ("queue_t1_union_hist1.out", "T1_UNION_HIST1_DONE", [
        ("make_core_table.py", [], "results/CORE_TABLE.md"),
        ("analyze_benchmark_value.py", ["--conditions", "nominal,force_x0.5,iso_x0.25,iso_x4.0,fric_x0.4,dens_x0.5",
                                        "--out", "results/controller_sweep_gpu_rep3/analysis_benchmark_value_union.md"],
         "results/controller_sweep_gpu_rep3/analysis_benchmark_value_union.md"),
    ]),
    ("queue_ms2_official_protocol.out", "MS2_OFFICIAL_DONE", [
        ("analyze_official_protocol.py", [], "results/controller_sweep_ms2_official/FINDING_official_protocol.md"),
        ("make_core_table.py", [], "results/CORE_TABLE.md"),
    ]),
    ("queue_t1_neartied.out", "T1B_NEARTIED_DONE", [
        ("make_core_table.py", [], "results/CORE_TABLE.md"),
        ("analyze_benchmark_value.py", ["--conditions", "nominal,force_x0.5,iso_x0.25,iso_x4.0,fric_x0.4,dens_x0.5",
                                        "--out", "results/controller_sweep_gpu_rep3/analysis_benchmark_value_union.md"],
         "results/controller_sweep_gpu_rep3/analysis_benchmark_value_union.md"),
        ("analyze_torque_mechanism.py", [], "results/controller_sweep_gpu_rep3/analysis_torque_mechanism.md"),
        ("make_figures_v2.py", [], "results/figures/fig_uncertainty_budget.png"),
    ]),
    ("queue_t2a_seeds.out", "T2A_SEEDS_DONE", [
        ("make_core_table.py", [], "results/CORE_TABLE.md"),
        ("analyze_benchmark_value.py", ["--conditions", "nominal,force_x0.5,iso_x0.25,iso_x4.0,fric_x0.4,dens_x0.5",
                                        "--out", "results/controller_sweep_gpu_rep3/analysis_benchmark_value_union.md"],
         "results/controller_sweep_gpu_rep3/analysis_benchmark_value_union.md"),
        ("analyze_seed_noise.py", ["--conditions", "nominal,force_x0.5,iso_x0.25,iso_x4.0,fric_x0.4,dens_x0.5",
                                   "--out", "results/controller_sweep_gpu_rep3/analysis_seed_noise_union.md"],
         "results/controller_sweep_gpu_rep3/analysis_seed_noise_union.md"),
        ("analyze_torque_mechanism.py", [], "results/controller_sweep_gpu_rep3/analysis_torque_mechanism.md"),
        ("make_figures_v2.py", [], "results/figures/fig_uncertainty_budget.png"),
    ]),
]


def wait_marker(fname, marker, timeout_h=24):
    deadline = time.time() + timeout_h * 3600
    while time.time() < deadline:
        f = LOGS / fname
        if f.exists() and marker in f.read_text(encoding="utf-8", errors="replace"):
            return True
        time.sleep(120)
    log(f"marker {marker} not seen within {timeout_h} h; skipping its analyses")
    return False


def main():
    for fname, marker, tasks in STAGES:
        if not wait_marker(fname, marker):
            continue
        log(f"=== refreshing analyses after {marker}")
        snap = SNAP / marker
        if snap.exists() and any(snap.iterdir()):
            # A restart (crash, reboot) replays completed stages against the data on disk now, which is
            # right for the live tables but would rewrite this stage's record with a later state. Snapshot
            # directories are append-only: a replay gets its own stamped directory.
            snap = SNAP / f"{marker}__replay_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
            log(f"stage already snapshotted; this replay goes to {snap.name}")
        snap.mkdir(parents=True, exist_ok=True)
        for script, args, out in tasks:
            if not (ROOT / "scripts" / script).exists():
                log(f"skip missing {script}")
                continue
            r = subprocess.run([str(PY), f"scripts/{script}"] + args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
            log(f"{script} rc={r.returncode}{'' if r.returncode == 0 else ' ' + (r.stderr or '')[-300:]}")
            src = ROOT / out
            if r.returncode == 0 and src.exists():
                shutil.copy2(src, snap / src.name)
    log("REFRESH_DONE")


if __name__ == "__main__":
    main()
