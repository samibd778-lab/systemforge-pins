"""Pinterest pins (1000x1500, rendered 2x = 2000x3000) from the Etsy listing images:
the scene half of each listing image (real Notion screen on a laptop + a readable card) under a keyword title.
Keywords: research/pinclicks-keywords-2026-11-11.md (PinClicks, Pinterest volumes).
Usage: python3 generator/v3/half_pins.py [habit budget ...] -> pins/v4/<id>.png"""
import os, subprocess, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import mini_listing as M  # noqa: E402  (colors)
L = M.L; B = L.B
FIN = os.path.join(ROOT, 'canva', 'v3', 'etsy', 'final')
OUT = os.path.join(ROOT, 'pins', 'v4'); TMP = os.path.join(OUT, '_tmp'); os.makedirs(TMP, exist_ok=True)
INK, MUT = '#2E2A25', '#5C554C'

# (image n, kicker = Pinterest keyword, title hook, sub = a true detail from the product)
S = {
 'habit': [
  (1, 'HABIT TRACKER IDEAS', 'The habit tracker I finally stuck to', 'Tick it every day. Your score fills in by itself.'),
  (2, 'DAILY HABIT TRACKER', 'Six habits, one row a day', 'Your score and day type show up by themselves.'),
  (3, 'MONTHLY HABIT TRACKER', 'A bar for every habit', 'Your best habit and your perfect days, every month.'),
  (4, 'HABIT TRACKER TEMPLATE', 'Your month at a glance', 'A calendar with your score on every day.'),
  (5, 'NOTION HABIT TRACKER', 'How to make a habit stick', 'The cue, the tiny version for busy days and your reward.')],
 'budget': [
  (1, 'BUDGET PLANNER', 'Know what is left every month', 'See what is left, never miss a bill, watch your debt go down.'),
  (2, 'MONTHLY BUDGET PLANNER', 'See what is left in every category', 'What you spent, what is left and if you are on track.'),
  (3, 'BUDGET PLANNER TEMPLATE', 'Never miss a bill again', 'Every bill with its due day: paid, due soon or late.'),
  (4, 'BUDGET PLANNER IDEAS', 'Every dollar, in and out', 'Pick a category and the budget updates.'),
  (5, 'NOTION BUDGET TEMPLATE', 'Savings goals with a deadline', 'See how much to save each month to hit your goal on time.')],
 'journal': [
  (1, 'JOURNAL IDEAS', 'A 2-minute journal you will actually keep', 'Your mood, one win and one thank you.'),
  (2, 'DAILY JOURNAL', 'One entry a day', 'Mood, energy, one win and one thing you are grateful for.'),
  (3, 'GRATITUDE JOURNAL', 'A jar for every thank you', 'Every thank you you wrote, in one place.'),
  (4, 'MOOD TRACKER', 'See how your month felt', 'Average mood, great days and low days for every month.'),
  (5, 'NOTION JOURNAL TEMPLATE', 'Your mood calendar', 'See your month at a glance and keep your favorite days.')],
 'life': [
  (1, 'LIFE PLANNER', 'Big dreams, small steps you can finish', 'Goals, milestones and a vision board on one page.'),
  (2, 'NOTION LIFE PLANNER', 'Goals that fill up as you go', 'Tick a milestone and the bar fills by itself.'),
  (3, 'VISION BOARD', 'Every dream with a photo', 'And the date you want it by.'),
  (4, 'LIFE PLANNER ORGANIZATION', 'Never miss a step', 'Steps due this month, with Late and This week flags.'),
  (5, 'LIFE PLANNER IDEAS', 'Score 8 areas of your life', 'Check in with your life and see where to grow.')],
 'meal': [
  (1, 'MEAL PLANNER', 'No more "what is for dinner?"', 'Plan the week, cook what you love, shop with one list.'),
  (2, 'WEEKLY MEAL PLANNER', 'Plan the whole week', 'Breakfast, lunch, dinner and snacks, each linked to a recipe.'),
  (3, 'MEAL PLANNER TEMPLATE', 'All your recipes in one place', 'Time, rating and tags on every card. Favorites first.'),
  (4, 'NOTION MEAL PLANNER', 'A grocery list sorted by aisle', 'Quantity, price and the recipe that needs each item.'),
  (5, 'MEAL PREP PLANNER', 'The next 7 days, planned', 'Tick Cooked when it is done. Plan leftovers too.')],
 'travel': [
  (1, 'TRAVEL PLANNER', 'Every trip on one page', 'Dates, plans, bookings, budget and packing.'),
  (2, 'TRAVEL PLANNER TEMPLATE', 'A countdown for every trip', 'Days to go, budget left and how much is packed.'),
  (3, 'TRAVEL ITINERARY PLANNER', 'Never forget to book', 'Plans not booked yet, with the date and the cost.'),
  (4, 'NOTION TRAVEL PLANNER', 'One page per trip', 'Budget left, packing bar and the itinerary with confirmation numbers.'),
  (5, 'PACKING LIST', 'Pack smarter', 'A packing list grouped by type. Tick Packed as you go.')],
 'job': [
  (1, 'JOB APPLICATION TRACKER', 'Track every job application', 'Every job, interview and follow-up in one place.'),
  (2, 'JOB SEARCH ORGANIZATION', 'One board for every job', 'From Wishlist to Offer, with the next step on each card.'),
  (3, 'JOB APPLICATION TRACKER', 'Follow up on time', 'Jobs with no answer after 7 days show up here.'),
  (4, 'INTERVIEW PREP', 'Walk in prepared', 'A prep checklist and the STAR method, with a real example.'),
  (5, 'JOB SEARCH TIPS', 'Follow-up emails ready to copy', 'Change the words in brackets, send it, done.')],
}
NAMES = {k: v['name'] for k, v in M.PROD.items()}


def img_path(pk, n):
    for f in os.listdir(os.path.join(FIN, pk)):
        if f.startswith(f'{pk}-{n}-') and f.endswith('.png'):
            return os.path.join(FIN, pk, f)
    raise FileNotFoundError(pk, n)


def half(pk, n):
    """the half of the listing image with the scene (more detail than the plain text half)"""
    im = Image.open(img_path(pk, n)).convert('RGB'); w, h = im.size; hw = 1380 if n == 1 else 1550
    a, b = im.crop((0, 0, hw, h)), im.crop((w - hw, 0, w, h))
    s = lambda q: float(np.asarray(q.convert('L'), dtype=np.float32).std())
    p = os.path.join(TMP, f'{pk}-{n}.jpg'); (a if s(a) > s(b) else b).save(p, quality=92)
    return p, round(h * 1000 / hw)


def html(pk, n, kicker, title, sub):
    p = M.PROD[pk]; c, acc = p['color'], p['accent']; hp, ih = half(pk, n)
    return (f'<div style="position:relative;width:1000px;height:1500px;overflow:hidden;background:{c}">'
            f'<div style="position:absolute;left:0;top:430px;width:1000px;height:1070px;background:url(file://{hp}) 0 {1070 - ih}px/1000px {ih}px no-repeat"></div>'
            f'<div style="position:absolute;left:0;top:430px;width:1000px;height:120px;background:linear-gradient({c},rgba(0,0,0,0))"></div>'
            f'<div style="position:absolute;left:70px;top:66px;width:860px">'
            f'<p style="margin:0 0 18px;font-size:24px;font-weight:700;letter-spacing:3px;color:{acc}">{kicker}</p>'
            f'<p style="margin:0 0 20px;font-size:74px;line-height:1.06;text-wrap:balance;color:{INK};{L.SER}">{title}</p>'
            f'<p style="margin:0;width:840px;font-size:31px;line-height:1.35;color:{MUT}">{sub}</p></div>'
            f'<p style="position:absolute;left:70px;bottom:56px;margin:0;padding:14px 26px;border-radius:999px;background:rgba(255,253,249,.94);font-size:24px;font-weight:700;color:{INK}">{NAMES[pk]} · Notion template</p>'
            '</div>')


def render(pid, body):
    F = os.path.join(ROOT, 'generator', 'remotion', 'public')
    h = os.path.join(TMP, '_p.html')
    open(h, 'w').write(L.HEAD.replace('</head>', L.FONTS % (F, F, F) + '</head>') + body + '</body></html>')
    shot = h + '.png'
    subprocess.run([B.CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=2', '--window-size=1000,1700', f'--screenshot={shot}', 'file://' + h], check=True, capture_output=True)
    Image.open(shot).crop((0, 0, 2000, 3000)).convert('RGB').save(os.path.join(OUT, pid + '.png'), optimize=True)
    os.remove(h); os.remove(shot)


# ---------- listicle pins (the top style for "notion template ideas") ----------
LIST = [
 ('list-ideas', 'NOTION TEMPLATE IDEAS', '8 Notion template ideas to organize your life',
  [('habit-week', 'Habit Tracker'), ('budget-categories', 'Budget Planner'), ('journal-entries', 'Daily Journal'), ('life-goals', 'Life Planner'),
   ('meal-recipes', 'Meal Planner'), ('travel-trips', 'Travel Planner'), ('job-pipeline', 'Job Tracker'), ('sb-goals', 'Second Brain')]),
 ('list-aesthetic', 'AESTHETIC NOTION TEMPLATE', 'Aesthetic Notion templates for every part of your life',
  [('life-vision', 'Vision board'), ('meal-calendar', 'Meal calendar'), ('habit-monthly', 'Monthly habits'), ('budget-savings', 'Savings goals'),
   ('journal-gratitude', 'Gratitude jar'), ('travel-pack', 'Packing list'), ('job-prep', 'Interview prep'), ('sb-journal', 'Daily journal')]),
]


def tile(name):
    f = os.path.join(L.B.HD, name + ('.png' if name.startswith('sb-') else '.jpg'))
    im = Image.open(f).convert('RGB'); w = im.width
    t = im.crop((0, 0, w, min(im.height, int(w * 0.62))))
    t.thumbnail((900, 900)); p = os.path.join(TMP, 't-' + name + '.jpg'); t.save(p, quality=90)
    return p


def listicle(kicker, title, tiles):
    cells = ''.join(
        f'<div style="background:#FFFDF9;border-radius:18px;overflow:hidden;box-shadow:0 6px 18px rgba(60,40,20,.12)">'
        f'<div style="height:172px;background:url(file://{tile(n)}) top center/cover"></div>'
        f'<p style="margin:0;padding:12px 16px;font-size:23px;font-weight:700;color:{INK}">{i + 1}. {lab}</p></div>'
        for i, (n, lab) in enumerate(tiles))
    return (f'<div style="position:relative;width:1000px;height:1500px;overflow:hidden;background:#F1E9DE">'
            f'<div style="position:absolute;left:60px;top:60px;width:880px"><p style="margin:0 0 16px;font-size:24px;font-weight:700;letter-spacing:3px;color:#A0643C">{kicker}</p>'
            f'<p style="margin:0;font-size:66px;line-height:1.06;text-wrap:balance;color:{INK};{L.SER}">{title}</p></div>'
            f'<div style="position:absolute;left:60px;top:330px;width:880px;display:grid;grid-template-columns:1fr 1fr;gap:22px">{cells}</div>'
            f'<p style="position:absolute;left:0;bottom:40px;width:1000px;margin:0;text-align:center;font-size:24px;font-weight:700;color:{MUT}">SystemForge · Notion templates</p></div>')


if __name__ == '__main__':
    if sys.argv[1:2] == ['list']:
        for pid, k, t, tl in LIST:
            render(pid, listicle(k, t, tl)); print('png', pid)
        sys.exit()
    for pk in sys.argv[1:] or list(S):
        for n, k, t, s in S[pk]:
            pid = f'{pk}-{n}'
            render(pid, html(pk, n, k, t, s)); print('png', pid)


