"""Separate replication of *declarations* from agreement to abstain, on the Track R replicate pairs.

Table 8's "stable" column counts a pair as stable whenever the two replicates return the same
verdict, and abstain-abstain qualifies. A criterion that abstains everywhere therefore scores 1.00,
which the paper says plainly for the all-axes row. The controller-axis row needs the same treatment
for a different reason: its 0.88 is 7 abstain-abstain agreements out of 8, so it cannot be read as
evidence that its declarations replicate. This script reports, per criterion:

  stable            same verdict on both replicates (the published column, reproduced as a check)
  declared_pairs    pairs where at least one replicate declared an ordering
  decl_replicated   of those, how many had BOTH replicates declare the SAME ordering
  decl_contradicted of those, how many had both declare OPPOSITE orderings

decl_replicated / declared_pairs is the affirmative replication rate -- the quantity a reader who
wants to trust a declaration actually needs, and the one the stability column cannot supply.

Input is the per-pair verdict table in results/benchmark/track_r/track_r_summary.md, whose entries
are '+', '-' or '0' per replicate. Only same-grid replications are counted, matching the headline.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "results/benchmark/track_r/track_r_summary.md"
# Datasets whose two replicate sides enumerate the same configuration grid. eggplant_stacks does not
# (8x8 vs 8x3 orientation grids), so it is excluded here exactly as it is from the headline table.
SAME_GRID = {"eggplant_seedsets", "spoon_stacks", "carrot_stacks"}
METHODS = ["point", "union_ctrl", "union_all"]


def parse():
    rows = []
    body = SRC.read_text(encoding="utf-8")
    sec = body.split("## Verdicts per pair", 1)[1]
    for line in sec.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 5 or cells[0] in ("dataset", "---") or set(cells[0]) <= set("-: "):
            continue
        ds, pair = cells[0], cells[1]
        if ds not in SAME_GRID:
            continue
        vs = {}
        for m, cell in zip(METHODS, cells[2:]):
            mt = re.match(r"^([+\-0])/([+\-0])$", cell)
            if not mt:
                raise SystemExit(f"unparsed verdict cell {cell!r} on line: {line}")
            vs[m] = (mt.group(1), mt.group(2))
        rows.append((ds, pair, vs))
    return rows


def main():
    rows = parse()
    print(f"# Declaration replication on the {len(rows)} same-grid replicate pairs\n")
    print("| criterion | pairs | stable | declared pairs | declarations replicated | rate |")
    print("|---|---:|---:|---:|---:|---:|")
    detail = []
    for m in METHODS:
        stable = sum(1 for _, _, v in rows if v[m][0] == v[m][1])
        decl = [(ds, p, v[m]) for ds, p, v in rows if v[m][0] != "0" or v[m][1] != "0"]
        rep = [d for d in decl if d[2][0] == d[2][1] != "0"]
        con = [d for d in decl if d[2][0] != "0" and d[2][1] != "0" and d[2][0] != d[2][1]]
        rate = f"{len(rep) / len(decl):.2f}" if decl else "n/a (never declared)"
        print(f"| {m} | {len(rows)} | {stable / len(rows):.2f} | {len(decl)} | {len(rep)} | {rate} |")
        detail.append((m, decl, rep, con))
    print("\n## Which pairs carried a declaration\n")
    for m, decl, rep, con in detail:
        print(f"**{m}** --- {len(decl)} pair(s) with a declaration on at least one replicate:")
        if not decl:
            print("  (none: this criterion abstained on every pair, so its stability is entirely "
                  "agreement to abstain)")
        for ds, p, (a, b) in decl:
            tag = "replicated" if a == b else "not replicated (declared on one side only)"
            if a != "0" and b != "0" and a != b:
                tag = "CONTRADICTED"
            print(f"  - {ds} / {p}: {a}/{b} -- {tag}")
        print()
    print("## Reading\n")
    for m, decl, rep, con in detail:
        if not decl:
            print(f"- {m}: made no declaration on any pair. Its stability score is 1.00 by "
                  f"abstention and says nothing about declaration reliability.")
        else:
            print(f"- {m}: {len(rep)} of {len(decl)} declared pairs replicated "
                  f"({len(rep) / len(decl):.2f}); {len(con)} contradicted.")


if __name__ == "__main__":
    main()
