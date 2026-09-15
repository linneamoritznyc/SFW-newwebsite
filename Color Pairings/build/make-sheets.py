#!/usr/bin/env python3
"""Build the green pairing sheets.

Every colour below is a token from css/site.css section 1, with the name and
role taken from docs/brand-guide.html. Nothing here is invented: to add a
colour, add its token, do not pick a new one.

    python3 "Color Pairings/build/make-sheets.py"
    node    "Color Pairings/build/render.js"
"""
import pathlib

CURRENT  = ("#59A66C", "Green Legacy")   # --green-legacy
PROPOSED = ("#156826", "Food Web Green") # --green

# (token, name, hex, role from the brand guide)
EXISTING = [
    ("--soil",    "Soil Brown",     "#4F3433", "Headings, footer text"),
    ("--legacy",  "Legacy Purple",  "#6B4C7A", "Dr. Elaine content only"),
    ("--edu",     "Education Blue", "#3780B8", "Course tags, student access"),
    ("--panel",   "Organic Cream",  "#F4F1EA", "Shape only, never the page"),
    ("--tan",     "Tan",            "#C89B7B", "Card borders, dividers"),
    ("--sage",    "Sage",           "#A7B097", "Textures, hover on dark"),
    ("--gold",    "Harvest Gold",   "#C9A227", "Donate button only"),
]

NEW = [
    ("--moss",        "Moss",            "#22371F", "Overlay menu, dark bands, hover"),
    ("--ground",      "Ground",          "#231F1D", "Footer and utility bar background"),
    ("--scope",       "Scope",           "#3C3841", "Microscopy footage background"),
    ("--olive",       "Olive",           "#5F6A3C", "Line accents, icon strokes"),
    ("--living",      "Living Green",    "#A2AE77", "From the field of the slide"),
    ("--glow",        "Glow",            "#DBE6A7", "Brightest thing in the frame"),
    ("--membrane",    "Membrane Violet", "#9E8FC2", "From the amoeba's cell wall"),
    ("--panel-green", "Specimen Case",   "#E6EADC", "Pale green ground behind grouped content"),
    ("--paper",       "Paper",           "#FFFFFF", "Page background"),
    ("--ink",         "Ink",             "#333130", "Body text"),
    ("--ink-soft",    "Ink Soft",        "#4A463F", "Secondary text"),
    ("--ink-faint",   "Ink Faint",       "#6A665C", "Captions, source lines"),
]


def lum(hexcolour):
    c = [int(hexcolour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>%s</title>
<style>
@font-face { font-family:"EB Garamond"; font-weight:400; src:url("/fonts/eb-garamond-latin-400-normal.woff2") format("woff2"); }
@font-face { font-family:"EB Garamond"; font-weight:500; src:url("/fonts/eb-garamond-latin-500-normal.woff2") format("woff2"); }
@font-face { font-family:"EB Garamond"; font-weight:400; font-style:italic; src:url("/fonts/eb-garamond-latin-400-italic.woff2") format("woff2"); }
@font-face { font-family:"Montserrat"; font-weight:600 700; src:url("/fonts/montserrat-latin-variable.woff2") format("woff2-variations"); }
@font-face { font-family:"Source Sans 3"; font-weight:400; src:url("/fonts/source-sans-3-latin-400-normal.woff2") format("woff2"); }
*,*::before,*::after { box-sizing:border-box; }
html,body { margin:0; background:#fff; }
.sheet { width:%dpx; height:%dpx; background:#fff; position:relative; overflow:hidden;
         font-family:"Source Sans 3",Arial,sans-serif; color:#333130; }
h1 { font-family:"EB Garamond",Georgia,serif; font-weight:500; color:#231F1D;
     margin:0; text-align:center; letter-spacing:.005em; }
.sub { font-family:"EB Garamond",Georgia,serif; font-style:italic; color:#6A665C;
       text-align:center; margin:8px 0 0; }
.pair { display:flex; position:relative; }
/* A pale swatch needs a hairline or it vanishes into the white sheet.
   It is an overlay, not an inset shadow on .pair: flex children paint
   over the parent background and would hide it. */
.pair .edge { position:absolute; inset:0; box-shadow:inset 0 0 0 1px rgba(79,52,51,.25); }
.pair .a { flex:0 0 28%%; }
.pair .b { flex:1 1 auto; }
</style></head><body>"""


def pair_html(green, partner, w, h, outline=False):
    """One swatch: a strip of green against the partner colour."""
    edge = '<div class="edge"></div>' if outline else ""
    return (f'<div class="pair" style="width:{w}px;height:{h}px">'
            f'<div class="a" style="background:{green}"></div>'
            f'<div class="b" style="background:{partner}"></div>{edge}</div>')


def comparison_sheet(path, title, subtitle, colours, cols, cell_w, cell_h,
                     col_gap, row_gap, top, gutter, width=1920, height=1080):
    """Current green on the left half, proposed on the right, same grid."""
    rows = -(-len(colours) // cols)
    side_w = cols * cell_w + (cols - 1) * col_gap
    grid_h = rows * cell_h + (rows - 1) * row_gap
    left_x = (width - gutter) / 2 - side_w
    right_x = (width + gutter) / 2

    out = [HEAD % (title, width, height), '<div class="sheet">']
    out.append(f'<h1 style="position:absolute;top:{top - 96}px;left:{left_x}px;'
               f'width:{side_w}px;font-size:46px">Current Green</h1>')
    out.append(f'<h1 style="position:absolute;top:{top - 96}px;left:{right_x}px;'
               f'width:{side_w}px;font-size:46px">Proposed Green</h1>')
    if subtitle:
        out.append(f'<p class="sub" style="position:absolute;top:{top + grid_h + 46}px;'
                   f'left:0;width:{width}px;font-size:23px">{subtitle}</p>')

    for side_x, (green, _) in ((left_x, CURRENT), (right_x, PROPOSED)):
        for i, (_tok, _name, hx, _role) in enumerate(colours):
            x = side_x + (i % cols) * (cell_w + col_gap)
            y = top + (i // cols) * (cell_h + row_gap)
            light = lum(hx) > 0.80
            out.append(f'<div style="position:absolute;left:{x}px;top:{y}px">'
                       + pair_html(green, hx, cell_w, cell_h, outline=light) + '</div>')

    out.append('</div></body></html>')
    pathlib.Path(path).write_text("\n".join(out))


def reference_sheet(path):
    """Every pairing with its token, role and the two contrast ratios."""
    colours = EXISTING + NEW
    width, row_h, top = 2000, 96, 250
    height = top + row_h * len(colours) + 150

    out = [HEAD % ("Green pairings, reference", width, height), '<div class="sheet">']
    out.append(f'<h1 style="position:absolute;top:80px;left:0;width:{width}px;'
               f'font-size:50px">Food Web Green against the rest of the palette</h1>')
    out.append(f'<p class="sub" style="position:absolute;top:146px;left:0;width:{width}px;'
               f'font-size:22px">Every colour and role from the brand guide. '
               f'Contrast is the green against that colour, current then proposed.</p>')

    hdr = [(150, "Current"), (330, "Proposed"), (530, "Colour"), (1130, "Token"),
           (1430, "Role"), (1840, "Contrast")]
    for x, label in hdr:
        out.append(f'<div style="position:absolute;left:{x}px;top:{top - 40}px;'
                   f'font-family:Montserrat,Arial;font-weight:700;font-size:15px;'
                   f'letter-spacing:.14em;text-transform:uppercase;color:#156826">{label}</div>')

    for i, (tok, name, hx, role) in enumerate(colours):
        y = top + i * row_h
        light = lum(hx) > 0.80
        r_cur, r_new = ratio(CURRENT[0], hx), ratio(PROPOSED[0], hx)
        better = r_new >= r_cur
        arrow = "#156826" if better else "#B4532A"
        out.append(f'<div style="position:absolute;left:0;top:{y + row_h - 1}px;'
                   f'width:{width}px;height:1px;background:rgba(79,52,51,.16)"></div>')
        out.append(f'<div style="position:absolute;left:150px;top:{y + 14}px">'
                   + pair_html(CURRENT[0], hx, 160, 62, outline=light) + '</div>')
        out.append(f'<div style="position:absolute;left:330px;top:{y + 14}px">'
                   + pair_html(PROPOSED[0], hx, 160, 62, outline=light) + '</div>')
        out.append(f'<div style="position:absolute;left:530px;top:{y + 22}px;font-size:25px;'
                   f'font-family:Montserrat,Arial;font-weight:600;color:#4F3433">{name}'
                   f'<span style="font-family:\'Source Sans 3\';font-weight:400;color:#6A665C;'
                   f'font-size:22px">&nbsp;&nbsp;{hx}</span></div>')
        out.append(f'<div style="position:absolute;left:1130px;top:{y + 26}px;font-size:21px;'
                   f'color:#6A665C;font-family:\'Source Sans 3\'">{tok}</div>')
        out.append(f'<div style="position:absolute;left:1430px;top:{y + 26}px;font-size:21px;'
                   f'color:#4A463F;width:390px">{role}</div>')
        out.append(f'<div style="position:absolute;left:1840px;top:{y + 26}px;font-size:21px;'
                   f'color:#6A665C">{r_cur:.1f} <span style="color:{arrow}">&rarr;</span> '
                   f'<b style="color:{arrow}">{r_new:.1f}</b></div>')

    out.append('</div></body></html>')
    pathlib.Path(path).write_text("\n".join(out))


here = pathlib.Path(__file__).parent
comparison_sheet(here / "sheet-existing.html", "Green pairings, the current set", "",
                 EXISTING + [("--paper", "Paper", "#FFFFFF", "Page background")],
                 cols=2, cell_w=248, cell_h=166, col_gap=86, row_gap=56,
                 top=195, gutter=250)
comparison_sheet(here / "sheet-new.html", "Green pairings, twelve more",
                 "Twelve more colours from the brand guide, in the same test.",
                 NEW, cols=3, cell_w=210, cell_h=152, col_gap=52, row_gap=54,
                 top=222, gutter=170)
reference_sheet(here / "sheet-reference.html")

print("Contrast of each green against every palette colour")
print(f"{'colour':<18}{'hex':<10}{'current':>9}{'proposed':>10}")
for tok, name, hx, role in EXISTING + NEW:
    print(f"{name:<18}{hx:<10}{ratio(CURRENT[0], hx):>9.2f}{ratio(PROPOSED[0], hx):>10.2f}")
