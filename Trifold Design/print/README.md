# Print files

Soil Food Web Foundation trifold, 2026 event brochure.

| File | What it is |
| :-- | :-- |
| `sfw-trifold-outside-CMYK-PDFX.pdf` | Outside: cover, Our story, Teaching. **Send this to the printer.** |
| `sfw-trifold-inside-CMYK-PDFX.pdf` | Inside: Research, Practice, Community. **Send this to the printer.** |
| `sfw-trifold-outside.pdf` / `-inside.pdf` | The same artwork in RGB, before colour conversion. Kept for reference. |

## Specification

- **Trim** 11 x 8.5in, letter, tri-fold. The tucked panel is 1/16in narrower.
- **Bleed** 0.125in on all four sides. Page is 11.25 x 8.75in (810 x 630pt).
- **TrimBox** 9 9 801 621pt, **BleedBox** and **MediaBox** 0 0 810 630pt. No
  visible crop marks: the boxes carry the trim, which is what a modern RIP
  imposes from. Ask if your workflow needs drawn marks and a slug.
- **PDF 1.6, PDF/X-4**, CMYK, with an embedded output intent.
- **Fonts** fully embedded and subsetted.
- **Photographs** 400 to 800 ppi. Nothing is downsampled.

## Two things the printer should know

**The output intent is a generic CMYK profile**, not a press condition. There is
no licensed FOGRA or SWOP profile in this repository and naming one we had not
actually converted through would be worse than declaring a generic one. Re-target
it to your own condition.

**Five to seven small images per sheet are low resolution, and that is correct.**
They are the colour gradients behind the panel headers and the community panel.
The browser writes them as shading patterns and Ghostscript converts pattern
fills to images whatever it is told; the largest lands near 45ppi. They are
smooth two-colour ramps with no detail, and they are marked `/Interpolate` so
the RIP smooths rather than steps them. Preflight will flag them. Everything
else, all type, every rule, and all five QR codes, is vector.

## The QR codes are vector, and this was tested rather than assumed

Building these with Ghostscript's own `-dPDFX` switch destroys them. That switch
forces PDF 1.3, which forbids live transparency, so the page is flattened, and
flattening turned the whole sheet into a single 8100 x 6300 raster with no text,
no paths and no codes. The build therefore converts colour without `-dPDFX` and
adds the PDF/X output intent, boxes and XMP identifier afterwards.

Proof, from `build/make-pdfx.py`'s own checks: every raster image in the file was
replaced with a single white pixel, the page re-rendered, and all five codes
still decoded. They are roughly 2,300 path segments each, not pixels.

## Rebuilding

    python3 "Trifold Design/build/make-qr.py"       # the codes
    node    "Trifold Design/build/render.js"        # 300 DPI PNG proofs
    python3 "Trifold Design/build/check-qr.py"      # decode them back out
    node    "Trifold Design/build/render-pdf.js"    # vector PDF
    python3 "Trifold Design/build/make-pdfx.py"     # CMYK PDF/X-4
