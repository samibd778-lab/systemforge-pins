"""Life Bundle pins in the "Complete Notion Planner" ad style (1000x1500, rendered 2x).
Hub list with pastel icons + real screenshots + badges. Only facts from pin-products.json.
Usage: python3 generator/v3/bundle_complete_pins.py -> pins/v5/v6-bundle-a.png, v6-bundle-b.png, /tmp/bundle-preview.jpg"""
import os, subprocess, sys, tempfile
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); import mini_listing as M  # noqa: E402
F = R + '/generator/remotion/public'; S = R + '/shots'

HUBS = [  # icon, name, line, pastel
    ('✓', 'Habit Tracker', 'Your score fills in by itself', '#E7DDF3'),
    ('$', 'Budget Planner', 'Bills, savings & debt payoff', '#DCEFE4'),
    ('✎', 'Daily Journal', 'Mood, one win, one thank you', '#F7DFE3'),
    ('★', 'Life Planner', 'Goals, steps & vision board', '#FBE8D3'),
    ('◐', 'Meal Planner', 'Your week + grocery list', '#E3EEDA'),
    ('✈', 'Travel Planner', 'Countdown, bookings, packing', '#DDEAF5'),
    ('◎', 'Job Tracker', 'Wishlist to Offer + emails', '#F1E6D8'),
    ('◇', 'Second Brain', 'Projects, tasks & notes', '#E6E3F2'),
]
VARIANTS = [
    ('v6-bundle-a', 'ALL-IN-ONE · 8 TEMPLATES', 'The Complete<br>Notion Life Planner', 'Eight planners, already connected.', '#F4EDE4', '#C9A27E', '#3B3129'),
    ('v6-bundle-b', '8 PLANNERS · 1 HOME PAGE', 'Your Whole Life<br>in One Notion Page', 'Habits, money, meals, goals and more.', '#FBF0F0', '#D88A93', '#3A2A2E'),
]
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1000px;height:1500px;font-family:Inter;overflow:hidden}
.w{position:relative;width:1000px;height:1500px;padding:54px 46px 0}
.pill{display:table;margin:0 auto;padding:10px 26px;border-radius:40px;font-size:19px;font-weight:700;letter-spacing:4px}
h1{font-family:"Playfair Display";font-weight:700;font-size:74px;line-height:1.04;text-align:center;margin-top:20px}
.sub{font-family:"Great Vibes";font-size:50px;text-align:center;margin-top:4px}
.main{display:flex;gap:26px;margin-top:30px}
.hubs{width:372px;display:flex;flex-direction:column;gap:12px}
.hub{display:flex;align-items:center;gap:14px;background:#fff;border-radius:16px;padding:12px 14px;box-shadow:0 4px 14px rgba(60,40,30,.07)}
.ic{width:46px;height:46px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:700;flex:none}
.hn{font-size:20px;font-weight:700;letter-spacing:.5px;text-transform:uppercase}
.hl{font-size:16.5px;font-weight:500;opacity:.72;margin-top:2px}
.shots{flex:1;display:flex;flex-direction:column;gap:16px}
.shot{background:#fff;border-radius:18px;padding:10px;box-shadow:0 8px 24px rgba(60,40,30,.12)}
.shot img{width:100%;display:block;border-radius:10px;border:1px solid #EEE6DC}
.cap{font-size:16px;font-weight:700;margin:2px 4px 8px;opacity:.8}
.cta{display:table;margin:30px auto 0;padding:20px 54px;border-radius:50px;color:#fff;font-size:28px;font-weight:700;letter-spacing:1.5px}
.badges{position:absolute;left:0;right:0;bottom:0;height:96px;background:#fff;display:flex;align-items:center;justify-content:space-around;font-size:18px;font-weight:700;padding:0 20px}
.badges span:before{content:"✓";margin-right:8px}
"""

def fonts():
    return ''.join(f'@font-face{{font-family:{f};{w}src:url(file://{F}/{n}.woff2)}}' for f, w, n in [
        ('"Great Vibes"', '', 'greatvibes400'), ('"Playfair Display"', 'font-weight:700;', 'playfair700'),
        ('Inter', 'font-weight:500;', 'inter500'), ('Inter', 'font-weight:700;', 'inter700')])

tmp = tempfile.mkdtemp(); ims = []
for pid, pill, title, sub, bg, accent, ink in VARIANTS:
    hubs = ''.join(f'<div class="hub"><div class="ic" style="background:{c};color:{ink}">{i}</div><div><div class="hn" style="color:{ink}">{n}</div><div class="hl" style="color:{ink}">{l}</div></div></div>' for i, n, l, c in HUBS)
    shots = ''.join(f'<div class="shot"><div class="cap" style="color:{ink}">{c}</div><img src="file://{S}/{s}"></div>' for c, s in [
        ('One home page for everything', 'hd3/bundle-home.jpg'), ('Habit Tracker', 'hd/habit-week.jpg'), ('Budget Planner', 'hd/budget-categories.jpg')])
    html = (f'<html><head><style>{fonts()}{CSS}</style></head><body style="background:{bg};color:{ink}"><div class="w">'
            f'<div class="pill" style="background:{accent}33;color:{ink}">✦ {pill} ✦</div><h1>{title}</h1><div class="sub" style="color:{accent}">{sub}</div>'
            f'<div class="main"><div class="hubs">{hubs}</div><div class="shots">{shots}</div></div>'
            f'<div class="cta" style="background:{accent}">SEE ALL 8 INSIDE ›</div>'
            f'<div class="badges" style="color:{ink}"><span>3-step start</span><span>7 bonus PDF guides</span><span>Phone, tablet &amp; desktop</span><span>Instant download</span></div>'
            f'</div></body></html>')
    f = f'{tmp}/{pid}.html'; open(f, 'w').write(html)
    subprocess.run([M.L.B.CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=2', '--window-size=1000,1500', '--virtual-time-budget=3000', f'--screenshot={f}.png', 'file://' + f],
                   capture_output=True, check=True)
    im = Image.open(f + '.png').crop((0, 0, 2000, 3000)).convert('RGB'); im.save(f'{R}/pins/v5/{pid}.png', optimize=True)
    ims.append(im.resize((600, 900)))
s = Image.new('RGB', (1200, 900), 'white')
for k, im in enumerate(ims): s.paste(im, (k * 600, 0))
s.save('/tmp/bundle-preview.jpg'); print('ok')
