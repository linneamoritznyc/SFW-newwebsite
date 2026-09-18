#!/usr/bin/env python3
"""Render the field trial pages from data/field-trials.json.

    python3 tools/fieldtrials.py

Same shape as tools/build.py, and it borrows that script's chrome so the
header, footer and share tags on these pages are the ones every other page
carries. Copy lives in the JSON, markup lives here.

Two outputs:

    evidence-field-trials.html          the index, filterable by crop,
                                        climate and country
    evidence-field-trials/<slug>.html   one page per entry

Students on the Advanced Programs run trials on real land and write the
results up. A report is about one site. It says what was measured there and
what changed. It is never turned into a claim about the method as a whole,
so no template here writes a sentence the data did not supply, and an entry
whose status is "placeholder" prints nothing but its own placeholder note.

The filter chips are generated from the values present in the data. A facet
with nothing in it prints no chips rather than a row of empty buttons, and
the page says so where ?notes=1 is on. Filtering is progressive enhancement:
with JavaScript off every entry is simply listed.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build  # noqa: E402  (same directory, deliberately)

ROOT = build.ROOT
OUT_DIR = "evidence-field-trials"
INDEX = "evidence-field-trials.html"

e, A, note = build.e, build.A, build.note

# The campaign tag every outbound course and event link on the evidence pages
# carries, so the Foundation can tell which page sent someone.
UTM = "?utm_source=website&utm_medium=evidence&utm_campaign=%s"

FACETS = [("crop", "Crop"), ("climate", "Climate"), ("country", "Country")]

# Printed on the index and on every entry. A trial is one site.
SCOPE = ("Each report covers one site. It says what was measured there and what changed. "
         "It is not a statement about what happens on other land.")


def load():
    with open(os.path.join(ROOT, "data", "field-trials.json"), encoding="utf-8") as f:
        return json.load(f)["trials"]


def token(v):
    """"Mediterranean, dry summer" -> "mediterranean-dry-summer".

    The filter script reads an attribute as a space separated list of keys, so
    a value with a space in it would answer to two chips that do not exist.
    """
    return re.sub(r"[^a-z0-9]+", "-", str(v).lower()).strip("-")


def human(s):
    """"example-orchard-transition" -> "Example orchard transition"."""
    return re.sub(r"-+", " ", s).strip().capitalize()


def title_of(t):
    """The heading for an entry.

    Once a report names its practitioner and its place, those are the heading:
    they are what a reader is looking for. Until then the slug stands in, and
    nothing is invented to fill the gap.
    """
    who, where = t.get("practitioner", "").strip(), t.get("location", "").strip()
    if who and where:
        return "%s, %s" % (who, where)
    return who or where or human(t["slug"])


def published(t):
    return t.get("status") != "placeholder"


def values(trials, key):
    """Distinct non-empty values for one facet, in the order they first appear."""
    out = []
    for t in trials:
        v = str(t.get(key, "")).strip()
        if v and v not in out:
            out.append(v)
    return out


def chips(trials):
    """One chip row per facet that has something to filter by.

    A facet with fewer than two distinct values would give a row of buttons
    that cannot change the list, so it prints nothing and says why under
    ?notes=1 instead.
    """
    out, empty = "", []
    for key, label in FACETS:
        vals = values([t for t in trials if published(t)], key)
        if len(vals) < 2:
            empty.append(label.lower())
            continue
        li = '<li><button class="chip" type="button" data-filter="all" aria-pressed="true">All</button></li>'
        li += "".join('<li><button class="chip" type="button" data-filter="%s" aria-pressed="false">%s</button></li>'
                      % (A(token(v)), e(v)) for v in vals)
        out += ('      <ul class="chips" data-filter-for="#trials" data-filter-attr="data-%s" aria-label="%s">%s'
                '<li class="small" data-filter-status style="align-self:center;color:var(--ink-faint)"></li></ul>\n'
                % (A(key), A(label), li))
    if empty:
        out += ('      <p class="todo">Filters for %s appear here as soon as published entries carry those '
                'values. They are generated from data/field-trials.json, so nothing needs editing by hand.</p>\n'
                % e(", ".join(empty)))
    return out


def row(t):
    """One entry in the index list."""
    href = "%s/%s" % (OUT_DIR, t["slug"])
    meta = [t.get(k, "").strip() for k in ("site_type", "crop", "location", "country", "duration")]
    meta = ", ".join(x for x in meta if x)
    # .entry is a three column row: kind on the left, title and line in the
    # middle, kind on the right. A row with one child lands in the 10rem first
    # column and reads as a broken list, so every row fills all three.
    if published(t):
        attrs = "".join(' data-%s="%s"' % (k, A(token(t.get(k, "")))) for k, _ in FACETS if str(t.get(k, "")).strip())
        line = '<p class="entry__line">%s</p>' % e(meta) if meta else ""
        return ('        <li class="entry"%s>\n'
                '          <span class="entry__kind" style="text-align:left">%s</span>\n'
                '          <div><h3 class="entry__t"><a href="%s">%s</a></h3>%s</div>\n'
                '          <span class="entry__kind">%s</span>\n'
                '        </li>\n' % (attrs, e(t.get("country", "").strip()), A(href),
                                     e(title_of(t)), line, e(t.get("duration", "").strip())))
    # A placeholder is structure, not content. Visitors see nothing; ?notes=1
    # shows the shell so the layout can be reviewed before real data arrives.
    return ('        <li class="entry notes-only">\n'
            '          <span class="entry__kind" style="text-align:left">Not published</span>\n'
            '          <div><h3 class="entry__t"><a href="%s">%s</a></h3>\n'
            '          %s</div>\n'
            '          <span></span>\n'
            '        </li>\n' % (A(href), e(title_of(t)), note(t)))


def index(trials):
    live = [t for t in trials if published(t)]
    o = []
    o.append('  <section class="stratum" style="border-top:0;padding-top:var(--s5)">\n    <div class="wrap">\n'
             '      <div class="head" style="margin-bottom:0">\n'
             '        <p class="eyebrow">EVIDENCE</p>\n'
             '        <h1 id="ft-h">Field trial results</h1>\n'
             '        <p class="lede">Students on our advanced programs run trials on real land and write up what '
             'they measured. The reports below are theirs. Each one names the site, the practice, the instrument '
             'and the numbers, so you can judge the work rather than take our word for it.</p>\n'
             '      </div>\n    </div>\n  </section>\n')

    o.append('  <section class="stratum" aria-labelledby="ft-what">\n    <div class="wrap">\n'
             '      <div class="grid">\n        <div class="span-6">\n'
             '          <h2 id="ft-what">What a report contains</h2>\n'
             '          <p>A practitioner picks a site, records its starting condition, applies a practice, and '
             'measures the same things again after a stated period. The report gives the site, the climate, the '
             'crop, the method, the duration, what was measured and how, and what changed.</p>\n'
             '          <p>%s</p>\n        </div>\n'
             '        <div class="span-5 start-8">\n'
             '          <h2>Why these and not the old case studies</h2>\n'
             '          <p>The case study material the Foundation has published for years was gathered around '
             'fifteen years ago. These reports are current, they are written by the people who did the work, and '
             'the measurements behind them can be checked.</p>\n'
             '        </div>\n      </div>\n    </div>\n  </section>\n' % e(SCOPE))

    body = "".join(row(t) for t in trials)
    empty_note = ""
    if not live:
        empty_note = ('      <p class="awaiting">No field trial report is published here yet. The reports exist and '
                      'circulate inside the advanced programs. Each one needs its author\'s written permission and a '
                      'check of the raw measurements before it goes on a public page, and that is in hand.</p>\n')
    o.append('  <section class="stratum stratum--deep" aria-labelledby="ft-list">\n    <div class="wrap">\n'
             '      <div class="head"><h2 id="ft-list">The reports</h2></div>\n'
             '%s'
             '      <ul class="rule-list" id="trials">\n%s'
             '        <li class="feed__empty" data-filter-empty hidden>Nothing matches that combination. '
             'Clear a filter to see the rest.</li>\n'
             '      </ul>\n%s    </div>\n  </section>\n' % (chips(trials), body, empty_note))

    o.append('  <section class="stratum" aria-labelledby="ft-next">\n    <div class="wrap">\n'
             '      <h2 id="ft-next">Next step</h2>\n'
             '      <p class="lede">These trials are coursework on our advanced programs. See what those programs '
             'ask of you before you enrol.</p>\n'
             '      <p><a class="btn" href="learn">See the advanced programs</a></p>\n'
             '    </div>\n  </section>\n')
    return build.MAIN("".join(o))


def detail(t):
    rows = [(k, t.get(v, "").strip()) for k, v in (
        ("Practitioner", "practitioner"), ("Place", "location"), ("Country", "country"),
        ("Climate", "climate"), ("Site", "site_type"), ("Crop", "crop"),
        ("Practice applied", "method"), ("Over", "duration"))]
    rows = [(k, v) for k, v in rows if v]

    o = []
    o.append('  <section class="stratum" style="border-top:0;padding-top:var(--s5)">\n    <div class="wrap">\n'
             '      <div class="head" style="margin-bottom:0">\n'
             '        <p class="eyebrow">FIELD TRIAL</p>\n'
             '        <h1 id="t-h">%s</h1>\n'
             '        <p class="lede">%s</p>\n'
             '      </div>\n    </div>\n  </section>\n' % (e(title_of(t)), e(SCOPE)))

    if rows:
        o.append('  <section class="stratum" aria-labelledby="t-site">\n    <div class="wrap">\n'
                 '      <div class="head"><h2 id="t-site">The site</h2></div>\n'
                 '%s    </div>\n  </section>\n'
                 % build.facts([{"k": k, "v": v} for k, v in rows]))

    ms = t.get("measurements") or []
    if ms:
        body = "".join(
            '          <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n'
            % (e(m.get("what", "")), e(m.get("before", "")), e(m.get("after", "")), e(m.get("method", "")))
            for m in ms)
        o.append('  <section class="stratum stratum--deep" aria-labelledby="t-meas">\n    <div class="wrap">\n'
                 '      <div class="head"><h2 id="t-meas">What was measured</h2></div>\n'
                 '      <table class="data-table">\n'
                 '        <thead><tr><th>Measure</th><th>At the start</th><th>At the end</th><th>How</th></tr></thead>\n'
                 '        <tbody>\n%s        </tbody>\n      </table>\n'
                 '      <p class="source small">%s</p>\n'
                 '    </div>\n  </section>\n' % (body, e(t.get("_source", "Practitioner's own field trial report."))))

    for hid, head, key in (("t-res", "What changed", "result"), ("t-con", "What the practitioner concluded", "conclusion")):
        v = t.get(key, "").strip()
        if v:
            o.append('  <section class="stratum" aria-labelledby="%s">\n    <div class="wrap">\n'
                     '      <div class="head"><h2 id="%s">%s</h2></div>\n      <div class="prose"><p>%s</p></div>\n'
                     '    </div>\n  </section>\n' % (hid, hid, e(head), e(v)))

    imgs = t.get("images") or []
    if imgs:
        li = "".join('        <li><figure class="shot">%s</figure></li>\n'
                     % build.img(i.get("src", ""), i.get("alt", ""), depth=1) for i in imgs)
        o.append('  <section class="stratum stratum--deep" aria-labelledby="t-img">\n    <div class="wrap">\n'
                 '      <div class="head"><h2 id="t-img">The site, photographed</h2></div>\n'
                 '      <ul class="faces">\n%s      </ul>\n    </div>\n  </section>\n' % li)

    if not published(t):
        o.append('  <section class="stratum" aria-labelledby="t-hold">\n    <div class="wrap">\n'
                 '      <div class="head"><h2 id="t-hold">This report is not published yet</h2></div>\n'
                 '      <p class="awaiting">This page is the shape a field trial report takes on this site. It '
                 'holds no findings. It is here so the structure can be reviewed before the first real report '
                 'arrives.</p>\n      %s\n'
                 '      <p class="todo">Owner: %s.</p>\n    </div>\n  </section>\n'
                 % (note(t), e(t.get("owner", "unassigned"))))

    o.append('  <section class="stratum stratum--deep" aria-labelledby="t-next">\n    <div class="wrap">\n'
             '      <h2 id="t-next">Next step</h2>\n'
             '      <p class="lede">Read the rest of the reports.</p>\n'
             '      <p><a class="btn" href="../evidence-field-trials">All field trial results</a></p>\n'
             '    </div>\n  </section>\n')
    return build.MAIN("".join(o))


def main():
    trials = load()
    os.makedirs(os.path.join(ROOT, OUT_DIR), exist_ok=True)
    build.render(
        INDEX,
        "Field trial results, Soil Food Web Foundation",
        "Trials run on real land by students on our advanced programs, with what was measured and what changed.",
        index(trials), depth=0, share="img/soil-sample-shovel-and-bag.jpg", tone="t-practice")
    for t in trials:
        build.render(
            "%s/%s.html" % (OUT_DIR, t["slug"]),
            "%s, field trial, Soil Food Web Foundation" % title_of(t),
            "One field trial: the site, what was measured, and what changed.",
            detail(t), depth=1, share="img/soil-sample-shovel-and-bag.jpg", tone="t-practice")
    print("done:", len(trials) + 1, "pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
