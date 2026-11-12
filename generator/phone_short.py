"""Short vertical video (1080x1920, 10-15 s) from Sami's phone screen recordings of a Notion template.
Crops the phone status bar and the bottom bar, speeds up the boring parts, adds big text lines and our music.
Spec: generator/phone-shorts.json  ->  videos/shorts/<id>.mp4 (+ <id>-nosound.mp4)
Usage: python3 generator/phone_short.py <id>"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
W, H = 1080, 1920


def text_png(path, text, y, size=64, box=True):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, size)
    lines = text.split('\n'); lh = int(size * 1.25)
    widths = [d.textlength(l, font=f) for l in lines]
    top = y
    if box:
        bw = max(max(widths) + 70, 940); bh = lh * len(lines) + 44
        d.rounded_rectangle(((W - bw) / 2, top - 22, (W + bw) / 2, top - 22 + bh), radius=28, fill=(255, 255, 255, 240))
    for i, l in enumerate(lines):
        x = (W - widths[i]) / 2
        if box:
            d.text((x, top + i * lh), l, font=f, fill=(20, 20, 20, 255))
        else:
            d.text((x, top + i * lh), l, font=f, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=(0, 0, 0, 230))
    im.save(path)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-2000:]); sys.exit(1)


def build(spec):
    tmp = tempfile.mkdtemp()
    parts = []
    for i, s in enumerate(spec['segments']):
        src = os.path.join(ROOT, s['src']); x, y, w, h = s['crop']; sp = s.get('speed', 1)
        hold = s.get('hold', 0)
        dur = (s['t1'] - s['t0']) / sp + hold
        vf = f"trim={s['t0']}:{s['t1']},setpts=(PTS-STARTPTS)/{sp},crop={w}:{h}:{x}:{y},scale={W}:{H}:flags=lanczos,fps=30"
        if hold:
            vf += f",tpad=stop_mode=clone:stop_duration={hold}"
        inputs = ['-i', src]; chain = f"[0:v]{vf}[v0]"; last = 'v0'
        for j, t in enumerate(s.get('texts', [])):
            p = os.path.join(tmp, f't{i}_{j}.png'); text_png(p, t['text'], t.get('y', 230), t.get('size', 64), t.get('box', True))
            inputs += ['-i', p]
            a, b = t.get('from', 0), t.get('to', dur)
            chain += f";[{last}][{j + 1}:v]overlay=0:0:enable='between(t,{a},{b})'[o{j}]"; last = f'o{j}'
        out = os.path.join(tmp, f'p{i}.mp4'); parts.append(out)
        run(['ffmpeg', '-loglevel', 'error', '-y', *inputs, '-filter_complex', chain, '-map', f'[{last}]', '-an',
             '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', out])
    lst = os.path.join(tmp, 'l.txt'); open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    od = os.path.join(ROOT, 'videos', 'shorts'); os.makedirs(od, exist_ok=True)
    ns = os.path.join(od, spec['id'] + '-nosound.mp4')
    run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', ns])
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', ns], capture_output=True, text=True).stdout)
    wav = os.path.join(tmp, 'm.wav')
    run(['python3', os.path.join(ROOT, 'generator', 'music2.py'), wav, str(d + 0.5), str(spec.get('music', 0)), '0', str(spec.get('seed', 1))])
    final = os.path.join(od, spec['id'] + '.mp4')
    run(['ffmpeg', '-loglevel', 'error', '-y', '-i', ns, '-i', wav, '-filter_complex', f"[1:a]afade=t=out:st={d - 1}:d=1[a]",
         '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', final])
    print(final, round(d, 1), 's')


if __name__ == '__main__':
    specs = {s['id']: s for s in json.load(open(os.path.join(ROOT, 'generator', 'phone-shorts.json')))}
    build(specs[sys.argv[1]])
