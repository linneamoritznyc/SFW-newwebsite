#!/usr/bin/env python3
"""Every image the pages reference exists on disk, srcset candidates included.

    python3 tools/imagecheck.py

A missing srcset file is invisible in most testing: the browser silently falls
back to another candidate, or to nothing, and only some viewport widths break.
"""
import re, os, sys, glob, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = ("lovable",)
IMG = re.compile(r'<(?:img|source)\b[^>]*>', re.I)
SRC = re.compile(r'\bsrc="([^"]+)"')
SRCSET = re.compile(r'\bsrcset="([^"]+)"')
POSTER = re.compile(r'\bposter="([^"]+)"')
DATASRC = re.compile(r'\bdata-src="([^"]+)"')
CSSURL = re.compile(r'url\((["\']?)([^)"\']+)\1\)')


def pages():
    out = sorted(glob.glob(os.path.join(ROOT, "*.html")))
    out += sorted(glob.glob(os.path.join(ROOT, "projects", "*.html")))
    out += sorted(glob.glob(os.path.join(ROOT, "news", "*.html")))
    return [p for p in out if not any(s in p for s in SKIP)]


def main():
    missing, seen = [], set()

    def check(rel, ref, where):
        if ref.startswith(("http", "data:", "#")):
            return
        target = os.path.normpath(os.path.join(os.path.dirname(rel), ref))
        seen.add(target)
        if not os.path.exists(os.path.join(ROOT, target)):
            missing.append((rel, ref, where))

    for p in pages():
        rel = os.path.relpath(p, ROOT)
        s = open(p, encoding="utf-8").read()
        for tag in IMG.findall(s):
            m = SRC.search(tag)
            if m:
                check(rel, m.group(1), "src")
            m = SRCSET.search(tag)
            if m:
                for cand in m.group(1).split(","):
                    u = cand.strip().split()[0]
                    if u:
                        check(rel, u, "srcset")
        for m in POSTER.finditer(s):
            check(rel, m.group(1), "poster")
        for m in DATASRC.finditer(s):
            for u in m.group(1).split(","):
                check(rel, u.strip(), "data-src")

    css = os.path.join(ROOT, "css", "site.css")
    for _, u in CSSURL.findall(open(css, encoding="utf-8").read()):
        check("css/site.css", u, "css url()")

    print("%d distinct image and media references" % len(seen))
    if missing:
        print("\n%d missing files:" % len(missing))
        for rel, ref, where in missing:
            print("  %s: %s (%s)" % (rel, ref, where))
        return 1
    print("every referenced file exists")

    # Anything sitting in img/w/ that no page asks for is dead weight.
    used = {t for t in seen if t.startswith("img/w/")}
    on_disk = {os.path.join("img", "w", f) for f in os.listdir(os.path.join(ROOT, "img", "w"))}
    orphans = sorted(on_disk - used)
    if orphans:
        print("\n%d derivatives in img/w/ that no page references:" % len(orphans))
        for o in orphans:
            print("  " + o)
    return 0


if __name__ == "__main__":
    sys.exit(main())
