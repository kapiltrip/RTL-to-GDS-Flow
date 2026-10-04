"""Validate portable Markdown links, source coverage and captured-image hashes."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re, json, hashlib, sys, argparse
from collections import Counter

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE/'vendor'))
from pypdf import PdfReader
from markdown_it import MarkdownIt
md=MarkdownIt('commonmark')
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--require-originals', action='store_true',
                    help='Require all eight raw PDFs in the local archive as well as portable images.')
parser.add_argument('--public-only', action='store_true',
                    help='Check published material without using the ignored local PDF archive.')
args=parser.parse_args()
assert not (args.require_originals and args.public_only), 'Choose one archive mode.'
excluded={'.git','.work','vendor','cache','qa','logs','history','__pycache__','.venv'}
files=sorted(p for p in ROOT.rglob('*.md')
             if not excluded.intersection(p.relative_to(ROOT).parts))

def anchors(file):
    counts={};result=set()
    for line in file.read_text(encoding='utf-8').splitlines():
        if not re.match(r'^#{1,6}\s',line):continue
        label=re.sub(r'^#+\s*','',line).strip()
        label=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',label)
        label=label.replace('`','').replace('*','')
        key=re.sub(r'\s','-',re.sub(r'[^\w\s-]','',label.lower()))
        n=counts.get(key,0);counts[key]=n+1
        result.add(key+(f'-{n}' if n else ''))
    result.update(re.findall(r'<a\s+(?:id|name)=[\"\']([^\"\']+)',file.read_text(encoding='utf-8')))
    return result

cache={p.resolve():anchors(p) for p in files}
errors=[];checked=0
for file in files:
    for t in md.parse(file.read_text(encoding='utf-8')):
        for child in t.children or []:
            if child.type not in ('link_open','image'):continue
            url=child.attrGet('href' if child.type=='link_open' else 'src')
            parsed=urlsplit(url)
            if parsed.scheme or parsed.netloc:continue
            path=(file.parent/unquote(parsed.path)).resolve() if parsed.path else file.resolve()
            checked+=1
            if not path.is_file():errors.append(f'{file.relative_to(ROOT)} -> missing {url}');continue
            if parsed.fragment and path.suffix.lower()=='.md':
                if path not in cache:cache[path]=anchors(path)
                if unquote(parsed.fragment) not in cache[path]:
                    errors.append(f'{file.relative_to(ROOT)} -> missing anchor {url}')
assert not errors,'\n'.join(errors)
register=json.loads((ROOT/'Resources/sources/study-register.json').read_text(encoding='utf-8'))
assert register['completed_sequence']==54
assert register['current_day']==(54-1)//6+1==9
assert register['current_day_lesson']==(54-1)%6+1==6
for source in register['handwritten_new_pages']:
    file=ROOT/'Daily Notes'/f'Day {source["day"]:02d}.md'
    assert source['anchor'] in cache[file.resolve()],source
    assert (ROOT/source['path']).is_file(),source
assert len(register['handwritten_new_pages'])==100

# Validate every original page, including the 28 older pages. The structural
# checks complement the human review of the page's content and explanations.
inventory=json.loads((ROOT/'Resources/sources/handwritten-inventory.json').read_text(encoding='utf-8'))
assert inventory['schema_version']==1 and inventory['readable_pages']==128
assert len(inventory['originals'])==8
expected={};pdf_inventory=[]
for original in inventory['originals']:
    label=original['source']; pdf_path=original['path']; count=original['pages']
    pdf=ROOT/pdf_path; local=original['local_archive']
    available=pdf.is_file() and not (args.public_only and local)
    if args.require_originals or not local: assert available,(label,'Missing original PDF')
    if available:
        assert len(PdfReader(pdf).pages)==count,(label,'PDF page count')
        assert hashlib.sha256(pdf.read_bytes()).hexdigest()==original['sha256'],(label,'Original PDF hash')
    pages=original['page_images']
    assert [p['pdf_page'] for p in pages]==list(range(1,count+1)),label
    paths={p['path'] for p in pages}; folder=(ROOT/pages[0]['path']).parent
    assert {p.relative_to(ROOT).as_posix() for p in folder.glob('*.jpg')}==paths,label
    for page in pages:
        path=page['path']
        assert path not in expected,path
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==page['sha256'],path
        expected[path]={'source':label,'pdf_page':page['pdf_page'],'source_pdf':pdf_path}
    pdf_inventory.append({k:original[k] for k in ('source','path','pages','sha256')})
    pdf_inventory[-1]['original_verified_in_this_run']=available
index=ROOT/'Resources/Handwritten Index.md'
mapped={}
for row in index.read_text(encoding='utf-8').splitlines():
    if not row.startswith('|') or 'sources/handwritten/' not in row or '.jpg)' not in row:continue
    paths=re.findall(r'\]\((sources/handwritten/[^)]+\.jpg)\)',row)
    assert len(paths)==1,row
    path='Resources/'+unquote(paths[0])
    assert path in expected and path not in mapped,path
    targets=re.findall(r'\]\((\.\./Daily%20Notes/Day%20(\d\d)\.md#[^)]+)\)',row)
    assert targets,(path,'Missing explanation')
    assert len({int(day) for url,day in targets})==1,(path,'Mixed-day source identity')
    mapped[path]={**expected[path],'path':path,'day':int(targets[0][1]),
                  'explanations':[url for url,day in targets],
                  'sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest()}
assert set(mapped)==set(expected),(set(expected)-set(mapped),set(mapped)-set(expected))
assert len(mapped)==128
for page in register['handwritten_new_pages']:
    target=f'../Daily%20Notes/Day%20{page["day"]:02d}.md#{page["anchor"]}'
    assert target in mapped[page['path']]['explanations'],page
    day_source=(ROOT/'Daily Notes'/f'Day {page["day"]:02d}.md').read_text(encoding='utf-8')
    assert '../'+page['path'] in unquote(day_source),(page,'Full image missing from day notes')
assert len({p['path'] for p in register['handwritten_new_pages']})==100
day_counts=Counter(p['day'] for p in mapped.values())
assert dict(sorted(day_counts.items()))=={1:16,2:12,3:14,4:7,5:8,6:15,7:17,8:17,9:22},day_counts
lesson_ids=[]
for day in range(1,10):
    ids=[int(x) for x in re.findall(r'^## Lesson (\d\d):',
         (ROOT/'Daily Notes'/f'Day {day:02d}.md').read_text(encoding='utf-8'),re.M)]
    assert ids==list(range((day-1)*6+1,day*6+1)),(day,ids)
    lesson_ids.extend(ids)
assert lesson_ids==list(range(1,55))
empty=ROOT/register['empty_upload']['path']
if empty.is_file() and not args.public_only: assert empty.stat().st_size==0
elif args.require_originals: raise AssertionError('Missing preserved empty upload')
captures=json.loads((ROOT/'Resources/sources/lecture-captures.json').read_text(encoding='utf-8'))
records=captures if isinstance(captures,list) else captures.get('captures',captures.get('frames',[]))
for c in records:
    path=ROOT/c['path']
    assert path.is_file(),c
    assert hashlib.sha256(path.read_bytes()).hexdigest()==c['sha256'],c
coverage={'source_pdfs':pdf_inventory,'readable_source_pages':128,
          'pages_per_day':dict(sorted(day_counts.items())),'completed_lessons':lesson_ids,
          'page_mappings':list(mapped.values()),'empty_upload':register['empty_upload'],
          'local_links_checked':checked,'markdown_files_checked':len(files),
          'lecture_capture_hashes_checked':len(records),
          'scope':'Structural coverage; depth and interpretation require source-to-note human review.'}
(HERE/'qa').mkdir(parents=True,exist_ok=True)
(HERE/'qa/source-coverage.json').write_text(json.dumps(coverage,indent=2),encoding='utf-8')
verified=sum(p['original_verified_in_this_run'] for p in pdf_inventory)
print(f'PASS: {checked} local links across {len(files)} Markdown files; all 128 source pages '
      f'(28 earlier + 32 previous + 68 October) mapped and hashed; {verified}/8 original PDFs verified here; 54 completed lessons; '
      f'{len(records)} lecture capture hashes; progress and empty-upload boundary.')
