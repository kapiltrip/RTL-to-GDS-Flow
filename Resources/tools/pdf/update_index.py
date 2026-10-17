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
from weekly_common import TOPICS as WEEK_TOPICS

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
WEEKLY = [
    ('Revision/Combined Revision.pdf', 'Combined revision', 'All prepared weeks in one PDF, expanded as new weeks are added'),
    ('Assignments/Original Course Questions - Weeks 01 to 12.pdf', 'Original course questions', '120 original questions across Weeks 1-12'),
    ('Assignments/Practice MCQs - 50 per Week.pdf', '50 practice MCQs per week', '600 newly authored questions across Weeks 1-12'),
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
    revision_paths=sorted((ROOT/'Revision').glob('Week ?? - Revision.pdf'))
    revisions=[(int(re.search(r'Week (\d+)',path.name)[1]),path,len(PdfReader(path).pages)) for path in revision_paths]
    weekly_specs=[WEEKLY[0]]+[(path.relative_to(ROOT).as_posix(),f'Week {week} revision',WEEK_TOPICS[week])
                             for week,path,_ in revisions]+WEEKLY[1:]
    weekly = [(relative, title, purpose, len(PdfReader(ROOT / relative).pages))
              for relative, title, purpose in weekly_specs if (ROOT / relative).is_file()]
    assert len(weekly) in (0, len(weekly_specs)), 'Incomplete weekly study pack'

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

    def weekly_table(index):
        from os.path import relpath
        rows = ['| Study pack | Read | Download | Pages |', '|---|---|---|---:|']
        for relative, title, purpose, count in weekly:
            href = quote(Path(relpath(ROOT / relative, index.parent)).as_posix(), safe='/')
            url = REPOSITORY + '/raw/refs/heads/main/' + quote(relative, safe='/')
            rows.append(f'| {title}: {purpose} | [Read PDF]({href}) | [Download PDF]({url}) | {count} |')
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
            if weekly:
                text, replaced = re.subn(
                    r'\| Study pack \| Read \| Download \| Pages \|\n.*?(?=\n\n)',
                    lambda _: weekly_table(path), text, count=1, flags=re.S)
                assert replaced == 1, 'Weekly study table missing from README.md'
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
        f'**{len(expected)} full reading PDFs · {total} pages.** This folder contains '
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
    if weekly:
        text += ('\n## Weekly revision and assignments\n\n' + weekly_table(DOC / 'README.md') + '\n\n'
                 'The weekly packs are in the separate [Revision](../Revision/README.md) and '
                 '[Assignments](../Assignments/README.md) folders. Use the combined revision for every prepared week; '
                 'both question sets cover all 12 weeks. The [browser practice download]('
                 + REPOSITORY + '/raw/refs/heads/main/Assignments/Practice/Browser%20Practice%20-%20All%20Weeks.zip) '
                 'lets you fill answers and reveal marks later without displaying correct answers.\n')
    (DOC / 'README.md').write_text(text, encoding='utf-8')
    combined=ROOT/WEEKLY[0][0]
    if combined.is_file():
        from os.path import relpath
        weeks=[week for week,_,_ in revisions]
        label=(f'Week {weeks[0]}' if len(weeks)==1 else
               f'Weeks {weeks[0]} to {weeks[-1]}' if weeks==list(range(weeks[0],weeks[-1]+1)) else
               'Weeks '+', '.join(map(str,weeks)))
        count=len(PdfReader(combined).pages)
        url=REPOSITORY+'/raw/refs/heads/main/'+quote(WEEKLY[0][0],safe='/')
        for index in (ROOT/'README.md',ROOT/'Revision/README.md'):
            read=quote(Path(relpath(combined,index.parent)).as_posix(),safe='/')
            block=('<!-- combined-revision:start -->\n'
                   f'**One revision download: [Download Combined Revision.pdf]({url})** '
                   f'· [Read PDF]({read})\n\n'
                   f'Includes **{label} · {count} pages**, with explanations, worked examples, original handwriting, '
                   'linked contents and bookmarks. Future prepared weeks are added to this same file; '
                   'the download link stays the same.\n'
                   '<!-- combined-revision:end -->')
            text=index.read_text(encoding='utf-8')
            text,changed=re.subn(r'<!-- combined-revision:start -->.*?<!-- combined-revision:end -->',lambda _:block,text,count=1,flags=re.S)
            assert changed==1,f'Combined revision block missing from {index}'
            if index.parent.name=='Revision':
                rows=['| Week | Revision | Download | Pages |','|---|---|---|---:|']
                for week,path,pages_in_week in revisions:
                    relative=path.relative_to(ROOT).as_posix()
                    rows.append(f'| {week:02d} | [{WEEK_TOPICS[week]}]({quote(path.name)}) | '
                                f'[Download PDF]({REPOSITORY}/raw/refs/heads/main/{quote(relative,safe="/")}) | {pages_in_week} |')
                text,changed=re.subn(r'\| Week \| Revision \| Download \| Pages \|\n.*?(?=\n\n)',lambda _:'\n'.join(rows),text,count=1,flags=re.S)
                assert changed==1,'Individual revision table missing'
            index.write_text(text,encoding='utf-8')
    print(f'Updated three indexes: {len(expected)} PDFs, {total} pages, '
          f'{len(days)} daily downloads, {len(REFERENCES)} reference downloads and '
          f'{len(weekly)} weekly-pack downloads.')


if __name__ == '__main__':
    main()
