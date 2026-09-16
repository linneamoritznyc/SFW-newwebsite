#!/usr/bin/env python3
"""Generate the QR codes for the trifold, one per panel.

Colours are taken from css/site.css section 1. See NOTES.md for the
token decision behind each one. Run from the repo root:

    python3 "Trifold Design/build/make-qr.py"
"""
import pathlib
import segno

OUT = pathlib.Path(__file__).parent / "qr"
OUT.mkdir(exist_ok=True)

# Short on purpose. Every character in the tail costs modules, every module
# costs physical size, and a print code that will not scan is worth nothing at
# all. utm_content still names the panel, which is the only breakdown anyone
# will actually read.
BASE = "utm_source=trifold&utm_medium=print"

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
        "#1F4E73",
    ),
    # panel 5, Practice. --green. The eleven case study films, which is where
    # a reader who believes the practice panel wants to go next.
    "case-studies": (
        # The fragment goes last. Written the other way round the whole UTM
        # tail lands inside the fragment and no analytics ever sees it.
        f"https://soilfoodweb.com/practice?{BASE}&utm_content=case_studies#case-studies",
        "#156826",
    ),
    # panel 6, Community. --soil, not --gold: the brand's gold is #C9A227,
    # which against white gives a code a scanner has to work for. The gold
    # appears on the rule above the code instead, where nothing has to read it.
    "donate": (
        f"https://soilfoodweb.com/donate?{BASE}&utm_content=donate",
        "#4F3433",
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
