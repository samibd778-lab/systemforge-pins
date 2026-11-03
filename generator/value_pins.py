"""Value (save-worthy) Pinterest pins, 1000x1500, TOBI style. Plan: marketing/pinterest-trends-2026-11.md
Run: python3 generator/value_pins.py -> pins/value/vp-XX.png"""
import os, subprocess, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
F = R/'generator/remotion/public'
E = R/'canva/v3/etsy/final/sb'; S = R/'shots/hd'
def u(p): return pathlib.Path(p).as_uri()
CSS = f"""@font-face{{font-family:SS;src:url({u(F/'sourceserif700.woff2')})}}@font-face{{font-family:I5;src:url({u(F/'inter500.woff2')})}}@font-face{{font-family:I7;src:url({u(F/'inter700.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1000px;height:1500px;overflow:hidden;position:relative;font-family:I5}}
.k{{font-family:I7;font-size:26px;letter-spacing:4px;text-transform:uppercase}}h1{{font-family:SS;line-height:1.02}}
.img{{position:absolute;overflow:hidden;border-radius:28px;box-shadow:0 30px 70px rgba(0,0,0,.22)}}.img img{{width:100%;display:block}}
.foot{{position:absolute;bottom:44px;left:0;right:0;text-align:center;font-family:I7;font-size:24px;letter-spacing:3px}}"""
def A(kick, title, img, bg='#F6F1E9', ink='#2E2A25', acc='#7A8B6F', num=None, crop_top=0, img_w=860, phone=False):
    """text on top, image card below"""
    n = f'<span style="color:{acc}">{num}</span> ' if num else ''
    w = 520 if phone else img_w
    return f'''<body style="background:{bg};color:{ink}"><div style="position:absolute;left:70px;right:70px;top:90px">
<div class="k" style="color:{acc}">{kick}</div><h1 style="font-size:92px;margin-top:22px">{n}{title}</h1></div>
<div class="img" style="left:{(1000-w)//2}px;width:{w}px;top:{640 if not phone else 560}px;height:{760 if not phone else 860}px;{'border-radius:56px;border:14px solid #1F1D1B' if phone else ''}"><img src="{u(img)}" style="margin-top:-{crop_top}px"></div>
<div class="foot" style="color:{acc}">SYSTEMFORGE · NOTION TEMPLATES</div></body>'''
def B(title, sub, img, ink='#FFFFFF', acc='#E8C3AA'):
    """full-bleed image, dark overlay, big centered text (TOBI)"""
    return f'''<body style="background:url({u(img)}) top center/cover;color:{ink}"><div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(25,32,24,.30),rgba(25,32,24,.78) 55%,rgba(25,32,24,.92))"></div>
<div style="position:absolute;left:80px;right:80px;bottom:200px"><h1 style="font-size:100px">{title}</h1><div style="margin-top:30px;font-size:36px;line-height:1.4;color:{acc};font-family:I7">{sub}</div></div>
<div class="foot" style="color:#D9E2D2">SYSTEMFORGE · NOTION TEMPLATES</div></body>'''
P = {
 'vp-01': A('Notion layout ideas','Notion layout ideas that actually look calm',E/'sb-1-main.png',num='12'),
 'vp-02': B('My aesthetic Notion homepage','Steal this layout: menu, today widget, goals and habits on one page',S/'sb-home.png'),
 'vp-03': A('Habit tracker ideas','The habit tracker I finally stuck to',S/'sbph-habits.png',bg='#E3E8DC',phone=True),
 'vp-04': B('Monthly habit tracker in Notion','5 habits, 2 minutes a day. Your score fills in by itself.',S/'sb-habits.png'),
 'vp-05': A('Notion template ideas','One Notion page for your whole life',E/'sb-3-feature.png',bg='#F1DDCF',acc='#B5714F'),
 'vp-06': B('Productive aesthetic','My Sunday reset in Notion: goals, projects and the week ahead',S/'sb-projects.png'),
 'vp-07': A('Time management aesthetic','The 15-minute weekly plan',S/'wcp-goals-clean.png',bg='#E3E8DC',img_w=900),
 'vp-08': A('Insta post ideas','Plan a whole week of posts in one place',S/'wcp-calendar-clean.png',bg='#F6F1E9',acc='#B5714F',img_w=900),
 'vp-09': B('Free Notion template','Plan a week of content in 15 minutes. Free to download.',S/'wcp-next7-pipeline-clean.png'),
 'vp-10': A('Digital planner template','I switched from a paper planner to this',S/'sbph-mhome.png',bg='#F1DDCF',acc='#B5714F',phone=True),
}
CH = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
out = R/'pins/value'; tmp = R/'pins/value/_t.html'
for k, body in P.items():
    tmp.write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>{body}</html>')
    subprocess.run([CH,'--headless=new','--no-sandbox','--disable-gpu','--hide-scrollbars','--allow-file-access-from-files',
                    '--window-size=1000,1700',f'--screenshot={out/(k+"_full.png")}',tmp.as_uri()],check=True,capture_output=True)
    from PIL import Image
    Image.open(out/(k+'_full.png')).crop((0,0,1000,1500)).save(out/(k+'.png')); os.remove(out/(k+'_full.png'))
tmp.unlink(); print('ok', len(P))
