"""Style 1: annotated laptop mockup (headline + laptop + numbered callouts with arrows + pills).

python3 callout_mockup.py  -> out/ccs-callouts.png (1080x1350)
Callout targets are given in screenshot pixels (1920x1080 frame from a recording).
"""
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, '..', 'remotion', 'public')
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)

INK, MUT, ACC, SAGE, CREAM, PAP, CLAY, SAGEL = '#2E2A25', '#5C554C', '#D9A07B', '#7A8B6F', '#F6F1E9', '#FFFDF9', '#EFDCCB', '#E3E8DC'

W, H = 1080, 1350
SCREEN_X, SCREEN_Y, SCREEN_W = 110, 480, 860  # where the screenshot sits inside the page
SHOT_W, SHOT_H = 1920, 1080
K = SCREEN_W / SHOT_W
SCREEN_H = SHOT_H * K


def pt(x, y):
    return SCREEN_X + x * K, SCREEN_Y + y * K


def page(shot, kicker, title_a, title_hl, title_b, sub, callouts, pills, name):
    # callouts: (n, label, label_x, label_y, target_x, target_y) — label pos in page px, target in shot px
    arrows, labels = [], []
    for n, text, lx, ly, tx, ty in callouts:
        ex, ey = pt(tx, ty)
        # curve from the label edge towards the target
        sx = lx + (0 if ex < lx else 200)
        sy = ly + 30
        cx1, cy1 = sx + (ex - sx) * 0.15, sy + (ey - sy) * 0.85 if abs(ey - sy) > 60 else sy - 60
        arrows.append(f'<path d="M{sx},{sy} Q{cx1},{cy1} {ex},{ey}" fill="none" stroke="{SAGE}" stroke-width="3.5" stroke-linecap="round" marker-end="url(#ah)"/>'
                      f'<circle cx="{ex}" cy="{ey}" r="9" fill="{ACC}" stroke="#fff" stroke-width="3"/>')
        labels.append(f'<div class="co" style="left:{lx}px;top:{ly}px"><span class="n">{n}</span>{text}</div>')
    pill_html = ''.join(f'<div class="pill">{p}</div>' for p in pills)
    html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Fraunces;src:url(file://{FONTS}/fraunces600.woff2);font-weight:600}}
@font-face{{font-family:InterW;src:url(file://{FONTS}/inter500.woff2);font-weight:500}}
@font-face{{font-family:InterW;src:url(file://{FONTS}/inter700.woff2);font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;background:{CREAM};position:relative;overflow:hidden;font-family:InterW}}
.blob{{position:absolute;border-radius:50%}}
.kick{{position:absolute;top:70px;left:0;right:0;text-align:center}}
.kick span{{display:inline-flex;align-items:center;gap:10px;background:{PAP};border-radius:40px;padding:12px 26px;font-weight:700;font-size:22px;letter-spacing:1.5px;color:{INK};box-shadow:0 6px 20px rgba(46,42,37,.08)}}
.kick i{{width:28px;height:28px;border-radius:50%;background:{SAGE};color:{PAP};font-style:italic;font-family:Fraunces;font-size:14px;display:flex;align-items:center;justify-content:center}}
h1{{position:absolute;top:150px;left:40px;right:40px;text-align:center;font-family:Fraunces;font-weight:600;font-size:92px;line-height:1.02;color:{INK};letter-spacing:-2.5px}}
h1 em{{font-style:normal;background:linear-gradient(transparent 12%,{CLAY} 12%,{CLAY} 92%,transparent 92%);padding:0 14px;border-radius:14px;color:#9A5F3C}}
.sub{{position:absolute;top:372px;left:0;right:0;text-align:center;font-size:30px;color:{MUT}}}
.sub b{{color:{INK}}}
.lap{{position:absolute;left:{SCREEN_X-26}px;top:{SCREEN_Y-26}px;width:{SCREEN_W+52}px;height:{SCREEN_H+52}px;background:#1F1D1A;border-radius:26px;box-shadow:0 40px 80px rgba(46,42,37,.25)}}
.scr{{position:absolute;left:{SCREEN_X}px;top:{SCREEN_Y}px;width:{SCREEN_W}px;height:{SCREEN_H}px;background:#fff url("file://{shot}") 0 0/100% 100%;border-radius:6px}}
.base{{position:absolute;left:{SCREEN_X-110}px;top:{SCREEN_Y+SCREEN_H+26}px;width:{SCREEN_W+220}px;height:30px;background:linear-gradient(#D8D2C8,#B9B2A6);border-radius:0 0 34px 34px}}
.base:after{{content:"";position:absolute;left:50%;top:0;width:150px;height:12px;margin-left:-75px;background:#A9A196;border-radius:0 0 12px 12px}}
svg{{position:absolute;left:0;top:0}}
.co{{position:absolute;width:200px;background:{PAP};border-radius:18px;padding:12px 16px 12px 14px;font-weight:700;font-size:21px;line-height:1.2;color:{INK};display:flex;gap:10px;align-items:center;box-shadow:0 10px 26px rgba(46,42,37,.14)}}
.n{{flex:none;width:34px;height:34px;border-radius:50%;background:{SAGE};color:{PAP};font-size:18px;display:flex;align-items:center;justify-content:center}}
.pills{{position:absolute;bottom:70px;left:0;right:0;display:flex;justify-content:center;gap:16px}}
.pill{{background:{PAP};border-radius:40px;padding:14px 26px;font-weight:700;font-size:22px;color:{INK};box-shadow:0 6px 18px rgba(46,42,37,.08)}}
</style></head><body>
<div class="blob" style="width:620px;height:620px;background:{SAGEL};left:-260px;top:-240px"></div>
<div class="blob" style="width:700px;height:700px;background:{CLAY};right:-330px;bottom:-330px;opacity:.8"></div>
<div class="kick"><span><i>SF</i>{kicker}</span></div>
<h1>{title_a} <em>{title_hl}</em><br>{title_b}</h1>
<div class="sub">{sub}</div>
<div class="lap"></div><div class="scr"></div><div class="base"></div>
<svg width="{W}" height="{H}"><defs><marker id="ah" markerWidth="10" markerHeight="10" refX="0" refY="0" orient="auto" viewBox="-5 -5 10 10"><path d="M-4,-4 L2,0 L-4,4" fill="none" stroke="{SAGE}" stroke-width="2"/></marker></defs>{''.join(arrows)}</svg>
{''.join(labels)}
<div class="pills">{pill_html}</div>
</body></html>'''
    src = os.path.join(HERE, 'out', name + '.html')
    open(src, 'w').write(html)
    out = os.path.join(HERE, 'out', name + '.png')
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--hide-scrollbars', '--force-device-scale-factor=2',
                    f'--window-size={W},{H + 200}', f'--screenshot={out}', 'file://' + src], check=True, capture_output=True)
    from PIL import Image
    Image.open(out).crop((0, 0, W * 2, H * 2)).save(out)
    print(out)


if __name__ == '__main__':
    page(
        shot=os.path.join(HERE, 'ccs_58.png'),
        kicker='NOTION TEMPLATE FOR CREATORS',
        title_a='Know what', title_hl='to post', title_b='this week',
        sub='Missed, today and upcoming posts on <b>one page.</b>',
        callouts=[
            (1, 'Missed, today or in X days', 30, 1095, 560, 575),
            (2, 'Every post in one card', 850, 1095, 1240, 585),
            (3, 'Your thumbnail on every post', 850, 405, 1380, 230),
        ],
        pills=['Instant access', 'Duplicate in 1 click', 'Pay once'],
        name='ccs-callouts',
    )
