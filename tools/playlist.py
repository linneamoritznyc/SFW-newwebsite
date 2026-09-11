#!/usr/bin/env python3
"""Read the WordPress video playlists, verify every video, write content/videos.json.

    cd /path/to/SFW-newwebsite
    python3 tools/playlist.py                 # scrape, verify, fetch thumbnails
    python3 tools/playlist.py --verify-only   # re-check what is already in the file

No installing anything. Standard library only, so the Python that ships with
macOS runs it as it is: no pip, no requests, no BeautifulSoup, no virtual
environment. The path is relative to this file rather than to where you are
standing, so `python3 ~/SFW-newwebsite/tools/playlist.py` works from anywhere.

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
import urllib.error
import urllib.parse as up
import urllib.request
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "content", "videos.json")
THUMBS = os.path.join(ROOT, "img", "video")
UA = {"User-Agent": "SFWF-rebuild-playlist/1.0 (linnea@soilfoodweb.com)"}
OEMBED = "https://vimeo.com/api/oembed.json"


class Playlist(HTMLParser):
    """Every anchor with its text and its thumbnail, plus every iframe src.

    A hand-rolled parser rather than BeautifulSoup, so that the script runs on
    a laptop with nothing installed. It does not need to understand the page,
    only to find links that carry a vID and whatever text and image sit inside
    them, which is well within what html.parser does reliably.
    """

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.links = []
        self.iframes = []
        self._open = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            # The visible text is the best title, but plenty of these anchors
            # wrap nothing but a thumbnail, so the attributes that carry a
            # name are collected too.
            self._open = {"href": a["href"], "lines": [], "img": "",
                          "alt": a.get("title") or a.get("aria-label") or ""}
        elif tag == "iframe" and a.get("src"):
            self.iframes.append(a["src"])
        elif tag == "img" and self._open is not None and not self._open["img"]:
            # WordPress lazy-loading leaves a data: URI in src and the real
            # file in one of these, so the attributes are tried in order.
            src = (a.get("data-src") or a.get("data-lazy-src") or a.get("src") or "")
            if src.startswith("data:"):
                src = (a.get("data-lazy-src") or a.get("data-srcset", "").split(" ")[0] or "")
            self._open["img"] = src
            if not self._open["alt"]:
                self._open["alt"] = a.get("alt") or a.get("title") or ""

    def handle_endtag(self, tag):
        if tag == "a" and self._open is not None:
            self.links.append(self._open)
            self._open = None

    def handle_data(self, data):
        if self._open is not None and data.strip():
            self._open["lines"].append(data.strip())


def fetch(url, params=None, binary=False):
    """GET, with the status code handed back rather than raised.

    Returns (status, body). A 403 or a 404 from Vimeo is an answer, not an
    accident: it is how the oembed endpoint says a hash is wrong.
    """
    if params:
        url = url + "?" + up.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
            if binary:
                return r.status, body
            return r.status, body.decode(r.headers.get_content_charset() or "utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, ""
    except (urllib.error.URLError, OSError) as exc:
        return 0, str(exc)


def slugify(text, fallback, taken):
    """What ?v= carries.

    Built from the title, because that is what a person reading a shared link
    expects to see, with the video id appended only when two videos would
    otherwise claim the same slug.
    """
    t = (text or "").replace("’", "").replace("'", "")
    slug = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:60] or str(fallback)
    if slug in taken:
        slug = "%s-%s" % (slug, fallback)
    taken.add(slug)
    return slug


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


def text_near(lines):
    """The title, and everything else in the order the page wrote it.

    A playlist item is an anchor wrapping a thumbnail and one to three lines:
    a title, and then some combination of a person and a place. Which is
    which varies between the six pages, so nothing here decides. The first
    line is the title and the rest are joined as they stand, because the page
    already knows the right order and a guess can only get it backwards.
    """
    lines = [l for l in lines if not l.lower().startswith("watch")]
    if not lines:
        return "", ""
    return lines[0], " \u00b7 ".join(lines[1:])


def scrape(page, raw_dir=None):
    status, html = fetch(page)
    if raw_dir and html:
        name = re.sub(r"[^a-z0-9]+", "-", up.urlparse(page).path.lower()).strip("-") or "index"
        with open(os.path.join(raw_dir, name + ".html"), "w", encoding="utf-8") as f:
            f.write(html)
    if status != 200:
        print("  could not read the page: %s" % (("HTTP %d" % status) if status else html))
        return None
    doc = Playlist()
    doc.feed(html)

    out, seen = [], set()
    for link in doc.links:
        vid, h = parse_link(link["href"])
        if not vid or vid in seen:
            continue
        seen.add(vid)
        title, subtitle = text_near(link["lines"])
        title = title or link.get("alt", "")
        out.append({"id": vid, "hash": h, "title": title, "subtitle": subtitle,
                    "remote_thumb": up.urljoin(page, link["img"]) if link["img"] else "",
                    "source": page})

    # The iframe holds the video the page opened with, which is sometimes the
    # only place a hash appears in one piece.
    for src in doc.iframes:
        if "player.vimeo.com" not in src:
            continue
        m = re.search(r"/video/(\d+)", src)
        h = up.parse_qs(up.urlparse(src).query).get("h", [""])[0]
        if m and h:
            for it in out:
                if it["id"] == m.group(1) and not it["hash"]:
                    it["hash"] = h
    return out


def verify(item, raw_dir=None):
    """Is this a video that will play, and how long is it?

    A 200 is not enough, which is what the first run of this script got wrong.
    Vimeo answers 200 for a showcase id as well as a video id, and the six
    playlist pages are full of showcase ids: every page links to the other
    five playlists in exactly the same ?vID= shape as a video. Those answers
    come back with no duration and no title, and 21 of the 27 ids found on
    the first run were that.

    So the test is what the answer contains, not what it says: type "video"
    and a real duration. Anything else is a showcase, or something else
    entirely, and is reported rather than written.
    """
    url = "https://vimeo.com/%s/%s" % (item["id"], item["hash"]) if item["hash"] \
        else "https://vimeo.com/%s" % item["id"]
    status, body = fetch(OEMBED, {"url": url, "width": 1280})
    if raw_dir:
        with open(os.path.join(raw_dir, "oembed-%s.json" % item["id"]), "w", encoding="utf-8") as f:
            f.write("%s %s\n%s" % (status, url, body))
    if status != 200:
        return None, "oembed %s" % (status or "no answer")
    try:
        meta = json.loads(body)
    except ValueError:
        return None, "oembed did not return JSON"
    if meta.get("type") != "video" or not meta.get("duration"):
        return None, "not a video: oembed gives type %r, duration %r (a showcase id?)" \
            % (meta.get("type"), meta.get("duration"))
    return meta, None


def fetch_thumb(url, slug):
    if not url:
        return ""
    os.makedirs(THUMBS, exist_ok=True)
    dst = os.path.join(THUMBS, slug + ".jpg")
    if os.path.exists(dst):
        return "img/video/" + slug + ".jpg"
    status, body = fetch(url, binary=True)
    if status != 200 or not body:
        return ""
    with open(dst, "wb") as f:
        f.write(body)
    return "img/video/" + slug + ".jpg"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify-only", action="store_true",
                    help="re-check the videos already in content/videos.json")
    ap.add_argument("--save-raw", action="store_true",
                    help="also write every page and every Vimeo answer to docs/playlist-raw/, "
                         "so the extraction can be corrected against what the pages actually contain")
    args = ap.parse_args()

    raw_dir = None
    if args.save_raw:
        raw_dir = os.path.join(ROOT, "docs", "playlist-raw")
        os.makedirs(raw_dir, exist_ok=True)
        print("saving raw pages and answers to %s" % raw_dir)

    if not os.path.exists(DATA):
        sys.exit("Cannot find %s.\nRun this from a clone of the repository: the script writes into\n"
                 "the content/ folder beside it." % DATA)

    print("writing to %s\n" % DATA)
    data = json.load(open(DATA, encoding="utf-8"))
    broken, kept, taken = [], 0, set()

    unreachable = 0
    for pl in data["playlists"]:
        items = pl["items"] if args.verify_only else scrape(pl["page"], raw_dir)
        if items is None:                       # the page itself did not answer
            unreachable += 1
            continue
        if not args.verify_only:
            print("%-26s %s  %d links" % (pl["id"], pl["page"], len(items)))
        out = []
        for it in items:
            meta, err = verify(it, raw_dir)
            slug = it.get("slug") or slugify(it.get("title"), it["id"], taken)
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
                "duration": meta.get("duration"),
                "thumb": (fetch_thumb(it.get("remote_thumb"), slug)
                          or fetch_thumb(meta.get("thumbnail_url", ""), slug)),
                "source": it.get("source", pl["page"]),
            }
            out.append(entry)
            kept += 1
            time.sleep(0.3)                    # be polite to both hosts
        pl["items"] = out
        print("  kept %d" % len(out))

    # Nothing readable means no result, and a file that says otherwise would
    # be worse than an empty one. Leave it exactly as it was.
    if unreachable and not kept:
        print("\nNone of the playlist pages could be read, so nothing was written.")
        print("Either this machine has no route to soilfoodweb.com, which is the")
        print("case in the cloud sandbox, or the pages have moved.")
        return 2

    data["_state"] = "Written by tools/playlist.py on %s. %d videos, every one verified against Vimeo oembed.%s" \
        % (time.strftime("%d %B %Y"), kept,
           " %d of the six pages could not be read." % unreachable if unreachable else "")
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("\n%d videos written to content/videos.json" % kept)

    # A showcase id is not a broken video, it is a link to another playlist,
    # and the pages are full of them. Worth counting, not worth reading.
    shows = [r for r in broken if "not a video" in r[4]]
    real = [r for r in broken if "not a video" not in r[4]]
    if shows:
        print("\n%d links were to other playlists rather than to videos, and were skipped."
              % len(shows))
    if real:
        print("\n%d WILL NOT PLAY, and are not in the file:" % len(real))
        for row in real:
            print("  %-26s %-28s id %s  h %s\n      %s" % row)
        print("\nEach one needs its hash checked in the Vimeo account, or the video")
        print("re-shared as unlisted. Re-run with --verify-only after fixing.")
    return 1 if real else 0


if __name__ == "__main__":
    sys.exit(main())
