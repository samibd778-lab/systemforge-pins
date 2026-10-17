"""Gumroad thumbnail 600x600 (rendered 1200x1200), black background, white title, module chips, Instant access pill.
Usage: python3 generator/styles/gumroad_thumb.py prop deal -> gumroad-thumb/<p>.png
"""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pins_v2 import ROOT, FONT_CSS, shoot  # noqa: E402

T = {
    'prop': ('Proposal<br>Tracker', ['Follow-ups', 'Pipeline', 'Clients', 'Price check']),
    'deal': ('Brand Deal<br>Tracker', ['Deals', 'Posts owed', 'Payments', 'Media kit']),
}
S = 1200


def html(p):
    title, mods = T[p]
    chips = ''.join(f'<div class="m"><span>&#10003;</span>{m}</div>' for m in mods)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{FONT_CSS}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{S}px;height:{S}px;background:#0A0A0A;color:#fff;font-family:InterW;position:relative;overflow:hidden}}
.top{{position:absolute;left:90px;top:90px;display:flex;align-items:center;gap:18px;font-family:monospace;font-size:30px;letter-spacing:6px;color:#BDBDBD}}
.top b{{width:64px;height:64px;border-radius:12px;background:#fff;color:#0A0A0A;display:flex;align-items:center;justify-content:center;font-family:InterW;font-size:28px;letter-spacing:0}}
h1{{position:absolute;left:86px;top:220px;font-weight:800;font-size:150px;line-height:.98;letter-spacing:-6px}}
.grid{{position:absolute;left:90px;right:90px;top:640px;display:grid;grid-template-columns:1fr 1fr;gap:22px}}
.m{{border:3px solid #fff;border-radius:22px;padding:26px 28px;font-weight:700;font-size:42px;display:flex;align-items:center;gap:18px}}
.m span{{width:46px;height:46px;border-radius:50%;background:#fff;color:#0A0A0A;font-size:26px;display:flex;align-items:center;justify-content:center;flex:none}}
.pill{{position:absolute;left:90px;bottom:90px;background:#fff;color:#0A0A0A;border-radius:60px;padding:22px 40px;font-weight:800;font-size:38px}}
</style></head><body><div class="top"><b>SF</b>NOTION TEMPLATE</div><h1>{title}</h1><div class="grid">{chips}</div><div class="pill">Instant access</div></body></html>'''


if __name__ == '__main__':
    out = os.path.join(ROOT, 'gumroad-thumb')
    os.makedirs(out, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for p in sys.argv[1:]:
            img = shoot(html(p), S, S, None, tmp, p)
            img.convert('RGB').resize((600, 600)).save(os.path.join(out, p + '.png'))
            print('ok', p)
