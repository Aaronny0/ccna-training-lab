/* Functional UI and responsive checks for the complete Frontend Excellence refactor. */
const {chromium}=require('/home/aaron/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const assert=require('node:assert/strict'),fs=require('node:fs');
const widths=[1440,1024,768,390,360];
const out='tests/visual-qa';fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/home/aaron/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell'});
 const context=await browser.newContext({viewport:{width:1440,height:1000},colorScheme:'light'});
 const page=await context.newPage(),errors=[],checks=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:8765');
 async function snap(view,width){
  await page.setViewportSize({width,height:width<600?844:1000});
  await page.locator('main').waitFor();
  assert.equal(await page.locator('button div,button pre,button p').count(),0,'Button contents use phrasing elements');
  await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.filter(i=>i.getClientRects().length).map(i=>{i.loading="eager";return i.decode().catch(()=>{});})));
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,`${view} at ${width}: unintended horizontal overflow`);
  const longClips=await page.locator('h1,.mode-copy,.setting-row,.module-open').evaluateAll(els=>els.filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>e.textContent));
  assert.deepEqual(longClips,[],`${view} at ${width}: clipped title/control`);
  await page.evaluate(()=>window.scrollTo(0,0));
  await page.screenshot({path:`${out}/${view}-${width}.png`,fullPage:true});
  if(width===1440||width===390)await page.screenshot({path:`${out}/${view}-${width}-viewport.png`});checks.push({view,width});
 }
 async function all(view){for(const width of widths)await snap(view,width);await page.setViewportSize({width:1440,height:1000});}
 async function nav(view){await page.locator(`[data-page="${view}"]`).first().click();}
 await nav('catalog');await all('catalog');assert.equal(await page.locator('[data-module-card]').count(),40);
 await page.locator('#search').fill('zz-no-module');assert.equal(await page.locator('[data-module-card]').count(),0);await snap('search-empty',390);await page.locator('[data-action="clear"]').click();assert.equal(await page.locator('[data-module-card]').count(),40);
 await nav('dashboard');await all('dashboard-empty');
 await nav('review');await all('review');
 await nav('favorites');await all('favorites-empty');
 await nav('history');await all('history-empty');
 await nav('settings');await all('settings');
 // Actual persisted appearance settings; changes must retain any session permutation.
 await page.locator('[data-theme="dark"]').last().click();assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');await snap('settings-dark',1440);
 await page.reload();assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');await page.locator('.theme-toggle').click();assert.equal(await page.locator('html').getAttribute('data-theme'),'light');assert.equal(await page.locator('.theme-toggle:focus').count(),1);
 await nav('catalog');await page.locator('[data-module="ccna-03"]').click();await all('module');
 await page.locator('[data-start="practice"]').click();await all('quiz');
 let s=await page.evaluate(()=>JSON.parse(localStorage.getItem('packetlab-progress-v1')).session);
 const q=await page.evaluate(id=>CCNABank.questions.find(q=>q.id===id),s.order[0].id);
 await page.locator('[data-lang="fr"]').first().click();assert.deepEqual(await page.evaluate(()=>JSON.parse(localStorage.getItem('packetlab-progress-v1')).session.order),s.order);
 assert.equal(await page.locator('[data-lang="fr"]:focus').count(),1,'Language focus preserved after rendering');
 await snap('quiz-fr',360);
 for(const id of q.answers)await page.locator(`[data-option="${id}"]`).click();await page.locator('.answer-review.correct').waitFor();await all('quiz-feedback');
 await page.locator('[data-bookmark]').first().click();await page.locator('[data-action="pause"]').click();await all('dashboard-resume');
 await nav('favorites');await all('favorites');
 await page.locator('[data-lang="en"]').first().click();await nav('dashboard');await page.locator('[data-action="resume"]').click();
 await page.locator('[data-action="finish"]').first().click();await snap('finish-dialog',360);await page.keyboard.press('Escape');assert.equal(await page.locator('dialog').evaluate(e=>e.open),false);
 await page.locator('[data-action="finish"]').first().click();await page.locator('[data-action="confirm-dialog"]').click();await all('results');await page.locator('.correction summary').first().click();await snap('correction-open',390);
 await nav('history');await all('history');await page.locator('.history-row').first().click();await page.locator('[data-action="retry-mistakes"]').click();await page.locator('.question-panel').waitFor();await page.locator('[data-action="pause"]').click();
 // Dialog error must be visible within the native modal and recoverable.
 await nav('catalog');await page.locator('[data-action="mixed"]').first().click();await all('mixed-dialog');
 for(const input of await page.locator('input[name="modules"]').all())await input.uncheck();await page.locator('#mixed-form button[type="submit"]').click();await page.locator('#mixed-error').waitFor();assert.equal(await page.locator('dialog').evaluate(e=>e.open),true);await snap('mixed-error',390);
 await page.locator('input[name="modules"][value="ccna-03"]').check();await page.locator('input[name="minutes"]').fill('5');await page.locator('#mixed-form button[type="submit"]').click();await page.locator('[data-action="confirm-dialog"]').click();await all('exam');
 assert.equal(await page.locator('.answer-review').count(),0);await page.locator('[data-action="pause"]').click();
 // Original topology with its intrinsic dimensions, readable in both themes and languages.
 await nav('catalog');await page.locator('[data-module="ccna-12"]').click();await page.locator('[data-start="practice"]').click();await page.locator('[data-action="confirm-dialog"]').click();
 s=await page.evaluate(()=>JSON.parse(localStorage.getItem('packetlab-progress-v1')).session);const n=s.order.findIndex(o=>o.id==='ccna-12-q001');await page.locator(`[data-jump="${n}"]`).click();await all('topology');
 const src=await page.locator('.exhibits img').first().getAttribute('src');await page.locator('[data-lang="fr"]').first().click();await page.locator('.theme-toggle').click();await snap('topology-fr-dark',390);assert.equal(await page.locator('.exhibits img').first().getAttribute('src'),src);
 assert.equal(await page.locator('.exhibits img').first().evaluate(i=>i.complete&&i.naturalWidth>0),true);
 await page.locator('.theme-toggle').click();await page.locator('[data-action="pause"]').click();
 await nav('catalog');await page.locator('[data-module="ccna-36"]').click();await page.locator('[data-start="practice"]').click();await page.locator('[data-action="confirm-dialog"]').click();await all('matching');
 s=await page.evaluate(()=>JSON.parse(localStorage.getItem('packetlab-progress-v1')).session);const m=await page.evaluate(id=>CCNABank.questions.find(q=>q.id===id),s.order[0].id);
 for(const [target,opt] of Object.entries(m.solution))await page.locator(`[data-match="${target}"]`).selectOption(opt);await page.locator('.answer-review.correct').waitFor();await snap('matching-correct',360);
 assert.deepEqual(errors,[]);fs.writeFileSync(`${out}/checks.json`,JSON.stringify({browser:'Chromium',checks,errors},null,2));
 console.log(`Frontend QA passed: ${checks.length} captures; all main views at ${widths.join(', ')} px; no overflow/clipped headings/page errors; themes persist; EN/FR permutation/focus, dialogs, matching and original topologies verified.`);
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
