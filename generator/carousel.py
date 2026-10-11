"""Instagram carousels (1080x1350 JPEG slides) from real Notion screenshots.

Spec: generator/carousels-spec.json -> carousels/<id>/<n>.jpg and carousels.json (read by n8n).
"""
import json, os, sys, subprocess, tempfile
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen
from gen import S, SER, PAP, SAGE, BR, INK, MUT, THEMES, PRODUCTS, crop_card, logo

ROOT = gen.ROOT
W, H = 1080, 1350


def page(theme, inner, n, total):
    bg, c1, c2 = THEMES[theme]
    dots = ''.join(f'<span style="width:{26 if i == n else 10}px;height:10px;border-radius:5px;background:{INK if i == n else "#CFC6B8"}"></span>' for i in range(total))
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0}}*{{box-sizing:border-box}}</style></head><body>
<div style="position:relative;overflow:hidden;width:{W}px;height:{H}px;background:{bg};color:{INK};{S};padding:80px 76px 70px;display:flex;flex-direction:column">
<div style="position:absolute;left:-200px;top:-220px;width:620px;height:620px;border-radius:50%;background:{c1}"></div>
<div style="position:absolute;right:-240px;bottom:-260px;width:740px;height:740px;border-radius:50%;background:{c2}"></div>
<div style="position:relative;flex:1;display:flex;flex-direction:column">{inner}</div>
<div style="position:relative;display:flex;justify-content:space-between;align-items:center;margin-top:30px">{logo()}<div style="display:flex;gap:8px">{dots}</div></div></div></body></html>'''


def slide_html(s, c, n, total):
    t = s['type']
    if t == 'cover':
        inner = f'''<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:34px">
<div style="font-size:26px;font-weight:700;letter-spacing:5px;color:{SAGE}">{s.get('kicker', '')}</div>
<h1 style="margin:0;{SER};font-size:{s.get('size', 112)}px;line-height:1.02;font-weight:700;letter-spacing:-3px">{s['title']}</h1>
<div style="{SER};font-style:italic;font-size:46px;color:{BR}">{s.get('sub', '')}</div>
<div style="margin-top:30px;font-size:30px;font-weight:700;color:{MUT}">Swipe →</div></div>'''
    elif t == 'tip':
        card = crop_card(None, None, width=880, max_h=640, parts=[(a, b) for a, b in s['parts']], direction=s.get('dir', 'h'))
        inner = f'''<div style="display:flex;align-items:baseline;gap:22px"><span style="{SER};font-size:84px;font-weight:700;color:{BR}">{s['num']}</span>
<h2 style="margin:0;{SER};font-size:62px;line-height:1.08;font-weight:700;letter-spacing:-1px">{s['title']}</h2></div>
<p style="margin:22px 0 0;font-size:34px;line-height:1.4;color:{MUT}">{s['text']}</p>
<div style="flex:1;display:flex;align-items:center;justify-content:center">{card}</div>'''
    else:  # cta
        inner = f'''<div style="flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;gap:34px">
<div style="font-size:26px;font-weight:700;letter-spacing:5px;color:{SAGE}">NOTION TEMPLATE</div>
<h1 style="margin:0;{SER};font-size:104px;line-height:1.04;font-weight:700;letter-spacing:-2px">{PRODUCTS[c['p']]}</h1>
<div style="{SER};font-style:italic;font-size:46px;color:{BR}">{s.get('sub', 'example data + a 5-minute start guide')}</div>
<div style="margin-top:20px;background:{INK};color:{PAP};border-radius:999px;padding:30px 64px;font-size:42px;font-weight:700">Link in bio</div>
<div style="font-size:30px;color:{MUT}">Save this post for later 🔖</div></div>'''
    return page(c['theme'], inner, n, total)


def render(html, out):
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f:
        f.write(html)
    tmp = f.name + '.png'
    subprocess.run([gen.CHROME, '--headless=new', '--no-sandbox', '--hide-scrollbars', '--allow-file-access-from-files',
                    f'--window-size={W},{H + 300}', f'--screenshot={tmp}', 'file://' + f.name],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    Image.open(tmp).crop((0, 0, W, H)).convert('RGB').save(out, quality=90)
    os.remove(f.name); os.remove(tmp)


def main():
    spec = json.load(open(os.path.join(ROOT, 'generator', 'carousels-spec.json')))['carousels']
    only = sys.argv[1:]
    for c in spec:
        if only and c['id'] not in only:
            continue
        d = os.path.join(ROOT, 'carousels', c['id'])
        os.makedirs(d, exist_ok=True)
        for n, s in enumerate(c['slides']):
            render(slide_html(s, c, n, len(c['slides'])), os.path.join(d, f'{n + 1}.jpg'))
        print('ok', c['id'])
    json.dump({'carousels': [{'id': c['id'], 'p': c['p'], 'slides': len(c['slides']), 'caption': c['caption']} for c in spec]},
              open(os.path.join(ROOT, 'carousels.json'), 'w'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
