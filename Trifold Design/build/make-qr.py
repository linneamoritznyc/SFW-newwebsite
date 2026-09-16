#!/usr/bin/env python3
"""Generate the five QR codes for the trifold, and the standalone PNGs.

Each code carries a Switchy short link, not the destination. Three reasons,
and the first two are the important ones:

  1. A printed code cannot be changed. The short link can, so a destination
     that moves, or a rebuilt site that renames a path, is a redirect edit
     rather than a reprint. This brochure has already had three addresses go
     404 under it once.
  2. Short payloads mean few modules, and few modules mean each module is
     physically large enough to survive press. These fit at error correction
     H with room to spare; the long URLs with UTM tails did not.
  3. The UTM parameters ride on the redirect, so the campaign reporting is
     unchanged and none of it costs modules here.

Pure black on white, error correction H, four modules of quiet zone.

    python3 "Trifold Design/build/make-qr.py"
    python3 "Trifold Design/build/check-qr.py"   # decodes them back out
"""
import pathlib
import segno

HERE = pathlib.Path(__file__).parent
SVG_OUT = HERE / "qr"                                   # placed in the artwork
PNG_OUT = HERE.parent.parent / "exports" / "qr"         # standalone, for reuse
SVG_OUT.mkdir(exist_ok=True)
PNG_OUT.mkdir(parents=True, exist_ok=True)

# A code has to read before it has to be on brand, and these sit on panels in
# four different colours. Black on white everywhere: maximum contrast, nothing
# for a scanner to argue with. The panel's own accent stays on the rule above
# the code, where nothing has to read it.
DARK, LIGHT = "#000000", "#FFFFFF"
ECC = "h"      # 30% recoverable: survives a crease, a thumb, a bad press day
QUIET = 4      # modules of quiet zone on every side, the spec minimum

CODES = {
    # name           short link                                      PNG name
    "webinar":      ("https://www.sfw.one/brochure-webinar",      "webinar"),
    "scholarship":  ("https://www.sfw.one/brochure-scholarship",  "scholarship"),
    "case-studies": ("https://www.sfw.one/brochure-casestudies",  "casestudies"),
    "community":    ("https://www.sfw.one/brochure-community",    "community"),
    "donate":       ("https://www.sfw.one/brochure-donate",       "donate"),
}

# The placed codes are 1.15in square including their quiet zone. Anything at or
# above 2cm is fine for print; this is 29.2mm.
PLACED_MM = 1.15 * 25.4

print(f"{'code':<14}{'ver':>4}{'modules':>9}{'mm/module':>11}   payload")
for name, (url, png_name) in CODES.items():
    qr = segno.make(url, error=ECC)
    modules = qr.symbol_size(scale=1, border=QUIET)[0]

    # Vector for the artwork: no resolution to get wrong at the printer.
    qr.save(SVG_OUT / f"{name}.svg", scale=10, border=QUIET,
            dark=DARK, light=LIGHT)

    # Standalone raster, comfortably over 1200px on the short side.
    scale = -(-1200 // modules)          # ceiling division
    qr.save(PNG_OUT / f"sfw-brochure-qr-{png_name}.png", scale=scale,
            border=QUIET, dark=DARK, light=LIGHT)

    print(f"{name:<14}{qr.version:>4}{modules:>9}{PLACED_MM/modules:>10.3f}   {url}")
    print(f"{'':14}{'':>4}{'':>9}{'':>11}   png {modules*scale}x{modules*scale}px")
