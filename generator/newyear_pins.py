"""New Year value pins (2026-11-27), 1000x1500 rendered at 2x.
Built from Pinterest Trends (US): 2027 vision board, new years goals, new year journal prompts,
habit tracker ideas, budget planner. Every text comes from our real guides / free printables.
Run: python3 generator/newyear_pins.py  ->  pins/ny/ny-XX.png"""
import os, subprocess, pathlib
from PIL import Image

R = pathlib.Path(__file__).resolve().parent.parent
F = R / 'generator/remotion/public'
FREE = R / 'dl/free'
OUT = R / 'pins/ny'
OUT.mkdir(parents=True, exist_ok=True)
CH = next(p for p in ['/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
                      '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'] if os.path.exists(p))


def u(p):
    return pathlib.Path(p).as_uri()


CSS = f"""
@font-face{{font-family:FR;src:url({u(F/'fraunces600.woff2')})}}
@font-face{{font-family:I5;src:url({u(F/'inter500.woff2')})}}
@font-face{{font-family:I7;src:url({u(F/'inter700.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1000px;height:1500px;overflow:hidden;position:relative;font-family:I5}}
.kick{{font-family:I7;font-size:24px;letter-spacing:5px;text-transform:uppercase}}
h1{{font-family:FR;font-weight:600;line-height:1.02;letter-spacing:-1px}}
.foot{{position:absolute;bottom:40px;left:0;right:0;text-align:center;font-family:I7;font-size:22px;letter-spacing:4px}}
.paper{{position:absolute;background:#fff;box-shadow:0 30px 70px rgba(0,0,0,.22);border-radius:6px;overflow:hidden}}
.paper img{{width:100%;display:block}}
.badge{{display:inline-block;font-family:I7;font-size:26px;letter-spacing:2px;padding:14px 26px;border-radius:40px}}
.row{{display:flex;gap:24px;align-items:flex-start;margin-bottom:34px}}
.n{{flex:0 0 70px;height:70px;border-radius:50%;font-family:I7;font-size:30px;display:flex;align-items:center;justify-content:center}}
.rt b{{font-family:I7;font-size:40px;display:block;margin-bottom:8px}}
.rt span{{font-size:31px;line-height:1.35;opacity:.85}}
.card{{border-radius:26px;padding:34px 34px 26px}}
.card b{{font-family:I7;font-size:35px;display:block;margin-bottom:14px}}
.card li{{font-size:30px;line-height:1.38;margin:0 0 10px 32px}}
"""

THEMES = {
    'sage':  dict(bg='#E6EBDF', ink='#26301F', acc='#5F7A52', soft='#F6F8F2'),
    'cream': dict(bg='#F6F0E6', ink='#2E2A25', acc='#A8734E', soft='#FFFFFF'),
    'blush': dict(bg='#F3DED6', ink='#3A2622', acc='#B0625A', soft='#FBF1EC'),
    'navy':  dict(bg='#22304A', ink='#F5EFE4', acc='#E7C27D', soft='#2E3E5C'),
    'sand':  dict(bg='#EFE3CF', ink='#30281C', acc='#7D6A3A', soft='#FBF6EC'),
}
FOOT = 'SYSTEMFORGE'
SRC = R / 'pins/ny/src'


def peek(T, img, top=1150):
    if not img:
        return ''
    return (f'<div class="paper" style="left:230px;top:{top}px;width:540px;transform:rotate(-3deg)"><img src="{u(img)}"></div>'
            f'<div style="position:absolute;left:0;right:0;bottom:0;height:110px;background:{T["bg"]}"></div>')


def printable(t, kick, title, imgs, badge, size=96):
    """Free printable: title on top, 1 or 2 real pages fanned below."""
    T = THEMES[t]
    pages = ''
    if len(imgs) == 1:
        pages = f'<div class="paper" style="left:190px;top:560px;width:620px;transform:rotate(-2deg)"><img src="{u(imgs[0])}"></div>'
    else:
        pages = (f'<div class="paper" style="left:90px;top:600px;width:520px;transform:rotate(-6deg)"><img src="{u(imgs[0])}"></div>'
                 f'<div class="paper" style="left:400px;top:560px;width:520px;transform:rotate(4deg)"><img src="{u(imgs[1])}"></div>')
    return f'''<body style="background:{T['bg']};color:{T['ink']}">
<div style="position:absolute;left:70px;right:70px;top:80px;text-align:center">
<div class="kick" style="color:{T['acc']}">{kick}</div>
<h1 style="font-size:{size}px;margin-top:22px">{title}</h1>
<div class="badge" style="margin-top:28px;background:{T['acc']};color:{T['bg']}">{badge}</div></div>
{pages}
<div class="foot" style="color:{T['acc']};background:{T['bg']};padding-top:22px;bottom:0;height:100px">{FOOT}</div></body>'''


def steps(t, kick, title, items, note='', size=90, img=None):
    """Numbered tips list. items = [(bold, text)]."""
    T = THEMES[t]
    rows = ''.join(f'<div class="row"><div class="n" style="background:{T["acc"]};color:{T["bg"]}">{i+1}</div>'
                   f'<div class="rt"><b>{b}</b><span>{s}</span></div></div>' for i, (b, s) in enumerate(items))
    nt = f'<div style="margin-top:14px;font-family:I7;font-size:28px;color:{T["acc"]}">{note}</div>' if note else ''
    return f'''<body style="background:{T['bg']};color:{T['ink']}">
<div style="position:absolute;left:80px;right:80px;top:90px">
<div class="kick" style="color:{T['acc']}">{kick}</div>
<h1 style="font-size:{size}px;margin:20px 0 50px">{title}</h1>
<div style="background:{T['soft']};border-radius:30px;padding:46px 44px 16px">{rows}</div>{nt}</div>
{peek(T, img)}<div class="foot" style="color:{T['acc']}">{FOOT}</div></body>'''


def grid(t, kick, title, cards, note='', size=90, img=None):
    """2x2 cards. cards = [(head, [lines])]."""
    T = THEMES[t]
    cs = ''.join(f'<div class="card" style="background:{T["soft"]}"><b style="color:{T["acc"]}">{h}</b><ul>'
                 + ''.join(f'<li>{x}</li>' for x in ls) + '</ul></div>' for h, ls in cards)
    nt = f'<div style="margin-top:34px;font-family:I7;font-size:30px;text-align:center;color:{T["acc"]}">{note}</div>' if note else ''
    return f'''<body style="background:{T['bg']};color:{T['ink']}">
<div style="position:absolute;left:70px;right:70px;top:90px">
<div class="kick" style="color:{T['acc']}">{kick}</div>
<h1 style="font-size:{size}px;margin:20px 0 46px">{title}</h1>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px">{cs}</div>{nt}</div>
{peek(T, img)}<div class="foot" style="color:{T['acc']}">{FOOT}</div></body>'''


def listing(t, kick, title, items, img=None, size=84):
    """Two-column list of short lines (prompts / ideas), optional page peek at the bottom."""
    T = THEMES[t]
    half = (len(items) + 1) // 2
    col = lambda xs, st: ''.join(f'<div style="font-size:31px;line-height:1.3;margin-bottom:24px"><span style="font-family:I7;color:{T["acc"]}">{st+i:02d}</span>&nbsp; {x}</div>' for i, x in enumerate(xs))
    pk = f'<div class="paper" style="left:250px;top:1160px;width:500px;transform:rotate(-2deg)"><img src="{u(img)}"></div>' if img else ''
    return f'''<body style="background:{T['bg']};color:{T['ink']}">
<div style="position:absolute;left:80px;right:80px;top:90px">
<div class="kick" style="color:{T['acc']}">{kick}</div>
<h1 style="font-size:{size}px;margin:20px 0 44px">{title}</h1>
<div style="display:flex;gap:40px"><div style="flex:1">{col(items[:half],1)}</div><div style="flex:1">{col(items[half:],half+1)}</div></div></div>
{pk}
<div class="foot" style="color:{T['acc']};background:{T['bg']};padding-top:22px;bottom:0;height:100px">{FOOT}</div></body>'''


G = lambda n: FREE / f'Free-Printable-2027-Goal-Planner-p-{n}.png'
P = {
    # ---- goals / vision board (Life Planner + free 2027 goal planner)
    'ny-01': printable('sage', 'Free printable · 2027', '2027 goal planner<br>+ vision board', [G(1), G(3)], 'FREE PDF · PRINT AT HOME'),
    'ny-02': printable('blush', 'New year vision board', 'Make your 2027<br>vision board on paper', [G(3)], 'FREE PRINTABLE', size=88),
    'ny-03-tip': steps('cream', 'New years goals', 'How to set 2027 goals you’ll actually keep', [
        ('Only 1 to 3 goals', 'Each new goal takes energy from the others.'),
        ('Make it clear', '“Get fit” is vague. “Run a 10K on Dec 13” is clear.'),
        ('Write why it matters', 'On hard days, the why keeps you going.'),
        ('Pick a reward', 'Something small and fun for when it’s done.'),
        ('Choose a date', '90 days: long enough to change, short enough to focus.'),
    ]),
    'ny-04-tip': grid('sand', 'Before you set goals', 'Score your life 1 to 10 in 8 areas', [
        ('Body & mind', ['💪 Health', '🧘 Peace of mind']),
        ('Work & money', ['💼 Career', '💰 Money']),
        ('People', ['❤️ Relationships', '🎉 Fun']),
        ('Your world', ['🏠 Home', '🌱 Growth']),
    ], note='Circle the 2 lowest scores. Your first goals usually live there.', img=SRC / 'life-cover-1.png'),
    'ny-05-tip': grid('navy', 'Goal setting', 'The 10-minute Sunday goal check‑in', [
        ('👀 Look back · 3 min', ['Tick finished steps', 'Write one win', 'What got in the way?']),
        ('🗓️ Plan · 5 min', ['Pick 3 important things', 'Put them in your calendar', 'Say no to one thing']),
        ('✨ Dream · 2 min', ['Look at your vision board', 'Add a new dream', 'Remember your why']),
        ('🔁 Off track?', ['Make the next step smaller', 'Change the plan, not the goal', 'Start again this Sunday']),
    ], size=82),
    # ---- journaling (Daily Journal + free gratitude journal)
    'ny-06': listing('blush', 'Free printable', '30 gratitude journal prompts', [
        'A person who made you smile this week', 'A small thing you love about your home', 'A skill you are glad you have',
        'A meal you really enjoyed', 'A place that makes you calm', 'Something your body did for you today',
        'A friend you can always call', 'A mistake that taught you something', 'A song that lifts your mood',
        'Something you have now that you once wished for',
    ], img=FREE / 'Free-Printable-Gratitude-Journal-p-1.png', size=80),
    'ny-07-tip': grid('cream', 'New year journal prompts', 'Journal prompts for every mood', [
        ('😄 Good day', ['What made today good?', 'What am I proud of?', 'What do I want to remember?']),
        ('😔 Low day', ['What do I need right now?', 'What is still okay today?', 'Who can I talk to?']),
        ('😣 Stressed', ['What exactly is worrying me?', 'What part can I control?', 'What can wait until tomorrow?']),
        ('😐 Normal day', ['What surprised me today?', 'What made me smile?', 'What did I learn?']),
    ], img=SRC / 'journal-cover-1.png'),
    'ny-08-tip': steps('sage', 'Journaling ideas', '4 easy ways to start journaling this year', [
        ('Brain dump', 'Write everything on your mind for 5 minutes. Then close it.'),
        ('Three good things', '3 things that went well today, and why.'),
        ('Letter', 'Write to someone, or your future self. You never send it.'),
        ('One question', 'Pick one prompt and write 3 lines. Done.'),
    ], note='Small and easy beats long and rare.', img=SRC / 'journal-last-6.png'),
    'ny-09-tip': grid('navy', 'Weekly reflection', '5-minute weekly review prompts', [
        ('👀 Look back', ['Read this week’s entries', 'Find your best moment', 'Find your hard moment']),
        ('💡 Learn', ['What gave you energy?', 'What drained you?', 'Write one lesson']),
        ('🧭 Look ahead', ['Pick one focus', 'Plan one thing to look forward to']),
        ('⭐ Rate your week', ['One word for this week', 'Then close the notebook']),
    ]),
    # ---- habits (Habit Tracker + free habit tracker)
    'ny-10-tip': grid('sage', 'Habit tracker ideas', '20 small habits for the new year', [
        ('Health', ['Water first thing', 'Walk 10 min after lunch', 'Stretch 5 minutes', 'In bed by 11']),
        ('Mind', ['Read 10 pages', 'One line in a journal', 'Meditate 3 minutes', 'No phone the first hour']),
        ('Home', ['Make your bed', 'Clear the sink before bed', 'Put 10 things away', 'Prep clothes at night']),
        ('Money', ['Write down what you spend', 'No-spend day each week', 'Move $5 to savings', 'Cook dinner at home']),
    ], note='Free printable habit tracker included', img=FREE / 'Free-Printable-Habit-Tracker-p-1.png'),
    'ny-11-tip': steps('sand', 'Habit reset', 'The 30-day habit reset plan', [
        ('Week 1 · Days 1–7', 'Only the tiny versions. Don’t add new habits.'),
        ('Week 2 · Days 8–14', 'Grow 1 or 2 habits a little. Aim for 4 out of 6.'),
        ('Week 3 · Days 15–21', 'Keep the rhythm. Try one perfect day.'),
        ('Week 4 · Days 22–30', 'Change the habit that isn’t working. Plan next month.'),
    ], note='Progress, not perfection. A 4 out of 6 day is a good day.', img=SRC / 'habit-last-6.png'),
    'ny-12-tip': grid('blush', 'Habit tips', 'Missed a day? Do this, not that', [
        ('“I forgot”', ['Move the cue where you can’t miss it', 'Set one phone reminder']),
        ('“I was too tired”', ['Do the tiny version only', 'Move the habit earlier']),
        ('“I got bored”', ['Change the place or the music', 'Raise the goal a little']),
        ('“I missed a week”', ['Don’t start from zero', 'Pick 3 habits, not 6, for a while']),
    ], note='Never miss twice. One missed day is normal.', img=SRC / 'habit-cover-1.png'),
    # ---- budget (Budget Planner + free budget planner)
    'ny-13': printable('cream', 'Free printable · budget planner', 'Budget, bills, savings and debt on paper',
                       [FREE / 'Free-Printable-Budget-Planner-p-1.png', FREE / 'Free-Printable-Budget-Planner-p-2.png'], 'FREE PDF · PRINT AT HOME', size=84),
    'ny-14-tip': steps('navy', 'Budget planner', 'Money reset in 7 days', [
        ('Day 1', 'Find your real income, after tax.'),
        ('Day 2', 'List every bill and subscription with its due day.'),
        ('Day 3', 'Look at last month’s spending. Don’t judge it.'),
        ('Day 4', 'Give each category a monthly budget.'),
        ('Day 5', 'List your debts with balance and interest rate.'),
        ('Day 6', 'Pick one savings goal: start with $500.'),
        ('Day 7', 'Plan a 5-minute money check every Sunday.'),
    ], size=80),
    'ny-15-tip': grid('sand', 'Budgeting tips', 'The 50/30/20 budget on $3,000 a month', [
        ('50% · Needs', ['About $1,500', 'Rent, food, bills, transport']),
        ('30% · Wants', ['About $900', 'Fun, eating out, hobbies']),
        ('20% · Savings & debt', ['About $600', 'Safety cushion first']),
        ('Rent is high?', ['Try 60/20/20', 'The best budget is the one you keep']),
    ], note='Simple method, not financial advice.', img=SRC / 'budget-cover-1.png', size=82),
}

if __name__ == '__main__':
    tmp = OUT / '_t.html'
    for k, body in P.items():
        tmp.write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>{body}</html>')
        full = OUT / f'{k}_full.png'
        subprocess.run([CH, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                        '--allow-file-access-from-files', '--force-device-scale-factor=2', '--window-size=1000,1500',
                        f'--screenshot={full}', tmp.as_uri()], check=True, capture_output=True)
        im = Image.open(full).convert('RGB').crop((0, 0, 2000, 3000))
        im.save(OUT / f'{k}.png', optimize=True)
        full.unlink()
    tmp.unlink()
    print('ok', len(P))
