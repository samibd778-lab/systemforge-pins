"""Etsy listing images (2000x1500, 4:3) from generator/etsy-spec.json.

Per product it writes etsy/<p>/01-hero.jpg, 02..05 feature images (screenshot card + numbered callouts),
06-inside.jpg (what's inside) and 07-how.jpg (how you get it).
Usage: python3 generator/styles/etsy.py [fco|ccs ...]
"""
import json
import os
import sys
import tempfile

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pins_v2 import ROOT, FONT_CSS, INK, MUT, ACC, SAGE, CREAM, PAP, CLAY, SAGEL, shoot  # noqa: E402

W, H = 2000, 1500
OUT = os.path.join(ROOT, 'etsy')

BASE_CSS = f'''{FONT_CSS}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;background:{CREAM};position:relative;overflow:hidden;font-family:InterW;color:{INK}}}
.blob{{position:absolute;border-radius:50%}}
.kick{{display:inline-flex;align-items:center;gap:12px;background:{PAP};border-radius:40px;padding:14px 28px;font-weight:700;font-size:24px;letter-spacing:2px;box-shadow:0 6px 20px rgba(46,42,37,.08)}}
.kick i{{width:32px;height:32px;border-radius:50%;background:{SAGE};color:{PAP};font-style:normal;font-weight:700;font-size:14px;display:flex;align-items:center;justify-content:center}}
h1{{font-weight:700;font-size:92px;line-height:1.05;letter-spacing:-3px}}
h1 em{{font-style:normal;background:linear-gradient(transparent 14%,{CLAY} 14%,{CLAY} 92%,transparent 92%);padding:0 14px;border-radius:14px;color:#9A5F3C}}
.sub{{font-weight:500;font-size:36px;line-height:1.35;color:{MUT}}}
.card{{position:absolute;background:#fff;border-radius:22px;overflow:hidden;box-shadow:0 40px 90px rgba(46,42,37,.18),0 0 0 1px rgba(46,42,37,.06)}}
.bar{{height:44px;background:#F3F0EB;display:flex;align-items:center;gap:10px;padding:0 20px;border-bottom:1px solid #E7E2DA}}
.bar span{{width:14px;height:14px;border-radius:50%;background:#D8D1C6}}
.bar b{{margin-left:16px;font-weight:500;font-size:18px;color:{MUT}}}
.pills{{display:flex;gap:16px}}
.pill{{background:{PAP};border-radius:40px;padding:16px 28px;font-weight:700;font-size:26px;box-shadow:0 6px 18px rgba(46,42,37,.08)}}
.pill:before{{content:"\\2713";color:{SAGE};margin-right:10px}}
.foot{{position:absolute;bottom:56px;right:90px;display:flex;align-items:center;gap:14px;font-weight:700;font-size:28px}}
.foot i{{width:50px;height:50px;border-radius:50%;background:{SAGE};color:{PAP};font-style:normal;font-weight:700;font-size:20px;display:flex;align-items:center;justify-content:center}}
'''
BLOBS = (f'<div class="blob" style="width:760px;height:760px;background:{SAGEL};left:-330px;top:-380px"></div>'
         f'<div class="blob" style="width:820px;height:820px;background:{CLAY};right:-360px;bottom:-420px;opacity:.75"></div>')
FOOT = '<div class="foot"><i>SF</i>SystemForge</div>'
PILLS = ['Instant download', 'Ready-made Notion template', '5-minute setup']


def page(body, extra_css=''):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}{extra_css}</style></head><body>{BLOBS}{body}{FOOT}</body></html>'


def crop(shot, box, tmp, name, trim=False):
    """Cut box out of the screenshot. trim=True removes empty white margins (returns the new box)."""
    im = Image.open(os.path.join(ROOT, shot)).convert('RGB')
    x0, y0, x1, y1 = box
    c = Image.new('RGB', (x1 - x0, y1 - y0), 'white')
    c.paste(im, (-x0, -y0))
    if trim:
        from PIL import ImageOps
        g = ImageOps.invert(c.convert('L')).point(lambda v: 255 if v > 14 else 0)
        bb = g.getbbox()
        if bb:
            pad = 28
            l, t, r, b = max(0, bb[0] - pad), max(0, bb[1] - pad), min(c.width, bb[2] + pad), min(c.height, bb[3] + pad)
            c = c.crop((l, t, r, b))
            box = [x0 + l, y0 + t, x0 + r, y0 + b]
    path = os.path.join(tmp, name + '.png')
    c.save(path)
    return (path, c.size, box) if trim else (path, c.size)


def card_html(path, x, y, w, h, title):
    return (f'<div class="card" style="left:{x}px;top:{y}px;width:{w}px">'
            f'<div class="bar"><span></span><span></span><span></span><b>{title}</b></div>'
            f'<img src="file://{path}" style="display:block;width:{w}px;height:{h}px"></div>')


def title_html(t):
    a, b = t
    return f'{a}<br><em>{b}</em>'


def hero(p, pr, tmp):
    """Etsy search shows the main photo cropped to a ~4:5 portrait tile (only the middle ~1200px of 2000).
    So the kicker, title, subtitle and pills stay inside x 420..1580; the screenshot card can run wider."""
    hs = pr['hero']
    path, (cw, ch) = crop(hs['shot'], hs['crop'], tmp, 'hero')
    w = 1640
    css = ('.col{position:absolute;left:0;right:0;top:64px;bottom:170px;display:flex;flex-direction:column;align-items:center;text-align:center}'
           '.col h1{margin-top:30px;font-size:108px;line-height:1.02;max-width:1160px}'
           '.col .sub{margin-top:24px;font-size:36px;max-width:1000px;text-wrap:balance}'
           f'.hc{{margin-top:48px;width:{w}px;flex:1;min-height:0}}'
           '.hc img{height:auto!important}'
           '.pills{position:absolute;left:0;right:0;bottom:52px;justify-content:center;gap:14px}'
           '.pill{font-size:25px;padding:15px 24px}.foot{display:none}')
    card = card_html(path, 0, 0, w, round(w * ch / cw), pr['name']).replace('position:absolute', 'position:relative').replace(
        'style="left:0px;top:0px;', 'style="')
    body = (f'<div class="col"><div class="kick"><i>SF</i>{pr["kicker"]}</div>'
            f'<h1>{title_html(hs["title"])}</h1>'
            f'<div class="sub">{hs["sub"]}</div>'
            f'<div class="hc" style="position:relative">{card.replace("class=\"card\"", "class=\"card\" ", 1)}</div></div>'
            + f'<div class="pills">{"".join(f"<div class=pill>{x}</div>" for x in PILLS)}</div>')
    return page(body, css + '.hc .card{height:100%}')


def feature(p, pr, f, v2, tmp, n):
    """Big zoomed screenshot card + a row of 3 benefit chips (readable even as a small Etsy photo)."""
    path, (cw, ch), _ = crop(f['shot'], f['crop'], tmp, f'feat{n}', trim=True)
    maxw, maxh = 1820, 740
    sc = min(maxw / cw, maxh / ch, 1.7)
    w, h = round(cw * sc), round(ch * sc)
    x0 = (W - w) // 2
    y0 = 450 + (780 - (h + 44)) // 2
    chips = ''.join(f'<div class="chip"><span class="n">{i + 1}</span>{c}</div>' for i, c in enumerate(f['chips'][:3]))
    css = (f'.chips{{position:absolute;left:90px;right:90px;bottom:150px;display:flex;justify-content:center;gap:22px}}'
           f'.chip{{display:flex;align-items:center;gap:16px;background:{PAP};border-radius:60px;padding:18px 32px 18px 18px;'
           f'font-weight:700;font-size:32px;box-shadow:0 10px 26px rgba(46,42,37,.1)}}'
           f'.n{{flex:none;width:50px;height:50px;border-radius:50%;background:{SAGE};color:{PAP};font-size:24px;display:flex;align-items:center;justify-content:center}}')
    body = (f'<div style="position:absolute;left:90px;top:80px;right:90px">'
            f'<div class="kick"><i>SF</i>{pr["kicker"]}</div>'
            f'<h1 style="margin-top:30px">{title_html(f["title"])}</h1>'
            f'<div class="sub" style="margin-top:18px">{f["sub"]}</div></div>'
            + card_html(path, x0, y0, w, h, pr['name'])
            + f'<div class="chips">{chips}</div>')
    return page(body, css)


def inside(p, pr):
    items = ''.join(f'<div class="it"><div class="ck">&#10003;</div><div><div class="t">{a}</div><div class="d">{b}</div></div></div>'
                    for a, b in pr['inside'])
    css = (f'.grid{{position:absolute;left:90px;right:90px;top:400px;display:grid;grid-template-columns:1fr 1fr;gap:26px}}'
           f'.it{{background:{PAP};border-radius:26px;padding:30px 34px;display:flex;gap:22px;align-items:flex-start;box-shadow:0 10px 26px rgba(46,42,37,.07)}}'
           f'.ck{{flex:none;width:52px;height:52px;border-radius:50%;background:{SAGE};color:{PAP};font-weight:700;font-size:26px;display:flex;align-items:center;justify-content:center}}'
           f'.t{{font-weight:700;font-size:36px}}.d{{margin-top:6px;font-weight:500;font-size:27px;line-height:1.35;color:{MUT}}}')
    body = (f'<div style="position:absolute;left:90px;top:80px;right:90px">'
            f'<div class="kick"><i>SF</i>{pr["kicker"]}</div>'
            f'<h1 style="margin-top:30px">What\'s <em>inside</em></h1></div>'
            f'<div class="grid">{items}</div>')
    return page(body, css)


def how(p, pr):
    steps = [('Buy and download', 'You get a PDF with your private template link.'),
             ('Open the link', 'Click the button in the PDF. It opens in your browser.'),
             ('Click Duplicate', 'The template is copied into your own Notion workspace.'),
             ('Open "Start here"', 'Follow the short guide, then delete the example data.')]
    st = ''.join(f'<div class="s"><div class="num">{i + 1}</div><div class="t">{a}</div><div class="d">{b}</div></div>'
                 for i, (a, b) in enumerate(steps))
    know = ['You need a Notion account. Create one at notion.com in a minute.',
            'Set it up on a computer first, then use it on the Notion app on your phone.',
            'Change anything: names, colors, columns and views.',
            'Digital product. No physical item will be shipped.']
    kn = ''.join(f'<li>{x}</li>' for x in know)
    css = (f'.row{{position:absolute;left:90px;right:90px;top:420px;display:grid;grid-template-columns:repeat(4,1fr);gap:26px}}'
           f'.s{{background:{PAP};border-radius:28px;padding:40px 34px;box-shadow:0 10px 26px rgba(46,42,37,.07);min-height:380px}}'
           f'.num{{width:70px;height:70px;border-radius:50%;background:{SAGE};color:{PAP};font-weight:700;font-size:34px;display:flex;align-items:center;justify-content:center}}'
           f'.t{{margin-top:28px;font-weight:700;font-size:38px;line-height:1.15}}.d{{margin-top:14px;font-weight:500;font-size:28px;line-height:1.4;color:{MUT}}}'
           f'.know{{position:absolute;left:90px;right:90px;top:880px;background:{PAP};border-radius:28px;padding:36px 44px;box-shadow:0 10px 26px rgba(46,42,37,.07)}}'
           f'.know h3{{font-size:34px}}.know ul{{margin:16px 0 0 30px;font-weight:500;font-size:28px;line-height:1.6;color:{MUT}}}')
    body = (f'<div style="position:absolute;left:90px;top:80px;right:90px">'
            f'<div class="kick"><i>SF</i>{pr["kicker"]}</div>'
            f'<h1 style="margin-top:30px">How you <em>get it</em></h1></div>'
            f'<div class="row">{st}</div><div class="know"><h3>Good to know</h3><ul>{kn}</ul></div>')
    return page(body, css)


def save(html, out, tmp, name):
    img = shoot(html, W, H, None, tmp, name)
    img.resize((W, H), Image.LANCZOS).convert('RGB').save(out, quality=92, subsampling=0)


def build(p, pr, v2):
    d = os.path.join(OUT, p)
    os.makedirs(d, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        save(hero(p, pr, tmp), os.path.join(d, '01-hero.jpg'), tmp, 'hero')
        for i, f in enumerate(pr['features']):
            save(feature(p, pr, f, v2, tmp, i), os.path.join(d, f'0{i + 2}-feature.jpg'), tmp, f'f{i}')
        n = len(pr['features']) + 2
        save(inside(p, pr), os.path.join(d, f'0{n}-inside.jpg'), tmp, 'inside')
        save(how(p, pr), os.path.join(d, f'0{n + 1}-how.jpg'), tmp, 'how')
    print('ok', p)


if __name__ == '__main__':
    spec = json.load(open(os.path.join(ROOT, 'generator', 'etsy-spec.json')))['products']
    v2 = {sp['id']: sp for sp in json.load(open(os.path.join(ROOT, 'generator', 'pins-v2-spec.json')))['pins']}
    only = sys.argv[1:] or list(spec)
    for p in only:
        build(p, spec[p], v2)
