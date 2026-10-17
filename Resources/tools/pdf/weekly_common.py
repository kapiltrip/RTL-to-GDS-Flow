"""Shared source handling for the weekly revision and unanswered assessments."""
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET
import hashlib, html, json, re, unicodedata

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DATA=ROOT/'Resources/weekly'
QA=HERE/'qa/weekly'
QA.mkdir(parents=True,exist_ok=True)
TOPICS={
1:'IC foundations and pre-RTL design',2:'Implementation, verification, manufacturing and Tcl',
3:'Verilog, simulation and high-level synthesis',4:'RTL synthesis and two-level logic optimization',
5:'Multi-level optimization, FSMs, BDDs and SAT',6:'Formal verification, equivalence and cell libraries',
7:'Static timing analysis and OpenSTA',8:'Constraints, technology mapping and timing optimization',
9:'Power analysis and scan-based test',10:'ATPG, BIST and physical-design foundations',
11:'Chip planning, power delivery and placement',12:'Clock trees, routing, extraction and signoff'}
PDF_NAMES={'original':'Original Course Questions - Weeks 01 to 12.pdf',
           'practice':'Practice MCQs - 50 per Week.pdf'}
HTML_NAMES={'original':'original-course.html','practice':'possible-mcqs.html'}
LICENSE='https://creativecommons.org/licenses/by-nc-sa/4.0/'

def clean(value):
    value=unicodedata.normalize('NFKC',value)
    value=value.replace('don\ufffdt',"don't").replace('\ufffd','"')
    for char in ('\u2011','\u2013','\u2014'):value=value.replace(char,'-')
    return value.replace('\u2061','').replace('\u2062','').replace('\xa0',' ')

def math_latex(value):
    root=ET.fromstring(value)
    def node(e):
        name=e.tag.rsplit('}',1)[-1]
        children=list(e)
        if name in ('mi','mn','mo','mtext'):
            text=clean(''.join(e.itertext())).strip()
            replacements={'\u2032':r'\prime','\u2264':r'\leq ','\u2265':r'\geq ',
                          '\u2260':r'\ne ','\u00ac':r'\neg ','\u2227':r'\wedge ',
                          '\u2228':r'\vee ','\u2192':r'\to ','\u22c5':r'\cdot ',
                          '{':r'\{','}':r'\}'}
            return ''.join(replacements.get(c,c) for c in text)
        if name=='msub':return node(children[0])+'_{'+node(children[1])+'}'
        if name=='msup':return node(children[0])+'^{'+node(children[1])+'}'
        if name=='msubsup':return node(children[0])+'_{'+node(children[1])+'}^{'+node(children[2])+'}'
        if name=='mfrac':return r'\frac{'+node(children[0])+'}{'+node(children[1])+'}'
        if name=='mover':return r'\overline{'+node(children[0])+'}'
        if name=='msqrt':return r'\sqrt{'+''.join(node(c) for c in children)+'}'
        return ''.join(node(c) for c in children)
    return node(root)

def prepare_original_checks():
    """Store comparison digests only; source answer indices stay in ignored work."""
    for week in range(1,13):
        path=DATA/f'Week {week:02d}'/'original.json'
        data=json.loads(path.read_text(encoding='utf-8'))
        private=ROOT/'.work/weekly-grading'/f'week{week:02d}-original.json'
        if private.exists():
            accepted=json.loads(private.read_text(encoding='utf-8'))['questions']
            for q,reference in zip(data['questions'],accepted):
                assert q['number']==reference['number'] and q['options']==reference['options']
                index=reference['acceptedIndex'];assert 0<=index<len(q['options'])
                salt=hashlib.sha256(f'original-{week}-{q["number"]}'.encode()).hexdigest()[:16]
                q['salt']=salt
                q['answerHash']=hashlib.sha256(f'{salt}:{index}'.encode()).hexdigest()
            path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
        assert all(q.get('answerHash') for q in data['questions']),f'Grading reference missing: {path}'

def load_banks(kind):
    weeks=[]
    for week in range(1,13):
        data=json.loads((DATA/f'Week {week:02d}'/f'{kind}.json').read_text(encoding='utf-8'))
        assert data['week']==week
        assert len(data['questions'])==(10 if kind=='original' else 50)
        for q in data['questions']:
            assert all(q['options']) and len(set(q['options']))==len(q['options'])
            assert not set(q)&{'acceptedIndex','acceptedPrivate','correct','answer','selected','score'}
        data['topic']=TOPICS[week];weeks.append(data)
    return weeks

def figure_path(url):
    records=json.loads((DATA/'figures.json').read_text(encoding='utf-8'))
    lookup={r['url']:r for r in records}
    record=lookup[url];path=ROOT/record['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256']
    return path

def plain_parts(parts):
    values=[]
    for part in parts:
        if part['type'] in ('text','code'):values.append(clean(part['text']))
        elif part['type']=='latex':values.append('$'+part['text']+'$')
        elif part['type']=='mathml':values.append('$'+math_latex(part['html'])+'$')
    return ''.join(values)

def markup(parts,math_renderer):
    values=[]
    for part in parts:
        kind=part['type']
        if kind=='text':values.append(html.escape(clean(part['text'])))
        elif kind=='code':values.append('<font name="Code" size="9.2">'+html.escape(clean(part['text']))+'</font>')
        elif kind in ('latex','mathml'):
            latex=part['text'] if kind=='latex' else math_latex(part['html'])
            values.append(math_renderer(latex))
        else:raise ValueError(kind)
    text=''.join(values)
    text=re.sub(r'[ \t]+',' ',text)
    text=re.sub(r' *\n *','\n',text).strip()
    return re.sub(r'\n{3,}','\n\n',text)
