"""Instagram carousels v2 (2026-10): bold dark design, big readable text, real Notion crops.

Spec: generator/carousels2-spec.json -> carousels/<id>/<n>.jpg, then carousels.json is rebuilt
(new v2 carousels first, then the older ones from carousels-spec.json).
Rules from the 2026 growth research: one idea per slide, text readable on a phone, real product
proof (crops of the real template), a save/send prompt at the end (sends + saves drive reach).
Usage: python3 generator/carousel2.py [id ...]
"""
import json, os, sys, subprocess, tempfile
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.environ.get('CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
FONTS = os.path.join(ROOT, 'generator', 'remotion', 'public')
W, H = 1080, 1350
TMP = tempfile.mkdtemp(prefix='car2-')

PRODUCTS = {'fco': 'Freelancer Client OS', 'ccs': 'Content Creator Studio', 'prop': 'Proposal Tracker', 'deal': 'Brand Deal Tracker'}
ACCENT = {'fco': '#7FE0B0', 'ccs': '#FFB547', 'prop': '#8AB8FF', 'deal': '#FF9EB5'}
BG1, BG2, INK, MUT = '#101216', '#1B1F27', '#F6F4EF', '#A9B0BC'

CSS = f'''
@font-face{{font-family:MontX;src:url(file://{FONTS}/montserrat800.woff2);font-weight:800}}
@font-face{{font-family:MontX;src:url(file://{FONTS}/montserrat900.woff2);font-weight:900}}
@font-face{{font-family:InterW;src:url(file://{FONTS}/inter500.woff2);font-weight:500}}
@font-face{{font-family:InterW;src:url(file://{FONTS}/inter700.woff2);font-weight:700}}
body{{margin:0}}*{{box-sizing:border-box}}
.h{{font-family:MontX;font-weight:900;letter-spacing:-2px;color:{INK};margin:0}}
.t{{font-family:InterW;font-weight:500;color:{MUT};margin:0}}
mark{{background:none;color:var(--acc)}}
'''


def crop(src, box, mark=None):
    """Crop a real screenshot (shots/...). box/mark in source pixels. Returns (path, w, h, mark_rel)."""
    im = Image.open(os.path.join(ROOT, src)).convert('RGB').crop(tuple(box))
    p = os.path.join(TMP, f'{abs(hash((src, tuple(box))))}.png')
    im.save(p)
    rel = None
    if mark:
        rel = [(mark[0] - box[0]) / im.width, (mark[1] - box[1]) / im.height, (mark[2] - mark[0]) / im.width, (mark[3] - mark[1]) / im.height]
    return p, im.width, im.height, rel


def card(shot, width=960, max_h=560, tilt=0):
    p, w, h, rel = crop(shot['src'], shot['box'], shot.get('mark'))
    s = min(width / w, max_h / h)
    cw, ch = int(w * s), int(h * s)
    ring = ''
    if rel:
        ring = (f'<div style="position:absolute;left:{rel[0]*cw-10}px;top:{rel[1]*ch-8}px;width:{rel[2]*cw+20}px;height:{rel[3]*ch+16}px;'
                f'border:6px solid var(--acc);border-radius:16px;box-shadow:0 0 0 8px rgba(0,0,0,.08),0 0 30px var(--acc)"></div>')
    return (f'<div style="position:relative;width:{cw}px;height:{ch}px;border-radius:26px;overflow:visible;transform:rotate({tilt}deg);'
            f'box-shadow:0 40px 80px rgba(0,0,0,.55)"><img src="file://{p}" style="width:{cw}px;height:{ch}px;border-radius:26px;display:block">{ring}</div>')


def page(c, inner, n, total):
    acc = ACCENT[c['p']]
    dots = ''.join(f'<span style="width:{30 if i == n else 10}px;height:10px;border-radius:5px;background:{acc if i == n else "#3A404C"}"></span>' for i in range(total))
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div style="--acc:{acc};position:relative;overflow:hidden;width:{W}px;height:{H}px;background:radial-gradient(120% 80% at 50% 0%,{BG2} 0%,{BG1} 60%);padding:84px 70px 64px;display:flex;flex-direction:column">
<div style="position:absolute;left:-160px;bottom:-200px;width:700px;height:700px;border-radius:50%;background:{acc};opacity:.10;filter:blur(90px)"></div>
<div style="position:relative;flex:1;display:flex;flex-direction:column">{inner}</div>
<div style="position:relative;display:flex;justify-content:space-between;align-items:center;margin-top:26px">
<div style="display:flex;align-items:center;gap:14px;font-family:InterW;font-weight:700;font-size:26px;color:{INK}"><span style="width:44px;height:44px;border-radius:12px;background:{acc};color:{BG1};display:grid;place-items:center;font-family:MontX;font-weight:900;font-size:20px">SF</span>SystemForge</div>
<div style="display:flex;gap:8px">{dots}</div></div></div></body></html>'''


def slide_html(s, c, n, total):
    t = s['type']
    if t == 'cover':
        peek = ''
        if s.get('shot'):
            peek = f'<div style="flex:1;display:flex;align-items:center;justify-content:center;margin-top:30px">{card(s["shot"], 940, 430, -3)}</div>'
        inner = f'''<div style="font-family:InterW;font-weight:700;font-size:28px;letter-spacing:6px;color:var(--acc)">{s.get('kicker', '')}</div>
<h1 class="h" style="margin-top:28px;font-size:{s.get('size', 118)}px;line-height:0.98">{s['title']}</h1>
<p class="t" style="margin-top:30px;font-size:42px;line-height:1.3;color:{INK};opacity:.85">{s.get('sub', '')}</p>
<div style="margin-top:34px;display:inline-flex;align-self:flex-start;align-items:center;gap:12px;padding:16px 30px;border-radius:999px;background:var(--acc);color:{BG1};font-family:MontX;font-weight:800;font-size:30px">Swipe →</div>
{peek}'''
    elif t == 'tip':
        shot = f'<div style="flex:1;display:flex;align-items:center;justify-content:center;padding-top:20px">{card(s["shot"], 940, s.get("max_h", 560))}</div>' if s.get('shot') else ''
        box = ''
        if s.get('box'):
            box = (f'<div style="margin-top:40px;border:3px solid var(--acc);border-radius:28px;padding:34px 40px">'
                   f'<div style="font-family:InterW;font-weight:700;font-size:24px;letter-spacing:4px;color:var(--acc)">{s.get("label", "EXAMPLE")}</div>'
                   f'<div class="h" style="margin-top:16px;font-size:52px;line-height:1.22;letter-spacing:-1px">{s["box"]}</div></div>')
        big = not s.get('shot')
        head = f'''<div style="font-family:MontX;font-weight:900;font-size:{56 if big else 40}px;color:{BG1};background:var(--acc);align-self:flex-start;padding:6px 24px;border-radius:14px">{s['num']}</div>
<h2 class="h" style="margin-top:28px;font-size:{s.get('size', 92 if big else 72)}px;line-height:1.02">{s['title']}</h2>
<p class="t" style="margin-top:28px;font-size:{44 if big else 38}px;line-height:1.38">{s['text']}</p>{box}'''
        inner = f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center">{head}</div>' if big else head + shot
    else:  # cta
        bullets = ''.join(f'<div style="display:flex;gap:18px;align-items:flex-start"><span style="color:var(--acc);font-family:MontX;font-weight:900">✓</span><span>{b}</span></div>' for b in s.get('bullets', []))
        inner = f'''<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:30px">
<div style="font-family:InterW;font-weight:700;font-size:28px;letter-spacing:6px;color:var(--acc)">WANT THIS DONE FOR YOU?</div>
<h1 class="h" style="font-size:96px;line-height:1.0">{PRODUCTS[c['p']]}</h1>
<div class="t" style="font-size:36px;line-height:1.45;color:{INK};display:flex;flex-direction:column;gap:14px">{bullets}</div>
<div style="margin-top:20px;align-self:flex-start;background:var(--acc);color:{BG1};border-radius:999px;padding:26px 56px;font-family:MontX;font-weight:900;font-size:42px">Link in bio</div>
<div class="t" style="font-size:32px;color:{INK};opacity:.8">🔖 Save this · ↗ Send it to {s.get('send', 'a friend who needs it')}</div></div>'''
    return page(c, inner, n, total)


def render(html, out):
    f = os.path.join(TMP, 'slide.html')
    open(f, 'w').write(html)
    tmp = f + '.png'
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=1', f'--window-size={W},{H + 300}', f'--screenshot={tmp}', 'file://' + f],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    Image.open(tmp).crop((0, 0, W, H)).convert('RGB').save(out, quality=94, subsampling=0)


def main():
    spec2 = json.load(open(os.path.join(ROOT, 'generator', 'carousels2-spec.json')))['carousels']
    only = sys.argv[1:]
    for c in spec2:
        if only and c['id'] not in only:
            continue
        d = os.path.join(ROOT, 'carousels', c['id'])
        os.makedirs(d, exist_ok=True)
        for n, s in enumerate(c['slides']):
            render(slide_html(s, c, n, len(c['slides'])), os.path.join(d, f'{n + 1}.jpg'))
        print('ok', c['id'])
    old = json.load(open(os.path.join(ROOT, 'generator', 'carousels-spec.json')))['carousels']
    allc = [{'id': c['id'], 'p': c['p'], 'slides': len(c['slides']), 'caption': c['caption']} for c in spec2 + old]
    json.dump({'carousels': allc}, open(os.path.join(ROOT, 'carousels.json'), 'w'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
