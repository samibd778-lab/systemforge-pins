"""Bonus PDF for the Job Application Tracker: The 30-Day Job Search Playbook (US Letter, 7 pages).
Reuses the helpers of generator/mini_guides.py. No store links inside (same file for every store).
Run: python3 generator/job_guide.py  -> products/job/30-Day-Job-Search-Playbook.pdf
"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "generator/mini_guides.py").read_text()
src = src.split("# ---------------- HABIT ----------------")[0]
g = {"__file__": str(ROOT / "generator/mini_guides.py")}
exec(src, g)
g["EXTRA"] += ".pl.q{gap:10px}.pl.q>div{padding:12px 16px}.pl.q li{font-size:12px;line-height:1.35;padding:3.5px 0 3.5px 18px}.pl.q h4{font-size:15px}"
g["THEMES"]["job"] = "--forest:#1E2B3A;--clay:#C98B4B;--clay2:#F3E3CF;--sage:#3D6A8F;--sage2:#DFE8F0"
cover, chap, steps, cards, bands, plist, build = (g[k] for k in ("cover", "chap", "steps", "cards", "bands", "plist", "build"))

def qlist(cols):
    n = 0; out = '<div class="pl q">'
    for t, qs in cols:
        lis = ""
        for q in qs:
            n += 1; lis += f"<li><b>{n}.</b> {q}</li>"
        out += f"<div><h4>{t}</h4><ul>{lis}</ul></div>"
    return out + "</div>"

def ws(head, rows):
    return ('<table class="ws"><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>" +
            "".join(f'<tr><td class="lab">{r}</td>' + "<td></td>" * (len(head) - 1) + "</tr>" for r in rows) + "</table>")

P = [
    cover("Bonus guide · 30-day plan", "The 30-Day", "Job Search Playbook",
          "A clear, step-by-step month to go from “I need a job” to interviews and offers. Use it with your Job Application Tracker.",
          ["A resume that gets calls", "Your 30-day plan", "30 interview questions", "Follow-ups that get answers", "Handle the offer", "Printable weekly scorecard"],
          "Read one chapter a day this week. Then follow the plan, one small step at a time."),
    ("Chapter 01", chap(1, "Get past the 6-second scan", "A resume that gets calls") + steps([
        ("Match the job post", "Copy 5 to 8 keywords from the job post and use the same words in your resume. Many companies filter resumes by keywords first."),
        ("Show results, not tasks", "Use: Did X, by doing Y, which led to Z. “Grew sign-ups 18% by rebuilding the pricing page” beats “Worked on the website”."),
        ("Keep it simple", "One column, normal headings (Experience, Education, Skills), no tables or photos, saved as PDF."),
        ("One version per job type", "Keep 2 or 3 base versions (for example Marketing and Content). Write the version name in Resume version for every application."),
        ("Read it out loud", "You hear typos you don't see. Then ask one friend to read it for 1 minute and tell you what you do."),
    ]) + '<div class="note"><span>TIP</span><div>Open the Resume Checklist page in your tracker before every application. It takes 10 minutes.</div></div>', ""),
    ("Chapter 02", chap(2, "Four weeks, one small step a day", "Your 30-day plan") + bands([
        ("Week 1", "Days 1–7", "🧭", ["Pick 1 or 2 job titles to aim for", "Update resume and LinkedIn", "Add 20 companies to Companies", "Write 3 stories in Story Bank"]),
        ("Week 2", "Days 8–14", "📨", ["Apply to 2 jobs a day (10 a week)", "Ask 3 people for a referral", "Log every job in Applications", "Message 1 recruiter a day"]),
        ("Week 3", "Days 15–21", "🔔", ["Follow up when Next step says so", "Keep applying: 10 a week", "Prep for every interview", "Send thank-you emails the same day"]),
        ("Week 4", "Days 22–30", "🎯", ["Look at Why I got rejected", "Fix the weak step (resume, call or interview)", "Check in with your Contacts", "Negotiate every offer"]),
    ]) + '<div class="note green"><span>RULE</span><div>Quality beats quantity. 10 tailored applications a week beat 50 copy-paste ones.</div></div>', ""),
    ("Chapter 03", chap(3, "Practice these out loud", "30 interview questions") + qlist([
        ("👋 About you", ["Tell me about yourself.", "Why are you looking for a new job?", "Why do you want to work here?", "What are you great at?", "What is your biggest weakness?", "Where do you see yourself in 3 years?", "Why should we hire you?", "What do you know about our company?"]),
        ("⭐ Your experience (use STAR)", ["Tell me about a project you're proud of.", "Tell me about a time you failed.", "Tell me about a conflict with a coworker.", "Tell me about a hard deadline.", "Tell me about a time you led without being the boss.", "Tell me about a mistake you made.", "Tell me about a time you used data to decide.", "Tell me about a time you changed someone's mind."]),
        ("🧩 How you work", ["How do you plan your week?", "How do you handle feedback?", "How do you learn something new fast?", "How do you work with people you disagree with?", "What kind of manager helps you do your best?", "How do you handle many tasks at once?", "What would you do in your first 90 days?"]),
        ("💰 The hard ones", ["What salary are you looking for?", "Why is there a gap in your resume?", "Why are you leaving after a short time?", "Are you talking to other companies?", "When can you start?", "Do you have any questions for us?", "Is there anything that worries you about this job?"]),
    ]), ""),
    ("Chapter 04", chap(4, "Most people never follow up", "Follow-ups that get answers") + cards([
        ("⏳", "Wait 7 days", "Give them a week after you apply. Your tracker shows “Wait X more days” until then."),
        ("🔔", "Day 7: first follow-up", "Short and friendly. Remind them of one result you bring. Copy it from Follow-up Emails."),
        ("👻", "Day 14: last follow-up", "Say you're still interested and leave the door open. Then move on with no hard feelings."),
        ("✉️", "Same day: thank-you", "After every interview. Name one thing they said. It takes 3 minutes and people remember it."),
        ("🤝", "Ask for referrals", "A referral is often the fastest way to an interview. Ask friends and old coworkers at your target companies."),
        ("📅", "Every 30 days: check in", "Send a short hello to recruiters and contacts. Your Contacts page tells you when."),
    ]), ""),
    ("Chapter 05", chap(5, "Ask for more, politely", "Handle the offer") + steps([
        ("Say thank you, not yes", "Ask for 2 days to look at the details. This is normal and expected."),
        ("Know your numbers", "Look up the salary for the role and city. Write a target and a walk-away number."),
        ("Ask once, with a reason", "Point to your research and one strong result. Then ask for a number near your target."),
        ("Ask for other things too", "If the salary can't move: signing bonus, vacation days, remote days, a review in 6 months."),
        ("Get it in writing", "Accept only after you see the final offer by email."),
    ]) + '<div class="note"><span>TIP</span><div>The Salary Negotiation Script page in your tracker has the exact words to use.</div></div>', ""),
    ("Printable", chap(6, "Fill it every Friday", "Weekly scorecard") +
        '<p style="margin:-14px 0 14px">Week of: ______________ &nbsp;&nbsp; Goal: 10 applications · 3 referral asks · every follow-up sent</p>' +
        ws(["This week", "Goal", "Done", "Notes"], ["📨 Applications sent", "🤝 Referrals asked", "🔔 Follow-ups sent", "📞 Interviews", "✉️ Thank-yous sent", "⭐ New STAR stories", "👋 People I checked in with"]) +
        '<div class="blk" style="margin-top:16px"><h4>What got me the most answers this week?</h4><div class="lines"><div></div><div></div></div></div>' +
        '<div class="blk"><h4>One thing I will change next week</h4><div class="lines"><div></div></div></div>', ""),
]
build("job", "Job Application Tracker · 30-Day Job Search Playbook", "", P, "30-Day-Job-Search-Playbook.pdf")
