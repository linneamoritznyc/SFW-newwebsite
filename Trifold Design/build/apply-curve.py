#!/usr/bin/env python3
"""Clip the six photographs to one curve drawn across the sheet.

Each picture is clipped by the segment of a single curve that falls in its own
panel, so the lower edges join into one line across both folds rather than
three repeated arcs.

The maths has to happen in SHEET coordinates, not per image. The cover's
photograph starts higher than the other five, because that panel carries the
wordmark where the others carry a colour band, so the same percentage means a
different height on the page. Positions come from build/measure-figs.js rather
than from reading the CSS, so this stays correct if the band or photo height
moves.

    node "Trifold Design/build/measure-figs.js"      # what the numbers are
    python3 "Trifold Design/build/apply-curve.py"    # apply them
    node "Trifold Design/build/render.js"
"""
import json, math, re, subprocess, pathlib

HERE = pathlib.Path(__file__).parent
REPO = HERE.parent.parent

raw = subprocess.run(["node", str(HERE / "measure-figs.js")],
                     capture_output=True, text=True, cwd=REPO, check=True).stdout
sheets = {}
for line in raw.strip().splitlines():
    name, payload = line.split(" ", 1)
    sheets[name] = json.loads(payload)

# The curve must stay inside every photograph on both sheets, or it would clip
# one of them away entirely at the ends.
tops = [p["imgTop"] for s in sheets.values() for p in s]
bots = [p["imgBot"] for s in sheets.values() for p in s]
lo, hi = max(tops), min(bots)
# The crest reaches the shallowest photograph's lower edge, so the pictures are
# full at the middle of the spread, and the trough still leaves about two fifths
# of the frame at the outer edges rather than a sliver.
base = lo + 0.45 * (hi - lo)
amp = hi - base

def sheet_y(x):
    """Height of the curve at x, as a fraction of sheet height."""
    return base + amp * math.sin(math.pi * (x ** 0.92))

def clip(p, n=64):
    pts = ["0% 0%", "100% 0%"]
    for i in range(n, -1, -1):
        u = i / n
        y = (sheet_y(p["imgX0"] + u * (p["imgX1"] - p["imgX0"])) - p["imgTop"]) / p["hFrac"]
        pts.append(f"{u*100:.2f}% {max(0.0, min(1.0, y))*100:.2f}%")
    return "clip-path: polygon(" + ", ".join(pts) + ")"

FIG = re.compile(r'(<figure class="figure figure--full[^"]*"[^>]*>\s*<img [^>]*?)(style="([^"]*)")?(>)')
for name, panels in sheets.items():
    f = HERE / f"{name}.html"
    s = re.sub(r';?\s*clip-path: polygon\([^)]*\)', '', f.read_text())
    out, last = [], 0
    for m, panel in zip(FIG.finditer(s), panels):
        keep = (m.group(3) or "").strip().rstrip(";").strip()
        style = (keep + "; " if keep else "") + clip(panel)
        out.append(s[last:m.start()]); out.append(m.group(1) + f'style="{style}"' + m.group(4))
        last = m.end()
    out.append(s[last:])
    f.write_text("".join(out))
    print(f"{name}: curve {base:.4f} to {base+amp:.4f} of sheet height, "
          f"inside every photograph ({lo:.4f} to {hi:.4f})")
