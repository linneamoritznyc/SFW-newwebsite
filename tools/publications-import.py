#!/usr/bin/env python3
"""Fold a publications import sheet into content/research.json.

    python3 tools/publications-import.py sfwpublicationsimport.csv

Authoring aid, run by hand when a new sheet arrives. It rewrites only the
"database" object's entries, counts and chip lists; the surrounding copy
(lede, source line, Google Scholar link, notes) stays as it is in the JSON
so an import never silently rewrites words someone wrote. Then run
tools/build.py to render research.html.

Sheet columns, Alex's template: id, title, status, year, type, collection,
topics, authors, citation, summary, content, external_url, source_url, slug.
Empty external_url means no stable link was found, and that entry is listed
by citation alone.
"""
import csv, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(ROOT, "content", "research.json")

# sheet collection -> chip slug, chip label. The label is what a reader sees;
# "Other relevant publications" is the sheet's word, not the site's.
COLLECTIONS = [("Dr. Elaine's publications", "elaine", "Dr. Elaine’s publications"),
               ("Other relevant publications", "field", "Soil food web science"),
               ("Internet articles", "internet", "Internet articles")]
SLUG = {c: s for c, s, _ in COLLECTIONS}
ORDER = {c: i for i, (c, _, _) in enumerate(COLLECTIONS)}
MONTHS = ("January February March April May June July August September "
          "October November December").split()


def curly(s):
    return (s or "").strip().replace("'", "’")


def full_date(citation):
    """Internet articles carry their publication date in the citation column."""
    m = re.match(r"^([A-Z][a-z]+) (\d{1,2}), (\d{4})$", (citation or "").strip())
    if not m or m.group(1) not in MONTHS:
        return None
    return ("%s-%02d-%02d" % (m.group(3), MONTHS.index(m.group(1)) + 1, int(m.group(2))),
            "%d %s %s" % (int(m.group(2)), m.group(1), m.group(3)))


def decade(year):
    return ("pre1980", "Before 1980") if year < 1980 else (("%ds" % (year // 10 * 10),) * 2)


def main(path):
    with open(path, encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("title") or "").strip()]
    unknown = {r["collection"] for r in rows} - set(SLUG)
    if unknown:
        sys.exit("unknown collection(s) in the sheet: %s" % ", ".join(sorted(unknown)))

    entries = []
    for r in sorted(rows, key=lambda r: (-int(r["year"]), ORDER[r["collection"]], r["title"].lower())):
        year = int(r["year"])
        d = full_date(r["citation"]) if r["collection"] == "Internet articles" else None
        x = {"title": curly(r["title"]),
             "collection": SLUG[r["collection"]],
             "type": "USDA publication" if r["type"] == "USDA" else r["type"],
             "decade": decade(year)[0],
             "datetime": d[0] if d else str(year),
             "dated": d[1] if d else str(year)}
        if r["authors"].strip():
            x["authors"] = curly(r["authors"])
        if r["citation"].strip() and not d:
            x["citation"] = curly(r["citation"])
        if r["external_url"].strip():
            x["url"] = r["external_url"].strip()
        entries.append(x)

    with open(TARGET, encoding="utf-8") as f:
        c = json.load(f)
    db = c["database"]
    db["entries"] = entries
    db["collections"] = [{"slug": s, "label": lbl,
                          "count": sum(1 for r in rows if r["collection"] == coll)}
                         for coll, s, lbl in COLLECTIONS]
    seen = {}
    for r in rows:
        seen.setdefault(*decade(int(r["year"])))
    db["decades"] = [{"slug": s, "label": seen[s]} for s in
                     sorted(seen, key=lambda s: -(1979 if s == "pre1980" else int(s[:4])))]

    linked = sum(1 for x in entries if x.get("url"))
    db["counts"] = ("%d entries. %d link to the publisher record, the journal or a "
                    "repository copy; the remaining %d are listed by citation because "
                    "no stable link was found." % (len(entries), linked, len(entries) - linked))

    with open(TARGET, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("%d entries, %d linked, %d citation only -> content/research.json"
          % (len(entries), linked, len(entries) - linked))
    print("check db['counts'], db['source'] and db['notes'] by hand, then run tools/build.py")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
