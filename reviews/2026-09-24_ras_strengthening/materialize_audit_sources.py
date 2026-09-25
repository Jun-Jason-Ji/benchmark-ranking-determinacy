"""Materialize frozen source inputs only in an extracted research working copy."""
from pathlib import Path,PurePosixPath
import hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
snap=HERE/'source_snapshots'
assert not (ROOT/'.git').exists(),'Use a fresh extracted research working copy, not a checkout.'
assert not (ROOT/'.venv-windows-ms3/Scripts').exists(),'Refusing an existing Python environment.'
data=json.loads((snap/'MANIFEST.json').read_text())
for rel,item in data['files'].items():
    q=PurePosixPath(rel);assert not q.is_absolute() and '..' not in q.parts
    target=(ROOT/rel).resolve();target.relative_to(ROOT.resolve())
    source=(snap/item['snapshot']).resolve();source.relative_to(snap.resolve())
    b=source.read_bytes();assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256']
    if target.exists():assert target.read_bytes()==b,f'Refusing to overwrite different source: {rel}'
    else:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
print(f"Verified/materialized {len(data['files'])} read-only source inputs; no package installed.")
