"""Bonus PDF for the Capsule Wardrobe Planner: Capsule Closet Guide (US Letter, 7 pages)."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "generator/mini_guides.py").read_text().split("# ---------------- HABIT ----------------")[0]
g = {"__file__": str(ROOT / "generator/mini_guides.py")}
exec(src, g)
g["THEMES"]["wardrobe"] = "--forest:#2E2433;--clay:#8C6A9E;--clay2:#EEE6F3;--sage:#A08A6E;--sage2:#F3EEE6"
cover, chap, steps, cards, bands, build = (g[k] for k in ("cover", "chap", "steps", "cards", "bands", "build"))
def ws(head, rows):
    return ('<table class="ws"><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>" +
            "".join(f'<tr><td class="lab">{r}</td>' + "<td></td>" * (len(head) - 1) + "</tr>" for r in rows) + "</table>")
P = [
    cover("Bonus guide · less clothes, more outfits", "Capsule", "Closet Guide",
          "Build a small closet you love, get dressed faster and spend less. Use it with your Capsule Wardrobe Planner.",
          ["Edit your closet", "Pick your colors", "The 30-piece capsule", "Make more outfits", "Shop smarter", "Printable outfit planner"],
          "No new clothes needed to start. Begin with what you own."),
    ("Chapter 01", chap(1, "Start with what you own", "Edit your closet") + steps([
        ("Take everything out", "One category at a time: tops first."),
        ("Make 3 piles", "Love it, maybe, let it go."),
        ("Try on the maybes", "Fit, feel, and would you buy it again today?"),
        ("Log the keepers", "Add them to My Closet with price and times worn."),
        ("Let go kindly", "Donate, sell or swap. Mark them in the planner."),
    ]), ""),
    ("Chapter 02", chap(2, "Everything matches", "Pick your colors") + bands([
        ("Base colors", "The backbone", "🤍", ["Black", "Navy", "Beige", "Gray"]),
        ("Accent colors", "The fun part", "💚", ["Green", "Pink", "Red", "Blue"]),
        ("Metals", "Pick one", "✨", ["Gold", "Silver", "Rose gold"]),
        ("Rule of thumb", "Easy mixing", "🎯", ["2–3 base", "1–2 accents", "Every top fits 2 bottoms"]),
    ]), ""),
    ("Chapter 03", chap(3, "A simple starting point", "The 30-piece capsule") + cards([
        ("👕", "9 tops", "Tees, shirts, sweaters, one blouse."),
        ("👖", "6 bottoms", "Jeans, trousers, a skirt, something comfy."),
        ("👗", "3 dresses", "One casual, one smart, one for going out."),
        ("🧥", "4 layers", "Coat, blazer, jacket, cardigan."),
        ("👟", "5 shoes", "Sneakers, boots, flats, sandals, heels."),
        ("👜", "3 extras", "A tote, a small bag, a scarf."),
    ]), ""),
    ("Chapter 04", chap(4, "Mix and match", "Make more outfits") + steps([
        ("Start with one piece", "Pick the piece you wear least."),
        ("Add 2 bottoms", "Try it with two different bottoms."),
        ("Change the layer", "Same outfit, different jacket = new look."),
        ("Swap the shoes", "Sneakers for day, boots for night."),
        ("Save it", "Add every good combo to Outfits so you never forget it."),
    ]), ""),
    ("Chapter 05", chap(5, "Buy less, choose well", "Shop smarter") + cards([
        ("⏳", "Wait 2 weeks", "Put it on your Wishlist first."),
        ("🧮", "Cost per wear", "Price ÷ wears. Aim for 30+ wears."),
        ("🧩", "3-piece rule", "It must go with 3 things you own."),
        ("📏", "Fit today", "Buy for the body you have now."),
        ("🔁", "One in, one out", "Something new in, something old out."),
        ("🧼", "Easy care", "Machine-wash pieces get worn more."),
    ]), ""),
    ("Printable", chap(6, "Plan the week", "Weekly outfit planner") +
        ws(["Day", "Top", "Bottom", "Layer", "Shoes", "Extra"], ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]) +
        '<div class="blk" style="margin-top:16px"><h4>Pieces to style next week</h4><div class="lines"><div></div><div></div></div></div>', ""),
]
build("wardrobe", "Capsule Wardrobe Planner · Capsule Closet Guide", "", P, "Capsule-Closet-Guide.pdf")
