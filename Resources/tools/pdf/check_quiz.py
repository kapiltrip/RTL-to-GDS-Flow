"""Check the existing question-only worksheet without rebuilding or altering it."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'vendor'))
from PIL import Image
from pypdf import PdfReader
import pdfplumber

from build_quiz import OUTPUT, QA, RESOURCES, LICENSE, read_questions, verify_capture, plain_stem, normalize
from runtime import pdftoppm


def flatten_outline(items, level=0):
    for item in items:
        if isinstance(item, list):
            yield from flatten_outline(item, level + 1)
        else:
            yield level, item


def pixel_hash(image):
    rgb = image.convert('RGB')
    return rgb.size, hashlib.sha256(rgb.tobytes()).hexdigest()


def check(path, weeks):
    reader = PdfReader(path)
    assert not reader.get_fields(), 'Question-only worksheet unexpectedly has form fields.'
    outline = list(flatten_outline(reader.outline))
    expected = [(0, 'Index')]
    for week in weeks:
        expected.append((0, f'Week {week["week"]} : Assignment {week["week"]}'))
        expected.extend((1, f'Question {q["number"]}') for q in week['questions'])
    assert [(level, str(dest.title)) for level, dest in outline] == expected, 'Worksheet outline changed.'
    pages = [page.extract_text() or '' for page in reader.pages]
    assert all(text.strip() for text in pages), 'Blank worksheet page.'
    questions = []
    offset = 1
    for week in weeks:
        offset += 1  # Week heading precedes its ten question bookmarks.
        for q in week['questions']:
            page = reader.get_destination_page_number(outline[offset][1])
            assert 0 <= page < len(pages)
            questions.append((week['week'], q, page))
            offset += 1
    assert [p for _, _, p in questions] == sorted(p for _, _, p in questions)

    source_figures = {n: [] for n in range(len(pages))}
    for week, question, page in questions:
        number = question['number']
        header = re.search(rf'(?m)^{number}\.\s*$', pages[page])
        assert header, (week, number, 'Question number missing on bookmarked page')
        start = header.end()
        following = re.search(r'(?m)^\d+\.\s*$', pages[page][start:])
        end = start + following.start() if following else len(pages[page])
        actual = pages[page][start:end].split('Source:', 1)[0]
        required = normalize(' '.join([plain_stem(question), *question['options']]))
        assert normalize(actual) == required, (week, number, 'Stem/options differ or are reordered')
        for kind, value in question['blocks']:
            if kind == 'image':
                with Image.open(RESOURCES / value) as image:
                    source_figures[page].append(pixel_hash(image))
    for page, originals in source_figures.items():
        embedded = [pixel_hash(image.image) for image in reader.pages[page].images]
        assert Counter(embedded) == Counter(originals), (page + 1, 'Embedded figure pixels differ')

    text = normalize(' '.join(pages))
    for forbidden in ('Accepted answer is', 'answer is correct', 'Your last recorded submission',
                      'Score:', 'Due date', '[checked]'):
        assert forbidden not in text, forbidden
    page_ids = {p.indirect_reference.idnum for p in reader.pages}
    index_id = reader.pages[0].indirect_reference.idnum
    internal = footer = 0
    external = []
    index_targets = []
    for n, page in enumerate(reader.pages):
        footer_found = False
        for reference in page.get('/Annots', []):
            annotation = reference.get_object()
            destination = annotation.get('/Dest')
            rect = [float(x) for x in annotation.get('/Rect', [])]
            if destination is not None:
                assert isinstance(destination, list) and destination[0].idnum in page_ids
                internal += 1
                if rect[1] < 48 and rect[3] < 48:
                    assert destination[0].idnum == index_id
                    footer_found = True
                if n == 0 and 600 < rect[1] < 640:
                    index_targets.append(destination[0].idnum)
            action = annotation.get('/A')
            if action:
                assert action.get('/S') == '/URI'
                external.append(str(action['/URI']))
        assert footer_found, (n + 1, 'Footer return to index missing')
        footer += 1
    assert index_targets == [reader.pages[p].indirect_reference.idnum for _, _, p in questions]
    assert Counter(external) == Counter([w['sourceUrl'] for w in weeks] + [LICENSE])

    circles = 0
    with pdfplumber.open(path) as pdf:
        for n, page in enumerate(pdf.pages, 1):
            assert abs(page.width - 595.276) < .1 and abs(page.height - 841.89) < .1
            for char in page.chars:
                assert 55 <= char['x0'] <= char['x1'] <= page.width - 55, (n, 'Horizontal text overflow')
                assert 20 <= char['top'] <= char['bottom'] <= page.height - 22, (n, 'Vertical text overflow')
            for curve in page.curves:
                if abs(curve['width'] - 6) < .1 and abs(curve['height'] - 6) < .1:
                    assert not curve['fill'] and curve['stroke'], (n, 'Marked option')
                    circles += 1
    options = sum(len(q['options']) for w in weeks for q in w['questions'])
    assert len(questions) == 20 and options == circles == 161
    figures = sum(len(images) for images in source_figures.values())
    assert figures == 6
    return dict(pages=len(pages), questions=len(questions), options=options, unmarked_circles=circles,
                figures=figures, bookmarks=len(outline), question_and_option_order=True,
                embedded_figure_pixels=True, internal_links=internal, footer_links=footer,
                external_links=len(external), layout_bounds=True,
                source_sha256=hashlib.sha256((RESOURCES / 'Week 07 and 08 - Practice Questions.md').read_bytes()).hexdigest(),
                sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def main():
    weeks = read_questions()
    verify_capture(weeks)  # Compare with the original capture when locally available.
    before = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    results = check(OUTPUT, weeks)
    QA.mkdir(parents=True, exist_ok=True)
    render = QA / f'pages-{results["pages"]}'
    render.mkdir(exist_ok=True)
    subprocess.run([str(pdftoppm()), '-r', '115', '-png', str(OUTPUT), str(render / 'page')],
                   check=True, capture_output=True)
    assert len(list(render.glob('page-*.png'))) == results['pages']
    assert hashlib.sha256(OUTPUT.read_bytes()).hexdigest() == before, 'Checker changed the worksheet.'
    (QA / 'checks.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    print(f'PASS: {results["pages"]} worksheet pages; 20 questions in order, '
          '161 unmarked options, six exact figures, bookmarks/index/footer links and bounds. PDF unchanged.')


if __name__ == '__main__':
    main()
