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

# Printed at the foot of every trial page, word for word, on every entry.
STANDING = ("This is one trial, on one site, in one set of conditions. It shows what happened "
            "there. Soil is local, and yours will differ.")


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
        where = ", ".join(x for x in (t.get("location", "").strip(), t.get("country", "").strip()) if x)
        line = ". ".join(x for x in (where, t.get("crop", "").strip()) if x)
        result = t.get("result", "").strip()
        mid = '<h3 class="entry__t"><a href="%s">%s</a></h3>' % (A(href), e(title_of(t)))
        if line:
            mid += '<p class="entry__line">%s</p>' % e(line)
        if result:
            mid += '<p class="entry__line">%s</p>' % e(result)
        return ('        <li class="entry"%s>\n'
                '          <span class="entry__kind" style="text-align:left">%s</span>\n'
                '          <div>%s</div>\n'
                '          <span class="entry__kind">%s</span>\n'
                '        </li>\n' % (attrs, e(t.get("country", "").strip()), mid,
                                     e(t.get("duration", "").strip())))
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
             '        <h1 id="ft-h">Field results</h1>\n'
             '        <p class="lede" data-source="Age of the published case study material, as at September 2026">'
             'Dr. Elaine Ingham\u2019s case studies convinced a generation that biology could do what chemistry was '
             'doing, and more cheaply. Some of that data is now fifteen years old.</p>\n'
             '        <p>So our Advanced Programme students run their own trials, on their own land, and write down '
             'what happened. Site, method, how long it ran, what was measured, what changed. Some worked. Some did '
             'not, and those are here too, because a method that only ever reports its successes is not being '
             'tested.</p>\n'
             '      </div>\n    </div>\n  </section>\n')

    body = "".join(row(t) for t in trials)
    empty_note = ""
    if not live:
        empty_note = ('      <p class="awaiting">No trial is published here yet. The reports exist and circulate '
                      'inside the Advanced Programme. Each one needs its author\u2019s permission and a check of the '
                      'raw measurements before it goes on a public page.</p>\n')
    o.append('  <section class="stratum" aria-labelledby="ft-list">\n    <div class="wrap">\n'
             '      <h2 id="ft-list" class="visually-hidden">The trials</h2>\n'
             '%s'
             '      <ul class="rule-list" id="trials">\n%s'
             '        <li class="feed__empty" data-filter-empty hidden>Nothing matches that combination. '
             'Clear a filter to see the rest.</li>\n'
             '      </ul>\n%s'
             '      <p class="todo">Three placeholder entries in data/field-trials.json. Real reports pending from '
             'the Advanced Programme team.</p>\n'
             '    </div>\n  </section>\n' % (chips(trials), body, empty_note))

    o.append('  <section class="stratum stratum--deep" aria-labelledby="ft-next">\n    <div class="wrap">\n'
             '      <h2 id="ft-next" class="visually-hidden">Next step</h2>\n'
             '      <p class="lede">Our Advanced Programme graduates run these trials as part of their training.</p>\n'
             '      <p><a class="btn" href="learn?utm_source=website&amp;utm_medium=evidence&amp;utm_campaign=evidence-field-trials">Learn about the Advanced Programme</a></p>\n'
             '    </div>\n  </section>\n')
    return build.MAIN("".join(o))


def detail(t):
    """One trial page, in the order the copy deck sets: who and where, crop,
    method, duration, what was measured, result, the practitioner's own words,
    and the standing note that every one of these pages carries."""
    rows = [(k, t.get(v, "").strip()) for k, v in (
        ("Practitioner", "practitioner"), ("Location", "location"), ("Country", "country"),
        ("Climate", "climate"), ("Site type", "site_type"), ("Crop", "crop"),
        ("Method used", "method"), ("Duration", "duration"))]
    rows = [(k, v) for k, v in rows if v]

    o = []
    o.append('  <section class="stratum" style="border-top:0;padding-top:var(--s5)">\n    <div class="wrap">\n'
             '      <div class="head" style="margin-bottom:0">\n'
             '        <p class="eyebrow">FIELD RESULTS</p>\n'
             '        <h1 id="t-h">%s</h1>\n'
             '      </div>\n    </div>\n  </section>\n' % e(title_of(t)))

    if rows:
        o.append('  <section class="stratum" aria-labelledby="t-site">\n    <div class="wrap">\n'
                 '      <h2 id="t-site" class="visually-hidden">The trial</h2>\n'
                 '%s    </div>\n  </section>\n'
                 % build.facts([{"k": k, "v": v} for k, v in rows]))

    ms = t.get("measurements") or []
    if ms:
        rowsm = "".join(
            '          <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n'
            % (e(m.get("what", "")), e(m.get("before", "")), e(m.get("after", "")), e(m.get("method", "")))
            for m in ms)
        o.append('  <section class="stratum stratum--deep" aria-labelledby="t-meas">\n    <div class="wrap">\n'
                 '      <div class="head"><h2 id="t-meas">What was measured</h2></div>\n'
                 '      <table class="data-table">\n'
                 '        <thead><tr><th>Measure</th><th>At the start</th><th>At the end</th><th>How</th></tr></thead>\n'
                 '        <tbody>\n%s        </tbody>\n      </table>\n'
                 '      <p class="source small">%s</p>\n'
                 '    </div>\n  </section>\n' % (rowsm, e(t.get("_source", "The practitioner\u2019s own trial report."))))

    res = t.get("result", "").strip()
    if res:
        o.append('  <section class="stratum" aria-labelledby="t-res">\n    <div class="wrap">\n'
                 '      <div class="head"><h2 id="t-res">Result</h2></div>\n'
                 '      <div class="prose"><p>%s</p></div>\n    </div>\n  </section>\n' % e(res))

    con = t.get("conclusion", "").strip()
    if con:
        o.append('  <section class="stratum stratum--deep" aria-labelledby="t-words">\n    <div class="wrap">\n'
                 '      <div class="head"><h2 id="t-words">In their words</h2></div>\n'
                 '      <figure class="testimonial"><blockquote><p>%s</p></blockquote>\n'
                 '        <figcaption>%s</figcaption>\n      </figure>\n'
                 '    </div>\n  </section>\n'
                 % (e(con), e(t.get("practitioner", "").strip() or "The practitioner")))

    imgs = t.get("images") or []
    if imgs:
        li = "".join('        <li><figure class="shot">%s</figure></li>\n'
                     % build.img(i.get("src", ""), i.get("alt", ""), depth=1) for i in imgs)
        o.append('  <section class="stratum" aria-labelledby="t-img">\n    <div class="wrap">\n'
                 '      <div class="head"><h2 id="t-img">The site, photographed</h2></div>\n'
                 '      <ul class="faces">\n%s      </ul>\n    </div>\n  </section>\n' % li)

    if not published(t):
        o.append('  <section class="stratum" aria-labelledby="t-hold">\n    <div class="wrap">\n'
                 '      <div class="head"><h2 id="t-hold">This trial is not published yet</h2></div>\n'
                 '      <p class="awaiting">This page is the shape a trial takes on this site. It holds no '
                 'findings. It is here so the structure can be reviewed before the first real report arrives.</p>\n'
                 '      %s\n      <p class="todo">Owner: %s.</p>\n    </div>\n  </section>\n'
                 % (note(t), e(t.get("owner", "unassigned"))))

    # The standing note, on every trial page, whatever else is on it.
    o.append('  <section class="stratum stratum--deep" aria-labelledby="t-next">\n    <div class="wrap">\n'
             '      <p class="aside-note">%s</p>\n'
             '      <h2 id="t-next" class="visually-hidden">Next step</h2>\n'
             '      <p style="margin-top:var(--s4)"><a class="btn" href="../evidence-field-trials">'
             'All field results</a></p>\n'
             '    </div>\n  </section>\n' % e(STANDING))
    return build.MAIN("".join(o))


def main():
    trials = load()
    os.makedirs(os.path.join(ROOT, OUT_DIR), exist_ok=True)
    build.render(
        INDEX,
        "Field results | Soil Food Web Foundation",
        "Trials run by our graduates on their own land, with site, method, duration, measurements and outcome recorded.",
        index(trials), depth=0, share="img/soil-sample-shovel-and-bag.jpg", tone="t-practice")
    for t in trials:
        build.render(
            "%s/%s.html" % (OUT_DIR, t["slug"]),
            "%s | Soil Food Web Foundation" % title_of(t),
            "One trial, on one site: method, duration, what was measured and what changed.",
            detail(t), depth=1, share="img/soil-sample-shovel-and-bag.jpg", tone="t-practice")
    print("done:", len(trials) + 1, "pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
