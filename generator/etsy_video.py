"""Etsy listing video (16:9, 1920x1080, no sound, under 15 s) from generator/etsy-spec.json.
4 scenes = the 4 feature screenshots: caption on the left, screenshot card on the right, slow zoom.
Usage: python3 generator/etsy_video.py prop deal   -> etsy/<p>/video.mp4
"""
import json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles'))
from pins_v2 import ROOT, FONT_CSS, INK, MUT, SAGE, CREAM, PAP, CLAY, SAGEL, shoot  # noqa: E402
from etsy import crop  # noqa: E402

W, H, SEC, FPS = 1920, 1080, 3.7, 30


def scene(pr, f, path, i, n):
    from PIL import Image
    cw, ch = Image.open(path).size
    maxw, maxh = 1120, 760
    sc = min(maxw / cw, maxh / ch, 1.6)
    w, h = round(cw * sc), round(ch * sc)
    a, b = f['title']
    dots = ''.join(f'<span style="background:{SAGE if k == i else "#D8D0C4"}"></span>' for k in range(n))
    css = f'''{FONT_CSS}*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;background:{CREAM};font-family:InterW;color:{INK};position:relative;overflow:hidden}}
.b1{{position:absolute;width:700px;height:700px;border-radius:50%;background:{SAGEL};left:-300px;top:-340px}}
.b2{{position:absolute;width:760px;height:760px;border-radius:50%;background:{CLAY};right:-330px;bottom:-400px;opacity:.75}}
.l{{position:absolute;left:90px;top:0;bottom:0;width:560px;display:flex;flex-direction:column;justify-content:center}}
.k{{font-weight:700;font-size:22px;letter-spacing:4px;color:{SAGE}}}
h1{{margin-top:18px;font-weight:800;font-size:68px;line-height:1.05;letter-spacing:-2px}}
h1 em{{font-style:normal;color:#9A5F3C}}
p{{margin-top:22px;font-weight:500;font-size:28px;line-height:1.4;color:{MUT}}}
.dots{{margin-top:40px;display:flex;gap:10px}}.dots span{{width:40px;height:8px;border-radius:4px}}
.c{{position:absolute;left:{700 + (maxw - w) // 2}px;top:{(H - h - 40) // 2}px;width:{w}px;background:#fff;border-radius:20px;overflow:hidden;
box-shadow:0 40px 90px rgba(46,42,37,.18),0 0 0 1px rgba(46,42,37,.06)}}
.bar{{height:40px;background:#F3F0EB;display:flex;align-items:center;gap:9px;padding:0 18px}}.bar span{{width:12px;height:12px;border-radius:50%;background:#D8D1C6}}
.c img{{display:block;width:{w}px;height:{h}px}}
.f{{position:absolute;right:70px;bottom:44px;font-weight:700;font-size:24px;color:{INK}}}'''
    html = (f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="b1"></div><div class="b2"></div>'
            f'<div class="l"><div class="k">{pr["name"].upper()}</div><h1>{a}<br><em>{b}</em></h1><p>{f["sub"]}</p><div class="dots">{dots}</div></div>'
            f'<div class="c"><div class="bar"><span></span><span></span><span></span></div><img src="file://{path}"></div>'
            f'<div class="f">SystemForge</div></body></html>')
    return html


def build(p, pr):
    with tempfile.TemporaryDirectory() as tmp:
        parts = []
        feats = pr['features'][:4]
        for i, f in enumerate(feats):
            path, _, _ = crop(f['shot'], f['crop'], tmp, f'v{i}', trim=True)
            img = shoot(scene(pr, f, path, i, len(feats)), W, H, None, tmp, f's{i}')
            png = os.path.join(tmp, f's{i}.png')
            img.convert('RGB').resize((W, H)).save(png)
            out = os.path.join(tmp, f'p{i}.mp4')
            frames = round(SEC * FPS)
            # slow push-in (zoom 1.00 -> 1.06), rendered at 2x then scaled down for smooth motion
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', png, '-vf',
                            f"scale={W * 2}:{H * 2},zoompan=z='1+0.06*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS},format=yuv420p",
                            '-frames:v', str(frames), '-c:v', 'libx264', '-crf', '20', out], check=True)
            parts.append(out)
        lst = os.path.join(tmp, 'l.txt')
        open(lst, 'w').write(''.join(f"file '{x}'\n" for x in parts))
        dst = os.path.join(ROOT, 'etsy', p, 'video.mp4')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', '-an', dst], check=True)
    print('ok', dst)


if __name__ == '__main__':
    spec = json.load(open(os.path.join(ROOT, 'generator', 'etsy-spec.json')))['products']
    for p in sys.argv[1:]:
        build(p, spec[p])
