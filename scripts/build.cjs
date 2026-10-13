const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'),E=require('../core.js'),modules=require('./catalog.cjs');
const questions=JSON.parse(fs.readFileSync(path.join(root,'data/questions.json'),'utf8'));
for(const q of questions){E.validateQuestion(q,modules);for(const p of [...(q.images||[]),...(q.explanationImages||[])])if(!fs.existsSync(path.join(root,p)))throw Error('Missing asset '+p);if(!fs.existsSync(path.join(root,'sources',q.source.file)))throw Error('Missing source '+q.source.file);}
if(new Set(questions.map(q=>q.id)).size!==questions.length)throw Error('Duplicate question IDs');
fs.writeFileSync(path.join(root,'data/bank.js'),'window.CCNABank = '+JSON.stringify({schemaVersion:1,modules,questions})+';\n');
console.log(`${modules.length} modules, ${questions.length} extracted questions, ${questions.filter(q=>q.verified).length} scored questions.`);
