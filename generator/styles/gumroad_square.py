"""Mobile-first square Gumroad cover (1600x1600), Gumroad black-and-white style.

A 16:9 cover shows very small on a phone; a square one fills the screen width with twice the height,
so the title and screenshot stay readable. Uses screenshots and texts from etsy-spec.json.
Writes gumroad-square/<p>.png. Usage: python3 generator/styles/gumroad_square.py [p ...]
"""
import json
import os
import sys
import tempfile

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pins_v2 import ROOT, FONT_CSS, shoot  # noqa: E402
from etsy import screen_img  # noqa: E402

S = 1600
OUT = os.path.join(ROOT, 'gumroad-square')
COPY = {
    'fco': ('Freelancer<br>Client OS', 'Run your whole freelance business from one Notion page.',
            ['Clients + proposals', 'Projects + tasks', 'Invoices + expenses']),
    'ccs': ('Content<br>Creator Studio', 'Plan every post on every platform and track brand deals.',
            ['Content calendar', 'Weekly channel goals', 'Brand deal tracker']),
    'fit': ('Freelance<br>Invoice Tracker', 'See who owes you money and which email to send next.',
            ['Late invoices flagged', 'Next step on each one', 'Reminder emails']),
    'wcp': ('Weekly<br>Content Planner', 'Move every idea to Posted and never miss a posting date.',
            ['Idea to Posted board', 'Goal per platform', '30 content ideas']),
}
FREE = {'fit', 'wcp'}


def html(p, pr, tmp):
    title, sub, chips = COPY[p]
    scr = screen_img(pr['hero'], tmp, 'sq')
    sw = 1400
    sh = 690
    tag = 'FREE NOTION TEMPLATE' if p in FREE else 'NOTION TEMPLATE'
    ch = ''.join(f'<div class="chip">{c}</div>' for c in chips)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{FONT_CSS}
*{{margin:0;box-sizing:border-box}}
body{{width:{S}px;height:{S}px;background:#F4F4F2;font-family:InterW;color:#0A0A0A;position:relative;overflow:hidden}}
.top{{position:absolute;left:100px;right:100px;top:90px}}
.k{{display:flex;align-items:center;gap:20px;font-family:"DejaVu Sans Mono",monospace;font-size:32px;letter-spacing:6px;color:#333}}
.k i{{font-style:normal;width:70px;height:70px;border-radius:14px;background:#0A0A0A;color:#fff;font-family:InterW;font-weight:700;font-size:30px;letter-spacing:0;display:flex;align-items:center;justify-content:center}}
h1{{margin-top:30px;font-weight:700;font-size:128px;line-height:.98;letter-spacing:-5px}}
.sub{{margin-top:24px;font-weight:500;font-size:42px;line-height:1.25;color:#333;max-width:1300px}}
.card{{position:absolute;left:100px;top:650px;width:{sw}px;border:3px solid #0A0A0A;border-radius:24px;overflow:hidden;background:#fff;box-shadow:16px 16px 0 #0A0A0A}}
.card img{{display:block;width:{sw}px;height:{sh}px;object-fit:cover;object-position:top}}
.chips{{position:absolute;left:100px;right:100px;bottom:110px;display:flex;gap:20px}}
.chip{{flex:1;text-align:center;background:#fff;border:3px solid #0A0A0A;border-radius:60px;padding:22px 10px;font-weight:700;font-size:36px}}
</style></head><body>
<div class="top"><div class="k"><i>SF</i>{tag}</div><h1>{title}</h1><div class="sub">{sub}</div></div>
<div class="card"><img src="file://{scr}"></div>
<div class="chips">{ch}</div>
</body></html>'''


if __name__ == '__main__':
    spec = json.load(open(os.path.join(ROOT, 'generator', 'etsy-spec.json')))['products']
    os.makedirs(OUT, exist_ok=True)
    for p in sys.argv[1:] or list(COPY):
        with tempfile.TemporaryDirectory() as tmp:
            img = shoot(html(p, spec[p], tmp), S, S, None, tmp, p)
            img.resize((S, S), Image.LANCZOS).convert('RGB').save(os.path.join(OUT, f'{p}.png'), optimize=True)
        print('ok', p)
