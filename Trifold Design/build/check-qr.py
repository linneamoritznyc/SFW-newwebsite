#!/usr/bin/env python3
"""Decode every QR code out of the rendered 300 DPI spreads.

A print code that will not scan is worth nothing, and nothing else in this
build catches it: the artwork looks perfectly correct with a dead code on it.
This found two real faults. The scholarship code was Education Blue #3780B8,
a mid tone that a decoder could not separate from white at this size; and the
codes on the colour panels were set 0.11in smaller than the ones on the white
panels, which took them to 0.45mm a module, under the practical print minimum.

    python3 "Trifold Design/build/render.js"   # first, the spreads must exist
    python3 "Trifold Design/build/check-qr.py"

Needs opencv-python-headless. Run it after any change to a URL, a code colour,
or the size of .qr img.
"""
import json, pathlib, subprocess, sys
import cv2, numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).parent
SPREADS = HERE.parent
SCALE = 300 / 96   # the render's deviceScaleFactor

boxes = json.loads(subprocess.run(
    ["node", str(HERE / "qr-boxes.js")], capture_output=True, text=True,
    cwd=SPREADS.parent, check=True).stdout)

det = cv2.QRCodeDetector()
failures = []
for sheet, items in boxes.items():
    sheet_img = Image.open(SPREADS / f"{sheet}-spread.png").convert("RGB")
    for it in items:
        pad = 6
        crop = sheet_img.crop((int(it["x"] * SCALE) - pad, int(it["y"] * SCALE) - pad,
                               int((it["x"] + it["w"]) * SCALE) + pad,
                               int((it["y"] + it["h"]) * SCALE) + pad))
        url, _, _ = det.detectAndDecode(np.array(crop))
        mm = it["w"] / 96 * 25.4
        print(f"{it['src']:<24} {mm:5.1f}mm  {'ok    ' if url else 'FAILED'}  {url}")
        if not url:
            failures.append(it["src"])

if failures:
    sys.exit("could not decode: " + ", ".join(failures))
print(f"all {sum(len(v) for v in boxes.values())} codes decode from the print render")
