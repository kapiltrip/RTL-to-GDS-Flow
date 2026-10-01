"""Build the two root-level, theory-focused PDF references from maintained Markdown."""
from pathlib import Path
from urllib.parse import unquote, quote, urlsplit
from html import escape
import hashlib, json, os, re, sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RES = ROOT / 'Resources'
QA = HERE / 'qa/references'
QA.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(HERE / 'vendor'))
from markdown_it import MarkdownIt
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
    Spacer, PageBreak, Table, TableStyle, Flowable, CondPageBreak)
from pypdf import PdfReader, PdfWriter

W, H = A4
MARGIN = 56.7
WIDTH = W - 2 * MARGIN
INK = colors.HexColor('#242424')
GRAY = colors.HexColor('#585858')
RULE = colors.HexColor('#B0B0B0')
for name, file in [('RefBook', 'cambria.ttc'), ('RefBold', 'cambriab.ttf'),
                   ('RefItalic', 'cambriai.ttf'), ('RefBI', 'cambriaz.ttf')]:
    if name not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(name, 'C:/Windows/Fonts/' + file))
pdfmetrics.registerFontFamily('RefBook', normal='RefBook', bold='RefBold',
    italic='RefItalic', boldItalic='RefBI')

STYLE = {
    'title': ParagraphStyle('RefTitle', fontName='RefBold', fontSize=20, leading=23,
                           textColor=INK, spaceAfter=6),
    'subtitle': ParagraphStyle('RefSubtitle', fontName='RefBook', fontSize=10.7,
                              leading=14, textColor=GRAY, spaceAfter=7),
    'body': ParagraphStyle('RefBody', fontName='RefBook', fontSize=10.8, leading=14.1,
                          textColor=INK, spaceAfter=5.2),
    'h2': ParagraphStyle('RefHeading', fontName='RefBold', fontSize=12.2, leading=15,
                        textColor=INK, spaceBefore=8.3, spaceAfter=3.5, keepWithNext=True),
    'small': ParagraphStyle('RefSmall', fontName='RefBook', fontSize=9.7, leading=12.5,
                           textColor=GRAY, spaceAfter=5),
    'cell': ParagraphStyle('RefCell', fontName='RefBook', fontSize=10.2, leading=12.7,
                          textColor=INK),
    'cellhead': ParagraphStyle('RefCellHead', fontName='RefBold', fontSize=10.2,
                              leading=12.7, textColor=INK),
    'term': ParagraphStyle('RefTerm', fontName='RefBold', fontSize=11, leading=14,
                          textColor=INK),
}
MD = MarkdownIt('commonmark').enable('table')
manifest = json.loads((HERE / 'qa/build-manifest.json').read_text(encoding='utf-8'))

def clean(value):
    return value.replace('\u2011', '-').replace('\u2013', '-').replace('\u2014', '-')

def slug(value):
    return re.sub(r'\s', '-', re.sub(r'[^\w\s-]', '', value.lower()))

def target(url):
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return url
    source = (RES / unquote(parsed.path)).resolve()
    match = re.fullmatch(r'Day (\d\d)\.md', source.name)
    if match and source.parent == ROOT / 'Daily Notes':
        day = int(match[1])
        destination = unquote(parsed.fragment) or 'contents'
        assert destination == 'contents' or destination in manifest[str(day)]['destinations'], url
        return 'PDFs/' + quote(manifest[str(day)]['filename']) + '#nameddest=' + quote(destination)
    relative = Path(os.path.relpath(source, ROOT)).as_posix()
    return quote(relative, safe='/') + (('#' + parsed.fragment) if parsed.fragment else '')

def inline(tokens):
    output = []
    for t in tokens or []:
        if t.type in ('text', 'code_inline'):
            output.append(escape(clean(t.content)))
        elif t.type == 'softbreak': output.append(' ')
        elif t.type == 'hardbreak': output.append('<br/>')
        elif t.type == 'strong_open': output.append('<b>')
        elif t.type == 'strong_close': output.append('</b>')
        elif t.type == 'em_open': output.append('<i>')
        elif t.type == 'em_close': output.append('</i>')
        elif t.type == 'link_open':
            output.append('<a href="' + escape(target(t.attrGet('href')), quote=True) + '" color="#242424"><u>')
        elif t.type == 'link_close': output.append('</u></a>')
        else: raise ValueError(('Unsupported inline element', t.type))
    return ''.join(output)

def paragraph(value, style='body'):
    return Paragraph(value, STYLE[style])

class Sequence(Flowable):
    """Native vector overview; click anywhere to return to the document index."""
    def __init__(self):
        super().__init__()
        self.width = WIDTH
        self.height = 35
    def draw(self):
        labels = ['RTL', 'Mapped netlist', 'Placed cells', 'Routed layout', 'GDSII']
        gap = 12
        bw = (WIDTH - gap * 4) / 5
        c = self.canv
        c.setStrokeColor(RULE); c.setFillColor(INK); c.setLineWidth(.5)
        c.setFont('RefBook', 9.3)
        for i, label in enumerate(labels):
            x = i * (bw + gap)
            c.rect(x, 8, bw, 23, stroke=1, fill=0)
            c.drawCentredString(x + bw / 2, 16, label)
            if i < 4:
                ax = x + bw + 2
                c.line(ax, 19.5, ax + 8, 19.5)
                c.line(ax + 8, 19.5, ax + 5, 22)
                c.line(ax + 8, 19.5, ax + 5, 17)
        c.linkRect('', 'contents', (0, 0, WIDTH, self.height), relative=1, thickness=0)

class ReferenceDoc(BaseDocTemplate):
    def __init__(self, path, title):
        super().__init__(str(path), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
            topMargin=MARGIN, bottomMargin=MARGIN + 3, title=title,
            author='Kapil Tripathi', subject='NPTEL RTL-to-GDS study reference',
            allowSplitting=True)
        self.title = title
        self.destinations = {}; self.headings = []
        frame = Frame(MARGIN, MARGIN + 3, WIDTH, H - MARGIN * 2 - 3,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(PageTemplate(id='reference', frames=frame, onPage=self.page))

    def page(self, c, doc):
        c.saveState()
        if doc.page > 1:
            c.setFillColor(GRAY); c.setFont('RefBook', 9)
            c.drawString(MARGIN, H - 34, self.title)
            c.setStrokeColor(RULE); c.setLineWidth(.4)
            c.line(MARGIN, H - 42, W - MARGIN, H - 42)
        c.setFont('RefBook', 9); c.setFillColor(GRAY)
        c.drawString(MARGIN, 30, 'RTL to GDS | Back to index')
        c.drawRightString(W - MARGIN, 30, str(doc.page))
        c.linkRect('', 'contents', (MARGIN, 24, W - MARGIN, 42), thickness=0)
        c.restoreState()

    def afterFlowable(self, f):
        if hasattr(f, '_destination'):
            key, title, level = f._destination
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(clean(title), key, level, False)
            self.destinations[key] = self.page
            self.headings.append({'key': key, 'title': clean(title), 'page': self.page, 'level': level})

def heading(title, key, level=0, style='h2'):
    p = paragraph(escape(clean(title)), style)
    p._destination = (key, title, level)
    return p

def finish(path, doc, story, source):
    doc.build(story)
    reader = PdfReader(path)
    writer = PdfWriter(); writer.clone_document_from_reader(reader)
    for key, page in doc.destinations.items():
        writer.add_named_destination(key, page - 1)
    writer.page_mode = '/UseOutlines'
    temporary = path.with_suffix('.named.pdf')
    with temporary.open('wb') as out: writer.write(out)
    os.replace(temporary, path)
    return {'filename': path.name, 'pages': len(reader.pages),
            'destinations': doc.destinations, 'headings': doc.headings,
            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest()}

def build_flow():
    source = RES / 'Flow Map.md'
    tokens = MD.parse(source.read_text(encoding='utf-8'))
    story = []; i = 0; page = 1; title_seen = False; table_no = 0
    while i < len(tokens):
        t = tokens[i]
        if t.type == 'heading_open':
            text = tokens[i + 1].content
            if t.tag == 'h1':
                key = 'contents' if not title_seen else 'iteration-and-course-approach'
                story.append(heading(text, key, 0, 'title')); title_seen = True
                if page == 1:
                    story.append(paragraph('<a href="#contents" color="#242424"><u>Implementation sequence</u></a> '
                        ' · <a href="#iteration-and-course-approach" color="#242424"><u>Iteration and course approach</u></a>', 'small'))
            else: story.append(heading(text, slug(text), 1))
            i += 3
        elif t.type == 'paragraph_open':
            style = 'subtitle' if page == 1 and i < 7 else 'body'
            if tokens[i + 1].content.startswith('[NPTEL official'): style = 'small'
            story.append(paragraph(inline(tokens[i + 1].children), style))
            if style == 'subtitle': story.append(Sequence())
            i += 3
        elif t.type == 'html_block' and 'pagebreak' in t.content:
            story.append(PageBreak()); page += 1; i += 1
        elif t.type == 'table_open':
            rows = []; row = []; header = True
            i += 1
            while tokens[i].type != 'table_close':
                cell = tokens[i]
                if cell.type == 'thead_close': header = False
                if cell.type == 'tr_open': row = []
                if cell.type == 'inline': row.append(paragraph(inline(cell.children), 'cellhead' if header else 'cell'))
                if cell.type == 'tr_close': rows.append(row)
                i += 1
            sizes = [111, 186, WIDTH - 297] if table_no == 0 else [46, WIDTH - 46]
            table = Table(rows, colWidths=sizes, repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LINEABOVE', (0, 0), (-1, 0), .6, INK),
                ('LINEBELOW', (0, 0), (-1, 0), .5, RULE),
                ('LINEBELOW', (0, 1), (-1, -1), .25, RULE),
            ]))
            story.extend([table, Spacer(1, 5)]); table_no += 1; i += 1
        else: raise ValueError(('Unsupported block', t.type))
    path = ROOT / 'RTL to GDS Flow.pdf'
    doc = ReferenceDoc(path, 'RTL to GDS Flow')
    result = finish(path, doc, story, source)
    assert result['pages'] == 2, ('The flow guide must remain two pages', result['pages'])
    return result

def build_glossary():
    source = RES / 'Glossary.md'
    rows = []
    for line in source.read_text(encoding='utf-8').splitlines():
        if line.startswith('| ') and not line.startswith('| Term |'):
            values = [s.strip() for s in line.strip('|').split('|')]
            assert len(values) == 4, line
            rows.append(values)
    groups = [('A-C', 'ABC'), ('D-F', 'DEF'), ('G-L', 'GHIJKL'),
              ('M-P', 'MNOP'), ('Q-S', 'QRS'), ('T-Z', 'TUVWXYZ')]
    story = [heading('Full forms and meanings', 'contents', 0, 'title'),
        paragraph('Alphabetical reference to course terminology. Meanings state the relevant context; '
                  'lesson links open the detailed daily PDFs.', 'subtitle'),
        paragraph(' · '.join('<a href="#group-' + name.lower() + '" color="#242424"><u>' + name + '</u></a>'
                            for name, _ in groups), 'body'),
        paragraph('SDC has distinct logic and timing meanings. CDC here is controllability don\'t-care. '
                  'Liberty is a format name; tCQ, tSU and tH are symbols. Operation names and '
                  'conventional abbreviations are identified by context.', 'small')]
    term_records = []
    for group, letters in groups:
        story.append(CondPageBreak(100))
        story.append(heading(group, 'group-' + group.lower(), 1))
        for term, full, meaning, deep in rows:
            if term[0].upper() not in letters: continue
            story.append(CondPageBreak(45))
            reference = MD.parseInline(deep)[0].children
            left = paragraph(escape(clean(term)), 'term')
            right = paragraph('<b>' + escape(clean(full)) + '</b><br/>' + escape(clean(meaning)), 'cell')
            ref = paragraph(inline(reference), 'small')
            table = Table([[left, right, ref]], colWidths=[76, WIDTH - 141, 65], hAlign='LEFT')
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LINEABOVE', (0, 0), (-1, 0), .25, RULE),
            ]))
            key = 'term-' + slug(term)
            table._destination = (key, term, 2)
            story.append(table)
            term_records.append({'term': term, 'expansion': full, 'meaning': meaning, 'key': key,
                                 'reference': target(re.search(r'\]\(([^)]+)\)', deep)[1])})
    assert rows and len(term_records) == len(rows)
    assert len({t['term'] for t in term_records}) == len(rows)
    story.append(CondPageBreak(110))
    story.append(heading('Reference trail', 'reference-trail', 1))
    story.append(paragraph('Meanings are concise study summaries. Each lesson link retains the lecture '
        'frames, timestamps and supporting sources. ATPG/BIST have later treatment in Weeks 9-10; '
        'FEOL/BEOL have further treatment in Week 10.', 'small'))
    story.append(paragraph('<a href="https://onlinecourses.nptel.ac.in/e-learning/preview/noc26_ee147" '
        'color="#242424"><u>NPTEL official course outline</u></a> · '
        '<a href="https://www.youtube.com/playlist?list=PLyqSpQzTE6M8iOrfy70ELk9W72JG5a98V" '
        'color="#242424"><u>Course lectures</u></a> · '
        '<a href="Resources/Sources.md" color="#242424"><u>Source register</u></a> · '
        '<a href="RTL%20to%20GDS%20Flow.pdf" color="#242424"><u>Flow guide</u></a>', 'small'))
    path = ROOT / 'Full Forms.pdf'
    doc = ReferenceDoc(path, 'Full forms and meanings')
    result = finish(path, doc, story, source)
    result['terms'] = term_records
    return result

def main():
    results = {'flow': build_flow(), 'glossary': build_glossary()}
    (QA / 'manifest.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    for name, record in results.items():
        print(f'{record["filename"]}: {record["pages"]} pages, {len(record["destinations"])} destinations', flush=True)

if __name__ == '__main__': main()
