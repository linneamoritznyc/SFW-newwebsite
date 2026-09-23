# Trifold for farmers

The second trifold, for farming and food conferences. First use: Farm Aid
"Homegrown 101", Virginia Beach, September 26, 2026.

## The files

| File | What it is |
| :-- | :-- |
| `print/sfw-farmers-trifold-2page-CMYK-PDFX.pdf` | **The file to send.** 2 pages, page 1 outside, page 2 inside. PDF/X-4, CMYK. |
| `outside-spread.png` | Preview, outside: first flap, back, cover. 300 DPI with bleed. |
| `inside-spread.png` | Preview, inside: microscopy, composting and liquid amendments, holistic management. |
| `COPY-farmers-trifold.txt` | Every word, panel by panel, in reading order, for the Google Doc review. |
| `print/alternates/` | RGB sources, PDF/X-1a, and single sheets, built the same way as the first trifold's. |
| `build/` | The two sheets as markup, the stylesheet, and the build scripts. |

Rebuild, from the repository root:

    python3 trifold-farmers/build/make-qr.py
    python3 trifold-farmers/build/apply-curve.py
    node    trifold-farmers/build/render.js
    node    trifold-farmers/build/render-pdf.js
    python3 trifold-farmers/build/make-pdfx.py
    python3 trifold-farmers/build/check-qr.py

## Print specs, matched to the first trifold

Same as `Trifold Design/print/PRINT-SPEC.md`, which can go to the printer
with this file:

- 11 × 8.5 in flat, roll fold, 0.125 in bleed. Media 810 × 630 pt, trim 9 9 801 621 pt, the same boxes as the first file.
- Panels 3.5 / 3.75 / 3.75 in outside and 3.75 / 3.75 / 3.5 in inside, mirrored. The tuck panel is 1/4 in narrower.
- 0.28 in safe margin. CMYK through the same profile and settings. Photographs capped at 400 ppi. QR codes stay vector.
- Panels sit where the first trifold's do: cover on the outside right, first flap on the outside left (the tuck panel), back in the outside middle, and the three methods across the inside.
- Each position keeps its colour: blue first flap, purple inside left, white inside middle, cream inside right, and green feet on the back and cover.

## Summary

**Specs I could not match exactly: one.** The inside right headline is four lines in the narrow tuck panel. At the first trifold's 0.98 in band height, its eyebrow was pushed into the trim, and headlines always stay. So the colour band is 1.40 in on the **inside sheet only**, on all three panels, so the three photographs still share one edge. Type sizes are unchanged. The outside sheet keeps 0.98 in. That change and one spacing rule (`.pillars + p`, one step of the existing scale) are the only additions, and they sit at the foot of `build/trifold.css`. The first 794 lines are the first trifold's stylesheet, unchanged.

**Images I could not place: none.** All six are the first trifold's own files:

- hands crumbling soil
- Dr. Elaine Ingham at the microscope
- the testate amoeba micrograph with its credit
- the workshop group around the compost pile
- the Rancho Cacachilas plots
- the mentor teaching on working land

The Elaine photograph prints at about 258 ppi, as it does in the first trifold.

**Copy cut: none.** Everything fits at the first trifold's own spacing. The shorter copy leaves open space on the first flap, the cover, and the inside left and middle. No filler was added.

**Things to check:**

1. **`soilfoodweb-qr.png` was not in the repository.** It is made in `build/make-qr.py` from `https://soilfoodweb.com/`, in the first trifold's QR style: error correction H, four-module quiet zone, moss `#22371F` on white. The PDF places its SVG twin, so the code stays vector like the others. If you have your own `soilfoodweb-qr.png`, it is a plain link to the homepage, so this one does the same job.
2. **The back code has no tracking.** It goes straight to soilfoodweb.com, as the brief says, not through a Switchy link. Scans from this brochure will not show up under a campaign. If you want them to, point it at a Switchy link instead: a one-line change in `make-qr.py`, then rebuild.
3. **On the inside right, the box sits above the case studies code, not below it.** The brief lists the code first. The first trifold's layout, which this design keeps, puts the call to action last on the panel. Tell me if you want them swapped.
4. **The inside left is purple.** It keeps its position's colour from the first trifold. There, the stylesheet reserves Legacy Purple for Dr. Elaine content, and this panel is now Microscopy.

**Checks run:**

- Both QR codes decode from both previews and from every page of every PDF (`build/check-qr.py`).
- Every word in the print PDF matches `COPY-farmers-trifold.txt`.
- No em dashes.
- No panel overflows.

**The first trifold is unchanged.** All 110 files under `Trifold Design/`, `SEND-TO-PRINTER/` and `exports/` are byte-identical to before this work, checked by SHA-256. The case studies code here is a byte-identical copy of its file.
