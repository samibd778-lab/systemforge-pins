"""Bonus PDF for Second Brain OS: 'Notion for beginners' quick guide (US Letter).
Run: python3 generator/sb_guide.py  ->  products/second-brain/Notion-Beginner-Guide.pdf
"""
import base64, pathlib, subprocess, json

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "products" / "second-brain"
OUT.mkdir(parents=True, exist_ok=True)
font = base64.b64encode((ROOT / "brand/fonts/dmserif.woff2").read_bytes()).decode()

def page(inner, cls=""):
    return f'<section class="pg {cls}">{inner}<div class="foot">Second Brain OS · Notion for beginners</div></section>'

pages = []

pages.append(page("""
<div class="cover">
  <div class="kicker">Bonus guide</div>
  <h1>Notion for beginners</h1>
  <p class="lead">Everything you need to feel at home in Notion and in your Second Brain, in 15 minutes.</p>
  <div class="toc">
    <div><b>1</b> Get set up</div>
    <div><b>2</b> The 6 things to know</div>
    <div><b>3</b> Databases, simply</div>
    <div><b>4</b> Your daily and weekly routine</div>
    <div><b>5</b> Make it yours</div>
    <div><b>6</b> Shortcuts and fixes</div>
  </div>
  <div class="brand">SystemForge</div>
</div>""", "dark"))

pages.append(page("""
<div class="num">1</div><h2>Get set up</h2>
<p class="lead">Five minutes, once.</p>
<ol class="steps">
<li><b>Create your Notion account</b> at notion.com (or log in). Use the same account on your computer and phone.</li>
<li><b>Open your template link</b> and click <b>Duplicate</b> in the top right corner. Pick your workspace. The full Second Brain is now copied into your account.</li>
<li><b>Get the apps.</b> Notion has apps for Mac, Windows, iPhone and Android. Everything syncs.</li>
<li><b>Add it to your sidebar favorites.</b> Open the Second Brain home page, click <b>⭐</b> (top right). Do the same for <b>📱 Mobile home</b> on your phone.</li>
<li><b>Open Start here</b> in the menu and follow the steps. Keep the example data at first: it shows how everything links together.</li>
</ol>
<div class="tip"><b>Tip:</b> Turn on <b>Full width</b> (••• top right) on the home page. It gives your dashboard room to breathe.</div>
"""))

pages.append(page("""
<div class="num">2</div><h2>The 6 things to know</h2>
<div class="grid">
<div class="card"><h3>Blocks</h3><p>Every line in Notion is a block: text, a checkbox, an image, a heading. Hover a block and drag <b>⋮⋮</b> to move it.</p></div>
<div class="card"><h3>The / menu</h3><p>Type <b>/</b> on any empty line to add anything: a heading, a to-do list, a toggle, a callout, an image.</p></div>
<div class="card"><h3>Pages</h3><p>A page can hold other pages, like folders. Every page can have an icon and a cover.</p></div>
<div class="card"><h3>Databases</h3><p>A list where every item is a page with fields (date, status, tags). Your Tasks, Notes and Projects are databases.</p></div>
<div class="card"><h3>Views</h3><p>The same data shown in different ways: table, board, calendar, gallery, list. Switch with the tabs above a database.</p></div>
<div class="card"><h3>Relations</h3><p>Links between databases. A task belongs to a project, a project to an area and a goal. That's how your progress bars work.</p></div>
</div>
"""))

pages.append(page("""
<div class="num">3</div><h2>Databases, simply</h2>
<p class="lead">Your Second Brain has 10 databases. You'll use 4 of them every day.</p>
<table class="t">
<tr><th>Database</th><th>What goes in it</th><th>How often</th></tr>
<tr><td>🗒️ Notes</td><td>Ideas, links, quotes, meeting notes</td><td>Every day</td></tr>
<tr><td>✅ Tasks</td><td>Small next steps with a due date</td><td>Every day</td></tr>
<tr><td>✔️ Habits</td><td>One row per day, tick what you did</td><td>Every day</td></tr>
<tr><td>📓 Journal</td><td>A 2-minute check-in: mood, win, thanks</td><td>Every day</td></tr>
<tr><td>🚀 Projects</td><td>Things with a finish line</td><td>Every week</td></tr>
<tr><td>🎯 Goals</td><td>The big things you want this year</td><td>Every month</td></tr>
<tr><td>🧭 Areas</td><td>Parts of life you keep up (health, money…)</td><td>Every month</td></tr>
<tr><td>📚 Resources · 📖 Reading list · 🔁 Weekly reviews</td><td>Topics, books, your reviews</td><td>When needed</td></tr>
</table>
<div class="row2">
<div class="card"><h3>Add an item</h3><p>Click <b>New</b> on a database, or the <b>+ New page</b> line at the bottom of a list.</p></div>
<div class="card"><h3>Filter and sort</h3><p>Use the filter and sort icons above a database. They only change the view, never your data.</p></div>
</div>
"""))

pages.append(page("""
<div class="num">4</div><h2>Your routine</h2>
<div class="row2">
<div class="card big"><h3>☕ Every day · 5 min</h3>
<ul class="check">
<li>Capture ideas into <b>Notes</b> (use ⚡ Quick capture)</li>
<li>Check <b>🔥 Next 7 days</b> and do the first task</li>
<li>Tick today's <b>habits</b></li>
<li>Write a 2-minute <b>journal</b> entry</li>
</ul></div>
<div class="card big"><h3>🔁 Every week · 15 min</h3>
<ul class="check">
<li>Empty the <b>📥 Inbox</b>: give each note a home</li>
<li>Check projects <b>In progress</b> and your goals</li>
<li>Pick the 3 most important tasks for next week</li>
<li>Add a page in <b>Weekly reviews</b></li>
</ul></div>
</div>
<div class="row2">
<div class="card big"><h3>🗓️ Every month · 30 min</h3>
<p>Open <b>Monthly review</b>: wins, lessons, an area check and your focus for next month.</p></div>
<div class="card big"><h3>🎆 Every year · 1–2 h</h3>
<p>Open <b>Yearly review</b>: look back, score each area and set 3 goals for next year.</p></div>
</div>
<div class="tip"><b>The golden rule:</b> capture first, sort later. A rough note in the inbox beats a perfect note you never wrote.</div>
"""))

pages.append(page("""
<div class="num">5</div><h2>Make it yours</h2>
<ol class="steps">
<li><b>Delete the example data</b> when you're ready. In a database, tick the box on the left of each row and press Delete. Start with Tasks and Notes, then Projects, Goals and Areas.</li>
<li><b>Rename your habits.</b> Open Habits, click a column name (like <i>🏃 Move</i>) and type your own.</li>
<li><b>Change covers and icons.</b> Hover the top of any page and click <b>Change cover</b> or the icon.</li>
<li><b>Set your areas.</b> Write one line in <b>Standard</b> for each: what “good” looks like for you.</li>
<li><b>Save repeat pages as templates.</b> In a database, click the arrow next to <b>New</b> → <b>+ New template</b>. Great for your journal and weekly review.</li>
<li><b>Turn on dark mode</b> if you like: Settings → Appearance.</li>
</ol>
"""))

pages.append(page("""
<div class="num">6</div><h2>Shortcuts and fixes</h2>
<table class="t keys">
<tr><th>Do this</th><th>Mac</th><th>Windows</th></tr>
<tr><td>Search everything</td><td>⌘ + P</td><td>Ctrl + P</td></tr>
<tr><td>New page</td><td>⌘ + N</td><td>Ctrl + N</td></tr>
<tr><td>Undo</td><td>⌘ + Z</td><td>Ctrl + Z</td></tr>
<tr><td>Show / hide sidebar</td><td>⌘ + \\</td><td>Ctrl + \\</td></tr>
<tr><td>Dark mode on / off</td><td>⌘ + Shift + L</td><td>Ctrl + Shift + L</td></tr>
<tr><td>Add any block</td><td colspan="2">Type / on an empty line</td></tr>
</table>
<h3 class="sub">Something looks wrong?</h3>
<div class="row2">
<div class="card"><h3>I deleted something</h3><p>Press undo right away, or open <b>Trash</b> in the sidebar to restore a page.</p></div>
<div class="card"><h3>A view is empty</h3><p>Check the filter icon above it. Some views only show this week or open items.</p></div>
</div>
<div class="tip"><b>Need help?</b> Send us a message where you bought this template. We read every message.</div>
"""))

css = f"""
@font-face{{font-family:'DM Serif';src:url(data:font/woff2;base64,{font}) format('woff2')}}
@page{{size:Letter;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;color:#2B241E;background:#F7F3EE}}
.pg{{width:8.5in;height:11in;padding:.8in .8in .9in;position:relative;page-break-after:always;background:#F7F3EE;overflow:hidden}}
.pg.dark{{background:#1B2F1B;color:#F3ECE2}}
h1,h2,h3{{font-family:'DM Serif',Georgia,serif;font-weight:400}}
h1{{font-size:64px;line-height:1.02;margin:18px 0 22px}}
h2{{font-size:44px;margin:4px 0 10px}}
h3{{font-size:21px;margin-bottom:6px}}
h3.sub{{margin:26px 0 10px}}
.num{{font-family:'DM Serif',serif;font-size:20px;color:#fff;background:#4A6B4F;width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center}}
.kicker{{text-transform:uppercase;letter-spacing:.2em;font-size:13px;color:#BFD3B8;margin-top:1.2in}}
.lead{{font-size:18px;line-height:1.5;color:#7A6A5B;margin-bottom:22px}}
.dark .lead{{color:#D8CDBE;max-width:5.4in}}
.toc{{margin-top:46px;display:grid;gap:14px;font-size:18px}}
.toc b{{display:inline-block;width:30px;color:#BFD3B8;font-family:'DM Serif',serif}}
.brand{{position:absolute;bottom:.8in;left:.8in;font-family:'DM Serif',serif;font-size:22px;color:#BFD3B8}}
.steps{{padding-left:22px;display:grid;gap:16px;font-size:16px;line-height:1.55}}
.steps li::marker{{color:#4A6B4F;font-weight:700}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:18px}}
.row2{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:18px}}
.card{{background:#fff;border:1px solid #E6DDD2;border-radius:14px;padding:18px 20px;font-size:15px;line-height:1.5}}
.card p{{color:#5A4D41}}
.card.big{{min-height:1.9in}}
.check{{list-style:none;display:grid;gap:8px;margin-top:6px}}
.check li::before{{content:'☐  ';color:#4A6B4F}}
.tip{{margin-top:24px;background:#E8EFE4;border-left:4px solid #4A6B4F;border-radius:8px;padding:14px 18px;font-size:15px;line-height:1.5}}
.t{{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;font-size:14.5px;margin-top:8px}}
.t th{{background:#1B2F1B;color:#F3ECE2;text-align:left;padding:11px 14px;font-weight:600}}
.t td{{padding:10px 14px;border-top:1px solid #EFE7DC}}
.keys td:nth-child(n+2){{font-family:ui-monospace,Menlo,monospace;color:#4A6B4F}}
.foot{{position:absolute;bottom:.45in;left:.8in;right:.8in;font-size:11px;color:#A3968A;letter-spacing:.06em}}
.dark .foot{{display:none}}
"""
html = f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(pages)}</body></html>"
hp = OUT / "guide.html"
hp.write_text(html)
pdf = OUT / "Notion-Beginner-Guide.pdf"
js = f"""
const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{hp}');await p.pdf({{path:'{pdf}',format:'Letter',printBackground:true}});
await p.setViewportSize({{width:816,height:1056}});
for(let i=0;i<{len(pages)};i++){{await p.evaluate(n=>window.scrollTo(0,n*1056),i);await p.screenshot({{path:'{OUT}/guide-p'+(i+1)+'.png'}});}}
await b.close();}})()"""
subprocess.run(["node", "-e", js], check=True)
hp.unlink()
print(pdf)
