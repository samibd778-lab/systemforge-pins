"""Bonus PDF v2 for Second Brain OS: 'Notion for beginners' (US Letter, 7 pages), editorial redesign.
Run: python3 generator/sb_guide2.py -> products/second-brain/Notion-Beginner-Guide.pdf (+ etsy/sb copy)
"""
import base64, pathlib, subprocess, shutil, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "generator" / "styles"))
from pins_v2 import FONT_CSS  # Fraunces (serif) + InterW
OUT = ROOT / "products" / "second-brain"
OUT.mkdir(parents=True, exist_ok=True)
dm = base64.b64encode((ROOT / "brand/fonts/dmserif.woff2").read_bytes()).decode()

TOTAL = 7
def head(n, label):
    dots = "".join(f'<i class="{"on" if i == n else ""}"></i>' for i in range(1, TOTAL + 1))
    return f'<div class="hd"><span>Second Brain OS · Notion for beginners</span><span class="dots">{dots}</span><span>{label}</span></div>'
def foot(n):
    return f'<div class="ft"><span>SystemForge</span><span>{n:02d} / {TOTAL:02d}</span></div>'
def page(n, label, inner, cls=""):
    return f'<section class="pg {cls}">{head(n, label) if n > 1 else ""}{inner}{foot(n) if n > 1 else ""}</section>'

P = []

# 1 COVER
P.append(page(1, "", """
<div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div>
<div class="cv">
  <div class="tag">Bonus guide · 15-minute read</div>
  <h1>Notion<br><em>for beginners</em></h1>
  <p class="cvlead">Feel at home in Notion and in your Second Brain, without reading a manual.</p>
</div>
<div class="cvbrand"><span class="logo">SF</span>SystemForge</div>
<div class="shot"><div class="bar"><i></i><i></i><i></i><span>Second Brain OS</span></div><img src="data:image/png;base64,SHOT_B64"></div>
""", "cover"))

# 2 SET UP
P.append(page(2, "Chapter 01", """
<div class="ch"><span class="big">01</span><div><div class="kick">Five minutes, once</div><h2>Get set up</h2></div></div>
<div class="tl">
 <div class="st"><div class="dot">1</div><div><h4>Create your Notion account</h4><p>Go to notion.com and sign up, or log in. Use the same account on your computer and your phone.</p></div></div>
 <div class="st"><div class="dot">2</div><div><h4>Duplicate the template</h4><p>Open your template link and click <b>Duplicate</b> in the top right corner. Pick your workspace. Your Second Brain is now yours.</p></div></div>
 <div class="st"><div class="dot">3</div><div><h4>Get the apps</h4><p>Notion has apps for Mac, Windows, iPhone and Android. Everything you add syncs everywhere.</p></div></div>
 <div class="st"><div class="dot">4</div><div><h4>Pin it to your favorites</h4><p>On the home page, click <b>☆</b> at the top right. On your phone, do the same for <b>📱 Mobile home</b>.</p></div></div>
 <div class="st"><div class="dot">5</div><div><h4>Open “Start here”</h4><p>It's the first link in the menu. Keep the example data at first: it shows how everything connects.</p></div></div>
</div>
<div class="note"><span>TIP</span><div>Turn on <b>Full width</b> (••• at the top right) on the home page. Your dashboard gets room to breathe.</div></div>
"""))

# 3 SIX THINGS
cards = [("▦", "Blocks", "Every line is a block: text, a checkbox, an image. Drag the ⋮⋮ handle to move one."),
         ("/", "The / menu", "Type / on an empty line to add anything: headings, to-dos, toggles, callouts."),
         ("❏", "Pages", "Pages hold other pages, like folders. Each one can have an icon and a cover."),
         ("☷", "Databases", "Lists where every item is a page with fields: a date, a status, a tag."),
         ("◫", "Views", "The same data as a table, board, calendar or gallery. Switch with the tabs."),
         ("⇄", "Relations", "Links between databases. A task belongs to a project, a project to a goal.")]
grid = "".join(f'<div class="c6"><div class="ic">{i}</div><h4>{t}</h4><p>{d}</p></div>' for i, t, d in cards)
P.append(page(3, "Chapter 02", f"""
<div class="ch"><span class="big">02</span><div><div class="kick">Learn these and you know Notion</div><h2>The 6 things to know</h2></div></div>
<div class="g6">{grid}</div>
<div class="quote">“Once you get blocks, pages and databases, the rest is just practice.”</div>
"""))

# 4 DATABASES
daily = [("🗒️", "Notes", "Ideas, links, quotes"), ("✅", "Tasks", "Next steps with a date"),
         ("✔️", "Habits", "Tick what you did"), ("📓", "Journal", "Mood, win, thanks")]
dl = "".join(f'<div class="d4"><div class="em">{e}</div><h4>{t}</h4><p>{d}</p><span class="pill">Every day</span></div>' for e, t, d in daily)
rest = [("🚀", "Projects", "Every week"), ("🎯", "Goals", "Every month"), ("🧭", "Areas", "Every month"),
        ("📚", "Resources", "When needed"), ("📖", "Reading list", "When needed"), ("🔁", "Weekly reviews", "Every week")]
rl = "".join(f'<div class="r6"><span>{e}</span><b>{t}</b><em>{f}</em></div>' for e, t, f in rest)
P.append(page(4, "Chapter 03", f"""
<div class="ch"><span class="big">03</span><div><div class="kick">10 databases, 4 you'll use daily</div><h2>Databases, simply</h2></div></div>
<h5 class="lbl">Your daily four</h5>
<div class="g4">{dl}</div>
<h5 class="lbl">The rest of your system</h5>
<div class="g3">{rl}</div>
<div class="duo">
 <div><h4>Add something</h4><p>Click <b>New</b> on any database, or <b>+ New page</b> at the bottom of a list.</p></div>
 <div><h4>Filter and sort</h4><p>Use the icons above a database. They only change the view, never your data.</p></div>
</div>
"""))

# 5 ROUTINE
bands = [("Every day", "5 min", "☕", ["Capture ideas with ⚡ Quick capture", "Do the first task in 🔥 Next 7 days", "Tick today's habits", "Write a 2-minute journal entry"]),
         ("Every week", "15 min", "🔁", ["Empty the 📥 Inbox: give each note a home", "Check projects in progress and your goals", "Pick the 3 most important tasks", "Add a page in Weekly reviews"]),
         ("Every month", "30 min", "🗓️", ["Open Monthly review", "Write your wins and lessons", "Score each area of your life", "Choose your focus for next month"]),
         ("Every year", "1–2 h", "🎆", ["Open Yearly review", "Look back at your best moments", "Score each area from 1 to 10", "Set 3 goals for next year"])]
bh = "".join(f'<div class="band"><div class="bl"><span class="be">{e}</span><h4>{t}</h4><span class="time">{m}</span></div><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></div>' for t, m, e, li in bands)
P.append(page(5, "Chapter 04", f"""
<div class="ch"><span class="big">04</span><div><div class="kick">Small habits, every day</div><h2>Your routine</h2></div></div>
<div class="bands">{bh}</div>
<div class="note green"><span>RULE</span><div>Capture first, sort later. A rough note in the inbox beats a perfect note you never wrote.</div></div>
"""))

# 6 MAKE IT YOURS
items = [("Delete the example data", "Tick the box on the left of each row and press Delete. Start with Tasks and Notes, then Projects, Goals and Areas."),
         ("Rename your habits", "In Habits, click a column name like “🏃 Move” and type your own."),
         ("Change covers and icons", "Hover the top of any page, then click Change cover or the icon."),
         ("Set your areas", "Write one line in Standard for each area: what “good” looks like for you."),
         ("Save templates", "In a database, click the arrow next to New → + New template. Perfect for your journal."),
         ("Try dark mode", "Settings → Appearance. Your Second Brain looks great in both.")]
ih = "".join(f'<div class="ck"><div class="box"></div><div><h4>{t}</h4><p>{d}</p></div></div>' for t, d in items)
P.append(page(6, "Chapter 05", f"""
<div class="ch"><span class="big">05</span><div><div class="kick">Your system, your way</div><h2>Make it yours</h2></div></div>
<div class="two"><div class="cks">{ih}</div>
<aside class="side"><div class="kick">Good to know</div><h4>Nothing breaks</h4><p>Everything you change only lives in your copy. Experiment freely.</p><h4>Undo is your friend</h4><p>Press undo right away, or restore a page from Trash in the sidebar.</p><h4>Start small</h4><p>Use Notes, Tasks and Habits for one week. Add the rest when you're ready.</p></aside></div>
"""))

# 7 SHORTCUTS
keys = [("Search everything", "⌘", "P", "Ctrl", "P"), ("New page", "⌘", "N", "Ctrl", "N"), ("Undo", "⌘", "Z", "Ctrl", "Z"),
        ("Show / hide sidebar", "⌘", "\\", "Ctrl", "\\"), ("Dark mode", "⌘ ⇧", "L", "Ctrl ⇧", "L")]
kh = "".join(f'<div class="kr"><span class="kn">{n}</span><span class="kk"><kbd>{a}</kbd><kbd>{b}</kbd></span><span class="kk"><kbd>{c}</kbd><kbd>{d}</kbd></span></div>' for n, a, b, c, d in keys)
P.append(page(7, "Chapter 06", f"""
<div class="ch"><span class="big">06</span><div><div class="kick">Work faster</div><h2>Shortcuts & fixes</h2></div></div>
<div class="keys"><div class="kr khd"><span class="kn"></span><span>Mac</span><span>Windows</span></div>{kh}
<div class="kr"><span class="kn">Add any block</span><span class="kk wide"><kbd>/</kbd> on an empty line</span></div></div>
<div class="duo">
 <div><h4>I deleted something</h4><p>Press undo right away, or open <b>Trash</b> in the sidebar to restore it.</p></div>
 <div><h4>A view looks empty</h4><p>Check the filter icon above it. Some views only show this week or open items.</p></div>
</div>
<div class="end"><div><div class="kick light">You're ready</div><h3>Open <em>Start here</em> and capture your first idea.</h3></div><p>Need help? Send us a message where you bought this template. We read every message.</p></div>
"""))

css = f"""{FONT_CSS}
@font-face{{font-family:'DMS';src:url(data:font/woff2;base64,{dm}) format('woff2')}}
@page{{size:Letter;margin:0}}*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--cream:#F6F1E9;--paper:#FFFDF9;--ink:#2E2A25;--mute:#6F665B;--sage:#7A8B6F;--sage2:#E3E8DC;--clay:#C98B6B;--clay2:#F1DDCF;--forest:#1F3324;--line:#E7DED2}}
body{{font-family:InterW;color:var(--ink);background:var(--cream)}}
.pg{{width:8.5in;height:11in;padding:.62in .7in .7in;position:relative;page-break-after:always;overflow:hidden;background:var(--cream)}}
h1,h2,h3,.big{{font-family:'DMS',Georgia,serif;font-weight:400}}
h4{{font-weight:700;font-size:14px;margin-bottom:4px}}p{{font-weight:500;font-size:12.5px;line-height:1.55;color:var(--mute)}}
.hd{{display:flex;justify-content:space-between;align-items:center;font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);font-weight:700}}
.dots{{display:flex;gap:6px}}.dots i{{width:18px;height:4px;border-radius:9px;background:var(--line)}}.dots i.on{{background:var(--sage)}}
.ft{{position:absolute;left:.7in;right:.7in;bottom:.42in;display:flex;justify-content:space-between;font-size:9.5px;color:#A39789;font-weight:700;letter-spacing:.1em;text-transform:uppercase}}
.ch{{display:flex;align-items:flex-end;gap:18px;margin:34px 0 26px;padding-bottom:20px;border-bottom:1.5px solid var(--line)}}
.big{{font-size:96px;line-height:.8;color:var(--clay)}}
.kick{{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;font-weight:700;color:var(--sage);margin-bottom:6px}}
h2{{font-size:40px;line-height:1}}
/* cover */
.cover{{background:var(--forest);color:#F3ECE2;padding:.9in .8in}}
.ring{{position:absolute;border-radius:50%;border:1.5px solid rgba(243,236,226,.13)}}
.r1{{width:6.5in;height:6.5in;right:-2.6in;top:-1.9in}}.r2{{width:4.6in;height:4.6in;right:-1.65in;top:-.95in}}.r3{{width:2.7in;height:2.7in;right:-.7in;top:0;background:var(--clay);border:none;opacity:.9}}
.cv{{position:relative;margin-top:.75in}}
.shot{{position:absolute;left:.95in;right:-.35in;bottom:.6in;background:#fff;border-radius:14px 0 0 14px;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.45),0 0 0 1px rgba(255,255,255,.08)}}
.shot .bar{{height:30px;background:#EDE7DF;display:flex;align-items:center;gap:7px;padding:0 14px}}
.shot .bar i{{width:10px;height:10px;border-radius:50%;background:#D3C8BB}}.shot .bar i:first-child{{background:#E39A82}}
.shot .bar span{{margin-left:14px;font-size:10px;font-weight:700;color:#8A7A6C;background:#F7F3EE;border-radius:6px;padding:4px 40px 4px 12px}}
.shot img{{display:block;width:100%}}
.tag{{display:inline-block;border:1px solid rgba(243,236,226,.35);border-radius:99px;padding:7px 14px;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:#D9E2D2}}
h1{{font-size:84px;line-height:.95;margin:26px 0 20px}}h1 em{{font-style:italic;color:#E8C3AA}}
.cvlead{{font-size:17px;color:#D6CCBE;max-width:4.6in;line-height:1.5}}
.cvgrid{{margin-top:.55in;display:grid;grid-template-columns:1fr 1fr;gap:0 28px;max-width:5.6in}}
.cvgrid div{{padding:12px 0;border-top:1px solid rgba(243,236,226,.18);font-size:14px;font-weight:500;color:#F3ECE2}}
.cvgrid b{{font-family:'DMS',serif;font-weight:400;color:#E8C3AA;margin-right:12px;font-size:16px}}
.cvbrand{{position:absolute;left:.8in;top:.7in;display:flex;align-items:center;gap:10px;font-weight:700;font-size:14px;color:#D9E2D2}}
.logo{{width:38px;height:38px;border-radius:50%;background:#F3ECE2;color:var(--forest);display:flex;align-items:center;justify-content:center;font-size:13px}}
/* setup timeline */
.tl{{position:relative;margin-left:8px}}.tl::before{{content:'';position:absolute;left:19px;top:20px;bottom:40px;width:2px;background:var(--line)}}
.st{{display:flex;gap:22px;margin-bottom:20px;position:relative}}
.dot{{flex:none;width:40px;height:40px;border-radius:50%;background:var(--paper);border:2px solid var(--sage);display:flex;align-items:center;justify-content:center;font-family:'DMS';font-size:18px;color:var(--sage)}}
.st h4{{font-size:16px;margin-top:9px}}
.note{{display:flex;gap:14px;align-items:center;background:var(--clay2);border-radius:14px;padding:16px 20px;font-size:13px;font-weight:500;line-height:1.5;margin-top:10px}}
.note span{{flex:none;background:var(--clay);color:#fff;font-weight:700;font-size:10px;letter-spacing:.14em;padding:6px 10px;border-radius:8px}}
.note.green{{background:var(--sage2)}}.note.green span{{background:var(--sage)}}
/* six */
.g6{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
.c6{{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:20px 22px}}
.ic{{width:42px;height:42px;border-radius:12px;background:var(--sage2);color:var(--forest);display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:700;margin-bottom:12px}}
.c6:nth-child(even) .ic{{background:var(--clay2);color:#8A4F33}}
.c6 h4{{font-size:16px}}
.quote{{margin-top:26px;font-family:'DMS';font-size:22px;line-height:1.35;color:var(--forest);padding-left:20px;border-left:3px solid var(--clay)}}
/* databases */
.lbl{{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);margin:4px 0 12px}}
.g4{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:26px}}
.d4{{background:var(--forest);color:#F3ECE2;border-radius:16px;padding:18px 16px}}
.d4 .em{{font-size:26px;margin-bottom:10px}}.d4 h4{{font-size:16px}}.d4 p{{color:#CFC5B7;font-size:11.5px;min-height:34px}}
.pill{{display:inline-block;margin-top:10px;background:rgba(243,236,226,.14);border-radius:99px;padding:4px 10px;font-size:10px;font-weight:700;letter-spacing:.06em}}
.g3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px}}
.r6{{display:flex;align-items:center;gap:10px;background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:12px 14px;font-size:13px}}
.r6 b{{flex:1}}.r6 em{{font-style:normal;font-size:10px;font-weight:700;color:var(--sage);text-transform:uppercase;letter-spacing:.06em}}
.duo{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:22px}}
.duo>div{{background:var(--paper);border-radius:14px;padding:18px 20px;border:1px solid var(--line)}}
/* routine */
.bands{{display:grid;gap:12px}}
.band{{display:grid;grid-template-columns:1.6in 1fr;background:var(--paper);border:1px solid var(--line);border-radius:16px;overflow:hidden}}
.bl{{background:var(--sage2);padding:18px;display:flex;flex-direction:column;gap:4px}}
.band:nth-child(2) .bl{{background:var(--clay2)}}.band:nth-child(3) .bl{{background:#EDE4F0}}.band:nth-child(4) .bl{{background:#E4ECF2}}
.be{{font-size:22px}}.bl h4{{font-size:16px;margin:4px 0 0}}.time{{font-size:11px;font-weight:700;color:var(--mute)}}
.band ul{{list-style:none;padding:16px 20px;display:grid;grid-template-columns:1fr 1fr;gap:8px 18px;align-content:center}}
.band li{{font-size:12px;font-weight:500;color:var(--ink);padding-left:20px;position:relative;line-height:1.4}}
.band li::before{{content:'';position:absolute;left:0;top:2px;width:11px;height:11px;border:1.5px solid var(--sage);border-radius:3px}}
/* make it yours */
.two{{display:grid;grid-template-columns:1fr 2.2in;gap:22px}}
.cks{{display:grid;gap:14px}}.ck{{display:flex;gap:16px}}
.box{{flex:none;width:22px;height:22px;border:2px solid var(--sage);border-radius:6px;margin-top:2px}}
.ck h4{{font-size:15px}}
.side{{background:var(--forest);color:#F3ECE2;border-radius:18px;padding:22px}}
.side h4{{font-size:15px;margin-top:16px}}.side p{{color:#CFC5B7;font-size:12px}}.side .kick{{color:#BFD3B8}}
/* shortcuts */
.keys{{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:8px 20px}}
.kr{{display:grid;grid-template-columns:1fr 1.5in 1.5in;align-items:center;padding:10px 0;border-bottom:1px solid var(--line);font-size:13px;font-weight:500}}
.kr:last-child{{border:none}}.khd{{font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}}
.kk{{display:flex;gap:6px;align-items:center}}.kk.wide{{grid-column:span 2;color:var(--mute)}}
kbd{{font-family:InterW;font-weight:700;font-size:11.5px;background:var(--cream);border:1px solid #D9CEBF;border-bottom-width:3px;border-radius:7px;padding:4px 9px;min-width:28px;text-align:center}}
.end{{margin-top:22px;background:var(--forest);border-radius:18px;padding:24px 26px;display:grid;grid-template-columns:1.3fr 1fr;gap:22px;align-items:center}}
.end h3{{font-size:25px;color:#F3ECE2;line-height:1.2}}.end h3 em{{color:#E8C3AA}}.end p{{color:#CFC5B7}}.kick.light{{color:#BFD3B8}}
/* scale up to fill the page */
p{{font-size:14.5px}}h4{{font-size:17px!important;margin-bottom:6px}}
.ch{{margin:44px 0 34px}}.big{{font-size:120px}}h2{{font-size:52px}}.kick{{font-size:12px}}
.st{{margin-bottom:30px}}.st h4{{margin-top:8px}}.dot{{width:46px;height:46px;font-size:21px}}.tl::before{{left:22px}}
.note{{font-size:15px;padding:22px 24px;margin-top:20px}}
.g6{{gap:18px}}.c6{{padding:28px 26px;min-height:2.1in}}.ic{{width:52px;height:52px;font-size:24px;margin-bottom:16px}}
.quote{{font-size:27px;margin-top:34px}}
.lbl{{font-size:12px;margin:8px 0 16px}}
.d4{{padding:24px 20px;min-height:2.5in}}.d4 .em{{font-size:34px;margin-bottom:16px}}.d4 p{{font-size:13.5px;min-height:44px}}.pill{{font-size:11px;padding:6px 12px}}
.g4{{margin-bottom:34px}}.g3{{gap:12px}}.r6{{padding:18px 16px;font-size:14.5px}}.r6 em{{font-size:10.5px}}
.duo{{gap:18px;margin-top:30px}}.duo>div{{padding:24px 24px}}
.bands{{gap:18px}}.bl{{padding:24px 20px}}.be{{font-size:28px}}.time{{font-size:12.5px}}
.band ul{{padding:24px 24px;gap:14px 20px}}.band li{{font-size:14px;padding-left:24px}}.band li::before{{width:13px;height:13px}}
.cks{{gap:24px}}.box{{width:24px;height:24px}}.side{{padding:28px 24px}}.side h4{{margin-top:24px}}.side p{{font-size:13.5px}}
.kr{{padding:15px 0;font-size:15px}}kbd{{font-size:13px;padding:6px 11px}}.keys{{padding:10px 24px}}
.end{{margin-top:30px;padding:32px 30px}}.end h3{{font-size:30px}}
/* per-page balance */
.st{{margin-bottom:40px}}.tl+.note{{margin-top:30px}}
.c6{{min-height:1.85in;padding:24px 24px}}.quote{{font-size:24px;margin-top:26px}}
.d4{{min-height:2.95in}}.r6{{padding:24px 16px}}.g3+.duo{{margin-top:44px}}.g3+.duo>div{{padding:30px 26px}}
.kr{{padding:11px 0}}.keys+.duo{{margin-top:22px}}.end{{margin-top:22px;padding:26px 28px}}.end h3{{font-size:27px}}
"""
shot = base64.b64encode((ROOT / "brand/shots/sb_home_top.png").read_bytes()).decode()
P[0] = P[0].replace("SHOT_B64", shot)
css += ".cover h1{font-size:76px;margin:22px 0 16px}.cover .cvgrid{margin-top:.4in}.cover .cvgrid div{padding:10px 0}"
html = f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(P)}</body></html>"
hp = OUT / "guide.html"; hp.write_text(html)
pdf = OUT / "Notion-Beginner-Guide.pdf"
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{hp}');await p.waitForTimeout(300);await p.pdf({{path:'{pdf}',format:'Letter',printBackground:true}});await b.close();}})()"""
subprocess.run(["node", "-e", js], check=True)
hp.unlink()
shutil.copy(pdf, ROOT / "etsy/sb/Notion-Beginner-Guide.pdf")
print(pdf)
