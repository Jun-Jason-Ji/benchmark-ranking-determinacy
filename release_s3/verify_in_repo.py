"""Verify the S3 research package as it sits inside this repository.

Supplement S3 was distributed as one archive (SHA-256
eb2813aec994a4972df4420b91052e42bb0722b89476343a72bf72951b1d772c) whose paths are
relative to its own root. In this repository the payload files keep those same paths
relative to the repository root; only the package-level files (README.md,
SHA256SUMS.txt, DATA_*, PACKAGE_PROVENANCE.json, licenses/, verify_manifest.py)
live in release_s3/. The original verify_manifest.py applies to an extracted archive;
this script checks every entry of release_s3/SHA256SUMS.txt against the repository.
Files outside the list are not checked, because the repository contains more than S3.
"""
from pathlib import Path
import hashlib

here = Path(__file__).resolve().parent
repo = here.parent
relocated = {'README.md', 'SHA256SUMS.txt', 'DATA_SCOPE.json', 'DATA_SHA256SUMS.txt',
             'DATA_VERIFICATION.json', 'PACKAGE_PROVENANCE.json', 'verify_manifest.py',
             'licenses/BASELINE_NOTICE.md', 'licenses/CURRENT_EVIDENCE_NOTICE.md'}
bad = []
n = 0
for line in (here / 'SHA256SUMS.txt').read_text(encoding='utf8').splitlines():
    digest, name = line.split('  ', 1)
    p = (here if name in relocated else repo) / name
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != digest:
        bad.append(name)
    n += 1
if bad:
    raise SystemExit(f'FAIL: {len(bad)} of {n} files differ or are missing, e.g. {bad[:5]}')
print(f'PASS: {n} S3 payload files verified in the repository')
