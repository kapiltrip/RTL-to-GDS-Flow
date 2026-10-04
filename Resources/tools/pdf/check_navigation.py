"""Check bookmark targets and clickable regions on every figure and footer."""
from pathlib import Path
import json, hashlib, sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'vendor'))
import pdfplumber
from pypdf import PdfReader

QA=HERE/'qa'
manifest=json.loads((QA/'build-manifest.json').read_text(encoding='utf-8'))
results=json.loads((QA/'navigation-detail.json').read_text(encoding='utf-8')) if (QA/'navigation-detail.json').exists() else {}
selected=sys.argv[1:] or list(manifest)

for day in selected:
    m=manifest[day]
    path=HERE.parents[2]/'PDFs'/m['filename']
    reader=PdfReader(path)
    first=reader.pages[0].indirect_reference
    def contents_link(annotation):
        dest=annotation.get('/Dest')
        if isinstance(dest,str):
            return dest in reader.named_destinations and reader.get_destination_page_number(reader.named_destinations[dest])==0
        return isinstance(dest,list) and dest[0]==first
    def bookmarks(items):
        for item in items:
            if isinstance(item,list):yield from bookmarks(item)
            else:yield str(item.title),reader.get_destination_page_number(item)+1
    actual=set(bookmarks(reader.outline))
    for heading in m['headings']:
        assert (heading['title'],m['destinations'][heading['key']]) in actual,heading
    figures=footers=0
    with pdfplumber.open(path) as pdf:
        for number,(page,native) in enumerate(zip(pdf.pages,reader.pages),1):
            links=[a.get_object() for a in native.get('/Annots',[]) if contents_link(a.get_object())]
            def enclosed(rect):
                x0,y0,x1,y1=rect
                return any(float(a['/Rect'][0])<=x0+.5 and float(a['/Rect'][1])<=y0+.5
                           and float(a['/Rect'][2])>=x1-.5 and float(a['/Rect'][3])>=y1-.5 for a in links)
            # Inline equation rasters are small; source figures occupy larger
            # rectangles. The exact total is checked against the builder.
            for picture in page.images:
                if picture['width']>100 and picture['height']>35:
                    assert enclosed((picture['x0'],picture['y0'],picture['x1'],picture['y1'])),(day,number,'Unlinked figure')
                    figures+=1
            assert enclosed((57,24,210,40)),(day,number,'Unlinked footer')
            footers+=1
    assert figures==m['figures'],(day,figures,m['figures'])
    results[day]={'pages':len(reader.pages),'figure_backlinks':figures,'footer_backlinks':footers,
                  'headings_with_verified_bookmarks':len(m['headings']),
                  'pdf_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
(QA/'navigation-detail.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(f'PASS: {sum(x["figure_backlinks"] for x in results.values())} figure regions, '
      f'{sum(x["footer_backlinks"] for x in results.values())} footer regions and '
      f'{sum(x["headings_with_verified_bookmarks"] for x in results.values())} heading bookmarks in all {len(results)} PDFs.')
