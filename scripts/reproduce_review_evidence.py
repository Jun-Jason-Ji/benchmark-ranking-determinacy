"""Regenerate selected manuscript evidence without evaluation or modifying recorded data.

Use the companion review snapshot for a frozen input set. The required --out directory must
not exist and may be outside the snapshot, preserving its inventory for verification.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSES = (
    ('make_core_table.py', 'CORE_TABLE.md'),
    ('make_evidence_chain.py', 'EVIDENCE_CHAIN.md'),
    ('analyze_multiplicity.py', 'MULTIPLICITY.md'),
    ('analyze_fitted_point.py', 'FITTED_POINT.md'),
    ('analyze_official_protocol.py', 'OFFICIAL_PROTOCOL.md'),
    ('analyze_torque_scope_current.py', 'TORQUE_SCOPE_CURRENT.json'),
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True, help='New output directory')
    args = parser.parse_args()
    out = args.out.resolve()
    if out.exists():
        parser.error('Output directory must not exist; use a new path.')
    out.mkdir(parents=True)
    records = []
    for script, filename in ANALYSES:
        source = ROOT / 'scripts' / script
        target = out / filename
        command = [sys.executable, str(source), '--out', str(target)]
        with (out / f'{source.stem}.log').open('w', encoding='utf-8') as log:
            result = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        record = {'script': script, 'output': filename, 'returncode': result.returncode,
                  'script_sha256': hashlib.sha256(source.read_bytes()).hexdigest()}
        if target.is_file():
            record['output_sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
        records.append(record)
        (out / 'REPRODUCTION.json').write_text(json.dumps({
            'source_root': str(ROOT), 'analyses': records,
            'scope': 'Selected headline analyses; not every experiment or a new statistical guarantee.'
        }, indent=2) + '\n', encoding='utf-8')
        if result.returncode != 0 or not target.is_file():
            raise SystemExit(f'{script} failed; inspect {out / (source.stem + ".log")}')
        print(f'OK {filename}', flush=True)
    print(f'Completed {len(records)} analyses in {out}')


if __name__ == '__main__':
    main()
