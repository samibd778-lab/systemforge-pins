"""Turn each Instagram carousel into a vertical Reel with our own music (no copyright).

Reads carousels/<id>/<n>.jpg (made by carousel.py) -> videos/<id>.mp4.
Usage: python3 generator/carousel_reel.py [ids...]
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen, reels, music2
from scipy.io import wavfile

ROOT = gen.ROOT
W, H, FPS, XF = 1080, 1920, 30, 0.3
SW = 960  # slide width on the reel


def frame_bg(theme, path):
    reels.render_png(reels.frame(theme, ''), path)


def compose(bg_path, slide_path, out):
    bg = Image.open(bg_path).convert('RGB')
    s = Image.open(slide_path).convert('RGB')
    sh = int(s.height * SW / s.width)
    s = s.resize((SW, sh), Image.LANCZOS)
    x, y = (W - SW) // 2, (H - sh) // 2
    mask = Image.new('L', (SW, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, SW, sh), 36, fill=255)
    shadow = Image.new('L', (W, H), 0)
    ImageDraw.Draw(shadow).rounded_rectangle((x, y + 24, x + SW, y + sh + 24), 36, fill=70)
    shadow = shadow.filter(ImageFilter.GaussianBlur(30))
    bg.paste(Image.new('RGB', (W, H), (46, 42, 37)), (0, 0), shadow)
    bg.paste(s, (x, y), mask)
    bg.save(out)


def build(c):
    work = tempfile.mkdtemp()
    d = os.path.join(ROOT, 'carousels', c['id'])
    bgp = os.path.join(work, 'bg.png')
    frame_bg(c['theme'], bgp)
    n = len(c['slides'])
    imgs, durs = [], []
    for i in range(n):
        p = os.path.join(work, f'{i}.png')
        compose(bgp, os.path.join(d, f'{i + 1}.jpg'), p)
        imgs.append(p)
        t = c['slides'][i]['type']
        durs.append(2.4 if t == 'cover' else 3.2 if t == 'tip' else 2.6)
    total = sum(durs) + XF
    wav = os.path.join(work, 'm.wav')
    music2.write_for(c['id'], total + 0.5, wav)
    args = ['ffmpeg', '-y', '-loglevel', 'error']
    for p, du in zip(imgs, durs):
        args += ['-loop', '1', '-t', f'{du + XF:.2f}', '-i', p]
    args += ['-i', wav]
    f = []
    for i, du in enumerate(durs):
        f.append(f"[{i}:v]scale=w='trunc({W}*(1+0.05*t/{du + XF:.2f})/2)*2':h=-2:eval=frame:flags=lanczos,crop={W}:{H},setsar=1,fps={FPS},format=yuv420p[s{i}]")
    last, off = 's0', 0.0
    for i in range(1, n):
        off += durs[i - 1]
        f.append(f'[{last}][s{i}]xfade=transition=slideleft:duration={XF}:offset={off:.2f}[x{i}]')
        last = f'x{i}'
    f.append(f'[{n}:a]afade=t=out:st={total - 1:.2f}:d=1,volume=0.8[a]')
    out = os.path.join(ROOT, 'videos', c['id'] + '.mp4')
    args += ['-filter_complex', ';'.join(f), '-map', f'[{last}]', '-map', '[a]',
             '-c:v', 'libx264', '-preset', 'slow', '-b:v', '10M', '-maxrate', '14M', '-bufsize', '20M', '-pix_fmt', 'yuv420p', '-r', str(FPS),
             '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out]
    subprocess.run(args, check=True)
    return out


if __name__ == '__main__':
    spec = json.load(open(os.path.join(ROOT, 'generator', 'carousels-spec.json')))['carousels']
    only = sys.argv[1:]
    for c in spec:
        if not only or c['id'] in only:
            print('ok', build(c))
