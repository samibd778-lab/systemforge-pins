"""Etsy delivery PDF (US Letter) rendered from HTML with headless Chrome, so Inter and the link button work.
Usage: python3 generator/etsy_pdf.py "<Product name>" "<notion.site link>" "<step 4 text>" out.pdf
Only Etsy links in the footer (no off-Etsy links in Etsy files)."""
import os, subprocess, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles'))
from pins_v2 import FONT_CSS  # noqa: E402

CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
name, url, step4, out = sys.argv[1:5]
steps = [('Open the link', 'Click the green button above. It opens in your browser.'),
         ('Log in to Notion', 'Use your Notion account, or create one in a minute.'),
         ('Click Duplicate', 'Top right corner. The template is copied into your workspace.'),
         ('Open "Start here"', step4)]
st = ''.join(f'<div class="s"><div class="n">{i + 1}</div><div><b>{a}</b><p>{b}</p></div></div>' for i, (a, b) in enumerate(steps))
html = f'''<!doctype html><html><head><meta charset="utf-8"><style>{FONT_CSS}
@page{{size:Letter;margin:0}}*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:8.5in;height:10.95in;overflow:hidden}}body{{background:#F6F1E9;font-family:InterW;color:#2E2A25;position:relative;overflow:hidden}}
.c1{{position:absolute;width:3in;height:3in;border-radius:50%;background:#E3E8DC;right:-1in;top:-1.2in}}
.c2{{position:absolute;width:3in;height:3in;border-radius:50%;background:#EFDCCB;left:-1.3in;bottom:-1.5in}}
.w{{position:absolute;left:.75in;right:.75in;top:.6in}}
.logo{{display:flex;align-items:center;gap:12px;font-weight:700;font-size:13px}}
.logo i{{width:48px;height:48px;border-radius:50%;background:#7A8B6F;color:#FFFDF9;font-style:normal;display:flex;align-items:center;justify-content:center;font-size:17px}}
.k{{margin-top:44px;font-weight:700;font-size:11px;letter-spacing:1.5px;color:#7A8B6F}}
h1{{margin-top:8px;font-weight:700;font-size:38px;letter-spacing:-1px}}
.t{{margin-top:8px;font-weight:500;font-size:13px;color:#5C554C}}
a.btn{{display:block;margin-top:24px;background:#7A8B6F;color:#FFFDF9;text-decoration:none;text-align:center;border-radius:14px;padding:18px;font-weight:700;font-size:19px}}
.u{{margin-top:10px;text-align:center;font-weight:500;font-size:8.5px;color:#5C554C;line-height:1.6}}.u a{{color:#2E2A25}}
.s{{margin-top:12px;background:#FFFDF9;border-radius:12px;padding:14px 18px;display:flex;gap:18px;align-items:center}}
.n{{flex:none;width:36px;height:36px;border-radius:50%;background:#E3E8DC;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;color:#5C554C}}
.s b{{font-size:14px}}.s p{{margin-top:3px;font-weight:500;font-size:11px;color:#5C554C}}
h3{{margin-top:22px;font-size:13px}}ul{{margin:8px 0 0 18px;font-weight:500;font-size:10.5px;line-height:1.8;color:#5C554C}}
.h{{margin-top:22px;font-weight:700;font-size:12px;color:#7A8B6F}}.f{{margin-top:6px;font-weight:500;font-size:9.5px;color:#5C554C}}
</style></head><body><div class="c1"></div><div class="c2"></div><div class="w">
<div class="logo"><i>SF</i>SystemForge</div>
<div class="k">YOUR TEMPLATE IS READY</div><h1>{name}</h1>
<div class="t">Thank you for your purchase! Here's how to get started in about 2 minutes.</div>
<a class="btn" href="{url}">Click here to get your Notion template &#8250;</a>
<div class="u">Link not working? Copy this into your browser:<br><a href="{url}">{url}</a></div>
{st}
<h3>Good to know</h3><ul>
<li>No Notion account yet? Create one at notion.com, then open the link again.</li>
<li>Works best on desktop. After duplicating, you can use it on the Notion mobile app too.</li>
<li>This template is for your own use. Please don't resell or share it.</li></ul>
<div class="h">Need help? Message me on Etsy. I reply to every message.</div>
<div class="f">SystemForge &nbsp;·&nbsp; etsy.com/shop/GetSystemForge</div>
</div></body></html>'''
with tempfile.TemporaryDirectory() as tmp:
    p = os.path.join(tmp, 'd.html')
    open(p, 'w').write(html)
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                    f'--print-to-pdf={os.path.abspath(out)}', 'file://' + p], check=True, capture_output=True)
print('ok', out)
