"""Build the additional single-page process and tool sheet without editing the full plan."""
from pathlib import Path
from html import escape
import hashlib
import json

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from pypdf import PdfReader

from build_synopsys_plan import ROOT, W, H, WIDTH, MARGIN, RULE, INK

SOURCE = ROOT / 'Resources/Synopsys RTL to GDS Tool Map.md'
OUTPUT = ROOT / 'Synopsys RTL to GDS Tool Map.pdf'
QA = ROOT / 'Resources/tools/pdf/qa/synopsys-tool-map'
MAIN_PDF = ROOT / 'Synopsys RTL to GDS Project Plan.pdf'
MAIN_SOURCE = ROOT / 'Resources/Synopsys RTL to GDS Project Plan.md'


def main():
    preserved = {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in (MAIN_PDF, MAIN_SOURCE)}
    source = SOURCE.read_text(encoding='utf-8')
    rows = []
    for line in source.splitlines():
        if line.startswith('|') and not line.startswith('|---'):
            rows.append([x.strip() for x in line.strip('|').split('|')])

    title = ParagraphStyle('MapTitle', fontName='PlanBold', fontSize=22,
                           leading=26, textColor=colors.black, spaceAfter=14)
    cell = ParagraphStyle('MapCell', fontName='PlanBook', fontSize=10.8,
                          leading=13.8, textColor=INK)
    number = ParagraphStyle('MapNumber', parent=cell, alignment=TA_CENTER)
    header = ParagraphStyle('MapHeader', parent=cell, fontName='PlanBold')
    small = ParagraphStyle('MapSmall', fontName='PlanBook', fontSize=9.7,
                           leading=12.8, textColor=INK, spaceAfter=5)
    data = []
    for r, values in enumerate(rows):
        data.append([Paragraph(escape(text), header if r == 0 else number if c == 0 else cell)
                     for c, text in enumerate(values)])
    table = Table(data, colWidths=[35, 217, WIDTH - 252], repeatRows=1)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), .45, RULE),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F4F4F4')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story = [Paragraph('Synopsys RTL to GDS Tool Map', title), table, Spacer(1, 10)]
    story.append(Paragraph('<b>Choose one implementation route:</b> Design Compiler + IC Compiler II, '
                           'or Fusion Compiler.', small))
    story.append(Paragraph('<b>* Scope dependent:</b> Include the checks required by your design and teacher. '
                           'Lint is recommended; clock and reset crossing checks depend on the design. '
                           'The full plan covers licenses, libraries and signoff requirements.', small))
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=(W, H), leftMargin=MARGIN,
                            rightMargin=MARGIN, topMargin=MARGIN, bottomMargin=MARGIN,
                            title='Synopsys RTL to GDS Tool Map', author='Kapil Tripathi',
                            subject='Single-page process and Synopsys tool names')
    doc.build(story)
    reader = PdfReader(OUTPUT)
    assert len(reader.pages) == 1, 'The additional tool sheet must fit on one page.'
    assert len(rows) == 19
    text = reader.pages[0].extract_text()
    for values in rows[1:]:
        assert values[2] in text.replace('\n', ' '), values[2]
    for path, expected_hash in preserved.items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected_hash
    QA.mkdir(parents=True, exist_ok=True)
    meta = {'pages': 1, 'process_stages': 18, 'source': str(SOURCE), 'pdf': str(OUTPUT),
            'pdf_sha256': hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
            'preserved_full_plan': preserved}
    (QA / 'build.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
    print(json.dumps(meta, indent=2))


if __name__ == '__main__':
    main()
