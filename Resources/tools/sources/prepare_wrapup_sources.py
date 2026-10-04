"""Preserve the October source uploads and prepare their portable page images."""
import sys
if "--apply-historical-import" not in sys.argv:
    raise SystemExit("Historical import only. Read Resources/tools/sources/README.md before using --apply-historical-import.")

from pathlib import Path
import json, hashlib, shutil, sys
ROOT = Path(__file__).resolve().parents[3]
QA = ROOT / 'Resources/tools/pdf/qa/incoming'
DATA = ROOT / 'Resources/Data'
SOURCES = ROOT / 'Resources/sources/handwritten'
sys.path.insert(0, str(Path(__file__).parent.parent / 'pdf/vendor'))
from pypdf import PdfReader

names = {
    'C': 'Scan-C-Constraints-Mapping-Power-and-DFT.pdf',
    'D': 'Scan-D-Scan-ATPG-BIST-and-Physical-Design.pdf',
    'E': 'Scan-E-Placement-CTS-Routing-and-Signoff.pdf',
    'N': 'Notebook-ATPG-Backtracking-and-Redundant-Faults.pdf',
}
records = []
for item in json.loads((QA / 'source-manifest.json').read_text('utf8')):
    key = item['key']
    original = ROOT / item['name']
    dest = DATA / names[key]
    if original.exists():
        assert not dest.exists(), dest
        digest = hashlib.sha256(original.read_bytes()).hexdigest()
        original.rename(dest)
        assert not original.exists() and hashlib.sha256(dest.read_bytes()).hexdigest() == digest
    else:
        assert dest.exists(), dest
        digest = hashlib.sha256(dest.read_bytes()).hexdigest()
    assert len(PdfReader(dest).pages) == item['pages']
    folder = SOURCES / ('notebook-atpg' if key == 'N' else f'scan-{key.lower()}')
    folder.mkdir(parents=True, exist_ok=True)
    images = sorted((QA / key).glob('page-*.jpg'))
    assert len(images) == item['pages']
    for i, image in enumerate(images, 1):
        target = folder / f'h{i:02d}.jpg'
        shutil.copyfile(image, target)
    records.append(dict(item, path=dest.relative_to(ROOT).as_posix(), sha256=digest,
                        image_folder=folder.relative_to(ROOT).as_posix()))
(ROOT / 'Resources/sources/october-source-register.json').write_text(
    json.dumps(records, ensure_ascii=False, indent=2) + '\n', 'utf8')
deck_folder = ROOT / 'Resources/sources/lectures/week12'
deck_folder.mkdir(parents=True, exist_ok=True)
for name in ['lecture-40.pdf', 'lecture-41.pdf', 'lecture-42.pdf', 'tutorial-12.pdf']:
    source = Path('C:/Users/kapil/Downloads') / name
    assert source.exists(), source
    shutil.copyfile(source, deck_folder / name)
print('Preserved 68 source pages and the four official week-12 decks.')
