from pathlib import Path
import html
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, LongTable, TableStyle, PageBreak
)

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "output" / "TUM_BAGLANTI_KONTROLU_20260911.md"
DEST = ROOT / "output" / "pdf" / "TUM_BAGLANTI_KONTROLU_20260911.pdf"
DEST.parent.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("ArialBold", "C:/Windows/Fonts/arialbd.ttf"))

base = getSampleStyleSheet()
styles = {
    "title": ParagraphStyle("title", parent=base["Title"], fontName="ArialBold", fontSize=21,
                            leading=26, textColor=colors.HexColor("#173f55"), spaceAfter=14),
    "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName="ArialBold", fontSize=13.5,
                         leading=17, textColor=colors.HexColor("#173f55"), spaceBefore=8, spaceAfter=6),
    "h3": ParagraphStyle("h3", parent=base["Heading3"], fontName="ArialBold", fontSize=11.5,
                         leading=15, textColor=colors.HexColor("#285d73"), spaceBefore=8, spaceAfter=5),
    "body": ParagraphStyle("body", parent=base["BodyText"], fontName="Arial", fontSize=8.9,
                           leading=12.5, spaceAfter=5),
    "bullet": ParagraphStyle("bullet", parent=base["BodyText"], fontName="Arial", fontSize=8.8,
                             leading=12.3, leftIndent=14, firstLineIndent=-10, spaceAfter=3),
    "cell": ParagraphStyle("cell", parent=base["BodyText"], fontName="Arial", fontSize=7.6,
                           leading=9.8),
    "cellhead": ParagraphStyle("cellhead", parent=base["BodyText"], fontName="ArialBold", fontSize=7.6,
                               leading=9.8),
}

def rich(text):
    text = html.escape(text.strip())
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`(.+?)`", r"<font name='Courier'>\1</font>", text)
    return text

lines = SOURCE.read_text(encoding="utf-8").splitlines()
story = []
i = 0
first_title = True
while i < len(lines):
    line = lines[i].rstrip()
    if not line:
        i += 1
        continue
    if line.startswith("# "):
        if not first_title:
            story.append(PageBreak())
        story.append(Paragraph(rich(line[2:]), styles["title"]))
        first_title = False
        i += 1
        continue
    if line.startswith("## "):
        story.append(Paragraph(rich(line[3:]), styles["h2"]))
        i += 1
        continue
    if line.startswith("### "):
        story.append(Paragraph(rich(line[4:]), styles["h3"]))
        i += 1
        continue
    if line.startswith("|"):
        table_lines = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            table_lines.append(lines[i].strip())
            i += 1
        rows = [[c.strip() for c in row.strip("|").split("|")] for row in table_lines]
        if len(rows) > 1 and all(re.fullmatch(r":?-{3,}:?", c) for c in rows[1]):
            rows.pop(1)
        n = max(len(r) for r in rows)
        usable = A4[0] - 34*mm
        if n == 2:
            widths = [usable*0.30, usable*0.70]
        elif n == 3:
            widths = [usable*0.22, usable*0.43, usable*0.35]
        elif n == 4:
            widths = [usable*0.15, usable*0.38, usable*0.33, usable*0.14]
        else:
            widths = [usable/n]*n
        data = []
        for ri, row in enumerate(rows):
            style = styles["cellhead"] if ri == 0 else styles["cell"]
            data.append([Paragraph(rich(c), style) for c in row])
        table = LongTable(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#dcecf2")),
            ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#aab9c0")),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (0,0), (-1,-1), 5),
            ("RIGHTPADDING", (0,0), (-1,-1), 5),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ]))
        story.extend([table, Spacer(1, 3*mm)])
        continue
    if re.match(r"^\d+\. ", line):
        story.append(Paragraph(rich(line), styles["bullet"]))
        i += 1
        continue
    if line.startswith("- "):
        story.append(Paragraph("• " + rich(line[2:]), styles["bullet"]))
        i += 1
        continue
    para = [line]
    i += 1
    while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||- |\d+\. )", lines[i].strip()):
        para.append(lines[i].strip())
        i += 1
    story.append(Paragraph(rich(" ".join(para)), styles["body"]))

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#c5d0d5"))
    canvas.line(17*mm, 13*mm, A4[0]-17*mm, 13*mm)
    canvas.setFont("Arial", 7.5)
    canvas.setFillColor(colors.HexColor("#566b75"))
    canvas.drawString(17*mm, 8.5*mm, "Tüm şematik bağlantı kontrolü • 11.09.2026")
    canvas.drawRightString(A4[0]-17*mm, 8.5*mm, f"Sayfa {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(str(DEST), pagesize=A4, leftMargin=17*mm, rightMargin=17*mm,
                        topMargin=15*mm, bottomMargin=16*mm,
                        title="Tüm şematik bağlantı kontrolü ve mühendislik açıklaması",
                        author="Codex")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(DEST)
