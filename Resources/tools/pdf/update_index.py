"""Refresh reader indexes from the actual nine PDF files and build manifest."""
from pathlib import Path
from urllib.parse import quote
import json, re, sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'vendor'))
from pypdf import PdfReader

ROOT = HERE.parents[2]
DOC = ROOT / 'PDFs'
manifest = json.loads((HERE / 'qa/build-manifest.json').read_text(encoding='utf-8'))
topics = ['IC foundations and synthesis', 'Physical design and Verilog',
          'Simulation, synthesis and Boolean covers',
          'Multilevel optimization and formal methods',
          'Equivalence, libraries and STA', 'Constraints, mapping and timing optimization',
          'Power, scan design and ATPG', 'BIST, physical foundations and chip planning',
          'Placement, clocks, routing and signoff']

def table(prefix):
    rows = ['| Day | Lessons | Topic | PDF | Pages |',
            '|---|---|---|---|---:|']
    for day in range(1, 10):
        m = manifest[str(day)]
        pdf = DOC / m['filename']
        actual = len(PdfReader(pdf).pages)
        assert actual == m['pages'], f'Stale manifest: {pdf.name}'
        lessons = f'{(day-1)*6+1:02d}–{day*6:02d}'
        href = prefix + 'PDFs/' + quote(pdf.name)
        rows.append(f'| [Day {day:02d}]({prefix}Daily%20Notes/Day%20{day:02d}.md) | {lessons} | '
                    f'{topics[day-1]} | [Read PDF]({href}) | {actual} |')
    return '\n'.join(rows)

readme = ROOT / 'README.md'
text = readme.read_text(encoding='utf-8')
text, count = re.subn(r'\| Day \| Lessons \| Topic \| PDF \| Pages \|\n.*?(?=\n\n)',
                     lambda _: table(''), text, count=1, flags=re.S)
assert count == 1, 'Master index table not found'
text = re.sub(r'\n{3,}', '\n\n', text)
readme.write_text(text, encoding='utf-8')

(DOC / 'README.md').write_text(
    '# PDF collection\n\n[Master index](../README.md) · '
    '[Full forms](../Full%20Forms.pdf) · [RTL-to-GDS flow](../RTL%20to%20GDS%20Flow.pdf)\n\n' + table('../') +
    '\n\nUse the contents or bookmarks to open a section. Click any figure or '
    'the footer to return to contents. The pages use white A4 paper, dark text '
    'and embedded Cambria/Consolas fonts. Keep the PDFs in this repository '
    'layout so cross-day and supporting-file links resolve.\n\n'
    'Study-day numbers are six-lesson blocks. All nine blocks are complete '
    'through Week 12. Page counts above are verified against the exported files.\n\n'
    'The editable explanation sources are in `../Daily Notes`. After an edit, '
    'rebuild the affected day and inspect its rendered pages. See the '
    '[build and verification guide](../Resources/tools/pdf/README.md).\n\n'
    '[Week 7 and Week 8 question-only worksheet](Week%2007%20and%2008%20-%20Practice%20Questions.pdf) '
    'contains 20 original questions, 161 unmarked options and six source figures. '
    'The worksheet has ' + str(len(PdfReader(DOC / 'Week 07 and 08 - Practice Questions.pdf').pages)) + ' pages.\n',
    encoding='utf-8')
(ROOT / 'Daily Notes/README.md').write_text(
    '# Daily RTL-to-GDS notes\n\n[Master index](../README.md) · '
    '[PDF collection](../PDFs/README.md)\n\n' + table('../') +
    '\n\nOpen a day to use its lesson and topic indexes. Figures return to the '
    'day index. The PDFs retain the same explanations, source handwriting and '
    'lecture frames. Each study day contains six lessons; Day 09 ends at '
    'the Week 12 tutorial, course Lesson 54.\n\n'
    'For each lesson, read the source figure, follow the mechanism and worked '
    'example, then answer its recall checks using the stated assumptions. '
    'The expanded notes include counterexamples where a superficially plausible '
    'optimization or timing repair fails. Use the '
    '[handwritten index](../Resources/Handwritten%20Index.md) to locate a '
    'specific notebook page and its explanation.\n\n'
    'These Markdown files are the maintained content source. Keep lesson and '
    'source-page anchors stable; edit the explanation alongside its source, '
    'then follow the [PDF workflow](../Resources/tools/pdf/README.md).\n', encoding='utf-8')
print('Updated three reading indexes:', sum(m['pages'] for m in manifest.values()), 'daily pages.')
