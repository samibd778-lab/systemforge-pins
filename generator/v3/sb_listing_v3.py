"""Second Brain OS listing images in the v3 lifestyle style (same look as the other SystemForge listings).
Shots: shots/hd/sb-*.png (real 2x captures, 2170 px wide). Coordinates below are on the 2000 scale.
Usage: python3 generator/v3/sb_listing_v3.py [labels...]   (no labels = all pages)"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_listing as L
B = L.B
B.CROPS.update({
    'sb-lap': ('sb-home', (95, 0, 1945, 1100)),
    'c-sb-widget': ('sb-home', (166, 968, 1382, 1456)),
    'c-sb-goals': ('sb-goals', (180, 330, 1330, 850)),
    'c-sb-journal': ('sb-journal', (180, 330, 820, 1000)),
    'sb-scr-widget': ('sb-home', (95, 330, 1945, 1460)),
    'sb-scr-goals': ('sb-goals', (150, 60, 1945, 1220)),
    'sb-scr-projects': ('sb-projects', (150, 330, 1990, 1220)),
})
B.COMPOSITE.update({
    'c-sb-projects': ('sb-projects', [(396, 940)], [(192, 700), (1253, 1751)]),
    'c-sb-habits': ('sb-habits', [(387, 922)], [(185, 1065)]),
})
L.P['sb'] = dict(name='Second Brain OS', kicker='NOTION LIFE PLANNER · PARA METHOD', color='#E3E8DC', accent='#7A8B6F',
    scene='s-sb-r.png', screens=['sb-lap'],
    sub='Goals, projects, notes, habits<br>and journal in one calm place.',
    features=['Goals &amp; projects with progress', 'Habit tracker + daily journal', 'Notes inbox (PARA method)', 'Bonus: Notion for beginners'],
    cards=[('Start every day clear', 'A live Today widget: clock, how much of the week, month and year is left, and a thought for the day.', 'c-sb-widget'),
           ('Goals with real progress', 'Link projects to a goal. Its bar fills up as the projects are done.', 'c-sb-goals'),
           ('Every project on one board', 'Progress bar from ticked tasks, plus days left or late.', 'c-sb-projects'),
           ('Small habits, every day', 'One row per day. Tick what you did. Rename the 5 habits.', 'c-sb-habits')],
    inside=['Home dashboard + Today widget', 'Goals with progress bars', 'Projects board + Tasks', 'Next 7 days + calendar',
            'Notes inbox + Quick capture', 'Areas + Resources (PARA)', 'Habit tracker', 'Daily journal + mood board',
            'Reading list + weekly, monthly, yearly reviews', 'Bonus PDF: Notion for beginners'])
import numpy as np
from PIL import Image, ImageDraw
W, H = L.W, L.H


def life_bg(scene, screen, out, text_side='right', dark=False):
    """scene scaled to page height, real screenshot warped into the blank screen, soft panel on the text side"""
    sc = Image.open(os.path.join(L.HERE, scene)).convert('RGB'); w0, h0 = sc.size
    k = (H * 2) / h0; Wb = int(w0 * k)
    ox = 0 if text_side == 'right' else Wb - W * 2
    base = (40, 30, 22) if dark else (246, 241, 233)
    bg = Image.new('RGBA', (W * 2, H * 2), base + (255,))
    scr = sc.resize((Wb, H * 2), Image.LANCZOS).convert('RGBA')
    bg.paste(scr.crop((max(0, ox), 0, max(0, ox) + W * 2, H * 2)), (max(0, -ox), 0))
    S = 2
    q = L.screens_of(scene, 1)[0]
    qq = [((x * k - ox) * S, y * k * S) for x, y in q]
    cx = sum(a for a, _ in qq) / 4; cy = sum(b for _, b in qq) / 4
    qq = [(cx + (x - cx) * 1.03, cy + (y - cy) * 1.025) for x, y in qq]
    c = Image.open(B.src(screen)).convert('RGB')
    sw = ((qq[1][0] - qq[0][0]) ** 2 + (qq[1][1] - qq[0][1]) ** 2) ** .5
    sh = ((qq[3][0] - qq[0][0]) ** 2 + (qq[3][1] - qq[0][1]) ** 2) ** .5
    ar = sw / sh; cw, ch = c.size
    c = c.crop((0, 0, int(ch * ar), ch)) if cw / ch > ar else c.crop((0, 0, cw, int(cw / ar)))
    cw, ch = c.size
    warped = c.convert('RGBA').transform((W * 2 * S, H * 2 * S), Image.PERSPECTIVE,
                                         B._coeffs(qq, [(0, 0), (cw, 0), (cw, ch), (0, ch)]), Image.BICUBIC)
    m = Image.new('L', (W * 2 * S, H * 2 * S), 0); ImageDraw.Draw(m).polygon(qq, fill=255)
    layer = Image.new('RGBA', (W * 2 * S, H * 2 * S), (0, 0, 0, 0)); layer.paste(warped, (0, 0), m)
    bg.alpha_composite(layer.resize((W * 2, H * 2), Image.LANCZOS))
    arr = np.zeros((H * 2, W * 2, 4), np.uint8); arr[..., :3] = base
    for x in range(W * 2):
        t = x / (W * 2)
        if text_side == 'right':
            a = 0.0 if t < 0.52 else min(0.96, 0.96 * (t - 0.52) / 0.07)
        else:
            a = 0.96 if t < 0.46 else max(0.0, 0.96 * (1 - (t - 0.46) / 0.06))
        arr[:, x, 3] = int(255 * a * (0.8 if dark else 1))
    bg.alpha_composite(Image.fromarray(arr))
    bg.convert('RGB').save(out, quality=92)


LIFE = [  # (n, title, desc, scene, screen crop, card crop, text side, dark)
    (1, 'Start every day clear', 'A live Today widget: the clock, how much of the week, month and year is left, and a thought for the day.',
     's-sb2.png', 'sb-scr-widget', 'c-sb-widget', 'right', False),
    (2, 'Goals with real progress', 'Link projects to a goal. Its bar fills up as the projects are done.',
     's-sb-m.png', 'sb-scr-goals', 'c-sb-goals', 'right', False),
    (3, 'Every project on one board', 'A progress bar from ticked tasks, plus days left or late. Drag a card when a project moves.',
     's-sb2-m.png', 'sb-scr-projects', 'c-sb-projects', 'left', False),
]

PH = os.path.join(B.HD)
PHONES = [  # (n, title, desc, [phone screenshots])
    (4, 'Small habits, every day', 'One row per day. Tick what you did, and see your score from 1 to 5. Rename the 5 habits to fit your life.', ['sbph-habits']),
    (5, 'A 2-minute daily journal', 'Mood, one win and one thank you before bed. Capture ideas on the go and sort them later.', ['sbph-journal', 'sbph-capture']),
    (6, 'Your Second Brain on your phone', 'A light Mobile home page: today, your next 7 days, habits and journal, one tap away.', ['sbph-mhome', 'sbph-tasks']),
]


def phone(src, left, top, w, rot=0, z=1):
    h = int(w * 1975 / 1080)
    return (f'<div style="position:absolute;left:{left}px;top:{top}px;width:{w + 24}px;height:{h + 24}px;border-radius:52px;background:#1F1D1B;'
            f'box-shadow:0 30px 70px rgba(46,42,37,.30);transform:rotate({rot}deg);z-index:{z}">'
            f'<img src="{src}" style="position:absolute;left:12px;top:12px;width:{w}px;height:{h}px;border-radius:40px"></div>')


def phone_page(n, title, desc, shots, base_url):
    p = L.P['sb']; lab = f'sb-{n + 1}-feature'
    srcs = ['file://' + os.path.join(B.HD, s_ + '.png') for s_ in shots]
    inner = (L.blobs(p['accent'])
             + f'<p style="position:absolute;left:90px;top:170px;width:64px;margin:0;padding:12px 0;text-align:center;border-radius:999px;background:{p["accent"]};color:{L.PAP};font-size:30px;font-weight:700">{n}</p>'
             + L.T(90, 265, 520, title, 60, f'line-height:1.05;color:{L.INK};{L.SER}')
             + L.T(90, 470 if len(title) > 22 else 420, 470, desc, 27, f'line-height:1.45;color:{L.MUT}')
             + L.T(90, 900, 0, 'Second Brain OS', 21, f'font-weight:700;letter-spacing:1px;color:{p["accent"]}'))
    if len(srcs) == 1:
        inner += phone(srcs[0], 790, 70, 400, 0)
    else:
        inner += phone(srcs[1], 960, 150, 330, 5, 1) + phone(srcs[0], 690, 60, 400, -3, 2)
    return L.page(lab, inner, None, p['color'])


def bonus_page(base_url):
    p = L.P['sb']; g = ['file://' + os.path.join(L.ROOT, 'canva', 'v3', 'crops', f'sbguide-{i}.png') for i in (1, 2, 3)]
    sh = 'box-shadow:0 28px 60px rgba(46,42,37,.28);border-radius:10px'
    inner = (L.blobs(p['accent'])
             + L.T(90, 170, 0, 'BONUS', 22, f'padding:10px 22px;border-radius:999px;background:{L.CLAY if hasattr(L, "CLAY") else "#C98B6B"};color:{L.PAP};font-weight:700;letter-spacing:3px')
             + L.T(90, 260, 520, 'Notion for beginners guide', 60, f'line-height:1.05;color:{L.INK};{L.SER}')
             + L.T(90, 470, 450, 'A 7-page PDF: set up, the 6 things to know, databases made simple, your routine, shortcuts and fixes. Learn Notion in 15 minutes.', 27, f'line-height:1.45;color:{L.MUT}')
             + L.T(90, 900, 0, 'Second Brain OS', 21, f'font-weight:700;letter-spacing:1px;color:{p["accent"]}')
             + f'<img src="{g[2]}" style="position:absolute;left:990px;top:190px;width:330px;transform:rotate(7deg);{sh}">'
             + f'<img src="{g[1]}" style="position:absolute;left:860px;top:140px;width:340px;transform:rotate(2deg);{sh}">'
             + f'<img src="{g[0]}" style="position:absolute;left:640px;top:110px;width:400px;transform:rotate(-5deg);{sh}">')
    return L.page('sb-10-bonus', inner, None, p['color'])


def life_page(n, title, desc, scene, screen, card, side, dark, base_url):
    p = L.P['sb']; fg = L.PAP if dark else L.INK; sub = '#F1E7DC' if dark else L.MUT
    lab = f'sb-{n + 1}-feature'; bgf = lab + '.jpg'
    life_bg(scene, screen, os.path.join(L.OUT, 'sb', bgf), side, dark)
    X = 790 if side == 'right' else 110
    inner = (f'<p style="position:absolute;left:{X}px;top:120px;width:64px;margin:0;padding:12px 0;text-align:center;border-radius:999px;background:{p["accent"]};color:{L.PAP};font-size:30px;font-weight:700">{n}</p>'
             + L.T(X, 215, 460, title, 58, f'line-height:1.05;color:{fg};{L.SER}')
             + L.T(X, 400, 430, desc, 26, f'line-height:1.4;color:{sub}')
             + L.T(X, 900, 0, 'Second Brain OS', 21, f'font-weight:700;letter-spacing:1px;color:{p["accent"]}'))
    CW = 560
    url, ih = B.fit(card, CW, 300, f'l{n}'); url = url.replace(B.RAW + 'crops/', base_url + 'crops/')
    cx = 130 if side == 'right' else 1350 - 130 - CW
    inner += (f'<div style="position:absolute;left:{cx}px;top:{H - ih - 120}px;width:{CW}px;height:{ih + 30}px;background:#FFFFFF;border-radius:20px;overflow:hidden;box-shadow:0 14px 40px rgba(0,0,0,.18)">'
              f'<img src="{url}" style="position:absolute;left:0;top:15px;width:{CW}px;height:{ih}px"></div>')
    return L.page(lab, inner, f'{base_url}sb/{bgf}')


if __name__ == '__main__':
    want = sys.argv[1:]
    os.makedirs(os.path.join(L.OUT, 'sb'), exist_ok=True); os.makedirs(os.path.join(L.OUT, 'final', 'sb'), exist_ok=True)
    base = 'file://' + os.path.join(L.ROOT, 'canva', 'v3') + '/LOCALMARK/'
    pages = L.build('sb', base)
    life = [life_page(*row, base) for row in LIFE] + [phone_page(*row, base) for row in PHONES]
    inside = pages[5].replace('sb-6-inside', 'sb-8-inside'); how = pages[6].replace('sb-7-how', 'sb-9-how')
    pages = [pages[0]] + life + [inside, how, bonus_page(base)]
    for pg in pages:
        pg2 = pg.replace('/LOCALMARK/crops/', '/crops/').replace('/LOCALMARK/', '/etsy/')
        lab = re.search(r'data-label="([^"]+)"', pg2).group(1)
        if want and not any(w in lab for w in want):
            continue
        L.render_png(pg2, os.path.join(L.OUT, 'final', 'sb', lab + '.png')); print('ok', lab)
