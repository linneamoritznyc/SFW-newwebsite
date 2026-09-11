#!/usr/bin/env python3
"""Fetch openly licensed stand-in images into the repository.

    python3 tools/pd-assets.py --list
    python3 tools/pd-assets.py --fetch --out img/pd

Local mode only, and there is no other mode. It writes into this repository and
nowhere else. It does not touch Google Drive, it holds no credentials, and it
signs in to nothing: everything it reads is a public URL.

WHY IT REFUSES THINGS

A nonprofit cannot publish a photograph whose licence it cannot state. So the
rule here is the strict one: an item with no machine-readable licence is
skipped, loudly, and the run carries on. Nothing is saved on a guess.

Every file that is saved gets a row in <out>/CREDITS.json carrying the source
page, the direct file URL, the author as the source states it, and the licence
as the source states it. That file is the record, and docs/volunteer-visuals.md
points at it.

HOW TO ADD SOMETHING

Put a row in WANTED below. A row is what you want and where it goes, not a
filename: the point is that the next person can see what was being looked for.

  {"slot": "...",              # which slot on /volunteer this fills
   "need": "...",              # what the picture has to show
   "source": "commons",        # commons | nrcs | bhl | archive
   "query": "...",             # Commons search terms, or a page URL
   "name": "..."}              # the filename it lands under, no extension

Commons is the only source this script can resolve automatically, because it is
the only one of the four with a licence field in its API. NRCS, the Biodiversity
Heritage Library and the Internet Archive are listed for a human to work through
by hand: their rights statements are prose, per item, and a script that guessed
at them would be worse than no script.
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "SoilFoodWebFoundation-site-build/1.0 (https://soilfoodweb.org; static site asset fetch)"

COMMONS_API = "https://commons.wikimedia.org/w/api.php"

# Licences we will publish on a nonprofit's website without further thought.
# CC BY-SA is deliberately NOT here: it is a fine licence, but it can reach
# through into anything it is composited with, and these are decorative
# stand-ins, not the point of the page. Anything outside this set is a
# decision for a person, which is what the skip message says.
OK_LICENCES = {
    "cc0", "cc-zero", "pd", "public domain", "publicdomain",
    "pd-usgov", "pd-usgov-usda", "pd-old", "pd-old-100", "pd-art",
    "cc-by-2.0", "cc-by-3.0", "cc-by-4.0",
}

WANTED = [
    {"slot": "ladder, visual 2", "source": "commons", "name": "root-system",
     "need": "a whole root system, washed, on a plain ground, ideally already cut out",
     "query": "root system washed plant roots white background"},
    {"slot": "ladder, visual 3", "source": "commons", "name": "soil-profile-core",
     "need": "a soil profile or core photographed from the side, horizons visible",
     "query": "soil profile horizons pedon"},
    {"slot": "ten-minute band, visual 1", "source": "commons", "name": "nematode-micrograph",
     "need": "a soil nematode under brightfield, as a poster frame only",
     "query": "soil nematode micrograph"},
    {"slot": "ten-minute band, visual 1", "source": "commons", "name": "protozoa-micrograph",
     "need": "soil protozoa under brightfield",
     "query": "soil protozoa amoeba micrograph"},
    {"slot": "margins, visual 12", "source": "commons", "name": "moss-cutout",
     "need": "a single moss or lichen clump on a plain ground, to cut out",
     "query": "moss clump white background"},

    # Listed, not fetched: rights on these three are prose, per item.
    {"slot": "ten-minute band, visual 1", "source": "nrcs", "name": "soil-biology-primer",
     "need": "bacteria, fungi, protozoa and nematode plates from chapters 1 to 5",
     "query": "https://www.nrcs.usda.gov/resources/education-and-teaching-materials/soil-biology-primer"},
    {"slot": "role cards, visual 8", "source": "bhl", "name": "root-engraving",
     "need": "an engraved root or soil-fauna plate to sit behind a role card",
     "query": "https://www.biodiversitylibrary.org/"},
    {"slot": "hero, visual 7", "source": "archive", "name": "usda-field-film",
     "need": "USDA extension field footage, as a stand-in for the drone move",
     "query": "https://archive.org/details/usda"},
]


def get(url, params=None, binary=False, timeout=30):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    return data if binary else json.loads(data.decode("utf-8"))


def commons_pick(query):
    """Search Commons and return the first hit whose licence we will publish.

    Returns (info, skipped) where skipped lists what was passed over and why,
    so a run that finds nothing still tells you what it looked at.
    """
    skipped = []
    hits = get(COMMONS_API, {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": "filetype:bitmap " + query, "gsrnamespace": "6", "gsrlimit": "12",
        "prop": "imageinfo", "iiprop": "url|extmetadata|size",
    })
    pages = (hits.get("query") or {}).get("pages") or {}
    for page in sorted(pages.values(), key=lambda p: p.get("index", 99)):
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata") or {}
        lic = (meta.get("LicenseShortName", {}).get("value")
               or meta.get("License", {}).get("value") or "").strip()
        author = (meta.get("Artist", {}).get("value") or "").strip()
        if not lic:
            skipped.append((page.get("title", "?"), "no licence field"))
            continue
        key = lic.lower().replace(" ", "-")
        if not any(k in key or k == lic.lower() for k in OK_LICENCES):
            skipped.append((page.get("title", "?"), "licence '%s' needs a person to decide" % lic))
            continue
        if info.get("width", 0) < 1000:
            skipped.append((page.get("title", "?"), "too small (%spx)" % info.get("width")))
            continue
        return {
            "title": page.get("title"),
            "url": info.get("url"),
            "page": info.get("descriptionurl"),
            "author_html": author,
            "licence": lic,
            "width": info.get("width"),
        }, skipped
    return None, skipped


def strip_tags(s):
    out, keep = [], True
    for ch in s:
        if ch == "<":
            keep = False
        elif ch == ">":
            keep = True
        elif keep:
            out.append(ch)
    return " ".join("".join(out).split())


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--list", action="store_true", help="print what would be fetched, fetch nothing")
    ap.add_argument("--fetch", action="store_true", help="fetch into --out")
    ap.add_argument("--out", default="img/pd", help="directory inside the repo (default img/pd)")
    a = ap.parse_args()

    if not (a.list or a.fetch):
        ap.print_help()
        return 2

    if a.list:
        for w in WANTED:
            print("%-28s %-9s %s" % (w["slot"], w["source"], w["need"]))
            print("%-28s %-9s %s" % ("", "", w["query"]))
        print("\nOnly the 'commons' rows can be resolved by this script. The nrcs, bhl and")
        print("archive rows are for a person: their rights statements are prose, per item.")
        return 0

    out = os.path.join(ROOT, a.out)
    if not os.path.abspath(out).startswith(ROOT + os.sep):
        sys.exit("--out must be inside the repository. Nothing is written anywhere else.")
    os.makedirs(out, exist_ok=True)

    credits_path = os.path.join(out, "CREDITS.json")
    credits = {}
    if os.path.exists(credits_path):
        with open(credits_path, encoding="utf-8") as f:
            credits = json.load(f)

    saved = skipped = failed = 0
    for w in WANTED:
        if w["source"] != "commons":
            print("SKIP  %-22s %s: check the rights by hand, then add the file" % (w["name"], w["source"]))
            skipped += 1
            continue
        try:
            pick, passed_over = commons_pick(w["query"])
        except Exception as err:                      # network, proxy, API, all the same to us
            print("FAIL  %-22s %s" % (w["name"], err))
            failed += 1
            continue
        for title, why in passed_over:
            print("      passed over %s: %s" % (title, why))
        if not pick:
            print("SKIP  %-22s nothing with a licence we can publish" % w["name"])
            skipped += 1
            continue

        ext = os.path.splitext(urllib.parse.urlparse(pick["url"]).path)[1].lower() or ".jpg"
        name = w["name"] + ext
        try:
            blob = get(pick["url"], binary=True, timeout=90)
        except Exception as err:
            print("FAIL  %-22s %s" % (name, err))
            failed += 1
            continue
        with open(os.path.join(out, name), "wb") as f:
            f.write(blob)
        credits[name] = {
            "slot": w["slot"],
            "need": w["need"],
            "source_page": pick["page"],
            "file_url": pick["url"],
            "author": strip_tags(pick["author_html"]) or "not stated on the source page",
            "licence": pick["licence"],
            "fetched_by": "tools/pd-assets.py",
        }
        print("SAVED %-22s %s  (%s)" % (name, pick["licence"], pick["page"]))
        saved += 1

    with open(credits_path, "w", encoding="utf-8") as f:
        json.dump(credits, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("\n%d saved, %d skipped, %d failed. Credits in %s" % (saved, skipped, failed, credits_path))
    print("Copy each row into the table in docs/volunteer-visuals.md before using the file,")
    print("and put the credit on the page beside the picture.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
