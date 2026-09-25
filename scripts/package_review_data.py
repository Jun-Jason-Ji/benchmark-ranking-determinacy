"""Create and verify a scoped companion review package, without changing live results.

Create requires a new --out directory. Selection starts from the historical root
SHA256SUMS inventory, adds the completed fitted-operating-point records for BOTH tasks
and the force-probe records, all cached replay NPZs, numeric Bridge inputs, analysis
code and dependency notices. No external publication.

Fitted spoon was excluded while the sweep was in progress. It has since completed and
the manuscript's Sect. 7.7 now rests on it, so excluding it would ship a package that
does not contain the data behind a headline result. It is included and validated on the
same terms as eggplant: every condition, both policies, both seed sets, and exactly the
24 configurations of that grid once each.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EGGPLANT = "PutEggplantInBasketScene-v1"
SPOON = "PutSpoonOnTableClothInScene-v1"
CONDITIONS = ("fitted", "fitted_force_x0.5", "fitted_iso_x0.25", "fitted_iso_x4.0",
              "fitted_fric_x0.4", "fitted_dens_x0.5")
# (task, configuration count, seed-set suffixes). Eggplant uses three census seed sets and
# spoon two, matching each task's own nominal census so the comparisons stay paired.
FITTED_TASKS = ((EGGPLANT, 64, ("A", "C", "D")), (SPOON, 24, ("A", "C")))
NOMINAL_DIRS = {"A": "controller_sweep_gpu_replayA", "C": "controller_sweep_gpu_rep3",
                "D": "controller_sweep_gpu_rep4"}
SUMS = "DATA_SHA256SUMS.txt"
SCOPE = "DATA_SCOPE.json"
VERIFY = "DATA_VERIFICATION.json"
PACKAGE_SUMS = "REVIEW_PACKAGE_SHA256SUMS.txt"
MARKER = ".INCOMPLETE"


def digest(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def safe_name(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and ".." not in p.parts \
        and ":" not in name and "\\" not in name and p.as_posix() == name


def parse_sums(blob: bytes) -> dict[str, str]:
    entries = {}
    for line in blob.decode("utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        m = re.fullmatch(r"([0-9a-f]{64}) \*(.+)", line)
        if not m or not safe_name(m[2]) or m[2] in entries:
            raise ValueError(f"Invalid or duplicate checksum entry: {line}")
        entries[m[2]] = m[1]
    return entries


def excluded(name: str) -> bool:
    """Nothing in the fitted sweeps is excluded now that both tasks are complete.

    This returned True for every fitted-spoon path while that sweep was running, so that a
    package could not ship half-written records. Both tasks are complete and both are behind
    results the manuscript reports, so the filter is empty; fitted_census below is what now
    guarantees completeness, and it raises rather than silently dropping a short file.
    """
    return False


def read_stable(path: Path) -> bytes:
    before = path.stat()
    blob = path.read_bytes()
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns) \
            or len(blob) != after.st_size:
        raise ValueError(f"Source changed during read: {path}")
    return blob


def selection(root: Path) -> tuple[set[str], set[str]]:
    previous = set(parse_sums(read_stable(root / "SHA256SUMS.txt")))
    selected = previous.copy()
    # Both operating points and both tasks, using each task's own seed sets.
    for task, _n_cfg, seeds in FITTED_TASKS:
        for seed in seeds:
            for directory in (NOMINAL_DIRS[seed], f"controller_sweep_fitted_{seed}"):
                for policy in ("octo-small", "octo-base"):
                    folder = root / "results" / directory / policy / task
                    for path in folder.iterdir():
                        if path.is_file() and path.suffix in {".json", ".jsonl"}:
                            selected.add(path.relative_to(root).as_posix())
    probe = root / "results/replay_sysid_ms2_force_probe/fitted_force_probe"
    for path in probe.iterdir():
        if path.is_file() and path.suffix in {".json", ".jsonl"}:
            selected.add(path.relative_to(root).as_posix())
    for folder in (root / "results").glob("replay_sysid*"):
        for path in folder.rglob("*.npz"):
            selected.add(path.relative_to(root).as_posix())
    for path in (root / "data/bridge_sysid").iterdir():
        if path.is_file() and path.suffix in {".json", ".npz"}:
            selected.add(path.relative_to(root).as_posix())
    for directory in ("scripts", "benchmark"):
        for path in (root / directory).rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                selected.add(path.relative_to(root).as_posix())
    for name in ("LICENSE", "NOTICE.md", "REPRODUCIBILITY.md", "README.md", "CITATION.cff", "CHANGELOG.md"):
        selected.add(name)
    for name in ("research_audit/simpler_published_scores.csv", "research_audit/simpler_manifest.json"):
        selected.add(name)
    # Analysis inputs, not a simulator install: two scripts parse SIMPLER_PERF.
    selected.add("third_party/SimplerEnv/simpler_env/utils/metrics.py")
    selected.add("third_party/SimplerEnv/LICENSE")
    # Small workload-specific compatibility layer discussed in Appendix B.
    # Ship its editable source and activation manifest, not a host-built binary.
    for name in ("fakesemfd_layer.c", "build.sh", "VkLayer_fakesemfd.json"):
        selected.add(f"third_party/vk_fakesemfd/{name}")
    selected.add("docs/software_rendering_compatibility.md")
    for path in root.glob("requirements*.txt"):
        selected.add(path.name)
    # These explanations are analysis references, not claims of a current deposit.
    for name in ("docs/methods_census_2026-09-19.md", "docs/theory_protocol.md"):
        if (root / name).is_file():
            selected.add(name)
    selected = {name for name in selected if not excluded(name)}
    # Resolve each shared parent once: resolving 16k individual Windows paths is
    # needlessly slow. Still reject file symlinks and any ancestor path escape.
    checked_parents = set()
    for name in selected:
        path = root / name
        if path.parent not in checked_parents:
            if not path.parent.resolve().is_relative_to(root):
                raise ValueError(f"Source parent escapes repository: {path.parent}")
            checked_parents.add(path.parent)
        if not safe_name(name) or not path.is_file() or path.is_symlink():
            raise ValueError(f"Unsafe or missing selected source: {name}")
    return selected, previous


def fitted_census(data: dict[str, bytes]) -> dict:
    """Validate every fitted-operating-point census file, per task, before packaging.

    A file that is short, duplicated or missing an episode id raises here rather than being
    packaged. That is the check that lets the package assert completeness instead of asserting
    that a sweep was believed to have finished.
    """
    out = {}
    for task, n_cfg, seeds in FITTED_TASKS:
        counts = {}
        want = set(range(n_cfg))
        for seed in seeds:
            for policy in ("octo-small", "octo-base"):
                for condition in CONDITIONS:
                    name = (f"results/controller_sweep_fitted_{seed}/{policy}/"
                            f"{task}/{condition}.jsonl")
                    if name not in data:
                        raise ValueError(f"Fitted census file absent from selection: {name}")
                    rows = [json.loads(line)
                            for line in data[name].decode("utf-8").splitlines() if line.strip()]
                    ids = [row["episode_id"] for row in rows]
                    if len(ids) != n_cfg or set(ids) != want:
                        raise ValueError(
                            f"Fitted census is not exactly 0..{n_cfg - 1} once: {name} "
                            f"({len(ids)} rows, {len(set(ids))} distinct)")
                    counts[name] = len(ids)
        out[task] = {"files": len(counts), "records": sum(counts.values()),
                     "configurations": n_cfg, "seed_sets": list(seeds),
                     "expected_ids_per_file": f"0..{n_cfg - 1} exactly once",
                     "per_file": counts}
    return out


def census_paths():
    for task, n_cfg, seeds in FITTED_TASKS:
        for seed in seeds:
            for policy in ("octo-small", "octo-base"):
                for fitted_condition in CONDITIONS:
                    nominal_condition = "nominal" if fitted_condition == "fitted" else fitted_condition.removeprefix("fitted_")
                    nominal = f"results/{NOMINAL_DIRS[seed]}/{policy}/{task}/{nominal_condition}.jsonl"
                    fitted = f"results/controller_sweep_fitted_{seed}/{policy}/{task}/{fitted_condition}.jsonl"
                    yield task, n_cfg, policy, nominal_condition, fitted_condition, nominal, fitted


def operating_point_censuses(data: dict[str, bytes]) -> dict:
    """Check both six-condition fibres and their episode-level policy-seed pairing."""
    tasks = {}
    for task, n_cfg, policy, nominal_cond, fitted_cond, nominal, fitted in census_paths():
        seed_maps = []
        for point, condition, name in (("nominal", nominal_cond, nominal), ("fitted", fitted_cond, fitted)):
            rows = [json.loads(line) for line in data[name].decode("utf-8").splitlines() if line.strip()]
            ids = [row["episode_id"] for row in rows]
            if len(ids) != n_cfg or set(ids) != set(range(n_cfg)):
                raise ValueError(f"Census is not exactly 0..{n_cfg - 1} once: {name}")
            if any(row.get("policy") != policy or row.get("env_id") != task
                   or row.get("condition") != condition for row in rows):
                raise ValueError(f"Record metadata disagrees with path: {name}")
            seed_maps.append({row["episode_id"]: row["policy_seed"] for row in rows})
            group = tasks.setdefault(task, {}).setdefault(point, {"files": 0, "records": 0,
                         "expected_ids_per_file": f"0..{n_cfg - 1} exactly once", "per_file": {}})
            group["files"] += 1
            group["records"] += len(ids)
            group["per_file"][name] = len(ids)
        if seed_maps[0] != seed_maps[1]:
            raise ValueError(f"Nominal/fitted policy seeds are not paired: {fitted}")
    return {"tasks": tasks, "nominal_fitted_seed_pairing_checked": True,
            "files": sum(x["files"] for task in tasks.values() for x in task.values()),
            "records": sum(x["records"] for task in tasks.values() for x in task.values())}


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sums_bytes(data: dict[str, bytes], comment: str) -> bytes:
    return (f"# {comment}\n" + "".join(f"{digest(blob)} *{name}\n"
            for name, blob in sorted(data.items()))).encode("utf-8")


def create(root: Path, out: Path) -> dict:
    root, out = root.resolve(), out.resolve()
    if out.exists():
        raise ValueError(f"Destination already exists; never overwrite a snapshot: {out}")
    names, previous = selection(root)
    print(f"Selected {len(names)} source files; capturing bytes.", file=sys.stderr, flush=True)
    data = {name: read_stable(root / name) for name in sorted(names)}
    census = fitted_census(data)
    point_censuses = operating_point_censuses(data)
    print("First capture complete; checking selection and bytes again.", file=sys.stderr, flush=True)
    if selection(root) != (names, previous):
        raise ValueError("Source selection changed during capture.")
    for name, blob in data.items():
        if digest(read_stable(root / name)) != digest(blob):
            raise ValueError(f"Source changed between capture passes: {name}")
    now = datetime.now(timezone.utc).isoformat()
    rev = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                         text=True, capture_output=True, timeout=20)
    source_sums = read_stable(root / "SHA256SUMS.txt")
    data[SUMS] = sums_bytes(data, "Scoped review data/code reference manifest; NOT a full release/deposit.")
    scope = {"kind": "scoped_companion_review_package", "schema_version": 2,
             "created_utc": now, "source_git_head": rev.stdout.strip() if rev.returncode == 0 else None,
             "source_root_manifest_sha256": digest(source_sums),
             "selection": ["Historical root SHA256SUMS inventory, rehashed at capture time",
                           "Completed nominal/fitted-operating-point JSON/JSONL for both tasks: "
                           "eggplant across A/C/D and spoon across A/C, both policies, all "
                           "six conditions per point, every file complete and policy seeds paired",
                           "Fitted force-probe JSON/JSONL", "All results/replay_sysid*/**/*.npz",
                           "Numeric data/bridge_sysid NPZ and shard manifests",
                           "Published SIMPLER score CSV and source manifest",
                           "SimplerEnv metrics.py reference constants with its upstream MIT LICENSE",
                           "Appendix B Vulkan layer source, build script, manifest and implementation notes",
                           "scripts/, benchmark/, LICENSE, NOTICE, REPRODUCIBILITY, requirements files and two methods documents"],
             "excluded": ["Live analysis markdown, logs/stderr, policy checkpoints, simulator assets",
                          "Simulator trees except the single reference metrics.py and its LICENSE; original TFRecord shards"],
             "scope_note": "Includes historical and contaminated records retained by the prior inventory; this inventory does not mark them as analysis-eligible. Script exclusions still apply.",
             "data_files_physically_copied": True, "full_release_completeness_claimed": False,
             "current_archive_deposit_verified": False, "fitted_spoon_included": True,
             "prior_inventory_entries": len(previous), "selected_source_files": len(names),
             "selected_source_bytes": sum(len(data[n]) for n in names),
             "replay_npz_files": sum(n.startswith("results/") and n.endswith(".npz") for n in names),
             "added_to_prior_inventory": sorted(names - previous),
             "excluded_prior_entries": sorted(previous - names),
             "fitted_census_by_task": census, "operating_point_censuses": point_censuses}
    data[SCOPE] = json_bytes(scope)
    data[VERIFY] = json_bytes({"status": "passed_two_source_capture_passes", "checked_utc": now,
                              "source_files_checked": len(names), "missing": [], "changed": [],
                              "data_manifest_sha256": digest(data[SUMS]),
                              "note": "Post-write verification checks every copied byte and exact package inventory."})
    data["README_REVIEW_PACKAGE.md"] = f"""# Companion review data and code

Created UTC: {now}. This local package supplies cached records and analysis code
for manuscript review. It is not a claim of a complete public release or a new
Zenodo deposit. The earlier public concept DOI is 10.5281/zenodo.22893458; it does
not identify this package. Exact scope and exclusions are in DATA_SCOPE.json.

Scope exception to the historical NOTICE.md: this review package includes the
single upstream SimplerEnv `simpler_env/utils/metrics.py` reference-data module
with its original MIT LICENSE (copyright 2024 simpler-env). Analysis scripts parse
its published constants without importing the simulator. It also includes numeric
Bridge input arrays and shard provenance, not original TFRecord/image shards.
All included upstream/derived files retain their original rights and attribution.

The nominal and fitted censuses for both completed tasks are included and validated:
all six conditions at each point and both policies, with eggplant on three seed sets
at 64 unique configurations per file (2304 records per point) and spoon on two seed
sets at 24 per file (576 records per point). All 120 census files have exactly their
grid's ids once each, totaling 5760 records; policy seeds match nominal/fitted episode
by episode. A short, duplicated, or unpaired file aborts the run. Fitted spoon was
excluded from earlier packages while that sweep was in progress. Historical
records, including quarantined results retained by the old inventory, remain
labelled by their original paths; their presence does not make them admissible.

DATA_SHA256SUMS.txt identifies every selected source byte, including analysis
code and cached replay trajectories. REVIEW_PACKAGE_SHA256SUMS.txt additionally
covers the generated scope and verification notes. From outside this directory:

    python -B scripts/package_review_data.py verify <this-directory>

Or, with sha256sum installed, run inside the package:

    sha256sum -c REVIEW_PACKAGE_SHA256SUMS.txt

The Python verifier also detects unexpected files. The workflow refuses existing
output directories, but does not make the filesystem tamper-proof.

For analysis, work in a copy to preserve the verified package. The scripts retain
their relative paths and can read cached records without any GPU evaluation.
Install appropriate dependencies separately; they are recorded in requirements
files. Examples: python scripts/make_core_table.py; python
scripts/analyze_compatible_set_v2.py; python scripts/analyze_fitted_point.py.
The fitted-point script reports both completed tasks. Simulator reruns additionally
require upstream assets/checkpoints and
third-party simulator code listed in NOTICE.md; these are excluded apart from the
reference-data module and license stated above.
""".encode("utf-8")
    data[PACKAGE_SUMS] = sums_bytes(data, "Companion review package; verify from its root.")
    print("Both source passes passed; writing new review package.", file=sys.stderr, flush=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.mkdir()
    (out / MARKER).write_text("Creation incomplete.\n", encoding="utf-8")
    for name, blob in sorted(data.items()):
        path = out / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(blob)
    (out / MARKER).unlink()
    print("Package written; verifying all copied bytes and inventory.", file=sys.stderr, flush=True)
    return verify(out)


def verify(out: Path) -> dict:
    out = out.resolve()
    if not out.is_dir() or (out / MARKER).exists():
        raise ValueError(f"Not a completed review package: {out}")
    entries = parse_sums((out / PACKAGE_SUMS).read_bytes())
    if not {SUMS, SCOPE, VERIFY, "README_REVIEW_PACKAGE.md"} <= set(entries):
        raise ValueError("Package metadata missing from checksums.")
    actual = set()
    checked_parents = set()
    for path in out.rglob("*"):
        if path.parent not in checked_parents:
            if not path.parent.resolve().is_relative_to(out):
                raise ValueError(f"Package parent escapes output directory: {path.parent}")
            checked_parents.add(path.parent)
        if path.is_symlink():
            raise ValueError(f"Symlink/path escape: {path}")
        if path.is_file():
            actual.add(path.relative_to(out).as_posix())
    if actual != set(entries) | {PACKAGE_SUMS}:
        raise ValueError("Package inventory changed (missing or unexpected files).")
    for name, expected in entries.items():
        if digest(read_stable(out / name)) != expected:
            raise ValueError(f"Checksum mismatch: {name}")
    referenced = parse_sums((out / SUMS).read_bytes())
    if any(excluded(name) for name in referenced):
        raise ValueError("Excluded data found in reference manifest.")
    if set(entries) != set(referenced) | {SUMS, SCOPE, VERIFY, "README_REVIEW_PACKAGE.md"}:
        raise ValueError("Reference manifest and package inventory disagree.")
    if any(entries.get(name) != value for name, value in referenced.items()):
        raise ValueError("Reference hashes and package hashes disagree.")
    scope = json.loads((out / SCOPE).read_text(encoding="utf-8"))
    if scope.get("kind") != "scoped_companion_review_package" \
            or scope.get("full_release_completeness_claimed") is not False \
            or scope.get("selected_source_files") != len(referenced):
        raise ValueError("Scope metadata disagrees with package.")
    if scope.get("schema_version") == 1 and scope.get("fitted_spoon_included") is False:
        if any(n.startswith("results/controller_sweep_fitted_") and f"/{SPOON}/" in n for n in referenced):
            raise ValueError("Legacy scope excludes fitted-spoon records.")
    elif scope.get("schema_version") == 2 and scope.get("fitted_spoon_included") is True:
        census_data = {name: read_stable(out / name) for *_, nominal, fitted in census_paths()
                       for name in (nominal, fitted)}
        if scope.get("operating_point_censuses") != operating_point_censuses(census_data) \
                or scope.get("fitted_census_by_task") != fitted_census(census_data):
            raise ValueError("Recorded census metadata disagrees with the copied records.")
    else:
        raise ValueError("Unsupported review package scope schema.")
    return {"status": "verified", "directory": str(out), "source_files": len(referenced),
            "package_files": len(actual), "data_manifest_sha256": entries[SUMS],
            "package_manifest_sha256": digest((out / PACKAGE_SUMS).read_bytes()),
            "fitted_spoon_included": scope["fitted_spoon_included"],
            "public_archive_deposit_claimed": False}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    new = sub.add_parser("create")
    new.add_argument("--source-root", type=Path, default=ROOT)
    new.add_argument("--out", type=Path, required=True)
    check = sub.add_parser("verify")
    check.add_argument("directory", type=Path)
    args = ap.parse_args()
    try:
        result = create(args.source_root, args.out) if args.command == "create" else verify(args.directory)
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print(f"Review package failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
