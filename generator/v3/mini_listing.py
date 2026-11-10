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

 'job': dict(name='Job Application Tracker', kicker='NOTION JOB TRACKER', color='#DFE8F0', accent='#3D6A8F',
   sub='Every job, every interview and<br>every follow-up in one place.',
   features=['Job pipeline from Wishlist to Offer', 'Follow-up reminders + email scripts', 'Interview prep + STAR stories', 'Bonus: 30-Day Job Search Playbook'],
   screens={'lap': ['job-top', 'job-pipeline'], 's1': ['job-pipeline', 'job-people'], 's2': ['job-followup', 'job-interviews', 'job-people'], 's3': ['job-prep'], 's4': ['job-emails']},
   cards=[('One board for every job', 'Every job from Wishlist to Offer, with the next step on each card.', ('job-pipeline', 0, 0, 1393, 495)),
          ('Follow up on time', 'Jobs with no answer after 7 days show up here, with what to do next.', ('job-followup', 0, 0, 1360, 240)),
          ('Walk in prepared', 'A prep checklist and the STAR method, with a real example.', ('job-prep', 0, 0, 725, 621)),
          ('Emails ready to copy', 'Change the words in [brackets], send it, done.', ('job-emails', 0, 0, 725, 560)),
          ('Your people + companies', 'Recruiters, referrals and target companies, linked to every job.', ('job-people', 0, 0, 1335, 380)),
          ('A 10-minute weekly review', 'Every Friday: a checklist and questions that show what to fix.', ('job-weekly', 0, 0, 725, 466))],
   inside=['Home page with a 10-minute daily check', 'Job pipeline: Wishlist to Offer', 'A next step for every job, by itself', 'Follow up today + interview reminders',
           'Interviews, Companies and Contacts', 'Story Bank for STAR answers', 'Follow-up email scripts', 'Interview Prep Guide + Resume Checklist',
           'Salary Negotiation Script + Weekly review', 'Bonus PDF: 30-Day Job Search Playbook'],
   bonus=('30-Day Job Search Playbook', 'A 7-page PDF: a resume that gets calls, a 30-day plan, 30 interview questions, follow-ups, the offer and a printable weekly scorecard.')),
 'meal': dict(name='Meal Planner', kicker='NOTION MEAL PLANNER', color='#E1ECDD', accent='#5E8C5A',
   sub='Plan the week, cook what you love<br>and shop with one simple list.',
   features=['Weekly meal plan calendar', 'Recipe organizer with ratings', 'Grocery list sorted by aisle', 'Bonus: Eat Well, Stress Less'],
   screens={'lap': ['meal-top', 'meal-week'], 's1': ['meal-calendar'], 's2': ['meal-recipes'], 's3': ['meal-buy'], 's4': ['meal-week']},
   cards=[('Plan the week', 'Breakfast, lunch, dinner and snacks for every day, each linked to a recipe.', ('meal-calendar', 0, 0, 1330, 487)),
          ('All your recipes', 'Time, rating and tags on every card. Favorites first.', ('meal-recipes', 0, 0, 1330, 604)),
          ('Shop by aisle', 'Quantity, price and the recipe that needs each item.', ('meal-buy', 0, 0, 1335, 624)),
          ('The next 7 days', 'Tick Cooked when it is done. Plan leftovers too.', ('meal-week', 0, 0, 1155, 569)),
          ('Tick the ingredients', 'Every recipe keeps its ingredients as a checklist.', ('meal-recipe', 0, 0, 615, 447)),
          ('Sunday in 15 minutes', 'A simple weekly checklist right on the home page.', ('meal-top', 455, 300, 1335, 615))],
   inside=['Home page with a 15-minute Sunday checklist', 'Meal Plan calendar for the week', 'Next 7 days board', 'Recipes with time, rating and tags',
           'Ingredient checklist in every recipe', 'Grocery List sorted by aisle', 'Price + recipe for every item', 'Staples you buy every week',
           'Meal Prep Guide + Save Money on Groceries', 'Bonus PDF: Eat Well, Stress Less'],
   bonus=('Eat Well, Stress Less', 'A 7-page PDF: plan a week in 15 minutes, a 4-week plan, batch cooking basics, meal ideas, saving at the store and a printable week + grocery list.')),
 'travel': dict(name='Travel Planner', kicker='NOTION TRAVEL PLANNER', color='#DCEBF1', accent='#2F7E9A',
   sub='Dates, plans, bookings, budget<br>and packing on one page.',
   features=['Trip countdown + budget left', 'Itinerary + still to book', 'Packing list with progress', 'Bonus: Plan Trips Like a Pro'],
   screens={'lap': ['travel-top', 'travel-trips'], 's1': ['travel-trips', 'travel-book'], 's2': ['travel-book', 'travel-trips'], 's3': ['travel-trip', 'travel-book'], 's4': ['travel-pack']},
   cards=[('A countdown per trip', 'Days to go, budget left and how much is packed, on every card.', ('travel-trips', 0, 0, 1330, 449)),
          ('Still to book', 'Upcoming plans that are not booked yet, with the date and the cost.', ('travel-book', 0, 0, 1355, 420)),
          ('One page per trip', 'Dates, budget left, packing bar and the itinerary with confirmation numbers.', ('travel-trip', 0, 0, 1395, 352)),
          ('Pack smarter', 'A packing list grouped by type. Tick Packed as you go.', ('travel-pack', 0, 0, 805, 545)),
          ('Track spending', 'Every expense linked to its trip, so the budget updates.', ('travel-expenses', 0, 0, 485, 530)),
          ('Plan before you go', 'A simple before-every-trip checklist on the home page.', ('travel-top', 455, 300, 1335, 615))],
   inside=['Home page with a before-every-trip checklist', 'Trips with countdown + status', 'Budget left on every trip', 'Itinerary with confirmation numbers',
           'Still to book list', 'Expenses linked to each trip', 'Packing list with a progress bar', 'Before You Go + Packing Checklist',
           'Travel Budget Guide', 'Bonus PDF: Plan Trips Like a Pro'],
   bonus=('Plan Trips Like a Pro', 'A 7-page PDF: a planning timeline, a realistic budget, planning the days, packing light, travel day tips and a printable trip sheet.')),
 'life': dict(name='Life Planner', kicker='NOTION LIFE PLANNER', color='#E8E2F2', accent='#7A63A8',
   sub='Big dreams, clear goals and<br>small steps you can finish.',
   features=['Goals with progress bars', 'Milestones + next steps', 'Vision board + Life Wheel', 'Bonus: 90-Day Goal Workbook'],
   screens={'lap': ['life-top', 'life-vision'], 's1': ['life-goals', 'life-steps'], 's2': ['life-vision'], 's3': ['life-steps', 'life-vision'], 's4': ['life-wheel']},
   cards=[('Goals with progress', 'Tick a milestone and the bar fills by itself.', ('life-goals', 0, 0, 905, 409)),
          ('Your vision board', 'Every dream with a photo and when you want it.', ('life-vision', 0, 0, 1330, 595)),
          ('Never miss a step', 'Steps due this month, with Late and This week flags.', ('life-steps', 0, 0, 1335, 309)),
          ('Check in with life', 'Score 8 areas of your life and see where to grow.', ('life-wheel', 0, 0, 725, 500)),
          ('Sunday in 10 minutes', 'A simple weekly checklist right on the home page.', ('life-top', 455, 300, 1335, 615)),
          ('Pick what matters', 'Simple questions help you choose the right goal.', ('life-wheel', 0, 480, 725, 781))],
   inside=['Home page with a 10-minute Sunday checklist', 'Goals board with progress bars', 'Milestones with due dates', 'Next steps: late + this week',
           'Vision board with photos', 'Life Wheel: score 8 areas', 'Weekly Check-in', 'Quarterly Review',
           'Why it matters + a reward for each goal', 'Bonus PDF: The 90-Day Goal Workbook'],
   bonus=('The 90-Day Goal Workbook', 'A 7-page PDF: check in with your life, pick the right goals, break them into steps, a weekly rhythm and a printable 90-day plan.')),
}
SCENES = {  # main scene (laptop right), then 4 lifestyle scenes (scene, text side)
 'habit': ('n-habit-a.png', [('n-habit-b.png', 'right'), ('n-habit-b-m.png', 'left'), ('n-habit-a-m.png', 'right'), ('n-habit-a.png', 'left')]),
 'journal': ('n-journal-a.png', [('n-journal-b.png', 'right'), ('n-journal-b-m.png', 'left'), ('n-journal-a-m.png', 'right'), ('n-journal-a.png', 'left')]),
 'budget': ('n-budget-a.png', [('n-budget-b.png', 'right'), ('n-budget-b-m.png', 'left'), ('n-budget-a-m.png', 'right'), ('n-budget-a.png', 'left')]),
 'job': ('n-job-a.png', [('n-job-b.png', 'right'), ('n-job-b-m.png', 'left'), ('n-job-a-m.png', 'right'), ('n-job-a.png', 'left')]),
 'meal': ('n-meal-a.png', [('n-meal-b.png', 'right'), ('n-meal-b-m.png', 'left'), ('n-meal-a-m.png', 'right'), ('n-meal-a.png', 'left')]),
 'travel': ('n-travel-a.png', [('n-travel-b.png', 'right'), ('n-travel-b-m.png', 'left'), ('n-travel-a-m.png', 'right'), ('n-travel-a.png', 'left')]),
 'life': ('n-life-a.png', [('n-life-a-m.png', 'right'), ('n-life-a.png', 'left'), ('n-life-a-m.png', 'right'), ('n-life-a.png', 'left')]),
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
