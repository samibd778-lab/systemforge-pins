"""Free printables (Gumroad $0 lead magnets). Clean, ink-light US Letter pages + a last page about the matching
Notion template (Gumroad link). Research: research/pinclicks-top-pins-2026-11-12.md ("free printable" wins).
Run: python3 generator/printables.py [set ...]  -> dl/free/<file>.pdf, dl/free/<file>-p-<N>.png, pins/v5/free-<set>-a1.png"""
import base64, os, subprocess, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, 'generator', 'remotion', 'public')
OUT = os.path.join(ROOT, 'dl', 'free'); os.makedirs(OUT, exist_ok=True)
FONTS = (f"@font-face{{font-family:GV;src:url(file://{F}/greatvibes400.woff2)}}"
         f"@font-face{{font-family:PF;font-weight:700;src:url(file://{F}/playfair700.woff2)}}"
         f"@font-face{{font-family:IN;font-weight:500;src:url(file://{F}/inter500.woff2)}}"
         f"@font-face{{font-family:IN;font-weight:700;src:url(file://{F}/inter700.woff2)}}")
CSS = FONTS + """
@page{size:8.5in 11in;margin:0}*{box-sizing:border-box;margin:0;padding:0}
body{font-family:IN;color:#2E2A25;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:8.5in;height:11in;padding:.55in .6in .45in;position:relative;page-break-after:always;background:#fff;overflow:hidden}
.kick{font:700 10px IN;letter-spacing:.32em;color:var(--acc);text-align:center}
h1{font:400 64px/1 GV;text-align:center;margin:6px 0 2px;color:#2E2A25}
.meta{display:flex;justify-content:center;gap:28px;font:500 11px IN;color:#6F665B;margin:6px 0 18px}
.meta span b{display:inline-block;width:1.3in;border-bottom:1px solid #CFC6BA;margin-left:6px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px 18px}
.box{border:1.2px solid var(--line);border-radius:14px;padding:10px 14px 8px}
.box h3{font:700 12px IN;letter-spacing:.14em;text-transform:uppercase;color:var(--acc);margin-bottom:4px;display:flex;gap:8px;align-items:center}
.row{display:flex;align-items:flex-end;gap:9px;height:24px;border-bottom:1px solid #EDE6DC}
.cb{width:12px;height:12px;border:1.3px solid #B9AFA2;border-radius:3px;margin-bottom:5px;flex:none}
.foot{position:absolute;left:.6in;right:.6in;bottom:.32in;display:flex;justify-content:space-between;font:700 8.5px IN;letter-spacing:.2em;color:#A79C8E}
table.wk{width:100%;border-collapse:separate;border-spacing:0;border:1.2px solid var(--line);border-radius:14px;overflow:hidden}
.wk th{font:700 10px IN;letter-spacing:.16em;text-transform:uppercase;color:var(--acc);background:var(--tint);padding:9px 10px;text-align:left}
.wk td{border-top:1px solid #EDE6DC;height:1.12in;padding:7px 10px;vertical-align:top;font:700 11px IN}
.wk td+td{border-left:1px solid #EDE6DC}
.up h2{font:700 30px/1.15 PF;text-align:center;margin:4px 0 10px}
.up p{font:500 13px/1.5 IN;color:#6F665B;text-align:center;margin:0 auto 16px;width:5.6in}
.up img{width:100%;border:1px solid var(--line);border-radius:12px}
.feat{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:16px 0}
.feat div{background:var(--tint);border-radius:12px;padding:12px 14px;font:500 12.5px/1.45 IN}
.feat b{display:block;font:700 12.5px IN;margin-bottom:2px}
.cta{display:block;text-align:center;background:var(--acc);color:#fff;text-decoration:none;font:700 15px IN;padding:14px;border-radius:12px;margin-top:6px}
.how{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:18px}
.how div{border:1.2px solid var(--line);border-radius:12px;padding:10px 12px;font:500 11.5px/1.45 IN;color:#6F665B}
.how b{display:block;font:700 22px PF;color:var(--acc)}
.tb{width:100%;border-collapse:separate;border-spacing:0;border:1.2px solid var(--line);border-radius:12px;overflow:hidden}
.tb th{font:700 9.5px IN;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);background:var(--tint);padding:8px 8px;text-align:left}
.tb td{border-top:1px solid #EDE6DC;padding:0 8px;font:700 11px IN}
.tb td+td,.tb th+th{border-left:1px solid #EDE6DC}
.hg td{padding:0;text-align:center}.hg th{padding:6px 2px;text-align:center;font-size:8px;letter-spacing:0}
.lab{font:700 11px IN;color:#6F665B;margin:2px 0 4px}
.wl{height:22px;border-bottom:1px solid #E3DBD0}
.dots{display:grid;gap:6px}.dots span{aspect-ratio:1;border:1.3px solid #C9BFB2;border-radius:50%;display:flex;align-items:center;justify-content:center;font:700 8px IN;color:#B3A898}
.ideas li{list-style:none;font:500 12px/1.5 IN;padding:5px 0 5px 18px;position:relative;border-bottom:1px dashed #E8E0D5}
.ideas li:before{content:'✦';position:absolute;left:0;color:var(--acc);font-size:10px;top:6px}
.photo{border:1.5px dashed var(--line);border-radius:12px;display:flex;align-items:flex-end;justify-content:center;padding:8px;font:700 10px IN;letter-spacing:.14em;color:var(--acc);background:var(--tint)}
"""


def b64(p): return 'data:image/jpeg;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
def lines(n): return ''.join('<div class="row"><span class="cb"></span></div>' for _ in range(n))
def wl(n): return ''.join('<div class="wl"></div>' for _ in range(n))
def foot(left): return f'<div class="foot"><span>{left}</span><span>SYSTEMFORGE · FREE PRINTABLE</span></div>'
def page(title, meta, inner, left, kick='FREE PRINTABLE', size=64):
    m = ''.join(f'<span>{x}<b{" style=" + chr(34) + "width:.8in" + chr(34) if x.endswith("$") else ""}></b></span>' for x in meta)
    return (f'<section class="pg"><div class="kick">{kick}</div><h1 style="font-size:{size}px">{title}</h1>'
            + (f'<div class="meta">{m}</div>' if meta else '<div style="height:14px"></div>') + inner + foot(left) + '</section>')
def box(t, inner, extra=''): return f'<div class="box" style="{extra}"><h3>{t}</h3>{inner}</div>'
def table(heads, widths, n, h=26, first=None):
    th = ''.join(f'<th style="width:{w}">{x}</th>' for x, w in zip(heads, widths))
    rows = ''.join('<tr>' + ''.join(f'<td style="height:{h}px">{(first[i] if first and j == 0 and i < len(first) else "")}</td>' for j in range(len(heads))) + '</tr>' for i in range(n))
    return f'<table class="tb"><tr>{th}</tr>{rows}</table>'
def col(*items): return '<div style="display:grid;gap:14px;align-content:start">' + ''.join(items) + '</div>'
def grid(*cols, tmpl='1fr 1fr'): return f'<div style="display:grid;grid-template-columns:{tmpl};gap:14px 18px">' + ''.join(cols) + '</div>'
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# ---------- page sets (printable pages only; the upsell page is added by build) ----------
def p_grocery():
    a = [('🥦', 'Produce', 9), ('🥛', 'Dairy & eggs', 7), ('🍗', 'Meat & fish', 6), ('🥖', 'Bakery', 4),
         ('🥫', 'Pantry', 9), ('🧊', 'Frozen', 7), ('🧃', 'Drinks', 6), ('🧻', 'Household', 4)]
    c = lambda it: col(*[box(f'<span>{e}</span>{t}', lines(n)) for e, t, n in it])
    p1 = page('Grocery List', ['Week of', 'Store', 'Budget $'], grid(c(a[:4]), c(a[4:])), 'SORTED BY AISLE')
    p2 = page('Weekly Meal Plan', ['Week of'],
              '<div style="display:grid;grid-template-columns:1fr 2.1in;gap:16px"><table class="wk"><tr><th style="width:.75in"></th><th>Breakfast</th><th>Lunch</th><th>Dinner</th></tr>'
              + ''.join(f'<tr><td style="color:var(--acc)">{d}</td><td></td><td></td><td></td></tr>' for d in DAYS) + '</table>'
              + col(box('To buy', lines(20)), box('Prep ahead', lines(7))) + '</div>', 'PLAN, THEN SHOP')
    return [p1, p2]

def p_habit():
    n = 31
    th = '<th style="width:1.45in;text-align:left;padding-left:8px">Habit</th>' + ''.join(f'<th>{d}</th>' for d in range(1, n + 1))
    tr = ''.join('<tr><td style="height:38px"></td>' + '<td></td>' * n + '</tr>' for _ in range(14))
    p1 = page('Habit Tracker', ['Month', 'My focus habit'],
              f'<table class="tb hg">{th}{tr}</table>'
              + grid(box('How it went', wl(5)), box('Next month I will', wl(5))).replace('display:grid', 'display:grid;margin-top:16px'),
              'COLOUR A BOX EACH DAY')
    ideas = {'Health': ['Drink a glass of water first thing', 'Walk 10 minutes after lunch', 'Stretch for 5 minutes', 'Eat one fruit a day', 'In bed by 11'],
             'Mind': ['Read 10 pages', 'Write one line in a journal', 'Meditate for 3 minutes', 'No phone for the first hour', 'Learn one new word'],
             'Home': ['Make your bed', 'Clear the sink before bed', 'Put 10 things away', 'Open the windows in the morning', 'Prep clothes the night before'],
             'Money': ['Write down what you spend', 'No-spend day once a week', 'Move $5 to savings', 'Check your bank app', 'Cook dinner at home']}
    lst = grid(*[box(k, '<ul class="ideas">' + ''.join(f'<li>{x}</li>' for x in v) + '</ul>') for k, v in ideas.items()])
    plan = table(['Habit', 'Cue: after I...', 'Tiny version', 'Reward'], ['1.6in', '2in', '1.6in', '1.5in'], 7, 40)
    p2 = page('Habit Ideas', [], lst + '<div style="height:16px"></div><div class="kick" style="text-align:left;margin-bottom:8px">MY HABIT PLAN</div>' + plan, '20 SMALL HABITS')
    return [p1, p2]

def p_budget():
    cats = ['Rent / mortgage', 'Bills & utilities', 'Groceries', 'Transport', 'Eating out', 'Subscriptions', 'Shopping', 'Health', 'Fun', 'Savings', 'Debt payments', 'Other']
    p1 = page('Monthly Budget', ['Month', 'Income $'],
              table(['Category', 'Budget', 'Spent', 'Left'], ['2.4in', '1.5in', '1.5in', '1.5in'], 12, 40, cats)
              + '<div style="height:14px"></div>' + grid(box('Income', table(['Source', 'Amount'], ['60%', '40%'], 3, 32)), box('Totals', table(['', 'Amount'], ['60%', '40%'], 3, 32, ['Budget', 'Spent', 'Left']))),
              'GIVE EVERY DOLLAR A JOB')
    months = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
    p2 = page('Bill Tracker', ['Year'],
              '<table class="tb hg"><tr><th style="width:1.9in;text-align:left;padding-left:8px">Bill</th><th style="width:.55in">Due</th><th style="width:.8in">Amount</th>'
              + ''.join(f'<th>{m}</th>' for m in months) + '</tr>' + ''.join('<tr>' + '<td style="height:31px"></td>' * 15 + '</tr>' for _ in range(16)) + '</table>'
              + '<p style="font:500 11px IN;color:#6F665B;margin-top:10px">Tick the month when the bill is paid.</p>', 'NEVER MISS A DUE DATE')
    goal = lambda: box('Goal: ____________________', '<div class="lab">Target $ ________ · By ________</div><div class="dots" style="grid-template-columns:repeat(10,1fr)">'
                       + ''.join(f'<span>{i * 5}%</span>' for i in range(1, 21)) + '</div>')
    p3 = page('Savings Tracker', ['Year'], col(goal(), goal(), goal(), goal()) + '<p style="font:500 11px IN;color:#6F665B;margin-top:10px">Colour a circle each time you reach the next 5%.</p>', 'SMALL STEPS ADD UP')
    p4 = page('Debt Payoff', ['Start date'],
              table(['Debt', 'Balance', 'Interest %', 'Minimum', 'Extra', 'Paid off by'], ['1.7in', '1.05in', '.9in', '.95in', '.85in', '1.05in'], 7, 38)
              + '<div style="height:14px"></div>' + box('Debt I pay first (highest interest)', '<div class="lab">Balance $ ________</div><div class="dots" style="grid-template-columns:repeat(10,1fr)">'
              + ''.join(f'<span>{i}</span>' for i in range(1, 51)) + '</div><p style="font:500 11px IN;color:#6F665B;margin-top:8px">Each circle = 2% of the balance. Colour one every time you pay it down.</p>'),
              'HIGHEST INTEREST FIRST')
    return [p1, p2, p3, p4]

def p_weekly():
    day = lambda d: box(d, lines(6))
    p1 = page('Weekly Planner', ['Week of'], grid(col(*[day(d) for d in DAYS[:4]]), col(*[day(d) for d in DAYS[4:]], box('Top 3 this week', lines(3)))), 'ONE WEEK, ONE PAGE')
    hours = [f'{h if h <= 12 else h - 12} {"am" if h < 12 else "pm"}' for h in range(6, 22)]
    sched = '<table class="tb">' + ''.join(f'<tr><td style="height:31px;width:.7in;color:var(--acc)">{h}</td><td></td></tr>' for h in hours) + '</table>'
    p2 = page('Daily Planner', ['Date'], grid(col(box('Schedule', sched)), col(box('Top 3 priorities', lines(3)), box('To do', lines(10)), box('Notes', wl(5)), box('Water', '<div class="dots" style="grid-template-columns:repeat(8,1fr);margin-top:6px">' + '<span></span>' * 8 + '</div>'))), 'PLAN YOUR DAY')
    return [p1, p2]

def p_travel():
    a = [('📄', 'Documents', 6), ('👕', 'Clothes', 12), ('🧴', 'Toiletries', 10),
         ('🔌', 'Tech', 6), ('🎒', 'Carry-on', 5), ('💊', 'Health', 4), ('🏖️', 'Extras', 4), ('✅', 'Before you leave', 4)]
    c = lambda it: col(*[box(f'<span>{e}</span>{t}', lines(n)) for e, t, n in it])
    p1 = page('Packing List', ['Trip', 'Dates'], grid(c(a[:3]), c(a[3:])), 'TICK AS YOU PACK')
    p2 = page('Trip Planner', ['Destination', 'Dates', 'Budget $'],
              table(['Day', 'Plan', 'Booked'], ['.9in', '5.1in', '.9in'], 7, 58, [f'Day {i}' for i in range(1, 8)]) + '<div style="height:14px"></div>'
              + grid(box('Still to book', lines(8)), box('Budget', table(['', 'Planned', 'Spent'], ['40%', '30%', '30%'], 6, 28, ['Flights', 'Stay', 'Food', 'Activities', 'Transport', 'Total']))),
              'ONE TRIP, ONE PAGE')
    return [p1, p2]

def p_journal():
    faces = ''.join(f'<span style="font-size:22px;margin-right:14px">{f}</span>' for f in ['😞', '😕', '😐', '🙂', '😄'])
    p1 = page('Gratitude Journal', ['Date'],
              box('Today I feel', f'<div style="padding:6px 0 4px">{faces}<span class="lab" style="margin-left:18px">Energy: low · ok · high</span></div>')
              + '<div style="height:14px"></div>' + col(box('3 things I am grateful for', ''.join(f'<div class="lab" style="margin-top:8px">{i}.</div>' + wl(2) for i in (1, 2, 3))),
              box('One win today, even a small one', wl(3)), box('Something kind I did or saw', wl(3)), box('Tomorrow I will', wl(3)), box('Notes', wl(3))), 'A FEW MINUTES A DAY')
    prompts = ['A person who made you smile this week', 'A small thing you love about your home', 'A skill you are glad you have', 'A meal you really enjoyed', 'A place that makes you calm',
               'Something your body did for you today', 'A friend you can always call', 'A mistake that taught you something', 'A song that lifts your mood', 'Something you have now that you once wished for',
               'A teacher who helped you', 'The best part of your morning', 'A book or show you enjoyed', 'A hard thing you got through', 'Something in nature you noticed',
               'A habit that makes your life better', 'A compliment you received', 'Something you are looking forward to', 'A tradition you love', 'A comfort you often forget',
               'A free thing that makes you happy', 'Someone who believes in you', 'A memory that still makes you laugh', 'Something you learned this month', 'A moment you felt proud',
               'A simple pleasure from today', 'Someone you can thank this week', 'A way you have grown this year', 'What made today better than yesterday', 'Why you are grateful for you']
    lst = grid(*['<ul class="ideas">' + ''.join(f'<li style="font-size:14px;padding:10px 0 10px 20px"><b style="color:var(--acc)">{i + 1 + k * 15:02d}</b> &nbsp;{x}</li>' for i, x in enumerate(prompts[k * 15:(k + 1) * 15])) + '</ul>' for k in (0, 1)])
    p2 = page('30 Gratitude Prompts', [], lst.replace('class="ideas"', 'class="ideas" style="font-size:13.5px"'), 'ONE PROMPT A DAY', size=56)
    return [p1, p2]

def p_goals():
    areas = ['💪 Health', '💼 Career', '💰 Money', '❤️ Relationships', '🏡 Home', '📚 Learning', '🎉 Fun', '🧘 Mind']
    p1 = page('My 2027 Goals', ['Word of the year'], grid(*[box(a, wl(6)) for a in areas]), 'ONE GOAL PER AREA')
    p2 = page('Goal Planner', ['Goal', 'By'],
              grid(box('Why it matters', wl(4)), box('Reward when I reach it', wl(4))) + '<div style="height:14px"></div>'
              + table(['Milestone', 'Due', 'Done'], ['4.6in', '1.4in', '.9in'], 10, 36, [f'{i}.' for i in range(1, 11)]) + '<div style="height:14px"></div>'
              + grid(box('Habits that help', lines(5)), box('What could get in the way', wl(5))), 'BIG GOAL, SMALL STEPS')
    tiles = ''.join(f'<div class="photo" style="height:{h}in">{t}</div>' for t, h in [('DREAM', 2.7), ('PLACE', 2.7), ('FEELING', 2.7), ('GOAL', 2.7), ('WORD', 2.7), ('ME IN 2027', 2.7)])
    p3 = page('Vision Board', ['Year'], f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px">{tiles}</div>'
              + '<div style="height:14px"></div>' + box('This year I want to feel', wl(4)), 'GLUE A PICTURE IN EACH BOX')
    return [p1, p2, p3]

def p_job():
    p1 = page('Job Application Tracker', ['Month'],
              table(['Company', 'Role', 'Applied', 'Status', 'Next step', 'Follow up'], ['1.5in', '1.5in', '.8in', '.9in', '1.5in', '.8in'], 20, 36)
              + '<p style="font:500 11px IN;color:#6F665B;margin-top:10px">Status: Wishlist · Applied · Interview · Offer · No</p>', 'EVERY JOB IN ONE PLACE', size=54)
    p2 = page('Interview Prep', ['Company', 'Date'],
              grid(box('About the company', wl(6)), box('Why I want this job', wl(6))) + '<div style="height:14px"></div>'
              + box('My stories (situation, task, action, result)', table(['Question', 'My story'], ['2.2in', '4.5in'], 3, 70, ['Tell me about yourself', 'A problem you solved', 'Why should we hire you'])) + '<div style="height:14px"></div>'
              + grid(box('Questions I will ask', lines(6)), box('After the interview', lines(6))), 'BE READY')
    return [p1, p2]

SETS = {
 'grocery': dict(f=p_grocery, file='Free-Printable-Grocery-List', acc='#5E7F5A', tint='#EEF3EA', line='#D9E3D3', bg='#F2F5EE', key='meal',
     title='Grocery List', sub='Sorted by aisle + a weekly meal plan', product='Meal Planner', shot='meal-grocery', box=(0, 0, 1350, 680),
     how=['Plan your week on the meal plan page.', 'Write what you need under the right aisle.', 'Tick each item in the store. Done.'],
     lead='The same idea in Notion: plan the next 7 days, and your grocery list sorts itself by aisle, with quantity and price.',
     feats=[('Grocery list by aisle', 'Tick Got it in the store and the item leaves the list.'), ('The next 7 days', 'Breakfast, lunch and dinner. Tick Cooked when it is done.'),
            ('Your recipes', 'Time, rating and tags on every card. Favorites first.'), ('On your phone', 'Open it in the Notion app at the store.')]),
 'habit': dict(f=p_habit, file='Free-Printable-Habit-Tracker', acc='#B0643C', tint='#F6EBE2', line='#EBD9CB', bg='#F7F0E9', key='habit',
     title='Habit Tracker', sub='Monthly tracker + 20 habit ideas', product='Habit Tracker', shot='habit-week', box=(0, 0, 1180, 600),
     how=['Pick up to 12 habits and write them on the left.', 'Colour a box each day you do it.', 'At the end of the month, write how it went.'],
     lead='The same idea in Notion: tick your habits each day and your score fills in by itself.',
     feats=[('Every day', 'Tick 6 habits in 10 seconds. Your score and day type fill in by themselves.'), ('Every month', 'A bar for every habit, your best habit and your perfect days.'),
            ('Every year', 'Your whole year in one line.'), ('Bonus', 'A habit plan, 50 habit ideas and the 30-Day Habit Reset guide.')]),
 'budget': dict(f=p_budget, file='Free-Printable-Budget-Planner', acc='#3F7D5C', tint='#E7F1EA', line='#D3E3D8', bg='#EFF5F0', key='budget',
     title='Budget Planner', sub='Budget, bills, savings + debt payoff', product='Budget Planner', shot='budget-tx', box=(0, 0, 1260, 608),
     how=['Write your income and a budget for each category.', 'Tick each bill when it is paid.', 'Colour your savings and debt circles as you go.'],
     lead='The same idea in Notion: add an expense and your budget, bills and savings update by themselves.',
     feats=[('Budget this month', 'Your budget per category, what you spent and what is left.'), ('Bills', 'Every bill with its due day: paid, due soon or late.'),
            ('Savings goals', 'How much to save each month to hit every goal on time.'), ('Debt payoff', 'Highest interest first. See your debt-free date move closer.')]),
 'weekly': dict(f=p_weekly, file='Free-Printable-Weekly-Planner', acc='#6B5B4B', tint='#F1ECE6', line='#E3DAD0', bg='#F4F0EA', key='sb',
     title='Weekly Planner', sub='Weekly planner + daily planner pages', product='Second Brain OS', shot='sb-projects', box=(0, 0, 920, 635),
     how=['Write your top 3 for the week first.', 'Spread the rest over the days.', 'Use the daily page on busy days.'],
     lead='The same idea in Notion: goals, projects, tasks and notes linked together in one workspace.',
     feats=[('Projects', 'Drag a card when a project moves. The bar fills up as you tick its tasks.'), ('Goals', 'Every goal with its own progress bar.'),
            ('Tasks', 'Your tasks linked to the project they belong to.'), ('Notes', 'Your notes and ideas in the same place.')]),
 'travel': dict(f=p_travel, file='Free-Printable-Packing-List', acc='#2F6E8E', tint='#E6F0F5', line='#D2E2EA', bg='#EEF4F7', key='travel',
     title='Packing List', sub='Packing list + one-page trip planner', product='Travel Planner', shot='travel-pack', box=(0, 0, 1185, 627),
     how=['Fill the trip planner one week before.', 'Write what to pack under each type.', 'Tick each item as it goes in the bag.'],
     lead='The same idea in Notion: every trip with its countdown, budget left and packing progress.',
     feats=[('Every trip', 'Countdown, budget left and packing progress.'), ('Still to book', 'Plans not booked yet, with the date. Tick Booked and they leave the list.'),
            ('Packing list', 'Sorted by type, linked to your trip. Tick Packed as you go.'), ('Expenses', 'Link each expense to its trip to update the budget.')]),
 'journal': dict(f=p_journal, file='Free-Printable-Gratitude-Journal', acc='#8A6A9C', tint='#F1EBF4', line='#E3D8E9', bg='#F4EFF6', key='journal',
     title='Gratitude Journal', sub='Daily journal page + 30 prompts', product='Daily Journal', shot='journal-entries', box=(0, 0, 1345, 700),
     how=['Print a few daily pages for the week.', 'Write for 3 minutes, morning or night.', 'Stuck? Pick a prompt from the list.'],
     lead='The same idea in Notion: your mood, your energy, one win and one thank you for every day.',
     feats=[('Every day', 'Mood, energy, one win and one thank you.'), ('Every month', 'Your average mood, great days and low days.'),
            ('Your entries', 'Open an entry to write more, with a photo on each card.'), ('Bonus', 'A short journaling guide.')]),
 'goals': dict(f=p_goals, file='Free-Printable-2027-Goal-Planner', acc='#7A5BA6', tint='#F0EBF7', line='#E2D9EE', bg='#F3EFF8', key='life',
     title='2027 Goals', sub='Goal planner + vision board pages', product='Life Planner', shot='life-steps', box=(0, 0, 1260, 304), shot2=('life-goals', (0, 0, 1536, 973)),
     how=['Write one goal for each part of your life.', 'Break your top goal into small steps with dates.', 'Glue a picture in each vision board box.'],
     lead='The same idea in Notion: goals that fill up as you tick each step, and a vision board with a photo for every dream.',
     feats=[('Goals', 'Every goal with its own progress bar.'), ('Next steps', 'Steps due this month and any that are late.'),
            ('Vision board', 'Every dream with a photo, and the date you want it by.'), ('Bonus', 'The 90-Day Goal Workbook (PDF).')]),
 'job': dict(f=p_job, file='Free-Printable-Job-Application-Tracker', acc='#3E6A8A', tint='#E8EFF5', line='#D5E0EA', bg='#EEF3F7', key='job',
     title='Job Tracker', sub='Application tracker + interview prep', product='Job Application Tracker', shot='job-pipeline', box=(0, 0, 920, 815),
     how=['Write every job you apply to.', 'Update the status and next step each week.', 'Fill the prep page before each interview.'],
     lead='The same idea in Notion: every job from Wishlist to Offer, with the next step on each card.',
     feats=[('Job pipeline', 'Drag a card when a company answers.'), ('Next step', 'The next step shows on every job.'),
            ('Every job', 'Click a card to see all its details.'), ('On your phone', 'Check it in the Notion app before an interview.')]),
}

def upsell(k, s):
    crop = Image.open(os.path.join(ROOT, 'shots', 'hd3', s['shot'] + '.jpg')).crop(s['box']).convert('RGB')
    tmp = os.path.join(OUT, '_shot.jpg'); crop.save(tmp, quality=92); img = b64(tmp); os.remove(tmp)
    url = f'https://getsystemforge.gumroad.com/l/{SLUG[s["key"]]}?utm_source=gumroad&utm_medium=free-pdf&utm_campaign=free-{k}'
    how = ''.join(f'<div><b>{i}</b>{t}</div>' for i, t in enumerate(s['how'], 1))
    feats = ''.join(f'<div><b>{a}</b>{b}</div>' for a, b in s['feats'])
    return ('<section class="pg up"><div class="kick">HOW TO USE IT</div>'
            f'<div class="how" style="margin-top:12px">{how}</div>'
            f'<div class="kick" style="margin-top:6px">WANT IT TO FILL IN BY ITSELF?</div><h2>{s["product"]} for Notion</h2>'
            f'<p>{s["lead"]}</p><img src="{img}" style="max-height:4.3in;object-fit:cover;object-position:top">'
            f'<div class="feat">{feats}</div><a class="cta" href="{url}">See the {s["product"]} for Notion →</a>{foot("NEXT STEP")}</section>')

import json as _json
SLUG = {k: v['gumroad'].rstrip('/').split('/l/')[-1] for k, v in _json.load(open(os.path.join(ROOT, 'generator', 'pin-products.json')))['products'].items() if v.get('gumroad') and '/l/' in v['gumroad']}

def pin(k, s, pngs):
    sys.path.insert(0, os.path.join(ROOT, 'generator', 'v3')); import mini_listing as M
    sh = 'box-shadow:0 22px 50px rgba(40,40,40,.22);border-radius:6px;position:absolute'
    back = f"<img src='file://{pngs[1]}' style='{sh};left:420px;top:420px;width:520px;transform:rotate(5deg)'>" if len(pngs) > 1 else ''
    tsize = 140 if len(s['title']) <= 13 else 118
    html = (f"<!doctype html><html><head><meta charset='utf-8'><style>{FONTS}body{{margin:0}}</style></head><body>"
            f"<div style='position:relative;width:1000px;height:1500px;overflow:hidden;background:{s['bg']};font-family:IN'>"
            f"<div style='position:absolute;top:60px;width:1000px;text-align:center;font:700 26px IN;letter-spacing:8px;color:{s['acc']}'>FREE PRINTABLE</div>"
            f"<div style='position:absolute;top:{96 + (140 - tsize) // 2}px;width:1000px;text-align:center;font:{tsize}px/1.1 GV;color:#2E2A25'>{s['title']}</div>"
            f"<div style='position:absolute;top:278px;width:1000px;text-align:center;font:500 32px IN;color:#5F5A55'>{s['sub']}</div>"
            f"{back}<img src='file://{pngs[0]}' style='{sh};left:70px;top:380px;width:640px;transform:rotate(-3deg)'>"
            f"<div style='position:absolute;left:690px;top:1170px;width:230px;height:230px;border-radius:115px;background:{s['acc']};color:#fff;display:flex;align-items:center;justify-content:center;text-align:center;font:700 30px/1.2 IN'>Free<br>PDF</div>"
            "<div style='position:absolute;bottom:34px;width:1000px;text-align:center;font:700 22px IN;letter-spacing:3px;color:#8A847D'>SYSTEMFORGE · INSTANT DOWNLOAD</div></div></body></html>")
    hp = os.path.join(OUT, '_pin.html'); open(hp, 'w').write(html)
    subprocess.run([M.L.B.CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', '--force-device-scale-factor=2',
                    '--window-size=1000,1700', '--virtual-time-budget=3000', f'--screenshot={hp}.png', 'file://' + hp], check=True, capture_output=True)
    out = os.path.join(ROOT, 'pins', 'v5', f'free-{k}-a1.png')
    Image.open(hp + '.png').crop((0, 0, 2000, 3000)).convert('RGB').save(out, optimize=True); os.remove(hp); os.remove(hp + '.png')
    return out

def build(k):
    s = SETS[k]
    css = CSS.replace('var(--acc)', s['acc']).replace('var(--tint)', s['tint']).replace('var(--line)', s['line'])
    pages = s['f']() + [upsell(k, s)]
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(pages)}</body></html>"
    hp = os.path.join(OUT, f'_{k}.html'); open(hp, 'w').write(html)
    pdf = os.path.join(OUT, s['file'] + '.pdf')
    js = (f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();"
          f"await p.goto('file://{hp}');await p.waitForTimeout(800);await p.pdf({{path:'{pdf}',width:'8.5in',height:'11in',printBackground:true}});await b.close();}})()")
    subprocess.run(['node', '-e', js], check=True); os.remove(hp)
    for f in os.listdir(OUT):
        if f.startswith(s['file'] + '-p-'): os.remove(os.path.join(OUT, f))
    subprocess.run(['pdftoppm', '-r', '150', '-png', pdf, os.path.join(OUT, s['file'] + '-p')], check=True)
    pngs = sorted(os.path.join(OUT, f) for f in os.listdir(OUT) if f.startswith(s['file'] + '-p-'))
    print(pdf, len(pages), 'pages', pin(k, s, pngs))

if __name__ == '__main__':
    for k in sys.argv[1:] or list(SETS):
        build(k)
