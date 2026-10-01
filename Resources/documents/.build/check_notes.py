"""Check PDF coverage, navigation and geometry, then render every page for review."""
from pathlib import Path
import sys, json, re, hashlib, subprocess, unicodedata
from urllib.parse import unquote

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent.parent
QA=HERE/'qa'
sys.path.insert(0,str(HERE/'vendor'))
from pypdf import PdfReader
import pdfplumber
from PIL import Image, ImageDraw, ImageFont

POPPLER=Path('C:/Users/kapil/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe')
manifest=json.loads((QA/'build-manifest.json').read_text(encoding='utf-8'))
days=[int(x) for x in sys.argv[1:]] or [1,2,3,4,5,6]
checks=json.loads((QA/'checks.json').read_text(encoding='utf-8')) if (QA/'checks.json').exists() else {}

def normalized(s):
    s=unicodedata.normalize('NFKC',s)
    return re.sub(r'[^a-z0-9]','',s.lower())

for day in days:
    m=manifest[str(day)]
    pdf=HERE.parent/m['filename']
    source=(ROOT/f'Day {day:02d}.md').read_text(encoding='utf-8')
    source_images=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',source)
    source_codes=re.findall(r'^```[^\n]*\n(.*?)^```',source,re.M|re.S)
    assert len(source_images)==m['figures']
    assert len(source_codes)==m['code_blocks']
    assert {unquote(s).replace('\\','/') for s in source_images}=={r['path'].replace('\\','/') for r in m['figures_detail']}
    assert hashlib.sha256((ROOT/f'Day {day:02d}.md').read_bytes()).hexdigest()==m['source_sha256']
    r=PdfReader(pdf)
    text='\n'.join(p.extract_text() or '' for p in r.pages)
    # Editorial acceptance criterion for the formal reading edition. Check
    # exported text so a stale builder caption cannot survive unnoticed.
    reader_text=' '.join(text.split()).lower()
    forbidden=('evidence pair:', 'comparison crop', 'click either image',
               'the full handwritten page is reproduced below',
               'the larger view preserves', 'your handwritten note',
               'i am studying', 'paired figures compare')
    assert not [phrase for phrase in forbidden if phrase in reader_text], (day, 'Repetitive comparison narration')
    (QA/f'day{day:02d}-extracted.txt').write_text(text,encoding='utf-8')
    cleaned=re.sub(r'^Lesson \d\d [^\n]*\n','',text,flags=re.M)
    cleaned=re.sub(r'^Day \d\d\s*\|\s*(?:IC foundations|Physical design)[^\n]*\n','',cleaned,flags=re.M)
    cleaned=re.sub(r'^RTL to GDS\s*\n','',cleaned,flags=re.M)
    cleaned=re.sub(r'^Day \d\d\s*\|\s*Study notes\s*\n','',cleaned,flags=re.M)
    cleaned=re.sub(r'^Day \d\d\s*\|[^\n]*\n','',cleaned,flags=re.M)
    cleaned=re.sub(r'^\d+\s*$','',cleaned,flags=re.M)
    norm=normalized(cleaned)
    code_missing=[]
    for block in source_codes:
        for line in block.splitlines():
            if line.strip() and normalized(line) not in norm:
                code_missing.append(line)
    assert not code_missing, code_missing
    missing=[]
    # Require a substantial native-text signature for every retained paragraph.
    for para in m['paragraphs']:
        plain=re.sub(r'\$[^$]*\$',' ',para)
        plain=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',plain)
        plain=re.sub(r'[*`_]','',plain)
        chunks=re.split(r'\s{2,}',plain)
        candidate=max(chunks,key=len).strip()
        signature=normalized(candidate[:110])
        if len(signature)>25 and signature not in norm:
            missing.append(candidate[:140])
    assert not missing, missing
    names=r.named_destinations
    assert 'contents' in names
    for key,page in m['destinations'].items():
        assert key in names,key
        assert r.get_destination_page_number(names[key])+1==page,key
    internal=external=0
    relative=[]
    for p in r.pages:
        for ref in p.get('/Annots',[]):
            a=ref.get_object()
            if '/Dest' in a:
                internal+=1
                dst=a['/Dest']
                if isinstance(dst,str):assert dst in names,dst
            if '/A' in a:
                action=a['/A']
                if action.get('/S')=='/URI':
                    uri=str(action['/URI'])
                    if uri.startswith('http'):external+=1
                    else:
                        relative.append(uri)
                        loc=unquote(uri.split('#')[0])
                        assert (pdf.parent/loc).resolve().is_file(),uri
                        if '.pdf#nameddest=' in uri:
                            other=PdfReader((pdf.parent/loc).resolve())
                            key=unquote(uri.split('#nameddest=')[1])
                            assert key in other.named_destinations,key
    geometry=[]; sparse=[]
    with pdfplumber.open(pdf) as pp:
        for n,p in enumerate(pp.pages,1):
            bad=[c for c in p.chars if (c['x0']<52 or c['x1']>p.width-52 or c['top']<20 or c['bottom']>p.height-22)]
            if bad:geometry.append({'page':n,'characters':''.join(c['text'] for c in bad)[:180]})
            bodychars=[c for c in p.chars if 50<c['top']<p.height-50]
            image_area=sum(max(0,x['x1']-x['x0'])*max(0,x['bottom']-x['top']) for x in p.images if (x['bottom']-x['top'])>35)
            used_bottom=max([c['bottom'] for c in bodychars]+[im['bottom'] for im in p.images if im['bottom']<p.height-40]+[0])
            if used_bottom<525 and n!=len(pp.pages):
                sparse.append({'page':n,'used_bottom':round(used_bottom),'characters':len(bodychars),'image_area':round(image_area)})
    assert not geometry,geometry
    renderdir=QA/f'day{day:02d}-pages-{len(r.pages)}'
    renderdir.mkdir(exist_ok=True)
    subprocess.run([str(POPPLER),'-r','100','-png',str(pdf),str(renderdir/'page')],check=True,capture_output=True)
    pages=sorted(renderdir.glob('page-*.png'))
    assert len(pages)==len(r.pages)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
    sheets=[]
    for offset in range(0,len(pages),4):
        sheet=Image.new('RGB',(1440,2100),'#D9D9D9')
        draw=ImageDraw.Draw(sheet)
        for j,p in enumerate(pages[offset:offset+4]):
            im=Image.open(p).convert('RGB')
            im.thumbnail((700,1000))
            x=10+(j%2)*720
            y=29+(j//2)*1050
            sheet.paste(im,(x,y))
            draw.text((x,y-24),f'Day {day:02d}   page {offset+j+1}',font=font,fill='black')
        path=QA/f'day{day:02d}-sheet-{offset//4+1:02d}.jpg'
        sheet.save(path,quality=91)
        sheets.append(str(path))
    checks[str(day)]={'pages':len(r.pages),'figures':m['figures'],'paragraphs_checked':len(m['paragraphs']),
                      'code_blocks_checked':len(source_codes),'named_destinations':len(names),
                      'internal_links':internal,'external_links':external,'relative_links':len(relative),
                      'geometry_issues':geometry,'sparse_pages_to_review':sparse,'contact_sheets':sheets}
    print(json.dumps({k:v for k,v in checks[str(day)].items() if k!='contact_sheets'},ensure_ascii=False),flush=True)
(QA/'checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
