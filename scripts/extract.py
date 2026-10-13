"""Extract originals, source answer IDs, and illustrations. Never infer absent answers."""
from pathlib import Path
import re,json,hashlib,subprocess
import pymupdf as fitz
ROOT=Path(__file__).resolve().parents[1]
MAP={'Cloud & Virtualization':3,'Trunking':6,'EtherChannel':9,'IP Routing':12,'OSPF Quiz 2':15,'NTP':18,'Access-list':21,'Security Quiz 2':24,'DNS':27,'Port Security':29,'Wireless':30,'SDN':32,'DNA Center':33,'Drag Drop Quiz 2':35,'Drag Drop Quiz 3':36,'DHCP':38,'Automation':39}
records=[]; manifest=[]; seen=set()
for p in sorted((ROOT/'sources').glob('*.pdf')):
 digest=hashlib.sha256(p.read_bytes()).hexdigest()
 if digest in seen:
  manifest.append({'file':p.name,'sha256':digest,'duplicate':True});continue
 seen.add(digest)
 key=p.stem.replace('CCNA Training » ','').replace(' (1)',''); key=key if key in MAP else key.removesuffix(' Quiz')
 if key not in MAP:continue
 module=f'ccna-{MAP[key]:02d}'
 doc=fitz.open(p); current=None; originals=[]; image_count=0; end=False
 scanned=sum(len(pg.get_text()) for pg in doc)/len(doc)<600
 if scanned:
  manifest.append({'file':p.name,'sha256':digest,'module':module,'scanned':True,'pages':len(doc)});continue
 for pi,page in enumerate(doc):
  # In reading order; question text is limited by the next heading.
  blocks=page.get_text('dict',sort=True)['blocks']
  for b in blocks:
   if b['type']==1:
    if current and not end:
     image_count+=1; out=f'{module}-q{current["source"]["question"]}-{image_count}.png'
     rect=fitz.Rect(b['bbox']); page.get_pixmap(matrix=fitz.Matrix(2,2),clip=rect).save(ROOT/'assets'/out)
     current['images'].append('assets/'+out)
    continue
   for l in b.get('lines',[]):
    s=''.join(x['text'] for x in l['spans']).strip()
    if not s:continue
    if re.match(r'Comments \(\d+\)',s) or s=='Add a Comment':end=True
    if end:continue
    m=re.fullmatch(r'Question (\d+)',s)
    if m:
     current={'id':f'{module}-q{int(m[1]):03d}','module':module,'source':{'file':p.name,'sha256':digest,'question':int(m[1]),'page':pi+1},'lines':[],'answers':[],'images':[]};records.append(current)
    elif current and not (l['bbox'][1]<27 or l['bbox'][1]>page.rect.height-25):
     current['lines'].append(s)
     a=re.match(r'^([A-H])\.\s',s)
     if a and any(x['color']==255 for x in l['spans']):current['answers'].append(a[1].lower())
  if end:break
 manifest.append({'file':p.name,'sha256':digest,'module':module,'scanned':False,'pages':len(doc)})
for r in records:
 lines=r.pop('lines'); txt='\n'.join(lines)
 r['originalExtract']=txt
 part=txt.split('\nExplanation',1); body=part[0]; exp=part[1].strip() if len(part)>1 else ''
 opts=list(re.finditer(r'^([A-H])\.\s',body,re.M))
 if opts:
  r['type']='choice'; r['prompt']={'en':body[:opts[0].start()].strip()};r['options']=[]
  for i,o in enumerate(opts):
   val=body[o.end():opts[i+1].start() if i+1<len(opts) else len(body)].strip()
   r['options'].append({'id':o[1].lower(),'text':{'en':val}})
 else:r['type']='match';r['prompt']={'en':body};r['options']=[]
 r['explanation']={'en':exp};r['translationStatus']='pending';r['required']=len(r['answers']);r['verified']=bool(opts and r['answers'])
(ROOT/'data'/'extracted.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
(ROOT/'data'/'sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('Extracted',len(records),'text questions;',sum(r['verified'] for r in records),'with explicit source answer keys')
for r in records: print(r['id'],r['answers'],'images',len(r['images']))
