"""Etsy delivery PDF (US Letter, 1 page), same look as the bonus guide.
Usage: python3 generator/etsy_pdf.py "<Product name>" "<notion.site link>" "<step 4 text>" out.pdf [screenshot.png]
Only Etsy links in the footer (no off-Etsy links in Etsy files). Screenshot must be a real one of the template."""
import base64, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, 'styles'))
from pins_v2 import FONT_CSS  # noqa: E402

CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
name, url, step4, out = sys.argv[1:5]
shot = sys.argv[5] if len(sys.argv) > 5 else None
dm = base64.b64encode(open(os.path.join(ROOT, 'brand/fonts/dmserif.woff2'), 'rb').read()).decode()

steps = [('Open the link', 'Click the button above. It opens in your browser.'),
         ('Log in to Notion', 'Use your Notion account, or create one in a minute.'),
         ('Click Duplicate', 'Top right corner. The template is copied into your workspace.'),
         ('Open “Start here”', step4)]
st = ''.join(f'<div class="s"><span class="n">{i + 1:02d}</span><b>{a}</b><p>{b}</p></div>' for i, (a, b) in enumerate(steps))
shot_html = ''
if shot:
    b64 = base64.b64encode(open(shot, 'rb').read()).decode()
    shot_html = (f'<div class="shot"><div class="bar"><i></i><i></i><i></i><span>{name}</span></div>'
                 f'<div class="vp"><img src="data:image/png;base64,{b64}"></div></div>')
first, _, rest = name.partition(' ')

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>{FONT_CSS}
@font-face{{font-family:DMS;src:url(data:font/woff2;base64,{dm}) format('woff2')}}
@page{{size:Letter;margin:0}}*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:8.5in;height:10.95in;overflow:hidden}}
body{{background:#F6F1E9;font-family:InterW;color:#2E2A25;position:relative}}
.hero{{position:relative;height:4.7in;background:#1F3324;color:#F3ECE2;overflow:hidden;padding:.5in .7in 0}}
.ring{{position:absolute;border-radius:50%;border:1.5px solid rgba(243,236,226,.13)}}
.r1{{width:5in;height:5in;right:-1.9in;top:-2.1in}}.r3{{width:2in;height:2in;right:-.5in;top:-.6in;background:#C98B6B;border:none;opacity:.9}}
.logo{{display:flex;align-items:center;gap:10px;font-weight:700;font-size:13px;color:#D9E2D2;position:relative}}
.logo i{{width:34px;height:34px;border-radius:50%;background:#F3ECE2;color:#1F3324;font-style:normal;display:flex;align-items:center;justify-content:center;font-size:12px}}
.k{{margin-top:20px;display:inline-block;border:1px solid rgba(243,236,226,.35);border-radius:99px;padding:6px 13px;font-weight:700;font-size:10px;letter-spacing:.14em;color:#D9E2D2}}
h1{{font-family:DMS;font-weight:400;font-size:48px;line-height:1;margin-top:14px}}h1 em{{color:#E8C3AA}}
.t{{margin-top:10px;font-weight:500;font-size:13.5px;color:#D6CCBE}}
.shot{{position:absolute;left:.7in;right:-.3in;top:2.45in;background:#fff;border-radius:12px 0 0 0;overflow:hidden;box-shadow:0 24px 50px rgba(0,0,0,.45)}}
.shot .bar{{height:24px;background:#EDE7DF;display:flex;align-items:center;gap:6px;padding:0 12px}}
.shot .bar i{{width:8px;height:8px;border-radius:50%;background:#D3C8BB}}.shot .bar i:first-child{{background:#E39A82}}
.shot .bar span{{margin-left:10px;font-size:8.5px;font-weight:700;color:#8A7A6C;background:#F7F3EE;border-radius:5px;padding:3px 30px 3px 10px}}
.shot .vp{{overflow:hidden}}.shot img{{display:block;width:100%;margin-top:-11%}}
.w{{padding:0 .7in}}
a.btn{{display:flex;justify-content:space-between;align-items:center;margin-top:20px;position:relative;background:#4A6B4F;color:#fff;text-decoration:none;border-radius:16px;padding:16px 24px;font-weight:700;font-size:19px;box-shadow:0 12px 26px rgba(31,51,36,.28)}}
a.btn span{{width:38px;height:38px;border-radius:50%;background:rgba(255,255,255,.22);display:flex;align-items:center;justify-content:center;font-size:20px}}
.u{{margin-top:9px;text-align:center;font-weight:500;font-size:8.5px;color:#6F665B;line-height:1.6}}.u a{{color:#2E2A25}}
.lbl{{margin:18px 0 9px;font-weight:700;font-size:10px;letter-spacing:.16em;color:#7A8B6F}}
.g{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.s{{background:#FFFDF9;border:1px solid #E7DED2;border-radius:14px;padding:12px 16px}}
.n{{font-family:DMS;font-size:26px;color:#C98B6B;line-height:1;display:block;margin-bottom:6px}}
.s b{{font-size:13.5px}}.s p{{margin-top:4px;font-weight:500;font-size:10.5px;line-height:1.5;color:#6F665B}}
.kn{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px}}
.kn div{{background:#E3E8DC;border-radius:12px;padding:12px 14px;font-weight:500;font-size:10px;line-height:1.5;color:#3E4A38}}.kn b{{display:block;font-size:11.5px;margin-bottom:3px;color:#1F3324}}
.f{{position:absolute;left:.7in;right:.7in;bottom:.35in;display:flex;justify-content:space-between;align-items:center;border-top:1px solid #E7DED2;padding-top:12px;font-weight:700;font-size:10.5px;color:#7A8B6F}}.f span:last-child{{color:#A39789;font-size:9.5px}}
</style></head><body>
<div class="hero"><div class="ring r1"></div><div class="ring r3"></div>
<div class="logo"><i>SF</i>SystemForge</div>
<div class="k">YOUR TEMPLATE IS READY</div>
<h1>{first} <em>{rest}</em></h1>
<div class="t">Thank you for your purchase! You'll be set up in about 2 minutes.</div>
{shot_html}</div>
<div class="w">
<a class="btn" href="{url}">Get your Notion template<span>&#8594;</span></a>
<div class="u">Link not working? Copy this into your browser:<br><a href="{url}">{url}</a></div>
<div class="lbl">4 QUICK STEPS</div><div class="g">{st}</div>
<div class="lbl">GOOD TO KNOW</div><div class="kn">
<div><b>No Notion account?</b>Create one at notion.com, then open the link again.</div>
<div><b>Desktop + phone</b>Works best on desktop. After duplicating, use it on the Notion app too.</div>
<div><b>For your own use</b>Please don't resell or share this template.</div></div>
</div>
<div class="f"><span>Need help? Message me on Etsy. I reply to every message.</span><span>SystemForge · etsy.com/shop/GetSystemForge</span></div>
</body></html>'''
with tempfile.TemporaryDirectory() as tmp:
    p = os.path.join(tmp, 'd.html')
    open(p, 'w').write(html)
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                    f'--print-to-pdf={os.path.abspath(out)}', 'file://' + p], check=True, capture_output=True)
print('ok', out)
