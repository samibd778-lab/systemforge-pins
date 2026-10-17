"""SystemForge pin generator.

Builds every pin listed in generator/pins-spec.json from the real Notion
screenshots in shots/, writes <id>.png (1000x1500) to the repo root and
rewrites pins.json (the list the n8n workflows read).

Usage:  python3 generator/gen.py            # all pins
        python3 generator/gen.py ccs-1 fco-2  # only ids starting with these
"""
import json, os, subprocess, sys, tempfile
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(ROOT, 'shots')
CHROME = os.environ.get('CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')

# ---- SystemForge warm identity ----
S = "font-family:'Helvetica Neue',Helvetica,Arial,sans-serif"
SER = "font-family:Georgia,'Times New Roman',serif"
CREAM, PAP, SAGE, SAGEL, CLAY = '#F6F1E9', '#FFFDF9', '#7A8B6F', '#E3E8DC', '#EFDCCB'
ACC, BR, INK, MUT = '#D9A07B', '#B07A57', '#2E2A25', '#5C554C'
THEMES = {  # background, top blob, bottom blob
    'sage': (SAGEL, CREAM, CLAY),
    'clay': (CLAY, CREAM, SAGEL),
    'cream': (CREAM, SAGEL, CLAY),
}
PRODUCTS = {'fco': 'Freelancer Client OS', 'ccs': 'Content Creator Studio', 'prop': 'Proposal Tracker', 'deal': 'Brand Deal Tracker'}
W, H = 1000, 1500


def shot(name):
    return 'file://' + os.path.join(SHOTS, name + '.png')


def shot_size(name):
    return Image.open(os.path.join(SHOTS, name + '.png')).size


def logo():
    return (f'<div style="display:flex;align-items:center;gap:14px"><div style="width:56px;height:56px;border-radius:50%;'
            f'background:{SAGE};color:{PAP};display:flex;align-items:center;justify-content:center;{SER};font-style:italic;'
            f'font-weight:700;font-size:24px">SF</div><div style="{S};font-size:22px;font-weight:700;color:{INK}">SystemForge</div></div>')


# ---- devices ----
def laptop(name, width=860, screen_h=470, show_w=1500):
    """Laptop showing the top-left of a wide Notion screenshot (show_w px of it across the screen)."""
    sw, _ = shot_size(name)
    scale = (width - 36) / min(show_w, sw)
    bg_w = int(sw * scale)
    return (f'<div style="width:{width}px;margin:0 auto">'
            f'<div style="background:#1F1D1A;border-radius:26px 26px 0 0;padding:18px 18px 22px">'
            f'<div style="height:{screen_h}px;border-radius:8px;background:#fff url(\'{shot(name)}\') no-repeat 0 0/{bg_w}px auto"></div></div>'
            f'<div style="height:26px;margin:0 -40px;background:linear-gradient(#D8D2C8,#BDB6AA);border-radius:0 0 30px 30px"></div></div>')


def phone(name, width=290, top=70, rotate=0):
    """Phone frame with a Notion mobile screenshot (status bar cropped)."""
    sw, sh = shot_size(name)
    inner = width - 24
    scale = inner / sw
    height = int(inner * 2.05)
    return (f'<div style="width:{width}px;padding:12px;background:#1F1D1A;border-radius:46px;box-shadow:0 30px 60px rgba(46,42,37,.25);transform:rotate({rotate}deg)">'
            f'<div style="height:{height}px;border-radius:34px;background:#fff url(\'{shot(name)}\') no-repeat 0 -{int(top*scale)}px/{inner}px auto"></div></div>')


CACHE = os.path.join(ROOT, 'generator', '.cache')


def compose(parts, direction='h'):
    """Glue crops from one or more screenshots into one image (only the columns that matter)."""
    os.makedirs(CACHE, exist_ok=True)
    key = ('_'.join(f"{n}-{'-'.join(map(str, b))}" for n, b in parts) + direction)[:180]
    path = os.path.join(CACHE, key + '.png')
    if not os.path.exists(path):
        ims = [Image.open(os.path.join(SHOTS, n + '.png')).convert('RGB').crop(tuple(b)) for n, b in parts]
        gap = 18
        if direction == 'h':
            h = max(i.height for i in ims)
            out = Image.new('RGB', (sum(i.width for i in ims) + gap * (len(ims) - 1), h), 'white')
            x = 0
            for i in ims:
                out.paste(i, (x, 0)); x += i.width + gap
        else:
            w = max(i.width for i in ims)
            out = Image.new('RGB', (w, sum(i.height for i in ims) + gap * (len(ims) - 1)), 'white')
            y = 0
            for i in ims:
                out.paste(i, (0, y)); y += i.height + gap
        out.save(path)
    return path


def crop_card(name, box, width=860, radius=24, max_h=760, parts=None, direction='h'):
    """A zoomed crop shown as a floating card. Either one box of one screenshot, or several parts glued together."""
    path = compose(parts or [(name, box)], direction)
    iw, ih = Image.open(path).size
    scale = min(width / iw, max_h / ih)
    w, h = int(iw * scale), int(ih * scale)
    pad = 26
    return (f'<div style="width:{w + 2*pad}px;margin:0 auto;border-radius:{radius}px;background:#fff;padding:{pad}px;'
            f'box-shadow:0 26px 60px rgba(46,42,37,.16);border:1px solid #EDE6DA">'
            f'<div style="width:{w}px;height:{h}px;background:url(\'file://{path}\') no-repeat 0 0/{w}px {h}px"></div></div>')


# ---- layouts ----
def visual(spec):
    L = spec['layout']
    s = spec['shots']
    if L == 'laptop':
        return f'<div style="width:100%">{laptop(s[0], show_w=spec.get("show_w", 1500))}</div>'
    if L == 'combo':  # laptop + phone
        return (f'<div style="position:relative;width:100%;height:760px">'
                f'<div style="position:absolute;left:-10px;top:40px">{laptop(s[0], width=760, screen_h=430, show_w=spec.get("show_w", 1500))}</div>'
                f'<div style="position:absolute;right:-6px;top:150px">{phone(s[1], width=250)}</div></div>')
    if L == 'phones':  # two phones
        return (f'<div style="display:flex;justify-content:center;gap:40px;align-items:center;width:100%">'
                f'{phone(s[0], rotate=-4)}<div style="margin-top:80px">{phone(s[1], rotate=4)}</div></div>')
    if L == 'zoom':
        parts = spec.get('parts')
        card = crop_card(s[0] if s else None, spec.get('box'), width=808,
                         parts=[(n, b) for n, b in parts] if parts else None, direction=spec.get('dir', 'h'))
        return f'<div style="width:100%">{card}</div>'
    if L == 'stack':  # three pages, overlapping
        cards = ''
        for i, n in enumerate(s[:3]):
            sw, _ = shot_size(n)
            box = (0, 0, min(sw, 1500), 520)
            cards += (f'<div style="position:absolute;left:{i*50}px;top:{i*190}px;transform:rotate({[-3,1,-1][i]}deg)">'
                      f'{crop_card(n, box, width=720, radius=20)}</div>')
        return f'<div style="position:relative;width:880px;height:760px;margin:0 auto">{cards}</div>'
    raise ValueError(L)


def pin_html(spec):
    bg, c1, c2 = THEMES[spec.get('theme', 'sage')]
    chips = ''.join(f'<span style="background:{PAP};border-radius:999px;padding:14px 26px;font-size:26px;font-weight:700;'
                    f'color:{INK};box-shadow:0 6px 16px rgba(46,42,37,.08)">{c}</span>' for c in spec.get('chips', []))
    size = spec.get('title_size', 104)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0}}*{{box-sizing:border-box}}</style></head><body>
<div style="position:relative;overflow:hidden;width:{W}px;height:{H}px;background:{bg};color:{INK};{S};padding:70px 70px 60px;display:flex;flex-direction:column;gap:28px">
<div style="position:absolute;left:-200px;top:-220px;width:640px;height:640px;border-radius:50%;background:{c1}"></div>
<div style="position:absolute;right:-240px;bottom:-260px;width:760px;height:760px;border-radius:50%;background:{c2}"></div>
<div style="position:relative;text-align:center;display:flex;flex-direction:column;gap:16px;align-items:center">
<div style="font-size:22px;font-weight:700;letter-spacing:4px;color:{SAGE}">{spec.get('kicker', 'NOTION TEMPLATE')}</div>
<h1 style="margin:0;{SER};font-size:{size}px;line-height:1.02;font-weight:700;letter-spacing:-2px">{spec['title']}</h1>
<div style="{SER};font-style:italic;font-size:44px;color:{BR}">{spec.get('sub', '')}</div></div>
<div style="position:relative;flex:1;display:flex;align-items:center">{visual(spec)}</div>
<div style="position:relative;display:flex;gap:14px;justify-content:center;flex-wrap:wrap">{chips}</div>
<div style="position:relative;display:flex;justify-content:space-between;align-items:center">{logo()}
<span style="font-size:24px;font-weight:600;color:{MUT}">{PRODUCTS[spec['p']]}</span></div></div></body></html>'''


def render(spec, out_dir=ROOT):
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f:
        f.write(pin_html(spec))
    tmp_png = f.name + '.png'
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--window-size=1000,1800', f'--screenshot={tmp_png}', 'file://' + f.name],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    Image.open(tmp_png).crop((0, 0, W, H)).convert('RGB').save(os.path.join(out_dir, spec['id'] + '.png'), optimize=True)
    os.remove(f.name); os.remove(tmp_png)


def main():
    specs = json.load(open(os.path.join(ROOT, 'generator', 'pins-spec.json')))['pins']
    only = sys.argv[1:]
    for sp in specs:
        if not only or any(sp['id'].startswith(o) for o in only):
            render(sp)
            print('ok', sp['id'])
    # pins.json = posting order read by n8n (id, product, what the image shows)
    old = [{'id': sp['id'], 'p': sp['p'], 'angle': sp['angle']} for sp in specs]
    # new-style pins (generator/styles/pins_v2.py) are mixed in from 'insert_at': new, old, new, old...
    v2 = json.load(open(os.path.join(ROOT, 'generator', 'pins-v2-spec.json')))
    new = [{'id': sp['id'], 'p': sp['p'], 'angle': sp['angle']} for sp in v2['pins'] if not sp.get('launch')]
    launch = [{'id': sp['id'], 'p': sp['p'], 'angle': sp['angle']} for sp in v2['pins'] if sp.get('launch')]
    # interleave launch products (prop, deal, prop, deal...) in spec order
    groups = {}
    for x in launch: groups.setdefault(x['p'], []).append(x)
    launch = []
    while any(groups.values()):
        for g in groups.values():
            if g: launch.append(g.pop(0))
    at = v2.get('insert_at', len(old))
    rest, mixed = old[at:], old[:at]
    while new or rest:
        if new: mixed.append(new.pop(0))
        if rest: mixed.append(rest.pop(0))
    # value-first tip pins (generator/styles/tips.py): from 'insert_at', one tip every 'every' slots
    tp = json.load(open(os.path.join(ROOT, 'generator', 'tips-spec.json')))
    tips = [{'id': sp['id'], 'p': sp['p'], 'kind': 'tip', 'angle': ' '.join(x for x in sp['title'] if x),
             'tips': [f'{a}: {b}' for a, b in sp['tips']]} for sp in tp['pins']]
    pos = tp.get('insert_at', len(mixed))
    for t in tips:
        pos = min(pos, len(mixed))
        mixed.insert(pos, t)
        pos += tp.get('every', 3)
    # new products (launch=true in pins-v2-spec.json): from 'launch_at', one every 'launch_every' slots
    pos = v2.get('launch_at', len(mixed))
    for t in launch:
        pos = min(pos, len(mixed))
        mixed.insert(pos, t)
        pos += v2.get('launch_every', 3)
    json.dump({'pins': mixed}, open(os.path.join(ROOT, 'pins.json'), 'w'), indent=1, ensure_ascii=False)
    print(len(mixed), 'pins in pins.json')


if __name__ == '__main__':
    main()
