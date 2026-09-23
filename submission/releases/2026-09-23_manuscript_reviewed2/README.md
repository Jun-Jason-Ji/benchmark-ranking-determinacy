# Journal submission materials snapshot

Created (UTC): 2026-09-23T12:20:30.398061+00:00
Source Git HEAD: 10c8a3b53af183c689ff8e45c8ece8b0eca57716

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
