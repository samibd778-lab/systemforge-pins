"""Pins in the style of the top Pinterest pins for our keywords (PinClicks, 2026-11-12):
the template page itself fills the pin (no laptop scene), light background, big script or serif keyword title,
one true promise line. Research: research/pinclicks-top-pins-2026-11-12.md
Usage: python3 generator/v3/top_pins.py [pin ids] -> pins/v5/<id>.png (2000x3000)"""
import os, subprocess, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import mini_listing as M  # noqa: E402
B = M.L.B
F = os.path.join(ROOT, 'generator', 'remotion', 'public')
HD = os.path.join(ROOT, 'shots', 'hd')
OUT = os.path.join(ROOT, 'pins', 'v5'); TMP = os.path.join(OUT, '_tmp'); os.makedirs(TMP, exist_ok=True)
INK, MUT = '#2B2723', '#6A625A'
FONTS = ("<style>"
         f"@font-face{{font-family:GV;src:url(file://{F}/greatvibes400.woff2)}}"
         f"@font-face{{font-family:PF;font-weight:700;src:url(file://{F}/playfair700.woff2)}}"
         f"@font-face{{font-family:Inter;font-weight:500;src:url(file://{F}/inter500.woff2)}}"
         f"@font-face{{font-family:Inter;font-weight:700;src:url(file://{F}/inter700.woff2)}}"
         "body{margin:0}</style>")

# style a = script title + 2 page crops; style b = big serif title band + 1 large crop + bonus badge
PINS = {
 'habit-a1': dict(p='habit', style='a', kicker='NOTION TEMPLATE', title='Habit Tracker',
                  sub='One row a day. Tick what you did and your score fills in by itself.',
                  crops=[('habit-week', (0, 0, 640, 515)), ('habit-monthly', (0, 0, 640, 605))]),
 'habit-b1': dict(p='habit', style='b', title='MONTHLY HABIT TRACKER', kicker='for Notion',
                  sub='A bar for every habit, your best habit and your perfect days.', badge='Bonus PDF:\n30-Day Habit Reset',
                  crops=[('habit-monthly', (0, 0, 820, 605)), ('habit-week', (560, 0, 1380, 683))]),
 'habit-a2': dict(p='habit', style='a', kicker='DAILY HABIT TRACKER', title='Never miss twice',
                  sub='Six habits, one row a day. Busy day? Do the tiny version and still tick it.',
                  crops=[('habit-plan', (0, 0, 700, 470)), ('habit-week', (560, 170, 1380, 560))]),
 'budget-a1': dict(p='budget', style='a', kicker='NOTION BUDGET TEMPLATE', title='Monthly Budget',
                   sub='See what you spent, what is left, and if you are on track.',
                   crops=[('budget-categories', (0, 0, 680, 540)), ('budget-bills', (0, 0, 680, 420))]),
 'budget-b1': dict(p='budget', style='b', title='MONTHLY BUDGET PLANNER', kicker='for Notion',
                   sub='Every category, every bill, every savings goal.', badge='Bonus PDF:\nMoney Reset in 7 Days',
                   crops=[('budget-categories', (0, 0, 860, 540)), ('budget-bills', (0, 0, 860, 420))]),
 'budget-a2': dict(p='budget', style='a', kicker='BUDGET PLANNER TEMPLATE', title='Savings Goals',
                   sub='Each goal shows how much to save every month to hit it on time.',
                   crops=[('budget-savings', (0, 0, 1000, 297)), ('budget-transactions', (0, 0, 680, 587))]),
}


def crop(name, box, w, maxh=10**6):
    x0, y0, x1, y1 = box
    y1 = min(y1, y0 + int(maxh * (x1 - x0) / w))
    box = (x0, y0, x1, y1)
    im = Image.open(os.path.join(HD, name + '.jpg')).convert('RGB').crop(box)
    p = os.path.join(TMP, f'{name}-{box[0]}-{box[2]}.jpg'); im.save(p, quality=93)
    return p, round(im.height * w / im.width)


def card(name, box, w, maxh=10**6):
    p, h = crop(name, box, w, maxh)
    return (f'<div style="width:{w}px;height:{h}px;margin:0 auto 26px;border-radius:18px;overflow:hidden;'
            f'background:#fff url(file://{p}) 0 0/{w}px {h}px no-repeat;box-shadow:0 10px 30px rgba(60,40,20,.16);border:1px solid #E7E1D8"></div>')


def html(s):
    pr = M.PROD[s['p']]; c, acc = pr['color'], pr['accent']
    if s['style'] == 'a':
        room = 1500 - 400 - 100; cards = ''
        for n, b in s['crops']:
            _, h = crop(n, b, 900)
            h = min(h, room); cards += card(n, b, 900, h); room -= h + 26
            if room < 120: break
        return (f'<div style="position:relative;width:1000px;height:1500px;overflow:hidden;background:#FBF8F3">'
                f'<div style="position:absolute;left:0;top:0;width:1000px;height:430px;background:{c}"></div>'
                f'<div style="position:relative;padding:58px 60px 0;text-align:center">'
                f'<p style="margin:0;font:700 24px Inter;letter-spacing:5px;color:{acc}">{s["kicker"]}</p>'
                f'<p style="margin:6px 0 0;font:{150 if len(s["title"]) < 14 else 128}px/1.05 GV;white-space:nowrap;color:{INK}">{s["title"]}</p>'
                f'<p style="margin:10px auto 40px;width:820px;font:500 31px/1.35 Inter;color:{MUT}">{s["sub"]}</p></div>'
                f'<div style="position:relative">{cards}</div>'
                f'<p style="position:absolute;left:0;bottom:34px;width:1000px;margin:0;text-align:center;font:700 22px Inter;letter-spacing:3px;color:{MUT}">SYSTEMFORGE · INSTANT DOWNLOAD</p></div>')
    room = 1500 - 640 - 100; shots = ''
    for n, b in s['crops']:
        _, h = crop(n, b, 1000); h = min(h, room); p, h = crop(n, b, 1000, h)
        shots += f'<div style="width:1000px;height:{h}px;margin-bottom:14px;background:#fff url(file://{p}) 0 0/1000px {h}px no-repeat;border-top:1px solid #E7E1D8;border-bottom:1px solid #E7E1D8"></div>'
        room -= h + 14
        if room < 120: break
    return (f'<div style="position:relative;width:1000px;height:1500px;overflow:hidden;background:#FBF8F3">'
            f'<div style="height:520px;background:{acc};color:#fff;text-align:center;padding-top:70px;box-sizing:border-box">'
            f'<p style="margin:0 auto;width:880px;font:700 104px/1.02 PF">{s["title"]}</p>'
            f'<p style="margin:14px 0 0;font:84px/1 GV">{s["kicker"]}</p></div>'
            f'<p style="margin:34px auto 30px;width:880px;text-align:center;font:500 34px/1.3 Inter;color:{INK}">{s["sub"]}</p>' +
            shots +
            f'<div style="position:absolute;right:40px;bottom:120px;width:220px;height:220px;border-radius:50%;background:{c};border:5px solid #fff;'
            f'display:flex;align-items:center;justify-content:center;text-align:center;font:700 25px/1.25 Inter;color:{INK};white-space:pre-line;box-shadow:0 8px 20px rgba(0,0,0,.15)">{s["badge"]}</div>'
            f'<p style="position:absolute;left:0;bottom:34px;width:1000px;margin:0;text-align:center;font:700 22px Inter;letter-spacing:3px;color:{MUT}">SYSTEMFORGE · INSTANT DOWNLOAD</p></div>')


def render(pid, body):
    h = os.path.join(TMP, '_p.html')
    open(h, 'w').write('<!doctype html><html><head><meta charset="utf-8">' + FONTS + '</head><body>' + body + '</body></html>')
    shot = h + '.png'
    subprocess.run([B.CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=2', '--window-size=1000,1700', '--virtual-time-budget=3000', f'--screenshot={shot}', 'file://' + h],
                   check=True, capture_output=True)
    Image.open(shot).crop((0, 0, 2000, 3000)).convert('RGB').save(os.path.join(OUT, pid + '.png'), optimize=True)
    os.remove(h); os.remove(shot)


if __name__ == '__main__':
    for pid in sys.argv[1:] or list(PINS):
        render(pid, html(PINS[pid])); print('png', pid)
