"""Tall "full dashboard" pins (1000x2100, rendered 2x) in the beige aesthetic-dashboard style.
Real Notion screenshots from shots/hd stacked in cards. Usage: python3 generator/v3/tall_pins.py
Writes pins/v5/v6-<p>-tall.png and /tmp/tall-preview.jpg."""
import os, subprocess, sys, tempfile
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); import mini_listing as M  # noqa: E402
F = R + '/generator/remotion/public'
S = R + '/shots/hd'

SPEC = [
    ('habit', 'My Habit<br>Dashboard', 'Small steps, every day.', 'NOTION HABIT TRACKER',
     [('Today', 'habit-top'), ('Tick your habits', 'habit-week'), ('Your month at a glance', 'habit-monthly')]),
    ('budget', 'My Money<br>Dashboard', 'Know where every dollar goes.', 'NOTION BUDGET PLANNER',
     [('This month', 'budget-top'), ('Budget by category', 'budget-categories'), ('Bills', 'budget-bills'), ('Savings goals', 'budget-savings'), ('Debt payoff', 'budget-debt')]),
    ('journal', 'My Journal<br>Dashboard', 'Two minutes a day.', 'NOTION DAILY JOURNAL',
     [('Today', 'journal-top'), ('Entries', 'journal-entries'), ('Gratitude jar', 'journal-gratitude'), ('Your month', 'journal-monthly')]),
    ('life', 'My 2027 Life<br>Dashboard', 'Make this the year.', 'NOTION LIFE PLANNER',
     [('Home', 'life-top'), ('Vision board', 'life-vision'), ('Goals with progress', 'life-goals'), ('Next steps', 'life-steps')]),
    ('meal', 'My Meal<br>Dashboard', 'Dinner, already planned.', 'NOTION MEAL PLANNER',
     [('Home', 'meal-top'), ('Your week of meals', 'meal-week'), ('Grocery list by aisle', 'meal-buy')]),
    ('travel', 'My Travel<br>Dashboard', 'Your whole trip, one page.', 'NOTION TRAVEL PLANNER',
     [('Home', 'travel-top'), ('Your trips', 'travel-trips'), ('Trip plan', 'travel-trip'), ('Still to book', 'travel-book')]),
    ('job', 'My Job Search<br>Dashboard', 'Never miss a follow-up.', 'NOTION JOB APPLICATION TRACKER',
     [('Home', 'job-top'), ('Job pipeline', 'job-pipeline'), ('Follow up today', 'job-followup'), ('Interviews', 'job-interviews')]),
]

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1000px;height:2100px;background:#F3ECE2;font-family:Inter;color:#3B3129;overflow:hidden}
.wrap{position:relative;width:1000px;height:2100px;padding:56px 50px 150px;display:flex;flex-direction:column}
.kick{font-size:19px;letter-spacing:5px;color:#9C8571;font-weight:700;text-align:center}
h1{font-family:"Playfair Display";font-weight:700;font-size:86px;line-height:1.02;text-align:center;margin-top:16px;color:#3B3129}
.sub{font-family:"Great Vibes";font-size:54px;color:#A0785A;text-align:center;margin-top:6px}
.cards{display:flex;flex-direction:column;justify-content:center;gap:22px;margin-top:30px;flex:1}
.card{background:#FFFDF9;border-radius:22px;padding:14px 14px 16px;box-shadow:0 8px 26px rgba(80,55,30,.10)}
.lab{font-size:20px;font-weight:700;color:#6B5A4B;margin:2px 6px 10px;letter-spacing:.3px}
.lab:before{content:"";display:inline-block;width:9px;height:9px;border-radius:50%;background:#C9A27E;margin-right:10px;vertical-align:middle}
.card img{width:100%;display:block;border-radius:12px;border:1px solid #EEE4D8}
.foot{position:absolute;left:0;right:0;bottom:0;height:120px;background:#3B3129;color:#F3ECE2;display:flex;align-items:center;justify-content:center;gap:26px;font-size:24px;font-weight:500;letter-spacing:.4px}
.foot b{font-weight:700;color:#E8C9A7}
"""

def fonts():
    return ''.join(f'@font-face{{font-family:{f};{w}src:url(file://{F}/{n}.woff2)}}' for f, w, n in [
        ('"Great Vibes"', '', 'greatvibes400'), ('"Playfair Display"', 'font-weight:700;', 'playfair700'),
        ('Inter', 'font-weight:500;', 'inter500'), ('Inter', 'font-weight:700;', 'inter700')])

def fit(cards, room):
    """Drop cards from the end until the stacked screenshots fit in the room (px at 1000 wide)."""
    def h(cs):
        return sum(Image.open(f'{S}/{s}.jpg').size[1] * 872 / Image.open(f'{S}/{s}.jpg').size[0] + 64 for _, s in cs) + 22 * (len(cs) - 1)
    while len(cards) > 2 and h(cards) > room:
        cards = cards[:-1]
    return cards, h(cards)

tmp = tempfile.mkdtemp(); ims = []
for p, title, sub, kick, cards in SPEC:
    cards, used = fit(cards, 2100 - 120 - 56 - 330 - 40)
    body = ''.join(f'<div class="card"><div class="lab">{l}</div><img src="file://{S}/{s}.jpg"></div>' for l, s in cards)
    html = (f'<html><head><style>{fonts()}{CSS}</style></head><body><div class="wrap">'
            f'<div class="kick">{kick}</div><h1>{title}</h1><div class="sub">{sub}</div>'
            f'<div class="cards">{body}</div>'
            f'<div class="foot"><span>Instant download</span><span>·</span><span><b>Real Notion template</b></span><span>·</span><span>Tap to see inside</span></div>'
            f'</div></body></html>')
    f = f'{tmp}/{p}.html'; open(f, 'w').write(html)
    subprocess.run([M.L.B.CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=2', '--window-size=1000,2100', '--virtual-time-budget=3000', f'--screenshot={f}.png', 'file://' + f],
                   capture_output=True, check=True)
    im = Image.open(f + '.png').crop((0, 0, 2000, 4200)).convert('RGB')
    im.save(f'{R}/pins/v5/v6-{p}-tall.png', optimize=True)
    print(p, len(cards), 'cards', int(used), 'px')
    ims.append(im.resize((300, 630)))
s = Image.new('RGB', (300 * len(ims), 630), 'white')
for k, im in enumerate(ims): s.paste(im, (k * 300, 0))
s.save('/tmp/tall-preview.jpg')
