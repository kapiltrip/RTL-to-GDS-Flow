"""Verify reference coverage, PDF navigation, local destinations and page geometry."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import hashlib, json, re, subprocess, sys, unicodedata
from pypdf import PdfReader
import pdfplumber

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
QA = HERE / 'qa/references'
POPPLER = Path('C:/Users/kapil/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe')
sys.path.insert(0, str(HERE / 'vendor'))
from markdown_it import MarkdownIt

def normalized(value):
    value = unicodedata.normalize('NFKC', value).casefold()
    return re.sub(r'[^a-z0-9]', '', value)

records = json.loads((QA / 'manifest.json').read_text(encoding='utf-8'))
results = {}
for key, record in records.items():
    path = ROOT / record['filename']
    reader = PdfReader(path)
    assert len(reader.pages) == record['pages']
    source = ROOT / 'Resources' / ('Flow Map.md' if key == 'flow' else 'Glossary.md')
    assert hashlib.sha256(source.read_bytes()).hexdigest() == record['source_sha256']
    assert key != 'flow' or len(reader.pages) == 2
    text = '\n'.join(p.extract_text() or '' for p in reader.pages)
    norm = normalized(text)
    if key == 'glossary':
        source_terms = [line.split('|')[1].strip() for line in source.read_text(encoding='utf-8').splitlines()
                        if line.startswith('| ') and not line.startswith('| Term |')]
        assert len(record['terms']) == len(source_terms)
        assert {term['term'] for term in record['terms']} == set(source_terms)
        for term in record['terms']:
            for field in ('term', 'expansion', 'meaning'):
                assert normalized(term[field]) in norm, (term['term'], field)
        assert {'SDC (logic)', 'SDC (timing)', 'CDC', 'Liberty', 'tCQ', 'tSU', 'tH'} <= {t['term'] for t in record['terms']}
    else:
        for token in MarkdownIt('commonmark').enable('table').parse(source.read_text(encoding='utf-8')):
            if token.type != 'inline': continue
            plain = ''.join(c.content for c in token.children if c.type in ('text', 'code_inline'))
            assert normalized(plain) in norm, ('Missing flow text', plain)
    names = reader.named_destinations
    for destination, page in record['destinations'].items():
        assert destination in names, destination
        assert reader.get_destination_page_number(names[destination]) + 1 == page, destination
    def outlines(items):
        for item in items:
            if isinstance(item, list): yield from outlines(item)
            else: yield str(item.title), reader.get_destination_page_number(item) + 1
    actual = set(outlines(reader.outline))
    for heading in record['headings']:
        assert (heading['title'], heading['page']) in actual, heading
    local = external = internal = footer = 0
    others = {}
    first = reader.pages[0].indirect_reference
    for n, page in enumerate(reader.pages, 1):
        footer_seen = False
        for ref in page.get('/Annots', []):
            annotation = ref.get_object()
            if '/Dest' in annotation:
                internal += 1
                dest = annotation['/Dest']
                if isinstance(dest, str):
                    assert dest in names, dest
                    contents = reader.get_destination_page_number(names[dest]) == 0
                else:
                    assert dest[0] in [p.indirect_reference for p in reader.pages]
                    contents = dest[0] == first
                if contents and float(annotation['/Rect'][1]) <= 30 <= float(annotation['/Rect'][3]):
                    footer_seen = True
            action = annotation.get('/A')
            if action and action.get('/S') == '/URI':
                url = str(action['/URI']); parsed = urlsplit(url)
                if parsed.scheme:
                    assert parsed.scheme in ('http', 'https'), url
                    external += 1
                else:
                    local += 1
                    target = (path.parent / unquote(parsed.path)).resolve()
                    assert target.is_file(), url
                    if target.suffix.casefold() == '.pdf' and parsed.fragment.startswith('nameddest='):
                        if target not in others: others[target] = PdfReader(target)
                        other = others[target]
                        assert unquote(parsed.fragment[len('nameddest='):]) in other.named_destinations, url
        assert footer_seen, (key, 'Footer back-link missing', n)
        footer += 1
    issues = []
    with pdfplumber.open(path) as pdf:
        for n, page in enumerate(pdf.pages, 1):
            for c in page.chars:
                if c['x0'] < 55 or c['x1'] > page.width - 55 or c['top'] < 20 or c['bottom'] > page.height - 22:
                    issues.append((n, c['text'], c['x0'], c['top']))
    assert not issues, issues[:20]
    (QA / f'{key}-extracted.txt').write_text(text, encoding='utf-8')
    output = QA / f'{key}-pages-{len(reader.pages)}'
    output.mkdir(exist_ok=True)
    subprocess.run([str(POPPLER), '-r', '115', '-png', str(path), str(output / 'page')],
                   check=True, capture_output=True)
    assert len(list(output.glob('page-*.png'))) == len(reader.pages)
    results[key] = {'pages': len(reader.pages), 'named_destinations': len(names),
                    'terms': len(record.get('terms', [])), 'internal_links': internal,
                    'local_links': local, 'external_links': external, 'footer_links': footer,
                    'geometry_issues': issues, 'cross_document_destinations': len(others)}
    print(key, json.dumps(results[key]), flush=True)
(QA / 'checks.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
