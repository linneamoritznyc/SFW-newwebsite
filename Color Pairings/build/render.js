/* Render the pairing sheets to PNG.
 *   node "Color Pairings/build/render.js"
 * Served over http rather than file:// so Chromium will load the
 * repository's own self-hosted @font-face files.
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const http = require('http');
const path = require('path');
const fs = require('fs');

const REPO = path.resolve(__dirname, '..', '..');
const OUT = path.resolve(__dirname, '..');
const TYPES = { '.html': 'text/html; charset=utf-8', '.woff2': 'font/woff2', '.png': 'image/png', '.svg': 'image/svg+xml' };

const SHEETS = [
  ['sheet-existing',  'pairings-current-set.png'],
  ['sheet-new',       'pairings-twelve-more.png'],
  ['sheet-reference', 'pairings-reference.png'],
];

(async () => {
  const server = http.createServer((req, res) => {
    const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '');
    const file = path.join(REPO, rel);
    if (!file.startsWith(REPO) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
      res.writeHead(404); res.end('not found: ' + rel); return;
    }
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream' });
    fs.createReadStream(file).pipe(res);
  });
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const port = server.address().port;

  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 2 });

  for (const [src, out] of SHEETS) {
    await page.goto(`http://127.0.0.1:${port}/Color%20Pairings/build/${src}.html`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const box = await page.locator('.sheet').boundingBox();
    await page.setViewportSize({ width: Math.round(box.width), height: Math.round(box.height) });
    await page.locator('.sheet').screenshot({ path: path.join(OUT, out), scale: 'device' });
    console.log(out, Math.round(box.width * 2) + 'x' + Math.round(box.height * 2));
  }

  await browser.close();
  server.close();
})();
