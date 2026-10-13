"""Generate one English question-and-answer PDF per complete source module.

Requires reportlab, Pillow and PyMuPDF (available in the Codex bundled runtime).
Run this script, then node scripts/build.cjs whenever the source bank changes.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import hashlib
import json
import re

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,
    Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'assets/pdf'
DEST.mkdir(parents=True, exist_ok=True)
questions = json.loads((ROOT / 'data/questions.json').read_text())
modules = json.loads(__import__('subprocess').check_output(
    ['node', '-e', "process.stdout.write(JSON.stringify(require('./scripts/catalog.cjs')))"], cwd=ROOT))
for name, file in [('Body', 'DejaVuSans.ttf'), ('Bold', 'DejaVuSans-Bold.ttf'), ('Mono', 'DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name, '/usr/share/fonts/truetype/dejavu/' + file))
pdfmetrics.registerFontFamily('Body', normal='Body', bold='Bold', italic='Body', boldItalic='Bold')
TEAL = colors.HexColor('#0E7C86')
WIDTH = A4[0] - 84
styles = {
    'body': ParagraphStyle('body', fontName='Body', fontSize=9, leading=12.5, spaceAfter=6),
    'title': ParagraphStyle('title', fontName='Bold', fontSize=21, leading=27, textColor=TEAL, spaceAfter=14),
    'question': ParagraphStyle('question', fontName='Bold', fontSize=15, leading=20, textColor=TEAL, spaceAfter=10),
    'label': ParagraphStyle('label', fontName='Bold', fontSize=10, leading=14, textColor=TEAL, spaceBefore=8, spaceAfter=6, keepWithNext=True),
    'small': ParagraphStyle('small', fontName='Body', fontSize=7.5, leading=10.5, textColor=colors.HexColor('#526670'), spaceAfter=6),
    'code': ParagraphStyle('code', fontName='Mono', fontSize=8, leading=11.5, spaceAfter=6),
}

def paragraph(text, style='body'):
    # Preserve source text, case, commands and explicit newlines. Only escape
    # XML markup for ReportLab; never substitute translations or new answers.
    return Paragraph(escape(text).replace('\n', '<br/>'), styles[style])

def complete(q):
    if not q.get('prompt', {}).get('en') or not q.get('options'):
        return False
    options = {o['id']: o.get('text', {}).get('en') for o in q['options']}
    if not all(options.values()):
        return False
    if q['type'] == 'match':
        return bool(q.get('targets')) and all(
            t.get('text', {}).get('en') and q.get('solution', {}).get(t['id']) in options
            for t in q['targets'])
    return bool(q.get('answers')) and all(a in options for a in q['answers'])

def append_image(story, asset):
    with PILImage.open(ROOT / asset) as im:
        scale = min(WIDTH / im.width, 340 / im.height)
        story.append(Image(str(ROOT / asset), width=im.width * scale, height=im.height * scale))
    story.append(Spacer(1, 7))

def answer_table(story, rows):
    table = Table([[paragraph(c) for c in row] for row in rows],
                  colWidths=[WIDTH * .52, WIDTH * .48], repeatRows=1, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E6F2F3')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F8F9')]),
        ('LINEBELOW', (0, 0), (-1, -1), .35, colors.HexColor('#DCE5E8')),
        ('LEFTPADDING', (0, 0), (-1, -1), 9), ('RIGHTPADDING', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(table)

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor('#DCE5E8'))
    canvas.line(42, 36, A4[0] - 42, 36)
    canvas.setFont('Body', 7)
    canvas.setFillColor(colors.HexColor('#526670'))
    canvas.drawString(42, 24, 'CCNA 200-301 | Questions and answers | Original English')
    canvas.drawRightString(A4[0] - 42, 24, str(doc.page))
    canvas.restoreState()

manifest = {'schemaVersion': 1,
            'bankSha256': hashlib.sha256((ROOT / 'data/questions.json').read_bytes()).hexdigest(),
            'modules': {}}
for module in modules:
    # Within a source, use its original question numbers, never session order.
    qs = sorted((q for q in questions if q['module'] == module['id']),
                key=lambda q: (q['source']['file'], q['source']['question']))
    if not qs or not all(complete(q) for q in qs):
        continue
    story = [paragraph('CCNA 200-301', 'small'), paragraph(module['name']['en'], 'title'),
             paragraph(f'{len(qs)} questions | Original English questions and source answers', 'small'), Spacer(1, 10)]
    for index, q in enumerate(qs):
        if index:
            story.append(PageBreak())
        story.append(paragraph(f"Question {q['source']['question']}", 'question'))
        story.append(paragraph(q['prompt']['en']))
        for asset in q.get('images', []):
            append_image(story, asset)
        options = {o['id']: o['text']['en'] for o in q['options']}
        if q['type'] == 'match':
            story.append(paragraph('Available items', 'label'))
            for o in q['options']:
                story.append(paragraph(o['text']['en'], 'code' if o['text']['en'].startswith(('ip ', 'switchport ')) else 'body'))
            story.append(paragraph('Descriptions / target positions', 'label'))
            for target in q['targets']:
                story.append(paragraph(target['text']['en']))
            story.append(paragraph('Answer', 'label'))
            answer_table(story, [['Description / position', 'Source answer']] + [
                [t['text']['en'], options[q['solution'][t['id']]]] for t in q['targets']])
            unused = [o['text']['en'] for o in q['options'] if o['id'] not in q['solution'].values()]
            if unused:
                story.append(paragraph('Unused items', 'label'))
                for item in unused:
                    story.append(paragraph(item))
        else:
            story.append(paragraph('Options', 'label'))
            for o in q['options']:
                text = o['text']['en']
                code = bool(re.search(r'^(?:.*[>#]|interface |ip |switchport |access-list |no |config t)', text, re.M))
                story.append(paragraph(f"{o['id'].upper()}. {text}", 'code' if code else 'body'))
            story.append(paragraph('Answer', 'label'))
            for answer in q['answers']:
                story.append(paragraph(f'{answer.upper()}. {options[answer]}'))
        explanation = q.get('explanation', {}).get('en', '')
        if explanation:
            story.append(paragraph('Source explanation', 'label'))
            for block in re.split(r'\n\s*\n', explanation):
                if block.strip():
                    story.append(paragraph(block))
        for asset in q.get('explanationImages', []):
            append_image(story, asset)
        source = q.get('origin', q['source'])
        citation = paragraph(f"Source: {source['file']} | Question {source['question']}", 'small')
        story.append(KeepTogether([story.pop(), citation]))
    dest = DEST / (module['id'] + '.pdf')
    doc = SimpleDocTemplate(str(dest), pagesize=A4, leftMargin=42, rightMargin=42, topMargin=42, bottomMargin=48,
                            title=module['name']['en'] + ' - Questions and answers', author='CCNA Training Lab')
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    manifest['modules'][module['id']] = {
        'path': 'assets/pdf/' + dest.name,
        'sha256': hashlib.sha256(dest.read_bytes()).hexdigest(),
        'questionIds': [q['id'] for q in qs], 'language': 'en',
    }
    print(module['id'], len(qs), 'questions', flush=True)
(ROOT / 'data/module-pdfs.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print('Generated', len(manifest['modules']), 'English module PDFs.')
