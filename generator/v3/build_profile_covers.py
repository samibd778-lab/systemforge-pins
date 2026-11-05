"""Pinterest profile covers (1920x1080) for both SystemForge accounts, real HD screenshots only.
Run: python3 generator/v3/build_profile_covers.py -> brand/profile/cover-etsy.jpg, cover-gumroad.jpg"""
import os, subprocess
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'brand', 'profile'); os.makedirs(OUT, exist_ok=True)
F = os.path.join(ROOT, 'generator', 'remotion', 'public')
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
S = os.path.join(ROOT, 'shots', 'hd')

def crop(name, box, w, out):
    im = Image.open(os.path.join(S, name + '.png')).convert('RGB').crop(box)
    im = im.resize((w, int(w * im.height / im.width)), Image.LANCZOS)
    p = os.path.join(OUT, '_' + out + '.jpg'); im.save(p, quality=92); return 'file://' + p

sb = crop('sb-home', (0, 1040, 2170, 2300), 1400, 'sb')
ccs = crop('ccs-calendar', (0, 200, 2880, 1800), 1400, 'ccs')
fco = crop('fco-money-flow', (0, 200, 2880, 1800), 1400, 'fco')
ph = crop('sbph-mhome', (0, 70, 1080, 1975), 500, 'ph')

FONTS = (f"@font-face{{font-family:Serif;font-weight:700;src:url(file://{F}/sourceserif700.woff2)}}"
         f"@font-face{{font-family:Inter;font-weight:500;src:url(file://{F}/inter500.woff2)}}"
         f"@font-face{{font-family:Inter;font-weight:700;src:url(file://{F}/inter700.woff2)}}")

def page(v):
    dark = v['dark']
    bg, ink, sub, chipbg, chipink, acc = (('#2F4232', '#F5EFE6', '#D5DCCB', 'rgba(245,239,230,.12)', '#F5EFE6', '#E3B796') if dark
                                          else ('#F3EDE4', '#2B2723', '#6F665B', '#FFFFFF', '#3E4A38', '#B9735A'))
    chips = ''.join(f'<span>{c}</span>' for c in v['chips'])
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:960px;height:540px;overflow:hidden}}
body{{background:{bg};font-family:Inter;color:{ink};position:relative}}
.blob{{position:absolute;border-radius:50%;filter:blur(2px)}}
.b1{{width:520px;height:520px;right:-120px;top:-160px;background:{'#3B5240' if dark else '#E3E8DC'}}}
.b2{{width:300px;height:300px;left:-90px;bottom:-140px;background:{'#283A2B' if dark else '#EADFD2'}}}
.txt{{position:absolute;left:60px;top:0;bottom:0;width:410px;display:flex;flex-direction:column;justify-content:center}}
.k{{font-weight:700;font-size:11px;letter-spacing:.18em;color:{acc}}}
h1{{font-family:Serif;font-weight:700;font-size:44px;line-height:1.05;margin-top:14px;letter-spacing:-.01em}}
h1 em{{font-style:normal;color:{acc}}}
.s{{margin-top:14px;font-weight:500;font-size:14.5px;line-height:1.5;color:{sub}}}
.chips{{margin-top:18px;display:flex;flex-wrap:wrap;gap:7px}}
.chips span{{background:{chipbg};color:{chipink};border-radius:99px;padding:6px 12px;font-weight:700;font-size:11px;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
.ft{{margin-top:20px;font-weight:700;font-size:11.5px;color:{sub}}}
.win{{position:absolute;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 22px 50px rgba(0,0,0,{'.45' if dark else '.18'})}}
.win .bar{{height:16px;background:#EDE7DF;display:flex;gap:4px;align-items:center;padding:0 8px}}
.win .bar i{{width:6px;height:6px;border-radius:50%;background:#D3C8BB}}
.win img{{display:block;width:100%}}
.w1{{width:380px;left:545px;top:44px;transform:rotate(3deg)}}
.w2{{width:380px;left:500px;top:300px;transform:rotate(-3deg)}}
.w3{{width:420px;left:505px;top:150px;z-index:3}}
.w1 .vp,.w2 .vp{{height:210px;overflow:hidden}}.w3 .vp{{height:255px;overflow:hidden}}
.ph{{position:absolute;left:818px;top:270px;width:118px;height:236px;border-radius:20px;background:#111;padding:5px;z-index:4;box-shadow:0 18px 40px rgba(0,0,0,.35)}}
.ph div{{width:100%;height:100%;border-radius:15px;overflow:hidden;background:#fff}}.ph img{{width:100%;display:block}}
</style></head><body><div class="blob b1"></div><div class="blob b2"></div>
<div class="txt"><div class="k">{v['kicker']}</div><h1>{v['title']}</h1><div class="s">{v['sub']}</div>
<div class="chips">{chips}</div><div class="ft">{v['foot']}</div></div>
<div class="win w1"><div class="bar"><i></i><i></i><i></i></div><div class="vp"><img src="{v['back']}"></div></div>
<div class="win w2"><div class="bar"><i></i><i></i><i></i></div><div class="vp"><img src="{v['mid']}"></div></div>
<div class="win w3"><div class="bar"><i></i><i></i><i></i></div><div class="vp"><img src="{sb}"></div></div>
<div class="ph"><div><img src="{ph}"></div></div>
</body></html>'''

V = {
 'etsy': dict(dark=False, kicker='SYSTEMFORGE SHOP · NOTION TEMPLATES', title='Aesthetic Notion templates to organize your <em>whole life</em>',
              sub='Calm Notion dashboards for your goals, habits, journal, content and clients.',
              chips=['Second brain', 'Habit tracker', 'Digital planner', 'Content calendar', 'Client tracker'],
              foot='Instant download on Etsy · Set up in 5 minutes', back=ccs, mid=fco),
 'gumroad': dict(dark=True, kicker='SYSTEMFORGE · NOTION TEMPLATES', title='Calm Notion templates for <em>life, work and content</em>',
              sub='One clear page for your goals, habits, projects, posts and clients.',
              chips=['Life planner', 'Notion dashboard', 'Habit tracker', 'Content planner', 'Freelancer CRM'],
              foot='Instant access · Works on desktop and phone', back=fco, mid=ccs),
}
for k, v in V.items():
    h = os.path.join(OUT, f'_{k}.html'); open(h, 'w').write(page(v))
    png = os.path.join(OUT, f'_{k}.png')
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=2', '--window-size=960,700', f'--screenshot={png}', 'file://' + h], check=True, capture_output=True)
    Image.open(png).convert('RGB').crop((0, 0, 1920, 1080)).save(os.path.join(OUT, f'cover-{k}.jpg'), quality=92)
    print('ok', k)
