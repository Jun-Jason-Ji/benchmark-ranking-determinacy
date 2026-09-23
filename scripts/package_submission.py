"""Freeze journal submission materials separately from the live research-data release.

Usage:
  python scripts/package_submission.py create --out output/submission_2026-09-23
  python scripts/package_submission.py verify output/submission_2026-09-23

The output directory must not exist. Only explicitly selected manuscript/material files
are copied, after two byte-level checks that the source files did not change. No records,
analysis outputs, root SHA256SUMS.txt, services, or queues are changed or included.
This is a write-once workflow with verifiable hashes, not OS-enforced immutable storage.
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
MANUSCRIPT = Path("submission/autonomous_robots")
MANIFEST = "SUBMISSION_MANIFEST.json"
CHECKSUMS = "SUBMISSION_SHA256SUMS.txt"
MARKER = ".INCOMPLETE"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def selection(root: Path, evidence_index: Path | None = None) -> dict[str, Path]:
    """Destination-relative name -> existing source; deliberately excludes results/."""
    required = ["main.tex", "main.pdf", "main.bbl", "references.bib", "sn-jnl.cls",
                "sn-apacite.bst", "cover_letter.md", "declarations_for_interface.md"]
    required += [f"Fig{i}.eps" for i in range(1, 7)]
    required += [f"Fig{i}-eps-converted-to.pdf" for i in range(1, 7)]
    optional = ["cover_letter.pdf", "cover_letter.docx", "SUBMISSION_CHECKLIST.md"]
    files = {}
    for name in required + optional:
        src = root / MANUSCRIPT / name
        if not src.is_file():
            if name in required:
                raise ValueError(f"Required submission file missing: {src}")
            continue
        files[(MANUSCRIPT / name).as_posix()] = src
    if evidence_index:
        src = evidence_index.resolve()
        if not src.is_relative_to(root) or src.suffix.lower() not in {".md", ".json"}:
            raise ValueError("Evidence index must be a .md/.json file inside the repository.")
        if not src.is_file():
            raise ValueError(f"Evidence index missing: {src}")
        files[f"reviewer_evidence_index{src.suffix.lower()}"] = src
    for src in files.values():
        if src.is_symlink() or not src.resolve().is_relative_to(root):
            raise ValueError(f"Refusing a source outside the repository or a symlink: {src}")
    return files


def git_value(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                                text=True, encoding="utf-8", timeout=20)
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def read_stable(src: Path) -> tuple[bytes, int]:
    before = src.stat()
    data = src.read_bytes()
    after = src.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError(f"Source changed while reading; retry after edits finish: {src}")
    if len(data) != after.st_size:
        raise ValueError(f"Incomplete source read: {src}")
    return data, after.st_mtime_ns


def package_readme(created: str, revision: str | None) -> bytes:
    return f"""# Journal submission materials snapshot

Created (UTC): {created}
Source Git HEAD: {revision or 'unavailable'}

This package freezes the manuscript source, compiled PDF, bibliography, figures,
cover letter, submission declarations, and any supplied reviewer evidence index.
It is **not the full reproducibility/data release** and is not evidence of a Zenodo
deposit. No episode records, live analysis outputs, or repository data checksum
manifest are included. The companion data/code package separately contains the
completed eggplant and spoon operating-point comparisons used by this manuscript.
Statements inside copied documents retain their own scope and must be reviewed separately.

The manifest records hashes of the actual copied bytes, including uncommitted
material edits. Git HEAD alone is not the identity of this snapshot. Creation
refuses an existing destination; later changes are detected by verification.
The filesystem itself is not write-protected or tamper-proof.

## Files for submission

The files in `submission/autonomous_robots/` include `main.pdf` and the manuscript
source bundle (`main.tex`, `main.bbl`, `references.bib`, the journal class/style,
and six EPS figures with their PDF conversions). `cover_letter.md` and any rendered
cover-letter files are separate submission materials. The declarations and checklist
are preparation aids, not pages to append to the manuscript.

Compile from that directory using a TeX installation:

    pdflatex main
    bibtex main
    pdflatex main
    pdflatex main

Compile in a **copy** of this snapshot; generated files would change its inventory.
This tool does not compile TeX or certify visual correctness of the supplied PDF.

## Integrity verification

From the research repository:

    python scripts/package_submission.py verify <this-directory>

The verifier checks every digest and rejects missing, unexpected, or changed files.
On a system providing sha256sum, `sha256sum -c SUBMISSION_SHA256SUMS.txt` also checks
the listed files, but does not detect extra files. Keep this material-package
manifest separate from the root research-data `SHA256SUMS.txt`.
""".encode("utf-8")


def create_snapshot(root: Path, out: Path, evidence_index: Path | None = None) -> dict:
    root, out = root.resolve(), out.resolve()
    if out.exists():
        raise ValueError(f"Destination already exists; snapshots are never overwritten: {out}")
    sources = selection(root, evidence_index)
    data, metadata = {}, []
    for target, src in sorted(sources.items()):
        blob, mtime = read_stable(src)
        data[target] = blob
        metadata.append({"path": target, "source": src.relative_to(root).as_posix(),
                         "source_mtime_ns": mtime, "bytes": len(blob), "sha256": digest(blob)})
    # A second full pass catches edits made while another source was being read.
    if selection(root, evidence_index) != sources:
        raise ValueError("Submission file selection changed during capture; retry after edits finish.")
    for target, src in sources.items():
        if digest(read_stable(src)[0]) != digest(data[target]):
            raise ValueError(f"Source changed during capture; no snapshot created: {src}")
    created = datetime.now(timezone.utc).isoformat()
    head = git_value(root, "rev-parse", "HEAD")
    data["README.md"] = package_readme(created, head)
    metadata.append({"path": "README.md", "source": "generated:package_submission.py",
                     "bytes": len(data["README.md"]), "sha256": digest(data["README.md"])})
    manifest = {"schema_version": 1, "kind": "submission_materials_snapshot",
                "created_utc": created, "git_head": head,
                "full_data_release_included": False, "archive_deposit_verified": False,
                "episode_records_included": False,
                "files": sorted(metadata, key=lambda row: row["path"])}
    data[MANIFEST] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    checksum_text = "# Submission materials only; NOT the research-data release.\n"
    checksum_text += "".join(f"{digest(blob)} *{name}\n" for name, blob in sorted(data.items()))
    data[CHECKSUMS] = checksum_text.encode("utf-8")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.mkdir()  # Exclusive: a concurrent creator cannot overwrite this snapshot.
    (out / MARKER).write_text("Snapshot creation has not completed.\n", encoding="utf-8")
    for name, blob in sorted(data.items()):
        dest = out / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("xb") as stream:
            stream.write(blob)
    (out / MARKER).unlink()
    return verify_snapshot(out)


def safe_relative(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and ".." not in p.parts and "\\" not in name \
        and ":" not in name and p.as_posix() == name


def verify_snapshot(out: Path) -> dict:
    out = out.resolve()
    if not out.is_dir() or (out / MARKER).exists():
        raise ValueError(f"Not a completed snapshot: {out}")
    entries = {}
    for line in (out / CHECKSUMS).read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        match = re.fullmatch(r"([0-9a-f]{64}) \*(.+)", line)
        if not match or not safe_relative(match[2]) or match[2] in entries:
            raise ValueError(f"Invalid or duplicate checksum entry: {line}")
        entries[match[2]] = match[1]
    if MANIFEST not in entries or "README.md" not in entries:
        raise ValueError("Snapshot checksum inventory is missing its manifest or README.")
    actual = set()
    for path in out.rglob("*"):
        if path.is_symlink() or not path.resolve().is_relative_to(out):
            raise ValueError(f"Symlink or path escape in snapshot: {path}")
        if path.is_file():
            actual.add(path.relative_to(out).as_posix())
    expected = set(entries) | {CHECKSUMS}
    if actual != expected:
        raise ValueError(f"Inventory mismatch; missing={sorted(expected - actual)}, "
                         f"unexpected={sorted(actual - expected)}")
    for name, wanted in entries.items():
        if digest((out / name).read_bytes()) != wanted:
            raise ValueError(f"Checksum mismatch: {name}")
    manifest = json.loads((out / MANIFEST).read_text(encoding="utf-8"))
    if manifest.get("kind") != "submission_materials_snapshot" \
            or manifest.get("full_data_release_included") is not False:
        raise ValueError("Manifest is not a submission-materials-only snapshot.")
    rows = manifest.get("files", [])
    if len({row["path"] for row in rows}) != len(rows):
        raise ValueError("Duplicate file in manifest.")
    if {row["path"] for row in rows} | {MANIFEST} != set(entries):
        raise ValueError("Manifest and checksum inventory disagree.")
    for row in rows:
        if row["sha256"] != entries[row["path"]] \
                or row["bytes"] != (out / row["path"]).stat().st_size:
            raise ValueError(f"Manifest metadata mismatch: {row['path']}")
    return {"status": "verified", "directory": str(out), "files": len(entries),
            "manifest_sha256": entries[MANIFEST], "data_release_included": False}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    commands = ap.add_subparsers(dest="command", required=True)
    create = commands.add_parser("create", help="Create a new write-once materials snapshot.")
    create.add_argument("--out", type=Path, required=True)
    create.add_argument("--evidence-index", type=Path,
                        help="Optional existing .md/.json reviewer evidence index in the repository.")
    verify = commands.add_parser("verify", help="Check hashes and exact inventory; makes no changes.")
    verify.add_argument("directory", type=Path)
    args = ap.parse_args()
    try:
        result = create_snapshot(ROOT, args.out, args.evidence_index) if args.command == "create" \
            else verify_snapshot(args.directory)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Submission snapshot failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
