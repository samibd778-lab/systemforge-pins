"""Lifestyle carousel (1080x1350, one page per slide) as Canva-importable HTML.
Real Notion screenshots (cropped to canva/assets) on free Unsplash photos, SystemForge colors.
Usage: python3 generator/canva_carousel.py prop  -> canva/carousel-prop.html
"""
import json, os, sys, tempfile, shutil
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles'))
from pins_v2 import ROOT, crop_image  # noqa: E402

RAW = 'https://raw.githubusercontent.com/samibd778-lab/systemforge-pins/main/'
U = 'https://images.unsplash.com/photo-{}?fm=jpg&q=80&w=1600&h=2000&fit=crop'
BG = {'glasses': '1746792651683-30fc8fcec1a3', 'mug': '1499750310107-5fef28a66643',
      'espresso': '1757447247562-31dd79dc4f0a', 'plant': '1746792613213-c154e2891449', 'minimal': '1752223638233-4c9545333f89'}
INK, MUT, SAGE, CLAY, CREAM, PAP, ACC, BR = '#2E2A25', '#5C554C', '#7A8B6F', '#EFDCCB', '#F6F1E9', '#FFFDF9', '#D9A07B', '#9A5F3C'
DOT = ['#E3E8DC', '#EFDCCB', '#F3E6C8', '#E6DDEB', '#DCE7EC', '#F2DADA']

SPEC = {'prop': {'name': 'Proposal Tracker', 'kicker': 'NOTION TEMPLATE FOR FREELANCERS', 'slides': [
  {'bg': 'plant', 'title': ['Never forget to', 'follow up', 'again'], 'sub': 'See which quote to chase today, what to say, and if your price is too low.',
   'shot': 'shots/free/prop-home-zoom.png', 'crop': [470, 60, 1680, 790], 'pills': [('🔔', 'Follow-ups'), ('🗂', 'Pipeline'), ('✅', 'Price check')], 'cover': True},
  {'bg': 'glasses', 'title': ['Know who to', 'follow up today', ''], 'sub': 'Every quote tells you what to do next, so nothing slips.',
   'shot': 'shots/free/prop-home.png', 'crop': [580, 330, 1800, 600], 'pills': [('➡️', 'Next step on every quote'), ('⏱', 'Days since you sent it'), ('⏳', 'Warns before it expires')]},
  {'bg': 'mug', 'title': ['Every quote', 'on one board', ''], 'sub': 'Drag a card when a client answers. Value and next step on every card.',
   'shot': 'shots/free/prop-board.png', 'crop': [588, 175, 1785, 753], 'pills': [('📝', 'Draft'), ('📨', 'Sent'), ('🤝', 'Negotiating'), ('🏆', 'Won or Lost')]},
  {'bg': 'espresso', 'title': ['Is your quote', 'too cheap?', ''], 'sub': 'Add your hours and your rate. Price check tells you if the quote is under it.',
   'shot': 'shots/free/prop-item.png', 'crop': [735, 40, 1660, 520], 'pills': [('⏱', 'Hours'), ('💵', 'Your rate'), ('✅', 'Price check')]},
  {'bg': 'glasses', 'title': ['See what each', 'client is worth', ''], 'sub': 'Every client page adds up their quotes for you.',
   'shot': 'shots/free/prop-client.png', 'crop': [810, 30, 1660, 480], 'pills': [('💼', 'Open value'), ('🏆', 'Won value'), ('📈', 'Win rate')]},
  {'bg': 'mug', 'title': ['All your proposals', 'in one list', ''], 'sub': 'Status, value and win chance for every quote you send.',
   'shot': 'shots/free/prop-db.png', 'crop': [110, 90, 1240, 520], 'pills': [('🏷', 'Status'), ('💵', 'Value'), ('🎯', 'Win chance')]},
  {'bg': 'espresso', 'title': ['6 follow-up emails,', 'ready to copy', ''], 'sub': 'Change the words in brackets and send. Short and friendly works best.',
   'list': ['Follow up #1 (3 days after sending)', 'Follow up #2 (one week later)', 'Follow up #3 (add value)', 'Last check-in', 'Quote is about to expire', 'When they say no']},
  {'bg': 'glasses', 'title': ["What's", 'inside', ''], 'sub': 'One Notion page for every quote you send.',
   'list': ['Follow up today list', 'Next step on every proposal', 'Pipeline board: Draft to Won', 'Price check: hours x your rate', 'Clients: open value, won value, win rate', '6 follow-up emails', 'Proposal Writing Guide + checklist', 'Weekly review + client inquiry form']},
  {'bg': 'plant', 'title': ['Win more work', 'with less chasing', ''], 'sub': 'Instant access. Duplicate it into your Notion in one click.',
   'shot': 'shots/free/prop-board.png', 'crop': [588, 175, 1785, 753], 'pills': [('⚡', 'Instant access'), ('📋', 'Duplicate in 1 click'), ('💚', '14-day refund')], 'final': True},
]}}

W, H = 1080, 1350


def box(x, y, w, h, bg, r=0, extra=''):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{bg};border-radius:{r}px;{extra}"></div>'


def text(x, y, w, t, size, color=INK, weight=700, family='Inter,sans-serif', lh=1.2, align='left', italic=False):
    st = 'font-style:italic;' if italic else ''
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;font-family:{family};font-weight:{weight};font-size:{size}px;'
            f'line-height:{lh};color:{color};text-align:{align};{st}">{t}</div>')


def laptop(src, cw, ch, top, max_h):
    width = min(900, round(max_h * cw / ch))
    h = round(width * ch / cw)
    left = (W - width) // 2
    return (box(left - 20, top, width + 40, h + 40, '#1F1D1A', 24, 'box-shadow:0 40px 80px rgba(30,25,20,.35)')
            + f'<img src="{src}" style="position:absolute;left:{left}px;top:{top + 20}px;width:{width}px;height:{h}px;border-radius:6px">'
            + box(left - 90, top + h + 40, width + 180, 26, '#C9C2B7', 0, 'border-radius:0 0 30px 30px'))


def page(p, i, s, n, tmp):
    name, kick = SPEC[p]['name'], SPEC[p]['kicker']
    a, em, b = s['title']
    cover = s.get('cover')
    fs = 96 if cover else 84
    lines = [(a, False), (em, True)] + ([(b, False)] if b else [])
    out = []
    y = 150
    for t, it in lines:
        out.append(text(70, y, 940, t, fs, BR if it else INK, 700, "'Source Serif 4',serif", 1.05, italic=it))
        y += round(fs * 1.08)
    y += 18
    out.append(text(70, y, 880, s['sub'], 30, MUT, 500, lh=1.4))
    y += 44 * (2 if len(s['sub']) > 52 else 1) + 40
    if 'shot' in s:
        path, (cw, ch) = crop_image({'id': f'k-{p}-{i}', 'shot': s['shot'], 'crop': s['crop']}, tmp)
        shutil.copy(path, os.path.join(ROOT, 'canva', 'assets', f'k-{p}-{i}.png'))
        src = RAW + f'canva/assets/k-{p}-{i}.png'
        pills = s['pills']
        cols = 2 if len(pills) > 3 else len(pills)
        pw = (940 - 16 * (cols - 1)) // cols
        for k, (ic, t) in enumerate(pills):
            px, py = 70 + (k % cols) * (pw + 16), y + (k // cols) * 82
            out.append(box(px, py, pw, 68, PAP, 34, 'box-shadow:0 8px 20px rgba(46,42,37,.10)'))
            out.append(box(px + 12, py + 12, 44, 44, DOT[k % 6], 22))
            out.append(text(px + 12, py + 20, 44, ic, 22, INK, 500, align='center', lh=1))
            out.append(text(px + 68, py + 20, pw - 80, t, 24 if cols == 3 else 26, INK, 700, lh=1.1))
        y += ((len(pills) - 1) // cols + 1) * 82 + 40
        out.append(laptop(src, cw, ch, y, 1200 - y - 66))
    else:
        rows = s['list']
        step = 84 if len(rows) < 7 else 80
        for k, t in enumerate(rows):
            ry = y + k * step
            out.append(box(70, ry, 940, step - 14, PAP, 20, 'box-shadow:0 8px 20px rgba(46,42,37,.08)'))
            out.append(box(88, ry + (step - 14 - 44) // 2, 44, 44, SAGE, 22))
            out.append(text(88, ry + (step - 14 - 44) // 2 + 11, 44, str(k + 1) if len(rows) < 7 else '✓', 22, PAP, 700, align='center', lh=1))
            out.append(text(152, ry + (step - 14) // 2 - 16, 840, t, 28, INK, 700, lh=1.15))
    tag = 'SWIPE  ›' if cover else ('LINK IN BIO' if s.get('final') else f'{i} / {n}')
    fade = 'linear-gradient(180deg, rgba(246,241,233,.97) 0%, rgba(246,241,233,.94) 45%, rgba(246,241,233,.5) 65%, rgba(246,241,233,0) 85%)'
    tw = 40 + 15 * len(tag)
    head = (box(70, 64, tw, 44, SAGE, 8) + text(70, 75, tw, tag, 20, PAP, 700, align='center', lh=1)
            + text(440, 76, 570, kick if cover else name.upper(), 20, SAGE, 700, align='right', lh=1))
    foot = box(340, 1244, 400, 56, PAP, 28) + text(340, 1260, 400, 'SystemForge · ' + name, 22, INK, 700, align='center', lh=1)
    return (f'<div data-document-role="page" data-label="{p} slide {i}" style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{CREAM}">'
            f'<img src="{U.format(BG[s["bg"]])}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:cover">'
            + box(0, 0, W, H, fade) + head + ''.join(out) + foot + '</div>')


if __name__ == '__main__':
    p = sys.argv[1]
    slides = SPEC[p]['slides']
    with tempfile.TemporaryDirectory() as tmp:
        pages = ''.join(page(p, i + 1, s, len(slides), tmp) for i, s in enumerate(slides))
    html = ('<!doctype html><html><head><meta charset="utf-8">'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700&family=Source+Serif+4:ital,wght@0,700;1,700&display=swap" rel="stylesheet">'
            f'<style>body{{margin:0;font-family:Inter,sans-serif}}div,span{{font-family:Inter,sans-serif}}</style></head><body>{pages}</body></html>')
    open(os.path.join(ROOT, 'canva', f'carousel-{p}.html'), 'w').write(html)
    print('ok', len(slides))
