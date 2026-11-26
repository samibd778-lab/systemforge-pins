"""SystemForge Etsy extra images (2026-11): slots 11-14 + a 12s silent video.
11 how it works (Etsy delivery), 12 all bonus pages, 13 perfect for, 14 good to know.
Usage: python3 generator/v4/listing_extra.py pregnancy
"""
import sys, os, json, asyncio, pathlib, subprocess, base64
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[2]
P = sys.argv[1]
CFG = json.load(open(ROOT/f'generator/v4/products/{P}.json'))
EX = json.load(open(ROOT/'generator/v4/extra.json'))[P]
SCR = ROOT/f'generator/v4/scr/{P}'
OUT = ROOT/f'etsy/{P}/v4'
C = CFG['colors']
def u(n): return 'data:image/png;base64,'+base64.b64encode((SCR/n).read_bytes()).decode()
src = open(ROOT/'generator/v4/listing_v4.py').read()
BASE = src.split('BASE = f"""')[1].split('"""')[0].replace('{{','{').replace('}}','}')
for k,v in C.items(): BASE = BASE.replace("{C['%s']}" % k, v)
hero = CFG['pages'][0][1]; bonus = [d for k,d in CFG['pages'] if k=='bonus'][0]
NAME = hero['title']

def laptop(img, x, y, w):
    return f'<div class="lap" style="left:{x}px;top:{y}px;width:{w}px"><div class="bez"><img src="{u(img)}"></div><div class="base"></div></div>'

def step(n, t, s):
    return f'''<div style="display:flex;gap:46px;align-items:flex-start;margin-top:110px">
<div style="flex:none;width:150px;height:150px;border-radius:75px;background:{C['accent']};color:#fff;display:grid;place-items:center;font:600 80px Gelasio">{n}</div>
<div><div style="font:600 74px/1.2 Inter">{t}</div><div class="sub" style="margin-top:16px;font-size:54px">{s}</div></div></div>'''

def p_how():
    return f'''<div style="position:absolute;top:150px;left:150px;width:1250px">
<div class="kick">How it works</div><h2 style="margin-top:24px">Ready in 5 minutes</h2>
{step(1,'Download the PDF','Find it in your Etsy purchases right after you buy.')}
{step(2,'Click the link inside','Then click Duplicate in the top right corner.')}
{step(3,'Open Start here','Follow the short steps and make it yours.')}</div>
{laptop('hero.png',1430,620,1150)}
<div class="chips" style="position:absolute;left:1430px;width:1150px;top:1480px;justify-content:center;flex-wrap:nowrap"><div class="chip" style="white-space:nowrap"><i>✓</i>Instant download</div><div class="chip" style="white-space:nowrap"><i>✓</i>No design skills needed</div></div>'''

def p_pages():
    n = len(bonus.get('all_pages') or [f'pdf-{i}.png' for i in range(1,8)])
    pages = [f'pdf-{i}.png' for i in range(1,n+1) if (SCR/f'pdf-{i}.png').exists()]
    W=540; gap=60; rows=[pages[:4],pages[4:]]
    html=''
    for r,row in enumerate(rows):
        tot=len(row)*W+(len(row)-1)*gap; x0=(2700-tot)//2
        for k,p in enumerate(row):
            html+=f'<img src="{u(p)}" style="position:absolute;width:{W}px;left:{x0+k*(W+gap)}px;top:{520+r*760}px;box-shadow:0 24px 50px rgba(60,40,30,.22);border-radius:8px">'
    return f'''<div style="position:absolute;top:110px;left:0;right:0;text-align:center">
<div class="kick">Included bonus</div><h2 style="margin-top:24px">{bonus['title']}: all {len(pages)} pages</h2>
<div class="sub" style="margin-top:18px">Read it on screen or print it at home.</div></div>{html}'''

def card(items, mark='✓'):
    return ''.join(f'<li style="padding:30px 0;border-bottom:3px solid {C["line"]};display:flex;gap:30px"><span style="color:{C["accent"]};flex:none">{mark}</span><span>{i}</span></li>' for i in items)

def p_for():
    return f'''<div style="position:absolute;top:150px;left:150px;width:1300px">
<div class="kick">Who it’s for</div><h2 style="margin-top:24px">Perfect for</h2>
<ul style="list-style:none;margin-top:40px;font:500 64px/1.3 Inter">{card(EX['for'])}</ul></div>
{laptop(EX.get('for_scr','inside.png'),1550,600,1030)}'''

def p_know():
    items = ['You need a Notion account. Create one in a minute at notion.com.',
             'Works on desktop, tablet and phone.',
             'Digital download. Nothing will be shipped.',
             'Sample rows show how it works. Delete them when you’re ready.',
             'For personal use. Please don’t resell or share it.']
    if EX.get('disc'): items.append(EX['disc'])
    return f'''<div style="position:absolute;top:140px;left:0;right:0;text-align:center">
<div class="kick">Before you buy</div><h2 style="margin-top:24px">Good to know</h2></div>
<ul style="position:absolute;left:420px;right:420px;top:470px;list-style:none;font:500 60px/1.3 Inter">{card(items,'•')}</ul>
<div class="foot">Questions? Send us a message on Etsy.</div>'''

async def main():
    async with async_playwright() as pw:
        exe = next(p for p in ['/opt/pw-browsers/chromium-1243/chrome-linux64/chrome','/opt/pw-browsers/chromium-1194/chrome-linux/chrome'] if os.path.exists(p))
        b = await pw.chromium.launch(executable_path=exe)
        pg = await b.new_page(viewport={'width':2700,'height':2025})
        start = len(CFG['pages'])+1
        for n,(slug,fn) in enumerate([('how-it-works',p_how),('bonus-pages',p_pages),('perfect-for',p_for),('good-to-know',p_know)], start):
            await pg.set_content('<html><body>'+BASE+f'<div class="cv" style="left:0">{fn()}</div></body></html>')
            await pg.wait_for_timeout(300)
            f = OUT/f'{n:02d}-{slug}.jpg'
            await pg.screenshot(path=str(f), type='jpeg', quality=88); print(f.name)
        await b.close()
    # video: 12s silent, 1920x1440, slow zoom on 5 listing images with crossfades
    imgs = sorted(OUT.glob('0[1-9]-*.jpg'))
    pick = [imgs[0]] + [i for i in imgs if 'inside' not in i.name and 'hero' not in i.name][:4]
    vid = OUT/'video.mp4'; d=2.8; fade=0.5
    args=['ffmpeg','-y','-loglevel','error']
    for i in pick: args += ['-i',str(i)]
    fc='';
    for k in range(len(pick)):
        fc+=f"[{k}:v]scale=3840:2880,zoompan=z='min(zoom+0.0009,1.08)':d={int(d*30)}:s=1920x1440:fps=30,setsar=1[v{k}];"
    last='v0'; off=d-fade
    for k in range(1,len(pick)):
        fc+=f"[{last}][v{k}]xfade=transition=fade:duration={fade}:offset={off:.2f}[x{k}];"; last=f'x{k}'; off+=d-fade
    args += ['-filter_complex',fc.rstrip(';'),'-map',f'[{last}]','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(vid)]
    subprocess.run(args, check=True)
    print('video', vid.name, round(off+fade,1),'s')
asyncio.run(main())
