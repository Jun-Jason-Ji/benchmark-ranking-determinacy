"""Check local reference/cross-reference integrity after the primary-source audit.

This checks structure and records the audited identifiers; it does not infer that
a paper exists from a syntactically valid DOI. Primary-source evidence is kept in
reviews/2026-09-23_final_reference_audit/.
"""
from pathlib import Path
import argparse
import json
import re
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]


def entries(text):
    found = []
    for m in re.finditer(r'(?m)^@(\w+)\{([^,]+),', text):
        level, i = 1, m.end()
        while i < len(text) and level:
            if text[i] == '{' and (i == 0 or text[i-1] != '\\'):
                level += 1
            elif text[i] == '}' and (i == 0 or text[i-1] != '\\'):
                level -= 1
            i += 1
        if level:
            raise ValueError(f'Unbalanced entry {m[2]}')
        block = text[m.end():i-1]
        fields = {}
        pos = 0
        while match := re.search(r'(\w+)\s*=\s*\{', block[pos:]):
            name = match[1].lower()
            a = pos + match.end()
            depth, b = 1, a
            while b < len(block) and depth:
                if block[b] == '{' and block[b-1] != '\\': depth += 1
                if block[b] == '}' and block[b-1] != '\\': depth -= 1
                b += 1
            if depth or name in fields:
                raise ValueError(f'Invalid/duplicate field {m[2]}/{name}')
            fields[name] = re.sub(r'\s+', ' ', block[a:b-1]).strip()
            pos = b
        found.append({'key': m[2].strip(), 'type': m[1].lower(), **fields})
    return found


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, default=ROOT/'submission/autonomous_robots/main.tex')
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    text = args.source.read_text(encoding='utf-8')
    bib = entries((args.source.parent/'references.bib').read_text(encoding='utf-8'))
    cited = set()
    for m in re.finditer(r'\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}', text):
        cited.update(k.strip() for k in m[1].split(','))
    keys = [b['key'] for b in bib]
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    refs = re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}', text)
    report = {'source': str(args.source), 'entries': len(bib), 'cited_keys': len(cited),
              'missing_bib_keys': sorted(cited-set(keys)), 'uncited_bib_keys': sorted(set(keys)-cited),
              'duplicate_bib_keys': [k for k,n in Counter(keys).items() if n > 1],
              'undefined_internal_labels': sorted(set(refs)-set(labels)),
              'duplicate_labels': [k for k,n in Counter(labels).items() if n > 1],
              'bibliography': bib,
              'verification_scope': 'Structural check only. Existence, metadata and claim scope were checked against primary sources in the accompanying audit reports.'}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    errors = {k:v for k,v in report.items() if (k.startswith(('missing','uncited','duplicate','undefined'))) and v}
    print(json.dumps({'entries':len(bib), 'cited_keys':len(cited), 'doi_entries':sum('doi' in b for b in bib), 'errors':errors}, ensure_ascii=False))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
