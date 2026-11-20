"""Bonus PDF for the Fitness & Workout Tracker: Strength Starter Guide (US Letter, 7 pages).
Reuses generator/mini_guides.py helpers. No store links inside. General info only, not medical advice.
Run: python3 generator/fit_guide.py -> products/fit/Strength-Starter-Guide.pdf
"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "generator/mini_guides.py").read_text().split("# ---------------- HABIT ----------------")[0]
g = {"__file__": str(ROOT / "generator/mini_guides.py")}
exec(src, g)
g["THEMES"]["fit"] = "--forest:#2B2523;--clay:#C2533A;--clay2:#F6DED6;--sage:#5E7A6B;--sage2:#E1EAE4"
cover, chap, steps, cards, bands, build = (g[k] for k in ("cover", "chap", "steps", "cards", "bands", "build"))

def ws(head, rows):
    return ('<table class="ws"><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>" +
            "".join(f'<tr><td class="lab">{r}</td>' + "<td></td>" * (len(head) - 1) + "</tr>" for r in rows) + "</table>")

P = [
    cover("Bonus guide · train smarter", "The Strength", "Starter Guide",
          "Simple rules to get stronger week after week, stay safe and keep going. Use it with your Fitness & Workout Tracker.",
          ["The 4 rules of progress", "How to add weight safely", "Your first 4 weeks", "Recovery that works", "When to rest", "Printable 4-week log"],
          "This guide is general information, not medical advice. If you are new to exercise or have a health condition, check with your doctor first."),
    ("Chapter 01", chap(1, "Get stronger without guessing", "The 4 rules of progress") + cards([
        ("📈", "Do a bit more", "Add a little weight, one rep or one set over time. Small steps, every week."),
        ("🔁", "Repeat the basics", "Squat, hinge, push, pull, carry. The same lifts, done often, beat random workouts."),
        ("📝", "Write it down", "If you log the weights, you know what to try next time. No guessing."),
        ("😴", "Recover", "You get stronger while you rest, not while you lift. Sleep and rest days count."),
        ("🎯", "Good form first", "A clean rep with less weight beats a messy rep with more."),
        ("📅", "Show up", "3 workouts a week for 3 months beat 6 a week for 3 weeks."),
    ]), ""),
    ("Chapter 02", chap(2, "Add weight the safe way", "Simple progression") + steps([
        ("Start light", "Pick a weight you can lift for all sets and reps with good form and 2 reps left in the tank."),
        ("Hit every rep", "When you complete all sets and reps cleanly, note it in Lifts."),
        ("Add a little", "Next time, add 5 lb to lower-body lifts and 2.5 to 5 lb to upper-body lifts."),
        ("Miss? Repeat", "If you miss reps, keep the same weight next time. Miss 3 times in a row? Drop 10% and build back up."),
        ("Watch your bests", "Your Personal best column shows your top weight and an estimated 1-rep max, so you see progress over weeks."),
    ]) + '<div class="note"><span>TIP</span><div>The estimated 1-rep max is a guess from your sets. You never need to test a true max to make progress.</div></div>', ""),
    ("Chapter 03", chap(3, "A clear plan for month one", "Your first 4 weeks") + bands([
        ("Week 1", "Learn", "🌱", ["3 full-body workouts", "Light weights, learn the moves", "Log every lift", "Walk on rest days"]),
        ("Week 2", "Build", "🧱", ["Same plan", "Add 5 lb where it felt easy", "Add your first goal", "First body check-in"]),
        ("Week 3", "Push", "💪", ["Same plan, a bit heavier", "Try 1 extra rep on the last set", "Keep sleeping 7+ h", "Check form on video"]),
        ("Week 4", "Review", "🔎", ["Compare week 1 and week 4 lifts", "Update your goals", "Pick the next plan", "Celebrate"]),
    ]), ""),
    ("Chapter 04", chap(4, "Feel good for the next workout", "Recovery that works") + cards([
        ("😴", "Sleep 7–9 h", "The simplest way to recover better. Same bedtime most nights."),
        ("🥤", "Drink water", "A glass when you wake up, one before training, sips during."),
        ("🍳", "Protein at meals", "Eggs, yogurt, fish, chicken, beans or tofu. A bit at every meal."),
        ("🚶", "Easy movement", "Walks and stretching on rest days help sore muscles."),
        ("🧘", "Warm up, cool down", "10 minutes before, 5 after. Use the Warm-up & Recovery page."),
        ("📏", "Weekly check-in", "Log weight, waist, sleep and steps once a week, same day, same time."),
    ]), ""),
    ("Chapter 05", chap(5, "Listen to your body", "Push, ease off or rest") + steps([
        ("Great and rested", "Train as planned. A good day to try for a new best."),
        ("A bit sore or tired", "Train, but keep last week's weights. Showing up still counts."),
        ("Very sore or slept badly", "Swap for a light day: a walk, yoga or mobility."),
        ("Joint pain, dizzy or sick", "Stop and rest. If it doesn't go away, see a doctor."),
    ]) + '<div class="note green"><span>RULE</span><div>Soreness that fades in 1 to 3 days is normal. Sharp pain during a lift is a signal to stop.</div></div>', ""),
    ("Printable", chap(6, "Track your first month on paper", "4-week lift log") +
        '<p style="margin:-14px 0 14px">Write the weight × reps for your top set each week.</p>' +
        ws(["Lift", "Week 1", "Week 2", "Week 3", "Week 4"], ["Squat", "Bench press", "Deadlift", "Overhead press", "Row", "Pull-up", "Plank (s)"]) +
        '<div class="blk" style="margin-top:16px"><h4>My goal for next month</h4><div class="lines"><div></div><div></div></div></div>', ""),
]
build("fit", "Fitness & Workout Tracker · Strength Starter Guide", "", P, "Strength-Starter-Guide.pdf")
