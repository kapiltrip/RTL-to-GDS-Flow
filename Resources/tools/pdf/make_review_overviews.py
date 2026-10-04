"""Build compact visual-review sheets from the final rendered pages."""
from pathlib import Path
import json, sys
from PIL import Image, ImageDraw, ImageFont
HERE=Path(__file__).resolve().parent
QA=HERE/'qa'
manifest=json.loads((QA/'build-manifest.json').read_text(encoding='utf-8'))
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
for day in ([int(x) for x in sys.argv[1:]] or range(1,10)):
    count=manifest[str(day)]['pages']
    pages=sorted((QA/f'day{day:02d}-pages-{count}').glob('page-*.png'))
    assert len(pages)==count,(day,len(pages),count)
    for offset in range(0,count,12):
        sheet=Image.new('RGB',(2000,2190),'#D9D9D9');draw=ImageDraw.Draw(sheet)
        for j,p in enumerate(pages[offset:offset+12]):
            with Image.open(p) as raw:im=raw.convert('RGB')
            im.thumbnail((480,685))
            x=10+(j%4)*500;y=30+(j//4)*730
            sheet.paste(im,(x,y))
            draw.text((x,y-25),f'Day {day:02d}   page {offset+j+1}',font=font,fill='black')
        sheet.save(QA/f'review-day{day:02d}-{offset//12+1:02d}.jpg',quality=93)
    print(f'Day {day:02d}: {count} pages ready for visual review.')
