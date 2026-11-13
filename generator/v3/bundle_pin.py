"""Life Bundle images: pin (1000x1500 @2x) and Gumroad cover (1280x720 @2x) + square thumb, from real crops.
Run: python3 generator/v3/bundle_pin.py -> pins/v5/bundle-a1.png, dl/bundle/cover.jpg, dl/bundle/thumb.jpg"""
import os, subprocess, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); import mini_listing as M  # noqa: E402
F = R + '/generator/remotion/public'; HD = R + '/shots/hd3'; TMP = R + '/dl/bundle/_tmp'
os.makedirs(TMP, exist_ok=True)
FONTS = (f"@font-face{{font-family:GV;src:url(file://{F}/greatvibes400.woff2)}}@font-face{{font-family:PF;font-weight:700;src:url(file://{F}/playfair700.woff2)}}"
         f"@font-face{{font-family:IN;font-weight:500;src:url(file://{F}/inter500.woff2)}}@font-face{{font-family:IN;font-weight:700;src:url(file://{F}/inter700.woff2)}}")
TILES = [('Habit Tracker', 'habit-week', (0, 0, 1180, 600)), ('Budget Planner', 'budget-cats', (0, 0, 1150, 600)),
         ('Meal Planner', 'meal-recipes', (0, 200, 1345, 900)), ('Daily Journal', 'journal-entries', (0, 250, 1345, 950)),
         ('Life Planner', 'life-vision', (0, 280, 1345, 980)), ('Travel Planner', 'travel-trips', (0, 0, 1000, 600)),
         ('Job Tracker', 'job-pipeline', (0, 150, 920, 700)), ('Second Brain', 'sb-projects', (0, 0, 920, 600))]

def tiles(w, h):
    out = ''
    for i, (lab, n, box) in enumerate(TILES):
        p = f'{TMP}/{n}.jpg'; Image.open(f'{HD}/{n}.jpg').convert('RGB').crop(box).save(p, quality=92)
        out += (f"<div style='background:#fff;border:1px solid #E5DDD2;border-radius:14px;overflow:hidden;box-shadow:0 6px 16px rgba(60,40,20,.08)'>"
                f"<div style='height:{h}px;background:url(file://{p}) top left/cover no-repeat'></div>"
                f"<div style='font:700 {max(15, w // 14)}px IN;color:#2E2A25;padding:8px 12px'>{lab}</div></div>")
    return out

def render(html, w, h, out, jpg=False):
    hp = f'{TMP}/_r.html'; open(hp, 'w').write(f"<!doctype html><html><head><meta charset='utf-8'><style>{FONTS}body{{margin:0}}</style></head><body>{html}</body></html>")
    subprocess.run([M.L.B.CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', '--force-device-scale-factor=2',
                    f'--window-size={w},{h + 200}', '--virtual-time-budget=3000', f'--screenshot={hp}.png', 'file://' + hp], check=True, capture_output=True)
    im = Image.open(hp + '.png').crop((0, 0, w * 2, h * 2)).convert('RGB')
    im.save(out, quality=92) if jpg else im.save(out, optimize=True)
    print(out, im.size)

pin = (f"<div style='position:relative;width:1000px;height:1500px;background:#F4EFE8;font-family:IN;overflow:hidden'>"
       "<div style='position:absolute;top:56px;width:1000px;text-align:center;font:700 24px IN;letter-spacing:8px;color:#A0643C'>NOTION TEMPLATE BUNDLE</div>"
       "<div style='position:absolute;top:92px;width:1000px;text-align:center;font:130px/1.1 GV;color:#2E2A25'>Life Bundle</div>"
       "<div style='position:absolute;top:262px;width:1000px;text-align:center;font:500 32px IN;color:#6A625A'>8 Notion templates + 7 bonus guides</div>"
       f"<div style='position:absolute;left:50px;top:340px;width:900px;display:grid;grid-template-columns:1fr 1fr;gap:18px'>{tiles(441, 190)}</div>"
       "<div style='position:absolute;bottom:34px;width:1000px;text-align:center;font:700 22px IN;letter-spacing:3px;color:#8A847D'>SYSTEMFORGE · INSTANT DOWNLOAD</div></div>")
cover = (f"<div style='position:relative;width:1280px;height:720px;background:#F4EFE8;font-family:IN;overflow:hidden'>"
         "<div style='position:absolute;left:60px;top:120px;width:420px'><div style='font:700 18px IN;letter-spacing:6px;color:#A0643C'>NOTION TEMPLATES</div>"
         "<div style='font:110px/1 GV;color:#2E2A25;margin-top:14px'>Life Bundle</div>"
         "<div style='font:500 26px/1.4 IN;color:#6A625A;margin-top:18px'>8 templates for your habits, money, meals, journal, goals, trips, job search and notes.</div>"
         "<div style='font:700 20px IN;color:#3B2A1E;margin-top:24px'>+ 7 bonus PDF guides</div></div>"
         f"<div style='position:absolute;left:520px;top:40px;width:720px;display:grid;grid-template-columns:repeat(4,1fr);gap:12px'>{tiles(171, 220)}</div></div>")
render(pin, 1000, 1500, R + '/pins/v5/bundle-a1.png')
render(cover, 1280, 720, R + '/dl/bundle/cover.jpg', True)
thumb = ("<div style='position:relative;width:600px;height:600px;background:#F4EFE8;font-family:IN;overflow:hidden'>"
         "<div style='position:absolute;top:26px;width:600px;text-align:center;font:700 14px IN;letter-spacing:5px;color:#A0643C'>8 NOTION TEMPLATES</div>"
         "<div style='position:absolute;top:44px;width:600px;text-align:center;font:84px/1.1 GV;color:#2E2A25'>Life Bundle</div>"
         f"<div style='position:absolute;left:30px;top:170px;width:540px;display:grid;grid-template-columns:repeat(4,1fr);gap:10px'>{tiles(127, 130)}</div></div>")
render(thumb, 600, 600, R + '/dl/bundle/thumb.jpg', True)
for f in os.listdir(TMP): os.remove(os.path.join(TMP, f))
os.rmdir(TMP)
