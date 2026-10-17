"""Build unanswered course-week worksheets and a selected weekly revision PDF."""
from pathlib import Path
from urllib.parse import quote,unquote,urlsplit
import hashlib,html,json,os,re,subprocess

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,
    PageBreak,KeepTogether,Table,TableStyle,Flowable,Image)
from reportlab.platypus.tableofcontents import TableOfContents
from pypdf import PdfReader,PdfWriter
from PIL import Image as PILImage

from weekly_common import (ROOT,DATA,QA,TOPICS,PDF_NAMES,LICENSE,clean,
    prepare_original_checks,load_banks,figure_path,markup)
from build_notes import (Builder,MD,Equation,CodeBlock,math_asset,STYLES)
from runtime import pdftoppm

W,H=A4
M=56.7
WIDTH=W-2*M
HEIGHT=H-2*M
INK=colors.HexColor('#25231F')
GRAY=colors.HexColor('#5C5C5C')
RULE=colors.HexColor('#D6D6D6')
S={
 'title':ParagraphStyle('WeeklyTitle',fontName='Book-Bold',fontSize=23,leading=27,spaceAfter=10,textColor=INK),
 'h1':ParagraphStyle('WeeklyHeading',fontName='Book-Bold',fontSize=16,leading=20,spaceAfter=9,keepWithNext=True,textColor=INK),
 'h2':ParagraphStyle('WeeklySubheading',fontName='Book-Bold',fontSize=12,leading=15,spaceBefore=9,spaceAfter=5,keepWithNext=True,textColor=INK),
 'body':ParagraphStyle('WeeklyBody',fontName='Book',fontSize=10.8,leading=14.3,spaceAfter=7,textColor=INK,allowWidows=0,allowOrphans=0),
 'small':ParagraphStyle('WeeklySmall',fontName='Book',fontSize=9.4,leading=12.1,spaceAfter=7,textColor=GRAY),
 'question':ParagraphStyle('WeeklyQuestion',fontName='Book-Bold',fontSize=11,leading=14,spaceBefore=8,spaceAfter=5,keepWithNext=True,textColor=INK),
 'option':ParagraphStyle('WeeklyOption',fontName='Book',fontSize=10.2,leading=13.2,textColor=INK),
}
RECORDS={}

def inline_math(src):
    p,w,h,d=math_asset(src,10.8)
    return f'<img src="{p}" width="{w:.3f}" height="{h:.3f}" valign="{-d:.3f}"/>'

class Option(Flowable):
    def __init__(self,name,index,text):
        super().__init__();self.name=name;self.index=index
        self.paragraph=Paragraph(text,S['option'])
    def wrap(self,width,height):
        self.width=width
        _,h=self.paragraph.wrap(width-29,height)
        self.height=max(17,h+5)
        return width,self.height
    def draw(self):
        y=self.height-12
        self.canv.acroForm.radio(name=self.name,value=str(self.index),selected=False,
            x=1,y=y,size=8,relative=True,borderWidth=.65,borderColor=INK,
            fillColor=colors.white,textColor=INK,fieldFlags='radio',
            tooltip=self.name.replace('_',' ')+' option '+str(self.index+1))
        self.canv.setFont('Book',9.2);self.canv.setFillColor(GRAY)
        self.canv.drawString(12,y-.1,str(self.index+1)+'.')
        self.paragraph.drawOn(self.canv,28,self.height-self.paragraph.height-2)

class WeeklyDoc(BaseDocTemplate):
    def __init__(self,path,title,label):
        super().__init__(str(path),pagesize=A4,leftMargin=M,rightMargin=M,topMargin=M,
            bottomMargin=M,title=title,author='Kapil Tripathi study collection',
            subject=label,pageCompression=1)
        self.label=label;self.current='Contents';self.destinations={};self.headings=[]
        frame=Frame(M,M,WIDTH,HEIGHT,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        self.addPageTemplates(PageTemplate(id='weekly',frames=frame,onPage=self.page_start,onPageEnd=self.page_end))
    def beforeDocument(self):
        self.destinations={};self.headings=[];self.current='Contents'
    def page_start(self,c,doc):
        if doc.page==1:c.bookmarkPage('index');c.addOutlineEntry('Contents','index',0)
    def page_end(self,c,doc):
        c.saveState();c.setFillColor(GRAY);c.setStrokeColor(RULE);c.setLineWidth(.35)
        c.setFont('Book',8.1)
        if doc.page>1:
            c.drawString(M,H-35,self.label+' | '+self.current)
            c.line(M,H-41,W-M,H-41)
        c.line(M,43,W-M,43);c.drawString(M,30,self.label+' | Contents')
        c.linkRect('','index',(M,23,M+210,41),thickness=0)
        c.drawRightString(W-M,30,str(doc.page));c.restoreState()
    def afterFlowable(self,f):
        if hasattr(f,'_weekly_heading'):
            level,key,title,toc=f._weekly_heading
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title,key,level,False)
            self.destinations[key]=self.page
            self.headings.append({'key':key,'title':title,'level':level,'page':self.page})
            if level==0:self.current=title
            if toc:self.notify('TOCEntry',(0,html.escape(title),self.page,key))

def heading(title,key,level=0,toc=False,style='h1'):
    p=Paragraph(html.escape(clean(title)),S[style]);p._weekly_heading=(level,key,title,toc)
    return p

def original_blocks(q):
    blocks=[];pending=[];pictures=[]
    def flush_text():
        if not pending:return
        text=markup(pending,inline_math)
        if text.strip():
            for chunk in text.split('\n\n'):
                if chunk.strip():blocks.append(Paragraph(chunk.replace('\n','<br/>'),S['body']))
        pending.clear()
    def flush_images():
        if not pictures:return
        n=len(pictures);col=(WIDTH-12*(n-1))/n
        images=[]
        for url in pictures:
            path=figure_path(url)
            with PILImage.open(path) as im:w,h=im.size
            scale=min(col/w,285/h,1)
            images.append(Image(str(path),width=w*scale,height=h*scale))
        if n==1:blocks.append(images[0])
        else:
            table=Table([images],colWidths=[WIDTH/n]*n)
            table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),8)]))
            blocks.append(table)
        blocks.append(Spacer(1,7));pictures.clear()
    for part in q['parts']:
        if part['type']=='image':flush_text();pictures.append(part['url'])
        elif part['type']=='text' and not part['text'].strip() and pictures:continue
        else:flush_images();pending.append(part)
    flush_text();flush_images()
    return blocks

def finish(path,doc,field_count=0):
    reader=PdfReader(path);writer=PdfWriter();writer.clone_document_from_reader(reader)
    for key,page in {'index':1,**doc.destinations}.items():writer.add_named_destination(key,page-1)
    temp=path.with_suffix('.tmp.pdf')
    with temp.open('wb') as out:writer.write(out)
    temp.replace(path)
    reader=PdfReader(path);fields=reader.get_fields() or {}
    assert len(fields)==field_count,(path,len(fields),field_count)
    assert all(f.get('/V') in (None,'/Off') for f in fields.values())
    widgets=0
    for page in reader.pages:
        for ref in page.get('/Annots',[]):
            a=ref.get_object()
            if a.get('/Subtype')=='/Widget':
                assert a.get('/AS')=='/Off';assert a.get('/Parent');assert a['/AP']['/N']
                widgets+=1
    record={'filename':path.relative_to(ROOT).as_posix(),'pages':len(reader.pages),
            'fields':field_count,'widgets':widgets,'destinations':doc.destinations,
            'headings':doc.headings,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    RECORDS[path.name]=record
    print(f'{path.name}: {record["pages"]} pages, {field_count} blank response fields.',flush=True)

def build_questions(kind):
    weeks=load_banks(kind)
    folder=ROOT/'Assignments';folder.mkdir(exist_ok=True)
    path=folder/PDF_NAMES[kind]
    title='Original course questions' if kind=='original' else 'Practice MCQs - 50 per week'
    doc=WeeklyDoc(path,title,'Original questions' if kind=='original' else 'Practice MCQs')
    story=[Paragraph(title,S['title']),Paragraph('Weeks 01 to 12 | VLSI Design Flow: RTL to GDS',S['body'])]
    if kind=='original':
        intro=('120 questions from the enrolled 2026 NPTEL course (noc26_ee147), Prof. Sneh Saurabh, IIIT Delhi. '
               'Original wording, option order and all 19 figures are retained. Prior selections and grading feedback are removed. '
               'Typographic encoding is cleaned where necessary; mathematical notation is preserved.')
    else:
        intro=('600 newly authored multiple-choice questions: 50 for each course week. '
               'They are syllabus-based practice, not authenticated past exam questions or a prediction of the examination. '
               'They combine conceptual questions, applications, code traces and numerical checks.')
    story.append(Paragraph(intro,S['body']))
    story.append(Paragraph('Choose exactly one option per question. No answers are selected or printed. '
        'The numbered circles are fillable PDF controls. Save a copy after filling. For marks, use the matching '
        f'<link href="Practice/{"original-course.html" if kind=="original" else "possible-mcqs.html"}" color="#25231F"><u>browser practice file</u></link>: '
        'finish an attempt, then choose Show marks. It displays the score without revealing correct answers.',S['body']))
    story.append(Paragraph('In Boolean expressions, adjacent variable names denote AND, + denotes OR and a prime denotes complement unless a question states a different notation. '
        'Numerical assumptions and units belong to each question. Use the bookmarks or the week index below.',S['small']))
    toc=TableOfContents();toc.levelStyles=[ParagraphStyle('WeeklyTOC',fontName='Book',fontSize=10.6,leading=17.2,leftIndent=0,rightIndent=0,textColor=INK,spaceBefore=2)]
    story.extend([Spacer(1,5),toc,Spacer(1,9)])
    if kind=='original':story.append(Paragraph('Question content: NPTEL / Prof. Sneh Saurabh. '
        f'<link href="{LICENSE}" color="#25231F"><u>CC BY-NC-SA 4.0</u></link>. '
        'Question-only study adaptation; no endorsement implied. Source links appear at each week.',S['small']))
    else:story.append(Paragraph('Prepared for independent revision. Primary topic reference: '
        '<link href="https://nptel.ac.in/courses/108106191" color="#25231F"><u>official NPTEL course outline</u></link>. '
        'Full source notes and provenance are in Resources/weekly.',S['small']))
    question_count=0
    for data in weeks:
        week=data['week'];story.append(PageBreak())
        story.append(heading(f'Week {week:02d} - {TOPICS[week]}',f'week{week:02d}',toc=True))
        if kind=='original':story.append(Paragraph(f'<link href="{data["sourceUrl"]}" color="#25231F"><u>NPTEL Assignment {week} source</u></link> | 10 questions | one option per question',S['small']))
        else:story.append(Paragraph('50 practice MCQs | one point per question | no negative marking in this practice set',S['small']))
        for q in data['questions']:
            number=q['number'];name=f'{kind}_w{week:02d}_q{number:02d}'
            key=f'{kind}-w{week:02d}-q{number:02d}'
            label=f'Week {week:02d} | Question {number:02d}'
            flows=[heading(label,key,level=1,style='question')]
            if kind=='original':flows+=original_blocks(q)
            else:flows.append(Paragraph(html.escape(clean(q['text'])).replace('\n','<br/>'),S['body']))
            options=[]
            for i,text in enumerate(q['options']):
                content=markup(q['optionParts'][i],inline_math).replace('\n',' ') if kind=='original' else html.escape(clean(text))
                options.append(Option(name,i,content))
            rows=[options[i:i+2]+([''] if len(options[i:i+2])==1 else []) for i in range(0,len(options),2)]
            table=Table(rows,colWidths=[WIDTH/2]*2,hAlign='LEFT')
            table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
            flows.extend([table,Spacer(1,9)])
            height=sum(f.wrap(WIDTH,HEIGHT)[1]+getattr(f,'spaceBefore',0)+getattr(f,'spaceAfter',0) for f in flows)
            story.append(KeepTogether(flows) if height<=HEIGHT-12 else flows[0])
            if height>HEIGHT-12:story.extend(flows[1:])
            question_count+=1
    doc.multiBuild(story)
    finish(path,doc,question_count)

class RevisionBuilder(Builder):
    def target(self,url):
        parsed=urlsplit(url)
        if parsed.scheme or parsed.netloc or not parsed.path:return url
        source=(DATA/f'Week {self.day:02d}'/unquote(parsed.path)).resolve()
        relative=Path(os.path.relpath(source,ROOT/'Revision')).as_posix()
        return quote(relative,safe='/')+(('#'+parsed.fragment) if parsed.fragment else '')

def revision_blocks(tokens,builder,section):
    out=[];i=0;number=0;ordered=None
    while i<len(tokens):
        token=tokens[i]
        if token.type=='heading_open':
            level=int(token.tag[1:]);label=tokens[i+1].content
            if level==1:out.append(Paragraph(html.escape(label),S['title']))
            else:
                number+=1;key=f'section{section}' if level==2 else f'section{section}-sub{number}'
                out.append(heading(label,key,level=0 if level==2 else 1,style='h1' if level==2 else 'h2'))
            i+=3
        elif token.type=='paragraph_open':
            if ordered is None:out.append(builder.paragraph(tokens[i+1].children,'body'))
            else:out.append(Paragraph(str(ordered)+'. '+builder.inline(tokens[i+1].children),STYLES['body']))
            i+=3
        elif token.type=='table_open':
            end=i+1
            while tokens[end].type!='table_close':end+=1
            out.append(builder.table(tokens[i:end+1]));i=end+1
        elif token.type=='math_block':out.append(Equation(token.content));i+=1
        elif token.type=='fence':out.append(CodeBlock(token.content,token.info));i+=1
        elif token.type=='ordered_list_open':ordered=int(token.attrGet('start') or 1)-1;i+=1
        elif token.type=='ordered_list_close':ordered=None;i+=1
        elif token.type=='list_item_open':
            if ordered is not None:ordered+=1
            i+=1
        elif token.type in ('bullet_list_open','bullet_list_close','list_item_close','html_block'):i+=1
        else:raise ValueError((token.type,token.content[:60]))
    return out

def revision_scans(folder,entries):
    """Render original handwriting, retaining a source digest and explicit crop."""
    assets=QA/f'{folder.name} handwriting';assets.mkdir(exist_ok=True)
    records=[]
    for entry in entries:
        source=folder/entry['source']
        digest=hashlib.sha256(source.read_bytes()).hexdigest()
        if entry.get('source_sha256'):
            assert digest==entry['source_sha256'],f'Original source changed: {source}'
        page=entry['page'];prefix=assets/f'{source.stem}-{page:02d}-{digest[:8]}'
        if source.suffix.lower()=='.pdf':
            subprocess.run([str(pdftoppm()),'-f',str(page),'-l',str(page),
                '-singlefile','-r','160','-png',str(source),str(prefix)],
                capture_output=True,check=True)
            path=prefix.with_suffix('.png')
        else:
            # Use canonical full-page scans directly, without recompression.
            with PILImage.open(source) as original:original.verify()
            path=source
        if entry.get('crop_top_ratio'):
            with PILImage.open(path) as original:
                top=round(original.height*entry['crop_top_ratio'])
                cropped=original.crop((0,top,original.width,original.height))
            path=assets/f'{prefix.name}-week-portion.png';cropped.save(path)
        records.append({**entry,'path':path,'source_sha256':digest})
    return records

def build_revision(week=1):
    source=DATA/f'Week {week:02d}'/'revision.md'
    parts=source.read_text(encoding='utf-8').split('<!-- page -->')
    config_path=source.with_suffix('.json')
    config=json.loads(config_path.read_text(encoding='utf-8')) if config_path.exists() else {
        'sections':['ICs','Styles','Economics','Partitioning','HLS','Trade-offs','Numericals','Unix/sources']}
    assert len(parts)==len(config['sections'])
    scans=revision_scans(source.parent,config.get('handwritten',[]))
    folder=ROOT/'Revision';folder.mkdir(exist_ok=True)
    path=folder/f'Week {week:02d} - Revision.pdf'
    doc=WeeklyDoc(path,f'Week {week} revision',f'Week {week} revision');builder=RevisionBuilder(week,'')
    # The source supplies explicit page sections; use compact links rather than a separate cover.
    story=[]
    for i,text in enumerate(parts,1):
        if i>1:story.append(PageBreak())
        if i==1:
            first=text.split('## 1.',1)
            story+=revision_blocks(MD.parse(first[0]),builder,1)
            links=' | '.join(f'<link href="#section{n}" color="#25231F"><u>{n}. {label}</u></link>'
                for n,label in enumerate(config['sections'],1))
            if scans:links+=' | <link href="#handwritten-1" color="#25231F"><u>Your handwriting</u></link>'
            story.append(Paragraph(links,S['small']))
            story+=revision_blocks(MD.parse('## 1.'+first[1]),builder,1)
        else:story+=revision_blocks(MD.parse(text),builder,i)
    for i,entry in enumerate(scans,1):
        story.append(PageBreak())
        story.append(heading(entry['title'],f'handwritten-{i}'))
        story.append(Paragraph(html.escape(entry['caption']),S['small']))
        with PILImage.open(entry['path']) as im:w,h=im.size
        scale=min(WIDTH/w,(HEIGHT-110)/h)
        picture=Image(str(entry['path']),width=w*scale,height=h*scale)
        picture.hAlign='CENTER';story.append(picture)
    doc.build(story)
    assert doc.page==len(parts)+len(scans),('Revision overflow',doc.page,len(parts)+len(scans))
    for i in range(1,len(parts)+1):
        assert doc.destinations[f'section{i}']==i,('Section overflow',i,doc.destinations)
    finish(path,doc)
    RECORDS[path.name]['guide_pages']=len(parts)
    RECORDS[path.name]['handwritten']=[{k:v for k,v in entry.items() if k!='path'} for entry in scans]

def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--revision-only',action='store_true',help='Rebuild the short revision without changing assignments.')
    mode.add_argument('--practice-only',action='store_true',help='Rebuild practice questions without changing the other PDFs.')
    parser.add_argument('--week',type=int,default=1,help='Revision week to build (default: 1).')
    args=parser.parse_args()
    if (QA/'build.json').exists():RECORDS.update(json.loads((QA/'build.json').read_text(encoding='utf-8')))
    if args.practice_only:
        build_questions('practice')
    elif not args.revision_only:
        prepare_original_checks()
        build_questions('original')
        build_questions('practice')
    if not args.practice_only:build_revision(args.week)
    (QA/'build.json').write_text(json.dumps(RECORDS,indent=2),encoding='utf-8')
    if not args.practice_only:
        from combine_revisions import build_combined
        build_combined()

if __name__=='__main__':main()
