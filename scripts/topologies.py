"""Preserve source pixels and document geometry. Never redraw network topologies."""
from pathlib import Path
import json,hashlib,re,io
import pymupdf as fitz
from PIL import Image
root=Path(__file__).resolve().parents[1];qs=json.loads((root/'data/questions.json').read_text());manifest={}
for info in json.loads((root/'data/sources.json').read_text()):
 if info.get('duplicate') or info.get('scanned'):continue
 doc=fitz.open(root/'sources'/info['file']);current=0;n=0;end=False
 for pi,pg in enumerate(doc):
  for b in pg.get_text('dict',sort=True)['blocks']:
   if b['type']==1 and current and not end:
    n+=1;name=f'{info["module"]}-q{current}-{n}.png';path=root/'assets'/name
    if not path.exists():continue
    raw=b['image'];im=Image.open(io.BytesIO(raw));im.save(path,'PNG')
    manifest['assets/'+name]={'source':info['file'],'page':pi+1,'bbox':b['bbox'],'method':'embedded image: original pixels, lossless PNG container','size':list(im.size),'pixelSha256':hashlib.sha256(im.tobytes()).hexdigest()}
   if b['type']==0:
    for l in b.get('lines',[]):
     text=''.join(s['text'] for s in l['spans']).strip()
     if re.match(r'Comments \(\d+\)',text) or text=='Add a Comment':end=True
     m=re.fullmatch(r'Question (\d+)',text)
     if m and not end:current=int(m[1])
  if end:break
# Scanned exhibits: copy original pixel region; add margins on all sides.
for id,name,pi,box in [('ccna-38-q008','DHCP Quiz',4,(.025,.827,.94,.912)),('ccna-35-q005','Drag Drop Quiz 2',4,(.025,.402,.96,.488)),('ccna-35-q010','Drag Drop Quiz 2',8,(.04,.142,.80,.568))]:
 d=fitz.open(root/'sources'/('CCNA Training » '+name+'.pdf'));pg=d[pi-1]
 w,h=pg.rect.width,pg.rect.height
 rect=fitz.Rect(box[0]*w,box[1]*h,box[2]*w,box[3]*h)
 pix=pg.get_pixmap(matrix=fitz.Matrix(3,3),clip=rect)
 path='assets/'+id+'-exhibit.png';pix.save(root/path)
 byq=next(q for q in qs if q['id']==id);byq['images']=[path]
 manifest[path]={'source':'CCNA Training » '+name+'.pdf','page':pi,'bbox':list(rect),'renderScale':3,'method':'direct PDF rendering of original exhibit, unchanged geometry, full labels with margins','size':[pix.width,pix.height],'pixelSha256':hashlib.sha256(pix.samples).hexdigest()}

for q in qs:
 for key in ['images','explanationImages']:
  q[key]=[p for p in q.get(key,[]) if p in manifest and manifest[p]['size'][0]>70]
 q['topologyStatus']='original-source-pixels' if q.get('images') else 'none'
(root/'data/topologies.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(root/'data/questions.json').write_text(json.dumps(qs,ensure_ascii=False,indent=2))
print('Preserved original pixel assets',len(manifest))
