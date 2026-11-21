"""Bonus PDF for the Skincare & Beauty Routine: Glow Routine Guide (US Letter, 7 pages)."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "generator/mini_guides.py").read_text().split("# ---------------- HABIT ----------------")[0]
g = {"__file__": str(ROOT / "generator/mini_guides.py")}
exec(src, g)
g["THEMES"]["skin"] = "--forest:#3E2A24;--clay:#C08872;--clay2:#F6E6DF;--sage:#8A9A7A;--sage2:#EDF1E8"
cover, chap, steps, cards, bands, build = (g[k] for k in ("cover", "chap", "steps", "cards", "bands", "build"))
def ws(head, rows):
    return ('<table class="ws"><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>" +
            "".join(f'<tr><td class="lab">{r}</td>' + "<td></td>" * (len(head) - 1) + "</tr>" for r in rows) + "</table>")
P = [
    cover("Bonus guide · simple skincare", "Glow Routine", "Guide",
          "A simple routine you can keep, products you understand, and a skin log that shows what works. Use it with your Skincare & Beauty Routine.",
          ["Build your routine", "The right order", "Read a label", "Add new products safely", "Habits that help", "Printable 4-week log"],
          "For everyday routines only. Not medical advice. See a dermatologist for skin concerns."),
    ("Chapter 01", chap(1, "Start simple", "Build your routine") + steps([
        ("List what you own", "Add each product to My Products with the date you opened it."),
        ("Pick the basics", "Cleanser, moisturizer and sunscreen. Everything else is extra."),
        ("Set the order", "Add your steps to Morning and Evening in Routine Steps."),
        ("Keep it short", "A 3-step routine you do beats a 10-step one you skip."),
        ("Log daily", "30 seconds in the Skin Log shows what really works."),
    ]), ""),
    ("Chapter 02", chap(2, "Thin to thick", "The right order") + bands([
        ("Morning", "Protect", "☀️", ["Cleanser", "Toner", "Serum", "Moisturizer", "Sunscreen"]),
        ("Evening", "Repair", "🌙", ["Remove makeup", "Cleanser", "Serum", "Moisturizer"]),
        ("Weekly", "Treat", "✨", ["Exfoliate 1–2x", "Face mask", "Wash brushes", "Fresh pillowcase"]),
        ("Short on time", "The minimum", "⏱️", ["Cleanse", "Moisturize", "Sunscreen (AM)"]),
    ]), ""),
    ("Chapter 03", chap(3, "No more guessing", "Read a label") + cards([
        ("🫙", "Open-jar icon", "12M means use within 12 months after opening."),
        ("📋", "Ingredient order", "Ingredients are listed from most to least."),
        ("💧", "Hydrating", "Look for glycerin or hyaluronic acid."),
        ("🧱", "Barrier", "Ceramides help support the skin barrier."),
        ("☀️", "SPF number", "Choose broad spectrum for daily use."),
        ("🌸", "Fragrance", "Sensitive skin? Try fragrance-free first."),
    ]), ""),
    ("Chapter 04", chap(4, "Go slow", "Add new products safely") + steps([
        ("One at a time", "Never start two new products in the same week."),
        ("Patch test", "Behind the ear or inner arm, wait 24 to 48 hours."),
        ("Start slowly", "2 to 3 times a week, then more if your skin is happy."),
        ("Watch your log", "Note any change in the Skin Log."),
        ("Rate after 4–6 weeks", "Then decide: rebuy, keep or let it go."),
    ]), ""),
    ("Chapter 05", chap(5, "Beyond the bottle", "Habits that help") + cards([
        ("😴", "Sleep", "Rested skin often looks brighter."),
        ("💧", "Water", "Keep a bottle where you can see it."),
        ("🧺", "Clean fabrics", "Fresh pillowcases and towels each week."),
        ("📱", "Clean phone", "Wipe your screen a few times a week."),
        ("🙌", "Hands off", "Try not to touch or pick at your face."),
        ("🩺", "Ask an expert", "A dermatologist is the right person for skin concerns."),
    ]), ""),
    ("Printable", chap(6, "Tick each day", "4-week skin log") +
        ws(["Week", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], ["Week 1", "Week 2", "Week 3", "Week 4"]) +
        '<div class="blk" style="margin-top:16px"><h4>What I noticed this month</h4><div class="lines"><div></div><div></div><div></div></div></div>', ""),
]
build("skin", "Skincare & Beauty Routine · Glow Routine Guide", "", P, "Glow-Routine-Guide.pdf")
