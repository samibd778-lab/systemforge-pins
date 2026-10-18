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


def laptop(src, cw, ch, top, width=900):
    h = round(width * ch / cw)
    left = (W - width) // 2
    return (f'<div style="position:absolute;left:{left - 22}px;top:{top}px;width:{width + 44}px;height:{h + 44}px;background:#1F1D1A;border-radius:26px;box-shadow:0 40px 80px rgba(30,25,20,.35)"></div>'
            f'<img src="{src}" style="position:absolute;left:{left}px;top:{top + 22}px;width:{width}px;height:{h}px;border-radius:6px">'
            f'<div style="position:absolute;left:{left - 110}px;top:{top + h + 44}px;width:{width + 220}px;height:30px;background:linear-gradient(#DAD4CA,#B8B1A5);border-radius:0 0 34px 34px"></div>')


def page(p, i, s, n, tmp):
    name, kick = SPEC[p]['name'], SPEC[p]['kicker']
    a, em, b = s['title']
    title = f'{a}<br><i style="color:{BR}">{em}</i>' + (f'<br>{b}' if b else '')
    body = ''
    if 'shot' in s:
        path, (cw, ch) = crop_image({'id': f'k-{p}-{i}', 'shot': s['shot'], 'crop': s['crop']}, tmp)
        dst = os.path.join(ROOT, 'canva', 'assets', f'k-{p}-{i}.png')
        shutil.copy(path, dst)
        src = RAW + f'canva/assets/k-{p}-{i}.png'
        width = 900 if cw / ch > 1.5 else 820
        body += laptop(src, cw, ch, 760 if not s.get('cover') else 720, width)
        pills = ''.join(f'<div style="display:inline-block;margin:0 12px 14px 0;background:{PAP};border-radius:40px;padding:12px 24px 12px 12px;font-family:Inter,sans-serif;font-weight:700;font-size:26px;color:{INK};box-shadow:0 8px 20px rgba(46,42,37,.10)">'
                        f'<span style="display:inline-block;width:44px;height:44px;line-height:44px;text-align:center;border-radius:50%;background:{DOT[k % 6]};margin-right:12px;font-size:22px">{ic}</span>{t}</div>'
                        for k, (ic, t) in enumerate(s['pills']))
        body += f'<div style="position:absolute;left:70px;right:70px;top:{560 if not s.get("cover") else 540}px">{pills}</div>'
    else:
        items = ''.join(f'<div style="display:block;margin-bottom:16px;background:{PAP};border-radius:22px;padding:20px 26px;font-family:Inter,sans-serif;font-weight:700;font-size:{30 if len(s["list"]) < 7 else 27}px;color:{INK};box-shadow:0 8px 20px rgba(46,42,37,.08)">'
                        f'<span style="display:inline-block;width:46px;height:46px;line-height:46px;text-align:center;border-radius:50%;background:{SAGE};color:{PAP};margin-right:18px;font-size:22px">{k + 1 if len(s["list"]) < 7 else "✓"}</span>{t}</div>'
                        for k, t in enumerate(s['list']))
        body += f'<div style="position:absolute;left:70px;right:70px;top:560px">{items}</div>'
    tag = 'SWIPE ›' if s.get('cover') else ('LINK IN BIO' if s.get('final') else f'{i} / {n}')
    fade = 'linear-gradient(180deg, rgba(246,241,233,.97) 0%, rgba(246,241,233,.95) 44%, rgba(246,241,233,.55) 62%, rgba(246,241,233,0) 80%)'
    return f'''<div data-document-role="page" data-label="{p} slide {i}" style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{CREAM}">
<img src="{U.format(BG[s['bg']])}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:cover">
<div style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;background:{fade}"></div>
<div style="position:absolute;left:70px;top:64px;background:{SAGE};color:{PAP};border-radius:8px;padding:10px 18px;font-family:Inter,sans-serif;font-weight:700;font-size:22px;letter-spacing:2px">{tag}</div>
<div style="position:absolute;right:70px;top:72px;font-family:Inter,sans-serif;font-weight:700;font-size:22px;letter-spacing:3px;color:{SAGE}">{kick if s.get('cover') else name.upper()}</div>
<div style="position:absolute;left:70px;right:70px;top:150px;font-family:'Source Serif 4',serif;font-weight:700;font-size:{96 if s.get('cover') else 84}px;line-height:1.04;color:{INK}">{title}</div>
<div style="position:absolute;left:70px;right:120px;top:{430 if s.get('cover') else 420}px;font-family:Inter,sans-serif;font-weight:500;font-size:30px;line-height:1.4;color:{MUT}">{s['sub']}</div>
{body}
<div style="position:absolute;left:0;right:0;bottom:46px;text-align:center;font-family:Inter,sans-serif;font-weight:700;font-size:24px;color:{INK}"><span style="display:inline-block;background:{PAP};border-radius:40px;padding:12px 26px">SF&nbsp; SystemForge · {name}</span></div>
</div>'''


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
