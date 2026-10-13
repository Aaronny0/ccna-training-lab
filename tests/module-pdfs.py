"""Verify every exported instruction, choice, answer and source order."""
import hashlib
import json
import re
from pathlib import Path
import pymupdf as fitz

root = Path(__file__).resolve().parents[1]
questions = json.loads((root / 'data/questions.json').read_text())
manifest = json.loads((root / 'data/module-pdfs.json').read_text())
assert manifest['bankSha256'] == hashlib.sha256((root / 'data/questions.json').read_bytes()).hexdigest()
normalize = lambda s: re.sub(r'\s+', '', s)
count = 0
for module, item in manifest['modules'].items():
    qs = sorted([q for q in questions if q['module'] == module], key=lambda q: (q['source']['file'], q['source']['question']))
    assert item['questionIds'] == [q['id'] for q in qs]
    path = root / item['path']
    assert item['sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert item['language'] == 'en'
    pdf = fitz.open(path)
    chunks = []
    for page in pdf:
        for block in page.get_text('dict')['blocks']:
            if block['type'] != 0:
                continue
            for line in block['lines']:
                if line['bbox'][1] > page.rect.height - 45:
                    continue
                text = ''.join(s['text'] for s in line['spans'])
                is_question = bool(re.fullmatch(r'Question \d+', text)) and any(abs(s['size'] - 15) < .1 for s in line['spans'])
                if is_question:
                    chunks.append([text, ''])
                elif chunks:
                    chunks[-1][1] += text + '\n'
                for span in line['spans']:
                    assert span['bbox'][0] >= 40 and span['bbox'][2] <= page.rect.width - 40, (module, span['text'])
    assert len(chunks) == len(qs), module
    for q, (heading, text) in zip(qs, chunks):
        assert heading == 'Question ' + str(q['source']['question'])
        body = normalize(text)
        for source in [q['prompt']['en'], *[o['text']['en'] for o in q['options']], *[t['text']['en'] for t in q.get('targets', [])], q.get('explanation', {}).get('en', '')]:
            assert normalize(source) in body, (q['id'], source[:120])
        answer = text.split('\nAnswer\n', 1)[1]
        if q['type'] == 'match':
            by_id = {o['id']: o['text']['en'] for o in q['options']}
            expected = [t['text']['en'] + by_id[q['solution'][t['id']]] for t in q['targets']]
            normalized = normalize(answer)
            offset = 0
            for pair in expected:
                offset = normalized.index(normalize(pair), offset) + len(normalize(pair))
        else:
            for value in q['answers']:
                correct = next(o['text']['en'] for o in q['options'] if o['id'] == value)
                assert normalize(value.upper() + '. ' + correct) in normalize(answer)
        count += 1
assert count == len(questions)
assert set(manifest['modules']) == {q['module'] for q in questions}
assert len(list((root / 'assets/pdf').glob('*.pdf'))) == len(manifest['modules'])
print(f'{len(manifest["modules"])} unique English PDFs: all {count} questions, source options, answer associations, explanations and order verified.')
