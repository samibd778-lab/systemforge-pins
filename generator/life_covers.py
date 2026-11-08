"""SVG/PNG covers (1500x600) for Goals and Milestones sample rows of the Life Planner (Gumroad original).
Vision Board rows use real photos. Writes covers/life/<page_id>.png. Usage: python3 generator/life_covers.py"""
import os, asyncio
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, 'mini_covers.py')).read().split('# ================= PROPOSAL TRACKER')[0]
exec(_src)
C = {}
AR = {'Health': SAGE, 'Career': BLUE, 'Money': '#E0B04F', 'Relationships': PINK, 'Growth': PURP, 'Fun': ACC}


def lines_of(t):
    if len(t) <= 17: return [t]
    w = t.split(' '); best = None
    for k in range(1, len(w)):
        a, b = ' '.join(w[:k]), ' '.join(w[k:])
        sc = max(len(a), len(b))
        if best is None or sc < best[0]: best = (sc, [a, b])
    return best[1]


def progress_card(area, done, total, col):
    out = f"<rect x='980' y='120' width='300' height='360' rx='18' fill='{PAPER}'/><text x='1010' y='170' font-family='{SANS}' font-size='18' font-weight='700' fill='{MUT}' letter-spacing='3'>PROGRESS</text>"
    p = done / total if total else 0
    out += f"<text x='1010' y='260' font-family='{SERIF}' font-size='56' font-weight='700' fill='{INK}'>{round(p*100)}%</text>"
    for i in range(10):
        out += f"<rect x='{1010+i*24}' y='290' width='18' height='26' rx='5' fill='{col if i < round(p*10) else LINE}'/>"
    out += f"<text x='1010' y='360' font-family='{SANS}' font-size='19' fill='{MUT}'>{done} of {total} steps</text>" if total else f"<text x='1010' y='360' font-family='{SANS}' font-size='19' fill='{MUT}'>Add your first steps</text>"
    bw = tw(area, 18) + 40
    out += f"<rect x='1010' y='410' width='{bw}' height='38' rx='19' fill='{col}'/><text x='1030' y='435' font-family='{SANS}' font-size='18' font-weight='700' fill='{PAPER}'>{esc(area)}</text>"
    return out

GOALS = [
    ('412727ea08a481e3ad6bd3590329ff16', 'Run a 10K race', 'Health', 2, 5, 'Dec 13'),
    ('412727ea08a48101abe3cca556823415', 'Save a $5,000 emergency fund', 'Money', 2, 4, 'Dec 31'),
    ('412727ea08a48100a58cc14a4b3f2a49', 'Get promoted to Senior Designer', 'Career', 1, 4, 'Mar 31'),
    ('412727ea08a48115ac65ce9e81351b1c', 'Read 12 books', 'Growth', 2, 3, 'Dec 31'),
    ('412727ea08a481dca164e4a30bcf59b0', 'Weekly date night', 'Relationships', 2, 2, 'Oct 31'),
    ('412727ea08a481b1816ee4305be6b90c', 'Learn to play guitar', 'Fun', 0, 0, 'Mar 31'),
]
GN = {g[0]: g for g in GOALS}
for i, (pid, name, area, d, t, when) in enumerate(GOALS):
    C[pid] = base(i, title_block('GOAL', lines_of(name), [(area, AR[area]), (when, INK)], size=54) + progress_card(area, d, t, AR[area]))

MS = [  # id, name, goal id, due, done, late
    ('412727ea08a481c2ba4fd4048bd84251', 'Run 3 times a week for 4 weeks', '412727ea08a481e3ad6bd3590329ff16', 'Oct 15', True),
    ('412727ea08a481399adcfd8888b21266', 'Run 5K without stopping', '412727ea08a481e3ad6bd3590329ff16', 'Nov 1', True),
    ('412727ea08a481059f4ee0e7f274749b', 'Sign up for a 10K race', '412727ea08a481e3ad6bd3590329ff16', 'Nov 10', False),
    ('412727ea08a4810ab947fea447a71158', 'Run 8K', '412727ea08a481e3ad6bd3590329ff16', 'Nov 22', False),
    ('412727ea08a481ba80cbe2c43eba46a7', 'Race day', '412727ea08a481e3ad6bd3590329ff16', 'Dec 13', False),
    ('412727ea08a4812a85fdfa672ae3f2ff', 'Open a high-yield savings account', '412727ea08a48101abe3cca556823415', 'Feb 1', True),
    ('412727ea08a481c7b6d1d336eec80dbc', 'Save $2,500', '412727ea08a48101abe3cca556823415', 'Jul 1', True),
    ('412727ea08a481c6adbffc85e21e6db9', 'Save $4,000', '412727ea08a48101abe3cca556823415', 'Nov 30', False),
    ('412727ea08a48130bd3cdeb1f4c178e7', 'Save $5,000', '412727ea08a48101abe3cca556823415', 'Dec 31', False),
    ('412727ea08a4814c903dd18401099977', 'Talk to my manager about the path', '412727ea08a48100a58cc14a4b3f2a49', 'Oct 10', True),
    ('412727ea08a48191910fe927064db10e', 'Finish a portfolio case study', '412727ea08a48100a58cc14a4b3f2a49', 'Nov 5', 'late'),
    ('412727ea08a481ad8829e1e06b342b4b', 'Lead one project from start to end', '412727ea08a48100a58cc14a4b3f2a49', 'Jan 15', False),
    ('412727ea08a48183bc4fd83487011b6b', 'Ask for the promotion review', '412727ea08a48100a58cc14a4b3f2a49', 'Mar 1', False),
    ('412727ea08a48187b75cec9b0e24ecba', 'Books 1 to 6', '412727ea08a48115ac65ce9e81351b1c', 'Jun 30', True),
    ('412727ea08a4815cb823fd00f4ca4e9b', 'Books 7 to 9', '412727ea08a48115ac65ce9e81351b1c', 'Sep 30', True),
    ('412727ea08a4811cb82dd452b5336168', 'Books 10 to 12', '412727ea08a48115ac65ce9e81351b1c', 'Dec 31', False),
    ('412727ea08a481f99f4ddb8b9fdb8f8b', 'Plan 4 date nights', '412727ea08a481dca164e4a30bcf59b0', 'Oct 1', True),
    ('412727ea08a4815ebf6ce02209f89058', 'Book a cooking class together', '412727ea08a481dca164e4a30bcf59b0', 'Oct 31', True),
]
for i, (pid, name, gid, due, st) in enumerate(MS):
    g = GN[gid]; col = AR[g[2]]
    badge = ('Done', SAGE) if st is True else ('Late', RED) if st == 'late' else ('To do', ACC)
    gl = g[1] if len(g[1]) <= 19 else ' '.join(g[1].split(' ')[:3])
    C[pid] = base(i, title_block('MILESTONE', lines_of(name), [(due, INK), (badge[0], badge[1])], size=50)
                  + doc('GOAL', [(gl, col), ('Due ' + due, SAGE), (badge[0], badge[1])]))


async def main():
    from playwright.async_api import async_playwright
    out = os.path.join(os.path.dirname(HERE), 'covers', 'life'); os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1500, 'height': 600})
        for k, svg in C.items():
            await pg.set_content(f"<html><body style='margin:0'>{svg}</body></html>")
            await pg.screenshot(path=os.path.join(out, k + '.png'))
        await b.close()
    print(len(C))

asyncio.run(main())
