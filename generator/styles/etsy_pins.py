"""Pinterest pins (1000x1500) for the SystemForge Shop account, which links straight to Etsy listings.

Built from generator/etsy-spec.json (same screenshots and texts as the Etsy listing images), so they look
different from the Gumroad pins. Per product: 1 hero pin, 1 pin per feature, 1 "what's inside" pin.
Writes etsy-pins/<p>-<n>-<kind>.png and rebuilds etsy-pins.json (rotation list, products interleaved).
Usage: python3 generator/styles/etsy_pins.py [p ...]
"""
import json
import os
import sys
import tempfile

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pins_v2 import ROOT, FONT_CSS, INK, MUT, ACC, SAGE, CREAM, PAP, CLAY, SAGEL, shoot  # noqa: E402
from etsy import crop, screen_img  # noqa: E402

W, H = 1000, 1500
OUT = os.path.join(ROOT, 'etsy-pins')
RAW = 'https://raw.githubusercontent.com/samibd778-lab/systemforge-pins/main/etsy-pins/'

CSS = f'''{FONT_CSS}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;background:{CREAM};position:relative;overflow:hidden;font-family:InterW;color:{INK}}}
.blob{{position:absolute;border-radius:50%}}
.top{{position:absolute;left:60px;right:60px;top:70px;text-align:center}}
.k0{{font-weight:700;font-size:24px;letter-spacing:6px;color:{SAGE}}}
h1{{margin-top:18px;font-weight:700;font-size:84px;line-height:1.04;letter-spacing:-3px}}
h1 em{{font-style:normal;background:linear-gradient(transparent 14%,{CLAY} 14%,{CLAY} 92%,transparent 92%);padding:0 10px;border-radius:12px;color:#9A5F3C}}
.sub{{margin:20px auto 0;max-width:820px;font-weight:500;font-size:30px;line-height:1.35;color:{MUT};text-wrap:balance}}
.card{{position:absolute;background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 34px 70px rgba(46,42,37,.2),0 0 0 1px rgba(46,42,37,.06)}}
.bar{{height:36px;background:#F3F0EB;display:flex;align-items:center;gap:8px;padding:0 16px;border-bottom:1px solid #E7E2DA}}
.bar span{{width:11px;height:11px;border-radius:50%;background:#D8D1C6}}
.chips{{position:absolute;left:50px;right:50px;display:flex;flex-direction:column;align-items:center;gap:14px}}
.chip{{display:flex;align-items:center;gap:14px;background:{PAP};border-radius:50px;padding:14px 28px 14px 14px;font-weight:700;font-size:28px;box-shadow:0 8px 20px rgba(46,42,37,.1)}}
.n{{flex:none;width:42px;height:42px;border-radius:50%;background:{SAGE};color:{PAP};font-size:20px;display:flex;align-items:center;justify-content:center}}
.strip{{position:absolute;left:0;right:0;bottom:0;height:110px;background:{SAGE};color:{PAP};display:flex;align-items:center;justify-content:center;gap:14px;font-weight:700;font-size:26px;letter-spacing:3px}}
.name{{position:absolute;left:0;right:0;bottom:132px;text-align:center;font-weight:700;font-size:40px}}
'''
BLOBS = (f'<div class="blob" style="width:520px;height:520px;background:{SAGEL};left:-240px;top:-260px"></div>'
         f'<div class="blob" style="width:560px;height:560px;background:{CLAY};right:-260px;bottom:-200px;opacity:.75"></div>')
STRIP = '<div class="strip">INSTANT DOWNLOAD &nbsp;•&nbsp; ON ETSY</div>'


def page(body, extra=''):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{extra}</style></head><body>{BLOBS}{body}{STRIP}</body></html>'


def card(path, x, y, w, h):
    return (f'<div class="card" style="left:{x}px;top:{y}px;width:{w}px"><div class="bar"><span></span><span></span><span></span></div>'
            f'<img src="file://{path}" style="display:block;width:{w}px;height:{h}px"></div>')


def hero_pin(pr, tmp):
    hs = pr['hero']
    scr = screen_img(hs, tmp, 'pinhero')
    sw, bz = 860, 16
    sh = round(sw / 1.6)
    lx, ly = (W - sw - 2 * bz) // 2, 470
    badges = ''.join(
        f'<div style="position:absolute;left:{[60, 720, 380][i]}px;top:{[1030, 1030, 1090][i]}px;width:220px;height:110px;border-radius:60px;'
        f'background:{[SAGE, ACC, "#9A5F3C"][i]};color:{PAP};display:flex;align-items:center;justify-content:center;text-align:center;'
        f'font-weight:700;font-size:26px;line-height:1.1;padding:12px;border:5px solid {PAP};box-shadow:0 12px 26px rgba(46,42,37,.2)">{b}</div>'
        for i, b in enumerate(hs['badges'][:3]))
    body = (f'<div class="top"><div class="k0">NOTION TEMPLATE</div><h1 style="font-size:{min(hs.get("size", 120) * 0.82, 104):.0f}px">{hs["keyword"]}</h1>'
            f'<div class="sub" style="font-size:24px;letter-spacing:3px;font-weight:700">{hs["features"]}</div></div>'
            f'<div style="position:absolute;left:{(W - 960) // 2}px;top:{ly + sh + 2 * bz - 4}px;width:960px;height:26px;'
            f'background:linear-gradient(#D9D4CC,#B9B2A7);border-radius:0 0 30px 30px"></div>'
            f'<div style="position:absolute;left:{lx}px;top:{ly}px;background:#1E1C1A;border-radius:26px;padding:{bz}px;'
            f'box-shadow:0 40px 80px rgba(46,42,37,.28)"><img src="file://{scr}" style="display:block;width:{sw}px;height:{sh}px;border-radius:6px"></div>'
            + badges + f'<div class="name">{pr["name"]}</div>')
    return page(body)


def feature_pin(pr, f, tmp, n):
    path, (cw, ch), _ = crop(f['shot'], f['crop'], tmp, f'pf{n}', trim=True)
    sc = min(940 / cw, 640 / ch, 2.0)
    w, h = round(cw * sc), round(ch * sc)
    y0 = 440 + (660 - (h + 36)) // 2
    a, b = f['title']
    chips = ''.join(f'<div class="chip"><span class="n">{i + 1}</span>{c}</div>' for i, c in enumerate(f['chips'][:3]))
    body = (f'<div class="top"><div class="k0">{pr["kicker"]}</div><h1>{a}<br><em>{b}</em></h1><div class="sub">{f["sub"]}</div></div>'
            + card(path, (W - w) // 2, y0, w, h)
            + f'<div class="chips" style="top:1110px;flex-direction:row;flex-wrap:wrap;justify-content:center">{chips}</div>')
    return page(body, '.chip{font-size:24px;padding:12px 22px 12px 12px}.n{width:36px;height:36px;font-size:18px}.name{display:none}')


def inside_pin(pr):
    items = ''.join(f'<div class="it"><div class="ck">&#10003;</div><div><b>{a}</b><p>{b}</p></div></div>' for a, b in pr['inside'])
    css = (f'.grid{{position:absolute;left:60px;right:60px;top:330px;display:flex;flex-direction:column;gap:14px}}'
           f'.it{{background:{PAP};border-radius:20px;padding:16px 22px;display:flex;gap:18px;align-items:center;box-shadow:0 8px 20px rgba(46,42,37,.07)}}'
           f'.ck{{flex:none;width:44px;height:44px;border-radius:50%;background:{SAGE};color:{PAP};font-weight:700;font-size:22px;display:flex;align-items:center;justify-content:center}}'
           f'.it b{{font-size:30px}}.it p{{margin-top:2px;font-weight:500;font-size:22px;color:{MUT}}}.name{{bottom:130px}}')
    body = (f'<div class="top"><div class="k0">{pr["kicker"]}</div><h1>What\'s <em>inside</em></h1>'
            f'<div class="sub" style="font-size:28px">{pr["name"]}</div></div><div class="grid">{items}</div>')
    return page(body, css)


def save(html, out, tmp, name):
    img = shoot(html, W, H, None, tmp, name)
    img.resize((W, H), Image.LANCZOS).convert('RGB').save(out, optimize=True)


def build(p, pr):
    os.makedirs(OUT, exist_ok=True)
    made = []
    with tempfile.TemporaryDirectory() as tmp:
        save(hero_pin(pr, tmp), os.path.join(OUT, f'{p}-1-hero.png'), tmp, 'h')
        made.append((f'{p}-1-hero', 'hero', pr['hero']['keyword']))
        for i, f in enumerate(pr['features']):
            nm = f'{p}-{i + 2}-feature'
            save(feature_pin(pr, f, tmp, i), os.path.join(OUT, nm + '.png'), tmp, f'f{i}')
            made.append((nm, 'feature', ' '.join(f['title']) + '. ' + f['sub']))
        nm = f'{p}-{len(pr["features"]) + 2}-inside'
        save(inside_pin(pr), os.path.join(OUT, nm + '.png'), tmp, 'in')
        made.append((nm, 'inside', 'What\'s inside: ' + ', '.join(a for a, _ in pr['inside'])))
    print('ok', p, len(made))
    return made


if __name__ == '__main__':
    spec = json.load(open(os.path.join(ROOT, 'generator', 'etsy-spec.json')))['products']
    links_path = os.path.join(ROOT, 'generator', 'etsy-links.json')
    links = json.load(open(links_path)) if os.path.exists(links_path) else {}
    only = sys.argv[1:] or list(spec)
    per = {p: build(p, spec[p]) for p in only}
    # rotation: interleave products so the same listing never runs twice in a row
    order, i = [], 0
    while any(i < len(v) for v in per.values()):
        for p in only:
            if i < len(per[p]):
                pid, kind, angle = per[p][i]
                order.append({'id': pid, 'product': p, 'name': spec[p]['name'], 'kind': kind, 'angle': angle,
                              'image': RAW + pid + '.png', 'link': links.get(p, ''), 'board': p})
        i += 1
    json.dump(order, open(os.path.join(ROOT, 'etsy-pins.json'), 'w'), indent=1, ensure_ascii=False)
    print('etsy-pins.json', len(order))
