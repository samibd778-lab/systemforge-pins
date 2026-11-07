"""Quick TikTok slideshow (9:16, 1080x1920, ~17 s, silent) from the real Etsy listing images.
Blurred listing image as background, the image itself in the middle, one big white line per scene.
Usage: python3 generator/v3/mini_tiktok.py [habit journal budget] -> tiktok/<p>-tiktok.mp4
"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'tiktok'); os.makedirs(OUT, exist_ok=True)
W, H, FPS, SEG, FADE = 1080, 1920, 30, 2.6, 0.35
FONT = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
if not os.path.exists(FONT):
    FONT = '/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'

LINES = {
 'habit': ['I stopped breaking my habits.\nHere is the Notion setup.', 'Tick 6 habits a day.\nThe score fills in by itself.',
           'Every habit gets a bar\nfor the month', 'Your whole month\nat a glance', 'A plan for the busy days',
           'Plus a 30-day reset guide', 'Habit Tracker for Notion\nLink in bio'],
 'journal': ['2 minutes a day changed\nhow my weeks feel', 'Mood, one win\nand one thank you', 'A gratitude jar\nfor the hard days',
             'See how your month\nreally felt', 'Your mood on a calendar', 'Plus a journaling guide', 'Daily Journal for Notion\nLink in bio'],
 'budget': ['Where did my money go?\nNow I know.', 'See what is left\nin every category', 'Never miss a bill again',
            'Every dollar in and out', 'Savings goals with a deadline', 'Plus a 7-day money reset', 'Budget Planner for Notion\nLink in bio'],
}
IMGS = ['1-main', '2-feature', '3-feature', '4-feature', '5-feature', '10-bonus', '1-main']


def scene(src, text, out):
    im = Image.open(src).convert('RGB')
    bg = im.resize((int(H * im.width / im.height), H)).crop(((int(H * im.width / im.height) - W) // 2, 0, (int(H * im.width / im.height) - W) // 2 + W, H))
    bg = bg.filter(ImageFilter.GaussianBlur(40)); bg = Image.blend(bg, Image.new('RGB', (W, H), (20, 20, 20)), 0.35)
    fg = im.resize((W - 60, int((W - 60) * im.height / im.width)), Image.LANCZOS)
    y0 = (H - fg.height) // 2 + 140
    mask = Image.new('L', fg.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, fg.width, fg.height), 28, fill=255)
    bg.paste(fg, (30, y0), mask)
    d = ImageDraw.Draw(bg); f = ImageFont.truetype(FONT, 68)
    lines = text.split('\n'); lh = 86; ty = y0 - 70 - lh * len(lines)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f)
        d.text(((W - tw) / 2, ty + i * lh), ln, font=f, fill='white', stroke_width=3, stroke_fill=(0, 0, 0))
    bg.save(out)


def build(p):
    src = os.path.join(ROOT, 'canva', 'v3', 'etsy', 'final', p)
    tmp = tempfile.mkdtemp()
    frames = []
    for i, (key, text) in enumerate(zip(IMGS, LINES[p])):
        f = os.path.join(tmp, f's{i}.png'); scene(os.path.join(src, f'{p}-{key}.png'), text, f); frames.append(f)
    n = int(SEG * FPS); args, fl = [], []
    for i, f in enumerate(frames):
        args += ['-i', f]
        z = 'min(1+0.0007*on,1.05)'
        fl.append(f"[{i}:v]scale={W*2}:{H*2},zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},setsar=1,format=yuv420p[v{i}]")
    last, off = 'v0', SEG - FADE
    for i in range(1, len(frames)):
        fl.append(f'[{last}][v{i}]xfade=transition=fade:duration={FADE}:offset={off:.2f}[x{i}]'); last = f'x{i}'; off += SEG - FADE
    out = os.path.join(OUT, f'{p}-tiktok.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *args, '-filter_complex', ';'.join(fl), '-map', f'[{last}]', '-an',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], check=True)
    os.system(f'cp {frames[1]} {OUT}/{p}-frame.png')
    print('ok', out)


if __name__ == '__main__':
    for p in sys.argv[1:] or ['habit', 'journal', 'budget']:
        build(p)
