"""SVG covers (1500x600) for the two free templates, warm SystemForge style.
Writes covers.json {key: data_uri} and PNG previews."""
import json, os, sys, urllib.parse, subprocess

CREAM, PAPER, SAGE, SAGEL, CLAY, ACC, INK, MUT, LINE = '#F6F1E9', '#FFFDF9', '#7A8B6F', '#E3E8DC', '#EFDCCB', '#D9A07B', '#2E2A25', '#5C554C', '#D8D0C4'
BGS = [(CREAM, SAGEL, CLAY), (SAGEL, CLAY, CREAM), (CLAY, CREAM, SAGEL)]
SANS = 'Helvetica, Arial, sans-serif'
SERIF = 'Georgia, serif'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def tw(s, size):  # rough text width
    return int(len(s) * size * 0.56)


def pill(x, y, text, color=INK, fill=PAPER, size=18):
    w = tw(text, size) + 44
    return w, f"<rect x='{x}' y='{y}' width='{w}' height='44' rx='22' fill='{fill}'/><text x='{x+22}' y='{y+29}' font-family='{SANS}' font-size='{size}' font-weight='700' fill='{color}'>{esc(text)}</text>"


def base(bg_i, inner):
    bg, c1, c2 = BGS[bg_i % 3]
    return (f"<svg xmlns='http://www.w3.org/2000/svg' width='1500' height='600' viewBox='0 0 1500 600'>"
            f"<rect width='1500' height='600' fill='{bg}'/><circle cx='80' cy='120' r='200' fill='{c1}'/>"
            f"<circle cx='1440' cy='560' r='230' fill='{c2}'/>{inner}</svg>")


def title_block(kicker, lines, pills=(), y0=None, size=62):
    n = len(lines)
    y = y0 or (250 if n == 1 else 215)
    out = f"<text x='150' y='{y-70}' font-family='{SANS}' font-size='16' font-weight='700' fill='{SAGE}' letter-spacing='4'>{esc(kicker)}</text>"
    for i, l in enumerate(lines):
        out += f"<text x='150' y='{y+i*int(size*1.15)}' font-family='{SERIF}' font-size='{size}' font-weight='700' fill='{INK if i == 0 else MUT}'>{esc(l)}</text>"
    x, py = 150, y + (n - 1) * int(size * 1.15) + 60
    for t, c in pills:
        w, s = pill(x, py, t, c)
        out += s
        x += w + 10
    return out


def card(x, y, w, h, heading, rows, badge=None):
    out = f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='18' fill='{PAPER}'/>"
    out += f"<text x='{x+30}' y='{y+50}' font-family='{SANS}' font-size='18' font-weight='700' fill='{MUT}' letter-spacing='3'>{esc(heading)}</text>"
    ry = y + 95
    for label, val, col in rows:
        out += f"<text x='{x+30}' y='{ry}' font-family='{SANS}' font-size='19' fill='{INK}'>{esc(label)}</text>"
        if val:
            out += f"<text x='{x+w-30}' y='{ry}' text-anchor='end' font-family='{SANS}' font-size='19' font-weight='700' fill='{col}'>{esc(val)}</text>"
        out += f"<rect x='{x+30}' y='{ry+16}' width='{w-60}' height='2' fill='{LINE}'/>"
        ry += 58
    if badge:
        t, c = badge
        bw = tw(t, 18) + 40
        out += f"<rect x='{x+30}' y='{y+h-62}' width='{bw}' height='38' rx='19' fill='{c}'/><text x='{x+50}' y='{y+h-37}' font-family='{SANS}' font-size='18' font-weight='700' fill='{PAPER}'>{esc(t)}</text>"
    return out


def bars(x, y, w, items):
    out = f"<rect x='{x}' y='{y}' width='{w}' height='{60+len(items)*62}' rx='18' fill='{PAPER}'/>"
    out += f"<text x='{x+30}' y='{y+48}' font-family='{SANS}' font-size='18' font-weight='700' fill='{MUT}' letter-spacing='3'>THIS WEEK</text>"
    yy = y + 95
    for name, done, goal in items:
        out += f"<text x='{x+30}' y='{yy}' font-family='{SANS}' font-size='19' fill='{INK}'>{esc(name)}</text>"
        bx = x + 170
        for i in range(goal):
            out += f"<rect x='{bx+i*28}' y='{yy-16}' width='22' height='18' rx='4' fill='{SAGE if i < done else LINE}'/>"
        out += f"<text x='{x+w-30}' y='{yy}' text-anchor='end' font-family='{SANS}' font-size='19' font-weight='700' fill='{INK}'>{done}/{goal}</text>"
        yy += 62
    return out


def board(x, y, cols):
    out = ''
    for i, (name, n, col) in enumerate(cols):
        cx = x + i * 112
        out += f"<rect x='{cx}' y='{y}' width='100' height='300' rx='14' fill='{PAPER}'/>"
        out += f"<circle cx='{cx+22}' cy='{y+30}' r='8' fill='{col}'/><text x='{cx+36}' y='{y+36}' font-family='{SANS}' font-size='15' font-weight='700' fill='{MUT}'>{esc(name)}</text>"
        for k in range(n):
            out += f"<rect x='{cx+12}' y='{y+60+k*62}' width='76' height='50' rx='8' fill='{CREAM}'/><rect x='{cx+22}' y='{y+75+k*62}' width='50' height='8' rx='4' fill='{LINE}'/><rect x='{cx+22}' y='{y+92+k*62}' width='34' height='8' rx='4' fill='{col}'/>"
    return out


C = {}
# ---------- Invoice tracker ----------
C['inv_home'] = base(0, title_block('FREE NOTION TEMPLATE', ['Get paid on time.'], [('Late invoices', ACC), ('Next step', SAGE), ('Reminder emails', INK)], y0=260, size=64)
                     + card(960, 110, 340, 380, 'INVOICES', [('October retainer', 'Late', ACC), ('Social media pack', 'Late', ACC), ('Logo design', 'Paid', SAGE), ('Website final', 'Draft', MUT)], ('Send reminder', ACC)))
C['inv_db'] = base(1, title_block('FREELANCE INVOICE TRACKER', ['Invoices'], [('Days overdue', ACC), ('Next step', SAGE)])
                   + card(960, 120, 340, 360, 'STATUS', [('Draft', '1', MUT), ('Sent', '2', ACC), ('Paid', '2', SAGE)], ('Chase these first', ACC)))
C['inv_clients'] = base(2, title_block('FREELANCE INVOICE TRACKER', ['Clients'], [('Owes you', ACC), ('Lifetime paid', SAGE), ('Pays on time?', INK)])
                        + card(960, 120, 340, 360, 'CLIENT', [('Owes you', '$1,200', ACC), ('Lifetime paid', '$4,300', SAGE), ('Pays', 'On time', SAGE)]))
C['inv_emails'] = base(0, title_block('FREELANCE INVOICE TRACKER', ['Reminder Emails'], [('Friendly', SAGE), ('Second', ACC), ('Final notice', INK)])
                       + card(960, 120, 340, 360, 'EMAIL', [('Invoice sent', '', INK), ('Friendly reminder', '', INK), ('Second reminder', '', INK), ('Final notice', '', INK)]))
C['inv_kit'] = base(1, title_block('FREELANCE INVOICE TRACKER', ['Get Paid Faster Kit'], [('Checklist', SAGE), ('Payment terms', ACC), ('5 habits', INK)], size=58)
                    + card(960, 120, 340, 360, 'BEFORE YOU SEND', [('Due date on it', 'OK', SAGE), ('Clear line items', 'OK', SAGE), ('How to pay', 'OK', SAGE), ('Right person', 'OK', SAGE)]))

INV_ROWS = {
    'inv_r1': ('INVOICE', 'October retainer', '$1,200', 'Late', ACC),
    'inv_r2': ('INVOICE', 'Logo design', '$900', 'Paid', SAGE),
    'inv_r3': ('INVOICE', 'Website deposit 50%', '$1,750', 'Paid', SAGE),
    'inv_r4': ('INVOICE', 'Social media pack', '$650', 'Late', ACC),
    'inv_r5': ('INVOICE', 'Website final 50%', '$1,750', 'Draft', MUT),
}
for i, (k, (kick, t, amt, st, col)) in enumerate(INV_ROWS.items()):
    inner = title_block(kick, [t], [(amt, INK), (st, col)], size=58)
    inner += f"<rect x='980' y='120' width='300' height='360' rx='18' fill='{PAPER}'/><text x='1010' y='170' font-family='{SANS}' font-size='18' font-weight='700' fill='{MUT}' letter-spacing='3'>INVOICE</text>"
    for j, w in enumerate((200, 160, 220)):
        inner += f"<rect x='1010' y='{210+j*34}' width='{w}' height='12' rx='6' fill='{LINE}'/>"
    inner += f"<rect x='1010' y='330' width='240' height='2' fill='{LINE}'/><rect x='1010' y='355' width='90' height='14' rx='7' fill='{INK}'/><rect x='1160' y='352' width='90' height='20' rx='10' fill='{INK}'/>"
    bw = tw(st, 18) + 40
    inner += f"<rect x='1010' y='410' width='{bw}' height='38' rx='19' fill='{col}'/><text x='1030' y='435' font-family='{SANS}' font-size='18' font-weight='700' fill='{PAPER}'>{st}</text>"
    C[k] = base(i, inner)
for i, (k, name, comp) in enumerate([('cli_r1', 'Priya Shah', 'Bloom Studio'), ('cli_r2', 'Tom Becker', 'Becker Coffee'), ('cli_r3', 'Jane Cooper', 'Cooper & Co')]):
    inner = title_block('CLIENT', [name], [(comp, INK)], size=58)
    inner += f"<rect x='980' y='150' width='300' height='300' rx='18' fill='{PAPER}'/><circle cx='1130' cy='250' r='56' fill='{[SAGE, ACC, '#A9A196'][i]}'/><text x='1130' y='268' text-anchor='middle' font-family='{SERIF}' font-size='48' font-weight='700' fill='{PAPER}'>{name[0]}</text><rect x='1050' y='340' width='160' height='12' rx='6' fill='{LINE}'/><rect x='1075' y='370' width='110' height='12' rx='6' fill='{LINE}'/>"
    C[k] = base(i + 1, inner)

# ---------- Content planner ----------
STAGES = [('Idea', 2, '#A9A196'), ('Draft', 1, '#E2C36B'), ('Create', 1, ACC), ('Edit', 1, '#A58BB8'), ('Sched.', 1, '#7FA2C4'), ('Posted', 2, SAGE)]
C['cp_home'] = base(0, title_block('FREE NOTION TEMPLATE', ['Plan your week', 'of content.'], [('Weekly goals', SAGE), ('Pipeline', ACC), ('30 ideas', INK)], size=60)
                    + bars(900, 130, 420, [('TikTok', 1, 4), ('Instagram', 2, 3), ('YouTube', 0, 1), ('Newsletter', 0, 1)]))
C['cp_content'] = base(1, title_block('WEEKLY CONTENT PLANNER', ['Content'], [('Idea to Posted', SAGE), ('Date check', ACC)]) + board(820, 150, STAGES[:6]))
C['cp_channels'] = base(2, title_block('WEEKLY CONTENT PLANNER', ['Channels'], [('Weekly goal', SAGE), ('Progress', ACC)])
                        + bars(900, 130, 420, [('TikTok', 1, 4), ('Instagram', 2, 3), ('YouTube', 0, 1), ('Newsletter', 0, 1)]))
C['cp_hooks'] = base(0, title_block('WEEKLY CONTENT PLANNER', ['Hook Starters'], [('10 hooks', SAGE), ('First 3 seconds', ACC)])
                     + card(960, 120, 340, 360, 'HOOKS', [('Stop doing...', '', INK), ('I tried ... for ...', '', INK), ('POV: you finally...', '', INK), ('Before vs after', '', INK)]))
C['cp_ideas'] = base(1, title_block('WEEKLY CONTENT PLANNER', ['30 Content Ideas'], [('5 pillars', SAGE), ('Repurpose map', ACC)], size=58)
                     + card(960, 120, 340, 360, 'PILLARS', [('Educate', '6', SAGE), ('Entertain', '6', ACC), ('Inspire', '6', SAGE), ('Behind the scenes', '6', ACC)]))
CONTENT_ROWS = [
    ('cp_r1', '3 mistakes I made|as a new creator', 'Short video', 'Posted', SAGE),
    ('cp_r2', 'My weekly|planning routine', 'Carousel', 'Posted', SAGE),
    ('cp_r3', 'Day in my life|as a creator', 'Short video', 'Create', ACC),
    ('cp_r4', 'How I plan a month|of content', 'Long video', 'Edit', '#A58BB8'),
    ('cp_r5', 'Weekly letter #12', 'Newsletter', 'Draft', '#C9A64A'),
    ('cp_r6', 'Before / after of|my desk setup', 'Short video', 'Idea', '#A9A196'),
    ('cp_r7', '5 tools I use|every day', 'Carousel', 'Create', ACC),
]
for i, (k, t, fmt, st, col) in enumerate(CONTENT_ROWS):
    inner = title_block('CONTENT', t.split('|'), [(fmt, INK), (st, col)], size=56)
    inner += f"<rect x='1000' y='110' width='230' height='380' rx='26' fill='{INK}'/><rect x='1014' y='124' width='202' height='352' rx='16' fill='{PAPER}'/><rect x='1034' y='150' width='162' height='190' rx='10' fill='{[SAGEL, CLAY, CREAM][i%3]}'/><polygon points='1100,215 1100,275 1145,245' fill='{col}'/><rect x='1034' y='362' width='140' height='10' rx='5' fill='{LINE}'/><rect x='1034' y='386' width='100' height='10' rx='5' fill='{LINE}'/><rect x='1034' y='420' width='70' height='26' rx='13' fill='{col}'/>"
    C[k] = base(i, inner)
for i, (k, name, done, goal) in enumerate([('ch_r1', 'TikTok', 1, 4), ('ch_r2', 'Instagram', 2, 3), ('ch_r3', 'YouTube', 0, 1), ('ch_r4', 'Newsletter', 0, 1)]):
    inner = title_block('CHANNEL', [name], [(f'Goal: {goal} a week', INK)], size=60)
    inner += bars(900, 170, 420, [(name, done, goal)])
    C[k] = base(i + 2, inner)

out = {}
pdir = os.path.join(os.path.dirname(__file__), 'png')
os.makedirs(pdir, exist_ok=True)
for k, svg in C.items():
    out[k] = 'data:image/svg+xml,' + urllib.parse.quote(svg, safe="=/:,'() ")
    open(os.path.join(pdir, k + '.svg'), 'w').write(svg)
json.dump(out, open(os.path.join(os.path.dirname(__file__), 'covers.json'), 'w'))
print(len(out), max(len(v) for v in out.values()))
