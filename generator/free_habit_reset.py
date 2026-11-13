"""Free lead-magnet version of the 30-Day Habit Reset (Gumroad $0 product).
Same guide as the paid bonus, but it works on paper (no Notion steps) and ends with a page about the
Habit Tracker for Notion, linked to its Gumroad page.
Run: python3 generator/free_habit_reset.py -> dl/habit-free/30-Day-Habit-Reset-Free.pdf"""
import base64, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "generator/mini_guides.py").read_text()
src = src[:src.index("# ---------------- JOURNAL")]
g = {"__file__": str(ROOT / "generator/mini_guides.py")}
exec(compile(src, "mini_guides_part", "exec"), g)
H = g["H"]

SWAP = [
    ("Bonus guide · 30-day plan", "Free guide · 30-day plan"),
    ("Use it with your Habit Tracker.", "All you need is a pen and the printable tracker inside."),
    ("Print the last page and stick it on your fridge, or keep it next to your Notion tracker.", "Print page 6 and stick it on your fridge. Tick a box every day."),
    ("Your tracker has 6 columns for this reason.", "The printable tracker has 6 rows for this reason."),
    ("One line per habit in My habit plan.", "One line per habit, on a sticky note or in your phone."),
    ("Rename the 6 columns in the Days database to your own habits. Everything else updates by itself.",
     "Write your 6 habits on the printable tracker before you start. Keep it where you see it every day."),
    ("Tick every day in Notion", "Tick every day on your tracker"),
    ("Check Monthly progress", "Count your ticks so far"),
]
def fix(t):
    for a, b in SWAP:
        t = t.replace(a, b)
    return t
H = [(fix(a), fix(b), c) for a, b, c in H]
for a, b in SWAP:
    assert any(b in x[0] or b in x[1] for x in H), "not replaced: " + a

shot = base64.b64encode((ROOT / "shots/hd3/habit-week.jpg").read_bytes()).decode()
URL = "https://getsystemforge.gumroad.com/l/habit-tracker?utm_source=gumroad&utm_medium=free-pdf&utm_campaign=habit-reset"
upsell = ("Next step", g["chap"](6, "Want it to track itself?", "Habit Tracker for Notion") +
    '<p style="margin:-14px 0 16px">The same 30-day method, in Notion. Tick a box and the rest fills in by itself.</p>'
    f'<img src="data:image/jpeg;base64,{shot}" style="width:100%;border:1px solid var(--line);border-radius:14px;margin-bottom:18px">'
    + g["plist"]([
        ("Every day", ["Tick 6 habits in 10 seconds", "Your score and day type fill in by themselves", "Works on your phone too"]),
        ("Every month and year", ["A bar for every habit", "Your best habit and your ⭐ perfect days", "Your whole year in one line"]),
    ]) +
    f'<div class="note green" style="margin-top:18px"><span>GET IT</span><div><a href="{URL}" style="color:inherit;font-weight:700">'
    'getsystemforge.gumroad.com/l/habit-tracker</a><br>Includes a habit plan, 50 habit ideas and this guide.</div></div>', "")
H.append(upsell)

g["build"]("habit", "30-Day Habit Reset · Free guide", "", H, "30-Day-Habit-Reset-Free.pdf")
out = ROOT / "dl/habit-free"; out.mkdir(parents=True, exist_ok=True)
shutil.move(str(ROOT / "products/habit/30-Day-Habit-Reset-Free.pdf"), str(out / "30-Day-Habit-Reset-Free.pdf"))
print(out / "30-Day-Habit-Reset-Free.pdf")
