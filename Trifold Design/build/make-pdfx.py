#!/usr/bin/env python3
"""Turn the vector PDFs into CMYK PDF/X-4 with trim and bleed marked.

    node "Trifold Design/build/render-pdf.js"    # first, the vector PDFs
    python3 "Trifold Design/build/make-pdfx.py"

Two decisions here, both the result of watching what the tools actually did.

NOT -dPDFX. Ghostscript's PDF/X switch forces PDF 1.3, which forbids live
transparency, so it flattens the page, and flattening rasterised the ENTIRE
sheet to a single 8100x6300 image: no text, no paths, no QR codes, one picture.
So the conversion runs without it and the PDF/X parts, the output intent, the
boxes and the XMP identifier, are written here afterwards. The codes stay as
about 2,300 path segments each, which is the point of shipping a PDF at all.

/Interpolate on the gradient ramps. Chromium writes the CSS gradients as
shading patterns, and Ghostscript turns pattern fills into images whatever
flags it is given; the largest comes out around 45ppi. They are smooth
two-colour ramps, not detail, so the fix is to mark them interpolated and let
the RIP smooth them rather than step them. Photographs are untouched. A
preflight report will still list those few images as low resolution; that is
expected and it is what they are.
"""
import pathlib, subprocess, sys
import pikepdf

HERE = pathlib.Path(__file__).parent
PRINT = HERE.parent / "print"
ICC = pathlib.Path("/usr/share/ghostscript/10.02.1/iccprofiles/default_cmyk.icc")

PT = 72.0
BLEED, TRIM_W, TRIM_H = 0.125 * PT, 11.0 * PT, 8.5 * PT
MEDIA = (TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED)          # 810 x 630 pt
TRIM = (BLEED, BLEED, MEDIA[0] - BLEED, MEDIA[1] - BLEED)  # 9 9 801 621
INTERPOLATE_BELOW_PPI = 200

XMP = """<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:pdf="http://ns.adobe.com/pdf/1.3/"
    xmlns:pdfx="http://ns.adobe.com/pdfx/1.3/"
    xmlns:pdfxid="http://www.npes.org/pdfx/ns/id/"
    xmlns:xmp="http://ns.adobe.com/xap/1.0/">
   <dc:title><rdf:Alt><rdf:li xml:lang="x-default">Soil Food Web Foundation trifold</rdf:li></rdf:Alt></dc:title>
   <pdfxid:GTS_PDFXVersion>PDF/X-4</pdfxid:GTS_PDFXVersion>
   <pdf:Trapped>False</pdf:Trapped>
   <xmp:CreatorTool>Soil Food Web Foundation trifold build</xmp:CreatorTool>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>"""


def to_cmyk(src, dst):
    """Colour-convert to CMYK, keeping every vector as a vector."""
    cmd = [
        "gs", "-dBATCH", "-dNOPAUSE", "-dQUIET", "-dSAFER",
        "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.6",
        "-dProcessColorModel=/DeviceCMYK", "-sColorConversionStrategy=CMYK",
        "-dOverrideICC=true", f"-sOutputICCProfile={ICC}",
        "-dDownsampleColorImages=false", "-dDownsampleGrayImages=false",
        "-dDownsampleMonoImages=false", "-dAutoFilterColorImages=false",
        "-dColorImageFilter=/DCTEncode",
        f"-sOutputFile={dst}", str(src),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stdout + r.stderr)


def finish(path):
    """Boxes, output intent, XMP, and interpolation on the gradient ramps."""
    with pikepdf.open(path, allow_overwriting_input=True) as pdf:
        page = pdf.pages[0]
        page.MediaBox = pikepdf.Array([0, 0, *MEDIA])
        page.CropBox = pikepdf.Array([0, 0, *MEDIA])
        page.BleedBox = pikepdf.Array([0, 0, *MEDIA])
        page.TrimBox = pikepdf.Array(list(TRIM))
        page.ArtBox = pikepdf.Array(list(TRIM))

        icc = pdf.make_stream(ICC.read_bytes())
        icc.N = 4
        intent = pdf.make_indirect(pikepdf.Dictionary(
            Type=pikepdf.Name("/OutputIntent"),
            S=pikepdf.Name("/GTS_PDFX"),
            OutputCondition=pikepdf.String("Generic CMYK"),
            OutputConditionIdentifier=pikepdf.String("Custom"),
            Info=pikepdf.String("Generic CMYK. Re-target to the press condition."),
            DestOutputProfile=icc))
        pdf.Root.OutputIntents = pikepdf.Array([intent])
        pdf.Root.Metadata = pdf.make_stream(
            XMP.encode("utf-8"), Type=pikepdf.Name("/Metadata"),
            Subtype=pikepdf.Name("/XML"))
        with pdf.open_metadata() as m:
            m["dc:title"] = "Soil Food Web Foundation trifold"

        # A transparency group that blends in DeviceRGB inside a CMYK PDF/X
        # file is a conformance failure, and it blends in the wrong space
        # besides. Chromium writes one; retarget it.
        regrouped = 0
        for obj in pdf.objects:
            try:
                if (str(obj.get("/Type")) == "/Group"
                        and str(obj.get("/S")) == "/Transparency"
                        and str(obj.get("/CS")) == "/DeviceRGB"):
                    obj.CS = pikepdf.Name("/DeviceCMYK")
                    regrouped += 1
            except (AttributeError, TypeError):
                continue

        smoothed = 0
        for name, xo in dict(page.Resources.get("/XObject", {})).items():
            if str(xo.get("/Subtype")) != "/Image":
                continue
            w = int(xo.Width)
            # width in points the image occupies is not in the object, so use a
            # proxy: the gradient ramps are the only images narrower than 600px.
            if w < 600:
                xo.Interpolate = True
                smoothed += 1

        # pikepdf edits an in-memory copy; without this the file on disk keeps
        # the boxes and the missing output intent it had before.
        pdf.save(path)
        return smoothed, regrouped


def main():
    if not ICC.exists():
        sys.exit(f"no CMYK profile at {ICC}")
    for src in ("outside", "inside"):
        i = PRINT / f"sfw-trifold-{src}.pdf"
        o = PRINT / f"sfw-trifold-{src}-CMYK-PDFX.pdf"
        to_cmyk(i, o)
        n, g = finish(o)
        print(f"{o.name}  {o.stat().st_size/1024/1024:.2f} MB  "
              f"({n} gradient ramp(s) interpolated, {g} blend group(s) to CMYK)")


if __name__ == "__main__":
    main()
