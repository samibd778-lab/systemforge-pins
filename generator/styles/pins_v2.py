"""SystemForge pins, style 2026-10 (built from generator/pins-v2-spec.json).

For every spec it writes:
  <repo>/<id>.png      1000x1500  Pinterest: headline + laptop + numbered callouts with arrows + pills
  <repo>/ig/<id>.jpg   1080x1350  Instagram/Facebook: the same screen tilted like a photo (no text)

Usage: python3 generator/styles/pins_v2.py [id-prefix ...]
Then:  python3 generator/gen.py --json   (rebuilds pins.json with old + new pins mixed)
"""
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
FONTS = os.path.join(ROOT, 'generator', 'remotion', 'public')
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

INK, MUT, ACC, SAGE, CREAM, PAP, CLAY, SAGEL = '#2E2A25', '#5C554C', '#D9A07B', '#7A8B6F', '#F6F1E9', '#FFFDF9', '#EFDCCB', '#E3E8DC'
PRODUCTS = {'fco': 'Freelancer Client OS', 'ccs': 'Content Creator Studio'}
PILLS = ['Instant access', 'Duplicate in 1 click', 'Pay once']

FONT_CSS = f'''@font-face{{font-family:Fraunces;src:url(file://{FONTS}/fraunces600.woff2);font-weight:600}}
@font-face{{font-family:InterW;src:url(file://{FONTS}/inter500.woff2);font-weight:500}}
@font-face{{font-family:InterW;src:url(file://{FONTS}/inter700.woff2);font-weight:700}}'''


def crop_image(sp, tmpdir):
    """Cut the crop box out of the screenshot (areas outside the screenshot become white)."""
    im = Image.open(os.path.join(ROOT, sp['shot'])).convert('RGB')
    x0, y0, x1, y1 = sp['crop']
    canvas = Image.new('RGB', (x1 - x0, y1 - y0), 'white')
    canvas.paste(im, (-x0, -y0))
    path = os.path.join(tmpdir, sp['id'] + '-crop.png')
    canvas.save(path)
    return path, canvas.size


def shoot(html, w, h, out, tmpdir, name):
    src = os.path.join(tmpdir, name + '.html')
    open(src, 'w').write(html)
    png = os.path.join(tmpdir, name + '.png')
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=2', f'--window-size={w},{h + 200}', f'--screenshot={png}', 'file://' + src],
                   check=True, capture_output=True)
    return Image.open(png).crop((0, 0, w * 2, h * 2))


# ---------- Pinterest: laptop + callouts ----------
PW, PH = 1000, 1500
SX, SY, SW = 90, 560, 820


def pin_html(sp, crop_path, size):
    cw, ch = size
    k = SW / cw
    sh = ch * k

    def pt(x, y):
        return SX + (x - sp['crop'][0]) * k, SY + (y - sp['crop'][1]) * k

    slots = [(24, 1112, 'up'), (646, 1112, 'up'), (646, 452, 'down')]
    arrows, labels = [], []
    for i, (text, tx, ty) in enumerate(sp['callouts'][:3]):
        lx, ly, d = slots[i]
        ex, ey = pt(tx, ty)
        sx, sy = lx + 165, (ly if d == 'up' else ly + 74)
        # stop the line at the edge of the ring so it never runs through the text
        dx, dy = ex - sx, 0.0
        d = max(abs(dx), 1.0)
        fx, fy = ex - (dx / d) * 24, ey
        if abs(dx) < 30:
            fx, fy = ex, ey + (24 if sy > ey else -24)
        arrows.append(f'<path d="M{sx},{sy} Q{sx},{ey} {fx},{fy}" fill="none" stroke="{SAGE}" '
                      f'stroke-width="4" stroke-linecap="round" stroke-dasharray="1 9"/>'
                      f'<circle cx="{ex}" cy="{ey}" r="19" fill="rgba(217,160,123,.12)" stroke="{ACC}" stroke-width="4"/>')
        labels.append(f'<div class="co" style="left:{lx}px;top:{ly}px"><span class="n">{i + 1}</span><span>{text}</span></div>')
    a, hl, b = sp['title']
    title = f'{a} <em>{hl}</em>' + (f'<br>{b}' if b else '')
    if len(a) + len(hl) > 22:
        title = f'{a}<br><em>{hl}</em>' + (f' {b}' if b and len(hl) + len(b) < 18 else (f'<br>{b}' if b else ''))
    pills = ''.join(f'<div class="pill">{p}</div>' for p in PILLS)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{FONT_CSS}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{PW}px;height:{PH}px;background:{CREAM};position:relative;overflow:hidden;font-family:InterW}}
.blob{{position:absolute;border-radius:50%}}
.kick{{position:absolute;top:56px;left:0;right:0;text-align:center}}
.kick span{{display:inline-flex;align-items:center;gap:10px;background:{PAP};border-radius:40px;padding:12px 24px;font-weight:700;font-size:21px;letter-spacing:1.6px;color:{INK};box-shadow:0 6px 20px rgba(46,42,37,.08)}}
.kick i{{width:28px;height:28px;border-radius:50%;background:{SAGE};color:{PAP};font-style:italic;font-family:Fraunces;font-size:14px;display:flex;align-items:center;justify-content:center}}
.top{{position:absolute;top:116px;left:36px;right:36px;height:322px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
h1{{font-family:Fraunces;font-weight:600;font-size:76px;line-height:1.04;color:{INK};letter-spacing:-2.4px}}
h1 em{{font-style:normal;background:linear-gradient(transparent 12%,{CLAY} 12%,{CLAY} 92%,transparent 92%);padding:0 12px;border-radius:14px;color:#9A5F3C}}
.sub{{margin-top:18px;font-size:27px;color:{MUT};line-height:1.3}}
.sub b{{color:{INK}}}
.lap{{position:absolute;left:{SX - 24}px;top:{SY - 24}px;width:{SW + 48}px;height:{sh + 48}px;background:#1F1D1A;border-radius:24px;box-shadow:0 40px 80px rgba(46,42,37,.25)}}
.scr{{position:absolute;left:{SX}px;top:{SY}px;width:{SW}px;height:{sh}px;background:#fff url("file://{crop_path}") 0 0/100% 100%;border-radius:6px}}
.base{{position:absolute;left:{SX - 100}px;top:{SY + sh + 24}px;width:{SW + 200}px;height:28px;background:linear-gradient(#D8D2C8,#B9B2A6);border-radius:0 0 32px 32px}}
.base:after{{content:"";position:absolute;left:50%;top:0;width:140px;height:11px;margin-left:-70px;background:#A9A196;border-radius:0 0 11px 11px}}
svg{{position:absolute;left:0;top:0}}
.co{{position:absolute;width:330px;min-height:74px;background:{PAP};border-radius:20px;padding:14px 18px 14px 14px;font-weight:700;font-size:23px;line-height:1.2;color:{INK};display:flex;gap:12px;align-items:center;box-shadow:0 12px 28px rgba(46,42,37,.14)}}
.n{{flex:none;width:38px;height:38px;border-radius:50%;background:{SAGE};color:{PAP};font-size:19px;display:flex;align-items:center;justify-content:center}}
.pills{{position:absolute;top:1292px;left:0;right:0;display:flex;justify-content:center;gap:14px}}
.pill{{background:{PAP};border-radius:40px;padding:13px 22px;font-weight:700;font-size:21px;color:{INK};box-shadow:0 6px 18px rgba(46,42,37,.08)}}
.foot{{position:absolute;bottom:56px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:14px;font-weight:700;font-size:26px;color:{INK}}}
.foot i{{width:46px;height:46px;border-radius:50%;background:{SAGE};color:{PAP};font-style:italic;font-family:Fraunces;font-size:21px;display:flex;align-items:center;justify-content:center}}
.foot span{{color:{MUT};font-weight:500}}
</style></head><body>
<div class="blob" style="width:600px;height:600px;background:{SAGEL};left:-250px;top:-230px"></div>
<div class="blob" style="width:700px;height:700px;background:{CLAY};right:-330px;bottom:-300px;opacity:.8"></div>
<div class="kick"><span><i>SF</i>{sp['kicker']}</span></div>
<div class="top"><h1>{title}</h1><div class="sub">{sp['sub']}</div></div>
<div class="lap"></div><div class="scr"></div><div class="base"></div>
<svg width="{PW}" height="{PH}">{''.join(arrows)}</svg>
{''.join(labels)}
<div class="pills">{pills}</div>
<div class="foot"><i>SF</i>SystemForge <span>· {PRODUCTS[sp['p']]}</span></div>
</body></html>'''


# ---------- Instagram / Facebook: tilted photo ----------
IW, IH = 1080, 1350


def photo_html(crop_path, size):
    cw, ch = size
    scr_w = 1650
    scr_h = int(scr_w * ch / cw)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0}}
body{{width:{IW}px;height:{IH}px;overflow:hidden;position:relative;background:radial-gradient(ellipse at 70% 20%,#F3E6D6 0%,#D9C3A8 45%,#9C8468 100%)}}
.stage{{position:absolute;inset:0;perspective:1400px;perspective-origin:30% 40%}}
.lap{{position:absolute;left:-140px;top:{max(120, 560 - scr_h // 3)}px;width:{scr_w + 60}px;transform-origin:0 50%;transform:rotateY(24deg) rotateX(9deg) rotateZ(-3deg);transform-style:preserve-3d}}
.bez{{background:#151413;border-radius:28px;padding:30px;box-shadow:0 60px 120px rgba(40,25,10,.45)}}
.scr{{width:{scr_w}px;height:{scr_h}px;background:#fff url("file://{crop_path}") 0 0/100% 100%;border-radius:6px;position:relative;overflow:hidden}}
.glare{{position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,0) 35%,rgba(255,255,255,.16) 48%,rgba(255,255,255,0) 62%)}}
.kb{{height:240px;margin:0 -40px;border-radius:0 0 40px 40px;transform:rotateX(78deg);transform-origin:50% 0;
  background-image:repeating-linear-gradient(90deg,#33302D 0 62px,#1A1918 62px 70px),repeating-linear-gradient(0deg,#1A1918 0 8px,transparent 8px 62px)}}
.dof{{position:absolute;inset:0;backdrop-filter:blur(5px);-webkit-mask-image:linear-gradient(100deg,transparent 0%,transparent 45%,#000 85%)}}
.dof2{{position:absolute;inset:0;backdrop-filter:blur(4px);-webkit-mask-image:linear-gradient(180deg,transparent 0%,transparent 72%,#000 100%)}}
.warm{{position:absolute;inset:0;background:radial-gradient(ellipse at 25% 35%,rgba(255,236,210,0) 0%,rgba(80,50,20,.28) 100%);mix-blend-mode:multiply}}
</style></head><body>
<div class="stage"><div class="lap"><div class="bez"><div class="scr"><div class="glare"></div></div></div><div class="kb"></div></div></div>
<div class="dof"></div><div class="dof2"></div><div class="warm"></div>
</body></html>'''


def build(sp):
    with tempfile.TemporaryDirectory() as tmp:
        crop_path, size = crop_image(sp, tmp)
        pin = shoot(pin_html(sp, crop_path, size), PW, PH, None, tmp, 'pin')
        pin.resize((PW, PH), Image.LANCZOS).convert('RGB').save(os.path.join(ROOT, sp['id'] + '.png'), optimize=True)
        ig = shoot(photo_html(crop_path, size), IW, IH, None, tmp, 'ig')
        os.makedirs(os.path.join(ROOT, 'ig'), exist_ok=True)
        ig.resize((IW, IH), Image.LANCZOS).convert('RGB').save(os.path.join(ROOT, 'ig', sp['id'] + '.jpg'), quality=93, subsampling=0)


if __name__ == '__main__':
    specs = json.load(open(os.path.join(ROOT, 'generator', 'pins-v2-spec.json')))['pins']
    only = sys.argv[1:]
    for sp in specs:
        if not only or any(sp['id'].startswith(o) for o in only):
            build(sp)
            print('ok', sp['id'])
