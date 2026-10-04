"""Build the question-only Week 7/8 worksheet from its editable Markdown.

One-time import: --import-source Resources/tools/pdf/qa/quiz/source.json.
Normal rebuilds read the Markdown; the capture stays local for fidelity checks.
"""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
from urllib.parse import unquote, quote
import argparse
import hashlib
import json
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / 'vendor'))

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, KeepTogether, Flowable,
)
from reportlab.platypus.tableofcontents import TableOfContents
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
RESOURCES = HERE.parent.parent
SOURCE = RESOURCES / 'Week 07 and 08 - Practice Questions.md'
OUTPUT = RESOURCES.parent / 'PDFs/Week 07 and 08 - Practice Questions.pdf'
QA = HERE / 'qa' / 'quiz'
CAPTURE = QA / 'source.json'
LICENSE = 'https://creativecommons.org/licenses/by-nc-sa/4.0/'
W, H = A4
MARGIN = 56.7
WIDTH = W - 2 * MARGIN
HEIGHT = H - 2 * MARGIN - 9
DARK = colors.HexColor('#252525')
GRAY = colors.HexColor('#555555')


def normalize(text):
    return ' '.join(text.split())


class ImportHTML(HTMLParser):
    """Retain source text/emphasis and the exact original figure files."""
    def __init__(self, week, number):
        super().__init__(convert_charrefs=True)
        self.week, self.number = week, number
        self.parts, self.bold_stack = [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        bold = tag in ('b', 'strong') or (
            tag == 'span' and 'font-weight: bold' in attrs.get('style', ''))
        if tag == 'br':
            self.parts.append('\n')
        elif tag == 'img':
            name = attrs['src'].rsplit('/', 1)[-1]
            target = f'images/Quizzes/Week {self.week:02d}/{name}'
            alt = f'Week {self.week} question {self.number} original figure'
            self.parts.append(f'\n\n[![{alt}]({quote(target, safe="/")})](#index)\n\n')
        else:
            self.bold_stack.append((tag, bold))
            if bold:
                self.parts.append('**')

    def handle_endtag(self, tag):
        if self.bold_stack and self.bold_stack[-1][0] == tag:
            _, bold = self.bold_stack.pop()
            if bold:
                self.parts.append('**')

    def handle_data(self, data):
        self.parts.append(data)

    def result(self):
        text = ''.join(self.parts)
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r' *\n *', '\n', text)
        return re.sub(r'\n{3,}', '\n\n', text).strip()


def import_source(path):
    capture = json.loads(path.read_text(encoding='utf-8'))
    lines = ['# Week 7 and Week 8 — Practice questions', '',
             'VLSI Design Flow: RTL to GDS · NPTEL · Prof. Sneh Saurabh', '',
             '[PDF](../PDFs/Week%2007%20and%2008%20-%20Practice%20Questions.pdf) · '
             '[Master index](../README.md)', '', '<a id="index"></a>', '## Index', '']
    for week in capture['weeks']:
        n = week['week']
        lines += [f'[Week {n} : Assignment {n}](#week{n})', '',
                  ' · '.join(f'[{i}](#week{n}-q{i})' for i in range(1, 11)), '']
    for week in capture['weeks']:
        n = week['week']
        lines += [f'<a id="week{n}"></a>', f'## Week {n} : Assignment {n}', '',
                  f'[NPTEL source]({week["sourceUrl"]})', '']
        for question in week['questions']:
            i = int(question['number'].rstrip('.'))
            parser = ImportHTML(n, i)
            parser.feed(question['html'])
            lines += [f'<a id="week{n}-q{i}"></a>', f'### {i}.', '',
                      parser.result(), '']
            lines += ['- ' + option for option in question['options']]
            lines += ['', '[Index](#index)', '']
    lines += ['---', '',
              'Questions and figures: NPTEL, VLSI Design Flow: RTL to GDS, '
              'Prof. Sneh Saurabh, July–December 2026 (noc26_ee147). '
              'Question-only edition; original wording and figure files retained.', '',
              '[CC BY-NC-SA 4.0](' + LICENSE + ') · '
              '[NPTEL attribution](https://nptel.ac.in/) · '
              '[Licence reference](https://archive.nptel.ac.in/)', '']
    SOURCE.write_text('\n'.join(lines), encoding='utf-8')


IMAGE_PATTERN = re.compile(r'^\[!\[[^\]]+\]\(([^)]+)\)\]\(#index\)$')


def read_questions():
    text = SOURCE.read_text(encoding='utf-8')
    weeks = []
    for week_num in (7, 8):
        start = text.index(f'## Week {week_num} : Assignment {week_num}\n')
        section = text[start:]
        if week_num == 7:
            section = section.split('<a id="week8"></a>')[0]
        else:
            section = section.split('\n---\n')[0]
        source_url = re.search(r'\[NPTEL source\]\(([^)]+)\)', section).group(1)
        questions = []
        matches = list(re.finditer(r'^### (\d+)\.\s*$', section, re.M))
        for i, match in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(section)
            body = section[match.end():end]
            body = re.sub(r'<a id="[^"]+"></a>', '', body)
            body = body.replace('[Index](#index)', '').strip()
            lines = body.splitlines()
            options = [line[2:] for line in lines if line.startswith('- ')]
            stem = '\n'.join(line for line in lines if not line.startswith('- ')).strip()
            blocks = []
            for block in re.split(r'\n\s*\n', stem):
                figure = IMAGE_PATTERN.fullmatch(block.strip())
                blocks.append(('image', unquote(figure.group(1))) if figure
                              else ('text', block.strip()))
            questions.append(dict(number=int(match.group(1)), blocks=blocks, options=options))
        assert [q['number'] for q in questions] == list(range(1, 11))
        weeks.append(dict(week=week_num, sourceUrl=source_url, questions=questions))
    return weeks


def plain_stem(question):
    return normalize(' '.join(value.replace('**', '') for kind, value in
                              question['blocks'] if kind == 'text'))


def verify_capture(weeks):
    if not CAPTURE.exists():
        return
    original = json.loads(CAPTURE.read_text(encoding='utf-8'))
    for old_week, new_week in zip(original['weeks'], weeks):
        assert old_week['week'] == new_week['week']
        assert old_week['sourceUrl'] == new_week['sourceUrl']
        for old, new in zip(old_week['questions'], new_week['questions']):
            assert int(old['number'].rstrip('.')) == new['number']
            assert normalize(old['text']) == plain_stem(new), (old_week['week'], new['number'])
            assert old['options'] == new['options'], (old_week['week'], new['number'])
            names = [Path(value).name for kind, value in new['blocks'] if kind == 'image']
            assert names == [image['url'].rsplit('/', 1)[-1] for image in old['images']]


def markup(text):
    text = escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    return text.replace('\n', '<br/>')


class LinkedImage(Image):
    def draw(self):
        super().draw()
        self.canv.linkRect('', 'index', (0, 0, self.drawWidth, self.drawHeight),
                           relative=1, thickness=0)


class Option(Flowable):
    def __init__(self, text, style):
        super().__init__()
        self.paragraph = Paragraph(escape(text), style)

    def wrap(self, width, height):
        self.width = width
        _, ph = self.paragraph.wrap(width - 15, height)
        self.height = max(16, ph + 2)
        return self.width, self.height

    def draw(self):
        self.canv.setStrokeColor(DARK)
        self.canv.setLineWidth(0.7)
        self.canv.circle(4, self.height - 7, 3, fill=0, stroke=1)
        self.paragraph.drawOn(self.canv, 14, self.height - self.paragraph.height)


class Worksheet(BaseDocTemplate):
    def __init__(self, path):
        super().__init__(str(path), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                         topMargin=MARGIN, bottomMargin=MARGIN + 9,
                         title='Week 7 and Week 8 - Practice questions',
                         author='NPTEL / Prof. Sneh Saurabh',
                         subject='Question-only practice, noc26_ee147')
        self.question_pages = {}
        self.addPageTemplates(PageTemplate(id='questions',
            frames=[Frame(MARGIN, MARGIN + 9, WIDTH, HEIGHT,
                          leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)],
            onPage=self.footer))

    def beforeDocument(self):
        self.question_pages = {}

    def footer(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Book', 9)
        canvas.setFillColor(GRAY)
        canvas.drawString(MARGIN, 34, 'Week 7 and Week 8 · Practice questions')
        canvas.drawRightString(W - MARGIN, 34, f'Index  ·  {doc.page}')
        canvas.linkRect('', 'index', (W - MARGIN - 85, 29, W - MARGIN, 47), thickness=0)
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if hasattr(flowable, 'destination'):
            destination, title, level = flowable.destination
            self.canv.bookmarkPage(destination)
            self.canv.addOutlineEntry(title, destination, level=level, closed=False)
            if destination.startswith('week') and '-q' not in destination:
                self.notify('TOCEntry', (0, title, self.page, destination))
            if '-q' in destination:
                self.question_pages[destination] = self.page


def build(weeks):
    font_dir = Path('C:/Windows/Fonts')
    for name, filename in [('Book', 'cambria.ttc'), ('Book-Bold', 'cambriab.ttf')]:
        pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))
    pdfmetrics.registerFontFamily('Book', normal='Book', bold='Book-Bold',
                                 italic='Book', boldItalic='Book-Bold')
    body = ParagraphStyle('body', fontName='Book', fontSize=11, leading=14.5,
                          textColor=DARK, spaceAfter=6)
    small = ParagraphStyle('small', parent=body, fontSize=9.1, leading=12, textColor=GRAY)
    title = ParagraphStyle('title', parent=body, fontName='Book-Bold', fontSize=22, leading=26)
    heading = ParagraphStyle('heading', parent=body, fontName='Book-Bold',
                             fontSize=15, leading=19, spaceAfter=9, keepWithNext=1)
    qstyle = ParagraphStyle('question', parent=body, fontName='Book-Bold',
                            fontSize=11.5, spaceAfter=4, keepWithNext=1)
    option_style = ParagraphStyle('option', parent=body, fontSize=10.8, leading=14.2, spaceAfter=0)
    story = [Paragraph('Practice questions', title),
             Paragraph('Week 7 and Week 8 · VLSI Design Flow: RTL to GDS', body),
             Paragraph('NPTEL · Prof. Sneh Saurabh · July–December 2026', small), Spacer(1, 4)]
    index = Paragraph('Index', heading)
    index.destination = ('index', 'Index', 0)
    story.append(index)
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle('toc', parent=body, leading=16, spaceBefore=0, spaceAfter=2)]
    story.append(toc)
    for week in weeks:
        n = week['week']
        links = ' · '.join(f'<link href="#week{n}-q{i}" color="#252525">{i}</link>'
                           for i in range(1, 11))
        story.append(Paragraph(f'Week {n}: {links}', small))
    story.append(Spacer(1, 12))
    for week in weeks:
        n = week['week']
        if n == 8:
            story.append(PageBreak())
        week_heading = Paragraph(f'Week {n} : Assignment {n}', heading)
        week_heading.destination = (f'week{n}', f'Week {n} : Assignment {n}', 0)
        story.append(week_heading)
        for q in week['questions']:
            items = []
            number = Paragraph(f'{q["number"]}.', qstyle)
            number.destination = (f'week{n}-q{q["number"]}', f'Question {q["number"]}', 1)
            items.append(number)
            for kind, value in q['blocks']:
                if kind == 'text':
                    items.append(Paragraph(markup(value), body))
                else:
                    path = RESOURCES / value
                    with PILImage.open(path) as original:
                        iw, ih = original.size
                    scale = min(min(WIDTH - 12, 420) / iw, 350 / ih)
                    figure = LinkedImage(str(path), width=iw * scale, height=ih * scale)
                    figure.hAlign = 'LEFT'
                    items += [figure, Spacer(1, 8)]
            columns = 2 if max(len(opt) for opt in q['options']) <= 35 else 1
            options = [Option(opt, option_style) for opt in q['options']]
            rows = [options[i:i + columns] for i in range(0, len(options), columns)]
            if len(rows[-1]) < columns:
                rows[-1].append('')
            table = Table(rows, colWidths=[WIDTH / columns] * columns, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 7),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ]))
            items += [Spacer(1, 2), table, Spacer(1, 14)]
            # Every stem, figure and choice set stays on the same page.
            story.append(KeepTogether(items))
    story.append(Spacer(1, 8))
    for week in weeks:
        n = week['week']
        story.append(Paragraph(f'Source: <link href="{escape(week["sourceUrl"])}" '
                               f'color="#555555">NPTEL Week {n} : Assignment {n}</link>.', small))
    story.append(Paragraph('Questions and figures: NPTEL / Prof. Sneh Saurabh. '
        f'<link href="{LICENSE}" color="#555555">CC BY-NC-SA 4.0</link>. '
        'Question-only edition.', small))
    doc = Worksheet(OUTPUT)
    doc.multiBuild(story)
    reader = PdfReader(OUTPUT)
    assert len(doc.question_pages) == 20
    assert sum(len(page.images) for page in reader.pages) == 6
    assert not reader.get_fields()
    extracted = normalize(' '.join(page.extract_text() for page in reader.pages))
    for week in weeks:
        for q in week['questions']:
            assert plain_stem(q) in extracted, (week['week'], q['number'], 'stem')
            for option in q['options']:
                assert normalize(option) in extracted, (week['week'], q['number'], option)
    for forbidden in ('Accepted answer is', 'answer is correct', 'Your last recorded submission',
                      'Score:', 'Due date', '[checked]'):
        assert forbidden not in extracted
    QA.mkdir(parents=True, exist_ok=True)
    results = dict(pages=len(reader.pages), questions=20,
                   options=sum(len(q['options']) for w in weeks for q in w['questions']),
                   figures=6, question_pages=doc.question_pages,
                   sha256=hashlib.sha256(OUTPUT.read_bytes()).hexdigest())
    (QA / 'verification.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--import-source', type=Path)
    args = parser.parse_args()
    if args.import_source:
        import_source(args.import_source)
    weeks = read_questions()
    verify_capture(weeks)
    build(weeks)
