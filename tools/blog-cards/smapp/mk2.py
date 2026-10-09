import os
from PIL import Image, ImageOps
from pptx import Presentation
from pptx.util import Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from mk import macbook, place, WES, R
import mk
NEM = {'nem1': (R + 'tools/blog-cards/photos/microbes/bacterial-feeding-nematode-40x-talbot-armstrong.jpg', (.42, .28)),
       'nem2': (R + 'tools/blog-cards/photos/microbes/bacterial-feeding-nematode-40x.jpg', (.70, .25))}
SCOPE = Image.open('cut/microscope-white.png')
LOGO = 'cut/sfw-school-logo-white.png'   # white Soil Food Web School logo, from soilmapp.com
BLUE = RGBColor(0x29, 0x80, 0xB9)        # the sMApp header blue

def add_png(sl, img, x, y, w, PX, name, anchor, before):
    h = w * img.height / img.width
    p = f'/tmp/mk2_{name}_{w}.png'; img.save(p)
    pic = sl.shapes.add_picture(p, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX))); pic.name = name
    (anchor._element.addprevious if before else anchor._element.addnext)(pic._element)
    return h

def build(src, out, key, o):
    p = Presentation(src); sl = p.slides[0]
    SW = {'desktop': 1920, 'square': 1400, 'tablet': 1024, 'mobile': 750, 'thumb': 1200}[key]; PX = p.slide_width / SW
    sh = {s.name: s for s in sl.shapes}; ph = sh['Photo']; paper = sh['Paper']
    W_, H_ = round(ph.width / PX), round(ph.height / PX); k = 2; Wk, Hk = W_ * k, H_ * k
    f, subj = NEM[o['bg']]; micro = Image.open(f).convert('RGB')
    img = Image.new('RGB', (Wk, Hk))
    bw = int(min(Wk * .5, Hk * WES.width / WES.height))
    img.paste(place(micro, Wk - bw, Hk, subj, o['tgt'][key], o.get('zoom', 1.2)), (0, 0))
    img.paste(ImageOps.fit(WES, (bw, Hk), Image.LANCZOS, centering=(.45, .45)), (Wk - bw, 0))
    t = f'/tmp/mk2_{key}_{o["name"]}.jpg'; img.save(t, quality=93)
    pic = sl.shapes.add_picture(t, ph.left, ph.top, ph.width, ph.height); pic.name = 'Photo'
    ph._element.addprevious(pic._element); ph._element.getparent().remove(ph._element)
    # the sMApp header: a blue bar across the microscope picture, menu icon and white logo at the left
    leftw = (Wk - bw) / k; barh = round(H_ * o['bar'][key])
    last = pic
    def put(shape):
        nonlocal last
        last._element.addnext(shape._element); last = shape
    bar = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Emu(int(leftw * PX)), Emu(int(barh * PX)))
    bar.fill.solid(); bar.fill.fore_color.rgb = BLUE; bar.line.fill.background(); bar.shadow.inherit = False; bar.name = 'sMApp bar'; put(bar)
    u = barh / 10; mx0 = barh * .42
    for i in range(3):
        ln = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(int(mx0 * PX)), Emu(int((barh / 2 - 2.6 * u + i * 2.2 * u) * PX)), Emu(int(3.6 * u * PX)), Emu(int(.75 * u * PX)))
        ln.fill.solid(); ln.fill.fore_color.rgb = RGBColor(255, 255, 255); ln.line.fill.background(); ln.shadow.inherit = False; ln.name = 'Menu icon'; put(ln)
    lh_ = barh * .84; lgx = mx0 + 3.6 * u + barh * .45
    lg = sl.shapes.add_picture(LOGO, Emu(int(lgx * PX)), Emu(int((barh - lh_) / 2 * PX)), Emu(int(lh_ * PX)), Emu(int(lh_ * PX))); lg.name = 'Logo'; put(lg)
    px, py, pw = paper.left / PX, paper.top / PX, paper.width / PX
    top = py + 24                                   # visible top edge of the paper
    room = top - barh - 18
    s = o['scale'][key]
    # MacBook resting on the paper
    lift = s.get('lift', 30)                         # the MacBook floats a little above the paper
    lw = int(SW * s['lap']); lap = macbook(lw * 2)
    if lap.height / 2 > room - lift: lw = int(lw * (room - lift) / (lap.height / 2)); lap = macbook(lw * 2)
    lx = px + s['lapx'] * pw
    add_png(sl, lap, lx, top - lift - lap.height / 2, lw, PX, 'MacBook', paper, False)
    # microscope sticker: its cut-off base tucks behind the paper
    mw = int(SW * s['scope']); mh = mw * SCOPE.height / SCOPE.width
    tuck = 6                                         # the whole microscope stands on the paper
    if mh - tuck > room: f_ = room / (mh - tuck); mw = int(mw * f_); mh *= f_; tuck *= f_
    mx = lx + lw + SW * .015 if s.get('after') else px + s['scopex'] * pw
    add_png(sl, SCOPE, mx, top + tuck - mh, mw, PX, 'Microscope', paper, True)
    p.save(out)

OPTS = [
 dict(name='final-layout', bg='nem1', zoom=1.1,
      bar={'desktop': .085, 'square': .075, 'tablet': .085, 'mobile': .085, 'thumb': .085},
      tgt={'desktop': (.88, .28), 'square': (.80, .28), 'tablet': (.80, .28), 'mobile': (.80, .25), 'thumb': (.82, .28)},
      scale={'desktop': dict(lap=.24, lapx=.03, scope=.15, scopex=0, lift=10, after=1),
             'square': dict(lap=.32, lapx=.03, scope=.16, scopex=0, lift=32, after=1),
             'tablet': dict(lap=.32, lapx=.03, scope=.15, scopex=0, lift=20, after=1),
             'mobile': dict(lap=.38, lapx=.02, scope=.17, scopex=0, lift=16, after=1),
             'thumb':  dict(lap=.31, lapx=.03, scope=.14, scopex=0, lift=10, after=1)}),
]
if __name__ == '__main__':
    os.makedirs('mk2', exist_ok=True)
    for o in OPTS:
        for key, f in [('desktop', 'sm/SFW-blog-cards--desktop-header-1920x720--brand.pptx'), ('square', 'sm/SFW-blog-cards--feature-social-1400x1400--brand.pptx')]:
            build(f, f'mk2/sMApp-option-{o["name"]}--{key}.pptx', key, o)
    print('ok')
