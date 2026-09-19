/* Render a header for every post in posts.js, all in one variation, so the
 * blog reads as one family. Also writes a contact sheet of the whole set,
 * which is the thing worth posting in team chat: the family shows up when
 * you see twelve at once, not one at a time.
 *
 *   node blog-header-templates/render-blog.js                 side-panel
 *   node blog-header-templates/render-blog.js faded-box       any other one
 *
 * Output goes to previews/blog-set-<variation>/.
 */
const chromium = (function () {
  try { return require('playwright').chromium; }
  catch (e) { return require('/opt/node22/lib/node_modules/playwright').chromium; }
}());
const http = require('http');
const path = require('path');
const fs = require('fs');

const REPO = path.resolve(__dirname, '..');
const POSTS = require('./posts.js');
const TEMPLATE = process.argv[2] || 'side-panel';
const OUT = path.join(__dirname, 'previews', 'blog-set-' + TEMPLATE);

const TYPES = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8', '.woff2': 'font/woff2',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml'
};

function serve() {
  return new Promise(resolve => {
    const server = http.createServer((req, res) => {
      const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '');
      const file = path.join(REPO, rel);
      if (!file.startsWith(REPO) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
        res.writeHead(404); res.end('not found'); return;
      }
      res.writeHead(200, { 'Content-Type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream' });
      fs.createReadStream(file).pipe(res);
    });
    server.listen(0, '127.0.0.1', () => resolve(server));
  });
}

(async () => {
  fs.rmSync(OUT, { recursive: true, force: true });
  fs.mkdirSync(OUT, { recursive: true });
  const server = await serve();
  const port = server.address().port;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });

  const made = [];
  for (const post of POSTS) {
    /* The emoji some titles carry is dropped: Montserrat has no glyph for
       it, so it falls back to whatever the machine has and the header
       stops being reproducible. */
    const title = post.title.replace(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}️]/gu, '').trim();
    const q = new URLSearchParams({
      title: title, category: post.category, author: post.author,
      image: post.image, focus: post.focus, theme: post.theme || ''
    });
    await page.goto(`http://127.0.0.1:${port}/blog-header-templates/${TEMPLATE}.html?${q}`, { waitUntil: 'networkidle' });
    await page.waitForSelector('html[data-ready="1"]');
    const file = `${post.date}--${post.slug}.png`;
    await page.locator('#header').screenshot({ path: path.join(OUT, file) });
    made.push({ file, post });
    console.log('wrote', path.relative(REPO, path.join(OUT, file)));
  }

  /* The contact sheet. */
  const rows = made.map(m => `<figure><img src="/blog-header-templates/previews/blog-set-${TEMPLATE}/${encodeURIComponent(m.file)}">` +
    `<figcaption>${m.post.date} &middot; ${m.post.category}</figcaption></figure>`).join('');
  const sheetHtml = `<!doctype html><meta charset="utf-8"><title>sheet</title>
  <style>body{margin:0;background:#231F1D;font:13px "Helvetica Neue",Arial,sans-serif;padding:26px}
  h1{color:#fff;font-size:20px;font-weight:600;margin:0 0 6px}
  p{color:rgba(255,255,255,.62);margin:0 0 24px}
  .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
  figure{margin:0}img{width:100%;display:block}
  figcaption{color:rgba(255,255,255,.6);padding-top:7px;font-size:12px;letter-spacing:.04em}</style>
  <h1>Soil Food Web Foundation blog headers &middot; ${TEMPLATE}</h1>
  <p>All twelve posts on page 1 of the news index, one layout. Photographs are stand-ins from the repository.</p>
  <div class="grid">${rows}</div>`;
  const sheetPath = path.join(__dirname, '_sheet.html');
  fs.writeFileSync(sheetPath, sheetHtml);
  await page.setViewportSize({ width: 1500, height: 1000 });
  await page.goto(`http://127.0.0.1:${port}/blog-header-templates/_sheet.html`, { waitUntil: 'networkidle' });
  const sheetOut = path.join(__dirname, 'previews', `contact-sheet-${TEMPLATE}.png`);
  await page.screenshot({ path: sheetOut, fullPage: true });
  fs.unlinkSync(sheetPath);
  console.log('wrote', path.relative(REPO, sheetOut));

  await browser.close();
  server.close();
})();
