"""Build the self-contained bilingual research-route page.

Reads docs/site/research_route.template.html, inlines results/figures/*.png as base64 data URIs
(placeholders {{FIG:fig_name}}), and writes docs/research_route.html plus a dated copy
(the dated name used to drift a day behind the content it carried).
No network, no CDN, no external fonts.
"""
import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "docs/site/research_route.template.html"
OUT = ROOT / "docs/research_route.html"
DATED = ROOT / f"docs/research_route_{__import__('time').strftime('%Y-%m-%d')}.html"
FIGS = ROOT / "results/figures"


def main():
    html = TEMPLATE.read_text(encoding="utf-8")

    def repl(m):
        p = FIGS / f"{m.group(1)}.png"
        if not p.exists():
            print("missing figure", p, file=sys.stderr)
            return ""
        return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode("ascii")

    html = re.sub(r"\{\{FIG:([a-z0-9_]+)\}\}", repl, html)
    assert "{{" not in html, "unresolved placeholder"
    assert "https://" not in html.replace("https://github.com", "").replace("https://huggingface.co", "").replace("https://arxiv.org", "").replace("https://rail-berkeley.github.io", "").replace("https://ieeexplore", ""), "unexpected external resource"
    OUT.write_text(html, encoding="utf-8")
    DATED.write_text(html, encoding="utf-8")
    print(OUT, f"{OUT.stat().st_size / 1024:.0f} KB", "| dated copy:", DATED.name)


if __name__ == "__main__":
    main()
