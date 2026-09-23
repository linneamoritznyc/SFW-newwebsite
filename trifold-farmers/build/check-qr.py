#!/usr/bin/env python3
"""Decode every QR code out of the farmers trifold's previews and print PDFs.

    python3 trifold-farmers/build/check-qr.py

Each sheet must yield exactly the codes it is meant to carry, or this fails.
Each code is cut out of the page and decoded on its own; the page is 600 DPI
for a PDF, rasterised with pdftoppm.
"""
import pathlib, subprocess, sys, tempfile
import cv2, numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

ROOT = pathlib.Path(__file__).parent.parent
WANT = {"outside": {"https://www.sfw.one/brochure-scholarship",
                    "https://www.sfw.one/brochure-community",
                    "https://soilfoodweb.com/"},
        "inside":  {"https://www.sfw.one/brochure-webinar",
                    "https://www.sfw.one/brochure-casestudies"}}

def decode(img):
    a = np.array(img.convert("RGB"))
    found = set()
    ok, texts, _, _ = cv2.QRCodeDetector().detectAndDecodeMulti(a)
    if ok: found |= {t for t in texts if t}
    if not found:  # a whole sheet can be too busy; try a smaller copy
        small = cv2.resize(a, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        ok, texts, _, _ = cv2.QRCodeDetector().detectAndDecodeMulti(small)
        if ok: found |= {t for t in texts if t}
    return found

bad = 0
def report(label, sheet, img):
    global bad
    got = decode(img)
    status = "ok  " if got == WANT[sheet] else "FAIL"
    bad += status == "FAIL"
    print(f"  {status} {label:<58} {', '.join(sorted(got)) or 'nothing decoded'}")

for sheet in ("outside", "inside"):
    report(f"{sheet}-spread.png", sheet, Image.open(ROOT / f"{sheet}-spread.png"))

for pdf in sorted((ROOT / "print").rglob("*.pdf")):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["pdftoppm", "-r", "600", "-png", str(pdf), f"{d}/p"], check=True)
        pages = sorted(pathlib.Path(d).glob("p*.png"))
        for n, pg in enumerate(pages, 1):
            if len(pages) == 2: sheet = "outside" if n == 1 else "inside"
            else: sheet = "outside" if "outside" in pdf.name else "inside"
            report(f"{pdf.relative_to(ROOT)} p{n}", sheet, Image.open(pg))

sys.exit(1 if bad else 0)
