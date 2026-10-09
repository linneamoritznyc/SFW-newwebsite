"""sMApp launch header, web-app version: the app on a laptop beside the
microscope (Brevity Media photo R5A_4268 from the Foundation's Drive).
Three layouts, each in all five sizes. The laptop screen is redrawn from
Linnea's screenshots of soilmapp.com in its desktop layout, as its own picture
so it can be replaced with a real screenshot in Canva."""
import os, sys
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = [sys.argv[0], OUT]
import build as B
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from pptx import Presentation
from pptx.util import Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
PX = B.PX
TMP = os.path.join(OUT, '_laptop'); os.makedirs(TMP, exist_ok=True)
F = os.path.expanduser('~/.fonts')
def f(n, s): return ImageFont.truetype(os.path.join(F, n), s)
SANS, BOLD = 'SourceSans3-Regular.ttf', 'Montserrat-Bold.ttf'
BLUE, DG, GOLD = (46, 123, 183), (34, 72, 58), (205, 154, 46)
REPO = B.REPO
SCOPE = os.path.join(REPO, 'tools', 'blog-cards', 'photos', 'drive', 'R5A_4268.jpg')
LOGO = Image.open(os.path.join(REPO, 'img', 'sfwlogo-240.png')).convert('RGBA')
WLOGO = Image.new('RGBA', LOGO.size, (255, 255, 255, 0)); WLOGO.putalpha(LOGO.split()[3])

def screen(w=1600, h=1000):
    im = Image.new('RGB', (w, h), (248, 248, 248)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w, 96), fill=BLUE)
    for y in (34, 46, 58): d.rectangle((30, y, 70, y + 5), fill='white')
    lg = WLOGO.resize((84, 84)); im.paste(lg, (100, 6), lg)
    d.text((200, 30), 'sMApp', font=f(BOLD, 34), fill='white')
    d.ellipse((w - 80, 22, w - 28, 74), fill='white')
    d.rectangle((0, 96, 96, h), fill='white'); d.line((96, 96, 96, h), fill=(225, 225, 225), width=2)
    for i in range(8): d.rounded_rectangle((30, 140 + i * 80, 66, 176 + i * 80), 6, fill=(120, 120, 120) if i else BLUE)
    d.rounded_rectangle((140, 130, w - 50, 470), 30, fill=DG)
    d.ellipse((w - 520, 40, w - 60, 500), fill=(52, 96, 78))
    d.rounded_rectangle((180, 170, 440, 220), 25, fill=(70, 110, 92))
    d.text((200, 178), 'Consultant portfolio', font=f(SANS, 28), fill='white')
    d.text((180, 245), 'Your client portfolio', font=f(BOLD, 62), fill='white')
    d.text((180, 330), 'See where every client stands, what changed recently, and where your', font=f(SANS, 30), fill=(225, 235, 230))
    d.text((180, 368), 'attention will have the most value.', font=f(SANS, 30), fill=(225, 235, 230))
    d.rounded_rectangle((w - 400, 360, w - 110, 430), 10, fill=GOLD)
    d.text((w - 360, 377), '+  ADD CLIENT', font=f(BOLD, 30), fill=(40, 30, 10))
    cw = (w - 190 - 3 * 30) / 4
    for i, (n, lab) in enumerate([('3', 'Clients'), ('5', 'Projects'), ('3', 'Locations'), ('36', 'Assessments')]):
        x = 140 + i * (cw + 30)
        d.rounded_rectangle((x, 510, x + cw, 700), 24, outline=(225, 225, 225), width=3, fill='white')
        d.ellipse((x + 30, 560, x + 120, 650), fill=(230, 238, 234))
        d.rounded_rectangle((x + 55, 585, x + 95, 625), 6, fill=DG)
        d.text((x + 150, 550), n, font=f(BOLD, 64), fill=(25, 25, 25))
        d.text((x + 150, 632), lab, font=f(SANS, 34), fill=(90, 90, 90))
    d.rounded_rectangle((140, 740, w - 50, h - 40), 20, outline=(225, 225, 225), width=3, fill='white')
    d.text((175, 765), 'Recent assessments', font=f(BOLD, 30), fill=(30, 30, 30))
    for i, t in enumerate(['Pasture 1', 'Mentor tea', 'compost f...']):
        y = 820 + i * 46; d.line((175, y - 6, w - 85, y - 6), fill=(235, 235, 235), width=2)
        d.text((175, y), t, font=f(SANS, 28), fill=(50, 50, 50))
    return im

def laptop(name):
    scr = screen()
    sw, sh = scr.size; bz = 36
    W, Hh = sw + 2 * bz, sh + 2 * bz + 12
    base_h = 70; over = 140
    pad = 90
    out = Image.new('RGBA', (W + 2 * over + 2 * pad, Hh + base_h + 2 * pad), (0, 0, 0, 0))
    sm = Image.new('L', out.size, 0); ImageDraw.Draw(sm).rounded_rectangle((pad + over - 40, pad + 60, pad + over + W + 40, pad + Hh + base_h + 40), 60, fill=150)
    sh_ = Image.new('RGBA', out.size, (10, 20, 12, 0)); sh_.putalpha(sm.filter(ImageFilter.GaussianBlur(45)))
    out = Image.alpha_composite(out, sh_)
    d = ImageDraw.Draw(out)
    x0, y0 = pad + over, pad
    d.rounded_rectangle((x0, y0, x0 + W, y0 + Hh), 34, fill=(24, 24, 26))
    out.paste(scr, (x0 + bz, y0 + bz + 6))
    d.ellipse((x0 + W // 2 - 6, y0 + 14, x0 + W // 2 + 6, y0 + 26), fill=(60, 60, 64))
    by = y0 + Hh
    d.polygon([(x0 - over, by + base_h - 18), (x0 + W + over, by + base_h - 18), (x0 + W + over - 20, by + base_h), (x0 - over + 20, by + base_h)], fill=(150, 152, 158))
    d.rectangle((x0 - over, by, x0 + W + over, by + base_h - 18), fill=(205, 207, 212))
    d.rounded_rectangle((x0 + W // 2 - 160, by, x0 + W // 2 + 160, by + 22), 10, fill=(175, 177, 182))
    p = os.path.join(TMP, f'laptop-{name}.png'); out.save(p)
    return p, out.size

LAP, LAPSIZE = laptop('a')

def scope_photo(w, h, focus=(.62, .5)):
    im = ImageOps.exif_transpose(Image.open(SCOPE)).convert('RGB')
    return ImageOps.fit(im, (w, h), Image.LANCZOS, centering=focus)

POST = dict(cat='Microscopy', head='A Fresh sMApp',
            deck='After lots of suggestions and lots of effort, our renovated SFW Microscopy App feels brand new again')

def green(s, x, y, w, h):
    sh = s.shapes.add_shape(1, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX))); sh.name = 'Green'
    sh.line.fill.background(); fl = sh.fill; fl.gradient(); fl.gradient_angle = 68
    st = fl.gradient_stops; st[0].color.rgb = RGBColor(0x15, 0x68, 0x26); st[0].position = 0; st[1].color.rgb = RGBColor(0x22, 0x37, 0x1F); st[1].position = 1

def pic(s, path, name, x, y, w, h):
    s.shapes.add_picture(path, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX))).name = name

def card(s, key, W, H, cx, cw, BIG):
    SMALL = round(BIG * .6); pad = BIG * .8; tw = cw - 2 * pad
    hl = B.wrap(POST['head'], B.font(B.F_HEAD, BIG), tw * .95)
    dl = B.wrap(POST['deck'], B.font(B.F_HEAD, SMALL), tw * .9)
    btn_h = SMALL * 2.0
    ch = int(pad + BIG * 1.08 + BIG * len(hl) + SMALL * .6 + SMALL * 1.25 * len(dl) + SMALL * 1.3 + btn_h + SMALL * 1.3 + pad * .8)
    cy = H - ch - cx
    png = B.torn_paper(key, 'smapp-laptop', cw, ch); m = B.PAPER_MARGIN
    pic(s, png, 'Paper', cx - m, cy - m, cw + 2 * m, ch + 2 * m)
    y = cy + pad
    B.text(s, cx + pad, y, tw, BIG * 1.1, POST['cat'], 'Montserrat', BIG, B.INK, 'Category', bold=True, spacing=-BIG * .75 * 3, line=BIG); y += BIG * 1.08
    B.text(s, cx + pad, y, tw, BIG * len(hl) + 4, '\v'.join(hl), 'Source Sans 3', BIG, B.INK, 'Headline', spacing=-BIG * .75 * 4, line=BIG); y += BIG * len(hl) + SMALL * .6
    B.text(s, cx + pad + 2, y, tw * .9, SMALL * 1.25 * len(dl) + 4, '\v'.join(dl), 'Source Sans 3', SMALL, B.INK, 'Deck', line=SMALL * 1.25); y += SMALL * 1.25 * len(dl)
    by = y + SMALL * 1.3
    bw = B.font(B.F_BTN, SMALL * 1.1).getlength('READ POST') + SMALL * 2.2
    B.rect(s, cx + pad, by, bw, btn_h, B.INK, 'Button')
    B.text(s, cx + pad, by, bw, btn_h, 'READ POST', 'EB Garamond', SMALL * 1.1, '#FFFFFF', 'Button label', align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=SMALL * .75 * 2)
    B.cursor(s, cx + pad + bw - SMALL * .5, by + btn_h * .55, SMALL * 1.5)
    B.text(s, cx + pad, by + btn_h + SMALL * .3, tw, SMALL, 'soilmapp.com  ·  www.soilfoodweb.com', 'Source Sans 3', SMALL * .85, B.INK, 'Web address', line=SMALL)
    return cy

def place_laptop(s, x, y, w):
    lw, lh = LAPSIZE; h = w * lh / lw
    pic(s, LAP, 'Laptop with sMApp', x, y, w, h)

SIZES = {'desktop-header-1920x720': (1920, 720, 40), 'tablet-header-1024x768': (1024, 768, 40), 'thumbnail-1200x800': (1200, 800, 42),
         'feature-social-1400x1400': (1400, 1400, 60), 'mobile-header-750x1000': (750, 1000, 42)}

def v_desk(s, key, W, H, BIG):
    """A: the photo full bleed, the laptop on the desk to the right of the microscope."""
    wide = W / H > 1.4
    p = os.path.join(TMP, f'scope-{key}.jpg'); scope_photo(W, H, (.4, .55) if not wide else (.5, .55)).save(p, quality=92); pic(s, p, 'Photo', 0, 0, W, H)
    if wide:
        lw = W * .36 if W > 1500 else W * .46
        place_laptop(s, W - lw * 1.02, H * .08, lw)
        card(s, key, W, H, 40, W * .34 if W > 1500 else W * .44, BIG)
    else:
        lw = W * .58
        place_laptop(s, W - lw * .98, H * .05, lw)
        card(s, key, W, H, 30, W - 60, BIG)

def v_split(s, key, W, H, BIG):
    """B: green field with the card, the microscope photo on the other side, the laptop across the seam."""
    green(s, 0, 0, W, H)
    if W / H > 1.4:
        px = W * .48
        p = os.path.join(TMP, f'scopeR-{key}.jpg'); scope_photo(int(W - px), H, (.6, .5)).save(p, quality=92); pic(s, p, 'Photo', px, 0, W - px, H)
        place_laptop(s, W * .30, H * .06, W * .38)
        card(s, key, W, H, 40, W * .36 if W > 1500 else W * .46, BIG)
    else:
        ph = H * .58
        p = os.path.join(TMP, f'scopeT-{key}.jpg'); scope_photo(W, int(ph), (.35, .5)).save(p, quality=92); pic(s, p, 'Photo', 0, 0, W, ph)
        lw = W * .5
        place_laptop(s, W - lw * .98, ph * .3, lw)
        card(s, key, W, H, 30, W - 60, BIG)

def v_window(s, key, W, H, BIG):
    """C: the microscope photo full bleed, the app as a browser window floating over it."""
    p = os.path.join(TMP, f'scopeW-{key}.jpg'); scope_photo(W, H, (.45, .5)).save(p, quality=92); pic(s, p, 'Photo', 0, 0, W, H)
    scr = screen(); bar = 54
    win = Image.new('RGBA', (scr.width + 120, scr.height + bar + 120), (0, 0, 0, 0))
    m = Image.new('L', win.size, 0); ImageDraw.Draw(m).rounded_rectangle((60, 80, scr.width + 60, scr.height + bar + 80), 22, fill=140)
    sh_ = Image.new('RGBA', win.size, (0, 0, 0, 0)); sh_.putalpha(m.filter(ImageFilter.GaussianBlur(30))); win = Image.alpha_composite(win, sh_)
    d = ImageDraw.Draw(win); d.rounded_rectangle((60, 60, scr.width + 60, scr.height + bar + 60), 22, fill=(236, 236, 238))
    for i, c in enumerate([(237, 94, 87), (245, 190, 79), (98, 197, 84)]): d.ellipse((90 + i * 34, 80, 112 + i * 34, 102), fill=c)
    d.rounded_rectangle((260, 74, 760, 108), 16, fill='white'); d.text((290, 78), 'soilmapp.com', font=f(SANS, 24), fill=(90, 90, 90))
    win.paste(scr, (60, 60 + bar))
    wp = os.path.join(TMP, 'window.png'); win.save(wp)
    if W / H > 1.4:
        ww = W * .44 if W > 1500 else W * .6
        ww = W * .36 if W > 1500 else W * .46
        pic(s, wp, 'Browser with sMApp', W - ww * 1.02, H * .06, ww, ww * win.height / win.width)
        card(s, key, W, H, 40, W * .36 if W > 1500 else W * .46, BIG)
    else:
        ww = W * .56
        pic(s, wp, 'Browser with sMApp', W - ww * 1.0, H * .03, ww, ww * win.height / win.width)
        card(s, key, W, H, 30, W - 60, BIG)

if __name__ == '__main__':
    for vname, fn in (('laptop-on-desk', v_desk), ('green-split', v_split), ('browser-window', v_window)):
        for key, (W, H, BIG) in SIZES.items():
            prs = Presentation(); prs.slide_width, prs.slide_height = Emu(W * PX), Emu(H * PX)
            s = prs.slides.add_slide(prs.slide_layouts[6]); fn(s, key, W, H, BIG)
            prs.save(os.path.join(OUT, f'sMApp-{vname}--{key}.pptx'))
    print('ok')
