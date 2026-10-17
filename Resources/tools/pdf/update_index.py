"""Refresh reading indexes and downloads from every delivered PDF.

Read the actual collection, including on a fresh clone without QA manifests.
Preserve curated descriptions outside the daily index tables.
"""
from pathlib import Path
from urllib.parse import quote
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'vendor'))
from pypdf import PdfReader

ROOT = HERE.parents[2]
DOC = ROOT / 'PDFs'
REPOSITORY = 'https://github.com/kapiltrip/RTL-to-GDS-Flow'
ARCHIVE = REPOSITORY + '/archive/refs/heads/main.zip'
TOPICS = [
    'IC foundations and synthesis', 'Physical design and Verilog',
    'Simulation, synthesis and Boolean covers',
    'Multilevel optimization and formal methods',
    'Equivalence, libraries and STA', 'Constraints, mapping and timing optimization',
    'Power, scan design and ATPG', 'BIST, physical foundations and chip planning',
    'Placement, clocks, routing and signoff',
]
REFERENCES = [
    ('Full Forms.pdf', 'Full forms and meanings', 'Terminology with meanings and lesson links'),
    ('RTL to GDS Flow.pdf', 'RTL to GDS flow', 'Implementation stages and course sequence'),
    ('Synopsys RTL to GDS Project Plan.pdf', 'Synopsys project plan',
     'Tool requirements, lab inventories, readiness trial and implementation plan'),
    ('Synopsys RTL to GDS Tool Map.pdf', 'Synopsys tool map', 'One-page process and tool table'),
    ('Week 07 and 08 - Practice Questions.pdf', 'Week 7 and 8 practice questions',
     '20 original questions, 161 unmarked options and six source figures'),
]


def download(name):
    return REPOSITORY + '/raw/refs/heads/main/PDFs/' + quote(name)


def main():
    days = []
    for day in range(1, 10):
        matches = list(DOC.glob(f'Day {day:02d} - *.pdf'))
        assert len(matches) == 1, (day, 'Expected one reading PDF', matches)
        path = matches[0]
        days.append((path.name, len(PdfReader(path).pages)))
    pages = {name: len(PdfReader(DOC / name).pages) for name, _, _ in REFERENCES}
    expected = {name for name, _ in days} | set(pages)
    assert {p.name for p in DOC.glob('*.pdf')} == expected, 'Unindexed or missing PDFs'
    total = sum(count for _, count in days) + sum(pages.values())

    def daily_table(index):
        from os.path import relpath
        def href(path):
            return quote(Path(relpath(path, index.parent)).as_posix(), safe='/')
        rows = ['| Day | Lessons | Topic | PDF | Download | Pages |',
                '|---|---|---|---|---|---:|']
        for day, (name, count) in enumerate(days, 1):
            lessons = f'{(day - 1) * 6 + 1:02d}–{day * 6:02d}'
            rows.append(
                f'| [Day {day:02d}]({href(ROOT / "Resources/Daily Notes" / f"Day {day:02d}.md")}) | '
                f'{lessons} | {TOPICS[day - 1]} | '
                f'[Read PDF]({href(DOC / name)}) | '
                f'[Download PDF]({download(name)}) | {count} |')
        return '\n'.join(rows)

    def reference_downloads(index):
        from os.path import relpath
        rows = ['| Document | PDF | Download | Pages |',
                '|---|---|---|---:|']
        for name, title, _ in REFERENCES:
            href = quote(Path(relpath(DOC / name, index.parent)).as_posix(), safe='/')
            rows.append(f'| {title} | [Read PDF]({href}) | '
                        f'[Download PDF]({download(name)}) | {pages[name]} |')
        return '\n'.join(rows)

    for relative in ['README.md', 'Resources/Daily Notes/README.md']:
        path = ROOT / relative
        text = path.read_text(encoding='utf-8')
        text, replaced = re.subn(
            r'\| Day \| Lessons \| Topic \| PDF \|(?: Download \|)? Pages \|\n.*?(?=\n\n)',
            lambda _: daily_table(path), text, count=1, flags=re.S)
        assert replaced == 1, f'Daily table missing from {relative}'
        if relative == 'README.md':
            text, replaced = re.subn(
                r'\| Document \| PDF \| Download \| Pages \|\n.*?(?=\n\n)',
                lambda _: reference_downloads(path), text, count=1, flags=re.S)
            assert replaced == 1, 'Reference download table missing from README.md'
        path.write_text(text, encoding='utf-8')

    reference_rows = ['| Document | Purpose | Read | Download | Pages |',
                      '|---|---|---|---|---:|']
    for name, title, purpose in REFERENCES:
        reference_rows.append(
            f'| {title} | {purpose} | [Read PDF]({quote(name)}) | '
            f'[Download PDF]({download(name)}) | {pages[name]} |')

    text = (
        '# PDF collection\n\n'
        '[Master index](../README.md) · [Editable daily notes](../Resources/Daily%20Notes/README.md)\n\n'
        f'**{len(expected)} reader PDFs · {total} pages.** This folder contains '
        'nine study days, two quick references, two Synopsys guides and '
        'one practice worksheet. Original scans and lecture decks stay in '
        '[Resources](../Resources/README.md).\n\n'
        f'[Download the complete collection ZIP]({ARCHIVE}). The ZIP includes all PDFs, '
        'editable notes and supporting files. Extract it before reading so links to '
        'other days and examples can resolve. For one document, use **Download PDF** '
        'in the tables below; the reader links open GitHub previews.\n\n'
        '## Daily reading\n\n' + daily_table(DOC / 'README.md') + '\n\n'
        'Each day contains six lessons. Together the nine days cover all 54 course '
        'lessons through Week 12. The PDFs retain the source figures, handwritten '
        'pages, explanations, worked examples, code and recall checks from the '
        'editable notes. Use clickable contents and hierarchical bookmarks; click '
        'a figure or footer to return to contents.\n\n'
        '## References and practice\n\n' + '\n'.join(reference_rows) + '\n\n'
        'The Synopsys project plan has lab meeting forms on pages 6–8 and the '
        'readiness trial on page 9. Its [editable source]'
        '(../Resources/Synopsys%20RTL%20to%20GDS%20Project%20Plan.md) '
        'contains the full requirements and execution plan. The separate '
        '[tool map source](../Resources/Synopsys%20RTL%20to%20GDS%20Tool%20Map.md) '
        'maintains the one-page process table.\n\n'
        'The practice worksheet contains questions and unmarked options. Its '
        '[checker](../Resources/tools/pdf/check_quiz.py) verifies the original '
        'sequence, figures, navigation and layout.\n\n'
        '## Reading and maintenance\n\n'
        'The reading editions use white A4 pages, dark text and embedded fonts. '
        'Keep the extracted folder structure for links to supporting files. '
        'A PDF viewer may ask before opening another local file.\n\n'
        'Page counts and download links in this index come from the actual PDFs. '
        'After editing a daily note, rebuild its PDF and inspect the rendered pages. '
        'The [build and verification guide](../Resources/tools/pdf/README.md) '
        'lists the content, navigation, source-coverage and layout checks.\n')
    (DOC / 'README.md').write_text(text, encoding='utf-8')
    print(f'Updated three indexes: {len(expected)} PDFs, {total} pages, '
          f'{len(days)} daily downloads and {len(REFERENCES)} reference downloads.')


if __name__ == '__main__':
    main()
