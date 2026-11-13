"""Life Bundle listing images (Etsy 2700x2025, 4:3) from real template crops.
Run: python3 generator/v3/bundle_listing.py -> etsy/bundle/01-hero.jpg ... 10-bonus.jpg"""
import os, subprocess, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); import mini_listing as M  # noqa: E402
F = R + '/generator/remotion/public'; HD = R + '/shots/hd3'; OUT = R + '/etsy/bundle'; TMP = OUT + '/_tmp'
os.makedirs(TMP, exist_ok=True)
W, H = 1350, 1013
FONTS = (f"@font-face{{font-family:GV;src:url(file://{F}/greatvibes400.woff2)}}@font-face{{font-family:PF;font-weight:700;src:url(file://{F}/playfair700.woff2)}}"
         f"@font-face{{font-family:IN;font-weight:500;src:url(file://{F}/inter500.woff2)}}@font-face{{font-family:IN;font-weight:700;src:url(file://{F}/inter700.woff2)}}")
INK, MUT, BG = '#2E2A25', '#6A625A', '#F4EFE8'

def crop(n, box):
    p = f'{TMP}/{n}-{box[0]}-{box[1]}-{box[2]}-{box[3]}.jpg'
    Image.open(f'{HD}/{n}.jpg').convert('RGB').crop(box).save(p, quality=93); return p

def render(body, name):
    hp = f'{TMP}/_r.html'
    open(hp, 'w').write(f"<!doctype html><html><head><meta charset='utf-8'><style>{FONTS}body{{margin:0}}*{{box-sizing:border-box}}</style></head><body>"
                        f"<div style='position:relative;width:{W}px;height:{H}px;background:{BG};font-family:IN;overflow:hidden'>{body}</div></body></html>")
    subprocess.run([M.L.B.CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', '--force-device-scale-factor=2',
                    f'--window-size={W},{H + 200}', '--virtual-time-budget=3000', f'--screenshot={hp}.png', 'file://' + hp], check=True, capture_output=True)
    Image.open(hp + '.png').crop((0, 0, 2700, 2025)).convert('RGB').save(f'{OUT}/{name}.jpg', quality=92); print(name)

T = [  # name, icon, accent, crop, box, bullets
 ('Habit Tracker', '✔️', '#B0643C', 'habit-week', (0, 0, 1180, 600), ['Tick 6 habits a day in 10 seconds', 'Your score and day type fill in by themselves', 'A bar for every habit each month, and your perfect days']),
 ('Budget Planner', '💰', '#3F7D5C', 'budget-cats', (0, 0, 1150, 865), ['Your budget per category, what you spent and what is left', 'Every bill with its due day: paid, due soon or late', 'Savings goals and a debt payoff plan']),
 ('Meal Planner', '🥗', '#5E7F5A', 'meal-recipes', (0, 0, 1345, 1228), ['Breakfast, lunch and dinner for the next 7 days', 'Your recipes with time, rating and tags', 'A grocery list sorted by aisle']),
 ('Daily Journal', '📓', '#8A6A9C', 'journal-entries', (0, 0, 1345, 1198), ['Mood, energy, one win and one thank you a day', 'A weekly review every Sunday', 'Your average mood, great days and low days each month']),
 ('Life Planner', '🌅', '#7A5BA6', 'life-goals', (0, 0, 1536, 973), ['Goals with progress bars that fill as you go', 'Milestones with dates. Late steps show first', 'A vision board with a photo for every dream']),
 ('Travel Planner', '✈️', '#2F6E8E', 'travel-trips', (0, 0, 1000, 730), ['Countdown, budget left and packing for every trip', 'Plans still to book, with the date', 'A packing list linked to your trip']),
 ('Job Application Tracker', '💼', '#3E6A8A', 'job-pipeline', (0, 0, 920, 815), ['Every job from Wishlist to Offer', 'The next step shows on every card', 'Follow-up emails, interview prep and a salary script']),
 ('Second Brain OS', '🧠', '#6B5B4B', 'sb-goals', (0, 0, 1150, 685), ['Goals, projects, tasks and notes linked together', 'Project bars fill up as you tick tasks', 'Weekly, monthly and yearly reviews']),
]

def tile(lab, n, box, h):
    p = crop(n, box)
    return (f"<div style='background:#fff;border:1px solid #E5DDD2;border-radius:14px;overflow:hidden;box-shadow:0 6px 16px rgba(60,40,20,.08)'>"
            f"<div style='height:{h}px;background:url(file://{p}) top left/cover no-repeat'></div><div style='font:700 17px IN;color:{INK};padding:9px 12px'>{lab}</div></div>")

GRID_BOX = {'habit-week': (0, 0, 1180, 600), 'budget-cats': (0, 0, 1150, 600), 'meal-recipes': (0, 200, 1345, 900), 'journal-entries': (0, 250, 1345, 950),
            'life-vision': (0, 280, 1345, 980), 'travel-trips': (0, 0, 1000, 600), 'job-pipeline': (0, 150, 920, 700), 'sb-projects': (0, 0, 920, 600)}
GRID = [('Habit Tracker', 'habit-week'), ('Budget Planner', 'budget-cats'), ('Meal Planner', 'meal-recipes'), ('Daily Journal', 'journal-entries'),
        ('Life Planner', 'life-vision'), ('Travel Planner', 'travel-trips'), ('Job Tracker', 'job-pipeline'), ('Second Brain', 'sb-projects')]
chips = ''.join(f"<span style='font:700 15px IN;color:{INK};background:#fff;border:1px solid #E2D6C6;border-radius:30px;padding:8px 14px'>{t}</span>"
                for t in ['8 templates', '7 bonus PDFs', 'Instant download'])
hero = (f"<div style='position:absolute;left:70px;top:150px;width:470px'><div style='font:700 18px IN;letter-spacing:6px;color:#A0643C'>NOTION TEMPLATE BUNDLE</div>"
        f"<div style='font:120px/1 GV;color:{INK};margin-top:16px'>Life Bundle</div>"
        f"<div style='font:500 27px/1.4 IN;color:{MUT};margin-top:22px'>Habits, money, meals, journal, goals, trips, job search and notes. All in one Notion page.</div>"
        f"<div style='display:flex;gap:10px;flex-wrap:wrap;margin-top:28px'>{chips}</div></div>"
        f"<div style='position:absolute;left:580px;top:60px;width:710px;display:grid;grid-template-columns:repeat(4,1fr);gap:14px'>"
        + ''.join(tile(l, n, GRID_BOX[n], 330) for l, n in GRID) + "</div>")
render(hero, '01-hero')

for i, (name, icon, acc, n, box, bullets) in enumerate(T, 2):
    p = crop(n, box); im = Image.open(p); ratio = im.width / im.height
    iw = 820; ih = min(820, round(iw / ratio)); iw = round(ih * ratio) if ih == 820 else iw
    bl = ''.join(f"<div style='display:flex;gap:12px;margin-top:18px;font:500 24px/1.35 IN;color:{INK}'><span style='color:{acc};font-weight:700'>✓</span><span>{b}</span></div>" for b in bullets)
    body = (f"<div style='position:absolute;left:0;top:0;width:430px;height:{H}px;background:{acc}'></div>"
            f"<div style='position:absolute;left:60px;top:110px;width:330px;color:#fff'><div style='font:700 17px IN;letter-spacing:5px;opacity:.85'>TEMPLATE {i - 1} OF 8</div>"
            f"<div style='font:56px/1 sans-serif;margin-top:26px'>{icon}</div><div style='font:700 50px/1.1 PF;margin-top:16px'>{name}</div></div>"
            f"<div style='position:absolute;left:60px;top:560px;width:330px;color:#fff'>{bl.replace(INK, '#fff').replace(acc, '#fff')}</div>"
            f"<div style='position:absolute;left:{430 + (920 - iw) // 2}px;top:{(H - ih) // 2}px;width:{iw}px;height:{ih}px;background:#fff url(file://{p}) 0 0/{iw}px {ih}px no-repeat;"
            f"border-radius:14px;box-shadow:0 18px 44px rgba(40,30,20,.18);border:1px solid #E5DDD2'></div>"
            f"<div style='position:absolute;right:30px;bottom:22px;font:700 14px IN;letter-spacing:3px;color:#8A847D'>LIFE BUNDLE · SYSTEMFORGE</div>")
    render(body, f'{i:02d}-{name.split()[0].lower()}')

guides = ['30-Day Habit Reset', 'Money Reset in 7 Days', 'Eat Well, Stress Less', 'Journaling guide', 'The 90-Day Goal Workbook', 'Plan Trips Like a Pro', '30-Day Job Search Playbook']
home = crop('bundle-home', (0, 0, 1520, 580))
bonus = (f"<div style='position:absolute;left:60px;top:60px;width:560px'><div style='font:700 18px IN;letter-spacing:6px;color:#A0643C'>ALSO INCLUDED</div>"
         f"<div style='font:700 46px/1.1 PF;color:{INK};margin-top:14px'>7 bonus PDF guides</div>"
         + ''.join(f"<div style='margin-top:14px;font:500 24px IN;color:{INK}'>🎁&nbsp; {g}</div>" for g in guides) + "</div>"
         f"<div style='position:absolute;left:660px;top:60px;width:630px'><div style='font:700 18px IN;letter-spacing:6px;color:#A0643C'>HOW IT WORKS</div>"
         + ''.join(f"<div style='margin-top:16px;background:#fff;border:1px solid #E5DDD2;border-radius:14px;padding:16px 20px;font:500 22px/1.35 IN;color:{INK}'><b style='font-family:PF;color:#A0643C;font-size:28px'>{k}</b>&nbsp; {t}</div>"
                   for k, t in [('1', 'Download the PDF from your Etsy purchases'), ('2', 'Open the link and click Duplicate in Notion'), ('3', 'Pick one template from the menu and start')]) + "</div>"
         f"<div style='position:absolute;left:660px;top:560px;width:630px;height:241px;background:#fff url(file://{home}) 0 0/630px 241px no-repeat;border-radius:14px;"
         f"box-shadow:0 14px 36px rgba(40,30,20,.16);border:1px solid #E5DDD2'></div>"
         f"<div style='position:absolute;left:60px;bottom:60px;width:560px;font:500 20px/1.4 IN;color:{MUT}'>Needs a Notion account. Works on desktop, tablet and phone. Digital download.</div>")
render(bonus, '10-bonus')
for f in os.listdir(TMP): os.remove(os.path.join(TMP, f))
os.rmdir(TMP)
