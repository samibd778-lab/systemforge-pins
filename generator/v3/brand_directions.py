"""3 visual directions for the SystemForge store banners (preview on the Etsy 3360x840 banner).
A dark studio · B forest block · C editorial light. All product visuals are real Notion crops.
Usage: python3 generator/v3/brand_directions.py  -> brand/directions/<A|B|C>-etsy.png
"""
import os, subprocess
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'brand', 'directions')
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
F = os.path.join(ROOT, 'generator', 'remotion', 'public')
CR = os.path.join(ROOT, 'canva', 'v3', 'crops')
PH = os.path.join(ROOT, 'shots', 'phone')
CSS = (f"@font-face{{font-family:Serif;font-weight:700;src:url(file://{F}/sourceserif700.woff2)}}"
       f"@font-face{{font-family:Fr;font-weight:600;src:url(file://{F}/fraunces600.woff2)}}"
       f"@font-face{{font-family:Inter;font-weight:500;src:url(file://{F}/inter500.woff2)}}"
       f"@font-face{{font-family:Inter;font-weight:700;src:url(file://{F}/inter700.woff2)}}"
       f"@font-face{{font-family:Mont;font-weight:800;src:url(file://{F}/montserrat800.woff2)}}"
       f"@font-face{{font-family:Mont;font-weight:900;src:url(file://{F}/montserrat900.woff2)}}"
       "body{margin:0}*{box-sizing:border-box}")
PRODUCTS = ['Freelancer Client OS', 'Content Creator Studio', 'Brand Deal Tracker', 'Proposal Tracker']


def render(html, w, h, out):
    p = os.path.join(OUT, '_d.html')
    open(p, 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>')
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    f'--window-size={w},{h + 200}', f'--screenshot={p}.png', 'file://' + p], check=True, capture_output=True)
    Image.open(p + '.png').crop((0, 0, w, h)).convert('RGB').save(out, optimize=True)
    os.remove(p); os.remove(p + '.png'); print('ok', out)


def window(img, w, x, y, rot=0, dark=False, z=1):
    """Real Notion crop inside a simple app window frame."""
    bar = '#2A2D33' if dark else '#EDEAE4'
    dots = ''.join(f'<span style="width:14px;height:14px;border-radius:50%;background:{c}"></span>' for c in ('#FF6B5B', '#FFB547', '#5BD6A0'))
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);z-index:{z};border-radius:22px;overflow:hidden;'
            f'background:#fff;box-shadow:0 40px 90px rgba(0,0,0,.35),0 0 0 1px rgba(0,0,0,.06)">'
            f'<div style="height:40px;background:{bar};display:flex;gap:9px;align-items:center;padding-left:18px">{dots}</div>'
            f'<img src="file://{img}" style="display:block;width:100%"></div>')


def phone(img, w, x, y, rot=0, z=3):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{int(w*2.05)}px;transform:rotate({rot}deg);z-index:{z};'
            f'border-radius:{int(w*.16)}px;background:#111;padding:{int(w*.035)}px;box-shadow:0 40px 90px rgba(0,0,0,.45)">'
            f'<div style="width:100%;height:100%;border-radius:{int(w*.13)}px;overflow:hidden;background:#fff">'
            f'<img src="file://{img}" style="width:100%;height:100%;object-fit:cover;object-position:top"></div></div>')


def logo(size, bg, fg):
    return (f'<div style="width:{size}px;height:{size}px;border-radius:{int(size*.28)}px;background:{bg};color:{fg};display:grid;place-items:center;'
            f'font-family:Mont;font-weight:900;font-size:{int(size*.42)}px;letter-spacing:-1px">SF</div>')


def A():  # dark studio
    W, H = 3360, 840
    vis = (window(f'{CR}/cv-fco-proj.png', 520, 1880, 150, -4, True, 1) + window(f'{CR}/cv-prop-table.png', 900, 2180, 110, 2, True, 2)
           + window(f'{CR}/cv-deal-now.png', 760, 2470, 380, -2, True, 2) + phone(f'{PH}/ccs-pipeline-posted.jpg', 250, 3020, 140, 4))
    txt = (f'<div style="position:absolute;left:220px;top:0;height:{H}px;display:flex;flex-direction:column;justify-content:center;z-index:5">'
           f'<div style="display:flex;align-items:center;gap:22px">{logo(84, "#7FE0B0", "#0E1013")}'
           f'<span style="font-family:Inter;font-weight:700;font-size:28px;letter-spacing:8px;color:#7FE0B0">NOTION TEMPLATES</span></div>'
           f'<div style="margin-top:30px;font-family:Mont;font-weight:900;font-size:150px;line-height:.95;letter-spacing:-5px;color:#F6F4EF">SystemForge</div>'
           f'<div style="margin-top:26px;font-family:Inter;font-weight:500;font-size:42px;color:#A9B0BC">Run your freelance or creator business from <span style="color:#F6F4EF">one Notion page.</span></div></div>')
    bg = (f'<div style="position:absolute;inset:0;background:radial-gradient(60% 120% at 75% 50%,#1F2A26 0%,#0E1013 70%)"></div>'
          f'<div style="position:absolute;left:1700px;top:-200px;width:1400px;height:1200px;border-radius:50%;background:#7FE0B0;opacity:.10;filter:blur(160px)"></div>')
    return f'<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden">{bg}{vis}{txt}</div>'


def B():  # forest block
    W, H = 3360, 840
    vis = (window(f'{CR}/cv-ccs-cal.png', 1150, 1900, 120, 0, False, 1) + phone(f'{PH}/fco-invoices-board.jpg', 270, 2880, 170, 0, 3)
           + window(f'{CR}/c-deal-now.png', 760, 1750, 520, 0, False, 2))
    chips = ''.join(f'<span style="padding:14px 26px;border-radius:999px;border:2px solid rgba(246,241,233,.35);font-family:Inter;font-weight:700;font-size:26px;color:#F6F1E9">{p}</span>' for p in PRODUCTS)
    txt = (f'<div style="position:absolute;left:200px;top:0;height:{H}px;width:1500px;display:flex;flex-direction:column;justify-content:center;z-index:5">'
           f'<div style="display:flex;align-items:center;gap:22px">{logo(80, "#F6F1E9", "#1F3A2E")}'
           f'<span style="font-family:Fr;font-weight:600;font-size:56px;color:#F6F1E9">SystemForge</span></div>'
           f'<div style="margin-top:34px;font-family:Fr;font-weight:600;font-size:96px;line-height:1.02;letter-spacing:-2px;color:#F6F1E9">Calm Notion systems for<br><i style="color:#E9C9A8">freelancers &amp; creators.</i></div>'
           f'<div style="margin-top:38px;display:flex;flex-wrap:wrap;gap:14px">{chips}</div></div>')
    bg = '<div style="position:absolute;inset:0;background:#1F3A2E"></div><div style="position:absolute;left:1650px;top:0;width:1710px;height:840px;background:#2C4D3D"></div>'
    return f'<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden">{bg}{vis}{txt}</div>'


def C():  # editorial light
    W, H = 3360, 840
    cards = [('cv-prop-pipe.png', 'Proposal Tracker'), ('cv-deal-board.png', 'Brand Deal Tracker'), ('cv-ccs-top.png', 'Content Creator Studio'), ('cv-fco-proj.png', 'Freelancer Client OS')]
    grid = '<div style="position:absolute;left:1820px;top:90px;width:1360px;display:grid;grid-template-columns:1fr 1fr;gap:26px;z-index:2">'
    for img, name in cards:
        grid += (f'<div style="border-radius:20px;overflow:hidden;background:#fff;border:2px solid #E7E2D9">'
                 f'<div style="height:250px;overflow:hidden"><img src="file://{CR}/{img}" style="width:100%;height:100%;object-fit:cover;object-position:left top"></div>'
                 f'<div style="padding:16px 22px;font-family:Inter;font-weight:700;font-size:26px;color:#1A1A1A;border-top:2px solid #E7E2D9">{name}</div></div>')
    grid += '</div>'
    txt = (f'<div style="position:absolute;left:200px;top:0;height:{H}px;display:flex;flex-direction:column;justify-content:center;z-index:5">'
           f'<div style="display:flex;align-items:center;gap:20px">{logo(76, "#1A1A1A", "#FAF8F3")}'
           f'<span style="font-family:Inter;font-weight:700;font-size:40px;color:#1A1A1A">SystemForge</span></div>'
           f'<div style="margin-top:34px;font-family:Mont;font-weight:900;font-size:118px;line-height:.98;letter-spacing:-4px;color:#1A1A1A">Notion templates<br>that <span style="background:#C9E4C5;padding:0 18px;border-radius:18px">do the work.</span></div>'
           f'<div style="margin-top:30px;font-family:Inter;font-weight:500;font-size:38px;color:#6B6B6B">For freelancers and content creators · Instant download</div></div>')
    return f'<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:#FAF8F3">{txt}{grid}</div>'


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for n, f in (('A', A), ('B', B), ('C', C)):
        render(f(), 3360, 840, os.path.join(OUT, f'{n}-etsy.png'))
