"""Bonus PDF for the Home & Cleaning Planner: Calm Home Cleaning Guide (US Letter, 7 pages)."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "generator/mini_guides.py").read_text().split("# ---------------- HABIT ----------------")[0]
g = {"__file__": str(ROOT / "generator/mini_guides.py")}
exec(src, g)
g["THEMES"]["home"] = "--forest:#22364A;--clay:#4F7FA3;--clay2:#E2ECF4;--sage:#6E9A7E;--sage2:#E6F0E9"
cover, chap, steps, cards, bands, build = (g[k] for k in ("cover", "chap", "steps", "cards", "bands", "build"))
def ws(head, rows):
    return ('<table class="ws"><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>" +
            "".join(f'<tr><td class="lab">{r}</td>' + "<td></td>" * (len(head) - 1) + "</tr>" for r in rows) + "</table>")
P = [
    cover("Bonus guide · a calmer home", "Calm Home", "Cleaning Guide",
          "Small tasks, done on time, shared by everyone. Use it with your Home & Cleaning Planner.",
          ["Set up your home", "Daily, weekly, monthly", "Share the work", "Speed-clean any room", "Keep up with home jobs", "Printable weekly chart"],
          "Always read product labels. Never mix cleaning products."),
    ("Chapter 01", chap(1, "10 minutes to start", "Set up your home") + steps([
        ("List your rooms", "Add each room in Rooms: kitchen, bathroom, bedrooms and more."),
        ("Add 10 tasks", "Start small. Pick a room, how often and who for each one."),
        ("Fill Last done", "Put the last date you did each task. Status updates by itself."),
        ("Add home jobs", "Filters, alarms, gutters: add how many months between each one."),
        ("Check every morning", "Open the home page and do what is due today."),
    ]), ""),
    ("Chapter 02", chap(2, "A simple rhythm", "Daily, weekly, monthly") + bands([
        ("Every day", "15 to 20 minutes", "☀️", ["Make the beds", "Wipe counters", "Dishes", "One load of laundry"]),
        ("Every week", "One room a day", "📅", ["Bathroom", "Floors", "Bed sheets", "Dusting"]),
        ("Every month", "One bigger job", "📆", ["Fridge", "Washer filter", "Under the beds", "Test alarms"]),
        ("Every season", "Deep clean", "🍂", ["Furnace filter", "Oven", "Baseboards", "Pillows"]),
    ]), ""),
    ("Chapter 03", chap(3, "Many hands", "Share the work") + cards([
        ("👥", "Give each task a name", "Use the Who field: Me, Partner, Kids or Everyone."),
        ("🧒", "Kids' tasks", "Short jobs work best: socks, dusting, setting the table."),
        ("🔁", "Rotate", "Swap the jobs nobody likes each month."),
        ("⏱️", "Use minutes", "Fair is about time, not the number of tasks."),
        ("🎵", "Make it fun", "Music on, timer on, everyone at once."),
        ("🙏", "Say thank you", "Notice the work. People keep doing what gets noticed."),
    ]), ""),
    ("Chapter 04", chap(4, "Fast and smart", "Speed-clean any room") + steps([
        ("Grab a basket", "Collect everything that belongs in another room."),
        ("Top to bottom", "Dust high places first, floors last."),
        ("Spray and wait", "Let the cleaner sit while you do something else."),
        ("Clear surfaces", "Clean counters and tables make a room look done."),
        ("Floors last", "Vacuum or sweep, then you're done."),
    ]), ""),
    ("Chapter 05", chap(5, "Protect your home", "Keep up with home jobs") + cards([
        ("🌬️", "Furnace filter", "Many homes change it every 1 to 3 months."),
        ("🚨", "Smoke & CO alarms", "Press the test button every month."),
        ("🌀", "Dryer vent", "Clean the lint trap every load, the vent twice a year."),
        ("🚿", "Water heater", "Check your manual for how often to flush it."),
        ("🍂", "Gutters", "Clean them in spring and fall, or hire a pro."),
        ("📒", "Write it down", "Log the date and cost so you know when it's due again."),
    ]) + '<p style="margin-top:10px;font-size:11px;color:#777">Always follow your manufacturer\'s manual. Call a pro for gas, electric or roof work.</p>', ""),
    ("Printable", chap(6, "Tick as you go", "Weekly cleaning chart") +
        ws(["Task", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
           ["Beds", "Dishes", "Counters", "Laundry", "Bathroom", "Floors", "Trash"]) +
        '<div class="blk" style="margin-top:16px"><h4>This week\'s one big task</h4><div class="lines"><div></div><div></div></div></div>', ""),
]
build("home", "Home & Cleaning Planner · Calm Home Cleaning Guide", "", P, "Calm-Home-Cleaning-Guide.pdf")
