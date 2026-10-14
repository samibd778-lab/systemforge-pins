"""Style 2: 'photo of a laptop screen' look — the Notion screen tilted in 3D, close up,
with soft depth of field, warm light and a keyboard edge. No text on the image (the hook goes in the post caption).

python3 photo_screen.py <shot.png> <name> [crop_x0 crop_y0 crop_x1 crop_y1]  -> out/<name>.png (1080x1350)
"""
import os
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
W, H = 1080, 1350

shot, name = sys.argv[1], sys.argv[2]
im = Image.open(shot)
if len(sys.argv) > 6:
    im = im.crop(tuple(int(v) for v in sys.argv[3:7]))
crop_path = os.path.join(HERE, 'out', name + '-crop.png')
im.save(crop_path)
sw, sh = im.size
SCR_W = 1650
SCR_H = int(SCR_W * sh / sw)

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0}}
body{{width:{W}px;height:{H}px;overflow:hidden;position:relative;
  background:radial-gradient(ellipse at 70% 20%,#F3E6D6 0%,#D9C3A8 45%,#9C8468 100%)}}
.stage{{position:absolute;inset:0;perspective:1400px;perspective-origin:30% 40%}}
.lap{{position:absolute;left:-140px;top:300px;width:{SCR_W + 60}px;transform-origin:0 50%;
  transform:rotateY(24deg) rotateX(9deg) rotateZ(-3deg);transform-style:preserve-3d}}
.bez{{background:#151413;border-radius:28px;padding:30px;box-shadow:0 60px 120px rgba(40,25,10,.45)}}
.scr{{width:{SCR_W}px;height:{SCR_H}px;background:#fff url("file://{crop_path}") 0 0/100% 100%;border-radius:6px;position:relative;overflow:hidden}}
.glare{{position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,.0) 35%,rgba(255,255,255,.16) 48%,rgba(255,255,255,0) 62%)}}
.kb{{height:240px;margin:0 -40px;background:linear-gradient(#2A2826,#1A1918);border-radius:0 0 40px 40px;transform:rotateX(78deg);transform-origin:50% 0;
  background-image:repeating-linear-gradient(90deg,#33302D 0 62px,#1A1918 62px 70px),repeating-linear-gradient(0deg,#1A1918 0 8px,transparent 8px 62px)}}
.dof{{position:absolute;inset:0;backdrop-filter:blur(5px);-webkit-mask-image:linear-gradient(100deg,transparent 0%,transparent 45%,#000 85%)}}
.dof2{{position:absolute;inset:0;backdrop-filter:blur(4px);-webkit-mask-image:linear-gradient(180deg,transparent 0%,transparent 70%,#000 100%)}}
.warm{{position:absolute;inset:0;background:radial-gradient(ellipse at 25% 35%,rgba(255,236,210,.0) 0%,rgba(80,50,20,.28) 100%);mix-blend-mode:multiply}}
.grain{{position:absolute;inset:0;opacity:.07;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='160' height='160' filter='url(%23n)'/></svg>")}}
</style></head><body>
<div class="stage"><div class="lap"><div class="bez"><div class="scr"><div class="glare"></div></div></div><div class="kb"></div></div></div>
<div class="dof"></div><div class="dof2"></div><div class="warm"></div><div class="grain"></div>
</body></html>'''
src = os.path.join(HERE, 'out', name + '.html')
open(src, 'w').write(html)
out = os.path.join(HERE, 'out', name + '.png')
subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--hide-scrollbars', '--force-device-scale-factor=2',
                f'--window-size={W},{H + 200}', f'--screenshot={out}', 'file://' + src], check=True, capture_output=True)
Image.open(out).crop((0, 0, W * 2, H * 2)).save(out)
print(out)
