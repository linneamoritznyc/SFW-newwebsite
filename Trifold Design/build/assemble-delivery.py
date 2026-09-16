#!/usr/bin/env python3
"""Collect everything anyone needs to download into one folder, named clearly.

    python3 "Trifold Design/build/assemble-delivery.py"

Run it after a rebuild. It copies rather than being the place things are built,
so the folder can never hold a stale file that quietly disagrees with the
artwork: delete it and run this again and it is exactly the current build.
"""
import hashlib, pathlib, shutil, zipfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "exports" / "brochure-2026"
TRI = ROOT / "Trifold Design"

FILES = {
    # the one to send
    "sfw-trifold-2page-CMYK-PDFX.pdf":   TRI / "print/sfw-trifold-2page-CMYK-PDFX.pdf",
    # separates, and the X-1a fallback for shops that ask for it
    "sfw-trifold-outside-CMYK-PDFX.pdf": TRI / "print/sfw-trifold-outside-CMYK-PDFX.pdf",
    "sfw-trifold-inside-CMYK-PDFX.pdf":  TRI / "print/sfw-trifold-inside-CMYK-PDFX.pdf",
    "sfw-trifold-2page-CMYK-PDFX1a.pdf": TRI / "print/sfw-trifold-2page-CMYK-PDFX1a.pdf",
    # proofs, for looking at and for anyone who wants a picture
    "sfw-trifold-outside-300dpi.png":    TRI / "outside-spread.png",
    "sfw-trifold-inside-300dpi.png":     TRI / "inside-spread.png",
    # the codes on their own
    "sfw-brochure-qr-webinar.png":       ROOT / "exports/qr/sfw-brochure-qr-webinar.png",
    "sfw-brochure-qr-scholarship.png":   ROOT / "exports/qr/sfw-brochure-qr-scholarship.png",
    "sfw-brochure-qr-casestudies.png":   ROOT / "exports/qr/sfw-brochure-qr-casestudies.png",
    "sfw-brochure-qr-community.png":     ROOT / "exports/qr/sfw-brochure-qr-community.png",
    "sfw-brochure-qr-donate.png":        ROOT / "exports/qr/sfw-brochure-qr-donate.png",
}

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)

missing = [n for n, p in FILES.items() if not p.exists()]
if missing:
    raise SystemExit("not built yet: " + ", ".join(missing))

for name, src in FILES.items():
    shutil.copy2(src, OUT / name)

# The README lives in build/ as a source file, not written into the folder by
# hand: this script deletes the folder every run, so a note left in there would
# be destroyed by the next rebuild. It was, once.
shutil.copy2(pathlib.Path(__file__).parent / "delivery-README.md", OUT / "README.md")

with zipfile.ZipFile(OUT / "sfw-brochure-2026-all.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for name in FILES:
        z.write(OUT / name, name)

for name in list(FILES) + ["sfw-brochure-2026-all.zip"]:
    p = OUT / name
    digest = hashlib.sha256(p.read_bytes()).hexdigest()[:12]
    print(f"  {name:<36}{p.stat().st_size/1024:>9.0f} KB  {digest}")
