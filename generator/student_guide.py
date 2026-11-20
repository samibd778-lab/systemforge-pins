"""Bonus PDF for the Student Planner: The Study Smarter Playbook (US Letter, 7 pages).
Reuses the helpers of generator/mini_guides.py. No store links inside (same file for every store).
Run: python3 generator/student_guide.py  -> products/student/Study-Smarter-Playbook.pdf
"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "generator/mini_guides.py").read_text()
src = src.split("# ---------------- HABIT ----------------")[0]
g = {"__file__": str(ROOT / "generator/mini_guides.py")}
exec(src, g)
g["THEMES"]["student"] = "--forest:#1F2E45;--clay:#C98B4B;--clay2:#F3E3CF;--sage:#3E6A9A;--sage2:#DFE8F3"
cover, chap, steps, cards, bands, plist, build = (g[k] for k in ("cover", "chap", "steps", "cards", "bands", "plist", "build"))

def ws(head, rows):
    return ('<table class="ws"><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>" +
            "".join(f'<tr><td class="lab">{r}</td>' + "<td></td>" * (len(head) - 1) + "</tr>" for r in rows) + "</table>")

P = [
    cover("Bonus guide · study smarter", "The Study", "Smarter Playbook",
          "Simple methods to learn more in less time, keep your grades on track and walk into exams calm. Use it with your Student Planner.",
          ["5 methods that beat re-reading", "Spaced reviews made easy", "The 7-day exam plan", "Grade math in 2 minutes", "Focus without willpower", "Printable weekly planner"],
          "Read one chapter a day this week. Then try one new method in your next study session."),
    ("Chapter 01", chap(1, "Stop re-reading, start recalling", "5 methods that work") + cards([
        ("🔁", "Active recall", "Close the book and write what you remember. Then check. Pulling facts out of your head is what makes them stick."),
        ("🗓️", "Spaced reviews", "Review a topic a few times over days and weeks, not 5 times in one night."),
        ("🍅", "Pomodoro", "25 minutes of focus, 5 minutes of break. After 4 rounds, a longer break."),
        ("✏️", "Practice problems", "Do problems without the solution, with a timer. Redo the wrong ones 2 days later."),
        ("🧑‍🏫", "Teach it", "Explain the topic in simple words. Where you get stuck is what to study next."),
        ("🔀", "Mix it up", "Switch between topics or problem types in one session, like on a real exam."),
    ]) + '<div class="note"><span>TIP</span><div>Pick the method for each session and log it in Study Sessions. After 2 weeks, look at which method gave you Deep focus most often.</div></div>', ""),
    ("Chapter 02", chap(2, "Review it before you forget it", "Spaced reviews made easy") + steps([
        ("After class: write the key ideas", "Add a row to Class Notes the same day. 3 to 5 key ideas in your own words, not a copy of the slides."),
        ("Day 1: first review", "Next review shows 🔁 Review today. Cover the note and recall the ideas. Then add 1 to Reviews done."),
        ("Day 3 and day 7", "Each review is faster than the last. Turn the ideas into questions and answer them out loud."),
        ("Day 14 and day 30", "Quick checks. If you forgot something, review it again the next day."),
        ("After 5 reviews: ✅ Learned", "The note leaves the Notes to review list. It is ready for the exam."),
    ]) + '<div class="note green"><span>RULE</span><div>10 minutes of reviews a day beats a whole night of cramming before the exam.</div></div>', ""),
    ("Chapter 03", chap(3, "Start a week before, not the night before", "The 7-day exam plan") + bands([
        ("Days 7–6", "Map it", "🧭", ["Ask what the exam covers", "List every topic on one page", "Mark each topic 🟢 🟡 🔴", "Plan sessions for every 🔴 topic"]),
        ("Days 5–3", "Learn it", "📚", ["🔴 topics first, then 🟡", "One summary page per topic", "Old exams with a timer", "Bring questions to office hours"]),
        ("Day 2", "Test it", "🔁", ["Active recall on every topic", "Redo the wrong problems", "Teach the hardest topic", "Fix the last gaps"]),
        ("Day 1", "Rest it", "🌙", ["Light review only", "Pack your bag the night before", "Check the room and time", "Sleep 7 to 9 hours"]),
    ]) + '<div class="note"><span>TIP</span><div>The Exam Prep Checklist page in your planner has this plan as tick boxes.</div></div>', ""),
    ("Chapter 04", chap(4, "Know where you stand", "Grade math in 2 minutes") + steps([
        ("Find the weights", "Your syllabus says how much each part counts, for example: labs 20%, midterm 25%, project 20%, final 35%."),
        ("Your grade so far", "Multiply each grade by its weight, add them, and divide by the weights graded so far. The planner does this in Current grade."),
        ("What you need on the rest", "Goal minus the points you have, divided by what's left. Example: goal 90, you have 40 points from 45%, so you need 50 out of 55, about 91%."),
        ("Your GPA", "Each letter has points (A = 4.0, B = 3.0…). Multiply by the course credits, add them, divide by total credits. See it on the Semesters page."),
        ("Act early", "If Need on the rest shows ⚠️ Goal out of reach, talk to your teacher now, not in finals week."),
    ]) + '<div class="note green"><span>NOTE</span><div>Schools use different grade scales. Check your syllabus and change the letters in the Letter formula if yours is different.</div></div>', ""),
    ("Chapter 05", chap(5, "Make focus the easy choice", "Focus without willpower") + cards([
        ("📵", "Phone out of sight", "Put it in another room or a bag. Out of sight is easier than “I won't look”."),
        ("🎯", "One task per round", "Write the one task for this pomodoro on paper before you start."),
        ("⏱️", "Start with 10 minutes", "Can't start? Set a 10-minute timer. Starting is the hardest part."),
        ("📍", "Same place, same time", "A fixed study spot and time turns studying into a habit."),
        ("🥤", "Water and a snack", "A drink on the desk saves you from getting up and losing focus."),
        ("😴", "Sleep counts as studying", "Your brain saves what you learned while you sleep. All-nighters cost you more than they give."),
    ]), ""),
    ("Printable", chap(6, "Fill it every Sunday", "Weekly study planner") +
        '<p style="margin:-14px 0 14px">Week of: ______________ &nbsp;&nbsp; Big deadline this week: ______________________</p>' +
        ws(["Day", "Course", "Task", "Method", "Done"], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]) +
        '<div class="blk" style="margin-top:16px"><h4>What worked best this week?</h4><div class="lines"><div></div><div></div></div></div>' +
        '<div class="blk"><h4>One thing I will change next week</h4><div class="lines"><div></div></div></div>', ""),
]
build("student", "Student Planner · Study Smarter Playbook", "", P, "Study-Smarter-Playbook.pdf")
