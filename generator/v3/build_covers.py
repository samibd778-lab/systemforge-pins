"""Notion page covers (3000x1200) in the v3 home-cover style:
same product scene as the home cover + the page's own real HD screenshot on the screen + page title.
Usage: python3 generator/v3/build_covers.py [cover_id ...]   (ids from COVERS below)
Writes covers/v3/sub/<id>.jpg
"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pins as B
from build_listing import screens_of

HERE, ROOT = B.HERE, B.ROOT
OUT = os.path.join(ROOT, 'covers', 'v3', 'sub')
os.makedirs(OUT, exist_ok=True)
CW, CH = 3000, 1200          # final size
FONTS = os.path.join(ROOT, 'generator', 'remotion', 'public')

# product -> scene, panel tone (dark scenes get light text)
PROD = {
    'fco':  dict(scene='w-fco.png',  dark=True,  kicker='FREELANCER CLIENT OS'),
    'fit':  dict(scene='w-fit.png',  dark=False, kicker='FREELANCE INVOICE TRACKER'),
    'wcp':  dict(scene='w-wcp.png',  dark=False, kicker='WEEKLY CONTENT PLANNER'),
    'ccs':  dict(scene='s-land.png', dark=False, kicker='CONTENT CREATOR STUDIO'),
    'prop': dict(scene='w-prop.png', dark=True,  kicker='PROPOSAL TRACKER'),
    'deal': dict(scene='w-deal.png', dark=False, kicker='BRAND DEAL TRACKER'),
}

# cover id -> (product, title, subtitle, screens [one per blank screen in the scene, left to right])
B.CROPS.update({
    'cv-fco-paid': ('fco-money-flow', (548, 250, 935, 950)),
    'cv-ccs-cal':  ('ccs-calendar', (145, 330, 1855, 1250)),
})

COVERS = {
    'fco-invoices': ('fco', 'Invoices', 'Draft, sent, paid. Late ones count the days.', ['cv-fco-paid']),
    'ccs-content':  ('ccs', 'Content', 'Every post from idea to posted, on one calendar.', ['cv-ccs-cal', 'ph-ccs-pipeline-posted.jpg']),
    'deal-rate':    ('deal', 'Rate Card', 'Write your prices once. Paste them into every pitch.', ['deal-rate']),
}


def screen_masks(scene_file, n):
    """exact white screen areas of the scene (fingers / bezels that overlap stay outside), left to right"""
    from scipy import ndimage
    im = np.array(Image.open(os.path.join(HERE, scene_file)).convert('RGB')).astype(int)
    white = (im.min(axis=2) > 232) & ((im.max(axis=2) - im.min(axis=2)) < 16)
    lab, _ = ndimage.label(white)
    sizes = ndimage.sum(white, lab, range(1, lab.max() + 1))
    ms = [ndimage.binary_fill_holes(lab == i + 1) for i in np.argsort(sizes)[::-1][:n]]
    return sorted(ms, key=lambda m: np.nonzero(m)[1].min())


def make_real(img, bg_tone):
    """make a crisp screenshot sit in the photo: match softness, light and colour, add glass glare"""
    from PIL import ImageFilter, ImageEnhance
    w, h = img.size
    img = img.convert('RGB').filter(ImageFilter.GaussianBlur(0.9))
    img = ImageEnhance.Contrast(img).enhance(0.9)
    img = ImageEnhance.Brightness(img).enhance(0.95)
    tint = Image.new('RGB', img.size, bg_tone)
    img = Image.blend(img, tint, 0.07)
    a = np.array(img).astype(float)
    yy, xx = np.mgrid[0:h, 0:w]
    glare = np.clip(1 - ((xx / w) * 0.8 + (yy / h) * 0.6), 0, 1) ** 2 * 26      # soft light from top-left
    vign = (np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy)) / (0.035 * max(w, h)))
    shade = (1 - np.clip(vign, 0, 1)) * 0.12                                     # dark inner edge
    a = a + glare[..., None]
    a = a * (1 - shade[..., None])
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def mobile(c):
    """desktop crop -> Notion mobile screen: scaled to phone width + the real Notion mobile bottom bar"""
    nav = Image.open(os.path.join(HERE, 'ph-fco-invoices-board.jpg')).convert('RGB')
    nav = nav.crop((0, nav.height - 330, nav.width, nav.height))
    W = nav.width; H = int(W * 2.11)
    k = W / c.width
    c = c.resize((W, int(c.height * k)), Image.LANCZOS)
    out = Image.new('RGB', (W, H), (255, 255, 255))
    out.paste(c.crop((0, 0, W, min(c.height, H - nav.height + 40))), (0, 70))
    out.paste(nav, (0, H - nav.height))
    return out


def warp_bg(prod, screens):
    p = PROD[prod]
    sc = Image.open(os.path.join(HERE, p['scene'])).convert('RGB')
    k = CW / sc.width
    W2, H2 = CW, int(sc.height * k)
    bg = sc.resize((W2, H2), Image.LANCZOS).convert('RGBA')
    tone = tuple(int(v) for v in np.array(sc).reshape(-1, 3).mean(axis=0))
    quads = screens_of(p['scene'], len(screens))
    masks = screen_masks(p['scene'], len(screens))
    cy_all = []
    for q, mk, s in zip(quads, masks, screens):
        qq = [(x * k, y * k) for x, y in q]
        cx = sum(a for a, _ in qq) / 4; cy = sum(b for _, b in qq) / 4; cy_all.append(cy)
        qq = [(cx + (x - cx) * 1.07, cy + (y - cy) * 1.05) for x, y in qq]
        c = Image.open(B.src(s)).convert('RGB')
        is_phone = mk.sum() and (np.ptp(np.nonzero(mk)[1]) < np.ptp(np.nonzero(mk)[0]))
        if is_phone and not s.startswith('ph-'):
            c = mobile(c)
        sw = ((qq[1][0] - qq[0][0]) ** 2 + (qq[1][1] - qq[0][1]) ** 2) ** .5
        sh = ((qq[3][0] - qq[0][0]) ** 2 + (qq[3][1] - qq[0][1]) ** 2) ** .5
        ar = sw / sh; cw, ch = c.size
        c = c.crop((0, 0, int(ch * ar), ch)) if cw / ch > ar else c.crop((0, 0, cw, int(cw / ar)))
        c = c.resize((int(sw * 1.2), int(sw * 1.2 / ar)), Image.LANCZOS)
        c = make_real(c, tone)
        cw, ch = c.size
        warped = c.convert('RGBA').transform((W2, H2), Image.PERSPECTIVE,
                                             B._coeffs(qq, [(0, 0), (cw, 0), (cw, ch), (0, ch)]), Image.BICUBIC)
        from PIL import ImageFilter
        m = Image.fromarray((mk * 255).astype(np.uint8)).resize((W2, H2), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2))
        bg.paste(warped, (0, 0), m)
    # vertical band of CH px centred on the screens
    mid = sum(cy_all) / len(cy_all) if cy_all else H2 / 2
    y0 = int(min(max(0, mid - CH / 2), max(0, H2 - CH)))
    bg = bg.crop((0, y0, CW, y0 + CH))
    # soft panel behind the text on the left (same as home covers)
    arr = np.zeros((CH, CW, 4), np.uint8)
    arr[..., :3] = (40, 28, 20) if p['dark'] else (246, 241, 233)
    for x in range(CW):
        t = x / CW; a = 0.92 if t < 0.30 else max(0.0, 0.92 * (1 - (t - 0.30) / 0.18))
        arr[:, x, 3] = int(255 * a * (0.80 if p['dark'] else 1))
    bg.alpha_composite(Image.fromarray(arr))
    return bg.convert('RGB')


def build(cid):
    prod, title, sub, screens = COVERS[cid]
    p = PROD[prod]
    bgp = os.path.join(OUT, f'_{cid}-bg.jpg'); warp_bg(prod, screens).save(bgp, quality=95)
    ink, mut, kick = ('#FFFDF9', '#F1E7DC', '#E8D6C3') if p['dark'] else ('#2E2A25', '#5C554C', '#7A6A58')
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:F;font-weight:600;src:url(file://{FONTS}/fraunces600.woff2)}}
@font-face{{font-family:I;font-weight:500;src:url(file://{FONTS}/inter500.woff2)}}
@font-face{{font-family:I;font-weight:700;src:url(file://{FONTS}/inter700.woff2)}}
body{{margin:0}} .c{{position:relative;width:1500px;height:600px;background:url(file://{bgp}) center/cover}}
.t{{position:absolute;left:150px;top:50%;transform:translateY(-50%);width:640px}}
.k{{font:700 16px I;letter-spacing:4px;color:{kick};margin:0 0 14px}}
.h{{font:600 78px/1.0 F;color:{ink};margin:0 0 16px}}
.s{{font:500 22px/1.35 I;color:{mut};margin:0}}
</style></head><body><div class="c"><div class="t"><p class="k">{p['kicker']}</p><p class="h">{title}</p><p class="s">{sub}</p></div></div></body></html>"""
    hp = os.path.join(OUT, f'_{cid}.html'); open(hp, 'w').write(html)
    shot = hp + '.png'
    subprocess.run([B.CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=2', '--window-size=1500,800', f'--screenshot={shot}', 'file://' + hp],
                   check=True, capture_output=True)
    Image.open(shot).crop((0, 0, CW, CH)).convert('RGB').save(os.path.join(OUT, f'{cid}.jpg'), quality=90, optimize=True, progressive=True)
    for f in (bgp, hp, shot): os.remove(f)
    print('ok', cid)


if __name__ == '__main__':
    for cid in sys.argv[1:] or list(COVERS):
        build(cid)
