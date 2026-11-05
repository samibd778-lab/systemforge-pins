"""Bonus PDF guides for Habit Tracker, Daily Journal and Budget Planner (US Letter, 6 pages each).
Reuses the editorial CSS of generator/sb_guide2.py. No store links inside (same file for Gumroad and Etsy).
Run: python3 generator/mini_guides.py  -> products/<p>/<file>.pdf
"""
import base64, pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "generator" / "styles"))
from pins_v2 import FONT_CSS
dm = base64.b64encode((ROOT / "brand/fonts/dmserif.woff2").read_bytes()).decode()
src = (ROOT / "generator/sb_guide2.py").read_text()
css_src = src[src.index('css = f"""') + 6: src.index('"""\nshot =') + 3]
BASE_CSS = eval(css_src, {"FONT_CSS": FONT_CSS, "dm": dm})

EXTRA = """
.cover .cvgrid{margin-top:.7in;max-width:6.4in}.cover .cvgrid div{font-size:16px;padding:16px 0}
.cover h1{font-size:80px}
.cvfoot{position:absolute;left:.8in;right:.8in;bottom:.75in;font-size:13px;color:#CFC5B7;border-top:1px solid rgba(243,236,226,.18);padding-top:16px}
.grid30{display:grid;grid-template-columns:1.5in repeat(10,1fr);gap:5px;align-items:center;margin-bottom:7px}
.grid30 .h{font-size:11px;font-weight:700;color:var(--mute);text-align:center}
.grid30 .n{font-size:13px;font-weight:700}
.grid30 .b{height:21px;border:1.5px solid var(--line);border-radius:6px;background:var(--paper)}
.blk{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:18px 22px;margin-bottom:16px}
.blk h4{margin-bottom:10px}
.lines div{height:30px;border-bottom:1.5px solid var(--line)}
.ws{width:100%;border-collapse:separate;border-spacing:0;background:var(--paper);border:1px solid var(--line);border-radius:14px;overflow:hidden;font-size:13.5px}
.ws th{background:var(--sage2);text-align:left;padding:11px 14px;font-size:11px;letter-spacing:.1em;text-transform:uppercase}
.ws td{padding:12px 14px;border-top:1px solid var(--line);height:34px}
.ws td.lab{font-weight:600;width:2.6in}
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.cmp>div{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:22px}
.cmp ol{margin:12px 0 0 18px;font-size:14px;line-height:1.6;color:var(--ink)}
.days{display:grid;gap:12px}
.day{display:grid;grid-template-columns:.9in 1fr;background:var(--paper);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.day .dn{background:var(--sage2);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'DMS';font-size:30px;color:var(--forest)}
.day .dn small{font-family:InterW;font-size:10px;letter-spacing:.14em;font-weight:700;color:var(--mute)}
.day>div:last-child{padding:14px 18px}
.pl{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.pl>div{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:18px 20px}
.pl ul{list-style:none;margin-top:8px}.pl li{font-size:13.5px;line-height:1.45;padding:6px 0 6px 20px;position:relative;border-top:1px dashed var(--line)}
.pl li:first-child{border-top:none}.pl li::before{content:'✦';position:absolute;left:0;color:var(--clay);font-size:11px;top:8px}
"""

THEMES = {
    "habit": "--forest:#3B2A1E;--clay:#C26A3D;--clay2:#F4DCCB;--sage:#B0643C;--sage2:#F1E4D8",
    "journal": "--forest:#2F2638;--clay:#B07FA0;--clay2:#EEDDE8;--sage:#8A6A9C;--sage2:#E9E1EF",
    "budget": "--forest:#1F3324;--clay:#C98B6B;--clay2:#F1DDCF;--sage:#3F7D5C;--sage2:#DDEBE1",
}

def build(key, title_small, guide_name, pages, out_name):
    total = len(pages)
    def head(n, label):
        dots = "".join(f'<i class="{"on" if i == n else ""}"></i>' for i in range(1, total + 1))
        return f'<div class="hd"><span>{title_small}</span><span class="dots">{dots}</span><span>{label}</span></div>'
    def foot(n):
        return f'<div class="ft"><span>SystemForge</span><span>{n:02d} / {total:02d}</span></div>'
    html_pages = []
    for i, (label, inner, cls) in enumerate(pages, 1):
        html_pages.append(f'<section class="pg {cls}">{head(i, label) if i > 1 else ""}{inner}{foot(i) if i > 1 else ""}</section>')
    css = BASE_CSS + EXTRA + ":root{" + THEMES[key] + "}"
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(html_pages)}</body></html>"
    out = ROOT / "products" / key
    out.mkdir(parents=True, exist_ok=True)
    hp = out / "guide.html"; hp.write_text(html)
    pdf = out / out_name
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{hp}');await p.waitForTimeout(400);await p.pdf({{path:'{pdf}',format:'Letter',printBackground:true}});await b.close();}})()"""
    subprocess.run(["node", "-e", js], check=True)
    hp.unlink()
    print(pdf)

def cover(tag, h1a, h1b, lead, items, foot):
    grid = "".join(f'<div><b>{i:02d}</b>{t}</div>' for i, t in enumerate(items, 1))
    return ("", f"""<div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div>
<div class="cvbrand"><span class="logo">SF</span>SystemForge</div>
<div class="cv"><div class="tag">{tag}</div><h1>{h1a}<br><em>{h1b}</em></h1><p class="cvlead">{lead}</p>
<div class="cvgrid">{grid}</div></div><div class="cvfoot">{foot}</div>""", "cover")

def chap(n, kick, title):
    return f'<div class="ch"><span class="big">{n:02d}</span><div><div class="kick">{kick}</div><h2>{title}</h2></div></div>'

def bands(rows):
    return '<div class="bands">' + "".join(
        f'<div class="band"><div class="bl"><span class="be">{e}</span><h4>{t}</h4><span class="time">{m}</span></div><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></div>'
        for t, m, e, li in rows) + '</div>'

def steps(rows):
    return '<div class="tl">' + "".join(f'<div class="st"><div class="dot">{i}</div><div><h4>{t}</h4><p>{d}</p></div></div>' for i, (t, d) in enumerate(rows, 1)) + '</div>'

def cards(rows):
    return '<div class="g6">' + "".join(f'<div class="c6"><div class="ic">{i}</div><h4>{t}</h4><p>{d}</p></div>' for i, t, d in rows) + '</div>'

def plist(cols):
    return '<div class="pl">' + "".join(f'<div><h4>{t}</h4><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></div>' for t, li in cols) + '</div>'

# ---------------- HABIT ----------------
habit_rows = ["💧 ____________", "📖 ____________", "🏃 ____________", "🧘 ____________", "📵 ____________", "😴 ____________"]
def tracker_grid(start):
    head = '<div class="grid30"><span></span>' + "".join(f'<span class="h">{d}</span>' for d in range(start, start + 10)) + '</div>'
    rows = "".join(f'<div class="grid30"><span class="n">{r}</span>' + '<span class="b"></span>' * 10 + '</div>' for r in habit_rows)
    return head + rows
H = [
    cover("Bonus guide · 30-day plan", "The 30-Day", "Habit Reset", "A simple plan to build habits that last, one small step at a time. Use it with your Habit Tracker.",
          ["Pick the right habits", "The habit loop", "Your 30-day plan", "When you miss a day", "Printable 30-day tracker"],
          "Print the last page and stick it on your fridge, or keep it next to your Notion tracker."),
    ("Chapter 01", chap(1, "Start small, start right", "Pick the right habits") + steps([
        ("Choose 6 habits, not 20", "Six is enough to change your days and few enough to tick in 10 seconds. Your tracker has 6 columns for this reason."),
        ("Mix easy and hard", "Pick 3 habits you already almost do (like drinking water) and 3 that stretch you. Early wins keep you going."),
        ("Make each one clear", "“Read” is vague. “Read 10 pages” is clear. You should know in one second if you did it."),
        ("Write the tiny version", "For each habit, write a 2-minute version for busy days: 1 page, 1 glass, a 5-minute walk."),
        ("Write why it matters", "One line per habit in My habit plan. On hard days, the why is what gets you to tick the box."),
    ]) + '<div class="note"><span>TIP</span><div>Rename the 6 columns in the Days database to your own habits. Everything else updates by itself.</div></div>', ""),
    ("Chapter 02", chap(2, "Cue, routine, reward", "The habit loop") + cards([
        ("⏰", "Cue", "Something that reminds you: a time, a place, or something you already do."),
        ("🔁", "Routine", "The habit itself. Keep it so small you can't say no."),
        ("🎁", "Reward", "Something you enjoy right after: coffee, music, ticking the box."),
        ("🔗", "Habit stacking", "Link a new habit to an old one: “After I pour my coffee, I drink a glass of water.”"),
        ("👀", "Make it visible", "Book on your pillow, shoes by the door, water bottle on your desk."),
        ("🧱", "Make it easy", "Remove the steps between you and the habit. Prepare tonight what you need tomorrow."),
    ]) + '<div class="quote">“After I ____________, I will ____________.” Write one for each habit.</div>', ""),
    ("Chapter 03", chap(3, "Four weeks, one step at a time", "Your 30-day plan") + bands([
        ("Week 1", "Days 1–7", "🌱", ["Do only the tiny versions", "Tick every day in Notion", "Notice when you forget", "Don't add new habits"]),
        ("Week 2", "Days 8–14", "🌿", ["Grow 1 or 2 habits a little", "Fix the cue for the hard ones", "Aim for 4 out of 6 a day", "Read your why on hard days"]),
        ("Week 3", "Days 15–21", "🌳", ["Keep the rhythm", "Try one ⭐ perfect day", "Check Monthly progress", "Write what helped"]),
        ("Week 4", "Days 22–30", "🏆", ["Look at your best habit", "Change the habit that isn't working", "Write a short Reflection", "Plan next month's Focus"]),
    ]) + '<div class="note green"><span>RULE</span><div>Progress, not perfection. A 4 out of 6 day is a good day.</div></div>', ""),
    ("Chapter 04", chap(4, "Bad days are part of it", "When you miss a day") + plist([
        ("“I forgot”", ["Move the cue somewhere you can't miss it", "Set one phone reminder at the same time", "Stack it on something you never skip"]),
        ("“I was too tired”", ["Do the tiny version only", "Move the habit earlier in the day", "Check your sleep habit first"]),
        ("“I got bored”", ["Change the place or the music", "Raise the goal a little", "Look back at your month to see how far you came"]),
        ("“I missed a whole week”", ["Don't start over from zero: start from today", "Go back to the tiny versions for 3 days", "Pick 3 habits instead of 6 for a while"]),
    ]) + '<div class="quote">Never miss twice. One missed day is normal. Two is the start of a new habit.</div>', ""),
    ("Printable", chap(5, "Print it, tick it", "30-day tracker") +
        '<p style="margin:-14px 0 18px">Write your 6 habits on the left. Colour a box each day you do it.</p>' +
        tracker_grid(1) + '<div style="height:14px"></div>' + tracker_grid(11) + '<div style="height:14px"></div>' + tracker_grid(21), ""),
]

# ---------------- JOURNAL ----------------
J = [
    cover("Bonus guide · 10-minute read", "Journaling for", "a calm mind", "Simple ways to write a little every day, even when you don't know what to say. Use it with your Daily Journal.",
          ["The 2-minute habit", "4 ways to journal", "Your weekly review", "Prompts for every mood", "Printable week page"],
          "Keep this guide next to your Notion journal. Pick one idea at a time."),
    ("Chapter 01", chap(1, "Small and easy beats long and rare", "The 2-minute habit") + steps([
        ("Same time every day", "Most people journal before bed. Pick a time and keep it. The habit matters more than the length."),
        ("Mood and energy first", "Two clicks. Even on days you write nothing else, your month chart keeps filling in."),
        ("One win", "Something you did, however small: you cooked, you called a friend, you went outside."),
        ("One thank you", "One person, moment or thing you're grateful for today."),
        ("More only if you want", "Open the entry and answer the daily questions when you have time. No pressure."),
    ]) + '<div class="note"><span>TIP</span><div>Add the journal to your phone’s home screen. Writing in bed takes 2 minutes.</div></div>', ""),
    ("Chapter 02", chap(2, "Pick the one that fits today", "4 ways to journal") + cards([
        ("🧠", "Brain dump", "Write everything on your mind for 5 minutes, without stopping. Then close it."),
        ("🙏", "Three good things", "Write 3 things that went well today and why they happened."),
        ("✉️", "Letter", "Write to someone (or your future self). You never have to send it."),
        ("❓", "One question", "Pick one prompt and write 3 lines. Done."),
        ("📸", "Snapshot", "Describe one moment with your 5 senses: what you saw, heard, smelled, felt."),
        ("🌱", "Tiny plan", "Write the one thing that would make tomorrow better."),
    ]), ""),
    ("Chapter 03", chap(3, "Five minutes every Sunday", "Your weekly review") + bands([
        ("Look back", "2 min", "👀", ["Read this week's entries", "Look at your average mood", "Find your best moment", "Find your hard moment"]),
        ("Learn", "2 min", "💡", ["What gave you energy?", "What drained you?", "What would you do again?", "Write one lesson"]),
        ("Look ahead", "1 min", "🧭", ["Pick one focus for next week", "Plan one thing to look forward to", "Rate your week", "Close the laptop"]),
    ]) + '<div class="note green"><span>WHY</span><div>Patterns show up after a few weeks: which days feel low, what helps, what doesn’t.</div></div>', ""),
    ("Chapter 04", chap(4, "Something to write for every day", "Prompts for every mood") + plist([
        ("😄 On a good day", ["What made today good, and how can I do it again?", "Who do I want to thank?", "What am I proud of?", "What do I want to remember?"]),
        ("😔 On a low day", ["What do I need right now?", "What is one small kind thing I can do for myself?", "What is still okay today?", "Who can I talk to?"]),
        ("😣 When stressed", ["What exactly is worrying me?", "What part can I control?", "What is one next step?", "What can wait until tomorrow?"]),
        ("😐 On a normal day", ["What surprised me today?", "What did I learn?", "What made me smile?", "What will I do differently tomorrow?"]),
    ]), ""),
    ("Printable", chap(5, "For days away from your screen", "My week on paper") +
        "".join(f'<div class="blk" style="padding:13px 20px;margin-bottom:10px"><h4>{d} &nbsp;<span style="font-weight:500;color:var(--mute)">Mood 😄 🙂 😐 😔 😣 &nbsp;·&nbsp; Win: ______________________ &nbsp;·&nbsp; Thanks: ______________________</span></h4></div>' for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]) +
        '<div class="blk"><h4>This week I learned…</h4><div class="lines"><div></div><div></div></div></div>', ""),
]

# ---------------- BUDGET ----------------
def ws(rows):
    return '<table class="ws"><tr><th>Category</th><th>Planned</th><th>Spent</th><th>Left</th></tr>' + "".join(f'<tr><td class="lab">{r}</td><td></td><td></td><td></td></tr>' for r in rows) + '</table>'
B = [
    cover("Bonus guide · 7-day plan", "Money Reset", "in 7 days", "A calm, step-by-step week to take control of your money. Use it with your Budget Planner.",
          ["Your 7-day plan", "Pick a budget style", "Pay off debt faster", "Build a safety cushion", "Printable budget worksheet"],
          "Not financial advice: a simple method to organize your own money. Adjust it to your life."),
    ("Chapter 01", chap(1, "One small step a day", "Your 7-day plan") + '<div class="days">' + "".join(
        f'<div class="day"><div class="dn"><small>DAY</small>{n}</div><div><h4>{t}</h4><p>{d}</p></div></div>' for n, t, d in [
            (1, "Find your real income", "Add your paychecks for one month in Transactions. Use what lands in your bank, after tax."),
            (2, "List every bill", "Add rent, phone, internet, insurance and every subscription in Bills & subscriptions with its due day."),
            (3, "Look at last month", "Add last month's spending in Transactions. Don't judge it, just see it."),
            (4, "Set your categories", "Give each category a Monthly budget. Start with needs, then savings, then wants."),
            (5, "List your debts", "Add each debt in Debt payoff with its balance, interest rate and minimum payment."),
            (6, "Pick one savings goal", "Start small: a $500 safety cushion. Add it in Savings goals with a deadline."),
            (7, "Plan your weekly check", "Pick a day (Sunday works well) for a 5-minute look at your Status column."),
        ]) + '</div>', ""),
    ("Chapter 02", chap(2, "There is no perfect budget", "Pick a budget style") + '<div class="cmp">' +
        '<div><div class="kick">Simple</div><h4>50 / 30 / 20</h4><p>Split your income after tax into three groups.</p><ol><li>About 50% for needs</li><li>About 30% for wants</li><li>About 20% for savings and debt</li></ol><p style="margin-top:12px">Best if you want a quick start and fewer numbers.</p></div>' +
        '<div><div class="kick">Detailed</div><h4>Every dollar has a job</h4><p>Plan every dollar before the month starts.</p><ol><li>Write your income</li><li>Give each category an amount</li><li>Keep going until $0 is left to plan</li></ol><p style="margin-top:12px">Best if money feels tight and you want full control.</p></div>' +
        '</div><div class="note"><span>EXAMPLE</span><div>With $3,000 a month after tax, 50/30/20 gives about $1,500 for needs, $900 for wants and $600 for savings and debt.</div></div>' +
        '<div class="note green"><span>TIP</span><div>Rent is high where you live? Try 60/20/20. The best budget is the one you can keep.</div></div>', ""),
    ("Chapter 03", chap(3, "Two methods that work", "Pay off debt faster") + '<div class="cmp">' +
        '<div><div class="kick">Saves the most interest</div><h4>Avalanche</h4><ol><li>Pay the minimum on every debt</li><li>Put every extra dollar on the highest interest rate</li><li>When it’s gone, move to the next highest</li></ol></div>' +
        '<div><div class="kick">Feels good fast</div><h4>Snowball</h4><ol><li>Pay the minimum on every debt</li><li>Put every extra dollar on the smallest balance</li><li>When it’s gone, roll its payment into the next one</li></ol></div>' +
        '</div><div class="blk" style="margin-top:20px"><h4>How the template helps</h4><p>Your Debt payoff table sorts by interest rate (avalanche order). Type an <b>Extra payment</b> and the <b>Payoff</b> column shows how many months are left and your debt-free month.</p></div>' +
        '<div class="note"><span>NOTE</span><div>Interest rates and terms differ. Check your real numbers with your lender.</div></div>', ""),
    ("Chapter 04", chap(4, "Your safety cushion", "Build an emergency fund") + steps([
        ("Start with $500", "A small cushion stops a flat tire from becoming new debt."),
        ("Then one month of needs", "Add up rent, food, bills and transport for one month. That's your next goal."),
        ("Then three months", "Three months of needs gives you room to breathe if something big happens."),
        ("Keep it separate", "Use a different savings account so you don't spend it by accident."),
        ("Automate it", "Move a fixed amount on payday, even $25. Update Saved in your Savings goals."),
    ]) + '<div class="quote">Pay yourself first: move money to savings on payday, before you spend.</div>', ""),
    ("Printable", chap(5, "For your monthly money date", "Budget worksheet") +
        '<p style="margin:-14px 0 14px">Month: ______________ &nbsp;&nbsp; Income after tax: $ ______________</p>' +
        ws(["🏠 Rent / mortgage", "🛒 Groceries", "💡 Bills & utilities", "🚌 Transport", "🛡️ Insurance", "🍽️ Eating out", "🛍️ Shopping", "📺 Subscriptions", "🎉 Fun", "💰 Savings", "📉 Extra debt payment", "Total"]) +
        '<div class="blk" style="margin-top:16px"><h4>One thing I’ll do differently this month</h4><div class="lines"><div></div></div></div>', ""),
]

build("habit", "Habit Tracker · 30-Day Habit Reset", "", H, "30-Day-Habit-Reset.pdf")
build("journal", "Daily Journal · Journaling for a calm mind", "", J, "Journaling-Guide.pdf")
build("budget", "Budget Planner · Money Reset in 7 Days", "", B, "Money-Reset-Guide.pdf")
