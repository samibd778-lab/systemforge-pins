"""Canva-importable v5 pins (page-first style from the PinClicks top pins): one HTML page per pin,
real Notion page crops as images, all text editable in Canva.
Step 1: python3 generator/v3/canva_v5.py crops        -> canva/v5/img/*.jpg   (commit + push, note the SHA)
Step 2: python3 generator/v3/canva_v5.py html <sha>   -> canva/v5/pins-<set>.html (commit + push, import in Canva)"""
import json, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import mini_listing as M  # noqa: E402
HD = os.path.join(ROOT, 'shots', 'hd'); IMG = os.path.join(ROOT, 'canva', 'v5', 'img'); os.makedirs(IMG, exist_ok=True)
INK, MUT, BG = '#2B2723', '#6A625A', '#FBF8F3'
RAW = 'https://raw.githubusercontent.com/samibd778-lab/systemforge-pins/{sha}/canva/v5/img/{f}'

SETS = {'mjl': {
 'meal-a1': dict(p='meal', style='a', kicker='WEEKLY MEAL PLANNER', title='Meal Planner',
                 sub='Plan the week, cook what you love, shop with one list.',
                 crops=[('meal-week', (0, 0, 640, 569)), ('meal-buy', (0, 0, 700, 624))]),
 'meal-b1': dict(p='meal', style='b', title='WEEKLY MEAL PLANNER', kicker='for Notion',
                 sub='Every meal linked to a recipe. A grocery list sorted by aisle.', badge='Bonus PDF:\nEat Well,\nStress Less',
                 crops=[('meal-recipes', (0, 0, 900, 604)), ('meal-calendar', (0, 0, 900, 487))]),
 'journal-a1': dict(p='journal', style='a', kicker='DAILY JOURNAL', title='Daily Journal',
                    sub='Your mood, one win and one thank you. A few minutes a day.',
                    crops=[('journal-entries', (0, 0, 820, 583)), ('journal-gratitude', (0, 0, 820, 512))]),
 'journal-b1': dict(p='journal', style='b', title='MOOD TRACKER', kicker='for Notion',
                    sub='See how your month felt: average mood, great days and low days.', badge='Bonus PDF:\nJournaling\nguide',
                    crops=[('journal-monthly', (0, 0, 820, 486)), ('journal-calendar', (0, 0, 900, 387))]),
 'life-a1': dict(p='life', style='a', kicker='DIGITAL VISION BOARD', title='Vision Board',
                 sub='Every dream with a photo, and the date you want it by.',
                 crops=[('life-vision', (0, 0, 1000, 595)), ('life-goals', (0, 0, 905, 409))]),
 'life-b1': dict(p='life', style='b', title='LIFE PLANNER', kicker='for Notion',
                 sub='Goals that fill up as you go. Tick a milestone and the bar moves.', badge='Bonus PDF:\n90-Day Goal\nWorkbook',
                 crops=[('life-goals', (0, 0, 905, 409)), ('life-steps', (0, 0, 1000, 309))]),
}}


def cname(n, b): return f'{n}-{b[0]}-{b[1]}-{b[2]}-{b[3]}.jpg'


def fit(n, b, w, maxh):
    """crop box trimmed so the image is at most maxh tall at width w; returns (box, h)"""
    x0, y0, x1, y1 = b
    y1 = min(y1, y0 + int(maxh * (x1 - x0) / w))
    return (x0, y0, x1, y1), round((y1 - y0) * w / (x1 - x0))


def layout(s):
    """list of (box, x, y, w, h) per image"""
    out = []
    if s['style'] == 'a':
        y, room, w, x = 400, 1500 - 400 - 100, 900, 50
    else:
        y, room, w, x = 660, 1500 - 660 - 100, 1000, 0
    for n, b in s['crops']:
        box, h = fit(n, b, w, room)
        if out and h < 230: break  # a thin strip looks cut off
        out.append((n, box, x, y, w, h)); y += h + 22; room -= h + 22
        if room < 120: break
    return out


def p(x, y, w, size, text, color, extra=''):
    return (f'<p style="position:absolute;left:{x}px;top:{y}px;width:{w}px;margin:0;font-size:{size}px;'
            f'text-align:center;color:{color};{extra}">{text}</p>')


def page(pid, s, sha):
    pr = M.PROD[s['p']]; c, acc = pr['color'], pr['accent']
    imgs = ''.join(f'<img src="{RAW.format(sha=sha, f=cname(n, box))}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
                   for n, box, x, y, w, h in layout(s))
    foot = p(0, 1440, 1000, 22, 'SYSTEMFORGE · INSTANT DOWNLOAD', MUT, 'font-weight:700;letter-spacing:3px')
    if s['style'] == 'a':
        head = (f'<div style="position:absolute;left:0;top:0;width:1000px;height:430px;background:{c}"></div>'
                + p(0, 58, 1000, 24, s['kicker'], acc, 'font-weight:700;letter-spacing:5px')
                + p(0, 92, 1000, 140, s['title'], INK, "font-family:'Great Vibes',cursive;line-height:1.1")
                + p(90, 268, 820, 31, s['sub'], MUT, 'line-height:1.35'))
    else:
        head = (f'<div style="position:absolute;left:0;top:0;width:1000px;height:520px;background:{acc}"></div>'
                + p(60, 70, 880, 104, s['title'], '#FFFFFF', "font-family:'Playfair Display',serif;font-weight:700;line-height:1.02")
                + p(0, 390, 1000, 84, s['kicker'], '#FFFFFF', "font-family:'Great Vibes',cursive")
                + p(60, 560, 880, 33, s['sub'], INK, 'line-height:1.3'))
        badge = (f'<div style="position:absolute;left:740px;top:1150px;width:220px;height:220px;border-radius:110px;background:{c}"></div>'
                 + p(740, 1210, 220, 25, s['badge'].replace('\n', '<br>'), INK, 'font-weight:700;line-height:1.25'))
        imgs += badge
    return (f'<div data-document-role="page" data-label="{pid}" style="position:relative;width:1000px;height:1500px;overflow:hidden;background:{BG}">'
            + head + imgs + foot + '</div>')


if __name__ == '__main__':
    mode = sys.argv[1]; S = SETS['mjl']
    if mode == 'crops':
        for pid, s in S.items():
            for n, box, *_ in layout(s):
                Image.open(os.path.join(HD, n + '.jpg')).convert('RGB').crop(box).save(os.path.join(IMG, cname(n, box)), quality=93)
        print(sorted(os.listdir(IMG)))
    else:
        sha = sys.argv[2]
        html = ('<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700'
                '&family=Great+Vibes&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">'
                '<style>body{margin:0}div,span,p{font-family:Inter,Arial,sans-serif}</style></head><body>'
                + '\n'.join(page(pid, s, sha) for pid, s in S.items()) + '</body></html>')
        out = os.path.join(ROOT, 'canva', 'v5', 'pins-mjl.html'); open(out, 'w').write(html); print(out, len(html))
