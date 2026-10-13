from pathlib import Path
import pymupdf as fitz
import subprocess,os,concurrent.futures
root=Path(__file__).resolve().parents[1];run=root/'tmp/ocr-runtime/root'
env={**os.environ,'LD_LIBRARY_PATH':str(run/'usr/lib/x86_64-linux-gnu'),'TESSDATA_PREFIX':str(run/'usr/share/tesseract-ocr/5/tessdata'),'OMP_THREAD_LIMIT':'1'}
print(env['TESSDATA_PREFIX'],flush=True)
if not Path(env['TESSDATA_PREFIX']).exists():env['TESSDATA_PREFIX']=str(next(run.glob('usr/share/tesseract-ocr/*/tessdata')))
names=['Port Security','SDN','DHCP','Drag Drop Quiz 2']
def pagejob(job):
 name,pi,path=job
 subprocess.run([str(run/'usr/bin/tesseract'),str(path),str(path.with_suffix('')),'--psm','3'],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
 return name,pi,path.with_suffix('.txt').read_text()
jobs=[]
for n in names:
 name='CCNA Training » '+(n if 'Quiz' in n else n+' Quiz')
 d=fitz.open(root/'sources'/(name+'.pdf'))
 for pi,p in enumerate(d):
  out=root/'tmp/extracted'/f'ocr-{n}-{pi+1}.png';p.get_pixmap(matrix=fitz.Matrix(2,2)).save(out);jobs.append((name,pi,out))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:res=list(pool.map(pagejob,jobs))
for n in names:
 name='CCNA Training » '+(n if 'Quiz' in n else n+' Quiz')
 t='\n\f\n'.join(t for nm,pi,t in sorted(res) if nm==name)
 (root/'tmp/extracted'/('ocr-'+name+'.txt')).write_text(t)
 print(name,len(t),flush=True)
