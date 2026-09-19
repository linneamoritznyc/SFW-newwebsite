/* Render every template with every example to a 1200x630 PNG.
 *
 *   node blog-header-templates/render.js
 *
 * The pages are served over http rather than opened as file://, because
 * Chromium will not load @font-face files across a file:// origin and the
 * headers are set in the repository's own self-hosted Montserrat.
 * Same approach as "Trifold Design/build/render.js".
 */
/* Playwright, from the project if it is installed there and from the
   global install otherwise. */
const chromium = (function () {
  try { return require('playwright').chromium; }
  catch (e) { return require('/opt/node22/lib/node_modules/playwright').chromium; }
}());
const http = require('http');
const path = require('path');
const fs = require('fs');

const REPO = path.resolve(__dirname, '..');
const OUT = path.join(__dirname, 'previews');

const TEMPLATES = ['faded-box', 'side-panel', 'bottom-band', 'microscope-circle'];

/* The examples posted to the team. Categories are the labels the blog
   already uses. The photographs are stand-ins from the repository, not the
   photographs these posts will carry.

   The fourth one is a real headline lifted off the live blog, at 147
   characters. It is here to prove the templates survive a title that long,
   because the blog runs them. */
const EXAMPLES = [
  {
    slug: 'ciliates',
    title: 'Ciliates and Soil Health: What We Saw Under the Microscope',
    category: 'Microscopy',
    author: 'Wes Sander',
    image: '../img/w/sfw-amoeba-still-wide.jpg',
    focus: '50% 50%'
  },
  {
    slug: 'watermelon',
    title: 'Case Study: Regenerating a Watermelon Farm',
    category: 'Science & Education',
    author: 'Wes Sander',
    image: '../img/w/erc-rancho-cacachilas-agro.jpg',
    focus: '50% 55%'
  },
  {
    slug: 'scholarships',
    title: 'Scholarship Opportunities for 2026',
    category: 'Foundation Update',
    author: '',
    image: '../img/w/ctpfw-student-moving-compost-1.jpg',
    focus: '50% 40%'
  },
  {
    slug: 'long-title',
    title: 'How A Rare Microscope Sighting Helps Deduce The Problem With Unhealthy Soil: Ciliates, Cysts, And The Clues Hiding In A Struggling Watermelon Crop',
    category: 'Microscopy',
    author: 'Wes Sander',
    image: '../img/w/hand-of-compost.jpg',
    focus: '50% 50%'
  }
];

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.woff2': 'font/woff2',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png': 'image/png',
  '.svg': 'image/svg+xml'
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
  fs.mkdirSync(OUT, { recursive: true });
  const server = await serve();
  const port = server.address().port;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });

  for (const template of TEMPLATES) {
    for (const ex of EXAMPLES) {
      const q = new URLSearchParams({
        title: ex.title, category: ex.category, author: ex.author,
        image: ex.image, focus: ex.focus
      });
      const url = `http://127.0.0.1:${port}/blog-header-templates/${template}.html?${q}`;
      await page.goto(url, { waitUntil: 'networkidle' });
      await page.waitForSelector('html[data-ready="1"]');
      await page.evaluate(() => document.fonts.ready);
      const out = path.join(OUT, `${template}--${ex.slug}.png`);
      await page.locator('#header').screenshot({ path: out });
      console.log('wrote', path.relative(REPO, out));
    }
  }

  await browser.close();
  server.close();
})();
