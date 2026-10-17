"""Prove every inventoried handwritten page is embedded at its PDF destination."""
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE / 'vendor'))
from pypdf import PdfReader


def embedded_jpegs(resources):
    """Read actual image streams; convenience image exports can recompress JPEGs."""
    for reference in resources.get('/XObject', {}).values():
        obj = reference.get_object()
        if obj.get('/Subtype') == '/Image':
            filters = obj.get('/Filter', [])
            filters = [filters] if isinstance(filters, str) else filters
            if '/DCTDecode' in filters:
                yield hashlib.sha256(obj.get_data()).hexdigest()
        elif obj.get('/Subtype') == '/Form':
            yield from embedded_jpegs(obj.get('/Resources', {}))


def main():
    inventory = json.loads((ROOT / 'Resources/sources/handwritten-inventory.json').read_text(encoding='utf-8'))
    expected = {}
    for original in inventory['originals']:
        for page in original['page_images']:
            expected[page['path']] = {**page, 'source': original['source']}
    manifest = json.loads((HERE / 'qa/build-manifest.json').read_text(encoding='utf-8'))
    verified = {}
    per_day = {}
    for day in range(1, 10):
        record = manifest[str(day)]
        path = ROOT / 'PDFs' / record['filename']
        reader = PdfReader(path)
        names = reader.named_destinations
        assert 'handwritten-page-finder' in names, path
        assert 'revision-route' in names, path
        assert 'revision-checks-and-explained-answers' in names, path
        source = ROOT / 'Resources/Daily Notes' / f'Day {day:02d}.md'
        assert hashlib.sha256(source.read_bytes()).hexdigest() == record['source_sha256'], source
        cache = {}
        for original in record['handwritten_pages']:
            image_path = original['path']
            assert image_path in expected and image_path not in verified, image_path
            entry = expected[image_path]
            assert (entry['source'], entry['pdf_page']) == (original['source'], original['pdf_page'])
            source_image = ROOT / image_path
            assert hashlib.sha256(source_image.read_bytes()).hexdigest() == entry['sha256'], source_image
            page_number = reader.get_destination_page_number(names[original['key']])
            if page_number not in cache:
                cache[page_number] = set(embedded_jpegs(reader.pages[page_number]['/Resources']))
            assert entry['sha256'] in cache[page_number], (path.name, page_number + 1, 'Exact original JPEG absent', image_path)
            verified[image_path] = {'day': day, 'pdf_page': page_number + 1,
                                    'source': entry['source'], 'original_page': entry['pdf_page'],
                                    'destination': original['key']}
        per_day[str(day)] = len(record['handwritten_pages'])
        print(f'Day {day:02d}: {per_day[str(day)]} complete original pages verified byte for byte in embedded image streams.', flush=True)
    assert set(verified) == set(expected), sorted(set(expected) - set(verified))
    assert len(verified) == inventory['readable_pages'] == 128
    assert list(per_day.values()) == [16, 12, 14, 7, 8, 15, 17, 17, 22], per_day
    result = {'verified_original_pages': len(verified), 'per_day': per_day,
              'method': 'Original JPEG bytes matched the actual embedded DCT streams on named PDF destination pages; no resizing or recompression.',
              'pdf_sha256': {m['filename']: hashlib.sha256((ROOT / 'PDFs' / m['filename']).read_bytes()).hexdigest()
                             for m in manifest.values()}, 'pages': verified}
    (HERE / 'qa/handwriting-embedded.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print('PASS: all 128 complete handwritten pages are embedded in the nine daily PDFs; no external-file dependency for reading them.')


if __name__ == '__main__':
    main()
