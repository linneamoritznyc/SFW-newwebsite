# Trifold for farmers

The first trifold (`Trifold Design/`) with the farmers copy. First use: Farm Aid
"Homegrown 101," Virginia Beach, September 26, 2026.

**Status: stopped at overflow. Not print-ready. No print PDF has been built.**
Five panels overflow at the first trifold's type sizes, and two headlines push
their eyebrows into or past the trim. Per the brief, all the copy is kept and
nothing was changed to make it fit. The overflow report is below.

## The files

| File | What it is |
| :-- | :-- |
| `outside-spread.png` | Preview, outside sheet: Teaching, Community (back), Cover. 300 DPI with bleed. |
| `inside-spread.png` | Preview, inside sheet: Our story, Research, Practice. |
| `COPY-farmers-trifold.txt` | Every word, panel by panel, for the Google Doc review. |
| `build/` | The two sheets as markup, the first trifold's stylesheet (byte-identical), and the build scripts. |

The previews show the overflow as it is. Content past the foot of a panel is
cut off, and the Practice QR code is not visible at all.

## Overflow

Measured at the first trifold's type sizes and spacing. One line of body text
is about 0.16 in.

| Panel | Where | Too long by | Also |
| :-- | :-- | :-- | :-- |
| 1. Cover | outside, right | fits | |
| 2. Our story | inside, left | **0.46 in**, about 3 lines | The webinar QR code runs off the foot. Body 3 (Rodale) is longer than the paragraph it replaces, and the first trifold's "Why this matters for climate" box is kept, as the brief keeps every box. |
| 3. Teaching | outside, left, fold-in | **0.34 in**, about 3 lines | The scholarship QR code runs into the bottom margin. |
| 4. Research | inside, middle | **0.90 in**, about 6 lines | The YouTube closing line is cut off. |
| 5. Practice | inside, right, fold-in | **1.47 in**, about 9 lines | The case studies QR code is off the panel. The headline runs to 4 lines, which pushes the PRACTICE eyebrow 0.12 in **past the trim**, so it would be cut off. |
| 6. Community | outside, middle, the back | **0.26 in**, about 2 lines | The headline runs to 3 lines. That puts the COMMUNITY eyebrow 0.08 in from the trim, inside the 0.28 in safe margin. The green foot sits 0.26 in lower than the cover's, so the two no longer line up across the fold. |

In the first trifold, every eyebrow sits exactly at the 0.28 in safe margin,
and every headline is 2 lines.

## Anything I could not match

- **Print specs:** nothing yet. The sheet, panels, fold, bleed, margins, type, colours, photographs, photo positions, and boxes are the first trifold's. The stylesheet is a byte-identical copy. The print scripts are the first trifold's, repointed to this folder. Once the overflow is settled, they produce the same PDF/X-4 CMYK file with the same boxes.
- **QR codes:** your copy puts the scholarship code on Teaching. That is where the first trifold carried it before the Foundation Courses code replaced it on September 22, so its original file is restored from the history, in Education Blue. The community code on the back is restored the same way, in moss.
- **Back "Learn more" code:** it uses Linnea's tracked Switchy link `https://www.sfw.one/brochure-website` (her upload is in `qr-uploads/`). It is redrawn in the brochure's moss, as vector art like the other codes, in `build/make-qr.py`. It takes the donate code's place in the green foot. The Switchy link redirects to soilfoodweb.com.
- **Cover subheadline:** the first trifold's cover has no subheadline. "The soil beneath our farms and forests is alive." is set as the heading style directly under "Grow your own biology."
- **Research closing line:** the YouTube link is printed as `[LINK: YouTube channel short link, to be confirmed]`, exactly as the copy has it. It must be replaced before print.

## The first trifold is unchanged

All 110 files under `Trifold Design/`, `SEND-TO-PRINTER/`, and `exports/` are
byte-identical to before this work, checked by SHA-256.

## Rebuild

From the repository root:

    python3 trifold-farmers/build/make-qr.py
    python3 trifold-farmers/build/apply-curve.py
    node    trifold-farmers/build/render.js          # previews + overflow report
    node    trifold-farmers/build/render-pdf.js      # only once nothing overflows
    python3 trifold-farmers/build/make-pdfx.py
    python3 trifold-farmers/build/check-qr.py
