"""Notion page covers (3000x1200) in the v3 home-cover style:
same product scene as the home cover + the page's own real HD screenshot on the screen + page title.
Usage: python3 generator/v3/build_covers.py [cover_id ...]   (ids from COVERS below)
Writes covers/v3/sub/<id>.jpg
"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pins as B
from build_listing import screens_of

HERE, ROOT = B.HERE, B.ROOT
OUT = os.path.join(ROOT, 'covers', 'v3', 'sub')
os.makedirs(OUT, exist_ok=True)
CW, CH = 3000, 1200          # final size
FONTS = os.path.join(ROOT, 'generator', 'remotion', 'public')

# product -> scene, panel tone (dark scenes get light text)
PROD = {
    'fco':  dict(scene='w-fco.png',  dark=True,  kicker='FREELANCER CLIENT OS'),
    'fit':  dict(scene='w-fit.png',  dark=False, kicker='FREELANCE INVOICE TRACKER'),
    'wcp':  dict(scene='w-wcp.png',  dark=False, kicker='WEEKLY CONTENT PLANNER'),
    'ccs':  dict(scene='s-land.png', dark=False, kicker='CONTENT CREATOR STUDIO'),
    'prop': dict(scene='w-prop.png', dark=True,  kicker='PROPOSAL TRACKER'),
    'deal': dict(scene='w-deal.png', dark=False, kicker='BRAND DEAL TRACKER'),
}

# cover id -> (product, title, subtitle, screens [one per blank screen in the scene, left to right])
B.CROPS.update({
    'cv-fco-paid':   ('fco-money-flow', (548, 250, 935, 950)),
    'cv-fco-menu':   ('fco-home-menu', (147, 587, 533, 1067)),
    'cv-fco-proj':   ('fco-projects-invoices', (145, 250, 800, 1250)),
    'cv-fco-week':   ('fco-money-flow', (145, 250, 700, 1250)),
    'cv-fco-review': ('fco-home-menu', (640, 540, 1300, 1250)),
    'cv-ccs-cal':    ('ccs-calendar', (145, 330, 1855, 1250)),
    'cv-ccs-home':   ('ccs-home-full', (78, 350, 930, 900)),
    'cv-ccs-deals':  ('ccs-calendar-deals', (163, 780, 1300, 1250)),
    'cv-ccs-top':    ('ccs-top-posts', (163, 380, 1500, 1200)),
    'cv-fit-inv':    ('fit-chase-owes', (145, 190, 1010, 1250)),
    'cv-fit-cli':    ('fit-chase-owes', (145, 560, 1010, 1250)),
    'cv-fit-mail':   ('fit-reminder-emails', (380, 330, 1300, 1250)),
    'cv-prop-top':   ('prop-followup-pipeline', (145, 150, 1700, 1150)),
    'cv-prop-pipe':  ('prop-pipeline', (145, 150, 1900, 1100)),
    'cv-prop-table': ('prop-proposals-table', (145, 150, 1700, 1100)),
    'cv-deal-now':   ('deal-do-now-board', (145, 150, 1700, 1100)),
    'cv-deal-board': ('deal-do-now-board', (145, 800, 1700, 1250)),
    'cv-deal-owe':   ('deal-posts-owe', (145, 250, 1700, 1250)),
    'cv-deal-rate':  ('deal-rate-card', (420, 150, 1500, 1100)),
})
PH_CCS = 'ph-ccs-pipeline-posted.jpg'
PH_W1, PH_W2 = 'ph-wcp-pipeline.jpg', 'ph-wcp-goals-next7.jpg'

# cover id -> (product, title, subtitle, screens [one per blank screen in the scene, left to right])
COVERS = {
    # Freelancer Client OS (phone)
    'fco-clients':    ('fco', 'Clients', 'Every client, where they came from and when to follow up.', ['cv-fco-menu']),
    'fco-proposals':  ('fco', 'Proposals', 'Value, win chance and expiry date on every quote.', ['cv-fco-review']),
    'fco-projects':   ('fco', 'Projects', 'Deadline, progress and health on every project.', ['cv-fco-proj']),
    'fco-tasks':      ('fco', 'Tasks', 'See what is overdue and what is due this week.', ['cv-fco-week']),
    'fco-invoices':   ('fco', 'Invoices', 'Draft, sent, paid. Late ones count the days.', ['cv-fco-paid']),
    'fco-expenses':   ('fco', 'Expenses', 'Linked to projects, so you see your real profit.', ['cv-fco-proj']),
    'fco-emails':     ('fco', 'Email Scripts', '8 client emails, ready to copy and send.', ['cv-fco-menu']),
    'fco-onboarding': ('fco', 'Client Onboarding', 'A calm checklist for every new client.', ['cv-fco-review']),
    # Freelance Invoice Tracker (tablet)
    'fit-invoices':   ('fit', 'Invoices', 'Every invoice, how late it is and the next step.', ['cv-fit-inv']),
    'fit-clients':    ('fit', 'Clients', 'What each client owes you, and if they pay on time.', ['cv-fit-cli']),
    'fit-emails':     ('fit', 'Reminder Emails', 'Friendly, second and final reminders, ready to send.', ['cv-fit-mail']),
    'fit-kit':        ('fit', 'Get Paid Faster Kit', 'Simple habits so clients pay on time.', ['cv-fit-inv']),
    # Weekly Content Planner (two phones)
    'wcp-content':    ('wcp', 'Content', 'Every idea from Idea to Posted.', [PH_W1, PH_W2]),
    'wcp-channels':   ('wcp', 'Channels', 'A weekly goal for every platform.', [PH_W2, PH_W1]),
    'wcp-hooks':      ('wcp', 'Hook Starters', 'Write the first line first.', [PH_W1, PH_W2]),
    'wcp-ideas':      ('wcp', '30 Content Ideas', 'Plus a map to repurpose every post.', [PH_W2, PH_W1]),
    # Content Creator Studio (laptop + phone)
    'ccs-content':    ('ccs', 'Content', 'Every post from idea to posted, on one calendar.', ['cv-ccs-cal', PH_CCS]),
    'ccs-pillars':    ('ccs', 'Content Pillars', 'See which topic brings the most reach.', ['cv-ccs-top', PH_CCS]),
    'ccs-channels':   ('ccs', 'Channels', 'Every platform with its own weekly goal.', ['cv-ccs-home', PH_CCS]),
    'ccs-deals':      ('ccs', 'Brand Deals', 'From pitch to paid, with the posts you still owe.', ['cv-ccs-deals', PH_CCS]),
    'ccs-scripts':    ('ccs', 'Brand Deal Scripts', 'Emails for pitching, following up and getting paid.', ['cv-ccs-deals', PH_CCS]),
    'ccs-hooks':      ('ccs', 'Hook Library', 'Strong first lines for every type of post.', ['cv-ccs-home', PH_CCS]),
    'ccs-review':     ('ccs', 'Weekly Review', 'What worked this week, and what to post next.', ['cv-ccs-top', PH_CCS]),
    'ccs-ideas':      ('ccs', '30 Content Ideas', 'Plus a map to repurpose every post.', ['cv-ccs-cal', PH_CCS]),
    # Proposal Tracker (laptop)
    'prop-start':     ('prop', 'Start here', 'Set it up in a few minutes.', ['cv-prop-top']),
    'prop-pipeline':  ('prop', 'Pipeline', 'Draft, sent, negotiating, won or lost.', ['cv-prop-pipe']),
    'prop-clients':   ('prop', 'Clients', 'Open value, won value and win rate per client.', ['cv-prop-table']),
    'prop-proposals': ('prop', 'Proposals', 'Every quote with its next step.', ['cv-prop-table']),
    'prop-emails':    ('prop', 'Follow-up Emails', 'Ready messages for every follow-up.', ['cv-prop-top']),
    'prop-guide':     ('prop', 'Proposal Writing Guide', 'Write quotes that clients say yes to.', ['cv-prop-table']),
    'prop-review':    ('prop', 'Weekly Review', 'Five minutes to keep every quote moving.', ['cv-prop-pipe']),
    'prop-form':      ('prop', 'Client Inquiry Form', 'New leads land in your tracker.', ['cv-prop-top']),
    # Brand Deal Tracker (laptop)
    'deal-start':     ('deal', 'Start here', 'Set it up in a few minutes.', ['cv-deal-now']),
    'deal-deals':     ('deal', 'Deals', 'Pitched, talking, signed, delivered, paid.', ['cv-deal-board']),
    'deal-owe':       ('deal', 'Posts you owe', 'Every deliverable with its due date.', ['cv-deal-owe']),
    'deal-brands':    ('deal', 'Brands', 'What each brand paid you, and what is pending.', ['cv-deal-now']),
    'deal-emails':    ('deal', 'Brand Email Scripts', 'Pitch, follow up and get paid.', ['cv-deal-now']),
    'deal-rate':      ('deal', 'Rate Card', 'Write your prices once. Paste them into every pitch.', ['cv-deal-rate']),
    'deal-media':     ('deal', 'Media Kit', 'Your numbers and audience on one page.', ['cv-deal-rate']),
    'deal-review':    ('deal', 'Weekly Review', 'Five minutes to keep every deal moving.', ['cv-deal-board']),
}


def screen_masks(scene_file, n):
    """exact white screen areas of the scene (fingers / bezels that overlap stay outside), left to right"""
    from scipy import ndimage
    im = np.array(Image.open(os.path.join(HERE, scene_file)).convert('RGB')).astype(int)
    white = (im.min(axis=2) > 232) & ((im.max(axis=2) - im.min(axis=2)) < 16)
    lab, _ = ndimage.label(white)
    sizes = ndimage.sum(white, lab, range(1, lab.max() + 1))
    ms = [ndimage.binary_fill_holes(lab == i + 1) for i in np.argsort(sizes)[::-1][:n]]
    return sorted(ms, key=lambda m: np.nonzero(m)[1].min())


def make_real(img, bg_tone):
    """make a crisp screenshot sit in the photo: match softness, light and colour, add glass glare"""
    from PIL import ImageFilter, ImageEnhance
    w, h = img.size
    img = img.convert('RGB').filter(ImageFilter.GaussianBlur(0.9))
    img = ImageEnhance.Contrast(img).enhance(0.9)
    img = ImageEnhance.Brightness(img).enhance(0.95)
    tint = Image.new('RGB', img.size, bg_tone)
    img = Image.blend(img, tint, 0.07)
    a = np.array(img).astype(float)
    yy, xx = np.mgrid[0:h, 0:w]
    glare = np.clip(1 - ((xx / w) * 0.8 + (yy / h) * 0.6), 0, 1) ** 2 * 26      # soft light from top-left
    vign = (np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy)) / (0.035 * max(w, h)))
    shade = (1 - np.clip(vign, 0, 1)) * 0.12                                     # dark inner edge
    a = a + glare[..., None]
    a = a * (1 - shade[..., None])
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def mobile(c):
    """desktop crop -> Notion mobile screen: scaled to phone width + the real Notion mobile bottom bar"""
    nav = Image.open(os.path.join(HERE, 'ph-fco-invoices-board.jpg')).convert('RGB')
    nav = nav.crop((0, nav.height - 330, nav.width, nav.height))
    W = nav.width; H = int(W * 2.11)
    k = W / c.width
    c = c.resize((W, int(c.height * k)), Image.LANCZOS)
    out = Image.new('RGB', (W, H), (255, 255, 255))
    out.paste(c.crop((0, 0, W, min(c.height, H - nav.height + 40))), (0, 70))
    out.paste(nav, (0, H - nav.height))
    return out


def warp_bg(prod, screens):
    p = PROD[prod]
    sc = Image.open(os.path.join(HERE, p['scene'])).convert('RGB')
    k = CW / sc.width
    W2, H2 = CW, int(sc.height * k)
    bg = sc.resize((W2, H2), Image.LANCZOS).convert('RGBA')
    tone = tuple(int(v) for v in np.array(sc).reshape(-1, 3).mean(axis=0))
    quads = screens_of(p['scene'], len(screens))
    masks = screen_masks(p['scene'], len(screens))
    cy_all = []
    for q, mk, s in zip(quads, masks, screens):
        qq = [(x * k, y * k) for x, y in q]
        cx = sum(a for a, _ in qq) / 4; cy = sum(b for _, b in qq) / 4; cy_all.append(cy)
        qq = [(cx + (x - cx) * 1.07, cy + (y - cy) * 1.05) for x, y in qq]
        c = Image.open(B.src(s)).convert('RGB')
        is_phone = mk.sum() and (np.ptp(np.nonzero(mk)[0]) > 1.6 * np.ptp(np.nonzero(mk)[1]))
        if is_phone and not s.startswith('ph-'):
            c = mobile(c)
        sw = ((qq[1][0] - qq[0][0]) ** 2 + (qq[1][1] - qq[0][1]) ** 2) ** .5
        sh = ((qq[3][0] - qq[0][0]) ** 2 + (qq[3][1] - qq[0][1]) ** 2) ** .5
        ar = sw / sh; cw, ch = c.size
        c = c.crop((0, 0, int(ch * ar), ch)) if cw / ch > ar else c.crop((0, 0, cw, int(cw / ar)))
        c = c.resize((int(sw * 1.2), int(sw * 1.2 / ar)), Image.LANCZOS)
        c = make_real(c, tone)
        cw, ch = c.size
        warped = c.convert('RGBA').transform((W2, H2), Image.PERSPECTIVE,
                                             B._coeffs(qq, [(0, 0), (cw, 0), (cw, ch), (0, ch)]), Image.BICUBIC)
        from PIL import ImageFilter
        m = Image.fromarray((mk * 255).astype(np.uint8)).resize((W2, H2), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2))
        bg.paste(warped, (0, 0), m)
    # vertical band of CH px centred on the screens
    mid = sum(cy_all) / len(cy_all) if cy_all else H2 / 2
    y0 = int(min(max(0, mid - CH / 2), max(0, H2 - CH)))
    bg = bg.crop((0, y0, CW, y0 + CH))
    # soft panel behind the text on the left (same as home covers)
    arr = np.zeros((CH, CW, 4), np.uint8)
    arr[..., :3] = (40, 28, 20) if p['dark'] else (246, 241, 233)
    for x in range(CW):
        t = x / CW; a = 0.92 if t < 0.30 else max(0.0, 0.92 * (1 - (t - 0.30) / 0.18))
        arr[:, x, 3] = int(255 * a * (0.80 if p['dark'] else 1))
    bg.alpha_composite(Image.fromarray(arr))
    return bg.convert('RGB')


def build(cid):
    prod, title, sub, screens = COVERS[cid]
    p = PROD[prod]
    bgp = os.path.join(OUT, f'_{cid}-bg.jpg'); warp_bg(prod, screens).save(bgp, quality=95)
    ink, mut, kick = ('#FFFDF9', '#F1E7DC', '#E8D6C3') if p['dark'] else ('#2E2A25', '#5C554C', '#7A6A58')
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:F;font-weight:600;src:url(file://{FONTS}/fraunces600.woff2)}}
@font-face{{font-family:I;font-weight:500;src:url(file://{FONTS}/inter500.woff2)}}
@font-face{{font-family:I;font-weight:700;src:url(file://{FONTS}/inter700.woff2)}}
body{{margin:0}} .c{{position:relative;width:1500px;height:600px;background:url(file://{bgp}) center/cover}}
.t{{position:absolute;left:150px;top:50%;transform:translateY(-50%);width:640px}}
.k{{font:700 16px I;letter-spacing:4px;color:{kick};margin:0 0 14px}}
.h{{font:600 78px/1.0 F;color:{ink};margin:0 0 16px}}
.s{{font:500 22px/1.35 I;color:{mut};margin:0}}
</style></head><body><div class="c"><div class="t"><p class="k">{p['kicker']}</p><p class="h">{title}</p><p class="s">{sub}</p></div></div></body></html>"""
    hp = os.path.join(OUT, f'_{cid}.html'); open(hp, 'w').write(html)
    shot = hp + '.png'
    subprocess.run([B.CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=2', '--window-size=1500,800', f'--screenshot={shot}', 'file://' + hp],
                   check=True, capture_output=True)
    Image.open(shot).crop((0, 0, CW, CH)).convert('RGB').save(os.path.join(OUT, f'{cid}.jpg'), quality=90, optimize=True, progressive=True)
    for f in (bgp, hp, shot): os.remove(f)
    print('ok', cid)


if __name__ == '__main__':
    for cid in sys.argv[1:] or list(COVERS):
        build(cid)
