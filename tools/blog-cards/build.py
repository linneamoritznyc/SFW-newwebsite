"""Blog cards: one editable .pptx per size, one slide per post.

Layers on every slide, bottom to top, each movable on its own in Canva:
  colour field (native shapes) > photo planes (one PNG each) > cream card
  > category word > headline > deck > READ POST button > cursor > web address
"""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = sys.argv[1]
TMP = os.path.join(OUT, '_layers')
os.makedirs(TMP, exist_ok=True)
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
PX = 9525  # EMU per px at 96 dpi
STYLE = os.environ.get('STYLE', 'rect')   # rect | window | lens | print
ONLY = [x for x in os.environ.get('ONLY', '').split(',') if x]

def hexrgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# Colour fields. The yellow pair is Linnea's, off the PDC card. The rest are
# site tokens from css/site.css, paired light over mid the same way.
FIELDS = {
    'yellow': ('#FBE77C', '#E6D156'),
    'glow':   ('#E4ECBC', '#A2AE77'),   # --glow lifted / --living
    'tan':    ('#F1DECF', '#C89B7B'),   # --tan
    'green':  ('#E6EADC', '#A7B097'),   # --panel-green / --sage
    'legacy': ('#E3D9EA', '#9E8FC2'),   # Dr. Elaine: lavender / --membrane
}
CREAM = '#F4F1EA'
INK = '#141312'
LEGACY = '#6B4C7A'

# Titles are the live titles, split at their own colon or dash into a
# headline and a deck line. Nothing added. The PDC card is Linnea's wording.
POSTS = [
 dict(slug='fungi-to-bacteria-ratio-history', date='undated', cat='Education', field='glow',
      head='A brief history of the fungi-to-bacteria ratio',
      deck='Knowledge of not only the science, but also its history, is important for any grower considering the transition',
      img='img/fungal-spores-in-suspension.jpg', focus=(.5, .5)),
 dict(slug='what-is-your-soil-test-telling-you', date='undated', cat='Blog', field='tan',
      head='What is your soil test really telling you?', deck='',
      img='tools/blog-cards/photos/what is your soil test really telling you? .jpeg', focus=(.4, .4)),
 dict(slug='ciliates-microscope-watermelon', date='2026-05-01', cat='Microscopy', field='glow',
      head='Ciliates, Cysts, and the Clues Hiding in a Struggling Watermelon Crop',
      deck='How a rare microscope sighting helps deduce the problem with unhealthy soil',
      img='img/uploads/Testate amoeba (encysting), 40x obj, Joy Kaluf.jpg', focus=(.5, .5)),
 dict(slug='permaculture-design-certificate', date='2026-04-13', cat='Education', field='yellow',
      head='SFW Launches first ever Permaculture Design Certificate', deck='',
      img='img/garden-vegetable-beds.jpg', focus=(.5, .5)),
 dict(slug='advanced-programs-reopening', date='2026-02-23', cat='School Updates', field='yellow',
      head='Soil Food Web School Advanced Programs Are Reopening!', deck='',
      img='tools/blog-cards/photos/Students and mentors practice microscopy together at our workshop in Costa Rica, March 2025. .jpg', focus=(0.5, 0.5)),
 dict(slug='obituary-dr-elaine-ingham', date='2026-02-18', cat='In Memoriam', field='legacy',
      head='Obituary for Dr. Elaine Ingham', deck='',
      img='tools/blog-cards/photos/Elaine Obituary, team with a sign that says Elaine .jpg', focus=(0.5, 0.55)),
 dict(slug='new-board-member-eric-feiler', date='2026-02-17', cat='Foundation Update', field='green',
      head='The Soil Food Web Welcomes a New Board Member', deck='Eric Feiler',
      img='img/erc-rancho-cacachilas-aerial-2.jpg', focus=(0.5, 0.5)),
 dict(slug='2025-in-review', date='2025-12-30', cat='Blog', field='green',
      head='2025 in Review: A time of transition',
      deck='Honoring our founder and guiding spirit, building stronger community, and preparing for a bright future',
      img='tools/blog-cards/photos/SFW School Mentor Gerald Ramirez (center) demonstrates production of liquid amendments at our workshop in Costa Rica, March 2025. .jpg', focus=(0.5, 0.45)),
 dict(slug='living-legacy-webinar-series', portrait=True, date='2025-11-03', cat='Events', field='legacy',
      head='A Living Legacy', deck='Join the free webinar series: The Science of the Soil Food Web',
      img='img/Dr Elaine Ingham with Microscope.jpg', focus=(.5, .4)),
 dict(slug='soil-health-week-pakistan', date='2025-10-22', cat='Events', field='tan',
      head='Soil Health Week 2025',
      deck='Wild Soils UK and TrashIt bring the Soil Food Web approach to Pakistan',
      img='tools/blog-cards/photos/Bridging Global Expertise and Local Action Soil Health Week Pakistan 2025 showcased the growing global impact of the Soil Food Web approach—demonstrating how soil biology can transform agriculture from the ground up. blog.png', focus=(0.5, 0.45)),
 dict(slug='foundation-launches-as-nonprofit', portrait=True, date='2025-10-17', cat='Foundation Update', field='green',
      head='Soil Food Web Foundation Launches as Nonprofit',
      deck='To carry forward Dr. Elaine Ingham’s legacy',
      img='tools/blog-cards/photos/Elaine Ruth Ingham, groundbreaking microbiologist and a leader in the regenerative agriculture movement, holding soil.jpg', focus=(0.5, 0.4)),
 dict(slug='retirement-dr-elaine-ingham', portrait=True, date='2025-10-16', cat='School Updates', field='legacy',
      head='Retirement Announcement: Dr. Elaine Ingham', deck='',
      img='img/copy-of-17.jpg', focus=(.6, .3)),
 dict(slug='october-2025-newsletter', date='2025-10-09', cat='Blog', field='yellow',
      head='October 2025 Newsletter', deck='',
      img='img/hand-of-compost.jpg', focus=(.5, .5)),
 dict(slug='sacramento-food-knowledge-culture', date='2025-09-23', cat='Events', field='tan',
      head='Help us celebrate food, knowledge and culture in Sacramento this September', deck='',
      img='img/uploads/carrot-growing-in-vegitable-bed-community-garden-2025-01-08-04-14-23-utc.jpg', focus=(.5, .4)),
]

# Per size: the photo zone, the card, and the type scale. px.
SIZES = {
 'feature-social-1400x1400': dict(W=1400, H=1400, zone=(430, 0, 970, 1040),  card=(84, 450, 960, 870),  pad=80, cat=150, head=116, deck=42, btn=44, clean=True, shape_zone=(420, 0, 980, 980), shape_card=(64, 620, 830, 716)),
 'mobile-header-750x1000':   dict(W=750,  H=1000, zone=(0, 0, 750, 590),     card=(30, 390, 690, 580),   pad=46, cat=82,  head=66, deck=26, btn=28, clean=True),
 'desktop-header-1920x720': dict(W=1920, H=720, zone=(700, 0, 1220, 720), card=(96, 56, 800, 608), pad=64, cat=104, head=86, deck=32, btn=34, clean=True),
 'tablet-header-1024x768':   dict(W=1024, H=768,  zone=(380, 0, 644, 768),   card=(44, 110, 660, 610),   pad=46, cat=74,  head=60, deck=24, btn=26, clean=True),
}

# The cubist planes, in zone coordinates 0..1. Each shows the same photograph
# from a slightly different distance and angle of view: scale, shift, and a
# tone. That is the move: one subject, several viewpoints, one surface.
PLANES = [
 dict(pts=[(0, 0), (.64, 0), (.50, .56), (0, .44)],         s=1.00, d=(0, 0),       tone=None),
 dict(pts=[(.64, 0), (1, 0), (1, .50), (.50, .56)],         s=1.22, d=(.06, -.03),  tone=('mid', .30)),
 dict(pts=[(0, .44), (.50, .56), (.38, 1), (0, 1)],         s=1.08, d=(-.04, .03),  tone=('grey', 0)),
 dict(pts=[(.50, .56), (1, .50), (1, 1), (.38, 1)],         s=1.10, d=(.03, .05),   tone=('light', .18)),
 dict(pts=[(.42, .26), (.74, .33), (.64, .74), (.33, .66)], s=1.45, d=(-.02, .01),  tone=None),
]

PLANES_PORTRAIT = [
 dict(pts=[(0, 0), (1, 0), (1, .70), (.72, .80), (0, .74)],   s=1.00, d=(0, 0),      tone=None),
 dict(pts=[(0, .74), (.72, .80), (.60, 1), (0, 1)],          s=1.08, d=(-.04, .04), tone=('grey', 0)),
 dict(pts=[(.72, .80), (1, .70), (1, 1), (.60, 1)],          s=1.25, d=(.05, .06),  tone=('mid', .30)),
 dict(pts=[(.80, .06), (1, .02), (1, .40), (.86, .44)],      s=1.35, d=(.10, -.02), tone=('light', .20)),
]

def font(name, size): return ImageFont.truetype(os.path.join(FONTS, name), max(1, int(size)))
F_CAT, F_HEAD, F_BTN = 'Montserrat-Bold.ttf', 'SourceSans3-Regular.ttf', 'EBGaramond-Regular.ttf'

def wrap(text, fnt, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if fnt.getlength(t) <= width or not cur: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def fit(text, fname, size, width, max_lines, floor):
    # Step down until it fits. The 0.93 leaves room for Canva's own metrics.
    while size > floor:
        f = font(fname, size)
        lines = wrap(text, f, width * .93)
        if len(lines) <= max_lines and max(f.getlength(l) for l in lines) <= width * .93: return size, lines
        size -= 1
    return size, wrap(text, font(fname, size), width * .93)

PHOTOS = os.path.join(REPO, 'tools', 'blog-cards', 'photos')

def photo_for(post):
    # a post's own photograph, uploaded to photos/ under its slug, wins over the stand-in
    for ext in ('jpg', 'jpeg', 'png', 'webp', 'JPG', 'JPEG', 'PNG'):
        f = os.path.join(PHOTOS, f"{post['slug']}.{ext}")
        if os.path.exists(f): return f
    return os.path.join(REPO, post['img'])

def grade(im):
    # One grade for every photograph, so pictures from many cameras read as a
    # set: levels set per photo, colour eased back a touch, and the highlights
    # warmed toward the cream of the card.
    from PIL import ImageEnhance
    im = ImageOps.autocontrast(im, cutoff=(.4, .8))
    im = ImageEnhance.Color(im).enhance(.9)
    warm = Image.new('RGB', im.size, hexrgb(CREAM))
    return Image.blend(im, Image.composite(warm, im, ImageOps.grayscale(im).point(lambda v: int(max(0, v - 150) * 1.2))), .5)

def cover(img, w, h, focus):
    return ImageOps.fit(img, (w, h), Image.LANCZOS, centering=focus)

def plane_png(post, key, zone, p, i, field):
    zx, zy, zw, zh = zone
    src = ImageOps.exif_transpose(Image.open(photo_for(post))).convert('RGB')
    s = p['s']
    # as sharp as the photograph allows, up to 2x the slide: never upscaled
    # past its own pixels, which only makes the file bigger
    k = max(1, min(2, min(src.width / (zw * s), src.height / (zh * s))))
    ZW, ZH = int(zw * k), int(zh * k)
    big = cover(src, int(ZW * s), int(ZH * s), post['focus'])
    ox = int((big.width - ZW) / 2 + p['d'][0] * ZW)
    oy = int((big.height - ZH) / 2 + p['d'][1] * ZH)
    ox = max(0, min(ox, big.width - ZW)); oy = max(0, min(oy, big.height - ZH))
    view = grade(big.crop((ox, oy, ox + ZW, oy + ZH)))
    tone = p['tone']
    if tone:
        kind, a = tone
        if kind == 'grey':
            view = ImageOps.grayscale(view).convert('RGB')
            view = Image.blend(view, Image.new('RGB', view.size, hexrgb(FIELDS[field][1])), .12)
        else:
            c = FIELDS[field][1 if kind == 'mid' else 0]
            view = Image.blend(view, Image.new('RGB', view.size, hexrgb(c)), a)
    pts = [(x * ZW, y * ZH) for x, y in p['pts']]
    mask = Image.new('L', view.size, 0)
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    rgba = view.copy(); rgba.putalpha(mask)
    # a cream seam where the planes meet, like the cut edge of paper
    d = ImageDraw.Draw(rgba)
    if p.get('seam', True): d.line(pts + [pts[0]], fill=hexrgb(CREAM) + (255,), width=max(2, int(3 * k)))
    x0, y0 = int(min(x for x, _ in pts)), int(min(y for _, y in pts))
    x1, y1 = int(math.ceil(max(x for x, _ in pts))), int(math.ceil(max(y for _, y in pts)))
    rgba = rgba.crop((x0, y0, x1, y1))
    if not p.get('seam', True):
        # a whole rectangle needs no transparency: a full-resolution JPEG at
        # high quality keeps the detail at a fraction of the PNG's weight
        path = os.path.join(TMP, f'{key}--{post["slug"]}--photo.jpg')
        rgba.convert('RGB').save(path, quality=93, subsampling=0)
    else:
        path = os.path.join(TMP, f'{key}--{post["slug"]}--plane{i+1}.png')
        rgba.save(path, compress_level=6)
    return path, zx + x0 / k, zy + y0 / k, (x1 - x0) / k, (y1 - y0) / k

def rgb(sh, h): sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor(*hexrgb(h)); sh.line.fill.background()

def poly(slide, pts, colour, name):
    fb = slide.shapes.build_freeform(Emu(int(pts[0][0] * PX)), Emu(int(pts[0][1] * PX)), scale=1.0)
    fb.add_line_segments([(Emu(int(x * PX)), Emu(int(y * PX))) for x, y in pts[1:]], close=True)
    sh = fb.convert_to_shape(); rgb(sh, colour); sh.name = name; sh.shadow.inherit = False
    return sh

def rect(slide, x, y, w, h, colour, name):
    sh = slide.shapes.add_shape(1, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
    rgb(sh, colour); sh.name = name; sh.shadow.inherit = False
    return sh

def text(slide, x, y, w, h, s, face, px, colour, name, bold=False, spacing=None, line=None, align=None, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
    tb.name = name
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.text = s
    if align: p.alignment = align
    if line: p.line_spacing = Pt(line * .75)  # exact, in px
    for r in p.runs:
        r.font.name = face; r.font.size = Pt(px * .75); r.font.bold = bold
        r.font.color.rgb = RGBColor(*hexrgb(colour))
        if spacing is not None: r._r.get_or_add_rPr().set('spc', str(int(spacing)))
    return tb

def field_shapes(slide, W, H, field, key):
    light, mid = FIELDS[field]
    rect(slide, 0, 0, W, H, light, 'Field light')
    # the mid plane: a sweep in from the top right that bends round, like the
    # yellow on the PDC card, but cut with a straight edge where it meets the photo
    arc = [(W * .70 - W * .70 * t, H * .30 + H * .30 * math.sin(t * math.pi / 2)) for t in [i / 24 for i in range(25)]]
    poly(slide, [(W * .78, 0), (W, 0), (W, H), (0, H)] + list(reversed(arc)), mid, 'Field mid')
    # a white corner, echoing the PDC card
    poly(slide, [(W, H * .86), (W, H), (W - H * .14, H)], '#FFFFFF', 'Corner')

def shade(h, f):
    r, g, b = hexrgb(h); return '#%02X%02X%02X' % tuple(int(c * f) for c in (r, g, b))

def field_planes(slide, W, H, field, slug):
    # Flat overlapping planes of colour, the cubist move made on the ground
    # instead of the photograph. Same grammar on every card; the angles shift
    # a little per post (seeded on its name) so the set is a family, not clones.
    import random
    rnd = random.Random(slug)
    j = lambda v, a=.04: v + rnd.uniform(-a, a)
    light, mid = FIELDS[field]
    rect(slide, 0, 0, W, H, light, 'Field light')
    poly(slide, [(0, H * j(.58)), (W * j(.46), H * j(.40)), (W * j(.62), H), (0, H)], mid, 'Plane mid')
    poly(slide, [(W * j(.70), 0), (W, 0), (W, H * j(.46)), (W * j(.84), H * j(.30))], shade(mid, .86), 'Plane deep')
    poly(slide, [(W * j(.52), H), (W * j(.80), H * j(.70)), (W, H * j(.78)), (W, H)], shade(light, .97), 'Plane pale')
    poly(slide, [(W, H * .86), (W, H), (W - H * .14, H)], '#FFFFFF', 'Corner')

def oval(slide, x, y, w, h, fill, name, line=None, lw=0):
    sh = slide.shapes.add_shape(9, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
    sh.name = name; sh.shadow.inherit = False
    if fill: sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor(*hexrgb(fill))
    else: sh.fill.background()
    if line: sh.line.color.rgb = RGBColor(*hexrgb(line)); sh.line.width = Emu(int(lw * PX))
    else: sh.line.fill.background()
    return sh

def arch_pts(x, y, w, h, n=40):
    r = w / 2
    pts = [(x, y + h), (x, y + r)]
    pts += [(x + r - r * math.cos(math.pi * t / n), y + r - r * math.sin(math.pi * t / n)) for t in range(n + 1)]
    pts += [(x + w, y + h)]
    return pts

def shaped_photo(slide, post, key, box, shape, field):
    # the whole photograph, shaped: an arch, a lens or a mounted print. Never cut.
    bx, by, bw, bh = box
    src = ImageOps.exif_transpose(Image.open(photo_for(post))).convert('RGB')
    k = max(1, min(2, min(src.width / bw, src.height / bh)))
    img = grade(cover(src, int(bw * k), int(bh * k), post['focus']))
    mid = FIELDS[field][1]
    if shape == 'print':
        off = bw * .045
        rect(slide, bx + off, by + off, bw, bh, shade(mid, .78), 'Print shadow block')
        rect(slide, bx - bw * .025, by - bw * .025, bw * 1.05, bh + bw * .05, '#FFFFFF', 'Print border')
        path = os.path.join(TMP, f'{key}--{post["slug"]}--print.jpg')
        img.save(path, quality=93, subsampling=0)
    else:
        mask = Image.new('L', img.size, 0); d = ImageDraw.Draw(mask)
        if shape == 'lens':
            d.ellipse((0, 0, img.width - 1, img.height - 1), fill=255)
            oval(slide, bx + bw * .06, by + bh * .06, bw, bh, shade(mid, .82), 'Lens shadow')
        else:
            d.polygon(arch_pts(0, 0, img.width, img.height), fill=255)
            poly(slide, arch_pts(bx + bw * .07, by - bh * .04, bw, bh), shade(mid, .82), 'Window shadow')
        img = img.copy(); img.putalpha(mask)
        path = os.path.join(TMP, f'{key}--{post["slug"]}--{shape}.png')
        img.save(path, compress_level=6)
    pic = slide.shapes.add_picture(path, Emu(int(bx * PX)), Emu(int(by * PX)), Emu(int(bw * PX)), Emu(int(bh * PX)))
    pic.name = 'Photo'
    if shape == 'lens':
        # the field of view: a fine ring, like looking down the eyepiece
        oval(slide, bx - bw * .03, by - bh * .03, bw * 1.06, bh * 1.06, None, 'Lens ring', line=INK, lw=max(2, bw * .004))


# ---------------------------------------------------------------------------
# BRAND: the website's own design system (docs/brand-guide.html), nothing new.
# White page. The photograph whole. A cream panel as a bounded shape with the
# 12px card radius and the site's one shadow. Eyebrow in Food Web Green,
# headline Montserrat in Soil Brown, the quiet line in EB Garamond italic, the
# primary button in Food Web Green with the 8px radius. Legacy Purple only on
# Dr. Elaine posts. The roundel on white, where it reads.
BR = dict(paper='#FFFFFF', cream='#F4F1EA', green='#156826', soil='#4F3433',
          ink_soft='#4A463F', ink_faint='#6A665C', legacy='#6B4C7A', case='#E6EADC')
BRAND_SIZES = {
 'feature-social-1400x1400': dict(photo=(0, 0, 1400, 830),   card=(84, 640, 1232, 676), pad=72, eye=26, head=84, deck=38, btn=30, logo=112),
 'desktop-header-1920x720':  dict(photo=(760, 0, 1160, 720), card=(80, 72, 820, 576),  pad=64, eye=22, head=64, deck=30, btn=26, logo=92),
 'tablet-header-1024x768':   dict(photo=(0, 0, 1024, 430),   card=(52, 320, 920, 404),  pad=44, eye=18, head=48, deck=22, btn=20, logo=70),
 'mobile-header-750x1000':   dict(photo=(0, 0, 750, 560),    card=(34, 430, 682, 530),  pad=40, eye=17, head=44, deck=21, btn=19, logo=64),
}
ELAINE = {'obituary-dr-elaine-ingham', 'living-legacy-webinar-series', 'retirement-dr-elaine-ingham', 'foundation-launches-as-nonprofit'}

def soft_shadow(shape):
    # the site's only shadow: 0 2px 12px rgba(79,52,51,.10)
    spPr = shape._element.spPr
    for e in spPr.findall(qn('a:effectLst')): spPr.remove(e)
    from lxml import etree
    eff = etree.SubElement(spPr, qn('a:effectLst'))
    sh = etree.SubElement(eff, qn('a:outerShdw'), blurRad=str(12 * PX), dist=str(2 * PX), dir='5400000', algn='t', rotWithShape='0')
    c = etree.SubElement(sh, qn('a:srgbClr'), val='4F3433'); etree.SubElement(c, qn('a:alpha'), val='10000')

def rrect(slide, x, y, w, h, colour, name, radius):
    sh = slide.shapes.add_shape(5, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
    rgb(sh, colour); sh.name = name
    sh.adjustments[0] = radius / min(w, h)
    return sh

def brand_slide(slide, post, key, W, H):
    b = BRAND_SIZES[key]
    rect(slide, 0, 0, W, H, BR['paper'], 'Page')
    px_, py_, pw, ph = b['photo']
    src = ImageOps.exif_transpose(Image.open(photo_for(post))).convert('RGB')
    k = max(1, min(2, min(src.width / pw, src.height / ph)))
    img = cover(src, int(pw * k), int(ph * k), post['focus'])
    path = os.path.join(TMP, f'{key}--{post["slug"]}--brand.jpg'); img.save(path, quality=93, subsampling=0)
    slide.shapes.add_picture(path, Emu(int(px_ * PX)), Emu(int(py_ * PX)), Emu(int(pw * PX)), Emu(int(ph * PX))).name = 'Photo'
    cx, cy, cw, ch = b['card']
    card = rrect(slide, cx, cy, cw, ch, BR['cream'], 'Panel', 12); soft_shadow(card)
    pad = b['pad']; tw = cw - 2 * pad
    accent = BR['legacy'] if post['slug'] in ELAINE else BR['green']
    eye_px = b['eye']; btn_h = b['btn'] * 2.3; logo = b['logo']
    head_max = b['head']
    while True:
        hs, hl = fit(post['head'], F_CAT, head_max, tw, 3, 16)
        ds, dl = (fit(post['deck'], 'EBGaramond-Italic.ttf', min(b['deck'], hs * .62), tw * .92, 2, 12) if post['deck'] else (0, []))
        head_lh, deck_lh = hs * 1.12, ds * 1.3
        total = eye_px * 1.3 + eye_px * .9 + head_lh * len(hl) + (pad * .25 + deck_lh * len(dl) if dl else 0) + pad * .5 + max(btn_h, logo * .0)
        if total <= ch - 2 * pad or head_max <= 16: break
        head_max -= 1
    y = cy + pad + (ch - 2 * pad - total) * .35
    text(slide, cx + pad, y, tw, eye_px * 1.4, post['cat'].upper(), 'Montserrat', eye_px, accent, 'Eyebrow', bold=True, spacing=eye_px * .75 * 18, line=eye_px * 1.3)
    y += eye_px * 1.3 + eye_px * .9
    text(slide, cx + pad, y, tw, head_lh * len(hl) + 4, '\v'.join(hl), 'Montserrat', hs, BR['soil'], 'Headline', bold=True, spacing=-hs * .75 * 1, line=head_lh)
    y += head_lh * len(hl)
    if dl:
        y += pad * .25
        tb = text(slide, cx + pad, y, tw * .92, deck_lh * len(dl) + 4, '\v'.join(dl), 'EB Garamond', ds, BR['ink_soft'], 'Lede', line=deck_lh)
        for r in tb.text_frame.paragraphs[0].runs: r.font.italic = True
        y += deck_lh * len(dl)
    # the button and the roundel share the bottom line of the panel
    by = cy + ch - pad - btn_h
    bw = font(F_CAT, b['btn']).getlength('Read the post  →') + b['btn'] * 2.4
    btn = rrect(slide, cx + pad, by, bw, btn_h, accent, 'Button', 8)
    text(slide, cx + pad, by, bw, btn_h, 'Read the post  →', 'Montserrat', b['btn'], '#FFFFFF', 'Button label', bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(slide, cx + pad + bw + b['btn'] * 1.1, by, tw - bw - logo - b['btn'] * 1.5, btn_h, 'soilfoodweb.com', 'Source Sans 3', b['btn'] * .9, BR['ink_faint'], 'Web address', anchor=MSO_ANCHOR.MIDDLE)
    slide.shapes.add_picture(os.path.join(REPO, 'img', 'sfwlogo-240.png'), Emu(int((cx + cw - pad - logo) * PX)), Emu(int((by + btn_h - logo) * PX)), Emu(int(logo * PX)), Emu(int(logo * PX))).name = 'Logo'

def cursor(slide, x, y, size):
    s = size / 24
    pts = [(0, 0), (0, 17), (4, 13), (7, 20), (10, 19), (7, 12), (12.5, 12)]
    sh = poly(slide, [(x + a * s, y + b * s) for a, b in pts], '#FFFFFF', 'Cursor')
    sh.line.color.rgb = RGBColor(*hexrgb(INK)); sh.line.width = Emu(int(1.6 * s * PX))

def build(key, cfg, previews):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(cfg['W'] * PX), Emu(cfg['H'] * PX)
    blank = prs.slide_layouts[6]
    for post in [p for p in POSTS if not ONLY or p['slug'] in ONLY]:
        W, H = cfg['W'], cfg['H']
        slide = prs.slides.add_slide(blank)
        if STYLE == 'brand':
            brand_slide(slide, post, key, W, H)
            slide.notes_slide.notes_text_frame.text = f"{post['slug']} ({post['date']})"
            continue
        if STYLE == 'rect': field_shapes(slide, W, H, post['field'], key)
        else: field_planes(slide, W, H, post['field'], post['slug'])
        zone = cfg['zone']
        cx, cy, cw, ch = cfg['card']
        if post.get('portrait') and ch > H * .7:
            left = max(zone[0], cx + cw - 30)
            zone = (left, zone[1], zone[0] + zone[2] - left, zone[3])
        # the clean version: the photograph whole, one layer, no cuts
        planes = ([dict(pts=[(0, 0), (1, 0), (1, 1), (0, 1)], s=1.0, d=(0, 0), tone=None, seam=False)] if cfg.get('clean')
                  else PLANES_PORTRAIT if post.get('portrait') else PLANES)
        if STYLE != 'rect':
            zx, zy, zw, zh = cfg.get('shape_zone', zone)
            m = min(W, H) * .06
            bx, by, bw, bh = zx + m, zy + m, zw - 2 * m, zh - 1.6 * m
            if STYLE == 'lens':
                dmt = min(bw, bh); bx, by, bw, bh = bx + (bw - dmt) / 2, by, dmt, dmt
            if STYLE == 'window':
                bw = min(bw, bh * .82); bx = zx + zw - m - bw
            shaped_photo(slide, post, key, (bx, by, bw, bh), STYLE, post['field'])
            planes = []
        for i, p in enumerate(planes):
            path, x, y, w, h = plane_png(post, key, zone, p, i, post['field'])
            pic = slide.shapes.add_picture(path, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
            pic.name = f'Photo plane {i+1}'
        cx, cy, cw, ch = cfg['shape_card'] if STYLE != 'rect' and 'shape_card' in cfg else cfg['card']
        card = rect(slide, cx, cy, cw, ch, CREAM, 'Card')
        pad = cfg['pad']; tw = cw - 2 * pad
        # the biggest headline that fits: step down until the whole stack sits in the card
        head_max = cfg['head']
        cs, _ = fit(post['cat'], F_CAT, cfg['cat'] * (.8 if STYLE != 'rect' else 1), tw, 1, 20)
        cat_lh = cs * 1.0
        btn_h = cfg['btn'] * 1.8
        url_px = max(13, cfg['btn'] * .6)
        while True:
            hs, hl = fit(post['head'], F_HEAD, head_max, tw, 5, 18)
            ds, dl = (fit(post['deck'], F_HEAD, min(cfg['deck'], hs * .45), tw * .95, 3, 13) if post['deck'] else (0, []))
            head_lh, deck_lh = hs * 1.02, ds * 1.28
            gap = pad * .32
            total = (cat_lh + gap * .5 + head_lh * len(hl) + (gap * .7 + deck_lh * len(dl) if dl else 0)
                     + gap * 1.6 + btn_h + url_px * 1.9)
            if total <= ch - 2 * pad or head_max <= 18: break
            head_max -= 1
        y = cy + pad + (ch - 2 * pad - total) * .45
        colour = LEGACY if post['field'] == 'legacy' else INK
        text(slide, cx + pad, y, tw, cat_lh * 1.1, post['cat'], 'Montserrat', cs, colour, 'Category', bold=True, spacing=-cs * .75 * 3, line=cat_lh)
        y += cat_lh + gap * .5
        text(slide, cx + pad, y, tw, head_lh * len(hl) + 4, '\v'.join(hl), 'Source Sans 3', hs, INK, 'Headline', spacing=-hs * .75 * 4, line=head_lh)
        y += head_lh * len(hl)
        if dl:
            y += gap * .7
            text(slide, cx + pad + 2, y, tw * .95, deck_lh * len(dl) + 4, '\v'.join(dl), 'Source Sans 3', ds, INK, 'Deck', line=deck_lh)
            y += deck_lh * len(dl)
        y += gap * 1.6
        bw = font(F_BTN, cfg['btn']).getlength('READ POST') + cfg['btn'] * 1.9
        rect(slide, cx + pad, y, bw, btn_h, INK, 'Button')
        text(slide, cx + pad, y, bw, btn_h, 'READ POST', 'EB Garamond', cfg['btn'], '#FFFFFF', 'Button label', align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=cfg['btn'] * .75 * 2)
        cursor(slide, cx + pad + bw - cfg['btn'] * .45, y + btn_h * .55, cfg['btn'] * 1.25)
        y += btn_h + url_px * .5
        text(slide, cx + pad, y, tw, url_px * 1.4, 'www.soilfoodweb.com', 'Source Sans 3', url_px, INK, 'Web address', line=url_px * 1.3)
        notes = slide.notes_slide.notes_text_frame
        notes.text = (f"{post['slug']} ({post['date']})\nPhotograph: {post['img']} is a stand-in from the website "
                      f"repository, not the post's own photograph.")
    path = os.path.join(OUT, f'SFW-blog-cards--{key}' + ('' if STYLE == 'rect' else '--' + STYLE) + '.pptx')
    prs.save(path)
    return path

if __name__ == '__main__':
    only = sys.argv[2:] or list(SIZES)
    for k in only:
        print(build(k, SIZES[k], None))
