/* Pure, language-independent quiz engine. Shared by the browser and Node tests. */
(function(root){
'use strict';
function shuffle(items,rng=Math.random){const a=[...items];for(let i=a.length-1;i>0;i--){const j=Math.floor(rng()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function equal(a,b){return Array.isArray(a)&&Array.isArray(b)&&a.length===b.length&&[...a].sort().every((v,i)=>v===[...b].sort()[i]);}
function correct(q,value){return q.type==='match'?!!value&&q.targets.every(t=>value[t.id]===q.solution[t.id])&&Object.keys(value).length===q.targets.length:equal(value,q.answers);}
function expectedCount(q){return Number.isInteger(q.required)&&q.required>0&&q.required<=q.options.length?q.required:null;}
function answered(q,value,confirmed=false){
 if(!q)return false;
 const ids=q.options.map(o=>o.id);
 if(q.type==='match')return !!value&&q.targets.every(t=>ids.includes(value[t.id]))&&Object.keys(value).length===q.targets.length;
 if(!Array.isArray(value)||!value.length||new Set(value).size!==value.length||value.some(id=>!ids.includes(id)))return false;
 const count=expectedCount(q);return count===null?confirmed:value.length===count;
}
function sessionComplete(session,questions){const byId=new Map(questions.map(q=>[q.id,q]));return !!session?.order.length&&session.order.every(({id})=>{const q=byId.get(id);return q&&answered(q,session.answers[id],session.confirmed?.[id]);});}
function recordAnswer(session,q,value,{questionId=q.id,confirm=false}={}){
 if(!session||session.finished||session.order[session.index]?.id!==questionId||q.id!==questionId||session.completed?.[q.id])return false;
 const ids=q.options.map(o=>o.id);
 if(q.type==='choice'&&(!Array.isArray(value)||value.some(id=>!ids.includes(id))||new Set(value).size!==value.length))return false;
 if(q.type==='match'&&(!value||Object.keys(value).some(id=>!q.targets.some(t=>t.id===id)||!ids.includes(value[id]))))return false;
 session.answers[q.id]=q.type==='match'?{...value}:[...value];
 session.confirmed||={};session.completed||={};
 if(confirm)session.confirmed[q.id]=true;
 if(answered(q,value,session.confirmed[q.id]))session.completed[q.id]=true;
 return true;
}
function createSession(questions,{mode='practice',module='mixed',minutes=60,rng=Math.random}={}){
 if(!questions.length)throw new Error('Empty question pool');
 const order=shuffle(questions,rng).map(q=>({id:q.id,options:shuffle(q.options.map(o=>o.id),rng),targets:q.targets?q.targets.map(t=>t.id):[]}));
 return {id:globalThis.crypto?.randomUUID?.()||`${Date.now()}-${Math.random()}`,module,mode,order,index:0,answers:{},validated:{},completed:{},confirmed:{},startedAt:Date.now(),elapsed:0,limit:mode==='exam'?minutes*60:0,finished:false};
}
function score(session,questions){const byId=new Map(questions.map(q=>[q.id,q]));const rows=session.order.map(({id})=>{const q=byId.get(id);return {id,answer:session.answers[id]??(q?.type==='match'?{}:[]),correct:q?correct(q,session.answers[id]):false};});const passed=rows.filter(r=>r.correct).length;return {rows,correct:passed,total:rows.length,percent:rows.length?Math.round(passed/rows.length*100):0};}
function recordProgress(progress,id,passed,at=Date.now()){
 const old=progress[id]||{attempts:0,correct:0,streak:0};const streak=passed?old.streak+1:0;
 return {...progress,[id]:{attempts:old.attempts+1,correct:old.correct+(passed?1:0),streak,last:at,due:at+(passed?Math.min(30,2**streak)*86400000:0)}};
}
function stats(modules,questions,progress={},history=[]){const available=modules.filter(m=>questions.some(q=>q.module===m.id));const active=questions;const mastered=active.filter(q=>(progress[q.id]?.streak||0)>=3).length;const exams=history.filter(h=>h.mode==='exam');const total=exams.reduce((n,h)=>n+h.total,0);return {modules:modules.length,available:available.length,pending:modules.length-available.length,questions:active.length,mastered,mastery:active.length?Math.round(mastered/active.length*100):0,coverage:Math.round(available.length/modules.length*100),exams:exams.length,performance:total?Math.round(exams.reduce((n,h)=>n+h.correct,0)/total*100):null};}
function reviewPool(questions,progress,now=Date.now()){return questions.filter(q=>(!progress[q.id]||progress[q.id].streak<3||progress[q.id].due<=now)).sort((a,b)=>(progress[a.id]?.due||0)-(progress[b.id]?.due||0));}
function validateQuestion(q,modules){
 if(!q||typeof q.id!=='string'||!/^ccna-\d{2}-[a-zA-Z0-9-]+$/.test(q.id))throw new Error('Invalid question ID');
 if(!modules.some(m=>m.id===q.module)||!q.id.startsWith(q.module+'-'))throw new Error('Unknown or mismatched module');
 if(typeof q.prompt?.en!=='string'||!q.prompt.en||typeof q.source?.file!=='string'||!q.source.file.endsWith('.pdf')||/[\\/]/.test(q.source.file)||!/^[a-f0-9]{64}$/.test(q.source?.sha256)||!Number.isInteger(q.source.question)||q.source.question<1||typeof q.verified!=='boolean')throw new Error('Missing original or source');
 if(!['choice','match'].includes(q.type)||!Array.isArray(q.options))throw new Error('Invalid type/options');
 const ids=q.options.map(o=>o.id);if(new Set(ids).size!==ids.length||q.options.some(o=>!/^[a-zA-Z0-9-]+$/.test(o.id)||typeof o.text?.en!=='string'||!o.text.en))throw new Error('Invalid options');
 if(q.type==='choice'&&(!Array.isArray(q.answers)||q.answers.length<1||new Set(q.answers).size!==q.answers.length||q.answers.some(id=>!ids.includes(id))||(q.required!=null&&q.required!==q.answers.length)))throw new Error('Invalid answer IDs');
 if(q.type==='match'&&(!q.targets?.length||new Set(q.targets.map(t=>t.id)).size!==q.targets.length||q.required!==q.targets.length||q.targets.some(t=>!/^[a-zA-Z0-9-]+$/.test(t.id)||!t.text?.en||!ids.includes(q.solution?.[t.id]))))throw new Error('Invalid matching solution');
 if(q.translationStatus==='validated'&&(!q.prompt.fr||q.options.some(o=>!o.text.fr)||q.targets?.some(t=>!t.text.fr)||q.explanation.en&&!q.explanation.fr))throw new Error('Incomplete validated translation');
 if(q.images?.some(p=>typeof p!=='string'||!/^assets\/[\w.-]+\.(png|jpg|svg|webp)$/.test(p)))throw new Error('Invalid asset path');
 return true;
}
function mergeQuestions(existing,incoming,modules){
 const result=[...existing];const ids=new Map(existing.map(q=>[q.id,q]));const fingerprints=new Map(existing.map(q=>[`${q.module}:${q.source.sha256}:${q.source.question}`,q]));let added=0,duplicates=0;
 const content=q=>{const {verified,...rest}=q;return JSON.stringify(rest);};
 for(const q of incoming){validateQuestion(q,modules);const key=`${q.module}:${q.source.sha256}:${q.source.question}`;if(ids.has(q.id)){if(content(ids.get(q.id))!==content(q))throw new Error(`Conflicting question ID: ${q.id}`);duplicates++;continue;}if(fingerprints.has(key)||result.some(x=>x.module===q.module&&x.prompt.en===q.prompt.en)){duplicates++;continue;}result.push(q);ids.set(q.id,q);fingerprints.set(key,q);added++;}
 return {questions:result,added,duplicates};
}
const api={shuffle,equal,correct,expectedCount,answered,sessionComplete,recordAnswer,createSession,score,recordProgress,stats,reviewPool,validateQuestion,mergeQuestions};if(typeof module==='object')module.exports=api;root.CCNAEngine=api;
})(typeof window==='object'?window:globalThis);
