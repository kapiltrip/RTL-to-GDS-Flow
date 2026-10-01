"""Build the six reader-facing PDFs from the editable daily notes."""
from pathlib import Path
import os, sys, re, json, hashlib, html, math, io, unicodedata
from urllib.parse import unquote, quote, urlparse, urlsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
OUT = ROOT / 'PDFs'
CACHE = HERE / 'cache'
QA = HERE / 'qa'
for folder in (CACHE, QA):
    folder.mkdir(exist_ok=True, parents=True)
os.environ['MPLCONFIGDIR'] = str(CACHE / 'matplotlib')
sys.path.insert(0, str(HERE / 'vendor'))
from markdown_it import MarkdownIt
from PIL import Image as PILImage
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib.mathtext import MathTextParser, math_to_image
from matplotlib.font_manager import FontProperties
from svglib.svglib import svg2rlg
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, KeepTogether, Flowable, CondPageBreak,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.graphics import renderPDF
from pypdf import PdfReader, PdfWriter

FONTDIR = Path('C:/Windows/Fonts')
for name, filename in [('Book','cambria.ttc'), ('Book-Bold','cambriab.ttf'),
                       ('Book-Italic','cambriai.ttf'), ('Book-BoldItalic','cambriaz.ttf'),
                       ('Code','consola.ttf'), ('Code-Bold','consolab.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONTDIR / filename)))
pdfmetrics.registerFontFamily('Book', normal='Book', bold='Book-Bold',
                             italic='Book-Italic', boldItalic='Book-BoldItalic')
pdfmetrics.registerFontFamily('Code', normal='Code', bold='Code-Bold',
                             italic='Code', boldItalic='Code-Bold')
matplotlib.rcParams.update({'mathtext.fontset': 'stix', 'font.family':'STIXGeneral'})
PAGE_W, PAGE_H = A4
MARGIN = 56.7
WIDTH = PAGE_W - 2*MARGIN
HEIGHT = PAGE_H - 2*MARGIN
DARK = colors.HexColor('#25231F')
GRAY = colors.HexColor('#5C5C5C')
RULE = colors.HexColor('#D6D6D6')

STYLES = {}
def style(name, **kw):
    defaults = dict(fontName='Book', fontSize=11.2, leading=15.3, textColor=DARK,
                    spaceAfter=7.2, allowWidows=0, allowOrphans=0,
                    splitLongWords=1, borderPadding=0)
    defaults.update(kw)
    STYLES[name] = ParagraphStyle(name, **defaults)
    return STYLES[name]

style('body')
style('title', fontName='Book-Bold', fontSize=24, leading=28, spaceAfter=10)
style('subtitle', fontSize=12.3, leading=16.5, spaceAfter=12)
style('small', fontSize=9.3, leading=12.1, textColor=GRAY, spaceAfter=7)
style('caption', fontSize=9.1, leading=11.6, textColor=GRAY, spaceBefore=5, spaceAfter=9)
style('lesson', fontName='Book-Bold', fontSize=17, leading=21, spaceBefore=0,
      spaceAfter=11, keepWithNext=1)
style('heading', fontName='Book-Bold', fontSize=13.4, leading=17.1,
      spaceBefore=13, spaceAfter=7, keepWithNext=1)
style('subheading', fontName='Book-Bold', fontSize=11.7, leading=15.1,
      spaceBefore=10, spaceAfter=5, keepWithNext=1)
style('cell', fontSize=9.6, leading=12.6, spaceAfter=0, allowWidows=1, allowOrphans=1)
style('cellhead', fontName='Book-Bold', fontSize=9.6, leading=12.6,
      spaceAfter=0, allowWidows=1, allowOrphans=1)
style('bullet', leftIndent=15, firstLineIndent=0, bulletIndent=1,
      spaceAfter=5.5, bulletFontName='Book', bulletFontSize=10.6)
style('quote', leftIndent=0, rightIndent=0, fontName='Book', spaceAfter=8)

TITLES = {
 1: ('IC foundations and logic synthesis', 'Lessons 01 to 06',
     'Integration, implementation choices, architectural design, Unix and synthesis'),
 2: ('Physical design and Verilog foundations', 'Lessons 07 to 12',
     'Layout, verification, manufacturing, Tcl and the first two Verilog lessons'),
}
TITLES.update({
3:('Simulation RTL synthesis and two-level optimization','Lessons 13 to 18','Simulation scheduling, hardware inference and minimum Boolean covers'),
4:('Multilevel optimization and formal verification','Lessons 19 to 24','Factoring, FSMs, BDDs, SAT and model checking'),
5:('Equivalence libraries and static timing analysis','Lessons 25 to 30','Equivalence, timing models, setup and hold, graph propagation and variation'),
6:('OpenSTA and clock constraints','Lessons 31 to 32','Timing reports and clock constraints through Week 8 Constraints I'),
})
FILES = {1:'Day 01 - IC Foundations and Logic Synthesis.pdf',
         2:'Day 02 - Physical Design and Verilog Foundations.pdf'}
FILES.update({3:'Day 03 - Simulation Synthesis and Logic Optimization.pdf',4:'Day 04 - Multilevel Optimization and Formal Verification.pdf',5:'Day 05 - Equivalence Libraries and Static Timing Analysis.pdf',6:'Day 06 - OpenSTA and Clock Constraints.pdf'})
LESSONS = {
1:'IC construction and manufacturing foundations',
2:'Implementation choices and design quality',
3:'Architecture and the design flow',
4:'High level synthesis and timing',
5:'Unix foundations for EDA',
6:'Logic synthesis and technology mapping',
7:'Physical design and closure',
8:'Verification and manufacturing test',
9:'From layout to a packaged chip',
10:'Tcl commands and automation',
11:'Verilog values types and hardware modeling',
12:'Verilog structure events and assignments',
}
LESSONS.update({13:'Functional verification using simulation',14:'High-level synthesis using Bambu',15:'RTL synthesis Part I',16:'RTL synthesis Part II',17:'Logic optimization Part I',18:'Simulation with Icarus',19:'Logic optimization Part II',20:'Logic optimization Part III',21:'Formal verification I',22:'Logic synthesis using Yosys',23:'Formal verification II',24:'Formal verification III',25:'Formal verification IV',26:'Technology library',27:'Logic optimization using Yosys',28:'Static timing analysis I',29:'Static timing analysis II',30:'Static timing analysis III',31:'Static timing analysis using OpenSTA',32:'Constraints I'})

def clean(text):
    return text.replace('\u202f',' ').replace('\u00a0',' ').replace('—',' - ').replace('–','-').replace('−','-').replace('‑','-')

def slug(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text, flags=re.UNICODE)
    return re.sub(r'\s', '-', text)

def md_math_inline(state, silent):
    start = state.pos
    if state.src[start] != '$' or state.src.startswith('$$', start):
        return False
    end = start+1
    while True:
        end = state.src.find('$', end)
        if end < 0:
            return False
        if state.src[end-1] != '\\':
            break
        end += 1
    if not silent:
        token = state.push('math_inline','math',0)
        token.content = state.src[start+1:end]
    state.pos = end+1
    return True

def md_math_block(state, startLine, endLine, silent):
    start = state.bMarks[startLine] + state.tShift[startLine]
    end = state.eMarks[startLine]
    if state.src[start:end].strip() != '$$':
        return False
    nextline = startLine+1
    while nextline < endLine:
        line = state.src[state.bMarks[nextline]:state.eMarks[nextline]].strip()
        if line == '$$':
            break
        nextline += 1
    if nextline == endLine:
        raise ValueError('Unclosed display equation')
    if not silent:
        token=state.push('math_block','math',0)
        token.block=True
        token.content=state.getLines(startLine+1,nextline,0,False).strip()
        token.map=[startLine,nextline+1]
    state.line=nextline+1
    return True

MD = MarkdownIt('commonmark', {'html':False}).enable('table')
MD.inline.ruler.before('escape','math_inline',md_math_inline)
MD.block.ruler.before('paragraph','math_block',md_math_block)
MATH_PARSER = MathTextParser('agg')
MATH_CACHE = {}

def latex_fix(src):
    for old,new in [('ge','geq'),('le','leq'),('land','wedge'),('lor','vee')]:
        src=re.sub(r'\\'+old+r'\b',lambda m:'\\'+new,src)
    return src

def math_asset(src, size=11.2, vector=False):
    src=latex_fix(src)
    key=hashlib.sha256(f'{src}|{size}|{vector}'.encode()).hexdigest()[:20]
    if key in MATH_CACHE:
        return MATH_CACHE[key]
    prop=FontProperties(size=size, family='STIXGeneral')
    formula='$'+src+'$'
    if vector:
        target=CACHE/(key+'.svg')
        if not target.exists():
            math_to_image(formula,str(target),prop=prop,format='svg',color='#25231F')
        d=svg2rlg(str(target))
        if d is None:
            raise ValueError(src)
        value=d
    else:
        dpi=300
        parsed=MATH_PARSER.parse(formula,dpi=dpi,prop=prop)
        alpha=np.asarray(parsed.image)
        rgba=np.empty((*alpha.shape,4),dtype=np.uint8)
        rgba[:,:,:3]=[37,35,31]
        rgba[:,:,3]=alpha
        target=CACHE/(key+'.png')
        PILImage.fromarray(rgba).save(target)
        value=(str(target).replace('\\','/'),parsed.width*72/dpi,
               parsed.height*72/dpi,parsed.depth*72/dpi)
    MATH_CACHE[key]=value
    return value

class Equation(Flowable):
    def __init__(self,src):
        Flowable.__init__(self)
        self.src=src
        self.drawing=math_asset(src,12,True)
        self.spaceBefore=6
        self.spaceAfter=10
    def wrap(self,aW,aH):
        self.scale=min(1,aW/self.drawing.width)
        self.width=aW
        self.height=self.drawing.height*self.scale+5
        return self.width,self.height
    def draw(self):
        self.canv.saveState()
        self.canv.translate((self.width-self.drawing.width*self.scale)/2,2)
        self.canv.scale(self.scale,self.scale)
        renderPDF.draw(self.drawing,self.canv,0,0)
        self.canv.restoreState()

class CodeBlock(Flowable):
    def __init__(self,text,language='',continued=False):
        Flowable.__init__(self)
        self.lines=text.rstrip('\n').split('\n')
        self.language=language
        self.continued=continued
        self.size=9.0
        self.leading=12.0
        self.spaceBefore=5
        self.spaceAfter=10
    def wrap(self,aW,aH):
        longest=max([pdfmetrics.stringWidth(x,'Code',self.size) for x in self.lines]+[1])
        if longest>aW-20:
            self.size=max(8.05,self.size*(aW-20)/longest)
            self.leading=self.size*1.34
        longest=max(pdfmetrics.stringWidth(x,'Code',self.size) for x in self.lines)
        if longest>aW-18:
            raise ValueError(f'Code line too wide {longest}: {self.lines}')
        self.width=aW
        self.height=24+len(self.lines)*self.leading+10
        return self.width,self.height
    def split(self,aW,aH):
        self.wrap(aW,aH)
        fit=int((aH-34)//self.leading)
        if fit<5 or len(self.lines)-fit<3:
            return []
        first=CodeBlock('\n'.join(self.lines[:fit]),self.language,self.continued)
        second=CodeBlock('\n'.join(self.lines[fit:]),self.language,True)
        return [first,second]
    def draw(self):
        c=self.canv
        c.setFillColor(colors.HexColor('#F7F7F7'))
        c.rect(0,0,self.width,self.height,fill=1,stroke=0)
        c.setStrokeColor(RULE)
        c.setLineWidth(.45)
        c.line(0,self.height,self.width,self.height)
        c.line(0,0,self.width,0)
        c.setFont('Book',8.3)
        c.setFillColor(GRAY)
        label={'verilog':'Verilog','tcl':'Tcl','bash':'Bash','text':'Expected output'}.get(self.language,self.language)
        c.drawString(10,self.height-13,label+(' continued' if self.continued else ''))
        c.setFont('Code',self.size)
        c.setFillColor(DARK)
        y=self.height-25
        for line in self.lines:
            c.drawString(10,y,clean(line))
            y-=self.leading

class StudyFigure(Flowable):
    """Keep each source figure with its caption and permit modest fit adjustments."""
    def __init__(self,path,w,h,caption,base_scale=1.0):
        Flowable.__init__(self)
        self.path=path
        self.base_w=w
        self.base_h=h
        self.caption=caption
        self.scale=base_scale
        self.spaceBefore=5
        self.spaceAfter=9
    def wrap(self,aW,aH):
        self.width=aW
        self.cap=Paragraph(self.caption,STYLES['caption'])
        _,self.cap_h=self.cap.wrap(aW,aH)
        self.height=self.base_h*self.scale+6+self.cap_h
        return self.width,self.height
    def split(self,aW,aH):
        self.wrap(aW,aH)
        possible=(aH-self.cap_h-8)/self.base_h
        # Avoid reducing the source below a comfortably readable size.
        if possible>=.80 and possible<self.scale:
            return [StudyFigure(self.path,self.base_w,self.base_h,self.caption,possible)]
        return []
    def draw(self):
        w=self.base_w*self.scale
        h=self.base_h*self.scale
        self.canv.drawImage(str(self.path),(self.width-w)/2,self.cap_h+6,
                            width=w,height=h,preserveAspectRatio=True,mask='auto')
        self.canv.linkRect('', 'contents', ((self.width-w)/2,self.cap_h+6,(self.width+w)/2,self.cap_h+6+h),relative=1,thickness=0)
        self.cap.drawOn(self.canv,0,0)

class EvidencePair(Flowable):
    def __init__(self,figures,caption):
        Flowable.__init__(self)
        self.figures=figures;self.caption=caption
        self.spaceBefore=5;self.spaceAfter=10
    def wrap(self,aW,aH):
        self.width=aW;self.col=(aW-14)/2
        self.dims=[]
        for f in self.figures:
            w,h=PILImage.open(f.path).size
            s=min(self.col/w,245/h)
            self.dims.append((w*s,h*s))
        self.image_h=max(h for w,h in self.dims)
        self.cap=Paragraph(self.caption,STYLES['caption'])
        _,self.cap_h=self.cap.wrap(aW,aH)
        self.height=19+self.image_h+8+self.cap_h
        return self.width,self.height
    def draw(self):
        c=self.canv
        for j,(f,(w,h)) in enumerate(zip(self.figures,self.dims)):
            x=j*(self.col+14)
            c.setFont('Book-Bold',9.6);c.setFillColor(DARK)
            c.drawString(x,self.height-10,'Lecture' if j==0 else 'Handwritten notes')
            px=x+(self.col-w)/2;py=self.height-19-h
            c.drawImage(str(f.path),px,py,width=w,height=h,mask='auto')
            c.linkRect('','contents',(px,py,px+w,py+h),relative=1,thickness=0)
        self.cap.drawOn(c,0,0)

def htmlplain(src):
    return re.sub(r'<[^>]*>','',html.unescape(src))

class Builder:
    def __init__(self,day,source):
        self.day=day
        self.source=source
        self.figure_count=0
        self.figure_records=[]
        self.headings=[]
        self.lesson=0
        self.external={}
        self.anchor_keys={}
        self.code_records=[]
        self.body_records=[]
        self.dest_pages={}
        self.counts={}
    def target(self,url):
        url=unquote(url)
        if url.startswith('#'):
            if re.match(r'#day-\d+-index$',url) or url=='#lesson-index':return '#contents'
            return '#'+url[1:]
        m=re.match(r'Day (0[1-6])\.md(?:#(.*))?$',url)
        if m:
            targetday=int(m.group(1))
            anchor=m.group(2) or 'contents'
            if targetday==self.day:
                return '#'+anchor
            return quote(FILES[targetday])+'#nameddest='+quote(anchor)
        if url.startswith('http'):
            if 'youtube.com' not in url:
                self.external.setdefault(url,'')
            return url
        parsed = urlsplit(url)
        target = (ROOT / 'Daily Notes' / parsed.path).resolve()
        references = {
            ROOT / 'Resources/Glossary.md': ROOT / 'Full Forms.pdf',
            ROOT / 'Resources/Flow Map.md': ROOT / 'RTL to GDS Flow.pdf',
        }
        target = references.get(target, target)
        relative = Path(os.path.relpath(target, OUT)).as_posix()
        result = quote(relative, safe='/')
        if parsed.fragment and target.suffix.lower() != '.pdf':
            result += '#' + quote(parsed.fragment)
        return result
    def inline(self,tokens,sty='body'):
        parts=[]
        size=STYLES[sty].fontSize
        for t in tokens or []:
            typ=t.type
            if typ=='text':parts.append(html.escape(clean(t.content)))
            elif typ=='softbreak':parts.append(' ')
            elif typ=='hardbreak':parts.append('<br/>')
            elif typ=='code_inline':
                # Keep comparisons and quoted bits native and searchable.
                parts.append(f'<font name="Code" size="{size*.86:.2f}">{html.escape(clean(t.content))}</font>')
            elif typ=='strong_open':parts.append('<b>')
            elif typ=='strong_close':parts.append('</b>')
            elif typ=='em_open':parts.append('<i>')
            elif typ=='em_close':parts.append('</i>')
            elif typ=='link_open':
                url=self.target(t.attrGet('href'))
                parts.append(f'<link href="{html.escape(url,quote=True)}" color="#25231F"><u>')
            elif typ=='link_close':parts.append('</u></link>')
            elif typ=='math_inline':
                p,w,h,d=math_asset(t.content,size)
                parts.append(f'<img src="{p}" width="{w:.3f}" height="{h:.3f}" valign="{-d:.3f}"/>')
            elif typ=='image':
                raise ValueError('Inline figure was not handled')
            else:
                raise ValueError(f'Unsupported inline {typ} {t.content}')
        return ''.join(parts)
    def paragraph(self,tokens,sty='body',bullet=None):
        return Paragraph(self.inline(tokens,sty),STYLES[sty],bulletText=bullet)
    def simple(self,text,sty='body'):
        return self.paragraph(MD.parseInline(text)[0].children,sty)
    def table(self,tokens,keep_small=True):
        rows=[]; row=[]; header=True
        for t in tokens:
            if t.type=='tr_open':row=[]
            elif t.type=='inline':row.append(t)
            elif t.type=='tr_close':rows.append(row)
        n=len(rows[0]); raw=[]; weights=[]
        for r in rows:
            if len(r)!=n: raise ValueError('Ragged table')
            raw.append([x.content for x in r])
        # Wide explanatory columns receive space; short record keys stay compact.
        for c in range(n):
            lens=[len(re.sub(r'[`*$]','',r[c])) for r in raw]
            weights.append(max(11,(sum(lens)/len(lens))**.68))
        if n==2:
            weights=[max(16,min(weights[0],weights[1]*.8)),max(26,weights[1])]
        widths=[WIDTH*w/sum(weights) for w in weights]
        # Key numeric/boolean columns do not take an equal share of narrative tables.
        numeric_heads={'Index','Input','PMOS','NMOS','Good `n`','Good `y`','New `q1`','New `q2`'}
        for c,head in enumerate(raw[0]):
            if head in numeric_heads:
                widths[c]=min(widths[c],60)
        total=sum(widths)
        widths=[w*WIDTH/total for w in widths]
        # An inline equation is an indivisible image. Reserve its actual width
        # before distributing the remaining space to prose columns.
        minimums=[]
        for c in range(n):
            formulas=[]
            for r in rows:
                children=r[c].children
                for j,t in enumerate(children):
                    if t.type!='math_inline':
                        continue
                    suffix=''
                    if j+1<len(children) and children[j+1].type=='text':
                        word=re.match(r'\s*\S*',children[j+1].content)
                        suffix=word.group(0) if word else ''
                    formulas.append(math_asset(t.content,9.6)[1]+12+
                                    pdfmetrics.stringWidth(suffix,'Book',9.6))
            minimums.append(max([28]+formulas))
        if sum(minimums)>WIDTH:
            raise ValueError(f'Table equations exceed the printable width: {raw[0]}')
        widths=[max(w,m) for w,m in zip(widths,minimums)]
        excess=sum(widths)-WIDTH
        if excess>0:
            spare=[w-m for w,m in zip(widths,minimums)]
            total_spare=sum(spare)
            widths=[w-excess*s/total_spare for w,s in zip(widths,spare)]
        assert all(w+0.01>=m for w,m in zip(widths,minimums)), raw[0]
        data=[]
        for i,r in enumerate(rows):
            data.append([self.paragraph(x.children,'cellhead' if i==0 else 'cell') for x in r])
        tbl=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT',spaceBefore=5,spaceAfter=11)
        tbl.setStyle(TableStyle([
          # Keep the last two body rows together on continuation pages.
          ('NOSPLIT',(0,max(1,len(data)-2)),(-1,len(data)-1)),
          ('VALIGN',(0,0),(-1,-1),'TOP'),
          ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
          ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
          ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#F5F5F5')),
          ('LINEABOVE',(0,0),(-1,0),.65,RULE),('LINEBELOW',(0,0),(-1,0),.65,RULE),
          ('LINEBELOW',(0,1),(-1,-1),.35,RULE),
        ]))
        return KeepTogether([tbl]) if keep_small and tbl.wrap(WIDTH,HEIGHT)[1]<=200 else tbl
    def figure(self,token,caption_tokens=None):
        self.figure_count+=1
        path=(ROOT/'Daily Notes'/unquote(token.attrGet('src'))).resolve()
        if not path.is_file():raise FileNotFoundError(path)
        w,h=PILImage.open(path).size
        hand='/h' in path.as_posix()
        maxh=HEIGHT-100 if hand else (235 if self.day >= 3 else 285)
        scale=min(WIDTH/w,maxh/h)
        img=Image(str(path),w*scale,h*scale)
        img.hAlign='CENTER'
        img.spaceBefore=5
        label=f'Figure {self.day}.{self.figure_count:02d}'
        caption=(f'<b>{label}.</b> '+self.inline(caption_tokens,'caption')) if caption_tokens else (
            f'<b>{label}.</b> '+html.escape(clean(token.content)))
        cap=Paragraph(caption,STYLES['caption'])
        self.figure_records.append({'id':label,'path':str(path.relative_to(ROOT)),
                                    'pixels':[w,h],'width_pt':w*scale,'height_pt':h*scale,
                                    'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        return StudyFigure(path,w*scale,h*scale,caption)
    def blocks(self,tokens):
        out=[]; i=0; lists=[]
        while i<len(tokens):
            t=tokens[i]; typ=t.type
            if typ=='heading_open':
                raw=tokens[i+1].content; level=int(t.tag[1])
                anchor=slug(raw)
                count=self.counts.get(anchor,0); self.counts[anchor]=count+1
                if count:anchor+=f'-{count}'
                m=re.match(r'Lesson (\d+):',raw)
                display=clean(raw)
                if level==2 and m:
                    self.lesson=int(m.group(1))
                    display=f'Lesson {self.lesson:02d} {LESSONS[self.lesson]}'
                    # Separate the first chapter from the contents. Later
                    # chapters may share space with a preceding conclusion.
                    first_new_chapter=self.day >= 3 and not any(h['level']==0 for h in self.headings)
                    out.append(PageBreak() if first_new_chapter else CondPageBreak(390))
                    out.append(Spacer(1,10))
                sty='lesson' if level==2 else ('heading' if level==3 else 'subheading')
                p=Paragraph(html.escape(display),STYLES[sty])
                p._heading=(max(0,level-2),anchor,display,self.lesson)
                self.headings.append({'level':max(0,level-2),'key':anchor,'title':display,'lesson':self.lesson})
                # A nested KeepTogether around a small table can interrupt
                # the heading's keepWithNext chain. Keep the actual heading
                # and table in one group so the heading travels with it.
                if level>=3 and i+3<len(tokens) and tokens[i+3].type=='table_open':
                    j=i+3
                    k=j+1
                    while tokens[k].type!='table_close':k+=1
                    tbl=self.table(tokens[j:k+1],keep_small=False)
                    if tbl.wrap(WIDTH,HEIGHT)[1]<=200:
                        out.append(KeepTogether([p,tbl]));i=k+1;continue
                out.append(p); i+=3; continue
            if typ=='paragraph_open':
                it=tokens[i+1]; children=it.children or []
                imgs=[x for x in children if x.type=='image']
                if imgs and all(x.type in ('image','link_open','link_close','hardbreak','softbreak') or (x.type=='text' and not x.content.strip()) for x in children):
                    caption=None; advance=3
                    if i+4<len(tokens) and tokens[i+3].type=='paragraph_open':
                        nxt=tokens[i+4]
                        if nxt.content.startswith(('*Lecture:','*Source:','*Video frame:','*Handwritten source:','*Evidence pair:')):
                            caption=nxt.children;advance=6
                    if len(imgs)==2:
                        figs=[self.figure(x) for x in imgs]
                        out.append(EvidencePair(figs,self.inline(caption,'caption') if caption else ''))
                    else:out.append(self.figure(imgs[0],caption))
                    i+=advance;continue
                sty='body';bullet=None
                if lists:
                    sty='bullet'
                    if lists[-1].get('pending'):
                        bullet=str(lists[-1]['index'])+'.' if lists[-1]['ordered'] else '\u2022'
                        lists[-1]['pending']=False
                if it.content.startswith('Week ') and '[Lecture video]' in it.content:sty='small'
                out.append(self.paragraph(children,sty,bullet))
                self.body_records.append(it.content)
                i+=3;continue
            if typ=='math_block':out.append(Equation(t.content));i+=1;continue
            if typ=='fence':
                out.append(CodeBlock(t.content,t.info.strip()))
                self.code_records.append({'language':t.info,'text':t.content});i+=1;continue
            if typ=='table_open':
                j=i+1
                while tokens[j].type!='table_close':j+=1
                out.append(self.table(tokens[i:j+1]));i=j+1;continue
            if typ in ('bullet_list_open','ordered_list_open'):
                lists.append({'ordered':typ=='ordered_list_open','index':int(t.attrGet('start') or 1)-1,'pending':False})
            elif typ=='list_item_open':
                lists[-1]['index']+=1;lists[-1]['pending']=True
            elif typ in ('bullet_list_close','ordered_list_close'):lists.pop()
            elif typ in ('list_item_close','blockquote_open','blockquote_close','hr'):pass
            else:raise ValueError(f'Unsupported block {typ} {t.content[:60]}')
            i+=1
        return out

class NotesDoc(BaseDocTemplate):
    def __init__(self,path,builder):
        super().__init__(str(path),pagesize=A4,leftMargin=MARGIN,rightMargin=MARGIN,
                         topMargin=MARGIN,bottomMargin=MARGIN,allowSplitting=1,
                         title=f'Day {builder.day:02d} {TITLES[builder.day][0]}',
                         author='Kapil Tripathi study collection',
                         subject='VLSI Design Flow RTL to GDS study notes',
                         pageCompression=1)
        self.builder=builder
        self.current_lesson='Contents and study guide'
        self.page_records=[]
        self._pass=0
        frame=Frame(MARGIN,MARGIN,WIDTH,HEIGHT,id='body',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        self.addPageTemplates(PageTemplate(id='normal',frames=frame,onPage=self.page_start,onPageEnd=self.page_end))
    def beforeDocument(self):
        self._pass+=1
        self.current_lesson='Contents and study guide'
        self.page_records=[]
        self.builder.dest_pages={}
    def page_start(self,c,doc):
        if doc.page==1:
            c.bookmarkPage('contents')
            c.addOutlineEntry('Contents and study guide','contents',0,False)
    def page_end(self,c,doc):
        c.saveState()
        if doc.page>1:
            c.setFont('Book',8.1);c.setFillColor(GRAY)
            c.drawString(MARGIN,PAGE_H-35,f'Day {self.builder.day:02d} | {TITLES[self.builder.day][0]}')
            c.drawRightString(PAGE_W-MARGIN,PAGE_H-35,'RTL to GDS')
            c.setStrokeColor(RULE);c.setLineWidth(.35)
            c.line(MARGIN,PAGE_H-41,PAGE_W-MARGIN,PAGE_H-41)
        c.setStrokeColor(RULE);c.setLineWidth(.35)
        c.line(MARGIN,43,PAGE_W-MARGIN,43)
        c.setFont('Book',8.2);c.setFillColor(GRAY)
        c.drawString(MARGIN,30,f'Day {self.builder.day:02d}  |  Back to contents')
        c.linkRect('','contents',(MARGIN,24,MARGIN+160,40),thickness=0)
        c.drawRightString(PAGE_W-MARGIN,30,str(doc.page))
        c.restoreState()
        self.page_records.append({'page':doc.page,'section':self.current_lesson})
    def afterFlowable(self,f):
        if hasattr(f,'_heading'):
            level,key,title,lesson=f._heading
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title,key,level,False)
            self.builder.dest_pages[key]=self.page
            if level==0:self.current_lesson=title
            if level<=1:
                self.notify('TOCEntry',(level,html.escape(title),self.page,key))

def assembled(day):
    original=(ROOT/'Daily Notes'/f'Day {day:02d}.md').read_text(encoding='utf-8')
    lessons=re.split(r'(?=^## Lesson \d+:)',original,flags=re.M)[1:]
    result=[]
    for lesson in lessons:
        lesson=re.sub(r'^\[Back to (?:lesson|day) index\].*\n?', '',lesson,flags=re.M)
        lesson=re.sub(r'^\[Course index\]\(\.\./README.md\) · ', '',lesson,flags=re.M)
        lesson=re.sub(r' · \[Handwritten index\]\(\.\./Resources/Handwritten%20Index.md\)', '',lesson)
        lesson=re.sub(r' · \[Back to day index\]\([^)]+\)', '',lesson)
        lesson=re.sub(r'^### Lesson \d+ outline\n.*?(?=^### )','',lesson,flags=re.M|re.S)
        result.append(lesson.strip())
    return '\n\n'.join(result)

def front(b):
    day=b.day;title,lessons,scope=TITLES[day]
    flow=[Paragraph(f'Day {day:02d}<br/>{title}',STYLES['title']),
          Paragraph(f'VLSI Design Flow RTL to GDS<br/>{lessons}',STYLES['subtitle']),
          b.simple(scope+'.'),
          b.simple('Contents and bookmarks link to sections; figures and page footers return to contents.','small'),
          b.simple('Course: Prof. Sneh Saurabh, IIIT Delhi, NPTEL. Unix and Tcl tutorials: Jasmine Kaur. Worked examples state their analytical assumptions.','small')]
    toc_heading=ParagraphStyle('contentsheading',parent=STYLES['heading'],keepWithNext=0)
    flow.append(Paragraph('Contents',toc_heading))
    toc=TableOfContents()
    toc.levelStyles=[
        ParagraphStyle('toc0',fontName='Book-Bold',fontSize=10.4,leading=14.4,
                       spaceBefore=7,spaceAfter=3,textColor=DARK,leftIndent=0,rightIndent=26,
                       keepWithNext=1),
        ParagraphStyle('toc1',fontName='Book',fontSize=9.55,leading=12.5,
                       spaceBefore=0,spaceAfter=1.5,textColor=DARK,leftIndent=13,rightIndent=26),
    ]
    toc.dotsMinLevel=0
    flow.append(toc)
    return flow

def backmatter(b):
    flow=[]
    def heading(title,key):
        p=Paragraph(title,STYLES['lesson']);p._heading=(0,key,title,0)
        flow.append(CondPageBreak(340));flow.append(Spacer(1,12));flow.append(p)
    heading('Sources and references','sources-and-study-boundary')
    flow.append(b.simple('Primary course: **VLSI Design Flow: RTL to GDS**, Prof. Sneh Saurabh, IIIT Delhi, NPTEL. Unix and Tcl tutorials: Jasmine Kaur. Lecture captions provide video timestamps. Additional derivations and practice examples are study annotations.'))
    flow.append(b.simple('[Open the course video playlist](https://www.youtube.com/playlist?list=PLyqSpQzTE6M8iOrfy70ELk9W72JG5a98V).'))
    handwritten={1:'Part 1 PDF pages 1 to 16',2:'Part 1 PDF pages 17 to 24 and Part 2 PDF pages 1 to 4',3:'Scan A PDF pages 1 to 14',4:'Scan A PDF pages 15 to 21 (A-21 upper section is discussed with BDDs and its full page appears with SAT)',5:'Scan B PDF pages 1 to 8',6:'Scan B PDF pages 9 to 11'}[b.day]
    flow.append(b.simple(f'Original handwritten sources: **{handwritten}**. Source identifiers are separate from the page numbers of this document.'))
    p=Paragraph('Primary references for the technical clarifications',STYLES['heading'])
    p._heading=(1,'primary-references','Primary references for the technical clarifications',0);flow.append(p)
    # Use the names in the maintained repository source register.
    sources=(ROOT/'Resources/Sources.md').read_text(encoding='utf-8')
    labels={}
    for label,url in re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)',sources):
        labels[url]=label
    for i,url in enumerate(list(b.external),1):
        label=labels.get(url,labels.get(url.split('#')[0],None))
        if not label:
            if 'sutherland-hdl' in url:label='Sutherland HDL - Verilog 2001 reference guide'
            elif 'OpenSTA' in url:label='OpenSTA - Timing analyzer inputs'
            else:label=urlparse(url).netloc+' - technical reference'
        flow.append(b.simple(f'{i}. [{label}]({url})'))
    flow.append(b.simple('Numerical examples use stated teaching assumptions. Technology-specific library values and manufacturing rules require their corresponding source models. Verilog examples use traditional Verilog semantics unless otherwise stated.'))
    # Keep this short reference section intact instead of exporting a final
    # page containing only the last two lines of its explanation.
    return [KeepTogether(flow)] if b.day == 5 else flow

def add_named_destinations(path, dests):
    reader=PdfReader(path)
    writer=PdfWriter()
    writer.clone_document_from_reader(reader)
    for key,page in dests.items():writer.add_named_destination(key,page-1)
    writer.add_named_destination('contents',0)
    writer.page_mode='/UseOutlines'
    temporary=path.with_suffix('.named.pdf')
    with temporary.open('wb') as f:writer.write(f)
    os.replace(temporary,path)

def main():
    saved=QA/'build-manifest.json'
    summary=json.loads(saved.read_text(encoding='utf-8')) if saved.exists() else {}
    days=[int(x) for x in sys.argv[1:]] or [1,2,3,4,5,6]
    for day in days:
        source=assembled(day)
        (CACHE/f'day{day:02d}-assembled.md').write_text(source,encoding='utf-8')
        b=Builder(day,source)
        body=b.blocks(MD.parse(source))
        story=front(b)+body+backmatter(b)
        path=OUT/FILES[day]
        doc=NotesDoc(path,b)
        doc.multiBuild(story,maxPasses=8)
        add_named_destinations(path,b.dest_pages)
        r=PdfReader(path)
        summary[str(day)]={'filename':path.name,'pages':len(r.pages),'figures':b.figure_count,
                          'code_blocks':len(b.code_records),'word_count':len(source.split()),
                          'headings':b.headings,'destinations':b.dest_pages,'figures_detail':b.figure_records,
                          'page_sections':doc.page_records,'passes':doc._pass,
                          'source_sha256':hashlib.sha256((ROOT/'Daily Notes'/f'Day {day:02d}.md').read_bytes()).hexdigest(),
                          'paragraphs':b.body_records,'code':b.code_records}
        saved.write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
        print(f'Day {day:02d}: {len(r.pages)} pages, {b.figure_count} figures, {len(b.code_records)} code blocks, {doc._pass} layout passes',flush=True)
    (QA/'build-manifest.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')

if __name__=='__main__':main()
