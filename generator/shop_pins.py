"""SystemForge Shop (Etsy Pinterest) pins for the 11 new products, 2026-11-27.
2 per product: a hook pin (short line + real screen + zoom card + "Get the template") like the account's best pin,
and a value pin from the product's bonus guide. Straight layout, Playfair caps, lining numbers (no Fraunces, no tilt).
Run: python3 generator/shop_pins.py  ->  pins/shop/<p>-hook.png, pins/shop/<p>-tip.png (2000x3000)"""
import json, os, subprocess, pathlib, sys
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import newyear_pins as NY  # CSS, layouts, fonts

R = NY.R
SCR = R / 'generator/v4/scr'
OUT = R / 'pins/shop'
OUT.mkdir(parents=True, exist_ok=True)
u = NY.u


def theme(p):
    c = json.load(open(R / f'generator/v4/products/{p}.json'))['colors']
    return dict(bg=c['bg'], ink=c['ink'], acc=c['accent'], soft='#FFFFFF', muted=c['muted'])


def zoomcard(p, zoom, T):
    f = SCR / p / ('z-' + zoom + '.png')
    w, h = Image.open(f).size
    cw = min(w, 760)                      # keep the left part so it shows bigger
    W = 900
    sc = W / cw
    return (f'<div style="position:absolute;left:50px;top:900px;width:{W}px;height:{min(int(h*sc), 400)}px;overflow:hidden;'
            f'border-radius:16px;background:#fff;box-shadow:0 22px 50px rgba(0,0,0,.22);border:3px solid {T["acc"]}">'
            f'<img src="{u(f)}" style="width:{int(w*sc)}px;display:block"></div>')


def hook(p, kick, title, sub, screen, zoom):
    T = theme(p)
    return f'''<body style="background:{T['bg']};color:{T['ink']}">
<div style="position:absolute;left:70px;right:70px;top:80px;text-align:center">
<div class="kick" style="color:{T['acc']}">{kick}</div>
<h1 style="font-size:84px;margin-top:20px">{title}</h1>
<div style="margin-top:22px;font-size:31px;line-height:1.4;color:{T['muted']}">{sub}</div></div>
<div style="position:absolute;left:60px;top:470px;width:880px;height:600px;border-radius:18px;overflow:hidden;background:#fff;box-shadow:0 26px 60px rgba(0,0,0,.16)">
<div style="height:34px;background:#F1EEEA;display:flex;gap:9px;align-items:center;padding-left:16px">
<i style="width:12px;height:12px;border-radius:50%;background:#E3A79A"></i><i style="width:12px;height:12px;border-radius:50%;background:#E8CF8E"></i><i style="width:12px;height:12px;border-radius:50%;background:#A9CDA0"></i></div>
<img src="{u(SCR / p / (screen + '.png'))}" style="width:880px;display:block"></div>
{zoomcard(p, zoom, T)}
<div style="position:absolute;left:0;right:0;top:1350px;text-align:center"><span class="badge" style="background:{T['ink']};color:#fff">Get the template &rarr;</span></div>
<div class="foot" style="color:{T['acc']}">SYSTEMFORGE · INSTANT DOWNLOAD</div></body>'''


def add_theme(p):
    T = theme(p)
    NY.THEMES[p] = dict(bg=T['bg'], ink=T['ink'], acc=T['acc'], soft='#FFFFFF')
    return p


PDF = lambda p, n: SCR / p / f'pdf-{n}.png'

P = {}
H = {  # product: (kicker, hook title, sub line, screen, zoom)
    'wedding': ('Wedding planner', 'Know what’s<br>left to pay', 'Your budget, deposits and payments due, all on one page.', 'budget', 'budget'),
    'pregnancy': ('Pregnancy planner', 'Baby shopping,<br>sorted', 'Must-haves, gifts and prices in one list.', 'shop', 'shop'),
    'home': ('Cleaning schedule', 'Know what to<br>clean today', 'Every room, every task, and what’s due next.', 'upnext', 'upnext'),
    'fitness': ('Workout planner', 'Watch your<br>lifts go up', 'Your personal bests, saved after every workout.', 'bests', 'bests'),
    'reading': ('Reading journal', 'Hit your yearly<br>reading goal', 'Your reading challenge fills in as you finish books.', 'challenge', 'challenge'),
    'selfcare': ('Self-care planner', 'A 2-minute<br>daily check-in', 'Mood, energy and one small kind thing a day.', 'checkin', 'checkin'),
    'student': ('Student planner', 'Never miss<br>a deadline', 'Everything due this week, by class.', 'due', 'due'),
    'skin': ('Skincare routine', 'Your skincare<br>routine, in order', 'Morning, evening and weekly, all in one place.', 'routine', 'routine'),
    'wardrobe': ('Capsule wardrobe', 'Your outfits,<br>ready to wear', 'Save the outfits you love and wear them again.', 'outfits', 'outfits'),
    'family': ('Mom & family planner', 'Chores kids<br>can follow', 'A chore chart with rewards they work for.', 'chores', 'chores'),
    'cycle': ('Cycle tracker', 'Your cycle day<br>at a glance', 'Log your day in one minute and spot your patterns.', 'today', 'today'),
}
for p, (k, t, s, sc, z) in H.items():
    P[f'{p}-hook'] = hook(p, k, t, s, sc, z)

for p in H:
    add_theme(p)
P['wedding-tip'] = NY.grid('wedding', 'Wedding planning checklist', 'A 12-month wedding timeline', [
    ('🏡 12–9 months', ['Budget and guest list', 'Book the venue', 'Book photographer', 'Book the caterer']),
    ('💐 9–4 months', ['Save-the-dates', 'Florist and music', 'Dress or suit', 'Cake tasting']),
    ('✉️ 3–1 months', ['Send invitations', 'Final headcount', 'Seating chart', 'Last fittings']),
    ('💍 The week of', ['Confirm all vendors', 'Pack the kit', 'Share the schedule', 'Rest']),
], img=PDF('wedding', 1))
P['pregnancy-tip'] = NY.grid('pregnancy', 'Pregnancy checklist', 'Your trimester checklist', [
    ('🌱 1st trimester', ['Book first visit', 'Add your due date', 'Start a baby budget', 'Write your questions']),
    ('🛍️ 2nd trimester', ['Make a shopping list', 'Sign up for a class', 'Plan the nursery', 'Pick a pediatrician']),
    ('👜 3rd trimester', ['Pack the hospital bag', 'Install the car seat', 'Freeze some meals', 'Tour the hospital']),
    ('👶 After birth', ['Log feeds and sleep', 'Accept help', 'Book baby checkups', 'Rest when you can']),
], img=PDF('pregnancy', 1))
P['home-tip'] = NY.grid('home', 'Cleaning checklist', 'Daily, weekly, monthly cleaning schedule', [
    ('☀️ Every day', ['Make the beds', 'Wipe counters', 'Dishes', 'One load of laundry']),
    ('📅 Every week', ['Bathroom', 'Floors', 'Bed sheets', 'Dusting']),
    ('📆 Every month', ['Fridge', 'Washer filter', 'Under the beds', 'Test alarms']),
    ('🍂 Every season', ['Furnace filter', 'Oven', 'Baseboards', 'Pillows']),
], img=PDF('home', 1))
P['fitness-tip'] = NY.grid('fitness', 'Workout plans for women', '4 rules to get stronger without guessing', [
    ('📈 Do a bit more', ['Add a little weight, one rep or one set over time']),
    ('🔁 Repeat the basics', ['Squat, hinge, push, pull, carry, done often']),
    ('📝 Write it down', ['Log the weights so you know what to try next']),
    ('📅 Show up', ['3 workouts a week for 3 months beat 6 a week for 3 weeks']),
], img=PDF('fitness', 1))
P['reading-tip'] = NY.steps('reading', 'Reading journal ideas', 'How to find time to read more', [
    ('10 pages a day', 'That’s about a dozen books a year.'),
    ('Before bed', 'Swap 15 minutes of scrolling for a book.'),
    ('In the gaps', 'Lunch, the bus, waiting rooms: keep a book with you.'),
    ('Listen', 'Audiobooks for walks, chores and drives count.'),
    ('Phone away', 'Out of the room while you read.'),
])
P['selfcare-tip'] = NY.grid('selfcare', 'Self care ideas', '6 small self-care basics for every day', [
    ('😴 Sleep', ['Aim for 7 hours or more', 'Same bedtime most nights']),
    ('💧 Water & 🚶 move', ['Keep a bottle where you see it', 'A walk, a stretch, a dance']),
    ('🌳 Outside', ['A few minutes of fresh air and daylight']),
    ('📵 Screen-free hour', ['One hour a day with the phone in another room', 'Plus one small ritual']),
], img=PDF('selfcare', 1))
P['student-tip'] = NY.steps('student', 'Study tips', '5 study methods that actually work', [
    ('Active recall', 'Close the book, write what you remember, then check.'),
    ('Spaced reviews', 'Review a topic over days and weeks, not 5 times in one night.'),
    ('Pomodoro', '25 minutes of focus, 5 minutes of break.'),
    ('Practice problems', 'Without the solution, with a timer.'),
    ('Teach it', 'Explain it in simple words. Where you get stuck is what to study next.'),
])
P['skin-tip'] = NY.grid('skin', 'Skincare routine order', 'Skincare routine order, thin to thick', [
    ('☀️ Morning', ['Cleanser', 'Toner', 'Serum', 'Moisturizer', 'Sunscreen']),
    ('🌙 Evening', ['Remove makeup', 'Cleanser', 'Serum', 'Moisturizer']),
    ('✨ Weekly', ['Exfoliate 1–2x', 'Face mask', 'Wash brushes', 'Fresh pillowcase']),
    ('⏱️ Short on time', ['Cleanse', 'Moisturize', 'Sunscreen (AM)']),
], img=PDF('skin', 1))
P['wardrobe-tip'] = NY.grid('wardrobe', 'Capsule wardrobe checklist', 'The 30-piece capsule wardrobe', [
    ('👕 9 tops', ['Tees, shirts, sweaters, one blouse']),
    ('👖 6 bottoms', ['Jeans, trousers, a skirt, something comfy']),
    ('👗 3 dresses', ['Casual, smart, going out']),
    ('🧥 4 layers', ['Coat, blazer, jacket, cardigan']),
    ('👟 5 shoes', ['Sneakers, boots, flats, sandals, heels']),
    ('👜 3 extras', ['A tote, a small bag, a scarf']),
])
P['family-tip'] = NY.grid('family', 'Chore chart for kids', 'Chores kids can do, by age', [
    ('🧸 Ages 3–5', ['Put toys away', 'Feed a pet', 'Match socks']),
    ('🛏️ Ages 6–8', ['Make the bed', 'Set the table', 'Water plants']),
    ('🧺 Ages 9–12', ['Fold laundry', 'Take out trash', 'Help cook']),
    ('🧽 Teens', ['Do laundry', 'Clean the bathroom', 'Cook a meal']),
], img=PDF('family', 1))
P['cycle-tip'] = NY.grid('cycle', 'Cycle tracker ideas', 'The 4 phases of your cycle, a simple map', [
    ('🩸 Period', ['Warm drinks', 'Gentle movement', 'Early nights']),
    ('🌱 Follicular', ['Start new things', 'Plan the month', 'Try a new workout']),
    ('🌕 Ovulation', ['Big tasks', 'Time with friends', 'Note how you feel']),
    ('🌙 Luteal', ['Lighter days', 'Extra sleep', 'Be kind to yourself']),
], note='Every body is different. Phases are estimates.', img=PDF('cycle', 1))

if __name__ == '__main__':
    only = sys.argv[1:]
    tmp = OUT / '_t.html'
    for k, body in P.items():
        if only and k not in only:
            continue
        tmp.write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{NY.CSS}</style></head>{body}</html>')
        full = OUT / f'{k}_full.png'
        subprocess.run([NY.CH, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                        '--allow-file-access-from-files', '--force-device-scale-factor=2', '--window-size=1000,1500',
                        f'--screenshot={full}', tmp.as_uri()], check=True, capture_output=True)
        Image.open(full).convert('RGB').crop((0, 0, 2000, 3000)).save(OUT / f'{k}.png', optimize=True)
        full.unlink()
    tmp.unlink()
    print('ok', len(P))
