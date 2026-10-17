"""Horizontal Gumroad cover 1280x720 (rendered 2560x1440), black-and-white style.
Gumroad rule: cover images must be horizontal, at least 1280x720px, 72 DPI.
Writes gumroad-wide/<p>.png. Usage: python3 generator/styles/gumroad_wide.py prop deal
"""
import json, os, sys, tempfile
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pins_v2 import ROOT, FONT_CSS, shoot  # noqa: E402
from etsy import screen_img  # noqa: E402
from gumroad_square import COPY, FREE  # noqa: E402

W, H = 2560, 1440
OUT = os.path.join(ROOT, 'gumroad-wide')


def html(p, pr, tmp):
    title, sub, chips = COPY[p]
    scr = screen_img({'screen': pr.get('gsq_screen', pr['hero']['screen'])}, tmp, 'w')
    tag = 'FREE NOTION TEMPLATE' if p in FREE else 'NOTION TEMPLATE'
    ch = ''.join(f'<div class="chip"><span>&#10003;</span>{c}</div>' for c in chips)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{FONT_CSS}
*{{margin:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;background:#F4F4F2;font-family:InterW;color:#0A0A0A;position:relative;overflow:hidden}}
.l{{position:absolute;left:150px;top:0;bottom:0;width:1000px;display:flex;flex-direction:column;justify-content:center}}
.k{{display:flex;align-items:center;gap:22px;font-family:"DejaVu Sans Mono",monospace;font-size:34px;letter-spacing:7px;color:#333}}
.k i{{font-style:normal;width:76px;height:76px;border-radius:16px;background:#0A0A0A;color:#fff;font-family:InterW;font-weight:700;font-size:32px;letter-spacing:0;display:flex;align-items:center;justify-content:center}}
h1{{margin-top:40px;font-weight:700;font-size:168px;line-height:.96;letter-spacing:-7px}}
.sub{{margin-top:36px;font-weight:500;font-size:50px;line-height:1.25;color:#333}}
.chips{{margin-top:56px;display:flex;flex-direction:column;gap:20px}}
.chip{{display:flex;align-items:center;gap:22px;font-weight:700;font-size:44px}}
.chip span{{width:56px;height:56px;border-radius:50%;background:#0A0A0A;color:#fff;font-size:30px;display:flex;align-items:center;justify-content:center;flex:none}}
.card{{position:absolute;left:1260px;top:190px;width:1500px;height:1060px;border:4px solid #0A0A0A;border-radius:28px;overflow:hidden;background:#fff;box-shadow:20px 20px 0 #0A0A0A}}
.card img{{display:block;width:1500px;height:1060px;object-fit:cover;object-position:left top}}
</style></head><body>
<div class="l"><div class="k"><i>SF</i>{tag}</div><h1>{title}</h1><div class="sub">{sub}</div><div class="chips">{ch}</div></div>
<div class="card"><img src="file://{scr}"></div>
</body></html>'''


if __name__ == '__main__':
    spec = json.load(open(os.path.join(ROOT, 'generator', 'etsy-spec.json')))['products']
    os.makedirs(OUT, exist_ok=True)
    for p in sys.argv[1:]:
        with tempfile.TemporaryDirectory() as tmp:
            img = shoot(html(p, spec[p], tmp), W, H, None, tmp, p)
            img.resize((W, H), Image.LANCZOS).convert('RGB').save(os.path.join(OUT, f'{p}.png'), optimize=True)
        print('ok', p)
