// Preserve the supplied HTML exhibits without changing the application's UI.
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('/home/aaron/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root = path.resolve(__dirname, '..');
(async () => {
  const html = fs.readFileSync(path.join(root, 'mi/CCNA 200-301 Questions.html'), 'utf8');
  const data = JSON.parse(html.match(/var D=(.*);\nvar GRID=/)[1]);
  const grid = JSON.parse(html.match(/var GRID=(.*);\nfunction/)[1]);
  const existing = JSON.parse(fs.readFileSync(path.join(root, 'data/questions.json'), 'utf8'));
  const style = html.match(/<style>([\s\S]*?)<\/style>/)[1];
  const browser = await chromium.launch({headless: true, executablePath: '/home/aaron/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell'});
  try {
    const page = await browser.newPage({viewport: {width: 900, height: 1000}, deviceScaleFactor: 2});
    const records = [];
    for (const [index, [name, key]] of grid.entries()) {
      const module = `ccna-${String(index + 1).padStart(2, '0')}`;
      if (!key || existing.some(q => q.module === module && !q.origin)) continue;
      for (const [j, original] of data[key].entries()) {
        const id = `${module}-mi-q${String(j + 1).padStart(3, '0')}`;
        const assets = {};
        for (const [kind, content] of [['exhibit', original.x], ['explanation', /<table\b|<svg\b/.test(original.e) ? original.e : '']]) {
          if (!content) continue;
          await page.setContent(`<html><head><style>${style}\nbody{margin:0;padding:0;background:#fff;color:#17212b}#capture{box-sizing:border-box;width:780px;padding:16px}pre{white-space:pre-wrap;overflow:visible}svg{max-width:100%}</style></head><body><div id="capture">${content}</div></body></html>`);
          const asset = `assets/${id}-${kind}.png`;
          await page.locator('#capture').screenshot({path: path.join(root, asset)});
          assets[kind] = asset;
        }
        records.push({id, module, name, question: j + 1, original, assets});
      }
    }
    fs.writeFileSync(path.join(root, 'tmp/mi-import.json'), JSON.stringify(records, null, 2));
    console.log(`${records.length} source questions; original exhibits rendered.`);
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exitCode = 1; });
