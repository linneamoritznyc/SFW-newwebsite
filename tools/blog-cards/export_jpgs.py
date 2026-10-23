"""Turn the builder's PPTX output into the five JPGs per post, one folder per post.

usage: python3 tools/blog-cards/export_jpgs.py PPTXDIR OUTDIR slug:"Folder name" [slug:"Folder name" ...]

PPTXDIR is what build.py wrote (run with STYLE=brand ONLY=slug1,slug2). The posts
must be listed in the same order as in POSTS, since each size file has one slide
per post in that order. Files come out as {slug}--{Size}.jpg.
"""
import io, os, subprocess, sys
import pymupdf
from PIL import Image

SIZES = {'desktop-header-1920x720': 'Desktop-1920x720', 'tablet-header-1024x768': 'Tablet-1024x768',
         'mobile-header-750x1000': 'Mobile-750x1000', 'feature-social-1400x1400': 'Social-Square-1400x1400',
         'thumbnail-1200x800': 'Thumbnail-3x2-1200x800'}

pptxdir, outdir = sys.argv[1], sys.argv[2]
pairs = [a.split(':', 1) for a in sys.argv[3:]]
for key, name in SIZES.items():
    pptx = os.path.join(pptxdir, f'SFW-blog-cards--{key}--brand.pptx')
    subprocess.run(['soffice', '-env:UserInstallation=file:///tmp/lo_prof', '--headless', '--convert-to', 'pdf',
                    '--outdir', pptxdir, pptx], check=True, capture_output=True, timeout=600)
    w, h = map(int, key.rsplit('-', 1)[1].split('x'))
    doc = pymupdf.open(pptx[:-5] + '.pdf')
    for i, (slug, folder) in enumerate(pairs):
        page = doc[i]
        pix = page.get_pixmap(matrix=pymupdf.Matrix(w / page.rect.width * 2, h / page.rect.height * 2))
        im = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB').resize((w, h), Image.LANCZOS)
        d = os.path.join(outdir, folder); os.makedirs(d, exist_ok=True)
        im.save(os.path.join(d, f'{slug}--{name}.jpg'), quality=92, subsampling=0, optimize=True)
        print(os.path.join(d, f'{slug}--{name}.jpg'))
