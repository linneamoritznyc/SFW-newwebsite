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
    if (blockKids.length > 0) {
      kids.forEach(walk);
      /* An element can hold a block-level child AND text of its own. The
         climate box is <p class="pull"><b>heading</b>body text</p> with
         .pull b { display: flex }, so descending into the children alone
         loses the whole paragraph. Emit each run of non-block siblings too. */
      let group = [];
      const flush = () => {
        if (group.length && group.some((n) => (n.textContent || '').trim())) {
          emit(el, group);
        }
        group = [];
      };
      for (const n of el.childNodes) {
        const blocky = n.nodeType === 1 && isBlocky(n) && hasText(n);
        if (blocky) flush(); else group.push(n);
      }
      flush();
      return;
    }
    if (!hasText(el)) return;
    emit(el, [...el.childNodes]);
  };

  /* Build one record from `nodes`, which are children of `el` that lay out as
     one continuous piece of text. */
  const emit = (el, nodes) => {
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') return;

    const whole = nodes.length === el.childNodes.length;
    let r, pl, pr, pt, pb;
    if (whole) {
      r = el.getBoundingClientRect();
      // Content box: where the glyphs actually start.
      pl = parseFloat(cs.paddingLeft); pr = parseFloat(cs.paddingRight);
      pt = parseFloat(cs.paddingTop);  pb = parseFloat(cs.paddingBottom);
    } else {
      // A slice of the element: measure the nodes themselves, and let the
      // usable width run to the element's content edge so it wraps as it did.
      const range = document.createRange();
      range.setStartBefore(nodes[0]);
      range.setEndAfter(nodes[nodes.length - 1]);
      const rr = range.getBoundingClientRect();
      const er = el.getBoundingClientRect();
      const epl = parseFloat(cs.paddingLeft), epr = parseFloat(cs.paddingRight);
      r = { left: er.left + epl, top: rr.top,
            width: er.width - epl - epr, height: rr.height };
      pl = pr = pt = pb = 0;
    }
    if (r.width < 1 || r.height < 1) return;

    // Inline runs, so bold and coloured spans survive.
    const runs = [];
    const runIndexOf = new Map();
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
      if (style !== node) runIndexOf.set(style, runs.length - 1);
    };
    const collect = (list, styleEl) => {
      for (const n of list) {
        if (n.nodeType === 3) pushRun(n, styleEl);
        else if (n.nodeType === 1) {
          if (n.tagName.toLowerCase() === 'br') runs.push({ br: true });
          else if (n.tagName.toLowerCase() === 'svg') continue;
          else collect([...n.childNodes], n);
        }
      }
    };
    collect(nodes, el);
    if (runs.every((r) => r.br || !r.text.trim())) return;

    /* The visual lines the browser produced, with each line's runs kept
       separate so bold and coloured spans survive. Nothing else reproduces
       text-wrap: balance, and a block that gains a line in PowerPoint lands on
       top of whatever sits under it, so the breaks are baked in rather than
       left to another engine's metrics. Line rects also give the true start of
       the text, which is what positions a heading that sits beside an icon. */
    const lineRuns = [];
    {
      const range = document.createRange();
      let cur = null;
      const walkText = (list, runIdx) => {
        for (const n of list) {
          if (n.nodeType === 3) {
            const t = n.textContent;
            for (let i = 0; i < t.length; i++) {
              range.setStart(n, i); range.setEnd(n, i + 1);
              const rect = range.getBoundingClientRect();
              if (rect.width === 0 && rect.height === 0) {
                if (cur && cur.parts.length) cur.parts[cur.parts.length - 1].text += t[i];
                continue;
              }
              const top = Math.round(rect.top * 10) / 10;
              if (!cur || Math.abs(top - cur.top) > 1) {
                cur = { top, left: rect.left, parts: [] };
                lineRuns.push(cur);
              }
              cur.left = Math.min(cur.left, rect.left);
              const last = cur.parts[cur.parts.length - 1];
              if (last && last.runIdx === runIdx) last.text += t[i];
              else cur.parts.push({ runIdx, text: t[i] });
            }
          } else if (n.nodeType === 1) {
            const tag = n.tagName.toLowerCase();
            if (tag === 'svg') continue;
            if (tag === 'br') { cur = null; continue; }
            walkText([...n.childNodes], runIndexOf.get(n) ?? runIdx);
          }
        }
      };
      // Text sitting directly in the element takes the element's own run, not
      // run 0, which would be the <b> lead-in when a block opens with one.
      walkText(nodes, runIndexOf.has(el) ? runIndexOf.get(el) : 0);
      for (const ln of lineRuns) {
        for (const part of ln.parts) part.text = part.text.replace(/\s+/g, ' ');
        while (ln.parts.length && !ln.parts[ln.parts.length - 1].text.trim()) ln.parts.pop();
        if (ln.parts.length) {
          ln.parts[0].text = ln.parts[0].text.replace(/^\s+/, '');
          const t = ln.parts[ln.parts.length - 1];
          t.text = t.text.replace(/\s+$/, '');
        }
      }
    }
    const lines = lineRuns
      .filter((l) => l.parts.length)
      .map((l) => ({ left: inX(l.left), parts: l.parts }));
    if (!lines.length) return;

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
      lines,
      linesLeft: lines.length ? lines[0].left : null,
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
