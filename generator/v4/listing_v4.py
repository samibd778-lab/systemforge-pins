"""SystemForge listing images v4 (2026-11): competitor style.
Big serif title + big real screenshot in a laptop + a zoom card. 10 images, 2700x2025 (Etsy 4:3).
Usage: python3 generator/v4/listing_v4.py pregnancy
"""
import sys, os, json, asyncio, pathlib
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[2]
P = sys.argv[1]
CFG = json.load(open(ROOT/f'generator/v4/products/{P}.json'))
SCR = ROOT/f'generator/v4/scr/{P}'
OUT = ROOT/f'etsy/{P}/v4'; OUT.mkdir(parents=True, exist_ok=True)
C = CFG['colors']
import base64
def u(n): return 'data:image/png;base64,'+base64.b64encode((SCR/n).read_bytes()).decode()

BASE = f"""
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:100vw;height:100vh;background:{C['bg']};font-family:Inter;color:{C['ink']};position:relative;overflow:hidden}}
.cv{{position:absolute;top:0;width:2700px;height:2025px}}
.kick{{font:600 38px Inter;letter-spacing:9px;text-transform:uppercase;color:{C['accent']}}}
.pill{{display:inline-flex;align-items:center;gap:18px;background:#fff;border-radius:60px;padding:16px 40px;font:600 40px Inter;color:{C['ink']};box-shadow:0 6px 20px rgba(0,0,0,.06)}}
.pill b{{display:inline-grid;place-items:center;width:52px;height:52px;border:4px solid {C['ink']};border-radius:10px;font:800 34px Gelasio}}
h1{{font:500 150px/1.05 Gelasio;letter-spacing:-2px}}
h2{{font:500 120px/1.08 Gelasio;letter-spacing:-1px}}
.sub{{font:400 52px/1.4 Inter;color:{C['muted']}}}
.lap{{position:absolute}}
.lap .bez{{background:#1c1c1e;border-radius:44px 44px 0 0;padding:34px 34px 40px}}
.lap .bez img{{display:block;width:100%;border-radius:6px}}
.lap .base{{height:46px;margin:0 -110px;background:linear-gradient(#d9d9dc,#b9b9bd);border-radius:0 0 40px 40px;position:relative}}
.lap .base:before{{content:'';position:absolute;left:50%;top:0;width:340px;height:16px;margin-left:-170px;background:#a4a4a8;border-radius:0 0 16px 16px}}
.lap{{filter:drop-shadow(0 40px 60px rgba(60,40,30,.25))}}
.zoom{{position:absolute;background:#fff;border-radius:30px;padding:26px;box-shadow:0 30px 80px rgba(60,40,30,.28);border:5px solid {C['accent']}}}
.zoom img{{display:block;width:100%;border-radius:10px}}
.chips{{display:flex;flex-wrap:wrap;gap:22px}}
.chip{{background:#fff;border-radius:60px;padding:20px 38px;font:600 44px Inter;box-shadow:0 6px 20px rgba(0,0,0,.06)}}
.chip i{{color:{C['accent']};font-style:normal;margin-right:14px}}
.foot{{position:absolute;bottom:50px;left:0;right:0;text-align:center;font:500 34px Inter;color:{C['muted']}}}
</style>"""

def laptop(img, x, y, w):
    return f'<div class="lap" style="left:{x}px;top:{y}px;width:{w}px"><div class="bez"><img src="{u(img)}"></div><div class="base"></div></div>'

def page_hero(d):
    return f"""<div style="position:absolute;top:100px;left:0;right:0;text-align:center">
<div class="pill"><b>N</b>Notion Template</div>
<h1 style="margin-top:40px">{d['title']}</h1>
<div class="sub" style="margin-top:22px">{d['sub']}</div>
<div class="chips" style="justify-content:center;margin-top:40px">{''.join(f'<div class="chip"><i>✓</i>{c}</div>' for c in d['chips'])}</div></div>
{laptop('hero.png',500,800,1700)}"""

def page_inside(d):
    items=''.join(f'<li><span style="color:{C["accent"]};margin-right:22px">✓</span>{i}</li>' for i in d['items'])
    return f"""<div style="position:absolute;top:150px;left:150px;width:900px">
<div class="kick">What you get</div><h2 style="margin-top:24px">{d['title']}</h2>
<ul style="list-style:none;margin-top:50px;font:500 48px/1.25 Inter">{items}</ul></div>
<style>li{{padding:15px 0;border-bottom:2px solid {C['line']}}}</style>
{laptop('inside.png',1150,520,1430)}
<div class="chips" style="position:absolute;left:1150px;width:1430px;top:1650px;justify-content:center">{''.join(f'<div class="chip">{c}</div>' for c in d['chips'])}</div>"""

def page_feature(d, i):
    left = i % 2 == 1
    lx = 230 if left else 2700-230-1700
    zw = d.get('zw',1200); zx = 2700-90-zw if left else 90
    return f"""<div style="position:absolute;top:110px;left:0;right:0;text-align:center">
<div class="kick">{d['kick']}</div><h2 style="margin-top:24px">{d['title']}</h2>
<div class="sub" style="margin-top:20px">{d['sub']}</div></div>
{laptop(d['scr'],lx,620,1700)}
<div class="zoom" style="left:{zx}px;top:{d.get('zy',1000)}px;width:{zw}px"><img src="{u(d['zoom'])}"></div>"""

def page_thumb(d):
    return f"""<div style="position:absolute;top:90px;left:0;right:0;text-align:center">
<div class="pill"><b>N</b>Notion Template</div>
<h1 style="margin-top:40px;font-size:128px">{d['thumb_title']}</h1></div>
{laptop('hero.png',230,560,1100)}"""

def page_bonus(d):
    pages=d['pages']
    imgs=''.join(f'<img src="{u(p)}" style="position:absolute;width:640px;left:{1300+k*330}px;top:{560+[60,0,60][k]}px;transform:rotate({[-6,0,6][k]}deg);box-shadow:0 30px 60px rgba(60,40,30,.25);border-radius:8px;z-index:{[1,3,2][k]}">' for k,p in enumerate(pages))
    items=''.join(f'<li><span style="color:{C["accent"]};margin-right:22px">✓</span>{i}</li>' for i in d['items'])
    return f"""<div style="position:absolute;top:170px;left:150px;width:1080px">
<div class="kick">Included bonus</div><h2 style="margin-top:24px">{d['title']}</h2>
<div class="sub" style="margin-top:26px">{d['sub']}</div>
<ul style="list-style:none;margin-top:46px;font:500 46px/1.25 Inter">{items}</ul></div>
<style>li{{padding:14px 0;border-bottom:2px solid {C['line']}}}</style>{imgs}
<div class="foot">{d.get('note','')}</div>"""

async def main():
    out_g = ROOT/f'dl/{P}/v4'; out_g.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as pw:
        exe = next(p for p in ['/opt/pw-browsers/chromium-1243/chrome-linux64/chrome','/opt/pw-browsers/chromium-1194/chrome-linux/chrome'] if os.path.exists(p))
        b = await pw.chromium.launch(executable_path=exe)
        for mode,(W,H),outdir in [('etsy',(2700,2025),OUT),('gumroad',(3600,2025),out_g)]:
            pg = await b.new_page(viewport={'width':W,'height':H})
            for n,(kind,d) in enumerate(CFG['pages'],1):
                body = {'hero':page_hero,'inside':page_inside,'bonus':page_bonus}.get(kind)
                inner = body(d) if body else page_feature(d,n)
                html = BASE + f'<div class="cv" style="left:{(W-2700)//2}px">{inner}</div>'
                await pg.set_content('<html><body>'+html+'</body></html>')
                await pg.wait_for_timeout(300)
                f = outdir/f"{n:02d}-{d.get('slug',kind)}.jpg"
                await pg.screenshot(path=str(f), type='jpeg', quality=88); print(mode, f.name)
            await pg.close()
        pg = await b.new_page(viewport={'width':1560,'height':1560})
        hero = CFG['pages'][0][1]
        await pg.set_content('<html><body>'+BASE+f'<div class="cv" style="left:0;width:1560px;height:1560px">{page_thumb(hero)}</div></body></html>')
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=str(out_g/'thumb.jpg'), type='jpeg', quality=90); print('thumb')
        await b.close()
asyncio.run(main())
