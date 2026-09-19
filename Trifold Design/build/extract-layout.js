/* Extract a text-free background render plus a JSON description of every text
 * block, so make-pptx.py can rebuild the spreads as real PowerPoint text boxes.
 *
 *   node "Trifold Design/build/extract-layout.js"
 *
 * Canva cannot import a PDF without guessing where the text boxes are, because
 * a PDF holds only glyphs at coordinates. A PPTX holds real text boxes, so
 * nothing has to be guessed and nothing moves. This produces the pieces.
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const http = require('http');
const path = require('path');
const fs = require('fs');

const REPO = path.resolve(__dirname, '..', '..');
const OUT = path.resolve(__dirname, '..', 'pptx');
const DPI = 300, SCALE = DPI / 96;
const W_IN = 11.25, H_IN = 8.75;

const TYPES = { '.html':'text/html; charset=utf-8', '.css':'text/css; charset=utf-8',
  '.svg':'image/svg+xml', '.png':'image/png', '.jpg':'image/jpeg', '.jpeg':'image/jpeg',
  '.JPG':'image/jpeg', '.woff2':'font/woff2' };

function serve() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '');
      for (const base of [path.join(REPO, 'Trifold Design', 'build'), REPO]) {
        const f = path.join(base, rel);
        if (f.startsWith(base) && fs.existsSync(f) && fs.statSync(f).isFile()) {
          res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' });
          return fs.createReadStream(f).pipe(res);
        }
      }
      res.writeHead(404); res.end('not found: ' + rel);
    });
    server.listen(0, '127.0.0.1', () => resolve(server));
  });
}

/* Runs inside the page. Returns one record per text block: a block is an
   element that holds text but no block-level child, i.e. the smallest thing
   that owns a paragraph of its own. */
const EXTRACT = () => {
  const sheet = document.querySelector('.sheet').getBoundingClientRect();
  const PX_IN = 96;
  const inX = (v) => +(((v - sheet.left) / PX_IN)).toFixed(4);
  const inY = (v) => +(((v - sheet.top) / PX_IN)).toFixed(4);

  const isBlocky = (el) => {
    const d = getComputedStyle(el).display;
    return d === 'block' || d === 'flex' || d === 'grid' || d === 'list-item' ||
           d === 'table' || d === 'flow-root';
  };
  const hasText = (el) => (el.textContent || '').trim().length > 0;

  const blocks = [];
  const walk = (el) => {
    if (el.tagName === 'SVG' || el.tagName === 'svg') return;
    const kids = [...el.children];
    const blockKids = kids.filter((k) => isBlocky(k) && hasText(k));
    if (blockKids.length > 0) { kids.forEach(walk); return; }
    if (!hasText(el)) return;

    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') return;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return;

    // Content box: where the glyphs actually start.
    const pl = parseFloat(cs.paddingLeft), pr = parseFloat(cs.paddingRight);
    const pt = parseFloat(cs.paddingTop), pb = parseFloat(cs.paddingBottom);

    // Inline runs, so bold and coloured spans survive.
    const runs = [];
    const pushRun = (node, style) => {
      const t = node.textContent;
      if (!t) return;
      const s = getComputedStyle(style);
      runs.push({
        text: t,
        weight: +s.fontWeight || 400,
        italic: s.fontStyle === 'italic',
        color: s.color,
        family: s.fontFamily.split(',')[0].replace(/["']/g, '').trim(),
        size: +parseFloat(s.fontSize).toFixed(2),
        spacing: s.letterSpacing === 'normal' ? 0 : +parseFloat(s.letterSpacing).toFixed(3),
        transform: s.textTransform,
      });
    };
    const collect = (node, styleEl) => {
      for (const n of node.childNodes) {
        if (n.nodeType === 3) pushRun(n, styleEl);
        else if (n.nodeType === 1) {
          if (n.tagName.toLowerCase() === 'br') runs.push({ br: true });
          else if (n.tagName.toLowerCase() === 'svg') continue;
          else collect(n, n);
        }
      }
    };
    collect(el, el);
    if (runs.every((r) => r.br || !r.text.trim())) return;

    const lh = cs.lineHeight === 'normal'
      ? parseFloat(cs.fontSize) * 1.2 : parseFloat(cs.lineHeight);

    blocks.push({
      tag: el.tagName.toLowerCase(),
      cls: el.className && el.className.baseVal === undefined ? el.className : '',
      panel: (el.closest('.panel') || {}).dataset ? el.closest('.panel').dataset.panel : null,
      x: inX(r.left + pl), y: inY(r.top + pt),
      w: +((r.width - pl - pr) / PX_IN).toFixed(4),
      h: +((r.height - pt - pb) / PX_IN).toFixed(4),
      align: cs.textAlign,
      lineHeightPx: +lh.toFixed(2),
      fontSizePx: +parseFloat(cs.fontSize).toFixed(2),
      runs,
    });
  };
  walk(document.querySelector('.sheet'));
  return { sheetW: +(sheet.width / PX_IN).toFixed(4), sheetH: +(sheet.height / PX_IN).toFixed(4), blocks };
};

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const server = await serve();
  const port = server.address().port;
  const browser = await chromium.launch();
  const result = {};

  for (const name of ['outside', 'inside']) {
    const page = await browser.newPage({
      viewport: { width: Math.round(W_IN * 96), height: Math.round(H_IN * 96) },
      deviceScaleFactor: SCALE,
    });
    await page.goto(`http://127.0.0.1:${port}/${name}.html`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);

    const data = await page.evaluate(EXTRACT);
    result[name] = data;

    /* Background render. -webkit-text-fill-color removes glyph paint only, so
       panel fields, photos, QR codes and the currentColor icons all stay. */
    await page.addStyleTag({ content: '*, *::before, *::after { -webkit-text-fill-color: transparent !important; }' });
    await page.screenshot({ path: path.join(OUT, `bg-${name}.png`), fullPage: false });

    console.log(`${name}: ${data.blocks.length} text blocks, bg-${name}.png written`);
    await page.close();
  }

  fs.writeFileSync(path.join(OUT, 'layout.json'), JSON.stringify(result, null, 1));
  console.log('layout.json written');
  await browser.close();
  server.close();
})().catch((e) => { console.error(e); process.exit(1); });
