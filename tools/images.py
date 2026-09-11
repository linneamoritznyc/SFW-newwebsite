#!/usr/bin/env python3
"""Make web-sized derivatives of the photograph library.

    python3 tools/images.py

img/ holds the Foundation's originals, at the sizes and filenames they arrived
with, and nothing here touches them. Some are very large: the portrait of Dr.
Ingham is 3.3 MB, and the homepage was pulling 10.4 MB of photographs before
this existed. A page that takes fifteen seconds to arrive is not beautiful,
whatever is on it.

So every photograph gets one derivative in img/w/, capped at 1600px on the
long edge and saved as a progressive JPEG. 1600 is chosen against the layout:
the widest a photograph is ever drawn is the full-bleed banner, and above
1600 the file grows faster than the picture improves.

Everything in img/w/ is a JPEG, including the derivatives of the PNGs, because
every file in the library is a photograph and PNG is the wrong container for
one. tools/build.py maps img/NAME.ext to img/w/NAME.jpg through web().

Skips anything already up to date, so it is cheap to re-run.
"""
import os
import re
import sys

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "img")
OUT = os.path.join(SRC, "w")

# Two tiers. 1600 is the widest a photograph is ever drawn, in the full-bleed
# banner. 800 covers every grid cell: a four-across step image is about 300 CSS
# pixels, so even on a 2x screen 800 is more than enough. Without the small
# tier the homepage ships 1600px files into 300px boxes.
WIDTHS = [1600, 800]
QUALITY = 78
# The logo is left alone: this script writes JPEGs, and a JPEG cannot hold
# the transparency a logo needs.
SKIP = ("icons.svg", "cutout-placeholder.svg")


def is_logo(name):
    """The logo is left alone whatever it is called: this script writes JPEGs,
    and a JPEG cannot hold the transparency a logo needs."""
    return "logo" in name.lower()


def safe_stem(filename):
    """Seven of the library filenames contain spaces and capitals, and they are
    kept exactly as they arrived. The derivatives cannot be: srcset is a
    comma-and-space delimited list, so a single space in a URL silently breaks
    the whole attribute and the browser falls back to src. Derivative names are
    therefore lowercased and hyphenated.
    """
    stem = os.path.splitext(filename)[0].lower()
    stem = re.sub(r"[^a-z0-9]+", "-", stem).strip("-")
    return stem


def derivative_name(filename, width):
    """img/Sampling equipment.jpg -> sampling-equipment.jpg / -800.jpg"""
    stem = safe_stem(filename)
    return stem + (".jpg" if width == WIDTHS[0] else "-%d.jpg" % width)


def main():
    os.makedirs(OUT, exist_ok=True)
    made = skipped = 0
    before = after = 0

    for name in sorted(os.listdir(SRC)):
        path = os.path.join(SRC, name)
        if not os.path.isfile(path):
            continue
        if name in SKIP or is_logo(name) or not name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        if "shutterstock" in name.lower():          # excluded by policy
            continue

        src_size = os.path.getsize(path)
        before += src_size
        original = None
        sizes_out = []

        for width in WIDTHS:
            dst = os.path.join(OUT, derivative_name(name, width))
            if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(path):
                after += os.path.getsize(dst)
                skipped += 1
                sizes_out.append(os.path.getsize(dst))
                continue
            if original is None:
                original = ImageOps.exif_transpose(Image.open(path))
                if original.mode not in ("RGB", "L"):
                    original = original.convert("RGB")
            im = original.copy()
            im.thumbnail((width, width), Image.LANCZOS)
            im.save(dst, "JPEG", quality=QUALITY, optimize=True, progressive=True)
            after += os.path.getsize(dst)
            sizes_out.append(os.path.getsize(dst))
            made += 1

        print("  %-52s %6.0fKB -> %s" % (name[:52], src_size / 1024,
                                         " / ".join("%.0fKB" % (n / 1024) for n in sizes_out)))

    print("\n  %d written, %d already current" % (made, skipped))
    print("  library %.1f MB -> %.1f MB" % (before / 1048576, after / 1048576))
    return 0


if __name__ == "__main__":
    sys.exit(main())
