"""SystemForge v3 pins: lifestyle scenes (Canva AI, blank screens) + real HD Notion screenshots.

Writes:
  canva/v3/crops/*.png   screenshot crops (cards / screens)
  canva/v3/bg/*.jpg      2000x3000 backgrounds (scene + real screens, no text)
  canva/v3/pins-batch1.html  one Canva-importable design, one page per pin, editable text
Usage: python3 generator/v3/build_pins.py
"""
import json, os, subprocess, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
HD = os.path.join(ROOT, 'shots', 'hd')
OUT = os.path.join(ROOT, 'canva', 'v3')
RAW = 'https://raw.githubusercontent.com/samibd778-lab/systemforge-pins/main/canva/v3/'
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
os.makedirs(os.path.join(OUT, 'crops'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'bg'), exist_ok=True)

# ---------- 1. crops (coords on a 2000-wide copy of each screenshot) ----------
CROPS = {
    'ccs-coming':   ('ccs-home-full', (82, 565, 612, 708)),
    'ccs-channels': ('ccs-home-full', (80, 350, 770, 478)),
    'ccs-lap':      ('ccs-home-full', (78, 490, 930, 1030)),
    'ccs-top':      ('ccs-top-posts', (163, 405, 1660, 860)),
    'ccs-cal':      ('ccs-calendar', (145, 930, 1855, 1250)),
    'ccs-deals':    ('ccs-calendar-deals', (163, 905, 1945, 1215)),
    'wcp-goals':    ('wcp-goals', (163, 870, 1850, 1150)),
    'wcp-next7':    ('wcp-next7-pipeline', (163, 360, 1840, 515)),
    'wcp-pipe':     ('wcp-next7-pipeline', (163, 745, 1940, 1240)),
    'wcp-cal':      ('wcp-calendar', (145, 965, 1855, 1250)),
    'fco-board':    ('fco-money-flow', (145, 250, 1330, 900)),
    'fco-projects': ('fco-projects-invoices', (145, 280, 1930, 430)),
    'fco-unpaid':   ('fco-projects-invoices', (145, 710, 1930, 860)),
    'fco-review':   ('fco-home-menu', (640, 800, 1855, 1050)),
    'fit-chase':    ('fit-chase-owes', (145, 315, 1930, 410)),
    'fit-owes':     ('fit-chase-owes', (145, 630, 1870, 830)),
    'fit-all':      ('fit-chase-owes', (145, 1050, 1930, 1250)),
    'fit-page':     ('fit-chase-owes', (145, 190, 1930, 1250)),
    'fit-emails':   ('fit-reminder-emails', (450, 840, 1540, 1070)),
    'prop-follow':  ('prop-followup-pipeline', (145, 325, 1930, 575)),
    'prop-pipe':    ('prop-followup-pipeline', (145, 860, 1990, 1250)),
    'prop-table':   ('prop-proposals-table', (145, 295, 1990, 700)),
    'prop-col':     ('prop-pipeline', (548, 285, 925, 990)),
    'deal-now':     ('deal-do-now-board', (145, 300, 1870, 560)),
    'deal-board':   ('deal-do-now-board', (145, 840, 2000, 1160)),
    'deal-owe':     ('deal-posts-owe', (145, 445, 1930, 600)),
    'deal-owe-all': ('deal-posts-owe', (145, 720, 1930, 1130)),
    'deal-rate':    ('deal-rate-card', (511, 430, 1170, 830)),
}
_cache = {}


# readable card crops: (screenshot, row ranges, column ranges) on the 2000-wide scale
COMPOSITE = {
    'prop-price':   ('prop-proposals-table', [(295, 345), (345, 395), (650, 700)], [(145, 420), (1565, 1825)]),
    'c-fco-projects': ('fco-projects-invoices', [(280, 430)], [(145, 530), (810, 1090)]),
    'c-fco-unpaid': ('fco-projects-invoices', [(710, 860)], [(145, 530), (1645, 1920)]),
    'c-fco-paid':   ('fco-money-flow', [(250, 900)], [(545, 930)]),
    'c-fco-review': ('fco-home-menu', [(800, 1050)], [(640, 1300)]),
    'c-fit-chase':  ('fit-chase-owes', [(315, 410)], [(145, 450), (1365, 1645)]),
    'c-fit-owes':   ('fit-chase-owes', [(630, 830)], [(145, 530), (810, 1090)]),
    'c-fit-all':    ('fit-chase-owes', [(1050, 1250)], [(145, 530), (1365, 1645)]),
    'c-fit-emails': ('fit-reminder-emails', [(840, 1070)], [(450, 1000)]),
    'c-prop-follow': ('prop-followup-pipeline', [(325, 525)], [(145, 465), (465, 735), (1010, 1150)]),
    'c-prop-sent':  ('prop-followup-pipeline', [(860, 1250)], [(545, 930)]),
    'c-deal-now':   ('deal-do-now-board', [(300, 510)], [(145, 535), (535, 810)]),
    'c-deal-col':   ('deal-do-now-board', [(840, 1160)], [(145, 530)]),
    'c-deal-owe':   ('deal-posts-owe', [(445, 600)], [(145, 535), (535, 810)]),
    'c-deal-owe-all': ('deal-posts-owe', [(720, 1130)], [(145, 535), (535, 810)]),
    'c-wcp-goals':  ('wcp-goals', [(870, 1150)], [(163, 500), (910, 1150), (1385, 1600)]),
    'c-wcp-goals2': ('wcp-goals', [(870, 1150)], [(163, 500), (1385, 1600)]),
    'c-wcp-next7':  ('wcp-next7-pipeline', [(360, 515)], [(163, 560), (1700, 1840)]),
    'c-wcp-col':    ('wcp-next7-pipeline', [(745, 1240)], [(163, 593)]),
    'c-wcp-cal':    ('wcp-calendar', [(965, 1250)], [(635, 1365)]),
    'c-ccs-cal':    ('ccs-calendar', [(930, 1250)], [(390, 1120)]),
    'c-ccs-top':    ('ccs-top-posts', [(405, 860)], [(163, 600), (600, 755)]),
    'c-ccs-deal':   ('ccs-calendar-deals', [(905, 1215)], [(163, 593)]),
    'c-ccs-ch2':    ('ccs-home-full', [(350, 478)], [(80, 540)]),
}


def crop(name):
    if name in _cache:
        return _cache[name]
    if name in COMPOSITE:
        srcf, rows, cols = COMPOSITE[name]
        im = Image.open(os.path.join(HD, srcf + '.png')).convert('RGB'); k = im.width / 2000
        W = sum(int(b * k) - int(a * k) for a, b in cols); H = sum(int(b * k) - int(a * k) for a, b in rows)
        c = Image.new('RGB', (W, H), 'white'); y = 0
        for r0, r1 in rows:
            x = 0
            for a, b in cols:
                q = im.crop((int(a * k), int(r0 * k), int(b * k), int(r1 * k))); c.paste(q, (x, y)); x += q.width
            y += int(r1 * k) - int(r0 * k)
        pth = os.path.join(OUT, 'crops', name + '.png'); c.save(pth); _cache[name] = pth
        return pth
    src, (x0, y0, x1, y1) = CROPS[name]
    im = Image.open(os.path.join(HD, src + '.png')).convert('RGB')
    k = im.width / 2000
    c = im.crop((int(x0 * k), int(y0 * k), int(x1 * k), int(y1 * k)))
    p = os.path.join(OUT, 'crops', name + '.png')
    c.save(p)
    _cache[name] = p
    return p


def src(name):
    """crop name, or a file in generator/v3"""
    return crop(name) if (name in CROPS or name in COMPOSITE) else os.path.join(HERE, name)


# ---------- 2. backgrounds ----------
SCENES = {  # background file, screens (left, top, w, h, radius) in 1000x1500 page px
    'desk':   ('scene-zoom.png', [(113, 530, 630, 400, 4), (833, 707, 150, 317, 18)]),
    'studio': ('s-studio-clean-big.png', [(355, 777, 495, 300, 3)]),
    'hand':   ('s-hand-big.png', [(380, 717, 238, 520, 26)]),
}


def render(html, out, w=1000, h=1500):
    with tempfile.NamedTemporaryFile('w', suffix='.html', dir=HERE, delete=False) as f:
        f.write(html)
        p = f.name
    shot = p + '.png'
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                    '--allow-file-access-from-files', '--force-device-scale-factor=2',
                    f'--window-size={w},{h + 200}', f'--screenshot={shot}', 'file://' + p],
                   check=True, capture_output=True)
    Image.open(shot).crop((0, 0, w * 2, h * 2)).convert('RGB').save(out, quality=92)
    os.remove(p); os.remove(shot)


def bg_rect(scene, screens, out, blur=0):
    file, boxes = SCENES[scene]
    parts = []
    for (l, t, w, h, r), s in zip(boxes, screens):
        if s is None:
            continue
        pos = 'top' if s.startswith('ph-') or s == 'prop-col' else 'top left'
        parts.append(f'<div style="position:absolute;left:{l}px;top:{t}px;width:{w}px;height:{h}px;'
                     f'border-radius:{r}px;overflow:hidden;background:#fff"><img src="file://{src(s)}" '
                     f'style="width:100%;height:100%;object-fit:cover;object-position:{pos}"></div>')
    f = f'filter:blur({blur}px)' if blur else ''
    html = (f'<html><body style="margin:0"><div style="position:relative;width:1000px;height:1500px;overflow:hidden">'
            f'<img src="file://{os.path.join(HERE, file)}" style="position:absolute;inset:0;width:1000px;height:1500px;{f}">'
            + ''.join(parts) + '</div></body></html>')
    render(html, out)


def _coeffs(dst, srcpts):
    A, B = [], []
    for (x, y), (u, v) in zip(dst, srcpts):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
        B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


def bg_flat(lap, tab, out):
    C = json.load(open(os.path.join(HERE, 'flat-corners.json')))
    bg = Image.open(os.path.join(HERE, 's-flat.png')).convert('RGBA').resize((2000, 3000), Image.LANCZOS)
    for key, s in (('laptop', lap), ('ipad', tab)):
        S = 2
        q = [(x * 5 * S, y * 5 * S) for x, y in C[key]]
        cx = sum(p[0] for p in q) / 4; cy = sum(p[1] for p in q) / 4
        q = [(cx + (x - cx) * 1.03, cy + (y - cy) * 1.04) for x, y in q]
        c = Image.open(src(s)).convert('RGB')
        sw = ((q[1][0] - q[0][0]) ** 2 + (q[1][1] - q[0][1]) ** 2) ** .5
        sh = ((q[3][0] - q[0][0]) ** 2 + (q[3][1] - q[0][1]) ** 2) ** .5
        ar = sw / sh; w, h = c.size
        c = c.crop((0, 0, int(h * ar), h)) if w / h > ar else c.crop((0, 0, w, int(w / ar)))
        w, h = c.size
        warped = c.convert('RGBA').transform((2000 * S, 3000 * S), Image.PERSPECTIVE,
                                             _coeffs(q, [(0, 0), (w, 0), (w, h), (0, h)]), Image.BICUBIC)
        m = Image.new('L', (2000 * S, 3000 * S), 0); ImageDraw.Draw(m).polygon(q, fill=255)
        layer = Image.new('RGBA', (2000 * S, 3000 * S), (0, 0, 0, 0)); layer.paste(warped, (0, 0), m)
        bg.alpha_composite(layer.resize((2000, 3000), Image.LANCZOS))
    bg.convert('RGB').save(out, quality=92)


def fit(name, w, maxh, tag):
    """scale a screenshot to width w; if taller than maxh, keep the top part. Returns (url, height)."""
    im = Image.open(src(name)).convert('RGB')
    W, H = im.size
    h = H * w / W
    if h > maxh:
        im = im.crop((0, 0, W, int(maxh * W / w))); h = maxh
    p = os.path.join(OUT, 'crops', f'{name}-{tag}.png')
    im.save(p)
    return RAW + 'crops/' + os.path.basename(p), int(round(h))


# ---------- 3. page templates (Canva HTML) ----------
SER = "font-family:'Source Serif 4',Georgia,serif;font-weight:700"
INK, MUT, SAGE, CLAY, PAP = '#2E2A25', '#7A6A58', '#7A8B6F', '#C98B6B', '#FFFDF9'


def P(l, t, w, txt, size, extra=''):
    wd = f'width:{w}px;' if w else ''
    return f'<p style="position:absolute;left:{l}px;top:{t}px;{wd}margin:0;font-size:{size}px;{extra}">{txt}</p>'


def pill(l, t, w, txt, bg, fg=PAP, size=24):
    return P(l, t, w, txt, size, f'padding:12px 0;text-align:center;border-radius:999px;background:{bg};color:{fg};font-weight:700')


def page(label, bgfile, inner, color='#F6F1E9'):
    return (f'<div data-document-role="page" data-label="{label}" style="position:relative;width:1000px;height:1500px;'
            f'overflow:hidden;background:{color}"><img src="{RAW}bg/{bgfile}" style="position:absolute;left:0;top:0;'
            f'width:1000px;height:1500px">{inner}</div>')


def card(l, t, w, title, name, img_h, tag):
    url, img_h = fit(name, w, img_h, tag)
    return (f'<div style="position:absolute;left:{l}px;top:{t}px;width:{w}px;height:{img_h + 66}px;background:#FFFFFF;'
            f'border-radius:22px;overflow:hidden">{P(26, 16, w - 52, title, 28, f"font-weight:700;color:{INK}")}'
            f'<img src="{url}" style="position:absolute;left:0;top:66px;width:{w}px;height:{img_h}px"></div>')


def chips3(chips, top):
    widths = [max(170, 16 * len(c) + 40) for c in chips]
    gap = 18; total = sum(widths) + gap * (len(widths) - 1); x = (1000 - total) // 2; out = ''
    for i, (c, w) in enumerate(zip(chips, widths)):
        out += pill(x, top, w, c, CLAY if i == 1 else SAGE); x += w + gap
    return out


def t_desk(p):
    return (P(0, 50, 1000, 'SYSTEMFORGE', 24, f'text-align:center;font-weight:700;letter-spacing:5px;color:{MUT}')
            + P(0, 90, 1000, p['title'], p.get('size', 100), f'text-align:center;line-height:1.05;color:{INK};{SER}')
            + P(0, 215, 1000, p['sub'], 40, f'text-align:center;color:#4A433B;{SER}')
            + chips3(p['chips'], 300)
            + pill(330, 1370, 340, 'NOTION TEMPLATE', PAP, INK, 24))


def t_zoom(p):
    (t1, c1), (t2, c2) = p['cards']
    return (P(0, 60, 1000, p['kicker'], 24, f'text-align:center;font-weight:700;letter-spacing:5px;color:{MUT}')
            + P(0, 100, 1000, p['title'], 92, f'text-align:center;line-height:1.02;color:{INK};{SER}')
            + card(40, 430, 920, t1, c1, 290, 'z1')
            + P(960 - (15 * len(p['label']) + 44), 392, 15 * len(p['label']) + 44, p['label'], 26, f'padding:12px 0;text-align:center;white-space:nowrap;border-radius:999px;background:{CLAY};color:{PAP};font-weight:700')
            + card(120, 1000, 840, t2, c2, 210, 'z2')
            + pill(250, 1380, 500, p['name'], PAP, INK, 26))


def t_flat(p):
    l1, l2 = p['title']
    return (P(80, 90, 840, p['kicker'], 24, 'font-weight:700;letter-spacing:5px;color:#8A7F72')
            + P(80, 160, 840, l1, 88, 'line-height:1.02;font-weight:700;color:#1F1C19')
            + P(80, 160 + 92 * l1.count('<br>') + 92, 840, l2, 88, f'line-height:1.02;font-weight:700;color:{SAGE}')
            + P(80, 160 + 92 * (l1.count('<br>') + 2) + 30, 840, p['name'] + ' · by SystemForge', 30, 'font-weight:500;color:#5C554C'))


def t_hand(p):
    return (f'<img src="{RAW}shade-top.png" style="position:absolute;left:0;top:0;width:1000px;height:1500px">'
            + P(70, 100, 0, p['kicker'], 24, f'padding:10px 20px;border-radius:8px;background:{CLAY};color:{PAP};font-weight:700;letter-spacing:3px')
            + P(70, 180, 860, p['title'], 100, f'line-height:1.02;color:{PAP};{SER}')
            + P(70, 420, 860, p['sub'], 32, 'line-height:1.35;font-weight:500;color:#F6EDE4'))


def t_studio(p):
    return (P(0, 120, 1000, p['title'], 104, f'text-align:center;line-height:1.02;color:{PAP};{SER}')
            + P(0, 360, 1000, p['sub'], 34, f'text-align:center;font-weight:500;color:{PAP}')
            + P(0, 430, 1000, '&nbsp;&nbsp;&nbsp;'.join('✓ ' + c for c in p['chips']), 27, f'text-align:center;font-weight:700;color:{PAP}')
            + pill(330, 1360, 340, 'NOTION TEMPLATE', PAP, INK, 26))


def t_steps(p):
    out = (P(60, 70, 880, p['title'], 76, f'line-height:1.05;color:#2F4A3A;{SER}')
           + P(60, 70 + 82 * (p['title'].count('<br>') + 1) + 14, 880, p['sub'], 30, 'font-weight:500;color:#4A433B'))
    pos = [(40, 470), (510, 470), (40, 930), (510, 930)]
    for i, ((lab, c), (x, y)) in enumerate(zip(p['steps'], pos)):
        url, ih = fit(c, 410, 300, f's{i}')
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;width:450px;height:420px;background:#FFFFFF;border-radius:20px;overflow:hidden">'
                f'<p style="position:absolute;left:20px;top:18px;width:50px;margin:0;padding:8px 0;text-align:center;border-radius:999px;background:#2F4A3A;color:{PAP};font-size:26px;font-weight:700">{i + 1}</p>'
                + P(84, 26, 350, lab, 28, f'font-weight:700;color:{INK}')
                + f'<img src="{url}" style="position:absolute;left:20px;top:{96 + (300 - ih) // 2}px;width:410px;height:{ih}px"></div>')
    out += P(40, 1390, 0, '⬇ Instant download', 26, f'padding:14px 26px;border-radius:999px;background:{PAP};color:{INK};font-weight:700')
    out += P(560, 1390, 400, p['name'], 26, f'padding:14px 0;text-align:center;border-radius:999px;background:#2F4A3A;color:{PAP};font-weight:700')
    return out


TEMPLATES = {'desk': t_desk, 'zoom': t_zoom, 'flat': t_flat, 'hand': t_hand, 'studio': t_studio, 'steps': t_steps}
NAMES = {'ccs': 'Content Creator Studio', 'wcp': 'Weekly Content Planner', 'fco': 'Freelancer Client OS',
         'fit': 'Freelance Invoice Tracker', 'prop': 'Proposal Tracker', 'deal': 'Brand Deal Tracker'}


def build(spec, out_html):
    pages = []
    for p in spec:
        p.setdefault('name', NAMES[p['p']])
        bgname = p['id'] + '.jpg'; bgpath = os.path.join(OUT, 'bg', bgname)
        st = p['style']
        if st == 'flat':
            bg_flat(p['screens'][0], p['screens'][1], bgpath)
        elif st == 'steps':
            bg_rect(p.get('scene', 'desk'), [], bgpath, blur=6)
        else:
            bg_rect({'desk': 'desk', 'zoom': 'desk', 'hand': 'hand', 'studio': 'studio'}[st], p['screens'], bgpath)
        pages.append(page(p['id'], bgname, TEMPLATES[st](p), '#3A2A20' if st == 'hand' else '#F6F1E9'))
        print('ok', p['id'])
    html = ('<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700'
            '&family=Source+Serif+4:wght@700&display=swap" rel="stylesheet"><style>body{margin:0}div,span,p{font-family:Inter,Arial,sans-serif}'
            '</style></head><body>' + '\n'.join(pages) + '</body></html>')
    open(out_html, 'w').write(html)


if __name__ == '__main__':
    spec = json.load(open(os.path.join(HERE, 'pins-v3-spec.json')))
    build(spec, os.path.join(OUT, 'pins-batch1.html'))
