"""Render a v5 Canva pin set locally at 2x (2000x3000 PNG), same HTML as the Canva import.
Usage: python3 generator/v3/render_v5.py <set> [preview.jpg]
Reads canva/v5/pins-<set>.html -> pins/v5/<id>.png + a contact sheet (default /tmp/<set>-preview.jpg)."""
import os, re, subprocess, sys, tempfile
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); import mini_listing as M  # noqa: E402
F = R + '/generator/remotion/public'
name = sys.argv[1]; prev = sys.argv[2] if len(sys.argv) > 2 else f'/tmp/{name}-preview.jpg'
h = open(f'{R}/canva/v5/pins-{name}.html').read()
h = re.sub(r'https://raw\.githubusercontent\.com/samibd778-lab/systemforge-pins/[A-Za-z0-9]+/', 'file://' + R + '/', h)
h = h.replace('<style>', '<style>' + ''.join(f'@font-face{{font-family:{f};{w}src:url(file://{F}/{n}.woff2)}}' for f, w, n in [
    ('"Great Vibes"', '', 'greatvibes400'), ('"Playfair Display"', 'font-weight:700;', 'playfair700'),
    ('Inter', 'font-weight:500;', 'inter500'), ('Inter', 'font-weight:700;', 'inter700')]), 1)
h = re.sub(r'<link[^>]+>', '', h)
pages = re.findall(r'(<div data-document-role="page" data-label="([^"]+)".*?</div>)(?=\n<div data-document-role|</body>)', h, re.S)
tmp = tempfile.mkdtemp(); ims = []
for pg, pid in pages:
    f = f'{tmp}/{pid}.html'; open(f, 'w').write(h.split('<body>')[0] + '<body>' + pg + '</body></html>')
    subprocess.run([M.L.B.CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=2', '--window-size=1000,1600', '--virtual-time-budget=3000', f'--screenshot={f}.png', 'file://' + f],
                   capture_output=True, check=True)
    im = Image.open(f + '.png').crop((0, 0, 2000, 3000)).convert('RGB'); im.save(f'{R}/pins/v5/{pid}.png', optimize=True)
    ims.append(im.resize((400, 600)))
cols = min(len(ims), 5); rows = (len(ims) + cols - 1) // cols
s = Image.new('RGB', (400 * cols, 600 * rows), 'white')
for k, im in enumerate(ims): s.paste(im, ((k % cols) * 400, (k // cols) * 600))
s.save(prev); print(prev, [p for _, p in pages])
