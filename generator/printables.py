"""Free printables (Gumroad $0 lead magnets). Clean, ink-light US Letter pages + a last page about the matching
Notion template (Gumroad link). Research: research/pinclicks-top-pins-2026-11-12.md ("free printable" wins).
Run: python3 generator/printables.py grocery  -> dl/free/<name>.pdf, dl/free/<name>-p<N>.png, pins/v5/<pin>.png"""
import base64, os, subprocess, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, 'generator', 'remotion', 'public')
OUT = os.path.join(ROOT, 'dl', 'free'); os.makedirs(OUT, exist_ok=True)
FONTS = (f"@font-face{{font-family:GV;src:url(file://{F}/greatvibes400.woff2)}}"
         f"@font-face{{font-family:PF;font-weight:700;src:url(file://{F}/playfair700.woff2)}}"
         f"@font-face{{font-family:IN;font-weight:500;src:url(file://{F}/inter500.woff2)}}"
         f"@font-face{{font-family:IN;font-weight:700;src:url(file://{F}/inter700.woff2)}}")
CSS = FONTS + """
@page{size:8.5in 11in;margin:0}*{box-sizing:border-box;margin:0;padding:0}
body{font-family:IN;color:#2E2A25;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:8.5in;height:11in;padding:.55in .6in .45in;position:relative;page-break-after:always;background:#fff;overflow:hidden}
.kick{font:700 10px IN;letter-spacing:.32em;color:var(--acc);text-align:center}
h1{font:400 64px/1 GV;text-align:center;margin:6px 0 2px;color:#2E2A25}
.meta{display:flex;justify-content:center;gap:28px;font:500 11px IN;color:#6F665B;margin:6px 0 18px}
.meta span b{display:inline-block;width:1.3in;border-bottom:1px solid #CFC6BA;margin-left:6px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px 18px}
.box{border:1.2px solid var(--line);border-radius:14px;padding:10px 14px 8px}
.box h3{font:700 12px IN;letter-spacing:.14em;text-transform:uppercase;color:var(--acc);margin-bottom:4px;display:flex;gap:8px;align-items:center}
.row{display:flex;align-items:flex-end;gap:9px;height:24px;border-bottom:1px solid #EDE6DC}
.cb{width:12px;height:12px;border:1.3px solid #B9AFA2;border-radius:3px;margin-bottom:5px;flex:none}
.foot{position:absolute;left:.6in;right:.6in;bottom:.32in;display:flex;justify-content:space-between;font:700 8.5px IN;letter-spacing:.2em;color:#A79C8E}
table.wk{width:100%;border-collapse:separate;border-spacing:0;border:1.2px solid var(--line);border-radius:14px;overflow:hidden}
.wk th{font:700 10px IN;letter-spacing:.16em;text-transform:uppercase;color:var(--acc);background:var(--tint);padding:9px 10px;text-align:left}
.wk td{border-top:1px solid #EDE6DC;height:1.12in;padding:7px 10px;vertical-align:top;font:700 11px IN}
.wk td+td{border-left:1px solid #EDE6DC}
.up h2{font:700 30px/1.15 PF;text-align:center;margin:4px 0 10px}
.up p{font:500 13px/1.5 IN;color:#6F665B;text-align:center;margin:0 auto 16px;width:5.6in}
.up img{width:100%;border:1px solid var(--line);border-radius:12px}
.feat{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:16px 0}
.feat div{background:var(--tint);border-radius:12px;padding:12px 14px;font:500 12.5px/1.45 IN}
.feat b{display:block;font:700 12.5px IN;margin-bottom:2px}
.cta{display:block;text-align:center;background:var(--acc);color:#fff;text-decoration:none;font:700 15px IN;padding:14px;border-radius:12px;margin-top:6px}
.how{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:18px}
.how div{border:1.2px solid var(--line);border-radius:12px;padding:10px 12px;font:500 11.5px/1.45 IN;color:#6F665B}
.how b{display:block;font:700 22px PF;color:var(--acc)}
"""

def b64(p): return 'data:image/jpeg;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
def lines(n): return ''.join('<div class="row"><span class="cb"></span></div>' for _ in range(n))
def foot(left): return f'<div class="foot"><span>{left}</span><span>SYSTEMFORGE · FREE PRINTABLE</span></div>'

SETS = {
 'grocery': dict(
   file='Free-Printable-Grocery-List', acc='#5E7F5A', tint='#EEF3EA', line='#D9E3D3',
   product='Meal Planner', url='https://getsystemforge.gumroad.com/l/meal-planner?utm_source=gumroad&utm_medium=free-pdf&utm_campaign=grocery-list',
   shot='shots/hd3/meal-grocery.jpg', shot_box=(0, 0, 1350, 680)),
}

def pages(k, s):
    aisles = [('🥦', 'Produce', 9), ('🥛', 'Dairy & eggs', 7), ('🍗', 'Meat & fish', 6), ('🥖', 'Bakery', 4),
              ('🥫', 'Pantry', 9), ('🧊', 'Frozen', 7), ('🧃', 'Drinks', 6), ('🧻', 'Household', 4)]
    col = lambda items: '<div style="display:grid;gap:14px">' + ''.join(
        f'<div class="box"><h3><span>{e}</span>{t}</h3>{lines(n)}</div>' for e, t, n in items) + '</div>'
    p1 = (f'<section class="pg"><div class="kick">FREE PRINTABLE</div><h1>Grocery List</h1>'
          '<div class="meta"><span>Week of<b></b></span><span>Store<b></b></span><span>Budget $<b style="width:.8in"></b></span></div>'
          f'<div class="grid">{col(aisles[:4])}{col(aisles[4:])}</div>{foot("SORTED BY AISLE")}</section>')
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    p2 = ('<section class="pg"><div class="kick">FREE PRINTABLE</div><h1>Weekly Meal Plan</h1>'
          '<div class="meta"><span>Week of<b></b></span></div>'
          '<div style="display:grid;grid-template-columns:1fr 2.1in;gap:16px">'
          '<table class="wk"><tr><th style="width:.75in"></th><th>Breakfast</th><th>Lunch</th><th>Dinner</th></tr>'
          + ''.join(f'<tr><td style="color:var(--acc)">{d}</td><td></td><td></td><td></td></tr>' for d in days) + '</table>'
          f'<div style="display:grid;gap:14px;align-content:start"><div class="box"><h3>To buy</h3>{lines(20)}</div>'
          f'<div class="box"><h3>Prep ahead</h3>{lines(7)}</div></div></div>{foot("PLAN, THEN SHOP")}</section>')
    crop = Image.open(os.path.join(ROOT, s['shot'])).crop(s['shot_box']).convert('RGB')
    tmp = os.path.join(OUT, '_shot.jpg'); crop.save(tmp, quality=92)
    p3 = ('<section class="pg up"><div class="kick">HOW TO USE IT</div>'
          '<div class="how" style="margin-top:12px"><div><b>1</b>Plan your week on the meal plan page.</div>'
          '<div><b>2</b>Write what you need under the right aisle.</div><div><b>3</b>Tick each item in the store. Done.</div></div>'
          f'<div class="kick" style="margin-top:6px">WANT IT TO SORT ITSELF?</div><h2>{s["product"]} for Notion</h2>'
          '<p>The same idea in Notion: plan the next 7 days, and your grocery list sorts itself by aisle, with quantity and price.</p>'
          f'<img src="{b64(tmp)}">'
          '<div class="feat"><div><b>Grocery list by aisle</b>Tick Got it in the store and the item leaves the list.</div>'
          '<div><b>The next 7 days</b>Breakfast, lunch and dinner. Tick Cooked when it is done.</div>'
          '<div><b>Your recipes</b>Time, rating and tags on every card. Favorites first.</div>'
          '<div><b>On your phone</b>Open it in the Notion app at the store.</div></div>'
          f'<a class="cta" href="{s["url"]}">See the {s["product"]} for Notion →</a>{foot("NEXT STEP")}</section>')
    os.remove(tmp)
    return [p1, p2, p3]

def build(k):
    s = SETS[k]
    css = CSS.replace('var(--acc)', s['acc']).replace('var(--tint)', s['tint']).replace('var(--line)', s['line'])
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(pages(k, s))}</body></html>"
    hp = os.path.join(OUT, f'_{k}.html'); open(hp, 'w').write(html)
    pdf = os.path.join(OUT, s['file'] + '.pdf')
    js = (f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();"
          f"await p.goto('file://{hp}');await p.waitForTimeout(800);await p.pdf({{path:'{pdf}',width:'8.5in',height:'11in',printBackground:true}});await b.close();}})()")
    subprocess.run(['node', '-e', js], check=True); os.remove(hp)
    subprocess.run(['pdftoppm', '-r', '200', '-png', pdf, os.path.join(OUT, s['file'] + '-p')], check=True)
    print(pdf)

if __name__ == '__main__':
    build(sys.argv[1])
