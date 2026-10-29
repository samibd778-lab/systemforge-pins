"""Etsy starter packs (v3 style, 2700x2026): Freelance Starter Pack and Creator Starter Pack (no overlapping templates).
Reuses the real listing images of each product. Only Etsy wording (delivery = PDF with one link per template).
Usage: python3 generator/v3/build_bundle.py [fs cs] -> canva/v3/etsy/final/<b>/<b>-N-*.png
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_listing as L

FIN = os.path.join(L.OUT, 'final')
INK, MUT, PAP, SER = L.INK, L.MUT, L.PAP, L.SER
B = {
 'fs': dict(name='Freelance Starter Pack', kicker='2 NOTION TEMPLATES FOR FREELANCERS', color='#F1E3D6', accent='#C98B6B',
            sub='Follow up on every quote,<br>then get paid on time.', prods=['prop', 'fit'],
            why={'prop': 'Follow up on every quote you send, with a next step and an expiry warning.',
                 'fit': 'Know who owes you, how late it is, and which reminder to send.'}),
 'cs': dict(name='Creator Starter Pack', kicker='2 NOTION TEMPLATES FOR CONTENT CREATORS', color='#E9EEE4', accent='#7A8B6F',
            sub='Plan your week of content<br>and track every brand deal.', prods=['wcp', 'deal'],
            why={'wcp': 'Plan your week in 15 minutes, with a weekly goal for every platform.',
                 'deal': 'Every brand deal from first pitch to paid, with the posts you still owe.'}),
}


def img(pk, n):
    import glob
    return 'file://' + glob.glob(os.path.join(FIN, pk, f'{pk}-{n}-*.png'))[0]


def card(src, x, y, w, rot=0, z=1):
    h = int(w * 2026 / 2700)
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z};'
            f'border-radius:18px;overflow:hidden;border:6px solid #FFFDF9;box-shadow:0 24px 50px rgba(46,42,37,.22)">'
            f'<img src="{src}" style="width:100%;height:100%;display:block"></div>')


def build(bk):
    b = B[bk]; P = L.P; acc = b['accent']; pages = []
    # 1. main: text inside the Etsy thumbnail square (x 169-1181), the two covers fanned on the right
    X = 205; n = len(b['prods'])
    inner = (L.blobs(acc)
             + L.T(X, 120, 520, b['kicker'], 16, f'font-weight:700;letter-spacing:3px;color:#7A6A58')
             + L.T(X, 160, 520, b['name'].replace(' ', '<br>', 1), 68, f'line-height:1.02;white-space:nowrap;color:{INK};{SER}')
             + L.T(X, 340, 440, b['sub'], 25, f'line-height:1.35;color:{MUT}'))
    for i, pk in enumerate(b['prods']):
        inner += (f'<p style="position:absolute;left:{X}px;top:{470 + i * 62}px;width:34px;margin:0;padding:3px 0;text-align:center;border-radius:999px;'
                  f'background:{acc};color:{PAP};font-size:19px;font-weight:700">✓</p>' + L.T(X + 48, 470 + i * 62, 420, P[pk]['name'], 25, f'font-weight:700;color:{INK}'))
    inner += L.T(X, 860, 0, f'INSTANT DOWNLOAD · {n} TEMPLATES', 19, f'padding:13px 26px;border-radius:999px;background:{INK};color:{PAP};font-weight:700;letter-spacing:2px')
    p0, p1 = b['prods']
    inner += card(img(p1, 1), 700, 120, 560, 4, 1) + card(img(p0, 1), 690, 470, 540, -3, 2)
    pages.append(L.page(f'{bk}-1-main', inner, None, b['color']))
    # 2-4. one page per included template
    for j, pk in enumerate(b['prods'], 2):
        p = P[pk]
        inner = (L.blobs(acc)
                 + f'<p style="position:absolute;left:70px;top:150px;margin:0;padding:10px 22px;border-radius:999px;background:{acc};color:{PAP};font-size:20px;font-weight:700;letter-spacing:2px">INCLUDED {j - 1} OF {n}</p>'
                 + L.T(70, 230, 440, p['name'], 56, f'line-height:1.05;color:{INK};{SER}')
                 + L.T(70, 400, 420, b['why'][pk], 26, f'line-height:1.4;color:{MUT}'))
        for i, f in enumerate(p['features']):
            inner += (f'<p style="position:absolute;left:70px;top:{600 + i * 56}px;width:30px;margin:0;padding:2px 0;text-align:center;border-radius:999px;'
                      f'background:{acc};color:{PAP};font-size:17px;font-weight:700">✓</p>' + L.T(114, 600 + i * 56, 400, f, 22, f'font-weight:500;color:{INK}'))
        inner += card(img(pk, 1), 540, 200, 760, 0, 1)
        pages.append(L.page(f'{bk}-{j}-included', inner, None, b['color']))
    # inside: one column per template
    k = len(b['prods']) + 2
    inner = (L.blobs(acc) + L.T(0, 80, 1350, "What's inside", 76, f'text-align:center;color:{INK};{SER}')
             + L.T(0, 185, 1350, b['name'] + f' · {len(b["prods"])} Notion templates', 28, f'text-align:center;color:{MUT}'))
    for c, pk in enumerate(b['prods']):
        x = 70 + c * 620
        inner += (f'<div style="position:absolute;left:{x}px;top:260px;width:590px;height:660px;background:#FFFFFF;border-radius:26px"></div>'
                  + L.T(x + 36, 292, 520, P[pk]['name'], 34, f'line-height:1.1;color:{INK};{SER}'))
        for i, it in enumerate(P[pk]['inside'][:8]):
            inner += (f'<p style="position:absolute;left:{x + 36}px;top:{380 + i * 64}px;width:28px;margin:0;padding:1px 0;text-align:center;border-radius:999px;'
                      f'background:{acc};color:{PAP};font-size:16px;font-weight:700">✓</p>' + L.T(x + 78, 378 + i * 64, 480, it, 22, f'font-weight:500;line-height:1.3;color:{INK}'))
    pages.append(L.page(f'{bk}-{k}-inside', inner, None, b['color']))
    # how it works (Etsy delivery: one PDF with the three links)
    steps = [('Download', 'After you buy, download the PDF from your Etsy purchases.'),
             ('Duplicate', 'The PDF has one link per template. Open each one and click Duplicate.'),
             ('Start', 'Open the Start here page of each template. Example data shows how it works.')]
    inner = L.blobs(acc) + L.T(0, 90, 1350, 'How it works', 76, f'text-align:center;color:{INK};{SER}')
    for j, (a, t) in enumerate(steps):
        x = 70 + j * 410
        inner += (f'<div style="position:absolute;left:{x}px;top:260px;width:380px;height:520px;background:#FFFFFF;border-radius:26px"></div>'
                  f'<p style="position:absolute;left:{x + 150}px;top:310px;width:80px;margin:0;padding:16px 0;text-align:center;border-radius:999px;background:{acc};color:{PAP};font-size:38px;font-weight:700">{j + 1}</p>'
                  + L.T(x, 440, 380, a, 44, f'text-align:center;color:{INK};{SER}')
                  + L.T(x + 40, 530, 300, t, 26, f'text-align:center;line-height:1.4;color:{MUT}'))
    inner += L.T(0, 850, 1350, f'Digital download · {len(b["prods"])} Notion templates · No physical item', 24, f'text-align:center;font-weight:500;color:{MUT}')
    pages.append(L.page(f'{bk}-{k + 1}-how', inner, None, b['color']))
    return pages


if __name__ == '__main__':
    import re
    for bk in sys.argv[1:] or list(B):
        os.makedirs(os.path.join(FIN, bk), exist_ok=True)
        for pg in build(bk):
            lab = re.search(r'data-label="([^"]+)"', pg).group(1)
            L.render_png(pg, os.path.join(FIN, bk, lab + '.png'))
        print('ok', bk)
