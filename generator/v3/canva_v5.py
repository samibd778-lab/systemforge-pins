"""Canva-importable v5 pins (page-first style from the PinClicks top pins): one HTML page per pin,
real Notion page crops as images, all text editable in Canva.
Step 1: python3 generator/v3/canva_v5.py crops        -> canva/v5/img/*.jpg   (commit + push, note the SHA)
Step 2: python3 generator/v3/canva_v5.py html <sha>   -> canva/v5/pins-<set>.html (commit + push, import in Canva)"""
import json, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import mini_listing as M  # noqa: E402
HD = os.path.join(ROOT, 'shots', 'hd3'); IMG = os.path.join(ROOT, 'canva', 'v5', 'img'); os.makedirs(IMG, exist_ok=True)
INK, MUT, BG = '#2B2723', '#6A625A', '#FBF8F3'
RAW = 'https://raw.githubusercontent.com/samibd778-lab/systemforge-pins/{sha}/canva/v5/img/{f}'

SETS = {'mjl': {
 'meal-a1': dict(p='meal', style='a', kicker='WEEKLY MEAL PLANNER', title='Meal Planner',
                 sub='Plan the week, cook what you love, shop with one list.',
                 crops=[('meal-next7', (0, 0, 1160, 1208))]),
 'meal-b1': dict(p='meal', style='b', title='WEEKLY MEAL PLANNER', kicker='for Notion',
                 sub='Every meal linked to a recipe. A grocery list sorted by aisle.', badge='Bonus PDF:\nEat Well,\nStress Less',
                 crops=[('meal-recipes', (0, 0, 1345, 1228))]),
 'journal-a1': dict(p='journal', style='a', kicker='DAILY JOURNAL', title='Daily Journal',
                    sub='Your mood, one win and one thank you. A few minutes a day.',
                    crops=[('journal-entries', (0, 0, 1345, 1198))]),
 'journal-b1': dict(p='journal', style='b', title='MOOD TRACKER', kicker='for Notion',
                    sub='See how your month felt: average mood, great days and low days.', badge='Bonus PDF:\nJournaling\nguide',
                    crops=[('journal-monthly', (0, 0, 1345, 983))]),
 'life-a1': dict(p='life', style='a', kicker='DIGITAL VISION BOARD', title='Vision Board',
                 sub='Every dream with a photo, and the date you want it by.',
                 crops=[('life-vision', (0, 0, 1345, 1198))]),
 'life-b1': dict(p='life', style='b', title='LIFE PLANNER', kicker='for Notion',
                 sub='Goals that fill up as you go. Tick a milestone and the bar moves.', badge='Bonus PDF:\n90-Day Goal\nWorkbook',
                 crops=[('life-goals', (0, 0, 1536, 973))]),
},
'vb': {
 'vb-a1': dict(p='life', style='a', kicker='NOTION TEMPLATE', title='2027&nbsp; Vision Board', tsize=118,
               sub='Every dream with a photo, and the date you want it by.',
               crops=[('life-vision', (0, 0, 1345, 1198))]),
 'vb-c1': dict(p='life', style='c', kicker='VISION BOARD IDEAS', title='Vision board ideas<br>for your 2027',
               foot='All in one Notion vision board, with a date for every dream.',
               tiles=[('life-vision', (16, 302, 658, 596), 'Slow mornings, every day'),
                      ('life-vision', (686, 302, 1328, 596), 'Watch a sunrise from a mountain top'),
                      ('life-vision', (16, 772, 658, 1064), 'Hike in the Alps'),
                      ('life-vision', (686, 772, 1328, 1064), 'Road trip with old friends')]),
 'vb-b1': dict(p='life', style='b', title='DIGITAL VISION BOARD', kicker='for Notion',
               sub='Your dreams, your goals and the next small step, on one page.', badge='Bonus PDF:\n90-Day Goal\nWorkbook',
               crops=[('life-vision', (0, 0, 1345, 600)), ('life-goals', (0, 0, 1536, 973))]),
},
'more': {
 'meal-c1': dict(p='meal', style='c', kicker='EASY MEAL IDEAS', title='Easy weekly meals<br>to plan this week',
                 foot='Every recipe with its time and your rating, in one Notion meal planner.',
                 tiles=[('meal-recipes', (16, 273, 432, 503), 'Overnight oats with berries ·&nbsp;5&nbsp;min'),
                        ('meal-recipes', (464, 273, 880, 503), 'Sheet-pan chicken and veggies ·&nbsp;40&nbsp;min'),
                        ('meal-recipes', (912, 273, 1328, 503), 'Salmon rice bowl ·&nbsp;25&nbsp;min'),
                        ('meal-recipes', (16, 783, 432, 1013), 'Chickpea veggie bowl ·&nbsp;15&nbsp;min')]),
 'meal-a2': dict(p='meal', style='a', kicker='RECIPE ORGANIZER', title='My Recipes',
                 sub='Time, rating and tags on every card. Favorites first.',
                 crops=[('meal-recipes', (0, 0, 1345, 1228))]),
 'meal-b2': dict(p='meal', style='b', title='MEAL PREP PLANNER', kicker='for Notion',
                 sub='The next 7 days, planned. Tick Cooked when it is done.', badge='Bonus PDF:\nEat Well,\nStress Less',
                 crops=[('meal-next7', (0, 0, 1160, 1208))]),
 'journal-c1': dict(p='journal', style='c', kicker='JOURNAL IDEAS', title='What to write<br>in a daily journal',
                    foot='Four small lines a day. Your Notion journal keeps them all.',
                    tiles=[('journal-entries', (16, 302, 432, 506), 'How you feel today'),
                           ('journal-entries', (464, 302, 880, 506), 'Your energy level'),
                           ('journal-entries', (912, 302, 1328, 506), 'One win, even a small one'),
                           ('journal-entries', (16, 910, 432, 1112), 'One thing you are thankful for')]),
 'journal-a2': dict(p='journal', style='a', kicker='MOOD TRACKER', title='Monthly Mood',
                    sub='Your average mood, great days and low days. It fills in by itself.',
                    crops=[('journal-monthly', (0, 0, 1345, 983))]),
 'journal-b2': dict(p='journal', style='b', title='DAILY JOURNAL', kicker='for Notion',
                    sub='Mood, energy, one win and one thank you for every day.', badge='Bonus PDF:\nJournaling\nguide',
                    crops=[('journal-entries', (0, 0, 1345, 1198))]),
 'life-c1': dict(p='life', style='c', kicker='2027 GOAL IDEAS', title='Goals to set<br>for 2027',
                 foot='Each goal with its progress bar and a date, in one Notion life planner.',
                 tiles=[('life-goals', (32, 373, 552, 638), 'Learn to play guitar'),
                        ('life-goals', (608, 373, 1128, 638), 'Get promoted at work'),
                        ('life-goals', (1184, 373, 1536, 638), 'A weekly date night')]),
 'life-a2': dict(p='life', style='a', kicker='GOAL SETTING', title='My Goals',
                 sub='Every goal with its own progress bar. Tick a step and it fills up.',
                 crops=[('life-goals', (0, 0, 1536, 973))]),
 'life-b2': dict(p='life', style='b', title='GOAL TRACKER', kicker='for Notion',
                 sub='Not started, in progress, done. See every goal at a glance.', badge='Bonus PDF:\n90-Day Goal\nWorkbook',
                 crops=[('life-goals', (0, 0, 1536, 973))]),
},
'b2': {
 'habit-a1': dict(p='habit', style='a', kicker='NOTION TEMPLATE', title='Habit Tracker',
                  sub='A bar for every habit, your best habit and your perfect days.',
                  crops=[('habit-monthly', (0, 0, 1000, 935))]),
 'habit-b1': dict(p='habit', style='b', title='MONTHLY HABIT TRACKER', kicker='for Notion',
                  sub='Every habit gets a bar for the month. Your score fills in by itself.', badge='Bonus PDF:\n30-Day\nHabit Reset',
                  crops=[('habit-monthly', (0, 0, 1000, 935))]),
 'budget-a1': dict(p='budget', style='a', kicker='NOTION BUDGET TEMPLATE', title='Monthly Budget',
                   sub='Your budget per category, what you spent and what is left.',
                   crops=[('budget-cats', (0, 0, 1150, 865))]),
 'budget-b1': dict(p='budget', style='b', title='MONTHLY BUDGET PLANNER', kicker='for Notion',
                   sub='Every bill with its due day: paid, due soon or late.', badge='Bonus PDF:\nMoney Reset\nin 7 Days',
                   crops=[('budget-bills', (0, 0, 1150, 635)), ('budget-cats', (0, 0, 1150, 865))]),
 'budget-a2': dict(p='budget', style='a', kicker='SAVINGS TRACKER', title='Savings Goals',
                   sub='How much to save each month to hit every goal on time.',
                   crops=[('budget-savings', (0, 0, 1000, 730))]),
 'budget-a3': dict(p='budget', style='a', kicker='BILL TRACKER', title='Bill Tracker',
                   sub='Every bill and subscription with its due day. Tick Paid when it is done.',
                   crops=[('budget-bills', (0, 0, 1150, 635))]),
 'budget-b2': dict(p='budget', style='b', title='BUDGET PLANNER TEMPLATE', kicker='for Notion',
                   sub='Categories, bills, savings goals and a debt payoff plan on one page.', badge='Bonus PDF:\nMoney Reset\nin 7 Days',
                   crops=[('budget-savings', (0, 0, 1000, 730))]),
 'travel-a1': dict(p='travel', style='a', kicker='NOTION TEMPLATE', title='Travel Planner',
                   sub='Countdown, budget left and packing progress for every trip.',
                   crops=[('travel-trips', (0, 0, 1000, 730))]),
 'travel-b1': dict(p='travel', style='b', title='TRAVEL ITINERARY PLANNER', kicker='for Notion',
                   sub='Plans not booked yet, with the date. Tick Booked and they leave the list.',
                   crops=[('travel-book', (0, 0, 1150, 635))]),
 'travel-b2': dict(p='travel', style='b', title='VACATION PLANNER', kicker='for Notion',
                   sub='Every trip with its countdown, budget left and packing bar.',
                   crops=[('travel-trips', (0, 0, 1000, 730))]),
 'job-a1': dict(p='job', style='a', kicker='JOB APPLICATION TRACKER', title='Job Tracker',
                sub='Every job from Wishlist to Offer, with the next step on each card.',
                crops=[('job-pipeline', (0, 0, 920, 815))]),
 'job-b1': dict(p='job', style='b', title='JOB SEARCH TRACKER', kicker='for Notion',
                sub='Drag a card when a company answers. The next step shows on every job.',
                crops=[('job-pipeline', (0, 0, 920, 815))]),
 'sb-a1': dict(p='sb', style='a', kicker='NOTION TEMPLATE', title='Second Brain',
               sub='Goals, projects, tasks and notes in one Notion workspace.',
               crops=[('sb-projects', (0, 0, 920, 635)), ('sb-goals', (0, 0, 1150, 685))]),
 'sb-a2': dict(p='sb', style='a', kicker='PROJECT TRACKER', title='My Projects',
               sub='Drag a card when a project moves. The bar fills up as you tick its tasks.',
               crops=[('sb-projects', (0, 0, 920, 635))]),
 'sb-b1': dict(p='sb', style='b', title='ALL-IN-ONE DASHBOARD', kicker='for Notion',
               sub='Goals with progress bars, projects and tasks, linked together.',
               crops=[('sb-goals', (0, 0, 1150, 685))]),
 'life-a3': dict(p='life', style='a', kicker='NOTION TEMPLATE', title='Life Planner',
                 sub='Goals with progress bars and a vision board on one page.',
                 crops=[('life-goals', (0, 0, 1536, 973)), ('life-vision', (0, 0, 1345, 600))]),
 'meal-a3': dict(p='meal', style='a', kicker='MEAL PLAN IDEAS', title='Weekly Meal Plan', tsize=112,
                 sub='Breakfast, lunch and dinner for the next 7 days. Tick Cooked when it is done.',
                 crops=[('meal-next7', (0, 0, 1160, 1208))]),
 'shop-c1': dict(p='shop', style='c', kicker='NOTION TEMPLATE IDEAS', title='Notion template ideas<br>for 2027',
                 foot='Simple Notion templates for every part of your life.',
                 tiles=[('habit-monthly', (12, 238, 490, 472), 'Habit Tracker'),
                        ('budget-savings', (12, 240, 490, 472), 'Budget Planner'),
                        ('meal-recipes', (16, 273, 432, 503), 'Meal Planner'),
                        ('travel-trips', (12, 238, 490, 472), 'Travel Planner'),
                        ('job-pipeline', (25, 295, 441, 532), 'Job Tracker')]),
 'shop-c2': dict(p='shop', style='c', kicker='AESTHETIC NOTION TEMPLATES', title='Aesthetic Notion<br>templates to try',
                 foot='Real pages, real photos. Duplicate and start in minutes.',
                 tiles=[('life-vision', (16, 302, 658, 596), 'Vision board'),
                        ('journal-entries', (16, 302, 432, 506), 'Daily journal'),
                        ('travel-trips', (515, 238, 993, 472), 'Trip countdown'),
                        ('sb-projects', (25, 295, 441, 532), 'Project board'),
                        ('habit-monthly', (515, 238, 993, 472), 'Monthly habits')]),
}}


def cname(n, b): return f'{n}-{b[0]}-{b[1]}-{b[2]}-{b[3]}.jpg'


def fit(n, b, w, maxh):
    """crop box trimmed so the image is at most maxh tall at width w; returns (box, h)"""
    x0, y0, x1, y1 = b
    y1 = min(y1, y0 + int(maxh * (x1 - x0) / w))
    return (x0, y0, x1, y1), round((y1 - y0) * w / (x1 - x0))


def layout(s):
    """list of (box, x, y, w, h) per image"""
    out = []
    if s['style'] == 'c':
        for i, (n, b, _) in enumerate(s['tiles']):
            k = len(s['tiles']); step = 950 // k; ratio = (b[2] - b[0]) / (b[3] - b[1])
            w = min(460, round((step - 26) * ratio)); h = round(w / ratio)
            out.append((n, b, 60 + (460 - w) // 2, 380 + i * step + (step - 26 - h) // 2, w, h))
        return out
    if s['style'] == 'a':
        y, room, w, x = 400, 1500 - 400 - 100, 900, 50
        if len(s['crops']) == 1: w, x = 1000, 0
    else:
        y, room, w, x = 660, 1500 - 660 - 100, 1000, 0
    for n, b in s['crops']:
        box, h = fit(n, b, w, room)
        if out and h < 230: break  # a thin strip looks cut off
        out.append((n, box, x, y, w, h)); y += h + 22; room -= h + 22
        if room < 120: break
    return out


def p(x, y, w, size, text, color, extra=''):
    return (f'<p style="position:absolute;left:{x}px;top:{y}px;width:{w}px;margin:0;font-size:{size}px;'
            f'text-align:center;color:{color};{extra}">{text}</p>')


def page(pid, s, sha):
    pr = M.PROD.get(s['p'], {'sb': {'color': '#EDE7DD', 'accent': '#6B5B4B'}, 'shop': {'color': '#F1E9DE', 'accent': '#A0643C'}}.get(s['p'])); c, acc = pr['color'], pr['accent']
    imgs = ''.join(f'<img src="{RAW.format(sha=sha, f=cname(n, box))}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
                   for n, box, x, y, w, h in layout(s))
    foot = p(0, 1440, 1000, 22, 'SYSTEMFORGE · INSTANT DOWNLOAD', MUT, 'font-weight:700;letter-spacing:3px')
    if s['style'] == 'a':
        head = (f'<div style="position:absolute;left:0;top:0;width:1000px;height:430px;background:{c}"></div>'
                + p(0, 58, 1000, 24, s['kicker'], acc, 'font-weight:700;letter-spacing:5px')
                + p(0, 92 + (140 - s.get('tsize', 140)) // 2, 1000, s.get('tsize', 140), s['title'], INK, "font-family:'Great Vibes',cursive;line-height:1.1")
                + p(90, 268, 820, 31, s['sub'], MUT, 'line-height:1.35'))
    elif s['style'] == 'c':
        L = layout(s)
        head = (f'<div style="position:absolute;left:0;top:0;width:1000px;height:350px;background:{c}"></div>'
                + p(0, 56, 1000, 24, s['kicker'], acc, 'font-weight:700;letter-spacing:5px')
                + p(60, 100, 880, 76, s['title'], INK, "font-family:'Playfair Display',serif;font-weight:700;line-height:1.1"))
        imgs += ''.join(p(555, y + h // 2 - 46, 390, 34, f'{i + 1}. {lab}', INK, "text-align:left;font-family:'Playfair Display',serif;font-weight:700;line-height:1.2")
                        for i, ((n, box, x, y, w, h), (_, _, lab)) in enumerate(zip(L, s['tiles'])))
        imgs += p(80, 1338, 840, 29, s['foot'], MUT, 'line-height:1.35')
    else:
        head = (f'<div style="position:absolute;left:0;top:0;width:1000px;height:520px;background:{acc}"></div>'
                + p(60, 70 if len(s['title']) <= 18 else 60, 880, 104 if len(s['title']) <= 18 else 80, s['title'], '#FFFFFF', "font-family:'Playfair Display',serif;font-weight:700;line-height:1.02")
                + p(0, 390, 1000, 84, s['kicker'], '#FFFFFF', "font-family:'Great Vibes',cursive")
                + p(60, 560, 880, 33, s['sub'], INK, 'line-height:1.3'))
        badge = '' if not s.get('badge') else (f'<div style="position:absolute;left:740px;top:1150px;width:220px;height:220px;border-radius:110px;background:{c}"></div>'
                 + p(740, 1210, 220, 25, s['badge'].replace('\n', '<br>'), INK, 'font-weight:700;line-height:1.25'))
        imgs += badge
    return (f'<div data-document-role="page" data-label="{pid}" style="position:relative;width:1000px;height:1500px;overflow:hidden;background:{BG}">'
            + head + imgs + foot + '</div>')


if __name__ == '__main__':
    mode, name = sys.argv[1], sys.argv[2]; S = SETS[name]
    if mode == 'crops':
        for pid, s in S.items():
            for n, box, *_ in layout(s):
                Image.open(os.path.join(HD, n + '.jpg')).convert('RGB').crop(box).save(os.path.join(IMG, cname(n, box)), quality=95)
        print(sorted(os.listdir(IMG)))
    else:
        sha = sys.argv[3]
        html = ('<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700'
                '&family=Great+Vibes&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">'
                '<style>body{margin:0}div,span,p{font-family:Inter,Arial,sans-serif}</style></head><body>'
                + '\n'.join(page(pid, s, sha) for pid, s in S.items()) + '</body></html>')
        out = os.path.join(ROOT, 'canva', 'v5', f'pins-{name}.html'); open(out, 'w').write(html); print(out, len(html))
