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

Each code takes its own panel's colour, on white, at error correction H with
four modules of quiet zone. Colour is the reason a code on this brochure has
already failed to scan once, so CONTRAST_MIN below is a build gate, not advice:
Education Blue #3780B8 is 4.25:1 against white and the brand gold #C9A227 is
2.42:1, and neither survives a press. Both panels use the deep end of their own
gradient here instead. Nothing ships under the threshold.

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

LIGHT = "#FFFFFF"   # every code keeps its own white ground, whatever it sits on
ECC = "h"           # 30% recoverable: survives a crease, a thumb, a bad press day
QUIET = 4           # modules of quiet zone on every side, the spec minimum
CONTRAST_MIN = 4.5  # against white. Below this a scanner starts having opinions.


def contrast_on_white(hex_colour):
    """WCAG contrast ratio of a colour against white."""
    ch = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    ch = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in ch]
    return 1.05 / (0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2] + 0.05)

# One colour per code, each taken from the panel it stands on. Tokens are
# css/site.css section 1, same as the rest of the piece.
CODES = {
    # name            short link                                    PNG name       colour
    "webinar":      ("https://www.sfw.one/brochure-webinar",     "webinar",     "#6B4C7A"),  # --legacy, the Dr. Elaine panel
    "scholarship":  ("https://www.sfw.one/brochure-scholarship", "scholarship", "#1F4E73"),  # --edu-deep, the teaching panel
    "case-studies": ("https://www.sfw.one/brochure-casestudies", "casestudies", "#156826"),  # --green, the practice panel
    "community":    ("https://www.sfw.one/brochure-community",   "community",   "#22371F"),  # --moss, the deep end of the community field
    "donate":       ("https://www.sfw.one/brochure-donate",      "donate",      "#8A6E15"),  # --gold taken down until it can be read
}

# The placed codes are 1.15in square including their quiet zone. Anything at or
# above 2cm is fine for print; this is 29.2mm.
PLACED_MM = 1.15 * 25.4

too_light = [(n, c, contrast_on_white(c)) for n, (_, _, c) in CODES.items()
             if contrast_on_white(c) < CONTRAST_MIN]
if too_light:
    raise SystemExit("colour too light to scan: " + ", ".join(
        f"{n} {c} at {r:.2f}:1, needs {CONTRAST_MIN}:1" for n, c, r in too_light))

print(f"{'code':<14}{'colour':<9}{'contrast':>9}{'ver':>4}{'modules':>9}{'mm/module':>11}   payload")
for name, (url, png_name, DARK) in CODES.items():
    qr = segno.make(url, error=ECC)
    modules = qr.symbol_size(scale=1, border=QUIET)[0]

    # Vector for the artwork: no resolution to get wrong at the printer.
    qr.save(SVG_OUT / f"{name}.svg", scale=10, border=QUIET,
            dark=DARK, light=LIGHT)

    # Standalone raster, comfortably over 1200px on the short side.
    scale = -(-1200 // modules)          # ceiling division
    qr.save(PNG_OUT / f"sfw-brochure-qr-{png_name}.png", scale=scale,
            border=QUIET, dark=DARK, light=LIGHT)

    print(f"{name:<14}{DARK:<9}{contrast_on_white(DARK):>8.2f}:1{qr.version:>4}"
          f"{modules:>9}{PLACED_MM/modules:>10.3f}   {url}")
