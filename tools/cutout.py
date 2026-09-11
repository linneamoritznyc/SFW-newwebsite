#!/usr/bin/env python3
"""Turn a studio photograph into a cut-out specimen on transparency.

    python3 tools/cutout.py                       # every file in img/illustration/
    python3 tools/cutout.py --grid 3x4 sheet.png  # slice a contact sheet first
    python3 tools/cutout.py --keep-bg strata.jpg  # trim and resize, no cut-out

The mood board is museum product shots: a specimen floating in empty space,
lit evenly, with nothing behind it. A photograph on a white studio sweep is
most of the way there already; what stops it floating on the page is the
background, which is never quite the same white as the paper and always ends
in a straight edge.

So: flood the background in from the four borders with a tolerance, feather
the resulting edge by one pixel so it does not read as a cut, trim to what is
left, and write a PNG with an alpha channel.

Flooding from the borders rather than keying a colour is the important part.
It cannot eat a pale patch inside the subject, because it only ever removes
pixels connected to the edge of the frame. A morel with a cream stem keeps
its stem.

Output goes to img/cut/, at 1400 and 700 on the long edge. tools/build.py
leaves img/cut/ alone when it maps photographs to their JPEG derivatives,
because a JPEG has no alpha and these are the one kind of image on the site
that needs one.
"""
import os
import re
import sys
from collections import deque

from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "img", "illustration")
OUT = os.path.join(ROOT, "img", "cut")
WIDTHS = [1400, 700]

# How far a pixel may sit from the corner colour and still count as
# background. Generous enough for a studio sweep with a soft shadow in it,
# tight enough to stop at a pale specimen.
TOLERANCE = 26


def slug(name):
    stem = os.path.splitext(os.path.basename(name))[0].lower()
    return re.sub(r"[^a-z0-9]+", "-", stem).strip("-")


def background_mask(im, tolerance=TOLERANCE):
    """True where the pixel is background: connected to the frame edge and
    within tolerance of the colour found there."""
    w, h = im.size
    px = im.convert("RGB").load()

    # The background colour is whatever the four corners agree on. Averaging
    # them survives a gradient sweep better than picking one.
    corners = [px[0, 0], px[w - 1, 0], px[0, h - 1], px[w - 1, h - 1]]
    bg = tuple(sum(c[i] for c in corners) // 4 for i in range(3))

    seen = bytearray(w * h)
    q = deque()

    def near(p):
        return (abs(p[0] - bg[0]) + abs(p[1] - bg[1]) + abs(p[2] - bg[2])) <= tolerance * 3

    for x in range(w):
        for y in (0, h - 1):
            if not seen[y * w + x] and near(px[x, y]):
                seen[y * w + x] = 1
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if not seen[y * w + x] and near(px[x, y]):
                seen[y * w + x] = 1
                q.append((x, y))

    while q:
        x, y = q.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and near(px[nx, ny]):
                seen[ny * w + nx] = 1
                q.append((nx, ny))
    return seen, w, h


def cut(im):
    """Photograph in, RGBA with the background gone, trimmed to the subject."""
    seen, w, h = background_mask(im)
    alpha = Image.new("L", (w, h), 255)
    ap = alpha.load()
    for y in range(h):
        row = y * w
        for x in range(w):
            if seen[row + x]:
                ap[x, y] = 0
    # one pixel of feather, so the edge reads as an edge and not as a cut
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.8))
    out = im.convert("RGBA")
    out.putalpha(alpha)
    box = out.getbbox()
    return out.crop(box) if box else out


def save(im, name):
    os.makedirs(OUT, exist_ok=True)
    for width in WIDTHS:
        c = im.copy()
        c.thumbnail((width, width), Image.LANCZOS)
        dst = os.path.join(OUT, name + ("" if width == WIDTHS[0] else "-%d" % width) + ".png")
        c.save(dst, "PNG", optimize=True)
        print("  %-44s %5dx%-5d %6.0fKB" % (os.path.relpath(dst, ROOT), c.width, c.height,
                                            os.path.getsize(dst) / 1024))


def tiles(im, rows, cols):
    w, h = im.size
    tw, th = w // cols, h // rows
    for r in range(rows):
        for c in range(cols):
            yield r * cols + c + 1, im.crop((c * tw, r * th, (c + 1) * tw, (r + 1) * th))


def main(argv):
    grid = None
    keep_bg = False
    args = []
    i = 0
    while i < len(argv):
        if argv[i] == "--grid":
            rows, cols = argv[i + 1].lower().split("x")
            grid = (int(rows), int(cols))
            i += 2
        elif argv[i] == "--keep-bg":
            keep_bg = True
            i += 1
        else:
            args.append(argv[i])
            i += 1

    if args:
        paths = [p if os.path.isabs(p) else os.path.join(ROOT, p) for p in args]
    else:
        if not os.path.isdir(SRC):
            print("Nothing to do: put the supplied files in img/illustration/ first.")
            print("(%s does not exist)" % os.path.relpath(SRC, ROOT))
            return 1
        paths = [os.path.join(SRC, n) for n in sorted(os.listdir(SRC))
                 if n.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))]

    if not paths:
        print("Nothing to do: no images found.")
        return 1

    for path in paths:
        im = Image.open(path)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGB")
        print(os.path.relpath(path, ROOT))
        if grid:
            for n, tile in tiles(im, *grid):
                save(tile if keep_bg else cut(tile), "%s-%02d" % (slug(path), n))
        else:
            save(im if keep_bg else cut(im), slug(path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
