#!/usr/bin/env python3
"""Render static pages from content/*.json.

Authoring aid, not a runtime dependency: the output is plain static HTML,
committed to the repo and served with no build step. Copy lives in
content/, markup lives here, so copy can change without touching design
and design without touching copy.

    python3 tools/build.py

Every string keys to the SFWF Website Copy Deck's own element names, so a
line in the deck maps to a line in the JSON. [VERIFY] and [PLACEHOLDER]
markers ride as `status` and `note` fields on the object they belong to,
never as body text; the templates turn them into hidden .todo blocks that
?notes=1 reveals.
"""
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTIALS = os.path.join(ROOT, "tools", "partials") + os.sep

def load(name):
    with open(os.path.join(ROOT, "content", name + ".json"), encoding="utf-8") as f:
        return json.load(f)

# Pages the six-item structure introduces (stage 2). Until those files
# exist, the deck's forward-looking hrefs resolve to today's equivalents,
# so the JSON never has to be rewritten when the URLs land.
ROUTES = {
    "practice.html": "projects.html",
    "calendar.html": "now.html",
    "news.html": "now.html#writing",
    "research.html": "publications.html",
}
def href(h):
    if not h or h.startswith(("http", "mailto:", "#")):
        return h
    path, _, frag = h.partition("#")
    if path in ROUTES:
        # The fragment names a section that stage 2 creates; until then the
        # alias page has no such anchor, so land on the page itself.
        return ROUTES[path]
    return h

e = lambda t: html.escape(str(t), quote=False)
A = lambda t: html.escape(str(t), quote=True)

def note(obj, extra=""):
    """A [VERIFY]/[PLACEHOLDER] marker as a hidden production note."""
    if not isinstance(obj, dict):
        return ""
    n = obj.get("note")
    if not n:
        return ""
    kind = {"verify": "Verify", "placeholder": "Placeholder",
            "removed": "Removed"}.get(obj.get("status"), "Note")
    return f'<p class="todo" data-status="{A(obj.get("status",""))}">{e(n)}{e(extra)}</p>\n'

def eyebrow(t):
    return f'<p class="eyebrow">{e(t)}</p>\n' if t else ""

def cta(c, cls="btn"):
    if not c:
        return ""
    return f'<a class="{cls}" href="{A(href(c["href"]))}">{e(c["label"])}</a>'


# ---------------------------------------------------------------- chrome
def chrome():
    g = load("global")
    hdr = open(PARTIALS + "header.html", encoding="utf-8").read()
    ftr = open(PARTIALS + "footer.html", encoding="utf-8").read()
    # Copy that the deck owns, fed from global.json.
    ftr = re.sub(r'(<p class="footer__tag">)[^<]*(</p>)',
                 lambda m: m.group(1) + e(g["footer"]["brandLine"]) + m.group(2), ftr)
    ftr = re.sub(r'(<li>)© 2026 Soil Food Web Foundation(</li>)',
                 lambda m: m.group(1) + e(g["footer"]["legalLine"]) + m.group(2), ftr)
    return hdr, ftr


# ---------------------------------------------------------------- home
def home():
    c = load("home")
    o = []
    h = c["hero"]
    o.append(f'''  <section class="stratum" style="border-top:0;padding-top:var(--s5)">
    <div class="wrap">
      <div class="grid">
        <div class="span-7">
          {eyebrow(h["eyebrow"]).strip()}
          <h1>{e(h["h1"])}</h1>
          <p class="lede">{e(h["subhead"])}</p>
          <p style="margin-top:var(--s4);display:flex;flex-wrap:wrap;gap:var(--s2);align-items:center">
            {cta(h["primaryCta"])}
            {cta(h["secondaryCta"], "btn btn--ghost")}
          </p>
        </div>
        <figure class="plate span-5">
          <div class="plate__f" style="aspect-ratio:4/3" data-empty="{A(h["image"]["note"])}"></div>
        </figure>
      </div>
    </div>
  </section>
''')

    s = c["stats"]
    cells = ""
    for k in ("stat1", "stat2", "stat3"):
        st = s[k]
        src = f'<p class="source small">{e(st["source"])}</p>' if st.get("source") else ""
        cells += f'''        <div class="span-4">
          <p style="font-family:var(--serif);font-size:var(--t4);line-height:1;color:var(--soil);margin-bottom:var(--s1)">{e(st["value"])}</p>
          <p>{e(st["label"])}</p>
          {src}
        </div>
'''
    o.append(f'''  <section class="stratum stratum--deep" aria-labelledby="stats-h">
    <div class="wrap">
      <h2 id="stats-h" class="visually-hidden">The Foundation in figures</h2>
      <div class="grid">
{cells}      </div>
      <p class="todo">{e(s["note"])}</p>
    </div>
  </section>
''')

    w = c["whoWeAre"]
    body = "\n          ".join(f"<p>{e(p)}</p>" for p in w["body"])
    o.append(f'''  <section class="stratum" aria-labelledby="who-h">
    <div class="wrap">
      <div class="grid">
        <div class="span-6">
          {eyebrow(w["eyebrow"]).strip()}
          <h2 id="who-h">{e(w["h2"])}</h2>
          {body}
          <p><a href="{A(href(w["link"]["href"]))}">{e(w["link"]["label"])}</a></p>
        </div>
      </div>
      {note(w).strip()}
    </div>
  </section>
''')

    a = c["howItWorks"]
    steps = ""
    for st in a["steps"]:
        steps += f'''        <div class="span-6">
          <div class="icon-row">
            <svg class="icon icon--olive icon--lg" aria-hidden="true"><use href="#i-cycle"/></svg>
            <div>
              <p class="small" style="color:var(--ink-faint)">Step {st["n"]}</p>
              <h3 style="font-size:var(--t2);margin-bottom:var(--s1)">{e(st["title"])}</h3>
              <p style="font-size:var(--t0);color:var(--ink-soft)">{e(st["body"])}</p>
            </div>
          </div>
        </div>
'''
    o.append(f'''  <section class="stratum" aria-labelledby="approach-h">
    <div class="wrap">
      <div class="head">
        {eyebrow(a["eyebrow"]).strip()}
        <h2 id="approach-h">{e(a["h2"])}</h2>
      </div>
      <div class="grid" style="row-gap:var(--s4)">
{steps}      </div>
      <p style="margin-top:var(--s4)"><a href="{A(href(a["link"]["href"]))}">{e(a["link"]["label"])}</a></p>
      {note(a).strip()}
    </div>
  </section>
''')

    l = c["learnWithUs"]
    cards = ""
    for cd in l["cards"]:
        cards += f'''        <li class="card">
          <div class="card__kind"><span>{e(cd["tag"])}</span></div>
          <h3 class="card__title"><a href="{A(href(cd["cta"]["href"]))}">{e(cd["title"])}</a></h3>
          <p class="card__line">{e(cd["body"])}</p>
          <p class="card__line"><a href="{A(href(cd["cta"]["href"]))}">{e(cd["cta"]["label"])} →</a></p>
          {note(cd).strip()}
        </li>
'''
    o.append(f'''  <section class="stratum stratum--deep" aria-labelledby="learn-h">
    <div class="wrap">
      <div class="head">
        {eyebrow(l["eyebrow"]).strip()}
        <h2 id="learn-h">{e(l["h2"])}</h2>
      </div>
      <ul class="cards">
{cards}      </ul>
      <p class="todo">{e(l["layoutNote"])}</p>
    </div>
  </section>
''')

    n = c["whatsNew"]
    links = " · ".join(f'<a href="{A(href(x["href"]))}">{e(x["label"])}</a>' for x in n["links"])
    o.append(f'''  <section class="stratum stratum--moss" aria-labelledby="new-h">
    <div class="wrap">
      <div class="head">
        {eyebrow(n["eyebrow"]).strip()}
        <h2 id="new-h">{e(n["h2"])}</h2>
      </div>
      <ul class="rule-list">
        <li class="entry">
          <span class="dated" style="color:var(--sage)"><time datetime="2026-09-16">16 September to 20 December 2026</time></span>
          <h3 class="entry__t"><a href="learn.html#pdc">Permaculture Design Certification cohort begins</a></h3>
          <span class="entry__kind" style="color:var(--sage)">Course, cohort</span>
        </li>
        <li class="entry">
          <span class="dated" style="color:var(--sage)"><time datetime="2026-10">October 2026, dates to confirm</time></span>
          <h3 class="entry__t"><a href="learn-workshops.html#india">India Accelerator Workshop, Coimbatore</a></h3>
          <span class="entry__kind" style="color:var(--sage)">Workshop</span>
        </li>
      </ul>
      <p style="margin-top:var(--s4)">{links}</p>
      {note(n).strip()}
    </div>
  </section>
''')

    t = c["testimonial"]
    o.append(f'''  <section class="stratum notes-only" aria-label="Testimonial">
    <div class="wrap">
      {note(t["quote"]).strip()}
      {note(t["attribution"]).strip()}
    </div>
  </section>
''')

    ec = c["ecosystem"]
    o.append(f'''  <section class="stratum" aria-labelledby="eco-h">
    <div class="wrap">
      <div class="head">
        {eyebrow(ec["eyebrow"]).strip()}
        <h2 id="eco-h" class="visually-hidden">Our ecosystem</h2>
        <p class="lede">{e(ec["line"])}</p>
      </div>
      <p>{cta(ec["cta"], "btn btn--ghost")}</p>
      {note(ec).strip()}
    </div>
  </section>
''')

    j = c["joinBand"]
    btns = " ".join(cta(x, "btn" if i == 0 else "btn btn--ghost")
                    for i, x in enumerate(j["ctas"]) if x.get("type") != "email")
    o.append(f'''  <section class="stratum stratum--moss" aria-labelledby="join-h">
    <div class="wrap">
      <h2 id="join-h">{e(j["h2"])}</h2>
      <p class="lede" style="color:var(--paper)">{e(j["body"])}</p>
      <p style="margin-top:var(--s4);display:flex;flex-wrap:wrap;gap:var(--s2);align-items:center">{btns}</p>
    </div>
  </section>
''')
    return "<main id=\"main\">\n\n" + "\n".join(o) + "\n</main>"


def render(path, title, desc, main):
    hdr, ftr = chrome()
    sprite = open(PARTIALS + "sprite.html", encoding="utf-8").read()
    head = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{A(desc)}">
  <meta property="og:site_name" content="Soil Food Web Foundation">
  <link rel="preload" href="fonts/eb-garamond-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="fonts/source-sans-3-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<!-- Icon sprite, inlined so the page works over file:// -->
'''
    out = head + sprite + "\n\n" + hdr + "\n" + main + "\n\n" + ftr + '\n<script src="js/site.js"></script>\n</body>\n</html>\n'
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(out)
    print("rendered", path, len(out), "bytes")


if __name__ == "__main__":
    h = load("home")
    render("index.html",
           "Soil Food Web Foundation, a nonprofit teaching the science of living soil",
           h["hero"]["subhead"], home())
