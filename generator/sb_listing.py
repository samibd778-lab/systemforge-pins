"""Second Brain OS listing images from REAL 2x screenshots (brand/shots/sb/*.png).
Etsy: 10 images 2000x1500 -> etsy/sb/listing/  |  Gumroad: cover 1280x720 + thumb 600x600 -> products/second-brain/gumroad/
Gumroad images never use hero1240 (it shows the Etsy footer)."""
import base64, pathlib, subprocess, sys
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'generator' / 'styles'))
from pins_v2 import FONT_CSS  # noqa
S = ROOT / 'brand/shots/sb'
TMP = pathlib.Path('/tmp/sb_listing'); TMP.mkdir(exist_ok=True)
DM = (ROOT / 'brand/fonts/dmserif.woff2').as_uri()

def crop(name, box, out):
    im = Image.open(S / f'{name}.png'); im.crop(box).save(TMP / f'{out}.png'); return (TMP / f'{out}.png').as_uri()

shots = {
    'home': crop('home', (0, 0, 2110, 2565), 'home'),
    'hometop': crop('home', (0, 0, 2110, 1600), 'hometop'),
    'widget': crop('home', (180, 1050, 2090, 2565), 'widget'),
    'goals': crop('goals', (150, 90, 2120, 1325), 'goals'),
    'projects': crop('projects', (150, 345, 2170, 1325), 'projects'),
    'next7': crop('next7', (150, 150, 2120, 1070), 'next7'),
    'habits': crop('habits', (150, 160, 2170, 1000), 'habits'),
    'month': crop('month', (150, 330, 2120, 1325), 'month'),
    'journal': crop('journal', (150, 200, 2120, 1325), 'journal'),
    'monthly': crop('monthly', (380, 60, 1900, 1325), 'monthly'),
}
guide = ROOT / 'products/second-brain/Notion-Beginner-Guide.pdf'
subprocess.run(['pdftoppm', '-r', '90', '-png', '-f', '1', '-l', '3', str(guide), str(TMP / 'g')], check=True)
g = [(TMP / f'g-{i}.png').as_uri() for i in (1, 2, 3)]

CSS = FONT_CSS + f'''
@font-face{{font-family:DMS;src:url({DM})}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:2000px;height:1500px;overflow:hidden;font-family:InterW;color:#2E2A25;background:#F6F1E9;position:relative}}
.dark{{background:#1F3324;color:#F3ECE2}}
.k{{font-weight:700;font-size:26px;letter-spacing:.16em;text-transform:uppercase;color:#7A8B6F}}
.dark .k{{color:#BFD3B8}}
h1{{font-family:DMS;font-weight:400;font-size:104px;line-height:1.02;letter-spacing:-.5px}}
h1 em{{color:#C98B6B;font-style:italic}}.dark h1 em{{color:#E8C3AA}}
.sub{{font-weight:500;font-size:34px;line-height:1.45;color:#6F665B;margin-top:22px}}.dark .sub{{color:#D6CCBE}}
.head{{position:absolute;left:110px;top:100px;right:110px}}
.win{{position:absolute;background:#fff;border-radius:22px;overflow:hidden;box-shadow:0 40px 90px rgba(46,42,37,.22),0 0 0 1px rgba(46,42,37,.06)}}
.dark .win{{box-shadow:0 50px 110px rgba(0,0,0,.5)}}
.bar{{height:46px;background:#EDE7DF;display:flex;align-items:center;gap:11px;padding:0 22px}}
.bar i{{width:15px;height:15px;border-radius:50%;background:#D3C8BB}}.bar i:first-child{{background:#E39A82}}
.bar span{{margin-left:18px;font-size:17px;font-weight:700;color:#8A7A6C;background:#F7F3EE;border-radius:8px;padding:6px 90px 6px 16px}}
.win img{{display:block;width:100%}}
.brand{{position:absolute;right:110px;top:112px;display:flex;align-items:center;gap:14px;font-weight:700;font-size:26px;color:#7A8B6F}}
.dark .brand{{color:#D9E2D2}}
.logo{{width:54px;height:54px;border-radius:50%;background:#1F3324;color:#F3ECE2;display:flex;align-items:center;justify-content:center;font-size:19px}}
.dark .logo{{background:#F3ECE2;color:#1F3324}}
.pill{{display:inline-flex;align-items:center;gap:10px;background:#fff;border:1.5px solid #E7DED2;border-radius:99px;padding:14px 26px;font-weight:700;font-size:26px;margin:0 12px 12px 0}}
.dark .pill{{background:rgba(243,236,226,.08);border-color:rgba(243,236,226,.25);color:#F3ECE2}}
.ring{{position:absolute;border-radius:50%}}
'''

def win(src, style, title='Second Brain OS'):
    return f'<div class="win" style="{style}"><div class="bar"><i></i><i></i><i></i><span>{title}</span></div><img src="{src}"></div>'

def page(body, dark=False, w=2000, h=1500, extra=''):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{extra}</style></head><body class="{"dark" if dark else ""}" style="width:{w}px;height:{h}px">{body}</body></html>'

BRAND = '<div class="brand"><span class="logo">SF</span>SystemForge</div>'

def feature(k, title, sub, src, wtitle, top=520, left=110, right=110, extra_html=''):
    return page(f'''{BRAND}<div class="head"><div class="k">{k}</div><h1 style="margin-top:18px">{title}</h1><div class="sub" style="max-width:1500px">{sub}</div></div>
{win(src, f"left:{left}px;right:{right}px;top:{top}px", wtitle)}{extra_html}''')

etsy = {}
etsy['01-cover'] = page(f'''
<div class="ring" style="width:1500px;height:1500px;right:-640px;top:-760px;border:2px solid rgba(243,236,226,.12)"></div>
<div class="ring" style="width:560px;height:560px;right:-150px;top:-200px;background:#C98B6B;opacity:.92"></div>
<div class="head" style="top:110px"><div class="k">Notion template · PARA method</div>
<h1 style="font-size:150px;margin-top:22px">Second Brain <em>OS</em></h1>
<div class="sub" style="font-size:38px;max-width:1150px">Your goals, projects, notes, habits, journal and books in one calm Notion home.</div>
<div style="margin-top:34px"><span class="pill">🎯 Goals</span><span class="pill">🚀 Projects</span><span class="pill">✔️ Habits</span><span class="pill">📓 Journal</span><span class="pill">📖 Books</span><span class="pill" style="background:#C98B6B;border-color:#C98B6B">🎁 Bonus guide</span></div></div>
{win(shots['hometop'], 'left:300px;right:-80px;top:760px')}''', dark=True)

items = [('🏠', 'Home dashboard', 'Today widget, menu, daily + weekly routine'), ('🎯', 'Goals', 'Progress fills up as projects are done'),
         ('🚀', 'Projects', 'Board with progress bars and days left'), ('✅', 'Tasks', 'Next 7 days list + calendar'),
         ('🗒️', 'Notes + Quick capture', 'Inbox, key takeaways, favorites'), ('🧭', 'Areas + 📚 Resources', 'The PARA method, ready to use'),
         ('✔️', 'Habit tracker', '5 habits you can rename, daily score'), ('📓', 'Daily journal', 'Mood, energy, one win, gratitude'),
         ('📖', 'Reading list', 'Bookshelf with progress and key idea'), ('🔁', 'Reviews', 'Weekly, monthly and yearly pages'),
         ('📱', 'Mobile home', 'A light page for your phone'), ('📘', '5 guides + bonus PDF', 'Start here, PARA, notes, FAQ')]
cards = ''.join(f'<div class="c"><div class="e">{e}</div><div><b>{t}</b><p>{d}</p></div></div>' for e, t, d in items)
etsy['02-whats-inside'] = page(f'''{BRAND}<div class="head"><div class="k">What's inside</div><h1 style="margin-top:18px">Everything in <em>one place</em></h1></div>
<div class="grid">{cards}</div>''', extra='''.grid{position:absolute;left:110px;right:110px;top:400px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:26px}
.c{background:#fff;border:1.5px solid #E7DED2;border-radius:24px;padding:34px 30px;display:flex;gap:24px;align-items:flex-start;min-height:220px}
.e{flex:none;width:84px;height:84px;border-radius:22px;background:#E3E8DC;display:flex;align-items:center;justify-content:center;font-size:44px}
.c:nth-child(even) .e{background:#F1DDCF}.c b{display:block;font-size:34px;margin:6px 0 10px}.c p{font-weight:500;font-size:26px;line-height:1.4;color:#6F665B}''')

etsy['03-today-widget'] = feature('Your home dashboard', 'Start every day <em>clear</em>', 'A live Today widget: clock, how much of the day, week, month and year is left, a mini calendar and a thought for the day.', shots['widget'], 'Second Brain OS', top=500)
etsy['04-goals'] = feature('Goals', 'Big goals, <em>visible</em> progress', 'Link projects to a goal. Its bar fills up as the projects are done.', shots['goals'], 'Goals', top=500)
etsy['05-projects'] = feature('Projects', 'Every project <em>on one board</em>', 'Drag a card when a project moves. Progress bars and days left update by themselves.', shots['projects'], 'Projects', top=500)
etsy['06-tasks'] = feature('Tasks', 'Know what to do <em>next</em>', 'Next 7 days shows open tasks, late ones first. Plus a calendar of every task by due date.', shots['next7'], 'Next 7 days', top=520)
etsy['07-habits'] = feature('Habit tracker', 'Small habits, <em>every day</em>', 'One row per day. Tick what you did. Rename the 5 habits to fit your life.', shots['habits'], 'Habits this week', top=520)
etsy['08-mood'] = feature('This month', 'See how your <em>month</em> felt', 'Your mood board and weekly ratings fill in by themselves from your Journal and Weekly reviews.', shots['month'], 'This month', top=500)
etsy['09-journal-books'] = feature('Journal + reading list', 'Reflect and <em>keep learning</em>', 'A 2-minute daily check-in, and a bookshelf with progress, rating and the key idea of each book.', shots['journal'], 'Journal + Bookshelf', top=500)
etsy['10-bonus-reviews'] = page(f'''{BRAND}<div class="head"><div class="k">Included</div><h1 style="margin-top:18px">Reviews + a <em>bonus guide</em></h1>
<div class="sub" style="max-width:1500px">Weekly, monthly and yearly review pages. And a 7-page PDF that teaches you Notion in 15 minutes.</div></div>
{win(shots['monthly'], 'left:110px;width:900px;top:560px', 'Monthly review')}
<img src="{g[0]}" style="position:absolute;left:1090px;top:600px;width:470px;border-radius:14px;box-shadow:0 30px 70px rgba(46,42,37,.28);transform:rotate(-4deg)">
<img src="{g[2]}" style="position:absolute;left:1440px;top:660px;width:450px;border-radius:14px;box-shadow:0 30px 70px rgba(46,42,37,.28);transform:rotate(5deg)">''')

gum = {
    'gumroad-cover': page(f'''
<div class="ring" style="width:900px;height:900px;right:-380px;top:-460px;border:2px solid rgba(243,236,226,.12)"></div>
<div class="ring" style="width:330px;height:330px;right:-90px;top:-120px;background:#C98B6B;opacity:.92"></div>
<div style="position:absolute;left:64px;top:70px;width:470px"><div class="k" style="font-size:15px">Notion template · PARA</div>
<h1 style="font-size:78px;margin-top:14px">Second Brain <em>OS</em></h1>
<div class="sub" style="font-size:21px;margin-top:16px">Goals, projects, notes, habits, journal and books in one calm Notion home.</div>
<div style="margin-top:26px;font-weight:700;font-size:17px;color:#E8C3AA">+ Bonus guide: Notion for beginners</div></div>
{win(shots['hometop'], 'left:575px;right:-40px;top:120px;border-radius:14px')}''', dark=True, w=1280, h=720,
        extra='.bar{height:28px;gap:7px;padding:0 14px}.bar i{width:9px;height:9px}.bar span{font-size:10px;padding:4px 50px 4px 10px;margin-left:10px}'),
    'gumroad-thumb': page(f'''
<div class="ring" style="width:300px;height:300px;right:-110px;top:-120px;background:#C98B6B;opacity:.92"></div>
<div style="position:absolute;left:46px;top:50px"><div class="k" style="font-size:14px">Notion template</div>
<h1 style="font-size:72px;margin-top:12px">Second<br>Brain <em>OS</em></h1></div>
{win(shots['hometop'], 'left:46px;right:-60px;top:300px;border-radius:12px')}''', dark=True, w=600, h=600,
        extra='.bar{height:22px;gap:6px;padding:0 10px}.bar i{width:7px;height:7px}.bar span{font-size:8px;padding:3px 30px 3px 8px;margin-left:8px}'),
}

def render(pages, outdir, w, h):
    outdir.mkdir(parents=True, exist_ok=True)
    items = []
    for name, html in pages.items():
        p = TMP / f'{name}.html'; p.write_text(html); items.append((p.as_uri(), str(outdir / f'{name}.png'), w, h))
    js = "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();for(const [u,o,w,h] of " + str(items).replace("'", '"').replace('(', '[').replace(')', ']') + "){const p=await b.newPage({viewport:{width:w,height:h}});await p.goto(u);await p.waitForTimeout(400);await p.screenshot({path:o});await p.close();}await b.close();})()"
    subprocess.run(['node', '-e', js], check=True)

render(etsy, ROOT / 'etsy/sb/listing', 2000, 1500)
render({'gumroad-cover': gum['gumroad-cover']}, ROOT / 'products/second-brain/gumroad', 1280, 720)
render({'gumroad-thumb': gum['gumroad-thumb']}, ROOT / 'products/second-brain/gumroad', 600, 600)
print('done')
