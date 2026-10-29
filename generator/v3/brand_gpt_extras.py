"""Logo, Pinterest cover and IG highlight covers in the same look as the ChatGPT banners
(cream wall, deep green serif, warm wood, real Notion screens). Writes brand/gpt/*.png.
Run after fill_gpt.py. Usage: python3 generator/v3/brand_gpt_extras.py
"""
import os, subprocess
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(ROOT, 'brand', 'gpt'); FT = os.path.join(ROOT, 'brand', 'fonts')
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
GREEN, CREAM, INK = '#1B2F1B', '#F6EADB', '#3B3A33'
CSS = (f"@font-face{{font-family:DM;src:url(file://{FT}/dmserif.woff2)}}"
       f"@font-face{{font-family:Mono;src:url(file://{FT}/plexmono.woff2)}}body{{margin:0}}*{{box-sizing:border-box}}")


def render(html, w, h, out):
    p = os.path.join(D, '_x.html')
    open(p, 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>')
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=1', f'--window-size={w},{h + 200}', f'--screenshot={p}.png', 'file://' + p], check=True, capture_output=True)
    Image.open(p + '.png').crop((0, 0, w, h)).convert('RGB').save(os.path.join(D, out), optimize=True)
    os.remove(p); os.remove(p + '.png'); print('ok', out)


ICONS = {  # simple line icons, 24x24 grid
    'freelance': '<rect width="20" height="14" x="2" y="7" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    'creators': '<path d="m16 13 5.2 3.5a.5.5 0 0 0 .8-.4V7.9a.5.5 0 0 0-.8-.4L16 10.5"/><rect x="2" y="6" width="14" height="12" rx="2"/>',
    'free': '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C10 3 12 8 12 8s2-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
    'how-it-works': '<circle cx="12" cy="12" r="10"/><path d="M10 8l6 4-6 4z"/>',
    'templates': '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/>',
}


def main():
    # 1) Pinterest cover 16:9: crop of the Facebook scene (name, tagline, laptop + phone with real screens)
    fb = Image.open(os.path.join(D, 'fb-filled.png'))  # 2x of fb-src (2055x765)
    x0 = 640 * 2; w = int(fb.height * 16 / 9)
    fb.crop((x0, 0, x0 + w, fb.height)).resize((1920, 1080), Image.LANCZOS).save(os.path.join(D, 'pinterest-cover-1920x1080.png'))
    print('ok pinterest-cover-1920x1080.png')

    # 2) Logo: deep green tile, cream serif monogram (reads well as a small round avatar)
    logo = (f'<div style="width:1080px;height:1080px;background:{GREEN};display:flex;align-items:center;justify-content:center">'
            f'<div style="font-family:DM;font-size:560px;line-height:1;color:{CREAM};letter-spacing:-18px;margin-top:-30px">SF</div></div>')
    render(logo, 1080, 1080, 'logo-1080.png')
    # wordmark on the cream wall (for headers, PDFs, watermarks)
    render(f'<div style="width:2400px;height:800px;background:{CREAM};display:flex;flex-direction:column;align-items:center;justify-content:center">'
           f'<div style="font-family:DM;font-size:300px;line-height:1;color:{GREEN};letter-spacing:-6px">SystemForge</div>'
           f'<div style="margin-top:40px;font-family:Mono;font-size:62px;color:{INK}">Notion templates for freelancers &amp; creators</div></div>',
           2400, 800, 'logo-wordmark-2400x800.png')

    # 3) IG highlight covers: warm blurred desk light behind a green circle with a cream line icon
    bg = Image.open(os.path.join(D, 'fb-src.png')).convert('RGB').crop((0, 0, 430, 765)).resize((1080, 1920)).filter(ImageFilter.GaussianBlur(28))
    bg.save(os.path.join(D, '_hl-bg.png'))
    for name, svg in ICONS.items():
        render(f'<div style="width:1080px;height:1920px;background:url(file://{D}/_hl-bg.png);display:flex;align-items:center;justify-content:center">'
               f'<div style="width:600px;height:600px;border-radius:50%;background:{GREEN};display:flex;align-items:center;justify-content:center;box-shadow:0 30px 70px rgba(27,47,27,.28)">'
               f'<svg width="300" height="300" viewBox="0 0 24 24" fill="none" stroke="{CREAM}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{svg}</svg>'
               f'</div></div>', 1080, 1920, f'ig-highlight-{name}.png')
    os.remove(os.path.join(D, '_hl-bg.png'))


if __name__ == '__main__':
    main()
