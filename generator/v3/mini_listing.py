"""Listing images for the 3 small trackers (habit, journal, budget) in the v3 lifestyle style.
Shots: shots/hd/<p>-<section>.jpg (real captures, no store names in them).
10 images: main, 4 lifestyle features, 2 flat features, inside, how it works, bonus.
Usage: python3 generator/v3/mini_listing.py [--gumroad] [habit journal budget]"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_listing as L
import sb_listing_v3 as SBL
from PIL import Image

B = L.B
HD = B.HD
CR = os.path.join(L.ROOT, 'canva', 'v3', 'crops')


def reg(name, im):
    p = os.path.join(CR, name + '.png'); im.save(p)
    B.CROPS[name] = ('-', (0, 0, 1, 1)); B._cache[name] = p


def shot(n):
    return Image.open(os.path.join(HD, n + '.jpg')).convert('RGB')


def stack(names, ar=1.6, top=0):
    """screen for a laptop: shots stacked, cropped to the screen ratio"""
    ims = [shot(n) for n in names]; w = ims[0].width
    c = Image.new('RGB', (w, sum(i.height for i in ims)), 'white'); y = 0
    for i in ims:
        c.paste(i.resize((w, int(i.height * w / i.width))), (0, y)); y += i.height
    h = int(w / ar)
    out = Image.new('RGB', (w, h), 'white'); out.paste(c.crop((0, top, w, min(c.height, top + h))), (0, 0))
    return out


def box(n, x0, y0, x1, y1):
    return shot(n).crop((x0, y0, x1, y1))


PROD = {
 'habit': dict(name='Habit Tracker', kicker='NOTION HABIT TRACKER', color='#F1E4D8', accent='#C26A3D',
   sub='Tick your habits every day.<br>Your score fills in by itself.',
   features=['Daily check-in with a score', 'A progress bar for every habit', 'Habit calendar + year review', 'Bonus: 30-Day Habit Reset'],
   screens={'lap': ['habit-top', 'habit-week'], 's1': ['habit-week'], 's2': ['habit-monthly'], 's3': ['habit-calendar'], 's4': ['habit-plan', 'habit-year']},
   cards=[('Tick, and your score fills in', 'Six habits, one row per day. Your score and day type show up by themselves.', ('habit-week', 0, 0, 1380, 535)),
          ('A bar for every habit', 'Every month gets a bar per habit, your best habit and your perfect days.', ('habit-monthly', 0, 0, 700, 605)),
          ('Your month at a glance', 'A calendar with your score on every day.', ('habit-calendar', 0, 0, 1380, 340)),
          ('A plan for every habit', 'The cue that starts it, the tiny version for busy days and your reward.', ('habit-plan', 0, 0, 1320, 470)),
          ('Start every day clear', 'A live Today widget: the clock, how much of the week, month and year is left, and a habit thought.', ('habit-top', 0, 330, 940, 683)),
          ('Your whole year in one line', 'Overall score, perfect days, days logged and habits done.', ('habit-year', 0, 0, 800, 215))],
   inside=['Home page + live Today widget', 'Daily check-in for 6 habits', 'Score + day type every day', 'Monthly bars for every habit',
           'Best habit + perfect days', 'Habit calendar', 'My habit plan: cue, tiny version, reward', 'Year in review',
           '50 habit ideas + how to make a habit stick', 'Bonus PDF: 30-Day Habit Reset'],
   bonus=('30-Day Habit Reset', 'A 6-page PDF: pick the right habits, the habit loop, a 30-day plan, what to do when you miss a day, and a printable tracker.')),
 'journal': dict(name='Daily Journal', kicker='NOTION DAILY JOURNAL', color='#ECE4EE', accent='#8A6A9C',
   sub='Two minutes a day: your mood,<br>one win and one thank you.',
   features=['Daily entries with mood', 'Weekly + monthly mood review', 'Gratitude jar + mood calendar', 'Bonus: Journaling guide PDF'],
   screens={'lap': ['journal-top', 'journal-entries'], 's1': ['journal-entries'], 's2': ['journal-gratitude'], 's3': ['journal-monthly', 'journal-calendar'], 's4': ['journal-calendar', 'journal-gratitude']},
   cards=[('One entry a day', 'Mood, energy, one win and one thing you are grateful for. A photo on every card.', ('journal-entries', 0, 0, 1320, 455)),
          ('A gratitude jar', 'Every thank you you wrote, in one place. Open it on a hard day.', ('journal-gratitude', 0, 0, 1320, 512)),
          ('How your month felt', 'Average mood, great days and low days for every month.', ('journal-monthly', 0, 0, 670, 486)),
          ('Your mood calendar', 'See your month at a glance and keep your favorite days.', ('journal-calendar', 0, 0, 1380, 387)),
          ('A prompt for every day', 'A live Today widget with the clock, your month and a new journal prompt each day.', ('journal-top', 0, 280, 1380, 583)),
          ('Your week in one line', 'Five minutes on Sunday. Your average mood and days written fill in by themselves.', ('journal-weekly', 0, 0, 880, 251))],
   inside=['Home page + live Today widget', 'A new journal prompt every day', 'Daily entries: mood, energy, win, gratitude', 'Weekly review with average mood',
           'Monthly mood: great + low days', 'Mood calendar', 'Favorite days', 'Gratitude jar',
           'Daily questions + 60 journal prompts', 'Bonus PDF: Journaling guide'],
   bonus=('Journaling guide', 'A 6-page PDF: the 2-minute habit, 4 ways to journal, your weekly review, prompts for every mood and a printable week page.')),
 'budget': dict(name='Budget Planner', kicker='NOTION BUDGET PLANNER', color='#E2ECE4', accent='#3F7D5C',
   sub='See what is left, never miss<br>a bill, watch your debt go down.',
   features=['Budget left per category', 'Bills with due dates', 'Savings goals + debt payoff', 'Bonus: Money Reset in 7 Days'],
   screens={'lap': ['budget-categories', 'budget-bills'], 's1': ['budget-categories'], 's2': ['budget-bills'], 's3': ['budget-transactions'], 's4': ['budget-savings', 'budget-debt']},
   cards=[('See what is left', 'Every category shows what you spent this month, what is left and if you are on track.', ('budget-categories', 0, 0, 1388, 540)),
          ('Never miss a bill', 'Every bill with its due day. Paid, due soon or late, at a glance.', ('budget-bills', 0, 0, 1000, 430)),
          ('Every dollar, in and out', 'Expenses show with a minus. Pick a category and the budget updates.', ('budget-transactions', 0, 0, 1100, 330)),
          ('Savings goals with a deadline', 'See how much to save each month to hit your goal on time.', ('budget-savings', 0, 0, 1000, 297)),
          ('Your debt-free date', 'Highest interest first. Add an extra payment and see the date move closer.', ('budget-debt', 0, 0, 1380, 285)),
          ('How much you saved', 'Income, spending, what is left over and how much of your income you saved.', ('budget-overview', 0, 0, 1290, 245))],
   inside=['Home page + live Today widget', 'Budget per category (50/30/20)', 'Spent, left + status per category', 'Transactions: money in and out',
           'Bills + subscriptions with due dates', 'Monthly overview + saved %', 'Savings goals: amount per month', 'Debt payoff plan + debt-free date',
           '50/30/20 guide + 25 ways to spend less', 'Bonus PDF: Money Reset in 7 Days'],
   bonus=('Money Reset in 7 Days', 'A 6-page PDF: a 7-day plan, how to pick a budget style, paying off debt faster, a safety cushion and a printable worksheet.')),
}
SCENES = {  # main scene (laptop right), then 4 lifestyle scenes (scene, text side)
 'habit': ('n-habit-a.png', [('n-habit-b.png', 'right'), ('n-habit-b-m.png', 'left'), ('n-habit-a-m.png', 'right'), ('n-habit-a.png', 'left')]),
 'journal': ('n-journal-a.png', [('n-journal-b.png', 'right'), ('n-journal-b-m.png', 'left'), ('n-journal-a-m.png', 'right'), ('n-journal-a.png', 'left')]),
 'budget': ('n-budget-a.png', [('n-budget-b.png', 'right'), ('n-budget-b-m.png', 'left'), ('n-budget-a-m.png', 'right'), ('n-budget-a.png', 'left')]),
}


def setup(pk):
    p = PROD[pk]
    for k, names in p['screens'].items():
        reg(f'{pk}-scr-{k}', stack(names))
    for i, (_, _, b) in enumerate(p['cards'], 1):
        n, x0, y0, x1, y1 = b; im = shot(n); reg(f'c-{pk}-{i}', im.crop((x0, y0, min(x1, im.width), min(y1, im.height))))
    main_scene, _ = SCENES[pk]
    L.P[pk] = dict(name=p['name'], kicker=p['kicker'], color=p['color'], accent=p['accent'], scene=main_scene,
                   screens=[f'{pk}-scr-lap'], sub=p['sub'], features=p['features'],
                   cards=[(t, d, f'c-{pk}-{i}') for i, (t, d, _) in enumerate(p['cards'], 1)][:4], inside=p['inside'])
    SBL.L.P['sb'] = L.P[pk]  # life/phone helpers read P['sb']


def life(pk, n, scene, side, base):
    p = PROD[pk]; t, d, _ = p['cards'][n - 1]
    html = SBL.life_page(n, t, d, scene, f'{pk}-scr-s{n}', f'c-{pk}-{n}', side, False, base)
    return html.replace('sb-', pk + '-').replace('/sb/', f'/{pk}/').replace('Second Brain OS', p['name'])


def flat(pk, n, base):
    p = PROD[pk]; t, d, _ = p['cards'][n - 1]; crop = f'c-{pk}-{n}'
    im0 = Image.open(B.src(crop)); a = im0.width / im0.height
    cw = max(420, min(740, int(840 * a)))
    url, ih = B.fit(crop, cw, 840, f'e{n}'); url = url.replace(B.RAW + 'crops/', base + 'crops/')
    top = max(60, (L.H - ih - 30) // 2)
    inner = (L.blobs(p['accent'])
             + f'<p style="position:absolute;left:70px;top:150px;width:64px;margin:0;padding:12px 0;text-align:center;border-radius:999px;background:{p["accent"]};color:{L.PAP};font-size:30px;font-weight:700">{n}</p>'
             + L.T(70, 250, 470, t, 60, f'line-height:1.05;color:{L.INK};{L.SER}')
             + L.T(70, 520, 450, d, 28, f'line-height:1.4;color:{L.MUT}')
             + L.T(70, 900, 450, p['name'], 22, f'font-weight:700;letter-spacing:1px;color:{p["accent"]}')
             + f'<div style="position:absolute;left:{560 + (740 - cw) // 2}px;top:{top}px;width:{cw}px;height:{ih + 30}px;background:#FFFFFF;border-radius:22px;overflow:hidden">'
             + f'<img src="{url}" style="position:absolute;left:0;top:15px;width:{cw}px;height:{ih}px"></div>')
    return L.page(f'{pk}-{n + 1}-feature', inner, None, p['color'])


def bonus(pk):
    p = PROD[pk]; title, desc = p['bonus']
    g = ['file://' + os.path.join(CR, f'{pk}guide-{i}.png') for i in (1, 2, 3)]
    sh = 'box-shadow:0 28px 60px rgba(46,42,37,.28);border-radius:10px'
    inner = (L.blobs(p['accent'])
             + L.T(90, 170, 0, 'BONUS', 22, f'padding:10px 22px;border-radius:999px;background:{p["accent"]};color:{L.PAP};font-weight:700;letter-spacing:3px')
             + L.T(90, 260, 520, title, 60, f'line-height:1.05;color:{L.INK};{L.SER}')
             + L.T(90, 470, 450, desc, 27, f'line-height:1.45;color:{L.MUT}')
             + L.T(90, 900, 0, p['name'], 21, f'font-weight:700;letter-spacing:1px;color:{p["accent"]}')
             + f'<img src="{g[2]}" style="position:absolute;left:990px;top:190px;width:330px;transform:rotate(7deg);{sh}">'
             + f'<img src="{g[1]}" style="position:absolute;left:860px;top:140px;width:340px;transform:rotate(2deg);{sh}">'
             + f'<img src="{g[0]}" style="position:absolute;left:640px;top:110px;width:400px;transform:rotate(-5deg);{sh}">')
    return L.page(f'{pk}-10-bonus', inner, None, p['color'])


if __name__ == '__main__':
    args = sys.argv[1:]; store = 'etsy'
    if args[:1] == ['--gumroad']:
        args = args[1:]; store = 'gumroad'; L.W = 1801
    for pk in args or list(PROD):
        setup(pk)
        if store == 'gumroad':
            L.BGOUT = os.path.join(L.OUT, 'gumroad'); final = os.path.join(L.OUT, 'gumroad', pk); sub = 'etsy/gumroad'
        else:
            L.BGOUT = L.OUT; final = os.path.join(L.OUT, 'final', pk); sub = 'etsy'
        os.makedirs(os.path.join(L.BGOUT, pk), exist_ok=True); os.makedirs(final, exist_ok=True)
        _lb = SBL.__dict__['life_bg'].__wrapped__ if hasattr(SBL.life_bg, '__wrapped__') else SBL.life_bg
        def lb(scene, screen, out, side='right', dark=False, _lb=_lb, pk=pk):
            return _lb(scene, screen, os.path.join(L.BGOUT, pk, os.path.basename(out).replace('sb-', pk + '-')), side, dark)
        lb.__wrapped__ = _lb; SBL.life_bg = lb
        base = 'file://' + os.path.join(L.ROOT, 'canva', 'v3') + '/LOCALMARK/'
        built = L.build(pk, base, store)
        _, ls = SCENES[pk]
        pages = ([built[0]] + [life(pk, n, s, side, base) for n, (s, side) in enumerate(ls, 1)]
                 + [flat(pk, 5, base), flat(pk, 6, base)]
                 + [built[5].replace(f'{pk}-6-inside', f'{pk}-8-inside'), built[6].replace(f'{pk}-7-how', f'{pk}-9-how'), bonus(pk)])
        for pg in pages:
            pg2 = pg.replace('/LOCALMARK/crops/', '/crops/').replace('/LOCALMARK/', '/' + sub + '/')
            lab = re.search(r'data-label="([^"]+)"', pg2).group(1)
            L.render_png(pg2, os.path.join(final, lab + '.png')); print('ok', store, lab)
