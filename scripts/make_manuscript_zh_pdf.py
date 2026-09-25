# -*- coding: utf-8 -*-
"""Render the Chinese manuscript translation (manuscript_zh_2026-09-22.md) to PDF.

Self-contained: parses the controlled markdown subset used in that file
(headings, paragraphs, tables, blockquotes, lists, inline bold/italic/code,
and $...$ math) and typesets with reportlab. English submission untouched.

Usage: python scripts/make_manuscript_zh_pdf.py
"""
import re
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.fonts import addMapping

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "manuscript_zh_2026-09-22.md"
OUT = ROOT / "manuscript_zh_2026-09-22.pdf"

# ---------------- fonts: prefer Microsoft YaHei (has real bold), fall back to STSong CID
BODY, BOLD, MONO = "ZhBody", "ZhBody-Bold", "ZhMono"
try:
    pdfmetrics.registerFont(TTFont(BODY, r"C:\Windows\Fonts\msyh.ttc", subfontIndex=0))
    pdfmetrics.registerFont(TTFont(BOLD, r"C:\Windows\Fonts\msyhbd.ttc", subfontIndex=0))
    pdfmetrics.registerFont(TTFont(MONO, r"C:\Windows\Fonts\consola.ttf"))
    addMapping(BODY, 0, 0, BODY)
    addMapping(BODY, 1, 0, BOLD)   # <b> -> YaHei Bold
    addMapping(BODY, 0, 1, BODY)
    addMapping(BODY, 1, 1, BOLD)
except Exception:
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    BODY = BOLD = "STSong-Light"
    MONO = "Courier"
    addMapping(BODY, 0, 0, BODY)
    addMapping(BODY, 1, 0, BOLD)

# ---------------- light TeX -> Unicode cleanup for readable math in prose
TEX_SYMS = {
    "\\Delta": "Δ", "\\delta": "δ", "\\alpha": "α", "\\beta": "β", "\\gamma": "γ",
    "\\pi": "π", "\\sigma": "σ", "\\theta": "θ", "\\tau": "τ", "\\ell": "ℓ",
    "\\rho": "ρ", "\\times": "×", "\\approx": "≈", "\\le": "≤", "\\ge": "≥",
    "\\to": "→", "\\in": "∈", "\\forall": "∀", "\\succ": "≻", "\\bmod": "mod",
    "\\mathbb{E}": "E", "\\mathcal{C}": "C", "\\mathrm": "", "\\hat": "",
    "\\bar": "", "\\textbf": "", "\\emph": "", "\\texttt": "", "\\text": "",
    "\\big": "", "\\Big": "", "\\left": "", "\\right": "", "\\,": " ", "\\;": " ",
    "\\ ": " ", "\\{": "{", "\\}": "}", "\\%": "%", "\\_": "_", "\\&": "&",
    "\\epsilon": "ε", "\\mu": "μ", "\\lambda": "λ", "\\infty": "∞", "\\neq": "≠",
    "\\subset": "⊂", "\\cup": "∪", "\\cap": "∩", "\\cdot": "·", "\\max": "max",
    "\\min": "min", "\\lfloor": "⌊", "\\rfloor": "⌋", "\\langle": "⟨", "\\rangle": "⟩",
}


def tex_clean(s):
    for k, v in TEX_SYMS.items():
        s = s.replace(k, v)
    s = re.sub(r"\\[a-zA-Z]+", "", s)          # drop remaining macros
    s = s.replace("{", "").replace("}", "")
    s = re.sub(r"\^\s*([-+0-9a-zA-Z()]+)", r"<super>\1</super>", s)
    s = re.sub(r"_\s*([-+0-9a-zA-Z()]+)", r"<sub>\1</sub>", s)
    return re.sub(r"\s+", " ", s).strip()


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(s):
    """markdown inline -> reportlab paragraph markup (already XML-aware)."""
    out, i, buf = [], 0, ""
    # tokenise code spans first to protect them
    parts = re.split(r"(`[^`]+`)", s)
    for p in parts:
        if p.startswith("`") and p.endswith("`"):
            out.append('<font face="%s" size="8.5">%s</font>' % (MONO, esc(p[1:-1])))
            continue
        # math spans
        p2 = re.sub(r"\$\$([^$]+)\$\$|\$([^$]+)\$",
                    lambda m: '<i>%s</i>' % esc(tex_clean(m.group(1) or m.group(2))), p)
        p2 = esc(p2)
        # reportlab needs real tags back for <i>/<sub>/<super> we escaped; use placeholders
        out.append(p2)
    s = "".join(out)
    # restore tags created by tex_clean (they were escaped above); redo math cleanly:
    return s


# simpler correct approach: escape everything first, then apply markdown on escaped text
def render_inline(s):
    tokens = []

    def stash(txt):
        tokens.append(txt)
        return "\x00%d\x00" % (len(tokens) - 1)

    s = re.sub(r"`([^`]+)`", lambda m: stash('<font face="%s" size="8.5">%s</font>'
                                             % (MONO, esc(m.group(1)))), s)
    s = re.sub(r"\$\$([^$]+)\$\$", lambda m: stash("<i>%s</i>" % esc(tex_clean(m.group(1)))), s)
    s = re.sub(r"\$([^$]+)\$", lambda m: stash("<i>%s</i>" % esc(tex_clean(m.group(1)))), s)
    s = esc(s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<i>\1</i>", s)
    s = re.sub(r"\x00(\d+)\x00", lambda m: tokens[int(m.group(1))], s)
    return s


# ---------------- styles
S = {
    "title": ParagraphStyle("title", fontName=BOLD, fontSize=19, leading=26,
                            alignment=TA_CENTER, spaceAfter=4),
    "subtitle": ParagraphStyle("subtitle", fontName=BOLD, fontSize=14, leading=20,
                               alignment=TA_CENTER, spaceAfter=10),
    "h1": ParagraphStyle("h1", fontName=BOLD, fontSize=15, leading=20,
                         spaceBefore=16, spaceAfter=7, textColor=colors.HexColor("#1a3350")),
    "h2": ParagraphStyle("h2", fontName=BOLD, fontSize=12.5, leading=17,
                         spaceBefore=11, spaceAfter=5, textColor=colors.HexColor("#1a3350")),
    "h3": ParagraphStyle("h3", fontName=BOLD, fontSize=11, leading=15,
                         spaceBefore=8, spaceAfter=4),
    "body": ParagraphStyle("body", fontName=BODY, fontSize=10, leading=16.5,
                           alignment=TA_JUSTIFY, firstLineIndent=20, spaceAfter=5),
    "bodynoind": ParagraphStyle("bodynoind", fontName=BODY, fontSize=10, leading=16.5,
                                alignment=TA_JUSTIFY, spaceAfter=5),
    "quote": ParagraphStyle("quote", fontName=BODY, fontSize=10, leading=16,
                            leftIndent=18, rightIndent=12, spaceAfter=6,
                            textColor=colors.HexColor("#444444"),
                            borderColor=colors.HexColor("#c8c8c8"), borderWidth=0,
                            borderPadding=0),
    "li": ParagraphStyle("li", fontName=BODY, fontSize=10, leading=16,
                         leftIndent=24, firstLineIndent=-12, spaceAfter=3),
    "caption": ParagraphStyle("caption", fontName=BODY, fontSize=9, leading=14,
                              spaceBefore=4, spaceAfter=8, textColor=colors.HexColor("#333333")),
    "meta": ParagraphStyle("meta", fontName=BODY, fontSize=9.5, leading=15,
                           alignment=TA_CENTER, textColor=colors.HexColor("#333333")),
    "foot": ParagraphStyle("foot", fontName=BODY, fontSize=8, leading=11,
                           alignment=TA_CENTER, textColor=colors.HexColor("#888888")),
}


def is_table_block(lines, i):
    return (i + 1 < len(lines) and lines[i].lstrip().startswith("|")
            and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1] or ""))


def parse_table(lines, i):
    rows = []
    while i < len(lines) and lines[i].lstrip().startswith("|"):
        line = lines[i].strip()
        if not re.match(r"^\|[\s:|-]+\|$", line):
            cells = [c.strip() for c in line.strip("|").split("|")]
            rows.append(cells)
        i += 1
    return rows, i


def build(md):
    flow = []
    lines = md.split("\n")
    i, ncols_seen = 0, 0
    para = []

    def flush():
        if para:
            flow.append(Paragraph(render_inline(" ".join(para)), S["body"]))
            para.clear()

    while i < len(lines):
        ln = lines[i]
        st = ln.strip()

        if is_table_block(lines, i):
            flush()
            rows, i = parse_table(lines, i)
            if not rows:
                continue
            ncol = max(len(r) for r in rows)
            rows = [r + [""] * (ncol - len(r)) for r in rows]
            avail = 170 * mm
            data = [[Paragraph(render_inline(c), ParagraphStyle(
                        "tc", fontName=BODY if ri else BOLD, fontSize=8.3, leading=11.5,
                        alignment=TA_LEFT)) for c in r] for ri, r in enumerate(rows)]
            t = Table(data, colWidths=[avail / ncol] * ncol, repeatRows=1)
            t.setStyle(TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b5b5b5")),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef5")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7f9fb")]),
            ]))
            flow.append(t)
            flow.append(Spacer(1, 7))
            continue

        if st.startswith("```"):
            flush()
            i += 1
            code = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i]); i += 1
            i += 1
            flow.append(Paragraph('<font face="%s" size="8.5">%s</font>'
                                  % (MONO, "<br/>".join(esc(c) for c in code)), S["quote"]))
            continue

        if not st:
            flush(); i += 1; continue
        if st == "---":
            flush()
            flow.append(Spacer(1, 4))
            flow.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#9db3c8")))
            flow.append(Spacer(1, 4))
            i += 1; continue
        if st.startswith("# "):
            flush(); flow.append(Paragraph(render_inline(st[2:]), S["h1"])); i += 1; continue
        if st.startswith("## "):
            flush()
            txt = st[3:]
            style = S["title"] if txt.startswith("什么决定") else S["h2"]
            flow.append(Paragraph(render_inline(txt), style)); i += 1; continue
        if st.startswith("### "):
            flush(); flow.append(Paragraph(render_inline(st[4:]), S["h3"])); i += 1; continue
        if st.startswith("> "):
            flush()
            q = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                q.append(lines[i].strip()[2:]); i += 1
            flow.append(Paragraph("│ " + render_inline(" ".join(q)), S["quote"]))
            continue
        m = re.match(r"^(\d+)\.\s+(.*)$", st)
        if m:
            flush()
            flow.append(Paragraph("<b>%s.</b> %s" % (m.group(1), render_inline(m.group(2))), S["li"]))
            i += 1; continue
        if st.startswith("- "):
            flush()
            flow.append(Paragraph("• " + render_inline(st[2:]), S["li"]))
            i += 1; continue
        para.append(st); i += 1

    flush()
    return flow


def on_page(canv, doc):
    canv.saveState()
    canv.setFont(BODY, 8)
    canv.setFillColor(colors.HexColor("#999999"))
    canv.drawCentredString(A4[0] / 2, 12 * mm, "— %d —" % doc.page)
    if doc.page > 1:
        canv.drawString(20 * mm, A4[1] - 12 * mm, "什么决定了仿真基准的排名？（中文审阅版）")
        canv.drawRightString(A4[0] - 20 * mm, A4[1] - 12 * mm, "2026-09-22")
    canv.restoreState()


def main():
    md = SRC.read_text(encoding="utf-8")
    doc = BaseDocTemplate(str(OUT), pagesize=A4,
                          leftMargin=20 * mm, rightMargin=20 * mm,
                          topMargin=18 * mm, bottomMargin=18 * mm,
                          title="什么决定了仿真基准的排名？（中文审阅版）",
                          author="Jun Ji et al. / 中译 枢")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=on_page)])
    doc.build(build(md))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
