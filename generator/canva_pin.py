"""Export a v2 pin as Canva-importable HTML (one page, editable text/shapes, real screenshot).
Writes canva/<id>.html + canva/assets/<id>-crop.png. Import in Canva via raw GitHub URL.
Usage: python3 generator/canva_pin.py <id> [...]
"""
import json, os, re, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles'))
from pins_v2 import ROOT, pin_html, crop_image, PW, PH  # noqa: E402

RAW = 'https://raw.githubusercontent.com/samibd778-lab/systemforge-pins/main/'
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700&family=Source+Serif+4:wght@700&display=swap" rel="stylesheet">')


def canva_html(sp):
    with tempfile.TemporaryDirectory() as tmp:
        path, size = crop_image(sp, tmp)
        dst = os.path.join(ROOT, 'canva', 'assets', sp['id'] + '-crop.png')
        os.replace(path, dst) if os.path.dirname(path) == os.path.dirname(dst) else __import__('shutil').copy(path, dst)
        h = pin_html(sp, dst, size)
    h = h.replace('file://' + dst, RAW + 'canva/assets/' + sp['id'] + '-crop.png')
    h = re.sub(r'@font-face\{[^}]*\}', '', h)
    h = h.replace('font-family:Fraunces', "font-family:'Source Serif 4',serif").replace('font-family:InterW', "font-family:Inter,sans-serif")
    h = h.replace('<head>', '<head>' + FONTS)
    h = h.replace('<body>', f'<body style="margin:0"><div class="pg" data-document-role="page" data-label="{sp["id"]}" style="position:relative;width:{PW}px;height:{PH}px;overflow:hidden;background:#F6F1E9">', 1)
    h = h.replace('</body>', '</div></body>')
    h = h.replace('body{', '.pg{')
    return h


if __name__ == '__main__':
    spec = {p['id']: p for p in json.load(open(os.path.join(ROOT, 'generator', 'pins-v2-spec.json')))['pins']}
    for i in sys.argv[1:]:
        open(os.path.join(ROOT, 'canva', i + '.html'), 'w').write(canva_html(spec[i]))
        print('ok', i)
