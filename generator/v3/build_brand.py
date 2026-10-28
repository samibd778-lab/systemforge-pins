"""SystemForge store branding (v3 lifestyle style): banners, logo, IG highlights, Gumroad product images.

Writes brand/<file>.png. Uses the real v3 lifestyle scenes (canva/v3/bg, real Notion screens on the devices)
and the Etsy v3 main images (canva/v3/etsy/final/<p>/<p>-1-main.png).
Usage: python3 generator/v3/build_brand.py
"""
import os, subprocess, shutil
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'brand')
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
F = os.path.join(ROOT, 'generator', 'remotion', 'public')
BG = os.path.join(ROOT, 'canva', 'v3', 'bg')
CREAM, INK, MUT, SAGE, SAGE_L, CLAY = '#F6F1E9', '#2E2A25', '#5C554C', '#7A8B6F', '#E3E8DC', '#EFDCCB'
FONTS = (f"@font-face{{font-family:Serif;font-weight:700;src:url(file://{F}/sourceserif700.woff2)}}"
         f"@font-face{{font-family:Inter;font-weight:500;src:url(file://{F}/inter500.woff2)}}"
         f"@font-face{{font-family:Inter;font-weight:700;src:url(file://{F}/inter700.woff2)}}"
         "body{margin:0}*{box-sizing:border-box}")
PRODUCTS = ['Freelancer Client OS', 'Content Creator Studio', 'Brand Deal Tracker', 'Proposal Tracker']
SCENES = ['v3-ccs-desk.jpg', 'v3-fco-hand.jpg', 'v3-prop-desk.jpg']


def render(html, w, h, out):
    p = os.path.join(OUT, '_b.html')
    open(p, 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}</style></head><body>{html}</body></html>')
    shot = p + '.png'
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=1', f'--window-size={w},{h + 200}', f'--screenshot={shot}', 'file://' + p],
                   check=True, capture_output=True)
    Image.open(shot).crop((0, 0, w, h)).convert('RGB').save(out, optimize=True)
    os.remove(p); os.remove(shot)
    print('ok', os.path.relpath(out, ROOT), w, h)


def logo_mark(size, fs=None):
    fs = fs or int(size * 0.42)
    return (f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:{SAGE};display:flex;align-items:center;justify-content:center;'
            f'color:{CREAM};font-family:Serif;font-style:italic;font-weight:700;font-size:{fs}px;letter-spacing:-1px;flex:none">SF</div>')


def banner(W, H, safe, tiles=3, products=True):
    """safe = (x, y, w, h): area that must hold all text and images (the rest is background)."""
    sx, sy, sw, sh = safe
    u = sh / 420  # scale unit: designed for a 420px-high safe area
    gap = int(18 * u)
    tile_h = int(min(sh * 0.86, (sw * 0.44 - gap * (tiles - 1)) / tiles / 0.62)); tile_w = int(tile_h * 0.62)
    imgs = ''
    for i, s in enumerate(SCENES[:tiles]):
        x = sx + sw - tile_w * (tiles - i) - gap * (tiles - 1 - i)
        y = sy + (sh - tile_h) // 2 + (int(16 * u) if i == 1 else 0)
        imgs += (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{tile_w}px;height:{tile_h}px;border-radius:{int(26*u)}px;overflow:hidden;'
                 f'box-shadow:0 {int(18*u)}px {int(40*u)}px rgba(46,42,37,.18);border:{max(2,int(5*u))}px solid #FFFDF9">'
                 f'<img src="file://{BG}/{s}" style="width:100%;height:100%;object-fit:cover;object-position:center 62%"></div>')
    chips = ''
    if products:
        chips = '<div style="display:flex;flex-wrap:wrap;gap:%dpx;margin-top:%dpx;max-width:%dpx">' % (int(10*u), int(22*u), int(sw * 0.5)) + ''.join(
            f'<span style="padding:{int(8*u)}px {int(16*u)}px;border-radius:999px;background:#FFFDF9;border:{max(1,int(2*u))}px solid {SAGE_L};'
            f'font-family:Inter;font-weight:700;font-size:{int(17*u)}px;color:{INK}">{p}</span>' for p in PRODUCTS) + '</div>'
    text = (f'<div style="position:absolute;left:{sx}px;top:{sy}px;height:{sh}px;width:{int(sw*0.52)}px;display:flex;flex-direction:column;justify-content:center">'
            f'<div style="display:flex;align-items:center;gap:{int(16*u)}px">{logo_mark(int(64*u))}'
            f'<span style="font-family:Inter;font-weight:700;font-size:{int(18*u)}px;letter-spacing:{int(4*u)}px;color:{SAGE}">NOTION TEMPLATES</span></div>'
            f'<div style="margin-top:{int(18*u)}px;font-family:Serif;font-weight:700;font-size:{int(92*u)}px;line-height:1;letter-spacing:{-2*u}px;color:{INK}">SystemForge</div>'
            f'<div style="margin-top:{int(14*u)}px;font-family:Inter;font-weight:500;font-size:{int(28*u)}px;line-height:1.3;color:{MUT}">Calm Notion systems for<br>freelancers and content creators.</div>'
            f'{chips}</div>')
    deco = (f'<div style="position:absolute;left:{-int(H*0.35)}px;top:{-int(H*0.45)}px;width:{int(H*1.1)}px;height:{int(H*1.1)}px;border-radius:50%;background:{SAGE_L}"></div>'
            f'<div style="position:absolute;right:{-int(H*0.4)}px;bottom:{-int(H*0.6)}px;width:{int(H*1.2)}px;height:{int(H*1.2)}px;border-radius:50%;background:{CLAY};opacity:.7"></div>')
    return f'<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{CREAM}">{deco}{imgs}{text}</div>'


def logo_page(S=1080):
    return (f'<div style="width:{S}px;height:{S}px;background:{CREAM};display:flex;align-items:center;justify-content:center">'
            f'{logo_mark(int(S*0.86), int(S*0.36))}</div>')


def highlight(label, icon, S=(1080, 1920)):
    w, h = S
    return (f'<div style="width:{w}px;height:{h}px;background:{SAGE};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px">'
            f'<div style="width:520px;height:520px;border-radius:50%;background:{CREAM};display:flex;align-items:center;justify-content:center;font-size:230px">{icon}</div>'
            f'<div style="font-family:Inter;font-weight:700;font-size:64px;letter-spacing:6px;color:{CREAM}">{label}</div></div>')


def main():
    os.makedirs(OUT, exist_ok=True)
    # store / channel banners
    render(banner(3360, 840, (180, 120, 3000, 600)), 3360, 840, os.path.join(OUT, 'etsy-banner-3360x840.png'))
    render(banner(2560, 1440, (507, 509, 1546, 423)), 2560, 1440, os.path.join(OUT, 'youtube-banner-2560x1440.png'))
    render(banner(1640, 856, (190, 170, 1260, 516), tiles=2), 1640, 856, os.path.join(OUT, 'facebook-cover-1640x856.png'))
    render(banner(1920, 1080, (150, 230, 1620, 620)), 1920, 1080, os.path.join(OUT, 'pinterest-cover-1920x1080.png'))
    render(banner(1500, 500, (80, 60, 1340, 380)), 1500, 500, os.path.join(OUT, 'gumroad-header-1500x500.png'))
    # logo + Instagram highlight covers
    render(logo_page(), 1080, 1080, os.path.join(OUT, 'logo-1080.png'))
    for name, icon in [('FREELANCE', '💼'), ('CREATORS', '🎬'), ('FREE', '🎁'), ('HOW IT WORKS', '✨')]:
        render(highlight(name, icon), 1080, 1920, os.path.join(OUT, f'ig-highlight-{name.lower().replace(" ", "-")}.png'))
    # Gumroad product images from the v3 Etsy mains: square thumbnail (the Etsy-safe centre square) + full cover
    for p in ['fco', 'ccs', 'deal', 'prop', 'fit', 'wcp']:
        src = os.path.join(ROOT, 'canva', 'v3', 'etsy', 'final', p, f'{p}-1-main.png')
        im = Image.open(src).convert('RGB'); w, h = im.size
        x0 = (w - h) // 2
        im.crop((x0, 0, x0 + h, h)).resize((1600, 1600), Image.LANCZOS).save(os.path.join(OUT, f'gumroad-thumb-{p}.png'), optimize=True)
        im.save(os.path.join(OUT, f'gumroad-cover-{p}.jpg'), quality=92)
        print('ok gumroad', p)


if __name__ == '__main__':
    main()
