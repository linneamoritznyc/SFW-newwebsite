#!/usr/bin/env python3
"""Generate the three QR codes for the trifold, one per panel.

Colours are taken from css/site.css section 1. See NOTES.md for the
token decision behind each one. Run from the repo root:

    python3 "Trifold Design/build/make-qr.py"
"""
import pathlib
import segno

OUT = pathlib.Path(__file__).parent / "qr"
OUT.mkdir(exist_ok=True)

BASE = "utm_source=trifold&utm_medium=print&utm_campaign=foundation_brochure"

CODES = {
    # panel 6, Community. --green, Food Web Green.
    "community": (
        "https://school.soilfoodweb.com/products/communities/SFW-public-community"
        f"?{BASE}&utm_content=community",
        "#156826",
    ),
    # panel 2, the Dr. Elaine story panel. --legacy, Legacy Purple.
    "webinar": (
        f"https://webinar.soilfoodweb.com/?{BASE}&utm_content=webinar",
        "#6B4C7A",
    ),
    # panel 3, Teaching. --edu, Education Blue.
    "scholarship": (
        "https://soilfoodweb.com/scholarship-opportunities"
        f"?{BASE}&utm_content=scholarship",
        "#3780B8",
    ),
}

for name, (url, colour) in CODES.items():
    # M correction (15%). Q would be sturdier, but these URLs carry long UTM
    # tails: at Q the community code is 65 modules, which at the 1.15in the
    # panel can spare is 0.45mm a module, under the practical print minimum.
    # M holds every code at 0.51mm or better. See NOTES.md.
    qr = segno.make(url, error="m")
    qr.save(OUT / f"{name}.svg", scale=10, border=2, dark=colour, light=None)
    print(f"{name:<12} version {qr.version:>2}  {qr.symbol_size(scale=1, border=2)[0]:>3} modules  {url}")
