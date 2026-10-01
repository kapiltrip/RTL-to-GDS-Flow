"""Refresh reader indexes from the actual six PDF files and build manifest."""
from pathlib import Path
from urllib.parse import quote
import json, re
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DOC = HERE.parent
manifest = json.loads((HERE / 'qa/build-manifest.json').read_text(encoding='utf-8'))
topics = ['IC foundations and synthesis', 'Physical design and Verilog',
          'Simulation, synthesis and Boolean covers',
          'Multilevel optimization and formal methods',
          'Equivalence, libraries and STA', 'OpenSTA and Constraints I']

def table(prefix):
    rows = ['| Day | Lessons | Topic | PDF | Pages |',
            '|---|---|---|---|---:|']
    for day in range(1, 7):
        m = manifest[str(day)]
        pdf = DOC / m['filename']
        actual = len(PdfReader(pdf).pages)
        assert actual == m['pages'], f'Stale manifest: {pdf.name}'
        lessons = f'{(day-1)*6+1:02d}–{min(day*6,32):02d}'
        href = prefix + 'Resources/documents/' + quote(pdf.name)
        rows.append(f'| [Day {day:02d}]({prefix}Day%20{day:02d}.md) | {lessons} | '
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
    '# Daily PDF collection\n\n[Master index](../../README.md)\n\n' + table('../../') +
    '\n\nUse the contents or bookmarks to open a section. Click any figure or '
    'the footer to return to contents. The pages use white A4 paper, dark text '
    'and embedded Cambria/Consolas fonts. Keep the PDFs in this repository '
    'layout so cross-day and supporting-file links resolve.\n\n'
    'Lecture frames are paired with handwritten comparison crops. Full source '
    'pages, corrections, worked examples and complete code follow. Study-day '
    'numbers are six-lesson blocks; the current partial block ends at '
    'Constraints I. Page counts above are verified against the exported files.\n',
    encoding='utf-8')
print('Updated both reading indexes:', sum(m['pages'] for m in manifest.values()), 'pages.')
