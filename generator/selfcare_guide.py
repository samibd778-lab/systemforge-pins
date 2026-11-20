"""Bonus PDF for the Self-Care & Wellness Planner: Gentle Reset Guide (US Letter, 7 pages).
Run: python3 generator/selfcare_guide.py -> products/selfcare/Gentle-Reset-Guide.pdf
"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "generator/mini_guides.py").read_text().split("# ---------------- HABIT ----------------")[0]
g = {"__file__": str(ROOT / "generator/mini_guides.py")}
exec(src, g)
g["THEMES"]["selfcare"] = "--forest:#22332D;--clay:#5E8C7A;--clay2:#E0EEE8;--sage:#A0703F;--sage2:#F3E7DA"
cover, chap, steps, cards, bands, build = (g[k] for k in ("cover", "chap", "steps", "cards", "bands", "build"))

def ws(head, rows):
    return ('<table class="ws"><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>" +
            "".join(f'<tr><td class="lab">{r}</td>' + "<td></td>" * (len(head) - 1) + "</tr>" for r in rows) + "</table>")

P = [
    cover("Bonus guide · take care of you", "The Gentle Reset", "Guide",
          "Small, simple ways to rest, recharge and feel more like yourself. Use it with your Self-Care & Wellness Planner.",
          ["The 6 daily basics", "Build your self-care menu", "Match care to your energy", "A 4-week reset plan", "The Sunday reset", "Printable weekly tracker"],
          "You don't need a perfect routine. Pick one idea and try it this week."),
    ("Chapter 01", chap(1, "Six small things, every day", "The daily basics") + cards([
        ("😴", "Sleep", "Aim for 7 hours or more. Same bedtime most nights helps."),
        ("💧", "Water", "8 cups is the planner's goal. Keep a bottle where you can see it."),
        ("🚶", "Move", "A walk, a stretch, a dance. Any movement counts."),
        ("🌳", "Outside", "A few minutes of fresh air and daylight."),
        ("📵", "Screen-free hour", "One hour a day with the phone in another room."),
        ("🌿", "One ritual", "Something from your self-care menu, even 5 minutes."),
    ]), ""),
    ("Chapter 02", chap(2, "Your go-to list for hard days", "Build your self-care menu") + steps([
        ("Write what already helps", "Think of the last time you felt calm. What were you doing?"),
        ("Add one for each area", "Mind, Body, Rest, Social and Joy. Variety keeps it fresh."),
        ("Include tiny ones", "Have a few 5-minute rituals for busy days."),
        ("Write the how-to", "One line on how to do it, so tired-you doesn't have to think."),
        ("Star your favorites", "Tick Favorite on the ones that work best for you."),
    ]), ""),
    ("Chapter 03", chap(3, "Low energy? Start small", "Match care to your energy") + cards([
        ("🪫", "Low energy", "Box breathing, an early night, a warm shower. Gentle and easy."),
        ("🔋", "Medium energy", "A walk outside, a call with a friend, tidy one small space."),
        ("⚡", "High energy", "Cook a cozy meal, dance to 3 songs, a longer workout."),
        ("📝", "Check in first", "Log your mood and energy, then pick from the menu."),
        ("🤍", "Be kind", "An okay day is fine. Rest is part of self-care too."),
        ("🔎", "Look for patterns", "Your Weekly Reset shows what helped on hard days."),
    ]), ""),
    ("Chapter 04", chap(4, "One step at a time", "A 4-week reset plan") + bands([
        ("Week 1", "Notice", "🌱", ["Daily check-in", "Log sleep and water", "Write one grateful line", "No changes yet"]),
        ("Week 2", "Basics", "💧", ["8 cups of water", "Same bedtime", "A short walk daily", "One ritual a day"]),
        ("Week 3", "Unplug", "📵", ["Screen-free hour", "Phone out of the bedroom", "Time outside", "Call a friend"]),
        ("Week 4", "Keep it", "🏆", ["Pick your top 3 habits", "Update your menu", "Weekly Reset review", "Celebrate"]),
    ]), ""),
    ("Chapter 05", chap(5, "20 minutes on Sunday", "The Sunday reset") + steps([
        ("Look back", "Open the Weekly Reset. Read your average mood, sleep and self-care score."),
        ("Name your wins", "Write 2 or 3 good things, even small ones."),
        ("Be honest about hard moments", "What was hard, and what helped you through it?"),
        ("Pick one intention", "One small thing to try next week. Just one."),
        ("Plan a treat", "Put one Joy ritual in your calendar for the week."),
    ]) + '<p style="margin-top:14px;font-size:11px;color:#777">This guide shares everyday wellness ideas. It is not medical or mental health advice. If you are struggling, please talk to a doctor or a professional you trust.</p>', ""),
    ("Printable", chap(6, "Tick the boxes as you go", "My weekly self-care tracker") +
        ws(["Day", "Sleep 7h+", "8 cups", "Moved", "Outside", "Screen-free", "Ritual"], ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]) +
        '<div class="blk" style="margin-top:16px"><h4>This week I\'m grateful for</h4><div class="lines"><div></div><div></div><div></div></div></div>', ""),
]
build("selfcare", "Self-Care & Wellness Planner · Gentle Reset Guide", "", P, "Gentle-Reset-Guide.pdf")
