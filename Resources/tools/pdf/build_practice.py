"""Make two self-contained, score-only practice files with no displayed answers."""
from pathlib import Path
from xml.etree import ElementTree as ET
import base64,hashlib,html,json,re,zipfile
from weekly_common import (ROOT,HERE,QA,PDF_NAMES,HTML_NAMES,LICENSE,clean,load_banks,figure_path,math_latex)
from build_notes import math_asset

def math_image(latex):
    path,w,h,d=math_asset(latex,12)
    data=base64.b64encode(Path(path).read_bytes()).decode()
    return f'<img class="inline-math" src="data:image/png;base64,{data}" style="width:{w:.2f}pt;height:{h:.2f}pt" alt="{html.escape(latex,quote=True)}">'

def parts_html(parts):
    out=[]
    for part in parts:
        kind=part['type']
        if kind=='text':out.append(html.escape(clean(part['text'])).replace('\n','<br>'))
        elif kind=='code':out.append('<code>'+html.escape(clean(part['text']))+'</code>')
        elif kind=='image':
            path=figure_path(part['url']);data=base64.b64encode(path.read_bytes()).decode()
            out.append('<img class="figure" src="data:image/png;base64,'+data+'" alt="Original NPTEL question figure">')
        elif kind=='latex':out.append(math_image(part['text']))
        elif kind=='mathml':
            # Only mathematical markup is emitted; event handlers and unrelated tags are not copied.
            math=ET.fromstring(part['html'])
            allowed={'math','mrow','mi','mn','mo','msub','msup','msubsup','mfrac','msqrt','mover','munder','mtext','mspace','mfenced'}
            def emit(e):
                tag=e.tag.rsplit('}',1)[-1];assert tag in allowed,tag
                return '<'+tag+(' xmlns="http://www.w3.org/1998/Math/MathML"' if tag=='math' else '')+'>'+html.escape(clean(e.text or ''))+''.join(emit(c)+html.escape(clean(c.tail or '')) for c in e)+'</'+tag+'>'
            out.append(emit(math))
        else:raise ValueError(kind)
    text=re.sub(r'(?:<br>\s*){3,}','<br><br>',''.join(out)).strip()
    return re.sub(r'^(?:<br>\s*)+|(?:\s*<br>)+$','',text)

def build(kind):
    weeks=[]
    for week in load_banks(kind):
        questions=[]
        for q in week['questions']:
            prompt=parts_html(q['parts']) if kind=='original' else html.escape(clean(q['text'])).replace('\n','<br>')
            options=[parts_html(p) for p in q['optionParts']] if kind=='original' else [html.escape(clean(o)) for o in q['options']]
            questions.append({'number':q['number'],'prompt':prompt,'options':options,'salt':q['salt'],'answerHash':q['answerHash']})
        weeks.append({'week':week['week'],'topic':week['topic'],'questions':questions})
    title='Original course questions' if kind=='original' else 'Practice MCQs - 50 per week'
    subtitle='120 original questions, July-October 2026' if kind=='original' else '600 newly authored practice questions'
    provenance=('Original question wording, option order and figures: NPTEL / Prof. Sneh Saurabh, IIIT Delhi, VLSI Design Flow: RTL to GDS, noc26_ee147. '
        f'<a href="{LICENSE}">CC BY-NC-SA 4.0</a>. Prior selections and grading feedback removed; mathematical formatting preserved. '
        'This is an independent question-only adaptation.' if kind=='original' else
        'Newly authored questions aligned with the <a href="https://nptel.ac.in/courses/108106191">official NPTEL course</a> and the saved lecture notes. '
        'These are not verified past exam questions. No promise is made that a question will appear in an examination.')
    version=hashlib.sha256(json.dumps(weeks,sort_keys=True).encode()).hexdigest()[:14]
    bank=json.dumps({'kind':kind,'version':version,'weeks':weeks},ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    template=(HERE/'practice_template.html').read_text(encoding='utf-8')
    for key,value in {'TITLE':title,'SUBTITLE':subtitle,'PROVENANCE':provenance,'BANK':bank}.items():template=template.replace('__'+key+'__',value)
    path=ROOT/'Assignments/Practice'/HTML_NAMES[kind];path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(template,encoding='utf-8')
    assert not re.search(r'acceptedIndex|acceptedPrivate|Accepted answer is|Yes, the answer is correct',template)
    print(f'{path.name}: {sum(len(w["questions"]) for w in weeks)} questions; offline score-only practice.',flush=True)

if __name__=='__main__':
    for kind in ('original','practice'):build(kind)
    folder=ROOT/'Assignments/Practice'
    with zipfile.ZipFile(folder/'Browser Practice - All Weeks.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name in HTML_NAMES.values():archive.write(folder/name,arcname=name)
