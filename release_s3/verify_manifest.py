"""Verify the curated supplement without modifying it."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent
entries={}
for line in (root/'SHA256SUMS.txt').read_text(encoding='utf8').splitlines():
    digest,name=line.split('  ',1)
    p=(root/name).resolve()
    assert p.is_relative_to(root.resolve()), name
    assert p.is_file(), name
    assert hashlib.sha256(p.read_bytes()).hexdigest()==digest, name
    entries[name]=digest
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
assert actual==set(entries)|{'SHA256SUMS.txt'}, 'Unexpected or missing files'
print(f'PASS: {len(entries)} payload files verified')
