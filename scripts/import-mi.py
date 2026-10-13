"""Import supplied HTML content using an archival PDF; leave the quiz engine intact.

Run render-mi-source.cjs first, then use the bundled Python runtime.
Existing records and permanent IDs are retained on every run.
"""
from pathlib import Path
from html.parser import HTMLParser
from xml.sax.saxutils import escape
import hashlib
import json
import re
import shutil
import pymupdf as fitz
from PIL import Image as PILImage
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'CCNA 200-301 Questions - HTML archive.pdf'
HTML = 'CCNA 200-301 Questions.html'

class PlainText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in ('br', 'p', 'div', 'tr', 'pre', 'li'):
            self.parts.append('\n')
        if tag in ('td', 'th'):
            self.parts.append(' | ')
        if tag == 'sup':
            self.parts.append('^')
    def handle_endtag(self, tag):
        if tag in ('p', 'div', 'tr', 'pre', 'li'):
            self.parts.append('\n')
    def handle_data(self, data):
        self.parts.append(data)

def plain(html):
    parser = PlainText()
    parser.feed(html)
    return re.sub(r'\n{3,}', '\n\n', ''.join(parser.parts)).strip()

# Source notes are documentary. The user requests grading all HTML questions
# with the exact answer keys supplied, including these six records.
ISSUES = {
    'ccna-07-mi-q002': ('Both dynamic auto and dynamic desirable can form a trunk with the stated neighbor; the source itself acknowledges this.', 'Les modes dynamic auto et dynamic desirable permettent tous deux de former le Trunk avec le voisin décrit ; la source le reconnaît.'),
    'ccna-11-mi-q003': ('A /27 supports only 30 usable hosts, not 40. All proposed SVI addresses use the network address rather than a usable host address.', 'Un /27 ne fournit que 30 adresses utilisables, pas 40. Les adresses proposées pour la SVI sont des adresses réseau.'),
    'ccna-08-mi-q011': ('Priority 0 is the minimum, but does not guarantee root election if another switch also has priority 0 and a lower MAC address.', 'La priorité 0 est minimale, mais ne garantit pas l’élection si un autre switch utilise la même priorité et une adresse MAC inférieure.'),
    'ccna-08-mi-q013': ('Priority 0 is the minimum, but does not guarantee root election if another switch also has priority 0 and a lower MAC address.', 'La priorité 0 est minimale, mais ne garantit pas l’élection si un autre switch utilise la même priorité et une adresse MAC inférieure.'),
    'ccna-34-mi-q001': ('The exhibit shows 192.168.1.0/26 while its host and gateway belong to 192.168.1.192/26; the source exhibit is inconsistent.', 'Le schéma indique 192.168.1.0/26 alors que l’hôte et la passerelle appartiennent à 192.168.1.192/26 ; la source est incohérente.'),
    'ccna-40-mi-q006': ('The command choice is valid, but the explanation shows 12:00:00 for 12:00 am; midnight should be 00:00:00.', 'La commande sélectionnée est valide, mais l’explication indique 12:00:00 pour minuit, qui devrait être 00:00:00.'),
}

records = json.loads((ROOT / 'tmp/mi-import.json').read_text())
questions = json.loads((ROOT / 'data/questions.json').read_text())
shutil.copyfile(ROOT / 'mi' / HTML, ROOT / 'sources' / HTML)
html_sha = hashlib.sha256((ROOT / 'mi' / HTML).read_bytes()).hexdigest()

# Archive the exact question content and source answer keys. Screenshots are
# embedded unchanged, so the existing pixel-provenance checks remain usable.
pdfmetrics.registerFont(TTFont('Archive', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
styles = getSampleStyleSheet()
for style in styles.byName.values():
    style.fontName = 'Archive'
styles['Normal'].fontSize = 9
styles['Normal'].leading = 13
styles['Heading1'].fontSize = 14
styles['Heading1'].leading = 18
flow = []
def para(value, style='Normal'):
    flow.append(Paragraph(escape(value).replace('\n', '<br/>'), styles[style]))
    flow.append(Spacer(1, 7))
def figure(asset):
    im = PILImage.open(ROOT / asset)
    scale = min(480 / im.width, 610 / im.height)
    flow.append(Image(str(ROOT / asset), width=im.width * scale, height=im.height * scale))
    flow.append(Spacer(1, 8))

for r in records:
    x = r['original']
    para(r['id'] + ' | ' + r['name'], 'Heading1')
    para('Provided HTML: ' + HTML + ' | Question ' + str(r['question']))
    para(plain(x['t']))
    if r['assets'].get('exhibit'):
        figure(r['assets']['exhibit'])
    if 'it' in x:
        para('Items')
        for item in x['it']: para(item)
        para('Categories')
        for category in x['g']: para(category)
        para('Source solution: ' + '; '.join(f'{item} -> {x["g"][x["a"][i]]}' for i, item in enumerate(x['it'])))
    else:
        for i, option in enumerate(x['o']): para(chr(65 + i) + '. ' + option)
        para('Source answers: ' + ', '.join(chr(65 + i) for i in x['c']))
    if x['e']:
        para('Source explanation', 'Heading2')
        para(plain(x['e']))
    if r['assets'].get('explanation'):
        figure(r['assets']['explanation'])
    flow.append(PageBreak())

doc = SimpleDocTemplate(str(ROOT / 'sources' / SOURCE), title='CCNA questions archived from supplied HTML', author='Source archive', leftMargin=42, rightMargin=42, topMargin=40, bottomMargin=40)
doc.build(flow[:-1])
pdf = fitz.open(ROOT / 'sources' / SOURCE)
pages = {}
for i, page in enumerate(pdf):
    match = re.search(r'ccna-\d{2}-mi-q\d{3}', page.get_text())
    if match: pages.setdefault(match[0], i + 1)
sha = hashlib.sha256((ROOT / 'sources' / SOURCE).read_bytes()).hexdigest()
manifest = json.loads((ROOT / 'data/topologies.json').read_text())
added = []
for r in records:
    x = r['original']
    q = dict(id=r['id'], module=r['module'], prompt={'en': plain(x['t'])},
             explanation={'en': plain(x['e'])}, images=[r['assets']['exhibit']] if r['assets'].get('exhibit') else [],
             translationStatus='pending', verified=True,
             source={'file': SOURCE, 'sha256': sha, 'question': r['question'], 'page': pages[r['id']]},
             origin={'file': HTML, 'sha256': html_sha, 'module': r['name'], 'question': r['question']})
    if r['assets'].get('explanation'): q['explanationImages'] = [r['assets']['explanation']]
    if 'it' in x:
        # The existing engine maps each description to a category. A category
        # can be reused: this preserves all many-to-one drag/drop exercises.
        q.update(type='match', options=[{'id': f'o{i+1}', 'text': {'en': s}} for i, s in enumerate(x['g'])],
                 targets=[{'id': f't{i+1}', 'text': {'en': s}} for i, s in enumerate(x['it'])],
                 solution={f't{i+1}': f'o{category+1}' for i, category in enumerate(x['a'])}, required=len(x['it']), answers=[])
    else:
        q.update(type='choice', options=[{'id': chr(97+i), 'text': {'en': s}} for i, s in enumerate(x['o'])],
                 answers=[chr(97+i) for i in x['c']], required=len(x['c']))
    q['originalExtract'] = '\n'.join([q['prompt']['en'], *[o['text']['en'] for o in q['options']], q['explanation']['en']])
    if r['id'] in ISSUES: q['issue'] = dict(zip(('en', 'fr'), ISSUES[r['id']]))
    if not any(old['id'] == q['id'] for old in questions):
        questions.append(q)
        added.append(q)
    else:
        # Rebuilding the derived PDF may change its hash; retain content and IDs.
        old = next(old for old in questions if old['id'] == q['id'])
        old['source'] = q['source']
        old['verified'] = True
    for asset in r['assets'].values():
        im = PILImage.open(ROOT / asset).convert('RGB')
        found = []
        for pi in range(pages[r['id']] - 1, len(pdf)):
            if pi > pages[r['id']] - 1 and re.search(r'ccna-\d{2}-mi-q\d{3}', pdf[pi].get_text()): break
            for b in pdf[pi].get_text('dict')['blocks']:
                if b['type'] != 1: continue
                import io
                original = PILImage.open(io.BytesIO(b['image'])).convert('RGB')
                if original.size == im.size and original.tobytes() == im.tobytes(): found.append((pi, b))
        assert found, asset
        pi, block = found[0]
        manifest[asset] = {'source': SOURCE, 'page': pi + 1, 'bbox': list(block['bbox']), 'pixelSha256': hashlib.sha256(im.tobytes()).hexdigest(), 'origin': HTML}

(ROOT / 'data/questions.json').write_text(json.dumps(questions, ensure_ascii=False, indent=2) + '\n')
(ROOT / 'data/topologies.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
sources = json.loads((ROOT / 'data/sources.json').read_text())
sources = [s for s in sources if s['file'] != SOURCE]
sources.append({'file': SOURCE, 'sha256': sha, 'pages': len(pdf), 'derivedFrom': HTML, 'originalSha256': html_sha, 'modules': sorted({r['module'] for r in records}), 'questions': len(records)})
(ROOT / 'data/sources.json').write_text(json.dumps(sources, ensure_ascii=False, indent=2) + '\n')
print(f'Added {len(added)} questions to {len({q["module"] for q in added})} modules; {len(pdf)} archive pages. Existing content retained.')
