"""SystemForge reels from PHONE screenshots (1080x2400): sharp, native vertical.

Each scene: big hook text on top, a phone that shows the real screenshot scrolling slowly,
then an end card. Our own music (music2, different style per video).

Spec (generator/phone-reels-spec.json):
{"videos": [{"id": "p01-...", "p": "fco", "theme": "cream",
  "scenes": [{"text": "Late invoices<br>flag themselves", "shot": "phone/fco-invoices.jpg", "top": 240, "bottom": 2110, "dur": 3.4}],
  "end": "Get paid on time"}]}

Usage: python3 generator/phone_reel.py [ids...] [--out DIR]
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen, reels, music2

ROOT = gen.ROOT
W, H, FPS, XF = 1080, 1920, 30, 0.35
FONTS = os.path.join(ROOT, 'generator', 'remotion', 'public')
INTER = (f"@font-face{{font-family:I;font-weight:500;src:url(file://{FONTS}/inter500.woff2)}}"
         f"@font-face{{font-family:I;font-weight:700;src:url(file://{FONTS}/inter700.woff2)}}")
# phone geometry
PX, PY, PW, PH, BEZ, RAD = 150, 560, 780, 1216, 16, 70
SX, SY, SW, SH = PX + BEZ, PY + BEZ, PW - 2 * BEZ, PH - 2 * BEZ


def page(theme, inner):
    bg, c1, c2 = gen.THEMES[theme]
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{INTER}body{{margin:0}}*{{box-sizing:border-box}}</style></head><body>
<div style="position:relative;overflow:hidden;width:{W}px;height:{H}px;background:{bg};color:{gen.INK};font-family:I">
<div style="position:absolute;left:-260px;top:-300px;width:760px;height:760px;border-radius:50%;background:{c1}"></div>
<div style="position:absolute;right:-300px;bottom:-320px;width:860px;height:860px;border-radius:50%;background:{c2}"></div>
{inner}</div></body></html>'''


def scene_bg(text, theme, product):
    return page(theme, f'''
<div style="position:absolute;left:60px;right:60px;top:120px;height:{PY - 160}px;display:flex;align-items:center;justify-content:center;text-align:center">
<div style="font-size:84px;line-height:1.08;font-weight:700;letter-spacing:-2.5px">{text}</div></div>
<div style="position:absolute;left:{PX}px;top:{PY}px;width:{PW}px;height:{PH}px;border-radius:{RAD}px;background:#1d1b19;
box-shadow:0 40px 90px rgba(46,42,37,.28)"></div>
<div style="position:absolute;left:0;right:0;bottom:46px;display:flex;justify-content:center;gap:18px;align-items:center;font-size:30px;font-weight:700;color:{gen.MUT}">
SystemForge <span style="opacity:.5">·</span> {gen.PRODUCTS[product]}</div>''')


def end_bg(line, theme, product):
    return page(theme, f'''
<div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;gap:46px;padding:0 70px">
<div style="width:150px;height:150px;border-radius:50%;background:{gen.SAGE};color:{gen.PAP};display:flex;align-items:center;justify-content:center;font-size:64px;font-weight:700">SF</div>
<div style="font-size:92px;line-height:1.06;font-weight:700;letter-spacing:-3px">{gen.PRODUCTS[product].replace(" OS", "&nbsp;OS").replace("Creator Studio","Creator<br>Studio")}</div>
<div style="font-size:50px;font-weight:500;color:{gen.BR}">{line}</div>
<div style="margin-top:24px;background:{gen.INK};color:{gen.PAP};border-radius:999px;padding:30px 66px;font-size:46px;font-weight:700">Link in bio</div></div>''')


def mask(path):
    m = Image.new('L', (SW, SH), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, SW - 1, SH - 1), RAD - BEZ, fill=255)
    m.save(path)


def build(v, outdir):
    work = tempfile.mkdtemp()
    mk = os.path.join(work, 'mask.png'); mask(mk)
    args, f, durs = ['ffmpeg', '-y', '-loglevel', 'error'], [], []
    n = 0
    for i, sc in enumerate(v['scenes']):
        d = sc.get('dur', 3.4)
        bg = os.path.join(work, f'bg{i}.png')
        reels.render_png(scene_bg(sc['text'], sc.get('theme', v.get('theme', 'cream')), v['p']), bg)
        src = os.path.join(ROOT, sc['shot'])
        im = Image.open(src)
        top, bot = sc.get('top', 240), sc.get('bottom', 2110)
        cw = im.width
        ch = bot - top
        scaled_h = int(ch * SW / cw) // 2 * 2
        scroll = max(0, scaled_h - SH)
        args += ['-loop', '1', '-t', f'{d + XF:.2f}', '-i', bg,
                 '-loop', '1', '-t', f'{d + XF:.2f}', '-i', src,
                 '-loop', '1', '-t', f'{d + XF:.2f}', '-i', mk]
        b, s, m = n, n + 1, n + 2
        n += 3
        # screenshot: crop content, scale to screen width (downscale = sharp), scroll from top to bottom
        f.append(f"[{s}:v]crop={cw}:{ch}:0:{top},scale={SW}:{scaled_h}:flags=lanczos,"
                 f"crop={SW}:{SH}:0:'min({scroll},{scroll}*t/{d:.2f})',format=rgba[sc{i}]")
        f.append(f"[{m}:v]format=gray[m{i}];[sc{i}][m{i}]alphamerge[sm{i}]")
        f.append(f"[{b}:v][sm{i}]overlay={SX}:{SY},fps={FPS},format=yuv420p,setsar=1[v{i}]")
        durs.append(d)
    endp = os.path.join(work, 'end.png')
    reels.render_png(end_bg(v.get('end', 'a calm Notion template'), v.get('theme', 'cream'), v['p']), endp)
    args += ['-loop', '1', '-t', '3.0', '-i', endp]
    f.append(f"[{n}:v]fps={FPS},format=yuv420p,setsar=1[v{len(durs)}]")
    durs.append(2.7)
    n += 1
    last, off = 'v0', 0.0
    for i in range(1, len(durs)):
        off += durs[i - 1]
        f.append(f'[{last}][v{i}]xfade=transition=fade:duration={XF}:offset={off:.2f}[x{i}]')
        last = f'x{i}'
    total = sum(durs) + XF
    wav = os.path.join(work, 'm.wav')
    style = music2.write_for(v['id'], total + 0.5, wav)
    args += ['-i', wav, '-filter_complex', ';'.join(f), '-map', f'[{last}]', '-map', f'{n}:a',
             '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-r', str(FPS),
             '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', os.path.join(outdir, v['id'] + '.mp4')]
    subprocess.run(args, check=True)
    Image.open(os.path.join(work, 'bg0.png')).resize((540, 960)).save(os.path.join(outdir, v['id'] + '-cover.jpg'), quality=88)
    return style


if __name__ == '__main__':
    a = sys.argv[1:]
    out = os.path.join(ROOT, 'videos')
    if '--out' in a:
        out = a[a.index('--out') + 1]; a = a[:a.index('--out')] + a[a.index('--out') + 2:]
    os.makedirs(out, exist_ok=True)
    spec = json.load(open(os.path.join(ROOT, 'generator', 'phone-reels-spec.json')))['videos']
    for v in spec:
        if not a or v['id'] in a:
            print('ok', v['id'], build(v, out))
