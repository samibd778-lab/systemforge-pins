"""Pro vertical reel from real Notion screen recordings.

Spec (JSON): {"id", "p", "theme", "hook", "segments": [
   {"src": "raw/x.mp4", "t0": 5.5, "t1": 10, "box": [x0,y0,x1,y1], "caption": "...", "zoom": 1.08}
 ], "music": optional path}
Each segment: real footage cropped to the action, big caption on top, slow push-in.
Starts with a 1.2s hook overlaid on the first segment, ends with the SystemForge card.
Without music the file is silent, ready for a trending sound inside TikTok / Instagram.
"""
import json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen, reels

W, H, VW, TOP = 1080, 1920, 1000, 560


def caption_bg(theme, text, big=False):
    size = 104 if big else 84
    return reels.frame(theme, f'''<div style="position:absolute;left:60px;right:60px;top:170px;height:330px;display:flex;align-items:center;justify-content:center;text-align:center;{gen.SER};font-size:{size}px;line-height:1.05;font-weight:700;letter-spacing:-2px">{text}</div>
<div style="position:absolute;left:0;right:0;bottom:110px;display:flex;justify-content:space-between;padding:0 80px;align-items:center">{gen.logo()}
<span style="font-size:30px;font-weight:600;color:{gen.MUT}">{{prod}}</span></div>''')


def build(spec, outdir):
    work = tempfile.mkdtemp()
    parts = []
    prod = gen.PRODUCTS[spec['p']]
    for i, s in enumerate(spec['segments']):
        x0, y0, x1, y1 = s['box']
        vh = int((y1 - y0) * VW / (x1 - x0)) // 2 * 2
        vh = min(vh, 1180)
        text = spec['hook'] if i == 0 and s.get('hook', True) else s['caption']
        bg = os.path.join(work, f'bg{i}.png')
        reels.render_png(caption_bg(spec['theme'], text, i == 0).replace('{prod}', prod), bg)
        d = s['t1'] - s['t0']
        z = s.get('zoom', 1.06)
        top = TOP + max(0, (1180 - vh) // 2)
        out = os.path.join(work, f's{i}.mp4')
        # slow push-in: scale the crop up over time, keep it centred, then pad into the card
        fc = (f"[0:v]crop={x1-x0}:{y1-y0}:{x0}:{y0},scale={VW}:{vh}:flags=lanczos,unsharp=5:5:0.9:5:5:0,setsar=1,"
              f"scale=w='trunc({VW}*(1+({z}-1)*t/{d})/2)*2':h=-2:eval=frame:flags=lanczos,crop={VW}:{vh},"
              f"pad={VW+16}:{vh+16}:8:8:color=white[c];"
              f"[1:v][c]overlay=32:{top}:shortest=1,fps=30,format=yuv420p[v]")
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(s['t0']), '-t', str(d), '-i', s['src'],
                        '-loop', '1', '-t', str(d), '-i', bg, '-filter_complex', fc, '-map', '[v]',
                        '-c:v', 'libx264', '-crf', '10', '-preset', 'medium', out], check=True)
        parts.append((out, d))
    endp = os.path.join(work, 'end.png')
    reels.render_png(reels.scene_html({'type': 'end', 'sub': spec.get('end_sub', 'a calm Notion template')}, spec['theme'], spec['p']), endp)
    endv = os.path.join(work, 'end.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-t', '2.4', '-i', endp,
                    '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-crf', '10', endv], check=True)
    parts.append((endv, 2.4))
    args = ['ffmpeg', '-y', '-loglevel', 'error']
    for p, _ in parts:
        args += ['-i', p]
    f, last, off = [], '0:v', 0.0
    for i in range(1, len(parts)):
        off += parts[i - 1][1] - 0.25
        f.append(f'[{last}][{i}:v]xfade=transition=fade:duration=0.25:offset={off:.2f}[x{i}]')
        last = f'x{i}'
    total = sum(d for _, d in parts) - 0.25 * (len(parts) - 1)
    music = spec.get('music')
    if music == 'auto':
        import music2
        music = os.path.join(work, 'm.wav')
        music2.write_for(spec['id'], total + 0.5, music)
    if music:
        args += ['-i', music]
        f.append(f'[{len(parts)}:a]atrim=0:{total:.2f},afade=t=out:st={total-1:.2f}:d=1,volume=0.8[a]')
    args += ['-filter_complex', ';'.join(f), '-map', f'[{last}]']
    if music:
        args += ['-map', '[a]', '-c:a', 'aac', '-b:a', '192k']
    out = os.path.join(outdir, spec['id'] + ('' if music else '-nosound') + '.mp4')
    args += ['-c:v', 'libx264', '-b:v', '10M', '-maxrate', '14M', '-bufsize', '20M', '-preset', 'slow', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]
    subprocess.run(args, check=True)
    return out


if __name__ == '__main__':
    root = gen.ROOT
    specs = json.load(open(os.path.join(root, 'generator', 'reels2-spec.json')))['videos']
    only = sys.argv[1:]
    os.makedirs(os.path.join(root, 'clips'), exist_ok=True)
    os.chdir(root)
    for s in specs:
        if not only or s['id'] in only:
            print('ok', build(s, os.path.join(root, 'clips')))
            print('ok', build(dict(s, music='auto'), os.path.join(root, 'videos')))
