"""Etsy listing videos: 12 s, silent (Etsy removes sound), 4:3 1920x1440 like the listing photos.
Slow zoom over the real listing images: main + 3 features, short crossfades.
Usage: python3 generator/v3/etsy_video.py [products...] -> etsy/videos/<p>-etsy.mp4
"""
import os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'canva', 'v3', 'etsy', 'final'); OUT = os.path.join(ROOT, 'etsy', 'videos')
SEG, FADE, FPS = 3.3, 0.4, 30


def build(p):
    import glob  # first 4 listing images (main + features, or main + included + inside for packs)
    imgs = [os.path.basename(f) for f in sorted(glob.glob(os.path.join(SRC, p, f'{p}-[1-4]-*.png'))) if 'gumroad' not in f][:4]
    args, fl = [], []
    n = int(SEG * FPS)
    for i, im in enumerate(imgs):
        args += ['-i', os.path.join(SRC, p, im)]
        z = "min(1+0.0009*on,1.08)" if i % 2 == 0 else "max(1.08-0.0009*on,1)"
        fl.append(f'[{i}:v]scale=3840:2880,zoompan=z=\'{z}\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d={n}:s=1920x1440:fps={FPS},setsar=1,format=yuv420p[v{i}]')
    last = 'v0'; off = SEG - FADE
    for i in range(1, len(imgs)):
        fl.append(f'[{last}][v{i}]xfade=transition=fade:duration={FADE}:offset={off:.2f}[x{i}]')
        last = f'x{i}'; off += SEG - FADE
    out = os.path.join(OUT, f'{p}-etsy.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *args, '-filter_complex', ';'.join(fl), '-map', f'[{last}]',
                    '-an', '-c:v', 'libx264', '-profile:v', 'main', '-level', '4.2', '-preset', 'slow', '-crf', '19', '-r', '30', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], check=True)
    print('ok', out)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for p in sys.argv[1:] or ['fco', 'ccs', 'deal', 'prop', 'fit', 'wcp']:
        build(p)
