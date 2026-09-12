#!/usr/bin/env python3
"""Bring the video thumbnails onto this site.

    python3 tools/thumbs.py            # download what is missing
    python3 tools/thumbs.py --check    # report only, change nothing

content/videos.json carries two fields per video. "thumb" is a file in this
repository; "remoteThumb" still points at soilfoodweb.com/wp-content/uploads,
the old WordPress site. build.py prefers the local one and falls back to the
remote, so every entry without a "thumb" makes a visitor's browser fetch an
image from the old site.

That is worth ending for three reasons. The new site should not go dark
because someone tidies the old site's uploads directory. Every such fetch
tells soilfoodweb.com who is reading this page. And the Content-Security-Policy
in vercel.json sets img-src to this origin, so those images are refused
outright once soilfoodweb.com is taken back out of that list, which is the
point of running this.

This replaces the --thumbs mode of tools/playlist.py, removed in 6d414c3.

Files land in img/video/<vimeo id>.<ext>, keeping whatever extension the
source served, and videos.json is rewritten in place with "thumb" set. Run it
again after adding videos; it only fetches what is missing.
"""
import json, os, sys, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEOS = os.path.join(ROOT, "content", "videos.json")
OUT = os.path.join(ROOT, "img", "video")


def entries(o, found=None):
    """Every video object in the file, wherever it sits in the tree."""
    found = [] if found is None else found
    if isinstance(o, dict):
        if "remoteThumb" in o or "thumb" in o:
            found.append(o)
        for v in o.values():
            entries(v, found)
    elif isinstance(o, list):
        for v in o:
            entries(v, found)
    return found


def main():
    check = "--check" in sys.argv
    with open(VIDEOS, encoding="utf-8") as f:
        data = json.load(f)

    todo = [v for v in entries(data) if v.get("remoteThumb") and not v.get("thumb")]
    print("%d videos, %d already local, %d to fetch"
          % (len(entries(data)), len(entries(data)) - len(todo), len(todo)))
    if check or not todo:
        for v in todo:
            print("  missing:", v.get("id"), v.get("remoteThumb"))
        return 0

    os.makedirs(OUT, exist_ok=True)
    failed = []
    for v in todo:
        url = v["remoteThumb"]
        ext = os.path.splitext(url.split("?")[0])[1].lower() or ".jpg"
        name = "%s%s" % (v.get("id") or v.get("slug"), ext)
        path = os.path.join(OUT, name)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "soilfoodweb.org thumbs"})
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read()
            if not body:
                raise ValueError("empty response")
            with open(path, "wb") as f:
                f.write(body)
            v["thumb"] = "img/video/" + name
            print("  ok  %-16s %6d bytes  %s" % (v.get("id"), len(body), name))
        except (urllib.error.URLError, ValueError, OSError) as err:
            # Leave remoteThumb in place: a half-written entry would render a
            # broken image, which is worse than the fallback it already has.
            failed.append((v.get("id"), url, err))
            print("  FAIL %-16s %s" % (v.get("id"), err))

    with open(VIDEOS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("\nwrote content/videos.json")
    if failed:
        print("%d could not be fetched; they keep pointing at the old site." % len(failed))
    else:
        print("Every thumbnail is local now. Next: drop https://soilfoodweb.com from\n"
              "img-src in vercel.json, run python3 tools/build.py, and check Practice.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
