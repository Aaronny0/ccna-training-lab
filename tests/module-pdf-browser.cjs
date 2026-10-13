const {chromium}=require('/home/aaron/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const manifest=JSON.parse(fs.readFileSync('data/module-pdfs.json','utf8'));
async function verify(page,base,language){
 await page.goto(base);
 await page.locator(`[data-lang="${language}"]`).click();
 for(let i=1;i<=40;i++){
  const module=`ccna-${String(i).padStart(2,'0')}`,pdf=manifest.modules[module];
  await page.locator('[data-page="catalog"]').first().click();
  if(!pdf){const card=page.locator(`[data-module-card="${module}"]`);assert.equal(await card.locator('[data-module-pdf]').count(),0);assert.equal(await card.locator('button:enabled').count(),0);continue;}
  await page.locator(`[data-module="${module}"]`).click();
  const link=page.locator('[data-module-pdf]');
  assert.equal(await link.count(),pdf?1:0,module);
  if(!pdf)continue;
  assert.equal(await link.innerText(),language==='en'?'Download PDF':'Télécharger le PDF');
  assert.equal(await link.getAttribute('href'),pdf.path);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,module);
  const before=await page.evaluate(()=>localStorage.getItem('packetlab-progress-v1'));
  const downloadEvent=page.waitForEvent('download');
  await link.click();const download=await downloadEvent;
  assert.equal(await download.failure(),null,module);
  const bytes=fs.readFileSync(await download.path());
  assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),pdf.sha256,module);
  assert.equal(bytes.subarray(0,5).toString(),'%PDF-');
  assert.equal(await page.evaluate(()=>localStorage.getItem('packetlab-progress-v1')),before,'Downloading must preserve progress');
 }
}
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/home/aaron/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell'});
 try{
  const ctx=await browser.newContext({acceptDownloads:true,viewport:{width:1440,height:1000}});
  const page=await ctx.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await verify(page,'http://127.0.0.1:8765','en');
  await page.screenshot({path:'tmp/pdfs/module-download-desktop.png'});
  await page.setViewportSize({width:390,height:844});
  await verify(page,'http://127.0.0.1:8765','fr');
  await page.screenshot({path:'tmp/pdfs/module-download-mobile.png'});
  // Direct file access is the site's existing offline distribution mode.
  await page.goto('file://'+path.resolve('index.html'));
  await page.locator('[data-page="catalog"]').first().click();
  await page.locator('[data-module="ccna-34"]').click();
  const event=page.waitForEvent('download');await page.locator('[data-module-pdf]').click();
  assert.equal(await (await event).failure(),null);
  assert.deepEqual(errors,[]);
  console.log('72 desktop/mobile native downloads passed: one button per available module, EN/FR labels, same English file, no progress changes, plus file:// offline download.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
