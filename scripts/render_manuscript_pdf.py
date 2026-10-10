#!/usr/bin/env python3
"""Render paper/manuscript.md into a clearly labelled draft PDF with ReportLab."""
from __future__ import annotations

import html
import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    ListFlowable, ListItem, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
)
from svglib.svglib import svg2rlg

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper" / "manuscript.md"
OUTPUT = ROOT / "paper" / "manuscript-draft.pdf"
PAGE_WIDTH, PAGE_HEIGHT = A4
CONTENT_WIDTH = PAGE_WIDTH - 34 * mm


def register_fonts() -> tuple[str, str, str]:
    """Register Unicode fonts for Greek letters and punctuation when available."""
    font_dir = Path("/usr/share/fonts/truetype/dejavu")
    regular = font_dir / "DejaVuSans.ttf"
    bold = font_dir / "DejaVuSans-Bold.ttf"
    italic = font_dir / "DejaVuSans-Oblique.ttf"
    mono = font_dir / "DejaVuSansMono.ttf"
    if all(p.exists() for p in (regular, bold, italic, mono)):
        pdfmetrics.registerFont(TTFont("PaperSans", str(regular)))
        pdfmetrics.registerFont(TTFont("PaperSans-Bold", str(bold)))
        pdfmetrics.registerFont(TTFont("PaperSans-Italic", str(italic)))
        pdfmetrics.registerFont(TTFont("PaperMono", str(mono)))
        pdfmetrics.registerFontFamily(
            "PaperSans", normal="PaperSans", bold="PaperSans-Bold",
            italic="PaperSans-Italic", boldItalic="PaperSans-Bold"
        )
        return "PaperSans", "PaperSans-Bold", "PaperMono"
    return "Helvetica", "Helvetica-Bold", "Courier"


def inline_markup(text: str, mono_font: str) -> str:
    """Translate the manuscript's limited Markdown inline syntax to ReportLab XML."""
    text = escape(text)

    def link_replace(match: re.Match[str]) -> str:
        label = match.group(1)
        url = html.unescape(match.group(2))
        return f'<link href="{html.escape(url, quote=True)}" color="#2457A6">{label}</link>'

    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+|[^)]+)\)", link_replace, text)
    tick = chr(96)
    text = re.sub(re.escape(tick) + r"([^" + tick + r"]+)" + re.escape(tick),
                  lambda m: f'<font name="{mono_font}">{m.group(1)}</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"~~([^~]+)~~", r"<strike>\1</strike>", text)
    return text


def parse_table(lines: list[str], body_font: str, bold_font: str, mono_font: str) -> Table:
    rows: list[list[str]] = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            continue
        rows.append(cells)
    if not rows:
        return Table([[""]])
    cell_style = ParagraphStyle("TableCell", fontName=body_font, fontSize=7.1, leading=8.7, spaceAfter=0)
    wrapped = [[Paragraph(inline_markup(cell, mono_font), cell_style) for cell in row] for row in rows]
    ncols = max(len(row) for row in wrapped)
    for row in wrapped:
        while len(row) < ncols:
            row.append(Paragraph("", cell_style))
    table = Table(wrapped, colWidths=[CONTENT_WIDTH / ncols] * ncols, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EDF4")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#17243A")),
        ("FONTNAME", (0, 0), (-1, 0), bold_font),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B8C0CC")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def add_svg(path: Path):
    drawing = svg2rlg(str(path))
    if drawing is None:
        return None
    scale = min(CONTENT_WIDTH / max(drawing.width, 1), 0.72 * PAGE_HEIGHT / max(drawing.height, 1), 1.0)
    drawing.width *= scale
    drawing.height *= scale
    drawing.scale(scale, scale)
    return drawing


def page_decor(canvas, doc) -> None:
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D8DEE8"))
    canvas.setLineWidth(0.5)
    canvas.line(17 * mm, 14 * mm, PAGE_WIDTH - 17 * mm, 14 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#697586"))
    canvas.drawString(17 * mm, 9 * mm, "DRAFT — NOT SUBMISSION-READY")
    canvas.drawRightString(PAGE_WIDTH - 17 * mm, 9 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build_story(markdown: str, body_font: str, bold_font: str, mono_font: str) -> list:
    base = getSampleStyleSheet()
    base.add(ParagraphStyle(
        "PaperTitle", parent=base["Title"], fontName=bold_font, fontSize=18,
        leading=23, alignment=TA_CENTER, textColor=colors.HexColor("#17243A"), spaceAfter=10
    ))
    base.add(ParagraphStyle(
        "PaperH1", parent=base["Heading1"], fontName=bold_font, fontSize=13.5,
        leading=17, textColor=colors.HexColor("#17365D"), spaceBefore=12, spaceAfter=5, keepWithNext=True
    ))
    base.add(ParagraphStyle(
        "PaperH2", parent=base["Heading2"], fontName=bold_font, fontSize=10.5,
        leading=13, textColor=colors.HexColor("#2457A6"), spaceBefore=8, spaceAfter=4, keepWithNext=True
    ))
    base.add(ParagraphStyle(
        "PaperH3", parent=base["Heading3"], fontName=bold_font, fontSize=9.3,
        leading=11.5, textColor=colors.HexColor("#35445B"), spaceBefore=6, spaceAfter=3, keepWithNext=True
    ))
    base.add(ParagraphStyle(
        "PaperBody", parent=base["BodyText"], fontName=body_font, fontSize=8.3,
        leading=11.5, alignment=TA_JUSTIFY, spaceAfter=4.5, allowWidows=0, allowOrphans=0
    ))
    base.add(ParagraphStyle(
        "PaperList", parent=base["BodyText"], fontName=body_font, fontSize=8.1,
        leading=10.8, leftIndent=10, firstLineIndent=-7, spaceAfter=2.8
    ))
    base.add(ParagraphStyle(
        "PaperCaption", parent=base["BodyText"], fontName=body_font, fontSize=7.2,
        leading=9, textColor=colors.HexColor("#596579"), alignment=TA_CENTER, spaceBefore=2, spaceAfter=6
    ))
    base.add(ParagraphStyle(
        "PaperSmall", parent=base["BodyText"], fontName=body_font, fontSize=7.6,
        leading=9.8, spaceAfter=3
    ))

    lines = markdown.splitlines()
    story: list = []
    i = 0
    first_heading = True
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        image_match = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", line)
        if image_match:
            alt, rel_path = image_match.groups()
            image_path = (SOURCE.parent / rel_path).resolve()
            if image_path.exists() and image_path.suffix.lower() == ".svg":
                drawing = add_svg(image_path)
                if drawing is not None:
                    story.extend([Spacer(1, 4), drawing, Paragraph(inline_markup(alt, mono_font), base["PaperCaption"])])
            else:
                story.append(Paragraph(f"[Figure asset unavailable: {escape(alt)}]", base["PaperCaption"]))
            i += 1
            continue

        if line.startswith("|") and i + 1 < len(lines) and lines[i + 1].strip().startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            story.extend([Spacer(1, 3), parse_table(table_lines, body_font, bold_font, mono_font), Spacer(1, 6)])
            continue

        heading = re.match(r"^(#{1,3})\s+(.*)$", line)
        if heading:
            level, title = len(heading.group(1)), heading.group(2)
            if level == 2 and title.strip().lower() == "references":
                story.append(PageBreak())
            if level == 1 and first_heading:
                story.append(Paragraph(inline_markup(title, mono_font), base["PaperTitle"]))
                first_heading = False
            else:
                story.append(Paragraph(inline_markup(title, mono_font), base[{1: "PaperH1", 2: "PaperH2", 3: "PaperH3"}[level]]))
            i += 1
            continue

        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", line):
            story.append(Spacer(1, 4))
            i += 1
            continue

        if re.match(r"^[-*]\s+", line) or re.match(r"^\d+\.\s+", line):
            ordered = bool(re.match(r"^\d+\.\s+", line))
            items = []
            while i < len(lines):
                candidate = lines[i].strip()
                match = re.match(r"^(?:[-*]|\d+\.)\s+(.*)$", candidate)
                if not match:
                    break
                items.append(ListItem(Paragraph(inline_markup(match.group(1), mono_font), base["PaperList"]), leftIndent=9))
                i += 1
            story.append(ListFlowable(
                items, bulletType="1" if ordered else "bullet", start="1",
                leftIndent=13, bulletFontName=body_font, bulletFontSize=7, spaceAfter=4
            ))
            continue

        if line.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            quote = " ".join(quote_lines)
            story.append(Paragraph(inline_markup(quote, mono_font), ParagraphStyle(
                "PaperQuote", parent=base["PaperBody"], leftIndent=9, rightIndent=9,
                borderColor=colors.HexColor("#AAB7C8"), borderWidth=0.7, borderPadding=5,
                backColor=colors.HexColor("#F5F7FA")
            )))
            continue

        paragraph_lines = [line]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if (
                not nxt or re.match(r"^#{1,3}\s+", nxt) or nxt.startswith("|")
                or nxt.startswith("![") or nxt.startswith("> ")
                or re.match(r"^[-*]\s+", nxt) or re.match(r"^\d+\.\s+", nxt)
                or re.fullmatch(r"-{3,}|\*{3,}|_{3,}", nxt)
            ):
                break
            paragraph_lines.append(nxt)
            i += 1
        paragraph = " ".join(paragraph_lines)
        if paragraph.startswith("**Author:**") or paragraph.startswith("**Research area:**") or paragraph.startswith("**Study type:**") or paragraph.startswith("**Version:**"):
            style = base["PaperSmall"]
        else:
            style = base["PaperBody"]
        story.append(Paragraph(inline_markup(paragraph, mono_font), style))

    return story


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Manuscript source not found: {SOURCE}")
    body_font, bold_font, mono_font = register_fonts()
    markdown = SOURCE.read_text(encoding="utf-8")
    story = build_story(markdown, body_font, bold_font, mono_font)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, rightMargin=17 * mm, leftMargin=17 * mm,
        topMargin=17 * mm, bottomMargin=19 * mm,
        title="Effects of Appended Distractor Context on RAG Answer Quality and Generation Latency — Draft",
        author="Shaik Jouzia Afreen H",
        subject="Exploratory appended-context RAG evaluation; not retrieval-ranking robustness",
    )
    doc.build(story, onFirstPage=page_decor, onLaterPages=page_decor)
    if OUTPUT.stat().st_size < 8_000:
        raise SystemExit(f"PDF looks unexpectedly small: {OUTPUT.stat().st_size} bytes")
    print(f"Rendered: {OUTPUT.relative_to(ROOT)}")
    print(f"Bytes: {OUTPUT.stat().st_size}")
    print("Warning: this is a draft PDF. Visual inspection and final provenance review remain required.")


if __name__ == "__main__":
    main()
