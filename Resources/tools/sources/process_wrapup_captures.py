"""Historical October import: crop actual Chrome lecture player rectangles."""
import sys
if "--apply-historical-import" not in sys.argv:
    raise SystemExit("Historical import only. Read Resources/tools/sources/README.md before using --apply-historical-import.")

from pathlib import Path
import hashlib, json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
path = ROOT / 'Resources/sources/wrapup-captures.json'
records = json.loads(path.read_text(encoding='utf-8'))
for record in records:
    image = Image.open(ROOT / record['raw_path']).convert('RGB')
    rect = record['clip']
    box = tuple(round(x) for x in (rect['x'], rect['y'], rect['x']+rect['width'], rect['y']+rect['height']))
    assert 0 <= box[0] < box[2] <= image.width and 0 <= box[1] < box[3] <= image.height, (record, image.size)
    image.crop(box).save(ROOT / record['path'], quality=95)
    record['sha256'] = hashlib.sha256((ROOT / record['path']).read_bytes()).hexdigest()
    record['url'] = f'https://www.youtube.com/watch?v={record["id"]}&t={record["time_seconds"]}s'
path.write_text(json.dumps(records, indent=2), encoding='utf-8')
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
qa=ROOT/'Resources/tools/pdf/qa'
for offset in range(0,len(records),4):
    sheet=Image.new('RGB',(2200,1400),'#EEEEEE')
    draw=ImageDraw.Draw(sheet)
    for j, record in enumerate(records[offset:offset+4]):
        im=Image.open(ROOT/record['path']); im.thumbnail((1060,630))
        x=20+(j%2)*1100; y=50+(j//2)*700
        sheet.paste(im,(x,y))
        draw.text((x,y-30),f'Lesson {record["lesson"]} | {record["time_seconds"]//60}:{record["time_seconds"]%60:02d}',font=font,fill='black')
    sheet.save(qa/f'wrapup-frames-{offset//4+1:02d}.jpg',quality=92)
print(f'Prepared {len(records)} verified lecture crops.')
