"""Problem -> solution reels (1080x1920, ~15 s): stop the scroll with a real problem, give 3 quick fixes,
show the tool at the end, then ask a question so people comment.

Scenes: hook (problem) -> why it happens -> 3 fixes -> the tool -> question.
Every reel gets its own music track (style/key/seed set in the spec, all different).
Spec: generator/pain-reels.json  ->  videos/<id>.mp4 + clips/<id>-nosound.mp4
Usage: python3 generator/pain_reel.py [ids...]   (no ids = all)
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from scipy.io import wavfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import music2
from life_reel import wrap, font, card, BOLD, MED, W, H, FPS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T_HOOK, T_WHY, T_TIP, T_TOOL, T_Q = 2.3, 2.6, 1.9, 2.6, 2.8


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def text_block(d, lines, f, y, color, lh, alpha=255, dx=0):
    for i, l in enumerate(lines):
        d.text(((W - d.textlength(l, font=f)) / 2 + dx, y + i * lh), l, font=f, fill=color + (alpha,))


def layer():
    return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def progress(im, frac, accent):
    d = ImageDraw.Draw(im)
    d.rectangle((0, H - 14, int(W * frac), H), fill=accent)


def scene_hook(s, t, P):
    im = Image.new('RGB', (W, H), P['dark'])
    k = ease(t / 0.35)
    f = font(BOLD, 96)
    d0 = ImageDraw.Draw(im)
    lines = wrap(d0, s['hook'], f, 940)
    lh = 124
    y = (H - lh * len(lines)) / 2 - 60
    L = layer(); d = ImageDraw.Draw(L)
    text_block(d, lines, f, y, (255, 255, 255), lh, int(255 * k))
    if k < 1:
        z = 0.88 + 0.12 * k
        L = L.resize((int(W * z), int(H * z)))
        pad = layer(); pad.paste(L, ((W - L.width) // 2, (H - L.height) // 2)); L = pad
    im.paste(L, (0, 0), L)
    return im


def scene_why(s, t, P):
    im = Image.new('RGB', (W, H), P['light'])
    d = ImageDraw.Draw(im)
    f = font(BOLD, 76)
    parts = s['why']
    y = 640
    for j, part in enumerate(parts):
        a = ease((t - j * 0.9) / 0.35)
        if a <= 0:
            continue
        lines = wrap(d, part, f, 920)
        L = layer(); dl = ImageDraw.Draw(L)
        col = (25, 25, 25) if j == 0 else P['accent']
        text_block(dl, lines, f, y + (1 - a) * 40, col, 98, int(255 * a))
        im.paste(L, (0, 0), L)
        y += 98 * len(lines) + 70
    return im


def scene_tip(s, t, P, n):
    im = Image.new('RGB', (W, H), P['light'])
    d = ImageDraw.Draw(im)
    fs = font(BOLD, 50)
    lab = 'Try this:'
    d.text(((W - d.textlength(lab, font=fs)) / 2, 520), lab, font=fs, fill=P['accent'])
    a = ease(t / 0.3)
    L = layer(); dl = ImageDraw.Draw(L)
    cx, cy, r = W / 2 + (1 - a) * 300, 760, 92
    dl.ellipse((cx - r, cy - r, cx + r, cy + r), fill=P['accent'] + (int(255 * a),))
    fn = font(BOLD, 110)
    num = str(n + 1)
    dl.text((cx - dl.textlength(num, font=fn) / 2, cy - 82), num, font=fn, fill=(255, 255, 255, int(255 * a)))
    f = font(BOLD, 80)
    lines = wrap(dl, s['tips'][n], f, 920)
    text_block(dl, lines, f, 930, (25, 25, 25), 104, int(255 * a), dx=(1 - a) * 300)
    im.paste(L, (0, 0), L)
    # dots: which tip we are on
    for i in range(3):
        x = W / 2 + (i - 1) * 46
        d.ellipse((x - 11, 1500 - 11, x + 11, 1500 + 11), fill=P['accent'] if i <= n else (210, 205, 200))
    return im


def tool_base(s, P):
    img = Image.open(os.path.join(ROOT, s['tool']['img'])).convert('RGB')
    bg = img.copy()
    sc = max(W / bg.width, H / bg.height)
    bg = bg.resize((int(bg.width * sc) + 1, int(bg.height * sc) + 1))
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(40))).enhance(0.55)
    d = ImageDraw.Draw(bg)
    f1, f2 = font(MED, 50), font(BOLD, 74)
    t1 = s['tool'].get('label', 'What I use for this:')
    d.text(((W - d.textlength(t1, font=f1)) / 2, 250), t1, font=f1, fill=(255, 255, 255))
    lines = wrap(d, s['tool']['name'], f2, 960)
    for i, l in enumerate(lines):
        d.text(((W - d.textlength(l, font=f2)) / 2, 330 + i * 92), l, font=f2, fill=(255, 255, 255))
    f3 = font(BOLD, 44)
    t3 = s['tool'].get('cta', 'Link in bio')
    tw = d.textlength(t3, font=f3) + 90
    d.rounded_rectangle(((W - tw) / 2, 1610, (W + tw) / 2, 1700), radius=45, fill=P['accent'])
    d.text(((W - d.textlength(t3, font=f3)) / 2, 1628), t3, font=f3, fill=(255, 255, 255))
    return bg, card(img).convert('RGBA')


def scene_tool(base, c, t):
    z = 1.0 + 0.06 * (t / T_TOOL)
    cc = c.resize((int(c.width * z), int(c.height * z)), Image.BILINEAR)
    fr = base.copy()
    cy = 1060 if c.width >= c.height else 1080
    fr.paste(cc, ((W - cc.width) // 2, cy - cc.height // 2), cc)
    return fr


def scene_q(s, t, P):
    im = Image.new('RGB', (W, H), P['accent'])
    d = ImageDraw.Draw(im)
    a = ease(t / 0.35)
    f = font(BOLD, 88)
    lines = wrap(d, s['question'], f, 940)
    lh = 112
    y = (H - lh * len(lines)) / 2 - 120
    L = layer(); dl = ImageDraw.Draw(L)
    text_block(dl, lines, f, y + (1 - a) * 40, (255, 255, 255), lh, int(255 * a))
    b = ease((t - 0.6) / 0.3)
    if b > 0:
        f2 = font(BOLD, 52)
        tx = s.get('comment', 'Comment below')
        tw = dl.textlength(tx, font=f2) + 100
        yy = y + lh * len(lines) + 90
        dl.rounded_rectangle(((W - tw) / 2, yy, (W + tw) / 2, yy + 112), radius=56, fill=(255, 255, 255, int(255 * b)))
        dl.text(((W - dl.textlength(tx, font=f2)) / 2, yy + 24), tx, font=f2, fill=P['accent'] + (int(255 * b),))
    im.paste(L, (0, 0), L)
    return im


def render(s):
    P = {'accent': tuple(s['accent']), 'dark': tuple(s['dark']), 'light': tuple(s['light'])}
    tb, tc = tool_base(s, P)
    plan = [('hook', T_HOOK), ('why', T_WHY), ('tip0', T_TIP), ('tip1', T_TIP), ('tip2', T_TIP), ('tool', T_TOOL), ('q', T_Q)]
    total = sum(int(d * FPS) for _, d in plan)
    tmp = tempfile.mkdtemp(); raw = os.path.join(tmp, 'v.mp4')
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', raw], stdin=subprocess.PIPE)
    done = 0; prev = None
    for name, dur in plan:
        n = int(dur * FPS)
        for k in range(n):
            t = k / FPS
            if name == 'hook': fr = scene_hook(s, t, P)
            elif name == 'why': fr = scene_why(s, t, P)
            elif name.startswith('tip'): fr = scene_tip(s, t, P, int(name[-1]))
            elif name == 'tool': fr = scene_tool(tb, tc, t)
            else: fr = scene_q(s, t, P)
            fr = fr.convert('RGB')
            if prev is not None and k < 5 and name in ('why', 'tool', 'q'):
                fr = Image.blend(prev, fr, (k + 1) / 6)
            progress(fr, (done + k + 1) / total, P['accent'] if name != 'q' else (255, 255, 255))
            p.stdin.write(fr.tobytes())
            last = fr
        prev = last
        done += n
    p.stdin.close(); p.wait()
    secs = total / FPS
    m = s['music']
    wav = os.path.join(tmp, 'm.wav')
    wavfile.write(wav, music2.SR, music2.make(secs + 0.5, m[0], m[1], m[2]))
    out = os.path.join(ROOT, 'videos', s['id'] + '.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k',
                    '-af', f'afade=t=in:d=0.2,afade=t=out:st={secs - 1.0:.2f}:d=1.0', '-shortest', out], check=True)
    subprocess.run(['cp', raw, os.path.join(ROOT, 'clips', s['id'] + '-nosound.mp4')], check=True)
    return out, music2.STYLES[m[0] % len(music2.STYLES)]


if __name__ == '__main__':
    specs = json.load(open(os.path.join(ROOT, 'generator', 'pain-reels.json')))['reels']
    want = set(sys.argv[1:])
    for s in specs:
        if not want or s['id'] in want:
            out, st = render(s)
            print(s['id'], st, out)
