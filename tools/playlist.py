#!/usr/bin/env python3
"""Read the WordPress video playlists, verify every video, write content/videos.json.

    pip install requests beautifulsoup4
    python3 tools/playlist.py                 # scrape, verify, fetch thumbnails
    python3 tools/playlist.py --verify-only   # re-check what is already in the file

RUN THIS LOCALLY. Like crawl.py, it needs soilfoodweb.com and vimeo.com, and
the cloud sandbox has no route to either.

WHY THIS EXISTS

The old playlist is five bugs, and four of them are one bug: the private
hash is carried in the URL and keeps getting lost.

  1. The videos are unlisted, so each one only plays with its own h= code.
     The page copies h from the query string into the player, so a link
     without h hands the player "?h=" and Vimeo refuses.
  2. One link has the hash pasted inside the id: vID=372925873%3Fh%3D707aa77aa3.
  3. The canonical URL carries no vID at all, so anyone arriving from a
     search engine gets an empty player.
  4. The items link to paths that 301 before they load.
  5. Every click reloads WordPress and boots a new player from zero.

Putting the hash in a data file fixes 1, 2 and 3 at the source: it is
written once, by a machine, from the page that already works, and checked
against Vimeo before it is committed. 4 disappears because the new site has
no /resources/ prefix to lose. 5 is fixed in the player itself, in
js/site.js job 11, which never reloads the page.

WHAT VERIFICATION MEANS

    https://vimeo.com/api/oembed.json?url=https://vimeo.com/ID/HASH

returns 200 with a title, a duration and a thumbnail for a video that will
play, and 403 or 404 for one whose hash is wrong or which has been made
private. Every entry is checked before it is written, so a broken video is
found here rather than by a visitor.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse as up

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "content", "videos.json")
THUMBS = os.path.join(ROOT, "img", "video")
UA = {"User-Agent": "SFWF-rebuild-playlist/1.0 (linnea@soilfoodweb.com)"}
OEMBED = "https://vimeo.com/api/oembed.json"


def need(mod):
    try:
        return __import__(mod)
    except ImportError:
        sys.exit("pip install requests beautifulsoup4   (missing: %s)" % mod)


requests = need("requests")
need("bs4")
from bs4 import BeautifulSoup  # noqa: E402


def slugify(*parts):
    t = " ".join(p for p in parts if p)
    t = t.replace("’", "").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:60]


def parse_link(href):
    """?vID=537966540&h=a79eb5d201 -> ("537966540", "a79eb5d201")

    Also survives the mangled form, where the hash was pasted into the id:
    ?vID=372925873%3Fh%3D707aa77aa3. Unquoting first turns that back into
    372925873?h=707aa77aa3, and the id is then everything before the ?.
    """
    q = up.parse_qs(up.urlparse(up.unquote(href)).query)
    vid = (q.get("vID") or q.get("vid") or [""])[0]
    h = (q.get("h") or [""])[0]
    if "?" in vid:
        vid, _, tail = vid.partition("?")
        h = h or up.parse_qs(tail).get("h", [""])[0]
    vid = re.sub(r"\D", "", vid)
    return (vid, h.strip()) if vid else (None, None)


def text_near(a):
    """Title, subtitle and person as the markup gives them, nothing invented.

    The playlist items are anchors wrapping a thumbnail and one to three
    lines of text. Which line is which varies between the pages, so the
    first line is the title and anything after it is kept in order.
    """
    lines = [t.strip() for t in a.stripped_strings if t.strip()]
    lines = [l for l in lines if not l.lower().startswith("watch")]
    title = lines[0] if lines else ""
    rest = lines[1:]
    return title, (rest[0] if rest else ""), (rest[1] if len(rest) > 1 else "")


def scrape(page):
    r = requests.get(page, headers=UA, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    out, seen = [], set()
    for a in soup.find_all("a", href=True):
        vid, h = parse_link(a["href"])
        if not vid or vid in seen:
            continue
        seen.add(vid)
        title, subtitle, person = text_near(a)
        img = a.find("img")
        src = ""
        if img:
            src = img.get("data-src") or img.get("src") or ""
            if src and "data:image" in src:                 # lazyload shim
                src = img.get("data-lazy-src") or img.get("data-srcset", "").split(" ")[0] or ""
        out.append({"id": vid, "hash": h, "title": title, "subtitle": subtitle,
                    "person": person, "remote_thumb": up.urljoin(page, src) if src else "",
                    "source": page})
    # The iframe holds the video the page opened with, which is sometimes the
    # only place a hash appears in one piece.
    for f in soup.find_all("iframe", src=True):
        if "player.vimeo.com" not in f["src"]:
            continue
        m = re.search(r"/video/(\d+)", f["src"])
        h = up.parse_qs(up.urlparse(f["src"]).query).get("h", [""])[0]
        if m and h:
            for it in out:
                if it["id"] == m.group(1) and not it["hash"]:
                    it["hash"] = h
    return out


def verify(item):
    """200 with a title means it plays. Anything else means it does not."""
    url = "https://vimeo.com/%s/%s" % (item["id"], item["hash"]) if item["hash"] \
        else "https://vimeo.com/%s" % item["id"]
    try:
        r = requests.get(OEMBED, params={"url": url, "width": 1280}, headers=UA, timeout=30)
    except requests.RequestException as exc:
        return None, str(exc)
    if r.status_code != 200:
        return None, "oembed %d for %s" % (r.status_code, url)
    return r.json(), None


def fetch_thumb(url, slug):
    os.makedirs(THUMBS, exist_ok=True)
    dst = os.path.join(THUMBS, slug + ".jpg")
    if os.path.exists(dst):
        return "img/video/" + slug + ".jpg"
    try:
        r = requests.get(url, headers=UA, timeout=30)
        r.raise_for_status()
    except requests.RequestException:
        return ""
    with open(dst, "wb") as f:
        f.write(r.content)
    return "img/video/" + slug + ".jpg"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify-only", action="store_true",
                    help="re-check the videos already in content/videos.json")
    args = ap.parse_args()

    data = json.load(open(DATA, encoding="utf-8"))
    broken, kept = [], 0

    for pl in data["playlists"]:
        items = pl["items"] if args.verify_only else scrape(pl["page"])
        if not args.verify_only:
            print("%-26s %s  %d links" % (pl["id"], pl["page"], len(items)))
        out = []
        for it in items:
            meta, err = verify(it)
            slug = it.get("slug") or slugify(it.get("person"), it.get("title") or it["id"])
            if err:
                broken.append((pl["id"], slug, it["id"], it.get("hash") or "NO HASH", err))
                continue
            entry = {
                "slug": slug,
                "id": it["id"],
                "hash": it["hash"],
                # The playlist markup is the better title where it has one:
                # oembed returns whatever the video was named on upload.
                "title": it.get("title") or meta.get("title", ""),
                "subtitle": it.get("subtitle", ""),
                "person": it.get("person", ""),
                "duration": meta.get("duration"),
                "thumb": fetch_thumb(it.get("remote_thumb") or meta.get("thumbnail_url", ""), slug),
                "source": it.get("source", pl["page"]),
            }
            out.append(entry)
            kept += 1
            time.sleep(0.3)                    # be polite to both hosts
        pl["items"] = out
        print("  kept %d" % len(out))

    data["_state"] = "Written by tools/playlist.py on %s. Every entry verified against Vimeo oembed." \
        % time.strftime("%d %B %Y")
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("\n%d videos written to content/videos.json" % kept)
    if broken:
        print("\n%d WILL NOT PLAY, and are not in the file:" % len(broken))
        for row in broken:
            print("  %-26s %-28s id %s  h %s\n      %s" % row)
        print("\nEach one needs its hash checked in the Vimeo account, or the video")
        print("re-shared as unlisted. Re-run with --verify-only after fixing.")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
