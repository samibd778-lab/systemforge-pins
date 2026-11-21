"""Bonus PDF for the Wedding Planner: Stress-Free Wedding Guide (US Letter, 7 pages)."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "generator/mini_guides.py").read_text().split("# ---------------- HABIT ----------------")[0]
g = {"__file__": str(ROOT / "generator/mini_guides.py")}
exec(src, g)
g["THEMES"]["wedding"] = "--forest:#3A2630;--clay:#B5677D;--clay2:#F6E3E9;--sage:#8A7A5A;--sage2:#EFEADF"
cover, chap, steps, cards, bands, build = (g[k] for k in ("cover", "chap", "steps", "cards", "bands", "build"))
def ws(head, rows):
    return ('<table class="ws"><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>" +
            "".join(f'<tr><td class="lab">{r}</td>' + "<td></td>" * (len(head) - 1) + "</tr>" for r in rows) + "</table>")
P = [
    cover("Bonus guide · plan with less stress", "The Stress-Free", "Wedding Guide",
          "A simple plan for your budget, your guests and your big day. Use it with your Wedding Planner.",
          ["Start with 3 numbers", "A 12-month timeline", "Budget without stress", "Guests and seating", "Choosing vendors", "Printable day-of plan"],
          "You don't need to do it all at once. One task a week is enough."),
    ("Chapter 01", chap(1, "Before you book anything", "Start with 3 numbers") + steps([
        ("Your total budget", "Agree on one number together. Write it in Our Wedding."),
        ("Your guest count", "A rough number is fine. It decides the venue and the catering."),
        ("Your date or season", "Popular dates book fast. Being flexible can save money."),
        ("Your top 3", "Pick the 3 things that matter most to you both. Spend more there."),
        ("Your no-go list", "Write what you don't want. It makes every choice easier."),
    ]), ""),
    ("Chapter 02", chap(2, "One step at a time", "A 12-month timeline") + bands([
        ("12-9 months", "The big pieces", "🏡", ["Budget and guest list", "Book the venue", "Book photographer", "Book the caterer"]),
        ("9-4 months", "The details", "💐", ["Save-the-dates", "Florist and music", "Dress or suit", "Cake tasting"]),
        ("3-1 months", "The final plan", "✉️", ["Send invitations", "Final headcount", "Seating chart", "Last fittings"]),
        ("The week of", "Calm and ready", "💍", ["Confirm all vendors", "Pack the kit", "Share the schedule", "Rest"]),
    ]), ""),
    ("Chapter 03", chap(3, "Know where every dollar goes", "Budget without stress") + cards([
        ("📝", "Estimate first", "Put a price on every item before you book anything."),
        ("🔁", "Then update", "When you get the real price, put it in Actual."),
        ("💳", "Track deposits", "Log every payment and the date the rest is due."),
        ("🧯", "Keep a cushion", "Leave about 5% to 10% free for surprises."),
        ("✂️", "Cut smart", "Fewer guests saves more than smaller flowers."),
        ("🤝", "Ask about packages", "Many vendors have lower prices for off-peak days."),
    ]), ""),
    ("Chapter 04", chap(4, "Everyone has a seat", "Guests and seating") + steps([
        ("List everyone first", "Add all names, then cut. It's easier than adding later."),
        ("Decide on plus ones", "Pick one rule for everyone, so no one feels left out."),
        ("Track the RSVPs", "Change RSVP as answers come in and follow the Next step."),
        ("Seat by groups", "Family, friends and work tables make the chart quick."),
        ("Send thank-you cards", "Log each gift and tick Thank-you sent when it's done."),
    ]), ""),
    ("Chapter 05", chap(5, "Pick the right team", "Choosing vendors") + cards([
        ("🔎", "Compare three", "Get at least 3 quotes for the big vendors."),
        ("📄", "Get it in writing", "Prices, hours and what's included, in a contract."),
        ("❓", "Ask the questions", "Use the Questions to Ask Vendors page in your planner."),
        ("⭐", "Check real work", "Ask to see a full wedding, not only the best photos."),
        ("📅", "Note every date", "Deposit, final payment and arrival time."),
        ("☎️", "Confirm the week of", "Call each vendor and confirm times and address."),
    ]), ""),
    ("Printable", chap(6, "Fill it in and share it", "My wedding day plan") +
        ws(["Time", "What happens", "Who", "Where", "Notes"], ["", "", "", "", "", "", "", "", "", ""]) +
        '<div class="blk" style="margin-top:16px"><h4>Who to call on the day</h4><div class="lines"><div></div><div></div><div></div></div></div>', ""),
]
build("wedding", "Wedding Planner · Stress-Free Wedding Guide", "", P, "Stress-Free-Wedding-Guide.pdf")
