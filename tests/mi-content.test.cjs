const test = require('node:test'), assert = require('node:assert/strict'), fs = require('node:fs'), crypto = require('node:crypto');
const html = fs.readFileSync('mi/CCNA 200-301 Questions.html', 'utf8');
const data = JSON.parse(html.match(/var D=(.*);\nvar GRID=/)[1]);
const grid = JSON.parse(html.match(/var GRID=(.*);\nfunction/)[1]);
const questions = JSON.parse(fs.readFileSync('data/questions.json', 'utf8'));
const additions = questions.filter(q => q.origin?.file === 'CCNA 200-301 Questions.html');
test('all 146 additional HTML questions retain their module, choices and source answer keys', () => {
  assert.equal(additions.length, 146);
  assert.equal(new Set(additions.map(q => q.module)).size, 19);
  for (const q of additions) {
    const key = grid[Number(q.module.slice(-2)) - 1][1];
    const original = data[key][q.origin.question - 1];
    if (q.type === 'choice') {
      assert.deepEqual(q.options.map(o => o.text.en), original.o, q.id);
      assert.deepEqual(q.answers.map(id => id.charCodeAt(0) - 97), original.c, q.id);
    } else {
      assert.deepEqual(q.options.map(o => o.text.en), original.g, q.id);
      assert.deepEqual(q.targets.map(t => t.text.en), original.it, q.id);
      assert.deepEqual(q.targets.map(t => Number(q.solution[t.id].slice(1)) - 1), original.a, q.id);
    }
    assert.equal(q.images.length, original.x ? 1 : 0, q.id);
    assert.equal(q.origin.sha256, crypto.createHash('sha256').update(html).digest('hex'));
  }
});
test('new source archive and linked assets have valid provenance; all supplied HTML questions remain eligible for scoring', () => {
  const sha = crypto.createHash('sha256').update(fs.readFileSync('sources/' + additions[0].source.file)).digest('hex');
  const manifest = JSON.parse(fs.readFileSync('data/topologies.json'));
  for (const q of additions) {
    assert.equal(q.source.sha256, sha, q.id);
    assert.ok(q.source.page > 0);
    for (const asset of [...q.images, ...(q.explanationImages || [])]) {
      assert.ok(fs.existsSync(asset));
      assert.equal(manifest[asset].source, q.source.file);
    }
    if (!q.verified) assert.ok(q.issue.en && q.issue.fr);
  }
  assert.equal(additions.filter(q => !q.verified).length, 0);
});
