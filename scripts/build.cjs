const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'..'),E=require('../core.js'),modules=require('./catalog.cjs');
const questions=JSON.parse(fs.readFileSync(path.join(root,'data/questions.json'),'utf8'));
for(const q of questions){E.validateQuestion(q,modules);for(const p of [...(q.images||[]),...(q.explanationImages||[])])if(!fs.existsSync(path.join(root,p)))throw Error('Missing asset '+p);if(!fs.existsSync(path.join(root,'sources',q.source.file)))throw Error('Missing source '+q.source.file);}
if(new Set(questions.map(q=>q.id)).size!==questions.length)throw Error('Duplicate question IDs');
const pdfManifestPath=path.join(root,'data/module-pdfs.json');
if(fs.existsSync(pdfManifestPath)){
 const manifest=JSON.parse(fs.readFileSync(pdfManifestPath,'utf8'));
 const bankSha=crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'data/questions.json'))).digest('hex');
 if(manifest.bankSha256===bankSha)for(const m of modules){
  const pdf=manifest.modules[m.id];if(!pdf)continue;
  const ids=questions.filter(q=>q.module===m.id).map(q=>q.id);
  if(pdf.language!=='en'||pdf.path!==`assets/pdf/${m.id}.pdf`||pdf.questionIds.length!==ids.length||new Set(pdf.questionIds).size!==ids.length||ids.some(id=>!pdf.questionIds.includes(id)))throw Error('Invalid module PDF manifest: '+m.id);
  const file=path.join(root,pdf.path);
  if(!fs.existsSync(file)||crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')!==pdf.sha256)throw Error('Missing or changed module PDF: '+m.id);
  m.pdf=pdf;
 }
}
fs.writeFileSync(path.join(root,'data/bank.js'),'window.CCNABank = '+JSON.stringify({schemaVersion:1,modules,questions})+';\n');
console.log(`${modules.length} modules, ${questions.length} extracted questions, ${questions.filter(q=>q.verified).length} scored questions.`);
