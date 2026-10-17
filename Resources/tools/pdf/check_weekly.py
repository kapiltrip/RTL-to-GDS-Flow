"""Verify blank forms, question coverage, source figures, links and rendered layout."""
from pathlib import Path
from urllib.parse import unquote,urlsplit
import hashlib,json,re,subprocess
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
from PIL import Image,ImageDraw,ImageFont
from pypdf import PdfReader,PdfWriter
import pdfplumber
from weekly_common import ROOT,DATA,QA,load_banks,clean,figure_path
from runtime import pdftoppm

def normalized(value):return re.sub(r'[^a-z0-9]','',clean(value).lower())
def pixels(image):
    rgb=image.convert('RGB');return rgb.size,hashlib.sha256(rgb.tobytes()).hexdigest()

def check(record):
    path=ROOT/record['filename'];reader=PdfReader(path)
    assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256']
    assert len(reader.pages)==record['pages']
    fields=reader.get_fields() or {}
    assert len(fields)==record['fields']
    names=reader.named_destinations
    for key,page in record['destinations'].items():
        assert reader.get_destination_page_number(names[key])+1==page,(path,key)
    text='\n'.join(p.extract_text() or '' for p in reader.pages)
    norm=normalized(text)
    assert not any(s in text for s in ('Accepted answer is','Yes, the answer is correct','No, the answer is incorrect'))
    native_widgets={}
    for number,page in enumerate(reader.pages,1):
        for ref in page.get('/Annots',[]):
            a=ref.get_object()
            if a.get('/Subtype')=='/Widget':
                assert a['/AS']=='/Off';parent=a['/Parent']
                assert parent.get('/V') in (None,'/Off');assert a['/AP']['/N']
                assert parent['/T'] in fields
                native_widgets.setdefault(str(parent['/T']),[]).append((number,a))
            action=a.get('/A')
            if action and action.get('/S')=='/URI':
                url=urlsplit(str(action['/URI']))
                if not url.scheme and url.path:assert (path.parent/unquote(url.path)).resolve().is_file(),str(action['/URI'])
    assert sum(map(len,native_widgets.values()))==record['widgets']
    issues=[];body_counts=[]
    with pdfplumber.open(path) as pdf:
        for number,p in enumerate(pdf.pages,1):
            chars=p.chars
            bad=[c for c in chars if c['x0']<54 or c['x1']>p.width-54 or c['top']<20 or c['bottom']>p.height-22]
            if bad:issues.append((number,''.join(c['text'] for c in bad)[:130]))
            body_counts.append(sum(52<c['top']<p.height-50 for c in chars))
    assert not issues,(path.name,issues[:15])
    assert all(n>50 for n in body_counts),(path.name,'Unexpected sparse text page',body_counts)
    kind='original' if path.name.startswith('Original') else ('practice' if path.name.startswith('Practice') else None)
    figures=0;math_parts=0;checked_text=0;handwritten_figures=0
    if kind:
        for week in load_banks(kind):
            for q in week['questions']:
                name=f'{kind}_w{week["week"]:02d}_q{q["number"]:02d}'
                assert name in fields and len(native_widgets[name])==len(q['options']),(name,'Options')
                assert fields[name].get('/V') in (None,'/Off')
                if kind=='practice':
                    assert normalized(q['text']) in norm,(name,'Missing prompt')
                    for option in q['options']:assert normalized(option) in norm,(name,'Missing option')
                else:
                    for part in q['parts']+sum(q['optionParts'],[]):
                        if part['type'] in ('text','code'):
                            signature=normalized(part['text'])
                            if len(signature)>18:assert signature in norm,(name,'Missing source text',part['text'][:80]);checked_text+=1
                        elif part['type'] in ('mathml','latex'):math_parts+=1
                    destination=f'original-w{week["week"]:02d}-q{q["number"]:02d}'
                    first=reader.get_destination_page_number(names[destination])
                    stop=first+3
                    observed=None
                    for image in q.get('images',[]):
                        if observed is None:
                            observed=set()
                            for p in reader.pages[first:stop]:
                                for saved in p.images:
                                    observed.add(pixels(saved.image))
                        with Image.open(figure_path(image['url'])) as original:assert pixels(original) in observed,(name,'Source figure pixels')
                        figures+=1
        assert len(fields)==(120 if kind=='original' else 600)
    if path.parent.name=='Revision':
        from build_notes import MD
        from build_weekly import revision_scans
        week=int(re.search(r'Week (\d+)',path.name)[1])
        source=DATA/f'Week {week:02d}'/'revision.md'
        parts=source.read_text(encoding='utf-8').split('<!-- page -->')
        assert len(parts)==record.get('guide_pages',len(parts))
        for number,part in enumerate(parts,1):
            assert reader.get_destination_page_number(names[f'section{number}'])==number-1
            page_norm=normalized(reader.pages[number-1].extract_text() or '')
            for token in MD.parse(part):
                fragments=[child.content for child in token.children or [] if child.type in ('text','code_inline')]
                if token.type=='fence':fragments.append(token.content)
                for fragment in fragments:
                    signature=normalized(fragment)
                    if len(signature)>10:
                        assert signature in page_norm,(path.name,number,'Missing revision text',fragment[:80])
                        checked_text+=1
        scans=revision_scans(source.parent,record.get('handwritten',[]))
        assert len(reader.pages)==len(parts)+len(scans)
        for index,scan in enumerate(scans,1):
            page=len(parts)+index-1
            assert reader.get_destination_page_number(names[f'handwritten-{index}'])==page
            embedded=list(reader.pages[page].images)
            if scan['path'].suffix.lower() in ('.jpg','.jpeg'):
                # pypdf's image-export helper can re-encode JPEGs. Check the
                # native DCT stream instead: ReportLab preserves it verbatim.
                original=scan['path'].read_bytes()
                assert any(saved.indirect_reference.get_object().get_data()==original for saved in embedded),(path.name,index,'Original JPEG changed')
            else:
                with Image.open(scan['path']) as original:expected=pixels(original)
                assert expected in {pixels(saved.image) for saved in embedded},(path.name,index,'Handwriting changed')
            handwritten_figures+=1
    output=QA/path.stem;output.mkdir(exist_ok=True)
    (output/'extracted.txt').write_text(text,encoding='utf-8')
    subprocess.run([str(pdftoppm()),'-r','90','-png',str(path),str(output/'page')],capture_output=True,check=True)
    pages=sorted(output.glob('page-*.png'))
    assert len(pages)==record['pages']
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    sheets=[]
    for offset in range(0,len(pages),4):
        sheet=Image.new('RGB',(1440,2100),'#DDDDDD');draw=ImageDraw.Draw(sheet)
        for index,image in enumerate(pages[offset:offset+4]):
            with Image.open(image) as original:im=original.convert('RGB');im.thumbnail((700,1000))
            x=10+(index%2)*720;y=32+(index//2)*1050
            sheet.paste(im,(x,y));draw.text((x,y-25),f'Page {offset+index+1}',font=font,fill='black')
        target=output/f'sheet-{offset//4+1:02d}.jpg';sheet.save(target,quality=90);sheets.append(str(target))
    return {'file':record['filename'],'pages':len(pages),'blank_fields':len(fields),
            'blank_widgets':record['widgets'],'verified_source_figures':figures,
            'verified_handwritten_figures':handwritten_figures,'source_math_parts':math_parts,
            'source_text_fragments_checked':checked_text,'geometry_issues':issues,'sheets':sheets}

def check_roundtrip(record):
    reader=PdfReader(ROOT/record['filename']);writer=PdfWriter();writer.clone_document_from_reader(reader)
    groups=reader.get_fields();chosen=list(groups)[::max(1,len(groups)-1)]
    values={name:'/0' for name in chosen}
    writer.update_page_form_field_values(None,values,auto_regenerate=False)
    target=QA/(Path(record['filename']).stem+' - form roundtrip.pdf')
    with target.open('wb') as output:writer.write(output)
    saved=PdfReader(target)
    for name in chosen:
        assert saved.get_fields()[name]['/V']=='/0'
        group=saved.get_fields()[name]
        states=[kid.get_object()['/AS'] for kid in group['/Kids']]
        assert states.count('/0')==1 and states.count('/Off')==len(states)-1
    print(f'PASS: form save/reopen round trip for {len(chosen)} groups in {Path(record["filename"]).name}.',flush=True)

def main():
    records=json.loads((QA/'build.json').read_text(encoding='utf-8'))
    with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(check,records.values()))
    for record in records.values():
        if record['fields']:check_roundtrip(record)
    assert sum(r['blank_fields'] for r in results)==720
    assert sum(r['blank_widgets'] for r in results)==3319
    assert sum(r['verified_source_figures'] for r in results)==19
    (QA/'checks.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    for result in results:print({k:v for k,v in result.items() if k!='sheets'},flush=True)

if __name__=='__main__':main()
