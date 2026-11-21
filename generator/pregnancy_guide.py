"""Bonus PDF for the Pregnancy & Baby Planner: Calm Baby Prep Guide (US Letter, 7 pages)."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "generator/mini_guides.py").read_text().split("# ---------------- HABIT ----------------")[0]
g = {"__file__": str(ROOT / "generator/mini_guides.py")}
exec(src, g)
g["THEMES"]["pregnancy"] = "--forest:#3B2A33;--clay:#C07A8E;--clay2:#F7E6EB;--sage:#6E8A86;--sage2:#E3ECEA"
cover, chap, steps, cards, bands, build = (g[k] for k in ("cover", "chap", "steps", "cards", "bands", "build"))
def ws(head, rows):
    return ('<table class="ws"><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>" +
            "".join(f'<tr><td class="lab">{r}</td>' + "<td></td>" * (len(head) - 1) + "</tr>" for r in rows) + "</table>")
P = [
    cover("Bonus guide · get ready, calmly", "The Calm", "Baby Prep Guide",
          "A simple to-do list for each stage, so you feel ready without the stress. Use it with your Pregnancy & Baby Planner.",
          ["Your trimester to-do list", "Smart baby shopping", "Set up the nursery", "Pack the hospital bag", "Plan the first weeks", "Printable newborn tracker"],
          "This guide helps you get organized. It is not medical advice: always follow your doctor or midwife."),
    ("Chapter 01", chap(1, "One stage at a time", "Your trimester to-do list") + bands([
        ("1st trimester", "Get set up", "🌱", ["Book first visit", "Add your due date", "Start a baby budget", "Write your questions"]),
        ("2nd trimester", "Plan and shop", "🛍️", ["Make a shopping list", "Sign up for a class", "Plan the nursery", "Pick a pediatrician"]),
        ("3rd trimester", "Get ready", "👜", ["Pack the hospital bag", "Install the car seat", "Freeze some meals", "Tour the hospital"]),
        ("After birth", "Rest and log", "👶", ["Log feeds and sleep", "Accept help", "Book baby checkups", "Rest when you can"]),
    ]), ""),
    ("Chapter 02", chap(2, "Spend on what you need", "Smart baby shopping") + cards([
        ("✅", "Must have first", "Buy the must-haves. Wait on the nice-to-haves."),
        ("🎁", "Plan for gifts", "Mark items as Gift so you don't buy them twice."),
        ("🤝", "Borrow and swap", "Friends often have baby gear they don't use anymore."),
        ("🏷️", "Track every price", "Your planner adds it up and shows money left."),
        ("📏", "Small sizes go fast", "Buy a few newborn clothes, more in the next size."),
        ("🛡️", "New car seat", "Safety gear is worth buying new and checking the rules."),
    ]), ""),
    ("Chapter 03", chap(3, "A calm, simple space", "Set up the nursery") + steps([
        ("Start with sleep", "A safe crib and mattress come first."),
        ("Make a changing spot", "Diapers, wipes and a pad all within reach."),
        ("Add a comfy chair", "For night feeds. Add a small lamp."),
        ("Keep it simple", "Fewer things means less to clean and tidy."),
        ("Wash the basics", "Clothes, sheets and swaddles, ready to use."),
    ]), ""),
    ("Chapter 04", chap(4, "Ready by the door", "Pack the hospital bag") + cards([
        ("🪪", "Papers", "ID, insurance card and your birth preferences."),
        ("👚", "For you", "Robe, loose clothes, toiletries and a long charger."),
        ("👶", "For baby", "Going-home outfit, hat, socks and a blanket."),
        ("🥨", "Snacks", "Easy snacks and a water bottle for both of you."),
        ("🚗", "Car seat", "Installed before your due date."),
        ("📞", "Call list", "Who to call, and in what order."),
    ]), ""),
    ("Chapter 05", chap(5, "Help makes it easier", "Plan the first weeks") + steps([
        ("Freeze meals", "Six to eight easy dinners save a lot of energy."),
        ("Share a help list", "Meals, laundry, pets, rides. Give people a clear job."),
        ("Keep a simple log", "Feeds, sleep and diapers help at baby checkups."),
        ("Protect your rest", "Short visits, phone on silent, naps when you can."),
        ("Speak up", "Tell your doctor and someone close if you feel low or worried."),
    ]), ""),
    ("Printable", chap(6, "Tick as you go", "Newborn daily tracker") +
        ws(["Time", "Feed (L / R / bottle)", "Minutes or oz", "Diaper", "Sleep"], ["", "", "", "", "", "", "", "", "", "", "", ""]) +
        '<div class="blk" style="margin-top:16px"><h4>Notes for the next checkup</h4><div class="lines"><div></div><div></div></div></div>', ""),
]
build("pregnancy", "Pregnancy & Baby Planner · Calm Baby Prep Guide", "", P, "Calm-Baby-Prep-Guide.pdf")
