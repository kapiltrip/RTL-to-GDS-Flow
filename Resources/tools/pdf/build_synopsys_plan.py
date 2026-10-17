"""Build the indexed Synopsys project plan from its maintained Markdown source.

Run with the Codex bundled Python runtime. ReportLab and pypdf are required.
Reader PDFs stay in PDFs; editable sources and QA stay in Resources.
"""
from pathlib import Path
from html import escape
import hashlib
import json
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Flowable, Frame, PageBreak, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents
from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / 'Resources/Synopsys RTL to GDS Project Plan.md'
OUTPUT = ROOT / 'PDFs/Synopsys RTL to GDS Project Plan.pdf'
OUTPUT.parent.mkdir(exist_ok=True)
QA = HERE / 'qa/synopsys-plan'
W, H = A4
MARGIN = 56.7
WIDTH = W - 2 * MARGIN
INK = colors.HexColor('#25231F')
GRAY = colors.HexColor('#555555')
RULE = colors.HexColor('#D6D6D6')

for name, filename in [
    ('PlanBook', 'cambria.ttc'), ('PlanBold', 'cambriab.ttf'),
    ('PlanItalic', 'cambriai.ttf'), ('PlanBI', 'cambriaz.ttf'),
    ('PlanCode', 'consola.ttf'),
]:
    pdfmetrics.registerFont(TTFont(name, str(Path('C:/Windows/Fonts') / filename)))
pdfmetrics.registerFontFamily(
    'PlanBook', normal='PlanBook', bold='PlanBold',
    italic='PlanItalic', boldItalic='PlanBI',
)

STYLES = {
    'title': ParagraphStyle('PlanTitle', fontName='PlanBold', fontSize=24,
                            leading=28.5, textColor=colors.black, spaceAfter=8),
    'body': ParagraphStyle('PlanBody', fontName='PlanBook', fontSize=11,
                           leading=14.4, textColor=INK, spaceAfter=6),
    'form': ParagraphStyle('PlanForm', fontName='PlanBook', fontSize=11,
                           leading=14.4, textColor=INK, spaceAfter=4),
    'h2': ParagraphStyle('PlanH2', fontName='PlanBold', fontSize=15,
                         leading=19, textColor=colors.black, spaceAfter=9,
                         keepWithNext=True),
    'h3': ParagraphStyle('PlanH3', fontName='PlanBold', fontSize=12,
                         leading=15.2, textColor=colors.black, spaceBefore=9,
                         spaceAfter=5, keepWithNext=True),
    'toc_title': ParagraphStyle('PlanContentsTitle', fontName='PlanBold',
                                fontSize=14, leading=18, textColor=colors.black,
                                spaceBefore=6, spaceAfter=8, keepWithNext=True),
    'toc': ParagraphStyle('PlanToc', fontName='PlanBook', fontSize=10.6,
                          leading=14.3, textColor=INK, spaceBefore=0,
                          leftIndent=0, firstLineIndent=0),
    'cell': ParagraphStyle('PlanCell', fontName='PlanBook', fontSize=9.9,
                           leading=12.8, textColor=INK, spaceAfter=0),
    'cellhead': ParagraphStyle('PlanCellHead', fontName='PlanBold', fontSize=9.9,
                               leading=12.8, textColor=colors.black),
    'list': ParagraphStyle('PlanList', fontName='PlanBook', fontSize=11,
                           leading=14.4, textColor=INK, spaceAfter=4.6,
                           leftIndent=13, firstLineIndent=-13),
    'refs': ParagraphStyle('PlanRefs', fontName='PlanBook', fontSize=10.1,
                           leading=13.4, textColor=INK, spaceAfter=5,
                           leftIndent=18, firstLineIndent=-18),
    'code': ParagraphStyle('PlanCodeBody', fontName='PlanCode', fontSize=9.1,
                           leading=12.6, textColor=INK, spaceAfter=0),
    'flowtitle': ParagraphStyle('PlanFlowTitle', fontName='PlanBold', fontSize=10.6,
                                leading=12.7, textColor=INK),
    'flowtool': ParagraphStyle('PlanFlowTool', fontName='PlanBook', fontSize=9.8,
                               leading=12.3, textColor=GRAY),
}


def slug(text):
    return re.sub(r'[^a-z0-9 ]', '', text.lower()).replace(' ', '-')


def inline(text):
    text = escape(text, quote=False)
    saved = []

    def save_link(match):
        label, target = match.groups()
        item = '<a href="%s" color="#333333"><u>%s</u></a>' % (
            escape(target, quote=True), label,
        )
        saved.append(item)
        return f'LINKTOKEN{len(saved)-1}END'

    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', save_link, text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'`([^`]+)`', r'<font name="PlanCode" size="9.5">\1</font>', text)

    def cite(match):
        nums = [n.strip() for n in match.group(1).split(',')]
        return '[' + ', '.join(
            f'<a href="#ref{n}" color="#333333"><u>{n}</u></a>' for n in nums
        ) + ']'

    text = re.sub(r'\[(\d+(?:,\s*\d+)*)\]', cite, text)
    for i, item in enumerate(saved):
        text = text.replace(f'LINKTOKEN{i}END', item)
    return text


class FlowDiagram(Flowable):
    def __init__(self, rows):
        super().__init__()
        self.rows = [line.split(' | ', 1) for line in rows]
        self.width = WIDTH
        self.row_height = 34
        self.gap = 10
        self.height = len(self.rows) * (self.row_height + self.gap) - self.gap + 3

    def draw(self):
        c = self.canv
        for i, (label, tool) in enumerate(self.rows):
            y = self.height - (i + 1) * (self.row_height + self.gap) + self.gap
            c.setStrokeColor(RULE)
            c.setLineWidth(.7)
            c.rect(0, y, WIDTH, self.row_height, stroke=1, fill=0)
            c.setFillColor(INK)
            c.setFont('PlanBold', 10.5)
            c.drawCentredString(17, y + 12, str(i + 1))
            p = Paragraph(escape(label), STYLES['flowtitle'])
            pw, ph = p.wrap(262, self.row_height - 5)
            p.drawOn(c, 33, y + (self.row_height - ph) / 2)
            q = Paragraph(escape(tool), STYLES['flowtool'])
            qw, qh = q.wrap(WIDTH - 310, self.row_height - 5)
            q.drawOn(c, 307, y + (self.row_height - qh) / 2)
            if i < len(self.rows) - 1:
                center = WIDTH / 2
                c.setStrokeColor(GRAY)
                c.line(center, y, center, y - self.gap + 3)
                c.line(center, y - self.gap + 3, center - 2, y - self.gap + 6)
                c.line(center, y - self.gap + 3, center + 2, y - self.gap + 6)


class PlanDoc(BaseDocTemplate):
    def __init__(self, path):
        super().__init__(str(path), pagesize=A4, leftMargin=MARGIN,
                         rightMargin=MARGIN, topMargin=MARGIN,
                         bottomMargin=MARGIN, title='Synopsys RTL to GDS Project Plan',
                         author='Kapil Tripathi', subject='Tools and laboratory readiness for an RTL to GDS project',
                         pageCompression=1)
        self.heading_pages = []
        self.addPageTemplates(PageTemplate(
            'PlanPage', [Frame(MARGIN, MARGIN, WIDTH, H - 2 * MARGIN,
                               leftPadding=0, rightPadding=0, topPadding=0,
                               bottomPadding=0)], onPage=self.decorate,
        ))

    def beforeDocument(self):
        self.heading_pages = []

    def decorate(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GRAY)
        if doc.page > 1:
            canvas.setFont('PlanBook', 8.1)
            canvas.drawString(MARGIN, H - 31, 'Synopsys RTL to GDS Project Plan')
        canvas.setFont('PlanBook', 8.5)
        canvas.drawString(MARGIN, 31, 'Contents')
        canvas.linkRect('', 'contents', (MARGIN, 28, MARGIN + 43, 40),
                        relative=0, thickness=0)
        canvas.drawRightString(W - MARGIN, 31, f'Page {doc.page}')
        canvas.restoreState()

    def afterFlowable(self, flowable):
        anchor = getattr(flowable, '_anchor', None)
        if anchor:
            y = self.frame._y + getattr(flowable, 'height', 0)
            self.canv.bookmarkHorizontalAbsolute(anchor, y)
        level = getattr(flowable, '_outline_level', None)
        if level is not None:
            title = flowable.getPlainText()
            self.canv.addOutlineEntry(title, anchor, level=level, closed=False)
            if getattr(flowable, '_in_toc', False):
                self.notify('TOCEntry', (0, title, self.page, anchor))
                self.heading_pages.append({'title': title, 'anchor': anchor, 'page': self.page})


def make_table(rows):
    count = len(rows[0])
    first = rows[0][0].lower()
    if count == 2:
        widths = [145, WIDTH - 145]
    elif count == 3 and first == 'required role':
        widths = [126, 144, WIDTH - 270]
    elif count == 3 and first == 'capability':
        widths = [110, 158, WIDTH - 268]
    elif count == 3 and first == 'period':
        widths = [71, 213, WIDTH - 284]
    elif count == 3:
        widths = [155, 158, WIDTH - 313]
    elif count == 4 and first.startswith('role'):
        widths = [138, 123, 151, WIDTH - 412]
    else:
        widths = [143, 97, 154, WIDTH - 394]
    data = []
    for rownum, row in enumerate(rows):
        style = STYLES['cellhead' if rownum == 0 else 'cell']
        data.append([Paragraph(inline(text), style) for text in row])
    table = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), .45, RULE),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F4F4F4')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    if first.startswith('role and') or first == 'resource' or first == 'missing or failing item':
        table.setStyle(TableStyle([
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
    if count == 4 and first.startswith('role'):
        table.setStyle(TableStyle([('ALIGN', (-1, 1), (-1, -1), 'CENTER')]))
    return table


def make_story(source):
    lines = source.splitlines()
    story = []
    i = 0
    references = False
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line == '<!-- pagebreak -->':
            story.append(PageBreak())
            i += 1
            continue
        if line.startswith('# '):
            story.append(Paragraph(inline(line[2:]), STYLES['title']))
            i += 1
            continue
        if line == '## Contents':
            p = Paragraph('Contents', STYLES['toc_title'])
            p._anchor = 'contents'
            p._outline_level = 0
            story.append(p)
            toc = TableOfContents()
            toc.levelStyles = [STYLES['toc']]
            toc.dotsMinLevel = 0
            story.append(toc)
            story.append(Spacer(1, 8))
            i += 1
            while i < len(lines) and (not lines[i].strip() or lines[i].startswith('- [')):
                i += 1
            continue
        if line.startswith('## '):
            title = line[3:]
            p = Paragraph(inline(title), STYLES['h2'])
            p._anchor = slug(title)
            p._outline_level = 0
            p._in_toc = True
            story.append(p)
            references = title.startswith('17 ')
            i += 1
            continue
        if line.startswith('### '):
            title = line[4:]
            p = Paragraph(inline(title), STYLES['h3'])
            p._anchor = slug(title)
            p._outline_level = 1
            story.append(p)
            i += 1
            continue
        if line.startswith('```'):
            language = line[3:]
            i += 1
            block = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                block.append(lines[i])
                i += 1
            if language == 'flow':
                story.append(FlowDiagram(block))
                story.append(Spacer(1, 6))
            else:
                for code_line in block:
                    text = escape(code_line).replace(' ', '&#160;') or '&#160;'
                    story.append(Paragraph(text, STYLES['code']))
                story.append(Spacer(1, 9))
            i += 1
            continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [part.strip() for part in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', cell) for cell in cells):
                    rows.append(cells)
                i += 1
            story.append(make_table(rows))
            story.append(Spacer(1, 8))
            continue
        numbered = re.match(r'^(\d+)\.\s+(.+)', line)
        if numbered:
            n, text = numbered.groups()
            p = Paragraph(f'{n}. ' + inline(text), STYLES['refs' if references else 'list'])
            if references:
                p._anchor = f'ref{n}'
            story.append(p)
            i += 1
            continue
        if line.startswith('- '):
            text = line[2:]
            if text.startswith('[ ] '):
                text = '[  ] ' + text[4:]
            else:
                text = '• ' + text
            story.append(Paragraph(inline(text), STYLES['list']))
            i += 1
            continue
        block = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(('#', '|', '-', '```', '<!--')):
            block.append(lines[i].strip())
            i += 1
        text = ' '.join(block)
        story.append(Paragraph(inline(text), STYLES['form' if '____' in text else 'body']))
    return story


def main():
    source = SOURCE.read_text(encoding='utf-8')
    OUTPUT.parent.mkdir(exist_ok=True, parents=True)
    QA.mkdir(exist_ok=True, parents=True)
    doc = PlanDoc(OUTPUT)
    doc.multiBuild(make_story(source))
    reader = PdfReader(OUTPUT)
    all_text = '\n'.join(page.extract_text() for page in reader.pages)
    missing = [item['title'] for item in doc.heading_pages if item['title'] not in all_text]
    if missing:
        raise RuntimeError(f'Missing headings in the exported PDF: {missing}')
    uri_count = 0
    internal_count = 0
    for page in reader.pages:
        for ref in page.get('/Annots', []):
            annotation = ref.get_object()
            action = annotation.get('/A', {})
            if action.get('/S') == '/URI':
                uri_count += 1
            elif annotation.get('/Dest') is not None or action.get('/S') == '/GoTo':
                internal_count += 1
    result = {
        'pdf': str(OUTPUT), 'pages': len(reader.pages),
        'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'pdf_sha256': hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        'headings': doc.heading_pages, 'external_links': uri_count,
        'internal_links': internal_count,
        'word_count': len(source.split()),
    }
    (QA / 'build.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    (QA / 'extracted.txt').write_text(all_text, encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
