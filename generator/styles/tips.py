"""SystemForge value-first tip pins (built from generator/tips-spec.json).

For every spec it writes:
  <repo>/<id>.png      1000x1500  Pinterest
  <repo>/ig/<id>.jpg   1080x1350  Instagram/Facebook
Both: kicker, big headline, numbered tips, a soft "want it done for you?" line, SystemForge footer.

Usage: python3 generator/styles/tips.py [id-prefix ...]
Then:  python3 generator/gen.py --json   (mixes the tips into pins.json)
"""
import json
import os
import sys
import tempfile

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pins_v2 import (ROOT, FONT_CSS, INK, MUT, ACC, SAGE, CREAM, PAP, CLAY, SAGEL, PRODUCTS, shoot)  # noqa: E402

SAVE = {'pin': 'Save this pin for later 📌', 'ig': 'Save this for later 🔖'}


def html(sp, w, h, kind):
    a, hl, b = sp['title']
    title = (f'{a}<br>' if a else '') + f'<em>{hl}</em>' + (f'<br>{b}' if b else '')
    n = len(sp['tips'])
    big = kind == 'pin'
    # sizes tuned so 4 or 5 tips always fit
    h1 = 96 if big else 80
    head = (40 if n <= 4 else 35) if big else (38 if n <= 4 else 34)
    det = (29 if n <= 4 else 26) if big else (28 if n <= 4 else 25)
    gap = (26 if n <= 4 else 18) if big else (20 if n <= 4 else 14)
    dot = SAGE if sp['p'] == 'fco' else ACC
    items = ''.join(
        f'<div class="t"><span class="n" style="background:{dot}">{i + 1}</span>'
        f'<div><div class="h">{t}</div><div class="d">{d}</div></div></div>'
        for i, (t, d) in enumerate(sp['tips']))
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{FONT_CSS}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;background:{CREAM};position:relative;overflow:hidden;font-family:InterW;color:{INK}}}
.blob{{position:absolute;border-radius:50%}}
.wrap{{position:absolute;inset:0;padding:{58 if big else 52}px {60 if big else 64}px {50 if big else 44}px;display:flex;flex-direction:column}}
.kick{{text-align:center}}
.kick span{{display:inline-flex;align-items:center;gap:10px;background:{PAP};border-radius:40px;padding:12px 24px;font-weight:700;font-size:21px;letter-spacing:1.6px;box-shadow:0 6px 20px rgba(46,42,37,.08)}}
.kick i{{width:28px;height:28px;border-radius:50%;background:{SAGE};color:{PAP};font-style:italic;font-family:Fraunces;font-size:14px;display:flex;align-items:center;justify-content:center}}
h1{{margin:{34 if big else 26}px 0 {34 if big else 26}px;text-align:center;font-family:Fraunces;font-weight:600;font-size:{h1}px;line-height:1.05;letter-spacing:-2.4px}}
h1 em{{font-style:normal;background:linear-gradient(transparent 12%,{CLAY} 12%,{CLAY} 92%,transparent 92%);padding:0 14px;border-radius:14px;color:#9A5F3C}}
.list{{flex:1;display:flex;flex-direction:column;justify-content:center;gap:{gap}px}}
.t{{display:flex;gap:20px;align-items:center;background:{PAP};border-radius:24px;padding:{30 if n <= 4 else 24 if big else 20}px 28px;box-shadow:0 10px 26px rgba(46,42,37,.08)}}
.n{{flex:none;width:{56 if big else 50}px;height:{56 if big else 50}px;border-radius:50%;color:{PAP};font-weight:700;font-size:24px;display:flex;align-items:center;justify-content:center}}
.h{{font-weight:700;font-size:{head}px;line-height:1.18}}
.d{{margin-top:5px;font-weight:500;font-size:{det}px;line-height:1.3;color:{MUT}}}
.cta{{margin-top:{30 if big else 22}px;text-align:center;font-size:{26 if big else 25}px;line-height:1.35;color:{MUT}}}
.cta b{{color:{INK}}}
.foot{{margin-top:{22 if big else 16}px;display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:24px}}
.foot .l{{display:flex;align-items:center;gap:12px}}
.foot i{{width:42px;height:42px;border-radius:50%;background:{SAGE};color:{PAP};font-style:italic;font-family:Fraunces;font-size:19px;display:flex;align-items:center;justify-content:center}}
.foot .s{{font-weight:500;font-size:22px;color:{MUT}}}
</style></head><body>
<div class="blob" style="width:600px;height:600px;background:{SAGEL};left:-260px;top:-250px"></div>
<div class="blob" style="width:680px;height:680px;background:{CLAY};right:-340px;bottom:-330px;opacity:.75"></div>
<div class="wrap">
<div class="kick"><span><i>SF</i>{sp['kicker']}</span></div>
<h1>{title}</h1>
<div class="list">{items}</div>
<div class="cta">Want this done for you? Try <b>{PRODUCTS[sp['p']]}</b> for Notion.</div>
<div class="foot"><div class="l"><i>SF</i>SystemForge</div><div class="s">{SAVE[kind]}</div></div>
</div></body></html>'''


def build(sp):
    with tempfile.TemporaryDirectory() as tmp:
        pin = shoot(html(sp, 1000, 1500, 'pin'), 1000, 1500, None, tmp, 'pin')
        pin.resize((1000, 1500), Image.LANCZOS).convert('RGB').save(os.path.join(ROOT, sp['id'] + '.png'), optimize=True)
        ig = shoot(html(sp, 1080, 1350, 'ig'), 1080, 1350, None, tmp, 'ig')
        os.makedirs(os.path.join(ROOT, 'ig'), exist_ok=True)
        ig.resize((1080, 1350), Image.LANCZOS).convert('RGB').save(os.path.join(ROOT, 'ig', sp['id'] + '.jpg'), quality=93, subsampling=0)


if __name__ == '__main__':
    specs = json.load(open(os.path.join(ROOT, 'generator', 'tips-spec.json')))['pins']
    only = sys.argv[1:]
    for sp in specs:
        if not only or any(sp['id'].startswith(o) for o in only):
            build(sp)
            print('ok', sp['id'])
