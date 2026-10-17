"""Maintain one stable revision download containing every prepared week."""
from io import BytesIO
from pathlib import Path
from urllib.parse import quote,unquote,urlsplit
import hashlib,html,json,re

from pypdf import PdfReader,PdfWriter
from pypdf.generic import DictionaryObject,NameObject,TextStringObject
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph,Spacer,Table,TableStyle

from weekly_common import ROOT,QA,TOPICS
from build_weekly import WeeklyDoc,S,W,H,M,WIDTH,GRAY,RULE

OUTPUT=ROOT/'Revision/Combined Revision.pdf'
COMBINED_QA=QA/'combined'
REPOSITORY='https://github.com/kapiltrip/RTL-to-GDS-Flow'

def portable_url(url):
    parsed=urlsplit(url)
    if parsed.scheme or parsed.netloc or not parsed.path:return url
    target=(ROOT/'Revision'/unquote(parsed.path)).resolve()
    assert target.is_file(),f'Missing further-reading target: {url}'
    relative=target.relative_to(ROOT).as_posix()
    route='/blob/main/' if target.suffix.lower()=='.md' else '/raw/refs/heads/main/'
    return REPOSITORY+route+quote(relative,safe='/')+('#'+parsed.fragment if parsed.fragment else '')

def discover(folder=None):
    paths=sorted((folder or ROOT/'Revision').glob('Week ?? - Revision.pdf'))
    assert paths,'No prepared weekly revision PDFs found.'
    weeks=[int(re.fullmatch(r'Week (\d\d) - Revision.pdf',p.name)[1]) for p in paths]
    assert weeks==sorted(set(weeks)) and all(1<=w<=12 for w in weeks)
    return paths

def coverage(weeks):
    if len(weeks)==1:return f'Week {weeks[0]}'
    if weeks==list(range(weeks[0],weeks[-1]+1)):return f'Weeks {weeks[0]} to {weeks[-1]}'
    return 'Weeks '+', '.join(map(str,weeks[:-1]))+' and '+str(weeks[-1])

def namespace(reader,prefix):
    """Prevent each week's identically named contents/section targets colliding."""
    def tree(node):
        node=node.get_object()
        if '/Names' in node:
            names=node['/Names']
            for i in range(0,len(names),2):names[i]=TextStringObject(prefix+str(names[i]))
        for child in node.get('/Kids',[]):tree(child)
    names=reader.root_object.get('/Names')
    if names and '/Dests' in names:tree(names['/Dests'])
    def destination(obj):
        for key in ('/Dest','/D'):
            value=obj.get(key)
            if isinstance(value,str):obj[NameObject(key)]=TextStringObject(prefix+value)
        action=obj.get('/A')
        if action and action.get('/S')=='/GoTo':destination(action)
    for page in reader.pages:
        for ref in page.get('/Annots',[]):destination(ref.get_object())
    outlines=reader.root_object.get('/Outlines')
    def outline(node):
        while node:
            node=node.get_object();destination(node)
            if node.get('/First'):outline(node['/First'])
            node=node.get('/Next')
    if outlines and outlines.get('/First'):outline(outlines['/First'])

def index_page(entries,total):
    output=BytesIO();doc=WeeklyDoc('', 'Combined revision','Combined revision')
    doc.filename=output
    weeks=[r['week'] for r in entries]
    story=[Paragraph('Combined Revision',S['title']),
        Paragraph('VLSI Design Flow: RTL to GDS | '+coverage(weeks),S['body']),
        Paragraph('One file for the prepared revision guides. Every weekly explanation, worked example, '
            'handwritten page and source link is retained. Choose a week below or use the PDF bookmarks.',S['body']),
        Spacer(1,8)]
    rows=[[Paragraph('Week',S['small']),Paragraph('Revision guide',S['small']),Paragraph('PDF pages',S['small'])]]
    for record in entries:
        url=f'combined:week{record["week"]:02d}'
        link=lambda label:Paragraph(f'<link href="{url}" color="#25231F"><u>{html.escape(label)}</u></link>',S['body'])
        rows.append([link(f'{record["week"]:02d}'),link(TOPICS[record['week']]),link(f'{record["start"]}-{record["end"]}')])
    table=Table(rows,colWidths=[48,WIDTH-130,82],hAlign='LEFT')
    table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),7),
        ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LINEABOVE',(0,0),(-1,0),.5,RULE),('LINEBELOW',(0,0),(-1,-1),.35,RULE)]))
    story.extend([table,Spacer(1,14),
        Paragraph(f'<b>{total} pages in this edition.</b> Page numbers in the right-hand column and '
            'the lower-right footer refer to this combined PDF. The contents link at the left of '
            'each weekly footer returns to that week; <b>All weeks</b> returns here.',S['body']),
        Paragraph('When another week is prepared, it will be added to this same file. '
            'The download filename stays <b>Combined Revision.pdf</b>; download it again to get the expanded edition.',S['body']),
        Paragraph('Coverage includes only the weeks listed above. The course has 12 weeks; later guides '
            'are added when requested. The local app remains for assignment practice.',S['small'])])
    doc.build(story)
    assert doc.page==1,('Combined contents overflow',doc.page)
    output.seek(0);return PdfReader(output)

def folio(number,total,all_weeks):
    output=BytesIO();c=canvas.Canvas(output,pagesize=(W,H))
    c.setFillColorRGB(1,1,1);c.rect(W-M-50,22,51,19,fill=1,stroke=0)
    c.setFillColor(GRAY);c.setFont('Book',8.1)
    c.drawRightString(W-M,30,f'{number} / {total}')
    if all_weeks:
        x=W-M-143;c.drawString(x,30,'All weeks')
        c.linkURL('combined:contents',(x,23,x+46,41),relative=0,thickness=0)
    c.save();output.seek(0);return PdfReader(output).pages[0]

def build_combined(paths=None,output=OUTPUT):
    paths=list(paths) if paths is not None else discover()
    entries=[];start=2
    for path in paths:
        reader=PdfReader(path);week=int(re.fullmatch(r'Week (\d\d) - Revision.pdf',path.name)[1])
        count=len(reader.pages)
        entries.append({'week':week,'file':path.relative_to(ROOT).as_posix(),
            'pages':count,'start':start,'end':start+count-1,
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        start+=count
    total=start-1
    writer=PdfWriter();writer.append(index_page(entries,total),import_outline=False)
    writer.add_named_destination('combined.contents',0)
    writer.add_outline_item('All weeks - contents',0)
    for path,entry in zip(paths,entries):
        reader=PdfReader(path);prefix=f'week{entry["week"]:02d}.'
        namespace(reader,prefix)
        writer.append(reader,outline_item=f'Week {entry["week"]:02d} - {TOPICS[entry["week"]]}',import_outline=True)
    assert len(writer.pages)==total
    for number,page in enumerate(writer.pages,1):page.merge_page(folio(number,total,number>1))
    for page in writer.pages:
        for ref in page.get('/Annots',[]):
            annotation=ref.get_object();action=annotation.get('/A')
            if not action or action.get('/S')!='/URI':continue
            url=str(action['/URI'])
            if url=='combined:contents':target='combined.contents'
            elif re.fullmatch(r'combined:week\d\d',url):target=url.split(':')[1]+'.index'
            else:
                action[NameObject('/URI')]=TextStringObject(portable_url(url))
                continue
            annotation[NameObject('/A')]=DictionaryObject({NameObject('/S'):NameObject('/GoTo'),NameObject('/D'):TextStringObject(target)})
    writer.add_metadata({'/Title':'Combined Revision - '+coverage([e['week'] for e in entries]),
        '/Author':'Kapil Tripathi study collection','/Subject':'Prepared weekly revision guides with original handwriting',
        '/Keywords':'NPTEL, VLSI Design Flow, RTL to GDS, revision'})
    output.parent.mkdir(parents=True,exist_ok=True)
    temp=output.with_suffix('.tmp.pdf')
    with temp.open('wb') as stream:writer.write(stream)
    temp.replace(output)
    record={'filename':output.relative_to(ROOT).as_posix(),'pages':total,'index_pages':1,
        'weeks':entries,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}
    if output==OUTPUT:
        COMBINED_QA.mkdir(exist_ok=True)
        (COMBINED_QA/'build.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
    print(f'{output.name}: {coverage([e["week"] for e in entries])}, {total} pages.',flush=True)
    return record

if __name__=='__main__':build_combined()
