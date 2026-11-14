"""Gumroad cover (1280x720 @2x) + thumb (600x600 @2x) for each free printable, from its real PDF pages.
Run after printables.py: python3 generator/printables_gumroad.py -> dl/free/gumroad/<key>-cover.jpg, <key>-thumb.jpg"""
import os, subprocess, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import printables as P  # noqa: E402
sys.path.insert(0, os.path.join(HERE, 'v3')); import mini_listing as M  # noqa: E402
OUT = os.path.join(P.OUT, 'gumroad'); os.makedirs(OUT, exist_ok=True)

def render(html, w, h, out):
    hp = os.path.join(OUT, '_r.html')
    open(hp, 'w').write(f"<!doctype html><html><head><meta charset='utf-8'><style>{P.FONTS}body{{margin:0}}</style></head><body>{html}</body></html>")
    subprocess.run([M.L.B.CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=2', f'--window-size={w},{h + 200}', '--virtual-time-budget=3000', f'--screenshot={hp}.png', 'file://' + hp],
                   check=True, capture_output=True)
    Image.open(hp + '.png').crop((0, 0, w * 2, h * 2)).convert('RGB').save(out, quality=92)
    os.remove(hp); os.remove(hp + '.png'); print(out)

sh = 'box-shadow:0 18px 40px rgba(40,40,40,.22);border-radius:5px;position:absolute'
for k, s in P.SETS.items():
    p1 = os.path.join(P.OUT, f"{s['file']}-p-1.png"); p2 = os.path.join(P.OUT, f"{s['file']}-p-2.png")
    cover = (f"<div style='position:relative;width:1280px;height:720px;overflow:hidden;background:{s['bg']};font-family:IN'>"
             f"<div style='position:absolute;left:70px;top:170px;width:560px'>"
             f"<div style='font:700 20px IN;letter-spacing:7px;color:{s['acc']}'>FREE PRINTABLE</div>"
             f"<div style='font:{110 if len(s['title']) <= 13 else 92}px/1.05 GV;color:#2E2A25;margin-top:14px'>{s['title']}</div>"
             f"<div style='font:500 28px/1.4 IN;color:#5F5A55;margin-top:20px'>{s['sub']}</div>"
             f"<div style='font:700 20px IN;color:#3B2A1E;margin-top:26px'>PDF · US Letter · print at home</div></div>"
             f"<img src='file://{p2}' style='{sh};left:880px;top:90px;width:340px;transform:rotate(6deg)'>"
             f"<img src='file://{p1}' style='{sh};left:690px;top:60px;width:440px;transform:rotate(-3deg)'></div>")
    render(cover, 1280, 720, os.path.join(OUT, f'{k}-cover.jpg'))
    thumb = (f"<div style='position:relative;width:600px;height:600px;overflow:hidden;background:{s['bg']};font-family:IN'>"
             f"<div style='position:absolute;top:28px;width:600px;text-align:center;font:700 15px IN;letter-spacing:5px;color:{s['acc']}'>FREE PRINTABLE</div>"
             f"<div style='position:absolute;top:50px;width:600px;text-align:center;font:{76 if len(s['title']) <= 13 else 64}px/1.1 GV;color:#2E2A25'>{s['title']}</div>"
             f"<img src='file://{p1}' style='{sh};left:150px;top:170px;width:300px'></div>")
    render(thumb, 600, 600, os.path.join(OUT, f'{k}-thumb.jpg'))
