"""Bonus PDF for the Cycle & Wellness Tracker: Know Your Cycle Guide (US Letter, 7 pages)."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "generator/mini_guides.py").read_text().split("# ---------------- HABIT ----------------")[0]
g = {"__file__": str(ROOT / "generator/mini_guides.py")}
exec(src, g)
g["THEMES"]["cycle"] = "--forest:#3A2430;--clay:#B25A73;--clay2:#F6E1E7;--sage:#7A6A9A;--sage2:#ECE8F3"
cover, chap, steps, cards, bands, build = (g[k] for k in ("cover", "chap", "steps", "cards", "bands", "build"))
def ws(head, rows):
    return ('<table class="ws"><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>" +
            "".join(f'<tr><td class="lab">{r}</td>' + "<td></td>" * (len(head) - 1) + "</tr>" for r in rows) + "</table>")
P = [
    cover("Bonus guide · listen to your body", "Know Your", "Cycle Guide",
          "A simple way to track your cycle, notice your patterns and plan kinder days. Use it with your Cycle & Wellness Tracker.",
          ["Start tracking", "The four phases", "Spot your patterns", "Plan with your cycle", "Comfort on hard days", "Printable 3-month tracker"],
          "This guide is for everyday wellness. It is not medical advice and not a form of birth control."),
    ("Chapter 01", chap(1, "One minute a day", "Start tracking") + steps([
        ("Set your usual numbers", "Your usual cycle and period length, in My Cycle."),
        ("Log the first day", "Add a row in Cycles on the day your period starts."),
        ("Check in daily", "Flow, mood, energy and how you feel. One minute."),
        ("Close each cycle", "Fill Next period start when the next one comes."),
        ("Let the numbers grow", "After a few cycles, your averages use your real data."),
    ]), ""),
    ("Chapter 02", chap(2, "A simple map", "The four phases") + bands([
        ("Period", "Rest and recharge", "🩸", ["Warm drinks", "Gentle movement", "Early nights", "Lighter plans"]),
        ("Follicular", "Fresh energy", "🌱", ["Start new things", "Plan the month", "Try a new workout", "Social plans"]),
        ("Ovulation window", "Feeling bright", "🌕", ["Big tasks", "Meetings and talks", "Time with friends", "Note how you feel"]),
        ("Luteal", "Slow down", "🌙", ["Lighter days", "Comfort food plan", "Extra sleep", "Be kind to yourself"]),
    ]) + '<p style="margin-top:10px;font-size:11px;color:#777">Every body is different. Phases in your tracker are estimates.</p>', ""),
    ("Chapter 03", chap(3, "Your log tells a story", "Spot your patterns") + cards([
        ("📈", "Cycle length", "See if your cycles stay close to your average."),
        ("🩸", "Period length", "Notice changes from one month to the next."),
        ("😣", "Symptoms", "Which ones come up, and on which cycle days?"),
        ("⚡", "Energy", "Find your high-energy days and use them well."),
        ("😴", "Sleep", "See how sleep and mood move together."),
        ("🩺", "Share with a doctor", "Bring your notes when something feels off."),
    ]), ""),
    ("Chapter 04", chap(4, "Work with your body", "Plan with your cycle") + steps([
        ("Look at the next date", "Your home page shows your next estimated period."),
        ("Protect a few days", "Keep the day before and the first day lighter if you can."),
        ("Use high-energy days", "Put big tasks and fun plans there."),
        ("Prepare early", "Comfort kit and snacks ready before you need them."),
        ("Review monthly", "Use the Monthly cycle review page in your tracker."),
    ]), ""),
    ("Chapter 05", chap(5, "Small things help", "Comfort on hard days") + cards([
        ("🔥", "Warmth", "A heating pad or a warm bath can feel soothing."),
        ("🍵", "Warm drinks", "Herbal tea or warm water with lemon."),
        ("🚶", "Gentle movement", "A short walk or stretching, if it feels good."),
        ("🛌", "Rest", "An early night and a slower morning."),
        ("📝", "Write it down", "Note what helped so you remember next time."),
        ("🩺", "Ask for help", "Talk to your doctor if pain or symptoms worry you."),
    ]), ""),
    ("Printable", chap(6, "Shade the days", "3-month cycle tracker") +
        ws(["Month", "1-7", "8-14", "15-21", "22-28", "29-31"], ["Month 1", "Month 2", "Month 3"]) +
        '<div class="blk" style="margin-top:16px"><h4>Patterns I noticed</h4><div class="lines"><div></div><div></div><div></div></div></div>', ""),
]
build("cycle", "Cycle & Wellness Tracker · Know Your Cycle Guide", "", P, "Know-Your-Cycle-Guide.pdf")
