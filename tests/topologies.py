from pathlib import Path
import json,io,hashlib
from PIL import Image
import pymupdf as fitz
root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'data/topologies.json').read_text());qs=json.loads((root/'data/questions.json').read_text());count=0
for q in qs:
 for path in q.get('images',[])+q.get('explanationImages',[]):
  m=manifest[path];pg=fitz.open(root/'sources'/m['source'])[m['page']-1];im=Image.open(root/path)
  if m.get('renderScale'):
   pix=pg.get_pixmap(matrix=fitz.Matrix(m['renderScale'],m['renderScale']),clip=fitz.Rect(m['bbox']))
   assert hashlib.sha256(pix.samples).hexdigest()==m['pixelSha256'],path
   assert im.tobytes()==pix.samples,path
  else:
   candidates=[b for b in pg.get_text('dict')['blocks'] if b['type']==1 and list(b['bbox'])==m['bbox']]
   assert candidates,path
   original=Image.open(io.BytesIO(candidates[0]['image']))
   assert im.size==original.size and im.tobytes()==original.tobytes(),path
  assert m['source']==q['source']['file'],(q['id'],'wrong source diagram')
  count+=1
print(f'{count} referenced exhibits match source pixels/render exactly. Equipment and geometry unchanged.')
