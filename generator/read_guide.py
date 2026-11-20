"""Bonus PDF for the Reading Journal: Read More Playbook (US Letter, 7 pages).
Run: python3 generator/read_guide.py -> products/read/Read-More-Playbook.pdf
"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "generator/mini_guides.py").read_text().split("# ---------------- HABIT ----------------")[0]
g = {"__file__": str(ROOT / "generator/mini_guides.py")}
exec(src, g)
g["THEMES"]["read"] = "--forest:#2E2620;--clay:#A0703F;--clay2:#F1E3D0;--sage:#5B6E5A;--sage2:#E2E9E0"
cover, chap, steps, cards, bands, build = (g[k] for k in ("cover", "chap", "steps", "cards", "bands", "build"))

def ws(head, rows):
    return ('<table class="ws"><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>" +
            "".join(f'<tr><td class="lab">{r}</td>' + "<td></td>" * (len(head) - 1) + "</tr>" for r in rows) + "</table>")

P = [
    cover("Bonus guide · read more", "The Read More", "Playbook",
          "Simple ways to read more books, remember what you read and enjoy every page. Use it with your Reading Journal.",
          ["Find time to read", "Pick books you'll finish", "Remember what you read", "30-day reading challenge", "Host a book club", "Printable book log"],
          "Pick one idea from this guide and try it this week. Small changes add up to many books."),
    ("Chapter 01", chap(1, "You have more time than you think", "Find time to read") + cards([
        ("📖", "10 pages a day", "That is about a dozen books a year. Small and steady wins."),
        ("🛏️", "Before bed", "Swap 15 minutes of scrolling for a book. A calm end to the day."),
        ("🚌", "In the gaps", "Lunch, the bus, waiting rooms. Keep a book or ebook with you."),
        ("🎧", "Listen", "Audiobooks for walks, chores and drives. They count."),
        ("📵", "Phone away", "Out of the room while you read. Fewer pings, longer focus."),
        ("📌", "Same time daily", "Tie reading to a habit you already have, like morning coffee."),
    ]), ""),
    ("Chapter 02", chap(2, "Choose books you'll actually finish", "Pick the right book") + steps([
        ("Read what you want", "Not what you think you should. Enjoyment keeps you reading."),
        ("Try the first page", "Read page 1 of three books, then pick the one that pulls you in."),
        ("Mix it up", "Follow a long book with a short one, fiction with non-fiction."),
        ("Ask people you trust", "Note who recommended each book in Recommended by."),
        ("Quit freely", "Not hooked after 50 pages? Mark it Did not finish and move on."),
    ]), ""),
    ("Chapter 03", chap(3, "Keep the best parts", "Remember what you read") + cards([
        ("✍️", "Save one quote", "One line per book in Quotes & Notes. It brings the whole book back."),
        ("🗣️", "Tell someone", "Explain the book to a friend in 2 minutes. You'll remember it."),
        ("🧠", "3 big ideas", "For non-fiction, write the 3 main ideas when you finish."),
        ("⭐", "Rate right away", "Rate and review on the day you finish, while it's fresh."),
        ("❓", "Ask questions", "Save questions as you read. Great for book clubs."),
        ("🔁", "Look back monthly", "The Monthly reading review keeps your favorites close."),
    ]), ""),
    ("Chapter 04", chap(4, "Build the habit in a month", "30-day reading challenge") + bands([
        ("Week 1", "Start small", "🌱", ["10 pages a day", "Pick one cozy spot", "Log each session", "Phone in another room"]),
        ("Week 2", "Add a slot", "⏰", ["Read before bed too", "Try one audiobook", "Save 3 quotes", "Finish book 1"]),
        ("Week 3", "Go deeper", "📚", ["20 pages a day", "Try a new genre", "Write a 3-line review", "Tell a friend"]),
        ("Week 4", "Make it yours", "🏆", ["Set a yearly goal", "Plan next month's books", "Check your challenge", "Celebrate"]),
    ]), ""),
    ("Chapter 05", chap(5, "Read together", "Host a book club") + steps([
        ("Pick the book early", "Choose 4 weeks ahead so everyone has time to finish."),
        ("Keep it small", "4 to 8 people is perfect. Everyone gets to talk."),
        ("Start light", "One word to describe the book, from each person."),
        ("Use good questions", "The Book Club Kit page has 10 that work for any book."),
        ("Choose the next one together", "End the meeting by picking next month's book."),
    ]), ""),
    ("Printable", chap(6, "Fill it as you go", "My book log") +
        ws(["Title", "Author", "Finished", "Rating", "Best line"], [str(i) for i in range(1, 11)]) +
        '<div class="blk" style="margin-top:16px"><h4>Books I want to read next</h4><div class="lines"><div></div><div></div></div></div>', ""),
]
build("read", "Reading Journal · Read More Playbook", "", P, "Read-More-Playbook.pdf")
