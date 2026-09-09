#!/usr/bin/env python3
"""Render static pages from content/*.json.

Authoring aid, not a runtime dependency: output is plain static HTML,
committed and served with no build step. Copy lives in content/, markup
lives here, so copy changes without touching design and design without
touching copy.

    python3 tools/build.py

Keys are the SFWF Website Copy Deck's own element names. [VERIFY] and
[PLACEHOLDER] ride as status/note fields on the object they belong to,
never as body text; templates turn them into .todo blocks hidden until
?notes=1.
"""
import json, os, html, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTIALS = os.path.join(ROOT, "tools", "partials") + os.sep

def load(n):
    with open(os.path.join(ROOT, "content", n + ".json"), encoding="utf-8") as f:
        return json.load(f)

e = lambda t: html.escape(str(t), quote=False)
A = lambda t: html.escape(str(t), quote=True)

def note(o, cls="todo"):
    if not isinstance(o, dict) or not o.get("note"):
        return ""
    return '<p class="%s" data-status="%s">%s</p>' % (cls, A(o.get("status", "")), e(o["note"]))

def eyebrow(t):
    return '<p class="eyebrow">%s</p>' % e(t) if t else ""

def cta(c, cls="btn"):
    if not c or not isinstance(c, dict) or "href" not in c:
        return ""
    return '<a class="%s" href="%s">%s</a>' % (cls, A(c["href"]), e(c["label"]))

def sec(inner, cls="", label=None, sid=None):
    a = ' aria-labelledby="%s"' % label if label else ""
    i = ' id="%s"' % sid if sid else ""
    k = (" " + cls) if cls else ""
    return '  <section class="stratum%s"%s%s>\n    <div class="wrap">\n%s\n    </div>\n  </section>\n' % (k, a, i, inner)

def slug(t):
    """Lowercase, drop punctuation, collapse to hyphens: "Contact & Legal" -> contact-legal."""
    t = t.replace("\u2019", "").replace("'", "")
    t = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
    return t


def hero(h, hid, sid=None):
    pills = ""
    if h.get("anchorPills"):
        pills = ('\n      <ul class="chips" aria-label="On this page">'
                 + "".join('<li><a class="chip" href="#%s">%s</a></li>' % (A(slug(p)), e(p))
                           for p in h["anchorPills"])
                 + "</ul>")
    intro = h.get("intro") or h.get("subhead") or ""
    ctas = ""
    if h.get("primaryCta"):
        ctas = ('\n      <p style="margin-top:var(--s4);display:flex;flex-wrap:wrap;gap:var(--s2);align-items:center">'
                + cta(h["primaryCta"]) + " " + cta(h.get("secondaryCta"), "btn btn--ghost") + "</p>")
    return ('  <section class="stratum" style="border-top:0"%s>\n    <div class="wrap">\n'
            '      <div class="head" style="margin-bottom:0">\n        %s\n        <h1 id="%s">%s</h1>\n'
            '        <p class="lede">%s</p>\n      </div>%s%s\n    </div>\n  </section>\n'
            % (' id="%s"' % sid if sid else "", eyebrow(h.get("eyebrow")), hid, e(h["h1"]), e(intro), pills, ctas))

def tabs(items, target, aria="Filter"):
    li = "".join('<li><button class="chip" type="button" data-filter="%s" aria-pressed="%s">%s</button></li>'
                 % (A("all" if i == 0 else t.lower().replace(" ", "-").replace("&", "and")),
                    "true" if i == 0 else "false", e(t)) for i, t in enumerate(items))
    return ('      <ul class="chips" data-filter-for="%s" aria-label="%s">%s'
            '<li class="small" data-filter-status style="align-self:center;color:var(--ink-faint)"></li></ul>\n'
            % (A(target), A(aria), li))

def cards(items, kind=None):
    out = '      <ul class="cards">\n'
    for c in items:
        k = '        <li class="card"%s>\n' % (' data-kind="%s"' % A(kind) if kind else "")
        if c.get("tag"):
            k += '          <div class="card__kind"><span>%s</span></div>\n' % e(c["tag"])
        title = e(c.get("title", c.get("name", "")))
        if isinstance(c.get("cta"), dict):
            title = '<a href="%s">%s</a>' % (A(c["cta"]["href"]), title)
        k += '          <h3 class="card__title">%s</h3>\n' % title
        if c.get("tagline"):
            k += '          <p class="card__line" style="color:var(--soil);font-weight:600">%s</p>\n' % e(c["tagline"])
        if c.get("body"):
            k += '          <p class="card__line">%s</p>\n' % e(c["body"])
        if isinstance(c.get("cta"), dict):
            k += '          <p class="card__line"><a href="%s">%s &rarr;</a></p>\n' % (A(c["cta"]["href"]), e(c["cta"]["label"]))
        n = note(c)
        if n:
            k += "          " + n + "\n"
        out += k + "        </li>\n"
    return out + "      </ul>\n"

def steps(items, icon="i-cycle"):
    out = '      <div class="grid" style="row-gap:var(--s4)">\n'
    for s in items:
        out += ('        <div class="span-6">\n          <div class="icon-row">\n'
                '            <svg class="icon icon--olive icon--lg" aria-hidden="true"><use href="#%s"/></svg>\n'
                '            <div>\n              <p class="small" style="color:var(--ink-faint)">Step %s</p>\n'
                '              <h3>%s</h3>\n              <p style="font-size:var(--t0);color:var(--ink-soft)">%s</p>\n'
                '            </div>\n          </div>\n        </div>\n'
                % (icon, s["n"], e(s.get("title", "")), e(s["body"])))
    return out + "      </div>\n"


# ------------------------------------------------------------------ chrome
def chrome(depth=0):
    g = load("global")
    b = "../" * depth
    def h(x):
        return x if x.startswith(("http", "mailto:", "#")) else b + x
    u = g["utilityBar"]
    util = "".join('<li><a href="%s">%s</a></li>' % (A(h(a["href"])), e(a["label"])) for a in u["actions"])
    acc = ""
    for it in g["nav"]["items"]:
        if not it.get("children"):
            continue
        sid = it["label"].lower().replace(" ", "-")
        links = "".join('                <li><a href="%s">%s</a></li>\n' % (A(h(c["href"])), e(c["label"]))
                        for c in it["children"])
        desc = it.get("pillar") or "Who we are and how we are governed"
        acc += ('          <li class="acc__item" data-acc-item data-open="false">\n'
                '            <button class="acc__btn" type="button" data-acc-btn aria-controls="acc-%s">\n'
                '              <span class="acc__name">%s</span><span class="acc__desc">%s</span>\n'
                '            </button>\n'
                '            <div class="acc__panel" id="acc-%s" data-acc-panel><div>\n'
                '              <ul class="acc__links">\n%s              </ul>\n'
                '            </div></div>\n          </li>\n' % (sid, e(it["label"]), e(desc), sid, links))
    topnav = "".join('<li><a href="%s">%s</a></li>' % (A(h(i["href"])), e(i["label"])) for i in g["nav"]["items"][1:])
    hdr = ('<!-- ============ UTILITY BAR + HEADER (every page) ============ -->\n'
           '<div class="utility">\n  <div class="wrap">\n'
           '    <p class="utility__tagline">%s</p>\n'
           '    <ul class="utility__links">%s</ul>\n  </div>\n</div>\n'
           '<header class="site-header">\n  <div class="wrap">\n'
           '    <a class="wordmark" href="%s">\n'
           '      <span class="wordmark__name">Soil Food Web Foundation</span>\n'
           '      <span class="wordmark__status">A 501(c)(3) nonprofit</span>\n    </a>\n'
           '    <ul class="site-header__links">%s</ul>\n'
           '    <a class="btn btn--donate" href="%s">Donate</a>\n'
           '    <button class="menu-btn" type="button" data-menu-open aria-controls="overlay" aria-expanded="false">\n'
           '      <svg class="icon" aria-hidden="true"><use href="#i-menu"/></svg><span class="menu-btn__label">Menu</span>\n'
           '    </button>\n  </div>\n</header>\n\n'
           '<div class="overlay" id="overlay" data-open="false" role="dialog" aria-modal="true" aria-label="Site menu">\n'
           '  <div class="wrap">\n    <div class="overlay__top">\n'
           '      <span class="wordmark">\n'
           '        <span class="wordmark__name">Soil Food Web Foundation</span>\n'
           '        <span class="wordmark__status">A 501(c)(3) nonprofit</span>\n      </span>\n'
           '      <button class="menu-btn" type="button" data-menu-close>\n'
           '        <svg class="icon" aria-hidden="true"><use href="#i-close"/></svg>Close\n'
           '      </button>\n    </div>\n'
           '    <div class="overlay__body">\n      <nav class="overlay__nav" aria-label="Sections">\n'
           '        <ul class="acc" data-accordion>\n%s        </ul>\n'
           '        <ul class="overlay__utility">%s</ul>\n      </nav>\n'
           '      <aside class="overlay__now" aria-labelledby="now-h">\n'
           '        <h2 id="now-h">Happening now</h2>\n        <ul class="now-list">\n'
           '          <li><span class="dated"><time datetime="2026-09-16">16 September to 20 December 2026</time></span>'
           '<a href="%slearn.html#pdc">Permaculture Design Certification cohort</a></li>\n'
           '          <li><span class="dated"><time datetime="2026-10">October 2026</time></span>'
           '<a href="%scalendar.html#workshops">India Accelerator Workshop, Coimbatore</a></li>\n'
           '        </ul>\n        <a class="more" href="%scalendar.html">Everything that is happening</a>\n'
           '      </aside>\n    </div>\n'
           '    <div class="cutout cutout--overlay">\n'
           '      <img src="%simg/cutout-placeholder.svg" alt="" loading="lazy" decoding="async" width="320" height="260">\n'
           '    </div>\n  </div>\n</div>\n\n'
           % (e(u["tagline"]), util, A(h("index.html")), topnav, A(h("donate.html")),
              acc, util, A(b), A(b), A(b), A(b)))

    f = g["footer"]
    cols = [("Foundation", [("About Us", "about.html"), ("Our Team", "about-team.html"),
                            ("Governance and financials", "about-governance.html"), ("Contact & Legal", "contact.html")]),
            ("Learn", [("Programs Overview", "learn.html"), ("Calendar", "calendar.html"),
                       ("Free Webinars", "learn-webinars.html"), ("Scholarships", "learn-scholarships.html")]),
            ("Resources", [("Research Database", "research.html"), ("How it works", "science.html"),
                           ("Case Studies", "practice.html#case-studies"), ("Media and press", "contact.html#media")]),
            ("Get Involved", [("Donate", "donate.html"), ("Volunteer", "donate.html#volunteer"),
                              ("Find a Professional", "directory.html"), ("Logo use", "contact.html#logo")])]
    navs = ""
    for i, (hn, links) in enumerate(cols):
        li = "".join('          <li><a href="%s">%s</a></li>\n' % (A(h(x[1])), e(x[0])) for x in links)
        # 4 wordmark + four 2-wide columns from track 5 = 12 exactly.
        span = "span-2 start-5" if i == 0 else "span-2"
        navs += ('      <nav class="%s" aria-labelledby="f-%d">\n        <h2 id="f-%d">%s</h2>\n'
                 '        <ul>\n%s        </ul>\n      </nav>\n' % (span, i, i, e(hn), li))
    ftr = ('<!-- ============ FOOTER (every page) ============ -->\n'
           '<footer class="site-footer">\n  <div class="wrap">\n    <div class="grid">\n'
           '      <div class="span-4">\n'
           '        <span class="wordmark"><span class="wordmark__name">Soil Food Web Foundation</span>'
           '<span class="wordmark__status">A 501(c)(3) nonprofit</span></span>\n'
           '        <p class="footer__tag">%s</p>\n'
           '        <form class="footer__news" action="#" method="post" aria-label="Newsletter">\n'
           '          <label for="footer-email" class="visually-hidden">Email address</label>\n'
           '          <input class="input" id="footer-email" type="email" name="email" placeholder="Email for the newsletter" required>\n'
           '          <button class="btn" type="submit">Subscribe</button>\n        </form>\n'
           '        <p class="caption" style="color:rgba(255,255,255,.75)">One email a month. Unsubscribe with one click.</p>\n'
           '      </div>\n%s    </div>\n'
           '    <div class="footer__legal">\n'
           '      <p>EIN 39-4439236. Registered office: 5441 S Macadam Ave Ste N, Portland, Oregon 97239. '
           'Our Form 990 and financial statements are available on the <a href="%s">governance page</a> and on request.</p>\n'
           '      <ul>\n        <li>%s</li>\n'
           '        <li><a href="%s">Privacy</a></li>\n        <li><a href="%s">Terms</a></li>\n'
           '        <li><a href="%s">Accessibility</a></li>\n      </ul>\n    </div>\n  </div>\n</footer>\n\n'
           % (e(f["brandLine"]), navs, A(h("about-governance.html")), e(f["legalLine"]),
              A(h("privacy.html")), A(h("terms.html")), A(h("accessibility.html"))))
    return hdr, ftr


def render(path, title, desc, main, depth=0):
    hdr, ftr = chrome(depth)
    b = "../" * depth
    sprite = open(PARTIALS + "sprite.html", encoding="utf-8").read()
    head = ('<!doctype html>\n<html lang="en">\n<head>\n  <meta charset="utf-8">\n'
            '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '  <title>%s</title>\n  <meta name="description" content="%s">\n'
            '  <meta property="og:site_name" content="Soil Food Web Foundation">\n'
            '  <link rel="preload" href="%sfonts/montserrat-latin-variable.woff2" as="font" type="font/woff2" crossorigin>\n'
            '  <link rel="preload" href="%sfonts/source-sans-3-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
            '  <link rel="stylesheet" href="%scss/site.css">\n</head>\n<body>\n'
            '<a class="skip" href="#main">Skip to content</a>\n\n'
            '<!-- Icon sprite, inlined so the page works over file:// -->\n' % (e(title), A(desc), b, b, b))
    out = head + sprite + "\n\n" + hdr + main + "\n\n" + ftr + '<script src="%sjs/site.js"></script>\n</body>\n</html>\n' % b
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(out)
    print("  rendered", path)

MAIN = lambda s: '<main id="main">\n\n' + s + '\n</main>'


# ------------------------------------------------------------------- pages
def p_home():
    c = load("home"); o = []
    h = c["hero"]
    o.append('  <section class="stratum" style="border-top:0">\n    <div class="wrap">\n      <div class="grid">\n'
             '        <div class="span-7">\n          %s\n          <h1>%s</h1>\n'
             '          <p class="lede">%s</p>\n'
             '          <p style="margin-top:var(--s4);display:flex;flex-wrap:wrap;gap:var(--s2);align-items:center">%s %s</p>\n'
             '        </div>\n        <figure class="plate span-5">\n'
             '          <div class="plate__f" style="aspect-ratio:4/3" data-empty="%s"></div>\n'
             '        </figure>\n      </div>\n    </div>\n  </section>\n'
             % (eyebrow(h["eyebrow"]), e(h["h1"]), e(h["subhead"]),
                cta(h["primaryCta"]), cta(h["secondaryCta"], "btn btn--ghost"), A(h["image"]["note"])))
    s = c["stats"]; cells = ""
    for k in ("stat1", "stat2", "stat3"):
        st = s[k]
        src_ = '<p class="source small">%s</p>' % e(st["source"]) if st.get("source") else ""
        cells += ('        <div class="span-4">\n          <p class="stat">%s</p>\n'
                  '          <p class="stat__label">%s</p>\n          %s\n        </div>\n'
                  % (e(st["value"]), e(st["label"]), src_))
    o.append(sec('      <h2 id="stats-h" class="visually-hidden">The Foundation in figures</h2>\n'
                 '      <div class="grid">\n%s      </div>\n      %s' % (cells, note(s)),
                 "stratum--deep", "stats-h"))
    w = c["whoWeAre"]
    o.append(sec('      <div class="grid">\n        <div class="span-7">\n          %s\n          <h2 id="who-h">%s</h2>\n'
                 '          %s\n          <p><a href="%s">%s</a></p>\n        </div>\n      </div>\n      %s'
                 % (eyebrow(w["eyebrow"]), e(w["h2"]),
                    "\n          ".join("<p>%s</p>" % e(p) for p in w["body"]),
                    A(w["link"]["href"]), e(w["link"]["label"]), note(w)), label="who-h"))
    a = c["howItWorks"]
    o.append(sec('      <div class="head">\n        %s\n        <h2 id="approach-h">%s</h2>\n      </div>\n%s'
                 '      <p style="margin-top:var(--s4)"><a href="%s">%s</a></p>\n      %s'
                 % (eyebrow(a["eyebrow"]), e(a["h2"]), steps(a["steps"]),
                    A(a["link"]["href"]), e(a["link"]["label"]), note(a)), label="approach-h"))
    l = c["learnWithUs"]
    o.append(sec('      <div class="head">\n        %s\n        <h2 id="learn-h">%s</h2>\n      </div>\n%s      %s'
                 % (eyebrow(l["eyebrow"]), e(l["h2"]), cards(l["cards"]),
                    '<p class="todo">%s</p>' % e(l["layoutNote"])), "stratum--deep", "learn-h"))
    n = c["whatsNew"]
    links = " &middot; ".join('<a href="%s">%s</a>' % (A(x["href"]), e(x["label"])) for x in n["links"])
    o.append(sec('      <div class="head">\n        %s\n        <h2 id="new-h">%s</h2>\n      </div>\n'
                 '      <ul class="rule-list">\n'
                 '        <li class="entry">\n          <span class="dated"><time datetime="2026-09-16">16 September to 20 December 2026</time></span>\n'
                 '          <h3 class="entry__t"><a href="learn.html#pdc">Permaculture Design Certification cohort begins</a></h3>\n'
                 '          <span class="entry__kind">Course, cohort</span>\n        </li>\n'
                 '        <li class="entry">\n          <span class="dated"><time datetime="2026-10">October 2026, dates to confirm</time></span>\n'
                 '          <h3 class="entry__t"><a href="calendar.html#workshops">India Accelerator Workshop, Coimbatore</a></h3>\n'
                 '          <span class="entry__kind">Workshop</span>\n        </li>\n      </ul>\n'
                 '      <p style="margin-top:var(--s4)">%s</p>\n      %s' % (eyebrow(n["eyebrow"]), e(n["h2"]), links, note(n)),
                 label="new-h"))
    t = c["testimonial"]
    o.append(sec("      %s\n      %s" % (note(t["quote"]), note(t["attribution"])), "notes-only"))
    ec = c["ecosystem"]
    o.append(sec('      <div class="head">\n        %s\n        <h2 id="eco-h" class="visually-hidden">Our ecosystem</h2>\n'
                 '        <p class="lede">%s</p>\n      </div>\n      <p>%s</p>\n      %s'
                 % (eyebrow(ec["eyebrow"]), e(ec["line"]), cta(ec["cta"], "btn btn--ghost"), note(ec)),
                 "stratum--deep", "eco-h"))
    j = c["joinBand"]
    btns = " ".join(cta(x, "btn" if i == 0 else "btn btn--ghost")
                    for i, x in enumerate(j["ctas"]) if x.get("type") != "email")
    o.append(sec('      <h2 id="join-h">%s</h2>\n      <p class="lede" style="color:var(--paper)">%s</p>\n'
                 '      <p style="margin-top:var(--s4);display:flex;flex-wrap:wrap;gap:var(--s2)">%s</p>'
                 % (e(j["h2"]), e(j["body"]), btns), "stratum--moss", "join-h"))
    return MAIN("\n".join(o))


def p_about():
    c = load("about"); o = [hero(c["hero"], "about-h")]
    m = c["missionVision"]
    o.append(sec('      <div class="grid">\n        <div class="span-6"><h2 id="mission-h">Mission</h2><p class="lede">%s</p></div>\n'
                 '        <div class="span-6"><h2>Vision</h2><p class="lede">%s</p></div>\n      </div>'
                 % (e(m["mission"]), e(m["vision"])), "stratum--deep", "mission-h", "mission"))
    hi = c["history"]
    rows = "".join('        <li class="entry">\n          <span class="dated">%s</span>\n'
                   '          <div><h3 class="entry__t">%s</h3><p class="entry__line">%s</p>%s</div>\n'
                   '          <span></span>\n        </li>\n'
                   % (e(x["year"]), e(x["title"]), e(x["body"]),
                      ('<p class="entry__line"><a href="%s">%s</a></p>' % (A(x["link"]), A(x["link"]))) if x.get("link") else "")
                   for x in hi["entries"])
    o.append(sec('      <div class="head"><h2 id="story-h">%s</h2></div>\n      <ul class="rule-list">\n%s      </ul>'
                 % (e(hi["h2"]), rows), label="story-h", sid="our-story"))
    wd = c["whatWeDo"]
    o.append(sec('      <div class="head"><h2 id="wd-h">%s</h2></div>\n%s'
                 % (e(wd["h2"]), steps([{"n": p["n"], "title": p["title"], "body": p["body"]} for p in wd["pillars"]], "i-web")),
                 "stratum--deep", "wd-h", "what-we-do"))
    t = c["team"]
    o.append(sec('      <div class="head"><h2 id="team-h">%s</h2></div>\n'
                 '      <p>The full roster, taken from soilfoodweb.com, lives on the team page.</p>\n'
                 '      <p><a class="btn btn--ghost" href="about-team.html">Our team and board</a></p>\n      %s'
                 % (e(t["h2"]), note(t)), label="team-h", sid="team"))
    el = c["elaine"]
    o.append(sec('      <div class="head">\n        %s\n        <h2 id="el-h">%s</h2>\n      </div>\n      %s\n'
                 '      <p><a href="%s">%s</a></p>'
                 % (eyebrow(el["eyebrow"]), e(el["h2"]),
                    "\n      ".join("<p>%s</p>" % e(p) for p in el["body"]),
                    A(el["link"]["href"]), e(el["link"]["label"])), "stratum--deep", "el-h", "dr-elaines-legacy"))
    cl = c["contactLegal"]
    o.append(sec('      <div class="grid">\n        <div class="span-6"><h2 id="cl-h">Contact &amp; Legal</h2>\n'
                 '          <p>%s</p><p><a class="btn btn--ghost" href="contact.html">Contact us</a></p></div>\n'
                 '        <div class="span-5 start-8"><p class="small">%s</p><p class="small">%s</p>%s</div>\n      </div>'
                 % (e(cl["contact"]), e(cl["legal"]), e(cl["brandUse"]),
                    note({"note": cl["brandUseNote"], "status": "note"})), label="cl-h", sid="contact-legal"))
    return MAIN("\n".join(o))


def p_learn():
    c = load("learn"); o = [hero(c["hero"], "learn-h")]
    ps = c["pathSelector"]
    o.append(sec('      <div class="head"><h2 id="path-h">%s</h2></div>\n'
                 '      <ul class="chips" aria-label="Paths">%s</ul>'
                 % (e(ps["h2"]), "".join('<li><span class="chip">%s</span></li>' % e(x) for x in ps["chips"])),
                 "stratum--deep", "path-h"))
    rows = ""
    for p in c["programs"]:
        rows += ('        <li class="entry" id="%s">\n          <span class="entry__kind" style="text-align:left">%s</span>\n'
                 '          <div><h3 class="entry__t">%s</h3>\n'
                 '            <p class="entry__line">%s</p>\n            <p class="entry__line">%s</p>%s</div>\n'
                 '          <span></span>\n        </li>\n'
                 % (A(p["id"]), e(p["tagline"]), e(p["name"]), e(p["body"]),
                    '<a href="%s">%s &rarr;</a>' % (A(p["cta"]["href"]), e(p["cta"]["label"])), note(p)))
    o.append(sec('      <div class="head"><h2 id="prog-h" class="visually-hidden">Programs</h2></div>\n'
                 '      <ul class="rule-list">\n%s      </ul>\n'
                 '      <p class="ribbon">%s</p>\n      %s'
                 % (rows, e(c["guarantee"]["ribbon"]), note(c["guarantee"])), label="prog-h", sid="programs"))
    t = c["testimonials"]
    o.append(sec('      <div class="head"><h2 id="tq-h">%s</h2></div>\n      %s'
                 % (e(t["h2"]), "\n      ".join(note(q) for q in t["quotes"])), "notes-only", "tq-h"))
    f = c["faq"]
    rows = "".join('        <li class="entry">\n          <span></span>\n'
                   '          <div><h3 class="entry__t">%s</h3><p class="entry__line">%s</p>%s</div>\n'
                   '          <span></span>\n        </li>\n' % (e(q["q"]), e(q["a"]), note(q)) for q in f["items"])
    o.append(sec('      <div class="head"><h2 id="faq-h">%s</h2></div>\n      <ul class="rule-list">\n%s      </ul>'
                 % (e(f["h2"]), rows), "stratum--deep", "faq-h"))
    return MAIN("\n".join(o))


def p_science():
    c = load("science"); o = [hero(c["hero"], "sci-h")]
    body = ""
    for m in c["mechanisms"]:
        body += ('      <div class="grid" style="padding-block:var(--s5);border-top:var(--hairline) solid var(--rule)" id="mechanism-%d">\n'
                 '        <div class="span-5">\n          <p class="small" style="color:var(--ink-faint)">%d of 6</p>\n'
                 '          <h3>%s</h3>\n          <p>%s</p>\n        </div>\n'
                 '        <figure class="plate span-6 start-7">\n'
                 '          <div class="plate__f" style="aspect-ratio:16/9" data-empty="%s"></div>\n'
                 '          <figcaption><span class="plate__n">Plate %d.</span> <span class="plate__t">%s</span></figcaption>\n'
                 '        </figure>\n      </div>\n'
                 % (m["n"], m["n"], e(m["title"]), e(m["body"]), A(m["animation"]["note"]), m["n"], e(m["title"])))
    o.append('  <section class="stratum" aria-labelledby="mech-h">\n    <div class="wrap">\n'
             '      <h2 id="mech-h" class="visually-hidden">The six mechanisms</h2>\n%s    </div>\n  </section>\n' % body)
    br = c["bridge"]
    o.append(sec('      <div class="head"><h2 id="br-h">%s</h2><p>%s</p></div>\n'
                 '      <p><a class="btn" href="practice.html#case-studies">Case studies</a> '
                 '<a class="btn btn--ghost" href="learn.html">Explore our programs</a></p>'
                 % (e(br["title"]), e(br["body"])), "stratum--deep", "br-h"))
    cs = c["cases"]
    o.append(sec('      <div class="head"><h2 id="cs-h">%s</h2><p>%s</p></div>\n      %s\n'
                 '      <p class="small">%s</p>' % (e(cs["h2"]), e(cs["intro"]), note(cs["cards"]), e(c["honestFooter"])),
                 label="cs-h"))
    return MAIN("\n".join(o))


def p_practice():
    c = load("practice"); o = [hero(c["hero"], "pr-h")]
    o.append(sec("      " + note(c["projects"]), "notes-only"))
    cs = c["caseStudies"]
    o.append(sec('      <div class="head">\n        %s\n        <h2 id="csx-h">%s</h2>\n        <p>%s</p>\n      </div>\n      %s\n'
                 '      <p><a class="btn btn--ghost" href="projects/market-garden-sweden.html">Market garden makeover, Sweden</a></p>'
                 % (eyebrow(cs["eyebrow"]), e(cs["h2"]), e(cs["lede"]), note(cs["cards"])),
                 label="csx-h", sid="case-studies"))
    w = c["workWithUs"]
    fields = "".join('          <p><label for="w-%d">%s</label><br><input class="input" id="w-%d" type="text"></p>\n'
                     % (i, e(f), i) for i, f in enumerate(w["form"]["fields"]))
    o.append(sec('      <div class="head">\n        <p class="eyebrow">%s</p>\n        <h2 id="ww-h">%s</h2>\n        <p>%s</p>\n      </div>\n%s'
                 '      <div class="grid" style="margin-top:var(--s5)">\n'
                 '        <div class="span-6">\n          <h3>%s</h3>\n          <form action="mailto:info@soilfoodweb.com" method="post">\n%s'
                 '            <p><button class="btn" type="submit">Send</button></p>\n          </form>\n          %s\n        </div>\n'
                 '        <div class="span-5 start-8"><p>%s</p></div>\n      </div>'
                 % (e(w["h2"]), e(w["tagline"]), e(w["lede"]), cards(w["cards"]),
                    e(w["form"]["title"]), fields, note(w["form"]),
                    " &middot; ".join('<a href="%s">%s</a>' % (A(x["href"]), e(x["label"])) for x in w["crossLinks"])),
                 "stratum--deep", "ww-h", "work-with-us"))
    return MAIN("\n".join(o))


def p_community():
    c = load("community"); o = [hero(c["hero"], "com-h")]
    m = c["map"]
    o.append(sec('      <div class="head">\n        %s\n        <h2 id="map-h">%s</h2>\n        <p>%s</p>\n      </div>\n'
                 '      <figure class="plate"><div class="plate__f" style="aspect-ratio:2/1" data-empty="%s"></div></figure>'
                 % (eyebrow(m["eyebrow"]), e(m["h2"]), e(m["lede"]), A(m["note"])),
                 "stratum--deep", "map-h", "community-map"))
    d = c["directory"]
    o.append(sec('      <div class="head">\n        %s\n        <h2 id="dir-h">%s</h2>\n      </div>\n'
                 '      <p class="lede">%s</p>\n'
                 '      <p><a class="btn" href="directory.html">Find a professional</a></p>\n'
                 '      <p class="small">%s</p>\n      %s'
                 % (eyebrow(d["eyebrow"]), e(d["h2"]), e(d["clarifyingHeader"]), e(d["footerLine"]),
                    note({"note": d["dataNote"], "status": d["dataStatus"]})),
                 label="dir-h", sid="find-a-professional"))
    j = c["joinBand"]
    o.append(sec('      <h2 id="cj-h">%s</h2>\n      <p class="lede" style="color:var(--paper)">%s</p>\n'
                 '      <p style="display:flex;flex-wrap:wrap;gap:var(--s2);margin-top:var(--s4)">%s</p>'
                 % (e(j["h2"]), e(j["body"]),
                    " ".join(cta(x, "btn" if i == 0 else "btn btn--ghost") for i, x in enumerate(j["ctas"]))),
                 "stratum--moss", "cj-h", "join"))
    return MAIN("\n".join(o))


def p_calendar():
    c = load("calendar"); o = [hero(c["hero"], "cal-h")]
    f = c["featured"]
    rows = ('        <li class="cal__row">\n          <div class="cal__rail">\n'
            '            <svg class="icon icon--olive" aria-hidden="true"><use href="#i-scholarship"/></svg>\n'
            '            <span><span class="cal__name">Permaculture Design Certification</span>'
            '<span class="cal__when">16 September to 20 December 2026</span></span>\n          </div>\n'
            '          <div class="cal__track"><span class="cal__bar" style="--l:4.11%;--w:26.301%"></span></div>\n        </li>\n'
            '        <li class="cal__row">\n          <div class="cal__rail">\n'
            '            <svg class="icon icon--olive" aria-hidden="true"><use href="#i-workshop"/></svg>\n'
            '            <span><span class="cal__name">India Accelerator Workshop, Coimbatore</span>'
            '<span class="cal__when">18 to 31 October 2026, dates to confirm</span></span>\n          </div>\n'
            '          <div class="cal__track"><span class="cal__bar" style="--l:12.877%;--w:3.836%"></span></div>\n        </li>\n'
            '        <li class="cal__row">\n          <div class="cal__rail">\n'
            '            <svg class="icon icon--olive" aria-hidden="true"><use href="#i-calendar"/></svg>\n'
            '            <span><span class="cal__name">The rest of 2027</span><span class="cal__when">Not yet scheduled</span></span>\n'
            '          </div>\n          <div class="cal__track">'
            '<span class="cal__bar cal__bar--todo" style="--l:33.425%;--w:66.575%"><span>dates not set</span></span></div>\n        </li>\n')
    months = ""
    grid = ""
    import calendar as _c
    y, mo = 2026, 9
    for _ in range(12):
        w = round(_c.monthrange(y, mo)[1] / 365 * 100, 3)
        months += '<li style="flex:0 0 %s%%">%s <span style="color:var(--ink-faint)">%s</span></li>' % (w, _c.month_abbr[mo], str(y)[2:])
        grid += '<span style="flex:0 0 %s%%"></span>' % w
        mo += 1
        if mo > 12:
            mo = 1; y += 1
    o.append(sec('      <h2 id="cal-h2" class="visually-hidden">Events</h2>\n'
                 + tabs(c["filterTabs"], "#cal-list", "Event type")
                 + '      <div class="cal-wrap" role="region" aria-label="Year calendar" tabindex="0">\n'
                   '        <div class="cal" data-cal data-cal-start="2026-09-01" data-cal-end="2027-08-31">\n'
                   '          <div class="cal__grid" aria-hidden="true">%s<span class="cal__today" data-cal-today hidden></span></div>\n'
                   '          <ol class="cal__months" aria-hidden="true">%s</ol>\n'
                   '          <ol class="cal__rows">\n%s          </ol>\n        </div>\n      </div>\n'
                   '      <p class="small">Bars are placed by their real dates across September 2026 to August 2027. '
                   'A solid bar is a confirmed run, the dashed band is time that is not scheduled yet, and the green line marks today.</p>\n'
                   '      <ul class="rule-list" id="cal-list">\n'
                   '        <li class="entry" data-kind="workshops" id="workshops">\n'
                   '          <span class="dated"><time datetime="2026-10">18 to 31 October 2026</time></span>\n'
                   '          <div><h3 class="entry__t">%s</h3><p class="entry__line">%s</p>\n          <p class="entry__line">%s</p></div>\n'
                   '          <span class="entry__kind">Workshop</span>\n        </li>\n'
                   '        <li class="entry" data-kind="public-webinars">\n'
                   '          <span class="dated">Monthly</span>\n'
                   '          <div><h3 class="entry__t"><a href="learn-webinars.html">Free educational webinar</a></h3></div>\n'
                   '          <span class="entry__kind">Public webinar</span>\n        </li>\n      </ul>\n      %s\n'
                   '      <p class="small">%s</p>'
                   % (grid, months, rows, e(f["title"]), e(f["body"]), cta(f["cta"], "btn btn--ghost"),
                      note(c["otherListings"]), e(c["footerLine"])), label="cal-h"))
    return MAIN("\n".join(o))


def p_news():
    c = load("news"); o = [hero(c["hero"], "news-h")]
    posts = [("14 Aug 2026", "2026-08-14", "Learning to see: what is your soil test really telling you?", "blog", ""),
             ("14 Jul 2026", "2026-07-14", "A brief history of the fungi-to-bacteria ratio", "blog", "Wes Sander"),
             ("1 May 2026", "2026-05-01", "Ciliates, cysts and the clues in a struggling watermelon crop", "blog", "Wes Sander"),
             ("13 Apr 2026", "2026-04-13", "The School launches its first Permaculture Design Certificate course", "foundation-news", ""),
             ("23 Feb 2026", "2026-02-23", "Advanced Programs are reopening", "foundation-news", "Evan Buckman"),
             ("18 Feb 2026", "2026-02-18", "Obituary for Dr. Elaine Ingham", "foundation-news", "")]
    rows = "".join('        <li class="entry" data-kind="%s">\n          <span class="dated"><time datetime="%s">%s</time></span>\n'
                   '          <div><h3 class="entry__t">%s</h3></div>\n          <span class="entry__kind">%s</span>\n        </li>\n'
                   % (k, dt, d, e(t), e(a or k.replace("-", " ").title())) for d, dt, t, k, a in posts)
    o.append(sec('      <h2 id="news-list-h" class="visually-hidden">All posts</h2>\n'
                 + tabs(c["filterTabs"], "#news-list", "Category")
                 + '      <ul class="rule-list" id="news-list">\n%s      </ul>\n'
                   '      <p class="todo">the six posts above carry no link until the blog is migrated to /news/[slug], '
                   'and all earlier posts still need pulling from the archive. Run crawl.py locally, keep every date and author. Linnea.</p>\n'
                   '      <p class="small">%s</p>' % (rows, e(c["featuredSlotRule"])), label="news-h", sid="foundation"))
    nl = c["newsletter"]
    o.append(sec('      <h2 id="nl-h">%s</h2>\n      <p>%s</p>\n'
                 '      <form action="#" method="post" aria-label="Newsletter" style="display:flex;gap:var(--s1);max-width:26rem">\n'
                 '        <label for="news-email" class="visually-hidden">Email address</label>\n'
                 '        <input class="input" id="news-email" type="email" placeholder="Email for the newsletter" required>\n'
                 '        <button class="btn" type="submit">%s</button>\n      </form>\n'
                 '      <p class="todo">form action: which service receives the email field (Ontraport?). DECISION 14. Evan.</p>'
                 % (e(nl["title"]), e(nl["body"]), e(nl["cta"])), "stratum--deep", "nl-h", "subscribe"))
    return MAIN("\n".join(o))


def p_research():
    c = load("research"); o = []
    o.append(hero({"eyebrow": "RESEARCH", "h1": "The research behind living soil",
                   "intro": "A growing database of soil food web science: Dr. Elaine Ingham's publications, research from the wider field, and, as our open-research program matures, studies from the Foundation and its partners."},
                  "res-h"))
    rows = ""
    for s in c["seedEntries"]:
        link = '<a href="%s">%s</a>' % (A(s["link"]), e(s["citation"])) if s.get("link") else e(s["citation"])
        rows += ('        <li class="entry">\n          <span class="dated">Seed entry</span>\n'
                 '          <div><h3 class="entry__t">%s</h3>%s</div>\n          <span class="entry__kind">Publication</span>\n        </li>\n'
                 % (link, note(s)))
    o.append(sec('      <h2 id="res-list-h" class="visually-hidden">The database</h2>\n'
                 + tabs(["All", "Dr. Elaine's publications", "Soil food web science", "Foundation research"], "#res-list", "Type")
                 + '      <ul class="rule-list" id="res-list">\n%s      </ul>\n      <p class="todo">%s</p>'
                 % (rows, e(c["databaseNote"])), label="res-h"))
    w = c["workWithUs"]
    o.append(sec('      <h2 id="rw-h">%s</h2>\n      <p class="lede">%s</p>\n      <p>%s</p>'
                 % (e(w["h2"]), e(w["body"]), cta(w["cta"])), "stratum--deep", "rw-h", "work-with-us"))
    return MAIN("\n".join(o))


def p_login():
    c = load("login"); o = [hero(c["hero"], "log-h")]
    items = []
    for ch in c["choosers"]:
        nm = ch["name"]["note"] if isinstance(ch["name"], dict) else ch["name"]
        pg = ch["programs"]["note"] if isinstance(ch["programs"], dict) else ch["programs"]
        items.append({"title": nm, "body": pg, "cta": ch["cta"] if ch["cta"]["href"] != "#" else None,
                      "note": "confirm which programs live on which platform before publish. Evan.", "status": "verify"})
    o.append(sec('      <h2 id="lms-h" class="visually-hidden">Choose your platform</h2>\n'
                 + cards(items) + '      <p>%s</p>' % e(c["helpLine"]), "stratum--deep", "lms-h"))
    return MAIN("\n".join(o))


def p_donate():
    c = load("donate"); o = [hero(c["hero"], "don-h")]
    g = c["makeGift"]
    o.append(sec('      <div class="grid">\n        <div class="span-6">\n          <h2 id="gift-h">Make a gift</h2>\n'
                 '          <form action="#" method="post" aria-label="Donate">\n'
                 '            <p role="group" aria-label="Frequency">%s</p>\n'
                 '            <p role="group" aria-label="Amount">%s</p>\n'
                 '            <p><button class="btn btn--donate" type="submit">%s</button></p>\n          </form>\n'
                 '          <p class="small">%s</p>\n          %s\n        </div>\n'
                 '        <div class="span-5 start-8">\n          <h2>%s</h2>\n          %s\n'
                 '          <p>%s <a href="%s">%s</a></p>\n        </div>\n      </div>'
                 % (" ".join('<button class="chip" type="button" aria-pressed="%s">%s</button>' % ("true" if i == 0 else "false", e(x)) for i, x in enumerate(g["frequencies"])),
                    " ".join('<button class="chip" type="button" aria-pressed="%s">%s</button>' % ("true" if i == 1 else "false", e(x)) for i, x in enumerate(g["amounts"])),
                    e(g["cta"]), e(g["finePrint"]), note(c["impactLines"]),
                    e(c["whyMonthly"]["h2"]), note(c["whyMonthly"]),
                    e(c["otherGiving"]["body"]), A(c["otherGiving"]["link"]["href"]), e(c["otherGiving"]["link"]["label"])),
                 label="gift-h"))
    v = c["volunteer"]
    fields = "".join('          <p><label for="v-%d">%s</label><br><input class="input" id="v-%d" type="text"></p>\n' % (i, e(f), i)
                     for i, f in enumerate(v["form"]["fields"]))
    o.append(sec('      <div class="head">\n        %s\n        <h2 id="vol-h">%s</h2>\n        <p>%s</p>\n      </div>\n'
                 '      <div class="grid"><div class="span-6"><form action="mailto:info@soilfoodweb.com" method="post">\n%s'
                 '        <p><button class="btn" type="submit">Send</button></p>\n      </form>\n      %s</div></div>'
                 % (eyebrow(v["eyebrow"]), e(v["h2"]), e(v["lede"]), fields, note(v)),
                 "stratum--deep", "vol-h", "volunteer"))
    return MAIN("\n".join(o))


def p_scholarships():
    c = load("scholarships"); o = [hero(c["hero"], "sch-h")]
    st = c["stories"]
    o.append(sec('      <div class="head"><h2 id="st-h">%s</h2></div>\n      %s' % (e(st["h2"]), note(st)),
                 "stratum--deep", "st-h"))
    ap = c["apply"]
    o.append(sec('      <div class="head"><h2 id="ap-h">%s</h2></div>\n%s      <p>%s</p>'
                 % (e(ap["h2"]), steps(ap["steps"], "i-scholarship"), cta(ap["cta"])), label="ap-h"))
    d = c["donorPanel"]
    o.append(sec('      <h2 id="dp-h">%s</h2>\n      <p class="lede">%s</p>\n      <p>%s</p>'
                 % (e(d["title"]), e(d["body"]), cta(d["cta"], "btn btn--donate")), "stratum--deep", "dp-h"))
    return MAIN("\n".join(o))


def p_webinars():
    c = load("webinars"); o = [hero(c["hero"], "web-h")]
    ns = c["nextSession"]
    o.append(sec('      <div class="head"><h2 id="ns-h">Next session</h2></div>\n      %s\n'
                 '      <p><a class="btn" href="https://webinar.soilfoodweb.com">%s</a></p>' % (note(ns), e(ns["cta"])),
                 "stratum--deep", "ns-h"))
    r = c["recordings"]
    o.append(sec('      <div class="head"><h2 id="rec-h">%s</h2></div>\n      %s\n      <p>%s <a href="%s">our community space</a></p>'
                 % (e(r["h2"]), note({"note": r["note"], "status": "placeholder"}), e(r["backlogLine"]), A(r["backlogHref"])),
                 label="rec-h"))
    res = c["resources"]
    o.append(sec('      <div class="head"><h2 id="fr-h">%s</h2></div>\n      <ul>%s</ul>'
                 % (e(res["h2"]), "".join("<li>%s</li>" % e(x) for x in res["items"])), "stratum--deep", "fr-h"))
    return MAIN("\n".join(o))


PAGES = [
    ("index.html", "Soil Food Web Foundation, a nonprofit teaching the science of living soil", "home", p_home),
    ("about.html", "About the Foundation, Soil Food Web Foundation", "about", p_about),
    ("learn.html", "Learn with us, Soil Food Web Foundation", "learn", p_learn),
    ("science.html", "How the soil food web works, Soil Food Web Foundation", "science", p_science),
    ("practice.html", "Practice, Soil Food Web Foundation", "practice", p_practice),
    ("community.html", "Community, Soil Food Web Foundation", "community", p_community),
    ("calendar.html", "Calendar, Soil Food Web Foundation", "calendar", p_calendar),
    ("news.html", "News and stories, Soil Food Web Foundation", "news", p_news),
    ("research.html", "Research, Soil Food Web Foundation", "research", p_research),
    ("login.html", "Student access, Soil Food Web Foundation", "login", p_login),
    ("donate.html", "Donate and get involved, Soil Food Web Foundation", "donate", p_donate),
    ("learn-scholarships.html", "Scholarships, Soil Food Web Foundation", "scholarships", p_scholarships),
    ("learn-webinars.html", "Free webinars, Soil Food Web Foundation", "webinars", p_webinars),
]

if __name__ == "__main__":
    for path, title, key, fn in PAGES:
        c = load(key)
        h = c.get("hero", {})
        desc = h.get("intro") or h.get("subhead") or title
        render(path, title, desc[:300], fn())
    print("done:", len(PAGES), "pages")
