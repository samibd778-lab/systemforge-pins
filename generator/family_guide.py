"""Bonus PDF for the Mom & Family Planner: Calm Family Week Guide (US Letter, 7 pages)."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "generator/mini_guides.py").read_text().split("# ---------------- HABIT ----------------")[0]
g = {"__file__": str(ROOT / "generator/mini_guides.py")}
exec(src, g)
g["THEMES"]["family"] = "--forest:#3A2A22;--clay:#D07A4E;--clay2:#F8E6DB;--sage:#6F9A86;--sage2:#E5F0EA"
cover, chap, steps, cards, bands, build = (g[k] for k in ("cover", "chap", "steps", "cards", "bands", "build"))
def ws(head, rows):
    return ('<table class="ws"><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>" +
            "".join(f'<tr><td class="lab">{r}</td>' + "<td></td>" * (len(head) - 1) + "</tr>" for r in rows) + "</table>")
P = [
    cover("Bonus guide · busy family, calm mom", "Calm Family", "Week Guide",
          "Plan the week in 20 minutes, share the load, and keep a little time for you. Use it with your Mom & Family Planner.",
          ["The Sunday reset", "Meal planning made easy", "Chores kids can do", "Mornings without the rush", "Time for you", "Printable weekly plan"],
          "Every family is different. Take what helps and skip the rest."),
    ("Chapter 01", chap(1, "20 minutes on Sunday", "The Sunday reset") + steps([
        ("Check the calendar", "Look at the week: school, activities, appointments."),
        ("Plan who drives", "Write it on each event so nobody has to ask."),
        ("Pick the meals", "5 dinners, 1 leftovers night, 1 easy night."),
        ("Reset chores", "Give rewards, then set every chore back to To do."),
        ("Book your me-time", "Put one thing just for you in the calendar."),
    ]), ""),
    ("Chapter 02", chap(2, "Less thinking at 5 pm", "Meal planning made easy") + bands([
        ("Theme nights", "Fewer decisions", "🌮", ["Taco Monday", "Pasta Tuesday", "Soup Wednesday", "Pizza Friday"]),
        ("Busy nights", "15 minutes or less", "⏱️", ["Wraps", "Eggs & toast", "Leftovers", "Freezer meal"]),
        ("Cook once", "Eat twice", "🍲", ["Chili", "Roast chicken", "Pasta sauce", "Soup"]),
        ("Kids help", "Small jobs", "🧒", ["Wash veggies", "Stir", "Set the table", "Pick a fruit"]),
    ]), ""),
    ("Chapter 03", chap(3, "Many hands", "Chores kids can do") + cards([
        ("🧸", "Ages 3–5", "Put toys away, feed a pet, match socks."),
        ("🛏️", "Ages 6–8", "Make the bed, set the table, water plants."),
        ("🧺", "Ages 9–12", "Fold laundry, take out trash, help cook."),
        ("🧽", "Teens", "Do laundry, clean the bathroom, cook a meal."),
        ("⭐", "Use points", "Bigger chores get more points. Pick a weekly reward."),
        ("🙏", "Notice the effort", "Say thank you. It matters more than perfect."),
    ]), ""),
    ("Chapter 04", chap(4, "Start the day calm", "Mornings without the rush") + steps([
        ("Prep at night", "Bags packed, clothes out, lunch ready."),
        ("Wake up first", "Even 15 minutes before the kids changes the day."),
        ("Same order every day", "Dress, breakfast, teeth, shoes, go."),
        ("A launch spot by the door", "Keys, bags and shoes in one place."),
        ("Leave 10 minutes early", "Buffer time beats rushing."),
    ]), ""),
    ("Chapter 05", chap(5, "You matter too", "Time for you") + cards([
        ("☕", "5 minutes", "A hot drink while it's still hot."),
        ("🚶", "15 minutes", "A short walk alone."),
        ("📖", "30 minutes", "Read, nap or call a friend."),
        ("🧘", "1 hour", "A class, a hobby, coffee out."),
        ("🤝", "Trade time", "Swap kid duty with your partner or a friend."),
        ("🗓️", "Book it", "If it's in the calendar, it happens."),
    ]), ""),
    ("Printable", chap(6, "Stick it on the fridge", "Weekly family plan") +
        ws(["", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], ["Events", "Who drives", "Dinner", "Chores", "Me-time"]) +
        '<div class="blk" style="margin-top:16px"><h4>This week we are grateful for</h4><div class="lines"><div></div><div></div></div></div>', ""),
]
build("family", "Mom & Family Planner · Calm Family Week Guide", "", P, "Calm-Family-Week-Guide.pdf")
