"""SystemForge Etsy listing images (v3): 7 images per product, 2700x2025 PNG.

1 main (lifestyle scene + real screens + title + 4 features), 4 feature images (one big readable crop each),
1 What's inside, 1 How it works (Etsy delivery).
Writes canva/v3/etsy/<p>/*.png and canva/v3/etsy/listing-<p>.html (Canva import, editable text).
Usage: python3 generator/v3/build_listing.py [products...]
"""
import json, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pins as B

HERE, ROOT = B.HERE, B.ROOT
OUT = os.path.join(ROOT, 'canva', 'v3', 'etsy')
os.makedirs(OUT, exist_ok=True)
W, H = 1350, 1013
B.CROPS['deal-lap'] = ('deal-do-now-board', (145, 140, 1870, 1160))
B.CROPS['prop-lap'] = ('prop-followup-pipeline', (145, 150, 1990, 1250))
B.COMPOSITE['c-prop-win'] = ('prop-proposals-table', [(295, 700)], [(145, 420), (1205, 1360), (1360, 1565)])

SER = "font-family:'Source Serif 4',Georgia,serif;font-weight:700"
INK, MUT, PAP = '#2E2A25', '#5C554C', '#FFFDF9'

P = {
 'ccs': dict(name='Content Creator Studio', kicker='NOTION TEMPLATE FOR CONTENT CREATORS', color='#E9EEE4', accent='#7A8B6F',
   scene='s-land.png', screens=['ccs-lap', 'ph-ccs-pipeline-posted.jpg'],
   sub='Plan, post and get paid,<br>for every platform.',
   features=['Content calendar &amp; pipeline', 'Weekly goal per platform', 'Brand deal tracker', 'Hooks, scripts &amp; weekly review'],
   cards=[('Every post on a calendar', 'Drag a card to move it to another day. Every platform in one view.', 'c-ccs-cal'),
          ('A weekly goal for each platform', 'See how many posts are left this week on TikTok, Instagram, YouTube and more.', 'c-ccs-ch2'),
          ('See which posts work', 'Add views and likes. Engagement % is calculated for you.', 'c-ccs-top'),
          ('Brand deals, pitch to paid', 'Fee, posts still owed, due dates and days late on every deal.', 'c-ccs-deal')],
   inside=['Content pipeline: Idea to Posted', 'Board, calendar and gallery views', 'Channels with a weekly goal (11 platforms)',
           'Post results with engagement %', 'Content pillars', 'Brand deal tracker', 'Brand deal email scripts',
           'Hook library + 30 content ideas', 'Weekly review page', 'Example data + Start here guide']),
 'wcp': dict(name='Weekly Content Planner', kicker='NOTION CONTENT CALENDAR', color='#E3E8DC', accent='#7A8B6F',
   scene='w-wcp.png', screens=['ph-wcp-pipeline.jpg', 'ph-wcp-goals-next7.jpg'],
   sub='Plan your week of content<br>in 15 minutes.',
   features=['Content calendar', 'Weekly goal per platform', 'Pipeline: Idea to Posted', '30 ideas + hook starters'],
   cards=[('Weekly goals that fill up', 'Set a goal for each platform. The bar fills up as you post.', 'c-wcp-goals'),
          ('Your next 7 days', 'See what is due today, tomorrow and this week.', 'c-wcp-next7'),
          ('Drag cards to Posted', 'Every idea moves from Idea to Draft, Create, Edit and Posted.', 'c-wcp-col'),
          ('A content calendar', 'Every post on its publish date. Drag to move it.', 'c-wcp-cal')],
   inside=['Content list: channel, format, hook, date', 'Pipeline board', 'Date check: today, tomorrow, missed',
           'Channels with a weekly goal', 'Calendar, Idea bank, Next 7 days views', 'Content pillars',
           'Hook Starters', '30 content ideas + repurpose map', '15-minute Sunday plan', 'Example data + Start here']),
 'fco': dict(name='Freelancer Client OS', kicker='NOTION TEMPLATE FOR FREELANCERS', color='#F1E3D6', accent='#C98B6B',
   scene='w-fco.png', screens=['ph-fco-invoices-board.jpg'], dark=True,
   sub='Clients, projects and invoices<br>in one calm place.',
   features=['Clients &amp; proposals', 'Projects with health', 'Invoices: days late', '8 ready client emails'],
   cards=[('Every project, on track or not', 'Health and progress bar on every project.', 'c-fco-projects'),
          ('Late invoices flag themselves', 'See what is late and what to send next.', 'c-fco-unpaid'),
          ('Your money flow', 'Draft, sent and paid invoices on one board.', 'c-fco-paid'),
          ('A 10-minute weekly review', 'Follow up, chase, check projects, send invoices.', 'c-fco-review')],
   inside=['Clients with follow-up dates', 'Proposals with win chance', 'Projects with health + progress',
           'Tasks: overdue, today, this week', 'Invoices with days late', 'Expenses, profit + real hourly rate',
           '8 ready-to-send client emails', 'Client onboarding checklist', 'Weekly review', 'Example data + Start here']),
 'fit': dict(name='Freelance Invoice Tracker', kicker='NOTION INVOICE TRACKER', color='#EFE6DA', accent='#B07A57',
   scene='w-fit.png', screens=['ph-fit-clients-invoices.jpg'],
   sub='Know who owes you,<br>and when to follow up.',
   features=['Chase these first', 'Who owes you', 'Next step on every invoice', 'Reminder emails'],
   cards=[('Chase these first', 'Late invoices, with the next step to take.', 'c-fit-chase'),
          ('Who owes you', 'What each client owes you, and if they pay on time.', 'c-fit-owes'),
          ('Send the right email', 'Friendly, second and final reminders, ready to copy.', 'c-fit-emails'),
          ('Every invoice in one list', 'Status, due date and how late it is.', 'c-fit-all')],
   inside=['Invoices: amount, client, due date, status', 'Late? On track or late X days', 'Next step on every invoice',
           'Due in: days before it is due', 'Clients: owes you + lifetime paid', 'Chase these first view',
           'Reminder emails', 'Get Paid Faster kit', '2-minute daily check', 'Example data + Start here']),
 'prop': dict(name='Proposal Tracker', kicker='NOTION TEMPLATE FOR FREELANCERS', color='#E4E9E0', accent='#2F4A3A',
   scene='w-prop.png', screens=['prop-lap'], dark=True,
   sub='Follow up on every quote<br>you send.',
   features=['Follow up today', 'Next step on every quote', 'Expiry warning', 'Price check'],
   cards=[('Follow up today', 'The quotes that need you now, with the next step.', 'c-prop-follow'),
          ('Your sent quotes', 'Pipeline: Draft, Sent, Negotiating, Won, Lost.', 'c-prop-sent'),
          ('Price check', 'Hours x your rate tells you if you priced too low.', 'prop-price'),
          ('Win chance + weighted value', 'What your open quotes are really worth.', 'c-prop-win')],
   inside=['Follow up today page', 'Next step: Send, Follow up #1-3, new quote', 'Days since sent + expiry warning',
           'Pipeline board', 'Win chance + weighted value', 'Price check', 'Clients: open value + win rate',
           '6 follow-up emails', 'Proposal writing guide', 'Weekly review + client inquiry form']),
 'deal': dict(name='Brand Deal Tracker', kicker='NOTION TEMPLATE FOR CREATORS', color='#F3E1DD', accent='#B9776E',
   scene='w-deal.png', screens=['deal-lap'],
   sub='Every deal, from first pitch<br>to paid.',
   features=['Do this now', 'Deal board: pitch to paid', 'Posts you owe', 'Rate card + media kit'],
   cards=[('Do this now', 'Everything that needs you today, with the next step.', 'c-deal-now'),
          ('A deal board', 'Pitched, talking, signed, delivered, paid.', 'c-deal-col'),
          ('Posts you owe', 'Every deliverable with its due date. Tick Posted when it is live.', 'c-deal-owe-all'),
          ('Your rate card', 'Write your prices once, copy them into every pitch.', 'deal-rate')],
   inside=['Do this now page', 'Next step on every deal', 'Deal board: pitched to paid', 'Posts you owe + days late',
           'Money: due in, late or paid', 'Brands: earned + pending', '6 brand email scripts',
           'Rate card page', 'Media kit page', 'Weekly review + Start here']),
}


def screens_of(scene_file, n):
    im = np.array(Image.open(os.path.join(HERE, scene_file)).convert('RGB')).astype(int)
    from scipy import ndimage
    white = (im.min(axis=2) > 232) & ((im.max(axis=2) - im.min(axis=2)) < 16)
    lab, _ = ndimage.label(white)
    sizes = ndimage.sum(white, lab, range(1, lab.max() + 1))
    out = []
    for i in np.argsort(sizes)[::-1][:n]:
        m = ndimage.binary_fill_holes(lab == i + 1); ys, xs = np.nonzero(m); s = xs + ys; d = xs - ys
        out.append([(xs[s.argmin()], ys[s.argmin()]), (xs[d.argmax()], ys[d.argmax()]),
                    (xs[s.argmax()], ys[s.argmax()]), (xs[d.argmin()], ys[d.argmin()])])
    return sorted(out, key=lambda q: q[0][0])


def main_bg(p, out):
    sc = Image.open(os.path.join(HERE, p['scene'])).convert('RGB'); w0, h0 = sc.size
    k = (H * 2) / h0; Wb = int(w0 * k); ox = max(0, Wb - W * 2)
    bg = sc.resize((Wb, H * 2), Image.LANCZOS).crop((ox, 0, ox + W * 2, H * 2)).convert('RGBA')
    for q, s in zip(screens_of(p['scene'], len(p['screens'])), p['screens']):
        S = 2; qq = [((x * k - ox) * S, y * k * S) for x, y in q]
        cx = sum(a for a, _ in qq) / 4; cy = sum(b for _, b in qq) / 4
        qq = [(cx + (x - cx) * 1.03, cy + (y - cy) * 1.025) for x, y in qq]
        c = Image.open(B.src(s)).convert('RGB')
        if s.startswith('ph-'):
            c = c.crop((0, int(c.height * 0.0), c.width, c.height))
        sw = ((qq[1][0] - qq[0][0]) ** 2 + (qq[1][1] - qq[0][1]) ** 2) ** .5
        sh = ((qq[3][0] - qq[0][0]) ** 2 + (qq[3][1] - qq[0][1]) ** 2) ** .5
        ar = sw / sh; cw, ch = c.size
        c = c.crop((0, 0, int(ch * ar), ch)) if cw / ch > ar else c.crop((0, 0, cw, int(cw / ar)))
        cw, ch = c.size
        warped = c.convert('RGBA').transform((W * 2 * S, H * 2 * S), Image.PERSPECTIVE,
                                             B._coeffs(qq, [(0, 0), (cw, 0), (cw, ch), (0, ch)]), Image.BICUBIC)
        m = Image.new('L', (W * 2 * S, H * 2 * S), 0); ImageDraw.Draw(m).polygon(qq, fill=255)
        layer = Image.new('RGBA', (W * 2 * S, H * 2 * S), (0, 0, 0, 0)); layer.paste(warped, (0, 0), m)
        bg.alpha_composite(layer.resize((W * 2, H * 2), Image.LANCZOS))
    # soft panel behind the text on the left
    arr = np.zeros((H * 2, W * 2, 4), np.uint8)
    base = (40, 28, 20) if p.get('dark') else (246, 241, 233)
    arr[..., :3] = base
    for x in range(W * 2):
        t = x / (W * 2); a = 0.97 if t < 0.46 else max(0.0, 0.97 * (1 - (t - 0.46) / 0.06))
        arr[:, x, 3] = int(255 * a * (0.78 if p.get('dark') else 1))
    bg.alpha_composite(Image.fromarray(arr))
    bg.convert('RGB').save(out, quality=92)


def T(l, t, w, txt, size, extra=''):
    wd = f'width:{w}px;' if w else ''
    return f'<p style="position:absolute;left:{l}px;top:{t}px;{wd}margin:0;font-size:{size}px;{extra}">{txt}</p>'


def page(label, inner, bg_url=None, color='#F6F1E9'):
    b = f'<img src="{bg_url}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px">' if bg_url else ''
    return (f'<div data-document-role="page" data-label="{label}" style="position:relative;width:{W}px;height:{H}px;'
            f'overflow:hidden;background:{color}">{b}{inner}</div>')


def blobs(accent):
    return (f'<div style="position:absolute;left:-180px;top:-200px;width:520px;height:520px;border-radius:50%;background:{accent};opacity:.12"></div>'
            f'<div style="position:absolute;right:-220px;bottom:-260px;width:640px;height:640px;border-radius:50%;background:{accent};opacity:.10"></div>')


def build(pk, base_url):
    p = P[pk]; pages = []
    d = p.get('dark'); fg = PAP if d else INK; sub = '#F1E7DC' if d else MUT
    # 1. main
    main = f'{pk}-1-main.jpg'; main_bg(p, os.path.join(OUT, pk, main))
    # everything inside the centre square (x 169-1181) so the Etsy square thumbnail keeps it all
    X = 205
    inner = (T(X, 95, 560, p['kicker'], 17, f'font-weight:700;letter-spacing:3px;color:{"#E8D6C3" if d else "#7A6A58"}')
             + T(X, 135, 470, p['name'].replace(' ', '<br>', 1), 56 if len(p['name']) > 18 else 64, f'line-height:1.02;white-space:nowrap;color:{fg};{SER}')
             + T(X, 300, 430, p['sub'], 25, f'line-height:1.3;color:{sub}'))
    for i, f in enumerate(p['features']):
        inner += (f'<p style="position:absolute;left:{X}px;top:{420 + i * 62}px;width:34px;margin:0;padding:3px 0;text-align:center;border-radius:999px;'
                  f'background:{p["accent"]};color:{PAP};font-size:19px;font-weight:700">✓</p>' + T(X + 48, 420 + i * 62, 380, f, 24, f'font-weight:500;color:{fg}'))
    t0, _, c0 = p['cards'][0]
    CW = 480
    url0, ih0 = B.fit(c0, CW, 230, 'm1'); url0 = url0.replace(B.RAW + 'crops/', base_url + 'crops/')
    inner += (f'<div style="position:absolute;left:{1160 - CW}px;top:{H - ih0 - 140}px;width:{CW}px;height:{ih0 + 56}px;background:#FFFFFF;border-radius:18px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.12)">'
              + T(18, 12, CW - 30, t0, 21, f'font-weight:700;color:{INK}')
              + f'<img src="{url0}" style="position:absolute;left:0;top:50px;width:{CW}px;height:{ih0}px"></div>')
    inner += T(X, 860, 0, 'INSTANT DOWNLOAD', 19, f'padding:13px 26px;border-radius:999px;background:{PAP if d else INK};color:{INK if d else PAP};font-weight:700;letter-spacing:2px')
    pages.append(page(f'{pk}-1-main', inner, f'{base_url}{pk}/{main}'))
    # 2-5. features
    for i, (title, desc, crop) in enumerate(p['cards'], 2):
        im0 = Image.open(B.src(crop)); a = im0.width / im0.height
        cw = max(420, min(740, int(840 * a)))
        url, ih = B.fit(crop, cw, 840, f'e{i}')
        url = url.replace(B.RAW + 'crops/', base_url + 'crops/')
        top = max(60, (H - ih - 30) // 2)
        inner = (blobs(p['accent'])
                 + f'<p style="position:absolute;left:70px;top:150px;width:64px;margin:0;padding:12px 0;text-align:center;border-radius:999px;background:{p["accent"]};color:{PAP};font-size:30px;font-weight:700">{i - 1}</p>'
                 + T(70, 250, 470, title, 60, f'line-height:1.05;color:{INK};{SER}')
                 + T(70, 520, 450, desc, 28, f'line-height:1.4;color:{MUT}')
                 + T(70, 900, 450, p['name'], 22, f'font-weight:700;letter-spacing:1px;color:{p["accent"]}')
                 + f'<div style="position:absolute;left:{560 + (740 - cw) // 2}px;top:{top}px;width:{cw}px;height:{ih + 30}px;background:#FFFFFF;border-radius:22px;overflow:hidden">'
                 + f'<img src="{url}" style="position:absolute;left:0;top:15px;width:{cw}px;height:{ih}px"></div>')
        pages.append(page(f'{pk}-{i}-feature', inner, None, p['color']))
    # 6. what's inside
    items = ''
    for j, it in enumerate(p['inside']):
        col, row = j % 2, j // 2
        items += (f'<p style="position:absolute;left:{110 + col * 590}px;top:{300 + row * 115}px;width:34px;margin:0;padding:3px 0;text-align:center;'
                  f'border-radius:999px;background:{p["accent"]};color:{PAP};font-size:20px;font-weight:700">✓</p>'
                  + T(162 + col * 590, 298 + row * 115, 500, it, 28, f'font-weight:500;line-height:1.25;color:{INK}'))
    inner = (blobs(p['accent']) + T(0, 90, W, "What's inside", 76, f'text-align:center;color:{INK};{SER}')
             + T(0, 195, W, p['name'] + ' · Notion template', 28, f'text-align:center;color:{MUT}')
             + f'<div style="position:absolute;left:70px;top:260px;width:1210px;height:640px;background:#FFFFFF;border-radius:28px"></div>' + items)
    pages.append(page(f'{pk}-6-inside', inner, None, p['color']))
    # 7. how it works (Etsy delivery)
    steps = [('Download', 'After you buy, download the PDF from your Etsy purchases.'),
             ('Duplicate', 'Open the link in the PDF and click Duplicate to add the template to your Notion.'),
             ('Start', 'Open the Start here page. Example data shows how it works. Delete it when ready.')]
    inner = blobs(p['accent']) + T(0, 90, W, 'How it works', 76, f'text-align:center;color:{INK};{SER}')
    for j, (a, b) in enumerate(steps):
        x = 70 + j * 410
        inner += (f'<div style="position:absolute;left:{x}px;top:260px;width:380px;height:520px;background:#FFFFFF;border-radius:26px"></div>'
                  f'<p style="position:absolute;left:{x + 150}px;top:310px;width:80px;margin:0;padding:16px 0;text-align:center;border-radius:999px;background:{p["accent"]};color:{PAP};font-size:38px;font-weight:700">{j + 1}</p>'
                  + T(x, 440, 380, a, 44, f'text-align:center;color:{INK};{SER}')
                  + T(x + 40, 530, 300, b, 26, f'text-align:center;line-height:1.4;color:{MUT}'))
    inner += T(0, 850, W, 'Digital download · Works on desktop, tablet and phone · No physical item', 24, f'text-align:center;font-weight:500;color:{MUT}')
    pages.append(page(f'{pk}-7-how', inner, None, p['color']))
    return pages


HEAD = ('<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700'
        '&family=Source+Serif+4:wght@700&display=swap" rel="stylesheet"><style>body{margin:0}div,span,p{font-family:Inter,Arial,sans-serif}</style></head><body>')
FONTS = ("<style>@font-face{font-family:'Source Serif 4';font-weight:700;src:url(file://%s/sourceserif700.woff2)}"
         "@font-face{font-family:Inter;font-weight:500;src:url(file://%s/inter500.woff2)}@font-face{font-family:Inter;font-weight:700;src:url(file://%s/inter700.woff2)}</style>")


def render_png(page_html, out):
    F = os.path.join(ROOT, 'generator', 'remotion', 'public')
    h = os.path.join(OUT, '_p.html')
    open(h, 'w').write(HEAD.replace('</head>', FONTS % (F, F, F) + '</head>') + page_html + '</body></html>')
    shot = h + '.png'
    subprocess.run([B.CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=2', f'--window-size={W},{H + 200}', f'--screenshot={shot}', 'file://' + h], check=True, capture_output=True)
    Image.open(shot).crop((0, 0, W * 2, H * 2)).convert('RGB').save(out, optimize=True)
    os.remove(h); os.remove(shot)


if __name__ == '__main__':
    prods = sys.argv[1:] or list(P)
    for pk in prods:
        os.makedirs(os.path.join(OUT, pk), exist_ok=True); os.makedirs(os.path.join(OUT, 'final', pk), exist_ok=True)
        local = build(pk, 'file://' + os.path.join(ROOT, 'canva', 'v3') + '/LOCALMARK/')
        for pg in local:
            pg2 = pg.replace('/LOCALMARK/crops/', '/crops/').replace('/LOCALMARK/', '/etsy/')
            lab = re.search(r'data-label="([^"]+)"', pg2).group(1)
            render_png(pg2, os.path.join(OUT, 'final', pk, lab + '.png'))
        remote = build(pk, '__RAW__')
        html = HEAD + '\n'.join(pg.replace('__RAW__crops/', '__RAW__crops/').replace('__RAW__' + pk + '/', '__RAW__etsy/' + pk + '/') for pg in remote) + '</body></html>'
        open(os.path.join(OUT, f'listing-{pk}.html'), 'w').write(html)
        print('ok', pk)
