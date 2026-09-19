# Editable PowerPoint, for Canva

`SFW-brochure-2026-EDITABLE.pptx` exists so the team can edit the brochure in
Canva without the layout falling apart.

## Why this and not the PDF

A PDF holds glyphs at coordinates, not text boxes. Canva's importer has to
guess where the text boxes are, and on this layout it guesses wrong: words lose
their spaces (`Countriesinourstudentand`) and blocks reorder themselves. Canva's
own documentation says imported layouts may shift or be flattened.

A PPTX holds real text boxes. Nothing is guessed, so nothing moves.

## How it is built

    node   "Trifold Design/build/extract-layout.js"   # layout.json + bg-*.png
    python3 "Trifold Design/build/make-pptx.py"       # the deck

`extract-layout.js` opens each spread in Chromium and does two things:

1. Records every text block: position, size, font, weight, colour, alpha,
   letter-spacing, line height and alignment, with inline runs kept separate so
   bold and coloured spans survive.
2. Screenshots the spread with `-webkit-text-fill-color: transparent`, which
   removes the glyph paint and nothing else. Photos, colour fields, rules, the
   logo, the QR codes and the `currentColor` icons all stay.

`make-pptx.py` lays that background on a slide and puts each text block back as
a real PowerPoint text box at its measured position.

## What is editable in Canva

Text only. Every paragraph is its own box, with the right font, size, colour and
position. The artwork behind it is a flat image, so photographs and colour
fields cannot be swapped in Canva.

**This is not a press file.** It has no bleed, no trim boxes, no CMYK and no
PDF/X intent, and its artwork is RGB raster. Printing goes from
`SEND-TO-PRINTER/SFW-brochure-2026-print-ready.pdf`, always.

## After changing the artwork

Re-run both commands. The deck is generated, never hand-edited.
