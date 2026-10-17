"""Check every preserved page, image, navigation target and combined-page render."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,re,subprocess

from pypdf import PdfReader
from PIL import Image,ImageDraw,ImageFont,ImageChops
import pdfplumber

from weekly_common import ROOT
from combine_revisions import COMBINED_QA,OUTPUT,discover,portable_url
from runtime import pdftoppm

def digest(data):return hashlib.sha256(data).hexdigest()
def normalized(text):return re.sub(r'\s+','',text or '')
def image_streams(page):
    return sorted(digest(image.indirect_reference.get_object().get_data()) for image in page.images)

def link_page(reader,annotation):
    target=annotation.get('/Dest')
    action=annotation.get('/A')
    if action and action.get('/S')=='/GoTo':target=action.get('/D')
    if target is None:return None
    if isinstance(target,str):
        name=str(target)
        assert name in reader.named_destinations,('Missing named destination',name)
        return reader.get_destination_page_number(reader.named_destinations[name])
    reference=target[0]
    if isinstance(reference,int):return reference
    for index,page in enumerate(reader.pages):
        if page.indirect_reference==reference:return index
    raise AssertionError(('Destination references a non-page object',target))

def link_signature(annotation):return tuple(round(float(n),3) for n in annotation['/Rect'])

def render(path,prefix):
    prefix.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run([str(pdftoppm()),'-r','90','-png',str(path),str(prefix)],capture_output=True,check=True)
    return sorted(prefix.parent.glob(prefix.name+'-*.png'))

def main():
    record=json.loads((COMBINED_QA/'build.json').read_text(encoding='utf-8'))
    assert digest(OUTPUT.read_bytes())==record['sha256']
    reader=PdfReader(OUTPUT);assert len(reader.pages)==record['pages']
    assert not reader.get_fields()
    assert [r['file'] for r in record['weeks']]==[p.relative_to(ROOT).as_posix() for p in discover()]
    assert reader.get_destination_page_number(reader.named_destinations['combined.contents'])==0
    links=0;images=0;pages=0;sources=[];reading_links=0
    for entry in record['weeks']:
        source=ROOT/entry['file'];assert digest(source.read_bytes())==entry['sha256']
        original=PdfReader(source);sources.append((source,original,entry))
        assert len(original.pages)==entry['pages']
        offset=entry['start']-1
        prefix=f'week{entry["week"]:02d}.'
        for name,target in original.named_destinations.items():
            assert reader.get_destination_page_number(reader.named_destinations[prefix+name])==offset+original.get_destination_page_number(target)
        for index,page in enumerate(original.pages):
            copied=reader.pages[offset+index]
            assert normalized(page.extract_text()) in normalized(copied.extract_text()),(entry['week'],index+1,'Missing text')
            assert list(page.mediabox)==list(copied.mediabox)
            assert image_streams(page)==image_streams(copied),(entry['week'],index+1,'Image content changed')
            images+=len(page.images);pages+=1
            destinations={};external={}
            for ref in copied.get('/Annots',[]):
                annotation=ref.get_object();target=link_page(reader,annotation)
                if target is not None:destinations.setdefault(link_signature(annotation),set()).add(target)
                action=annotation.get('/A')
                if action and action.get('/S')=='/URI':
                    url=urlsplit(str(action['/URI']))
                    assert url.scheme in ('http','https'),('Nonportable reference link',str(action['/URI']))
                    external.setdefault(link_signature(annotation),set()).add(str(action['/URI']))
            for ref in page.get('/Annots',[]):
                annotation=ref.get_object();target=link_page(original,annotation)
                if target is not None:
                    assert target+offset in destinations.get(link_signature(annotation),set()),(entry['week'],index+1,'Week link escaped its section')
                    links+=1
                action=annotation.get('/A')
                if action and action.get('/S')=='/URI':
                    assert portable_url(str(action['/URI'])) in external.get(link_signature(annotation),set())
                    reading_links+=1
            assert any(link_page(reader,ref.get_object())==0 and ref.get_object().get('/A') for ref in copied.get('/Annots',[])),('Missing all-weeks footer',offset+index+1)
    index_targets=[link_page(reader,ref.get_object()) for ref in reader.pages[0].get('/Annots',[])]
    for entry in record['weeks']:assert entry['start']-1 in index_targets
    def outlines(items):
        for item in items:
            if isinstance(item,list):yield from outlines(item)
            else:
                page=reader.get_destination_page_number(item)
                assert 0<=page<len(reader.pages)
                yield item['/Title'],page
    outline=list(outlines(reader.outline))
    for entry in record['weeks']:
        assert any(title.startswith(f'Week {entry["week"]:02d} - ') and page==entry['start']-1 for title,page in outline)
    with pdfplumber.open(OUTPUT) as pdf:
        for number,page in enumerate(pdf.pages,1):
            bad=[c for c in page.chars if c['x0']<54 or c['x1']>page.width-54 or c['top']<20 or c['bottom']>page.height-22]
            assert not bad,(number,''.join(c['text'] for c in bad)[:80])
    tasks=[(OUTPUT,COMBINED_QA/'pages/page')]+[(source,COMBINED_QA/f'sources/week{entry["week"]:02d}/page') for source,_,entry in sources]
    with ThreadPoolExecutor(max_workers=4) as pool:renders=list(pool.map(lambda task:render(*task),tasks))
    combined=renders[0];assert len(combined)==record['pages']
    for (_,original,entry),rendered in zip(sources,renders[1:]):
        assert len(rendered)==len(original.pages)
        for index,path in enumerate(rendered):
            with Image.open(path) as before,Image.open(combined[entry['start']-1+index]) as after:
                assert before.size==after.size
                body=(0,0,before.width,before.height-63)
                assert ImageChops.difference(before.convert('RGB').crop(body),after.convert('RGB').crop(body)).getbbox() is None,(entry['week'],index+1,'Rendered body changed')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18);sheets=[]
    for offset in range(0,len(combined),4):
        sheet=Image.new('RGB',(1440,2100),'#DDDDDD');draw=ImageDraw.Draw(sheet)
        for index,path in enumerate(combined[offset:offset+4]):
            with Image.open(path) as original:im=original.convert('RGB');im.thumbnail((700,1000))
            x=10+(index%2)*720;y=32+(index//2)*1050
            sheet.paste(im,(x,y));draw.text((x,y-25),f'Combined page {offset+index+1}',font=font,fill='black')
        path=COMBINED_QA/f'sheet-{offset//4+1:02d}.jpg';sheet.save(path,quality=90);sheets.append(str(path))
    result={'filename':record['filename'],'sha256':record['sha256'],'pages':record['pages'],
        'preserved_weekly_pages':pages,'preserved_image_streams':images,'verified_original_internal_links':links,
        'verified_portable_reference_links':reading_links,
        'outline_items':len(outline),'pixel_identical_page_bodies':pages,'sheets':sheets}
    (COMBINED_QA/'checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='sheets'},indent=2))

if __name__=='__main__':main()
