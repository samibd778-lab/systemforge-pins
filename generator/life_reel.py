"""Vertical reels (1080x1920, ~15 s) from listing images or printable pages, with our own music.

Each slide: blurred background of the image, a hook line at the top, the image as a card with a slow zoom,
then an end card (product name, benefit, "Link in bio").
Spec: generator/life-reels.json  ->  videos/<id>.mp4 + clips/<id>-nosound.mp4
Usage: python3 generator/life_reel.py [ids...]   (no ids = all)
"""
import json, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
from scipy.io import wavfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import music2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
SLIDE, XF, END = 3.2, 0.3, 2.6
BOLD = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
MED = '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, maxw):
    out = []
    for para in text.split('\n'):
        line = ''
        for w in para.split():
            t = (line + ' ' + w).strip()
            if d.textlength(t, font=f) <= maxw:
                line = t
            else:
                out.append(line); line = w
        out.append(line)
    return out


def base_layer(img, hook, accent):
    """Background + hook text (static part of a slide)."""
    bg = img.copy()
    s = max(W / bg.width, H / bg.height)
    bg = bg.resize((int(bg.width * s) + 1, int(bg.height * s) + 1))
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = bg.filter(ImageFilter.GaussianBlur(38))
    bg = ImageEnhance.Brightness(bg).enhance(0.62)
    d = ImageDraw.Draw(bg)
    f = font(BOLD, 74)
    lines = wrap(d, hook, f, 940)
    lh = 96
    top = 400
    bw = max(d.textlength(l, font=f) for l in lines) + 90
    d.rounded_rectangle(((W - bw) / 2, top - 34, (W + bw) / 2, top + lh * len(lines) + 20), radius=34, fill=(255, 255, 255))
    for i, l in enumerate(lines):
        d.text(((W - d.textlength(l, font=f)) / 2, top + i * lh), l, font=f, fill=(22, 22, 22))
    f2 = font(MED, 40)
    t = 'Link in bio'
    d.rounded_rectangle(((W - 330) / 2, 1560, (W + 330) / 2, 1640), radius=40, fill=accent)
    d.text(((W - d.textlength(t, font=f2)) / 2, 1575), t, font=f2, fill=(255, 255, 255))
    return bg


def card(img):
    """Image card scaled to fit the middle area, rounded corners."""
    maxw, maxh = (1000, 1060) if img.width >= img.height else (1000, 840)
    s = min(maxw / img.width, maxh / img.height)
    c = img.resize((int(img.width * s), int(img.height * s)), Image.LANCZOS)
    m = Image.new('L', c.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, c.width - 1, c.height - 1), radius=26, fill=255)
    c.putalpha(m)
    return c


def slide_frame(base, c, t, dur, cy=None):
    if cy is None:
        cy = 1080 if c.width >= c.height else 1100
    z = 1.0 + 0.07 * (t / dur)
    cc = c.resize((int(c.width * z), int(c.height * z)), Image.BILINEAR)
    fr = base.copy()
    sh = Image.new('RGBA', (cc.width + 60, cc.height + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((30, 40, cc.width + 30, cc.height + 40), radius=30, fill=(0, 0, 0, 110))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    x, y = (W - cc.width) // 2, cy - cc.height // 2
    fr.paste(sh, (x - 30, y - 30), sh)
    fr.paste(cc, (x, y), cc)
    return fr


def end_frame(name, line, accent, bgcol):
    im = Image.new('RGB', (W, H), bgcol)
    d = ImageDraw.Draw(im)
    f1, f2, f3 = font(BOLD, 104), font(MED, 54), font(BOLD, 52)
    y = 700
    for l in wrap(d, name, f1, 940):
        d.text(((W - d.textlength(l, font=f1)) / 2, y), l, font=f1, fill=(22, 22, 22)); y += 128
    y += 30
    for l in wrap(d, line, f2, 900):
        d.text(((W - d.textlength(l, font=f2)) / 2, y), l, font=f2, fill=(70, 70, 70)); y += 76
    y += 70
    t = 'Link in bio'
    tw = d.textlength(t, font=f3) + 110
    d.rounded_rectangle(((W - tw) / 2, y, (W + tw) / 2, y + 110), radius=55, fill=accent)
    d.text(((W - d.textlength(t, font=f3)) / 2, y + 22), t, font=f3, fill=(255, 255, 255))
    f4 = font(MED, 34)
    t = 'SystemForge'
    d.text(((W - d.textlength(t, font=f4)) / 2, 1760), t, font=f4, fill=(120, 120, 120))
    return im


def render(spec, idx):
    accent = tuple(spec.get('accent', [40, 40, 40]))
    bgcol = tuple(spec.get('bg', [245, 240, 233]))
    slides = []
    for s in spec['slides']:
        img = Image.open(os.path.join(ROOT, s['img'])).convert('RGB')
        slides.append((base_layer(img, s['hook'], accent), card(img).convert('RGBA')))
    endf = end_frame(spec['end']['name'], spec['end']['line'], accent, bgcol)
    n_sl = int(SLIDE * FPS); n_x = int(XF * FPS); n_end = int(END * FPS)
    tmp = tempfile.mkdtemp()
    raw = os.path.join(tmp, 'v.mp4')
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', raw],
                         stdin=subprocess.PIPE)
    frames = []
    for si, (b, c) in enumerate(slides):
        for k in range(n_sl):
            frames.append(('s', si, k))
    for k in range(n_end):
        frames.append(('e', 0, k))
    prev = None
    total = len(frames)
    # cross-fade: blend the first n_x frames of each segment with the last frame of the previous one
    seg_start = 0
    cur_seg = None
    for i, (kind, si, k) in enumerate(frames):
        if kind == 's':
            fr = slide_frame(slides[si][0], slides[si][1], k / FPS, SLIDE)
        else:
            fr = endf
        seg = (kind, si)
        if seg != cur_seg:
            cur_seg = seg; last_prev = prev
        if last_prev is not None and k < n_x:
            fr = Image.blend(last_prev, fr, (k + 1) / (n_x + 1))
        p.stdin.write(fr.tobytes())
        prev = fr
    p.stdin.close(); p.wait()
    secs = total / FPS
    wav = os.path.join(tmp, 'm.wav')
    style, shift, seed = music2.pick(idx, spec['id'])
    wavfile.write(wav, music2.SR, music2.make(secs + 0.5, style, shift, seed))
    out = os.path.join(ROOT, 'videos', spec['id'] + '.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac',
                    '-b:a', '160k', '-af', f'afade=t=in:d=0.4,afade=t=out:st={secs - 1.4:.2f}:d=1.4', '-shortest', out], check=True)
    os.makedirs(os.path.join(ROOT, 'clips'), exist_ok=True)
    subprocess.run(['cp', raw, os.path.join(ROOT, 'clips', spec['id'] + '-nosound.mp4')], check=True)
    return out, music2.STYLES[style]


if __name__ == '__main__':
    specs = json.load(open(os.path.join(ROOT, 'generator', 'life-reels.json')))['reels']
    want = set(sys.argv[1:])
    for i, s in enumerate(specs):
        if want and s['id'] not in want:
            continue
        out, st = render(s, 40 + i)
        print(s['id'], st, out)
