"""SVG covers (1500x600) for every page of the two $4.99 templates:
Proposal Tracker and Brand Deal Tracker. Same warm style as free_covers.py.
Writes mini_covers.json {page_id: data_uri} and SVG previews in png/."""
import json, os, urllib.parse

HERE = os.path.dirname(__file__)
# Reuse the helpers from free_covers.py without running its page list.
_src = open(os.path.join(HERE, 'free_covers.py')).read().split('\nC = {}')[0]
exec(_src)

PINK, BLUE, PURP, GRAY, RED = '#D88FA6', '#7FA2C4', '#A58BB8', '#A9A196', '#C9705B'
C = {}  # page_id -> svg


def steps(x0, labels, colors):
    out = ''
    for i, (lab, c) in enumerate(zip(labels, colors)):
        x = x0 + i * 166
        cx = x + 68
        out += f"<rect x='{x}' y='200' width='136' height='190' rx='20' fill='{PAPER}'/><circle cx='{cx}' cy='265' r='30' fill='{c}'/>"
        out += f"<text x='{cx}' y='345' text-anchor='middle' font-family='{SANS}' font-size='21' font-weight='700' fill='{INK}'>{esc(lab)}</text>"
        if i < len(labels) - 1:
            out += f"<polygon points='{x+142},288 {x+142},302 {x+160},295' fill='#B07A57'/>"
    return out


def doc(heading, lines):
    out = f"<rect x='980' y='110' width='300' height='380' rx='18' fill='{PAPER}'/><text x='1010' y='160' font-family='{SANS}' font-size='18' font-weight='700' fill='{MUT}' letter-spacing='3'>{esc(heading)}</text>"
    y = 200
    for t, c in lines:
        out += f"<rect x='1010' y='{y}' width='18' height='18' rx='4' fill='{c}'/><text x='1040' y='{y+15}' font-family='{SANS}' font-size='18' fill='{INK}'>{esc(t)}</text>"
        y += 48
    return out


def person(i, initial, company):
    col = [SAGE, ACC, GRAY, PURP][i % 4]
    return (f"<rect x='980' y='150' width='300' height='300' rx='18' fill='{PAPER}'/><circle cx='1130' cy='250' r='56' fill='{col}'/>"
            f"<text x='1130' y='268' text-anchor='middle' font-family='{SERIF}' font-size='48' font-weight='700' fill='{PAPER}'>{esc(initial)}</text>"
            f"<text x='1130' y='360' text-anchor='middle' font-family='{SANS}' font-size='20' font-weight='700' fill='{INK}'>{esc(company)}</text>"
            f"<rect x='1075' y='385' width='110' height='12' rx='6' fill='{LINE}'/>")


def ticket(kicker, amount, badge, col):
    out = f"<rect x='980' y='120' width='300' height='360' rx='18' fill='{PAPER}'/><text x='1010' y='170' font-family='{SANS}' font-size='18' font-weight='700' fill='{MUT}' letter-spacing='3'>{esc(kicker)}</text>"
    for j, w in enumerate((200, 160, 220)):
        out += f"<rect x='1010' y='{210+j*34}' width='{w}' height='12' rx='6' fill='{LINE}'/>"
    out += f"<text x='1010' y='370' font-family='{SERIF}' font-size='40' font-weight='700' fill='{INK}'>{esc(amount)}</text>"
    bw = tw(badge, 18) + 40
    out += f"<rect x='1010' y='410' width='{bw}' height='38' rx='19' fill='{col}'/><text x='1030' y='435' font-family='{SANS}' font-size='18' font-weight='700' fill='{PAPER}'>{esc(badge)}</text>"
    return out


# ================= PROPOSAL TRACKER =================
PT = 'PROPOSAL TRACKER'
C['3fb727ea08a481d5b3b3f4c6c41882cb'] = base(0, title_block(PT, ['Send it. Follow up.', 'Win it.'])
                                             + steps(786, ['Draft', 'Sent', 'Follow up', 'Won'], [GRAY, ACC, '#B07A57', SAGE]))
C['3fb727ea08a48138a039e5858b05b87a'] = base(1, title_block(PT, ['Start here'], [('5 minutes', SAGE), ('3 steps', ACC)])
                                             + doc('SET UP', [('Delete the examples', SAGE), ('Add your first client', SAGE), ('Add a proposal', SAGE), ('Follow up when told', ACC)]))
C['3fb727ea08a4818091d7d2f1bdc7bdac'] = base(2, title_block(PT, ['Pipeline'], [('Board', SAGE), ('Weighted value', ACC)])
                                             + board(820, 150, [('Draft', 1, GRAY), ('Sent', 3, BLUE), ('Talks', 1, ACC), ('Won', 1, SAGE), ('Lost', 1, RED)]))
C['3fb727ea08a481b5a62fd39ef6b48ecf'] = base(0, title_block(PT, ['Clients'], [('Win rate', SAGE), ('Won value', ACC)])
                                             + card(960, 120, 340, 360, 'CLIENT', [('Open value', '$2,800', ACC), ('Won value', '$900', SAGE), ('Win rate', '50%', SAGE)]))
C['3fb727ea08a481cabe39ce2fc20a486e'] = base(1, title_block(PT, ['Follow-up Emails'], [('6 emails', SAGE), ('Copy & send', ACC)], size=58)
                                             + card(960, 120, 340, 360, 'EMAIL', [('Quick check-in', '', INK), ('Add value', '', INK), ('Deadline', '', INK), ('Last check-in', '', INK)]))
C['3fb727ea08a4810fa6e0db2ab02dc003'] = base(2, title_block(PT, ['Writing Guide'], [('6 parts', SAGE), ('Copy-paste outline', ACC)])
                                             + doc('PROPOSAL', [('Their goal', SAGE), ('The plan', SAGE), ("What's included", SAGE), ('Price + timeline', ACC), ('Next step', ACC)]))
C['3fb727ea08a481e9afa0ff928acc88a4'] = base(0, title_block(PT, ['Weekly review'], [('10 minutes', SAGE), ('Why I lost', ACC)])
                                             + doc('FRIDAY', [('Follow-ups sent', SAGE), ('Expired quotes', SAGE), ('Lost reasons', ACC), ('One new proposal', SAGE)]))
C['3fb727ea08a4818fa871f9392d39e9ce'] = base(1, title_block(PT, ['Client inquiry form'], [('Share a link', SAGE), ('Leads land here', ACC)], size=54)
                                             + doc('NEW INQUIRY', [('Name', LINE), ('Email', LINE), ('Project', LINE), ('Budget', LINE)]))

PROPS = [  # page_id, name, value, status, color
    ('3fb727ea08a4811594f0f64f0b69a0c7', 'Monthly Social Retainer', '$1,500', 'Negotiating', ACC),
    ('3fb727ea08a48139881fc09be92858df', 'Email Sequence', '$1,100', 'Sent', BLUE),
    ('3fb727ea08a4813999bec4f316e1a850', 'Logo Refresh', '$750', 'Sent', BLUE),
    ('3fb727ea08a481599752d02fca37f0c2', 'SEO Audit', '$600', 'Lost', RED),
    ('3fb727ea08a4815ba4b9e04e6e02973f', 'Brand Photo Shoot', '$1,200', 'Draft', GRAY),
    ('3fb727ea08a48194976ceec8e9011a4d', 'Newsletter Setup', '$900', 'Won', SAGE),
    ('3fb727ea08a481af9f45e15026c2ced0', 'Website Refresh', '$2,800', 'Sent', BLUE),
]
for i, (pid, name, val, st, col) in enumerate(PROPS):
    lines = [name] if len(name) <= 18 else name.rsplit(' ', 1)
    C[pid] = base(i, title_block('PROPOSAL', lines, [(val, INK), (st, col)], size=56) + ticket('QUOTE', val, st, col))

CLIENTS = [
    ('3fb727ea08a481c59695d860005cfa23', 'Priya Shah', 'Lumen Health'),
    ('3fb727ea08a481cfb2f5e8fe2624422d', 'Tom Becker', 'Becker & Co'),
    ('3fb727ea08a481f1a9dfe15d60c88529', 'Jordan Blake', 'Northline Fitness'),
    ('3fb727ea08a481f69b2cfda9a5517494', 'Maya Chen', 'Bloom Bakery'),
]
for i, (pid, name, comp) in enumerate(CLIENTS):
    C[pid] = base(i + 1, title_block('CLIENT', [name], [(comp, INK)], size=58) + person(i, name[0], comp))

# ================= BRAND DEAL TRACKER =================
BD = 'BRAND DEAL TRACKER'
C['3fb727ea08a48136a0daddc0a9549d06'] = base(0, title_block(BD, ['Pitch. Post.', 'Get paid.'])
                                             + steps(786, ['Pitched', 'Signed', 'Posted', 'Paid'], [GRAY, ACC, '#B07A57', SAGE]))
C['3fb727ea08a48142a553f039d67e4940'] = base(1, title_block(BD, ['Start here'], [('5 minutes', SAGE), ('3 steps', ACC)])
                                             + doc('SET UP', [('Delete the examples', SAGE), ('Add a brand', SAGE), ('Add a deal + posts', SAGE), ('Do what it says', ACC)]))
C['3fb727ea08a4818287bcf43df2783d1c'] = base(2, title_block(BD, ['Deals'], [('Board', SAGE), ('Money', ACC)])
                                             + board(820, 150, [('Pitch', 1, GRAY), ('Talk', 1, '#E2C36B'), ('Signed', 1, BLUE), ('Done', 1, PURP), ('Paid', 1, SAGE)]))
C['3fb727ea08a481e2bf0de2947d83bc53'] = base(0, title_block(BD, ['Posts you owe'], [('By due date', SAGE), ('Late first', ACC)])
                                             + card(960, 120, 340, 380, 'DUE', [('Before / after TikTok', 'Late', ACC), ('Story with link', '6 days', INK), ('Serum Reel', 'Posted', SAGE), ('Recipe video 3', 'Posted', SAGE)]))
C['3fb727ea08a48100bddbc11e2cad0b68'] = base(1, title_block(BD, ['Brands'], [('Earned', SAGE), ('Pending', ACC)])
                                             + card(960, 120, 340, 360, 'BRAND', [('Earned', '$600', SAGE), ('Pending', '$900', ACC), ('Deals', '2', INK)]))
C['3fb727ea08a48168b64cf62e2589d2bd'] = base(2, title_block(BD, ['Brand Email Scripts'], [('6 emails', SAGE), ('Copy & send', ACC)], size=54)
                                             + card(960, 120, 340, 360, 'EMAIL', [('First pitch', '', INK), ('Follow up', '', INK), ('Send my rates', '', INK), ('Payment reminder', '', INK)]))
C['3fb727ea08a481818b19e8af21437a5b'] = base(0, title_block(BD, ['Rate card'], [('Your prices', SAGE), ('Usage rights', ACC)])
                                             + card(960, 120, 340, 360, 'RATES', [('1 TikTok', '$ ___', INK), ('1 Reel', '$ ___', INK), ('Story set', '$ ___', INK), ('Usage, 30 days', '+ ___', ACC)]))
C['3fb727ea08a4813eb795fc54eb24d6ff'] = base(1, title_block(BD, ['Media kit'], [('Fill + publish', SAGE), ('Send to brands', ACC)])
                                             + person(2, 'You', 'Your niche').replace("font-size='48'", "font-size='36'"))
C['3fb727ea08a48185a016ed1b3aba294a'] = base(2, title_block(BD, ['Weekly review'], [('10 minutes', SAGE), ('Chase money', ACC)])
                                             + doc('FRIDAY', [('Posts due this week', SAGE), ('Late payments', ACC), ('New pitches sent', SAGE), ('Links added', SAGE)]))

DEALS = [
    ('3fb727ea08a48103b0deee1f20c48f18', 'Desk setup video', '$700', 'Pitched', GRAY),
    ('3fb727ea08a481439664d82d63328624', '3-video recipe series', '$900', 'Delivered', PURP),
    ('3fb727ea08a481668f24ddcaf321b0c9', 'Holiday gift guide', '$800', 'Talking', '#C9A64A'),
    ('3fb727ea08a4816b9c1bd779b0d2b0da', 'Gym bag review', '$600', 'Paid', SAGE),
    ('3fb727ea08a481b08362c94c317c062b', 'Newsletter mention', '$250', 'Lost', RED),
    ('3fb727ea08a481cda39bcc5bdf518160', 'Fall serum launch', '$1,200', 'Signed', BLUE),
]
for i, (pid, name, fee, st, col) in enumerate(DEALS):
    lines = [name] if len(name) <= 18 else name.rsplit(' ', 1)
    C[pid] = base(i, title_block('BRAND DEAL', lines, [(fee, INK), (st, col)], size=56) + ticket('DEAL', fee, st, col))

POSTS = [
    ('3fb727ea08a481278785ec91d2d00ad8', 'Recipe video 2', 'TikTok', 'Posted', SAGE),
    ('3fb727ea08a4818e9a18e4f0f20f52de', 'Before / after TikTok', 'TikTok', 'To post', ACC),
    ('3fb727ea08a4819aa940f9555515dd75', 'Recipe video 3', 'YouTube', 'Posted', SAGE),
    ('3fb727ea08a4819cb737d016dcdcc5db', 'Serum routine Reel', 'Instagram', 'Posted', SAGE),
    ('3fb727ea08a481a4a180c76ffdad9332', 'Story with link', 'Instagram', 'To post', ACC),
    ('3fb727ea08a481cc9d1dc7563c2dc40a', 'Gym bag review video', 'YouTube', 'Posted', SAGE),
    ('3fb727ea08a481f88c9afd9774f3171b', 'Recipe video 1', 'TikTok', 'Posted', SAGE),
]
for i, (pid, name, plat, st, col) in enumerate(POSTS):
    lines = [name] if len(name) <= 18 else name.rsplit(' ', 1)
    inner = title_block('POST', lines, [(plat, INK), (st, col)], size=56)
    inner += (f"<rect x='1000' y='110' width='230' height='380' rx='26' fill='{INK}'/><rect x='1014' y='124' width='202' height='352' rx='16' fill='{PAPER}'/>"
              f"<rect x='1034' y='150' width='162' height='190' rx='10' fill='{[SAGEL, CLAY, CREAM][i % 3]}'/><polygon points='1100,215 1100,275 1145,245' fill='{col}'/>"
              f"<rect x='1034' y='362' width='140' height='10' rx='5' fill='{LINE}'/><rect x='1034' y='386' width='100' height='10' rx='5' fill='{LINE}'/><rect x='1034' y='420' width='70' height='26' rx='13' fill='{col}'/>")
    C[pid] = base(i, inner)

BRANDS = [
    ('3fb727ea08a4810da548f82cc57715d8', 'Lumi Desk', 'Tech'),
    ('3fb727ea08a481468300e2f36e199a75', 'FreshBox Meals', 'Food'),
    ('3fb727ea08a48149b432e187dff027ba', 'Glow Skin Co', 'Beauty'),
    ('3fb727ea08a481e8b5d6d39e0464f6a3', 'PeakFit Gear', 'Fitness'),
]
for i, (pid, name, niche) in enumerate(BRANDS):
    C[pid] = base(i + 1, title_block('BRAND', [name], [(niche, INK)], size=58) + person(i, name[0], niche))

out = {}
pdir = os.path.join(HERE, 'png', 'mini')
os.makedirs(pdir, exist_ok=True)
for k, svg in C.items():
    out[k] = 'data:image/svg+xml,' + urllib.parse.quote(svg, safe="=/:,'() ")
    open(os.path.join(pdir, k + '.svg'), 'w').write(svg)
json.dump(out, open(os.path.join(HERE, 'mini_covers.json'), 'w'))
print(len(out), max(len(v) for v in out.values()))
