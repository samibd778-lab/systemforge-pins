"""SystemForge short videos (Reels / TikTok / Shorts) from real Notion screenshots.

Reads generator/reels-spec.json, renders each scene as a 1080x1920 image with
headless Chrome, then animates them (slow zoom + crossfades) into
videos/<id>.mp4 with ffmpeg. Also writes videos.json (read by n8n).

Usage: python3 generator/reels.py            # all videos
       python3 generator/reels.py r01 r02     # only these ids
"""
import json, os, subprocess, sys, tempfile
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen  # reuse identity, devices and crops
from gen import S, SER, PAP, SAGE, BR, INK, MUT, THEMES, PRODUCTS, laptop, phone, crop_card, logo

ROOT = gen.ROOT
OUT = os.path.join(ROOT, 'videos')
W, H = 1080, 1920
FPS = 30
XF = 0.3  # crossfade seconds


def frame(theme, inner):
    bg, c1, c2 = THEMES[theme]
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0}}*{{box-sizing:border-box}}</style></head><body>
<div style="position:relative;overflow:hidden;width:{W}px;height:{H}px;background:{bg};color:{INK};{S};padding:150px 80px 170px;display:flex;flex-direction:column;gap:50px">
<div style="position:absolute;left:-220px;top:-240px;width:720px;height:720px;border-radius:50%;background:{c1}"></div>
<div style="position:absolute;right:-260px;bottom:-280px;width:840px;height:840px;border-radius:50%;background:{c2}"></div>
{inner}</div></body></html>'''


def scene_html(sc, theme, product):
    t = sc['type']
    if t == 'hook':
        return frame(theme, f'''<div style="position:relative;flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;gap:40px">
<div style="font-size:30px;font-weight:700;letter-spacing:6px;color:{SAGE}">{sc.get('kicker','')}</div>
<h1 style="margin:0;{SER};font-size:{sc.get('size',128)}px;line-height:1.04;font-weight:700;letter-spacing:-3px">{sc['text']}</h1>
<div style="{SER};font-style:italic;font-size:54px;color:{BR}">{sc.get('sub','')}</div></div>''')
    if t == 'shot':
        L = sc['layout']
        if L == 'laptop':
            vis = laptop(sc['shots'][0], width=940, screen_h=540, show_w=sc.get('show_w', 1400))
        elif L == 'phone':
            vis = phone(sc['shots'][0], width=520)
        elif L == 'phones':
            vis = f'<div style="display:flex;gap:40px;justify-content:center">{phone(sc["shots"][0], width=440, rotate=-3)}{phone(sc["shots"][1], width=440, rotate=3)}</div>'
        else:  # zoom
            vis = crop_card(None, None, width=960, max_h=1150, parts=[(n, b) for n, b in sc['parts']], direction=sc.get('dir', 'h'))
        return frame(theme, f'''<div style="position:relative;flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:80px">
<div style="text-align:center;{SER};font-size:{sc.get('size',96)}px;line-height:1.06;font-weight:700;letter-spacing:-2px">{sc['text']}</div>
<div style="display:flex;justify-content:center;width:100%">{vis}</div></div>''')
    if t == 'end':
        return frame(theme, f'''<div style="position:relative;flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;gap:44px">
<div style="transform:scale(1.8)">{logo()}</div>
<h1 style="margin:40px 0 0;{SER};font-size:104px;line-height:1.05;font-weight:700;letter-spacing:-2px">{PRODUCTS[product]}</h1>
<div style="{SER};font-style:italic;font-size:54px;color:{BR}">{sc.get('sub','a calm Notion template')}</div>
<div style="margin-top:30px;background:{INK};color:{PAP};border-radius:999px;padding:30px 60px;font-size:44px;font-weight:700">Link in bio</div></div>''')
    raise ValueError(t)


def render_png(html, path):
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f:
        f.write(html)
    tmp = f.name + '.png'
    subprocess.run([gen.CHROME, '--headless=new', '--no-sandbox', '--hide-scrollbars', '--allow-file-access-from-files',
                    f'--window-size={W},{H + 300}', f'--screenshot={tmp}', 'file://' + f.name],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    Image.open(tmp).crop((0, 0, W, H)).convert('RGB').save(path)
    os.remove(f.name); os.remove(tmp)


def build(v):
    work = tempfile.mkdtemp()
    imgs, durs = [], []
    for i, sc in enumerate(v['scenes']):
        p = os.path.join(work, f'{i}.png')
        render_png(scene_html(sc, sc.get('theme', v['theme']), v['p']), p)
        imgs.append(p); durs.append(sc.get('dur', 2.6))
    args = ['ffmpeg', '-y', '-loglevel', 'error']
    for p, d in zip(imgs, durs):
        args += ['-loop', '1', '-t', f'{d + XF:.2f}', '-i', p]
    total = sum(durs) + XF
    import music
    from scipy.io import wavfile
    wav = os.path.join(work, 'music.wav')
    wavfile.write(wav, music.SR, music.make(total + 0.5, shift=0 if v['p'] == 'fco' else 5,
                                             variant=sum(map(ord, v['id'])) % 2))
    args += ['-i', wav]
    f = []
    for i, d in enumerate(durs):  # slow push-in on every scene
        z = 0.06
        f.append(f"[{i}:v]scale=w='trunc({W}*(1+{z}*t/{d + XF:.2f})/2)*2':h=-2:eval=frame:flags=lanczos,crop={W}:{H},setsar=1,fps={FPS},format=yuv420p[s{i}]")
    last, off = 's0', 0.0
    for i in range(1, len(durs)):
        off += durs[i - 1]
        f.append(f'[{last}][s{i}]xfade=transition=fade:duration={XF}:offset={off:.2f}[x{i}]')
        last = f'x{i}'
    args += ['-filter_complex', ';'.join(f), '-map', f'[{last}]', '-map', f'{len(durs)}:a',
             '-c:v', 'libx264', '-preset', 'slow', '-b:v', '10M', '-maxrate', '14M', '-bufsize', '20M', '-pix_fmt', 'yuv420p', '-r', str(FPS),
             '-c:a', 'aac', '-b:a', '64k', '-shortest', '-movflags', '+faststart',
             os.path.join(OUT, v['id'] + '.mp4')]
    subprocess.run(args, check=True)
    Image.open(imgs[0]).resize((540, 960)).save(os.path.join(OUT, v['id'] + '-cover.jpg'), quality=85)


def main():
    os.makedirs(OUT, exist_ok=True)
    spec = json.load(open(os.path.join(ROOT, 'generator', 'reels-spec.json')))['videos']
    only = sys.argv[1:]
    for v in spec:
        if only != ['--json'] and (not only or v['id'] in only):
            build(v); print('ok', v['id'])
    extra = json.load(open(os.path.join(ROOT, 'generator', 'videos-extra.json')))['videos']
    # entries with "after": "<id>" are pinned right after that video (used to jump the queue)
    pinned = [v for v in extra if v.get('after')]
    extra = [v for v in extra if not v.get('after')]
    real = [{k: v[k] for k in ('id', 'p', 'title', 'caption', 'tags')} for v in spec]
    mixed = [real.pop(0)]  # r01 was already posted first; then real recordings and slideshows alternate
    while extra or real:
        if extra: mixed.append(extra.pop(0))
        if real: mixed.append(real.pop(0))
    for v in pinned:
        ids = [m['id'] for m in mixed]
        pos = ids.index(v['after']) + 1 if v['after'] in ids else len(mixed)
        mixed.insert(pos, {k: v[k] for k in ('id', 'p', 'title', 'caption', 'tags')})
    json.dump({'videos': mixed},
              open(os.path.join(ROOT, 'videos.json'), 'w'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
