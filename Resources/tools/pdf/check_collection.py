"""Validate portable Markdown links, source coverage and captured-image hashes."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re, json, hashlib, sys
from collections import Counter
from pypdf import PdfReader

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE/'vendor'))
from markdown_it import MarkdownIt
md=MarkdownIt('commonmark')
files=list(ROOT.glob('*.md')) + list((ROOT/'Resources').glob('*.md'))
files += list((ROOT/'Daily Notes').glob('*.md'))
files += [ROOT/'PDFs/README.md', ROOT/'Resources/Data/README.md']
files += list((ROOT/'Resources/examples').rglob('README.md'))

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
assert register['completed_sequence']==32
assert register['current_day']==(32-1)//6+1==6
assert register['current_day_lesson']==(32-1)%6+1==2
for source in register['handwritten_new_pages']:
    file=ROOT/'Daily Notes'/f'Day {source["day"]:02d}.md'
    assert source['anchor'] in cache[file.resolve()],source
    assert (ROOT/source['path']).is_file(),source
assert len(register['handwritten_new_pages'])==32

# Validate every original page, including the 28 older pages. The structural
# checks complement the human review of the page's content and explanations.
groups=[
    ('Part 1','Resources/sources/handwritten/Part-1-original.pdf',
     'Resources/sources/handwritten/part1',24,'page-{n:02d}.jpg'),
    ('Part 2','Resources/sources/handwritten/Part-2-original.pdf',
     'Resources/sources/handwritten/scan',4,'page-{n:02d}.jpg'),
    ('Scan A','Resources/Data/Scan-A-Simulation-Synthesis-Logic-and-Formal.pdf',
     'Resources/sources/handwritten/scan-a',21,'h{n:02d}.jpg'),
    ('Scan B','Resources/Data/Scan-B-Timing-and-Constraints.pdf',
     'Resources/sources/handwritten/scan-b',11,'h{n:02d}.jpg'),
]
expected={};pdf_inventory=[]
for label,pdf_path,image_folder,count,pattern in groups:
    pdf=ROOT/pdf_path
    assert len(PdfReader(pdf).pages)==count,(label,'PDF page count')
    paths={f'{image_folder}/{pattern.format(n=n)}' for n in range(1,count+1)}
    assert {p.relative_to(ROOT).as_posix() for p in (ROOT/image_folder).glob('*.jpg')}==paths,label
    for n in range(1,count+1):
        path=f'{image_folder}/{pattern.format(n=n)}'
        expected[path]={'source':label,'pdf_page':n,'source_pdf':pdf_path}
    pdf_inventory.append({'source':label,'path':pdf_path,'pages':count,
                          'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()})
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
assert len(mapped)==60
for page in register['handwritten_new_pages']:
    target=f'../Daily%20Notes/Day%20{page["day"]:02d}.md#{page["anchor"]}'
    assert target in mapped[page['path']]['explanations'],page
    day_source=(ROOT/'Daily Notes'/f'Day {page["day"]:02d}.md').read_text(encoding='utf-8')
    assert '../'+page['path'] in unquote(day_source),(page,'Full image missing from day notes')
assert len({p['path'] for p in register['handwritten_new_pages']})==32
day_counts=Counter(p['day'] for p in mapped.values())
assert dict(sorted(day_counts.items()))=={1:16,2:12,3:14,4:7,5:8,6:3},day_counts
lesson_ids=[]
for day in range(1,7):
    ids=[int(x) for x in re.findall(r'^## Lesson (\d\d):',
         (ROOT/'Daily Notes'/f'Day {day:02d}.md').read_text(encoding='utf-8'),re.M)]
    assert ids==list(range((day-1)*6+1,min(day*6,32)+1)),(day,ids)
    lesson_ids.extend(ids)
assert lesson_ids==list(range(1,33))
empty=ROOT/register['empty_upload']['path']
assert empty.is_file() and empty.stat().st_size==0
captures=json.loads((ROOT/'Resources/sources/lecture-captures.json').read_text(encoding='utf-8'))
records=captures if isinstance(captures,list) else captures.get('captures',captures.get('frames',[]))
for c in records:
    path=ROOT/c['path']
    assert path.is_file(),c
    assert hashlib.sha256(path.read_bytes()).hexdigest()==c['sha256'],c
coverage={'source_pdfs':pdf_inventory,'readable_source_pages':60,
          'pages_per_day':dict(sorted(day_counts.items())),'completed_lessons':lesson_ids,
          'page_mappings':list(mapped.values()),'empty_upload':register['empty_upload'],
          'local_links_checked':checked,'markdown_files_checked':len(files),
          'lecture_capture_hashes_checked':len(records),
          'scope':'Structural coverage; depth and interpretation require source-to-note human review.'}
(HERE/'qa/source-coverage.json').write_text(json.dumps(coverage,indent=2),encoding='utf-8')
print(f'PASS: {checked} local links across {len(files)} Markdown files; all 60 source pages '
      f'(28 earlier + 32 new) mapped; 4 readable PDF page counts; 32 completed lessons; '
      f'{len(records)} lecture capture hashes; progress and empty-upload boundary.')
