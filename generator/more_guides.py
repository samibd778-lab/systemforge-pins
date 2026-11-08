"""Bonus PDFs for Meal Planner, Travel Planner and Life Planner (US Letter, 7 pages each).
Reuses the helpers of generator/mini_guides.py. No store links inside (same file for every store).
Run: python3 generator/more_guides.py -> products/<meal|travel|life>/<file>.pdf
"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "generator/mini_guides.py").read_text().split("# ---------------- HABIT ----------------")[0]
g = {"__file__": str(ROOT / "generator/mini_guides.py")}
exec(src, g)
g["THEMES"].update({
    "meal": "--forest:#22362A;--clay:#D9822B;--clay2:#F6E2CC;--sage:#5E8C5A;--sage2:#E1ECDD",
    "travel": "--forest:#16324A;--clay:#D98B4E;--clay2:#F5E3D2;--sage:#2F7E9A;--sage2:#DCEBF1",
    "life": "--forest:#2E2442;--clay:#D4A24C;--clay2:#F5E8CF;--sage:#7A63A8;--sage2:#E8E2F2",
})
g["EXTRA"] += ".ws.sm td{height:26px;padding:7px 12px}.ws.sm th{padding:9px 12px}"
cover, chap, steps, cards, bands, plist, build = (g[k] for k in ("cover", "chap", "steps", "cards", "bands", "plist", "build"))

def ws(head, rows, cls=""):
    return (f'<table class="ws {cls}"><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>" +
            "".join(f'<tr><td class="lab">{r}</td>' + "<td></td>" * (len(head) - 1) + "</tr>" for r in rows) + "</table>")

def checks(cols):
    return plist(cols)

# ---------------- MEAL ----------------
M = [
    cover("Bonus guide · 4-week plan", "Eat Well,", "Stress Less", "A simple 4-week plan to cook at home more, waste less food and spend less. Use it with your Meal Planner.",
          ["Plan a week in 15 minutes", "Your 4-week plan", "Batch cooking basics", "Mix-and-match meal ideas", "Save money at the store", "Printable week + grocery list"],
          "Start with week 1 this Sunday. Small steps beat a perfect plan."),
    ("Chapter 01", chap(1, "Every Sunday", "Plan a week in 15 minutes") + steps([
        ("Look in the fridge first", "What needs to be used soon? Plan it for Monday or Tuesday so nothing goes to waste."),
        ("Check your calendar", "Busy nights get a quick recipe or leftovers. Calm nights can be a new recipe."),
        ("Plan 5 dinners, not 7", "Leave 2 nights for leftovers or eating out. Real life always changes the plan."),
        ("Cook once, eat twice", "Double one or two dinners and plan the leftovers as lunch the next day."),
        ("Write the grocery list", "Add only what you don't have, sorted by aisle. Your To buy view does this for you."),
    ]) + '<div class="note"><span>TIP</span><div>Keep a list of 10 meals your family loves. When you are tired, pick from that list.</div></div>', ""),
    ("Chapter 02", chap(2, "One small habit a week", "Your 4-week plan") + bands([
        ("Week 1", "Start small", "🌱", ["Plan 3 dinners only", "Add 5 favorite recipes", "Shop with a list", "Tick Cooked each night"]),
        ("Week 2", "Add lunches", "🥪", ["Plan 4 dinners", "Turn 2 dinners into lunches", "Try 1 new recipe", "Rate the new recipe"]),
        ("Week 3", "Prep ahead", "🍱", ["Do a 60-minute Sunday prep", "Make overnight oats for 4 days", "Plan 5 dinners", "Freeze 1 extra meal"]),
        ("Week 4", "Make it yours", "🏆", ["Use your Favorites first", "Write the price of what you buy", "Plan a use-it-up meal", "Look back at what worked"]),
    ]) + '<div class="note green"><span>RULE</span><div>Done is better than perfect. A sandwich night is still a planned night.</div></div>', ""),
    ("Chapter 03", chap(3, "One hour, a whole week easier", "Batch cooking basics") + cards([
        ("🍚", "Cook a big grain", "Rice, quinoa or pasta for 3 meals. It keeps 4 to 5 days in the fridge."),
        ("🥦", "Roast a big tray", "Veggies and a protein on one sheet pan at 425°F (220°C) for 25 to 35 minutes."),
        ("🥚", "Boil 6 eggs", "Breakfasts, snacks and salads for the week. They keep 7 days."),
        ("🥣", "Make 1 sauce", "Tahini lemon, pesto or vinaigrette makes plain food taste new."),
        ("🧊", "Freeze 1 meal", "Soup, chili or sauce for a night when you can't cook."),
        ("🏷️", "Label everything", "Write the name and the date. Eat the oldest first."),
    ]), ""),
    ("Chapter 04", chap(4, "No recipe needed", "Mix-and-match meals") + plist([
        ("🥗 Bowl = 1 + 1 + 1 + 1", ["A grain: rice, quinoa, pasta", "A protein: chicken, eggs, beans, tofu", "Veggies: raw or roasted", "A sauce: tahini, pesto, salsa"]),
        ("🌮 Wrap night", ["Tortillas or flatbread", "Leftover protein", "Crunchy veggies", "Yogurt or salsa"]),
        ("🍳 Clean-the-fridge omelet", ["3 eggs", "Any leftover veggies", "Cheese if you have it", "Toast on the side"]),
        ("🍝 Pantry pasta", ["Pasta + canned tomatoes", "Garlic and olive oil", "Frozen peas or spinach", "Parmesan on top"]),
    ]), ""),
    ("Chapter 05", chap(5, "Same food, smaller bill", "Save money at the store") + steps([
        ("Shop from the list only", "Eat before you go. Your To buy list is sorted by aisle, so you walk less and buy less."),
        ("Compare the price per ounce", "Big packs are not always cheaper. Look at the small price on the shelf label."),
        ("Buy store brands for basics", "Oats, rice, pasta, canned beans and frozen veggies are often the same quality."),
        ("Use frozen fruit and veggies", "Same nutrients, no waste, ready when you need them."),
        ("Track what you spend", "Write the Price in your Grocery List. After a month you know where the money goes."),
    ]), ""),
    ("Printable", chap(6, "Stick it on the fridge", "My week + grocery list") +
        ws(["Day", "Breakfast", "Lunch", "Dinner"], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "sm") +
        '<div style="height:12px"></div>' +
        ws(["Aisle", "To buy", "", ""], ["🥦 Produce", "🥛 Dairy & eggs", "🍗 Meat & fish", "🥫 Pantry", "🍞 Bakery", "🧊 Frozen"], "sm"), ""),
]

# ---------------- TRAVEL ----------------
T = [
    cover("Bonus guide · trip planning", "Plan Trips", "Like a Pro", "From the first idea to the flight home: a simple plan for calm, well-organized trips. Use it with your Travel Planner.",
          ["Your planning timeline", "Build a realistic budget", "Plan the days", "Pack light, pack smart", "Travel day and on the trip", "Printable trip sheet"],
          "Read it once when you start dreaming about a trip. Then follow the timeline."),
    ("Chapter 01", chap(1, "What to do and when", "Your planning timeline") + bands([
        ("3 months", "Before", "🗺️", ["Pick dates and a budget", "Check passport and visa", "Book flights", "Book the stay"]),
        ("1 month", "Before", "🎟️", ["Book popular tickets", "Buy travel insurance", "Plan each day roughly", "Reserve special restaurants"]),
        ("1 week", "Before", "🧳", ["Tell your bank", "Get an eSIM or phone plan", "Download offline maps", "Start the packing list"]),
        ("2 days", "Before", "✅", ["Check in online", "Screenshot bookings", "Pack and charge everything", "Plan the way to the airport"]),
    ]), ""),
    ("Chapter 02", chap(2, "No surprises at the end", "Build a realistic budget") + steps([
        ("Flights", "Check prices for your dates, then add 10% for bags and seats."),
        ("Stay", "Price per night × nights. A kitchen can save a lot on breakfast."),
        ("Food", "A daily amount per person × days × people. Mix cheap and nice meals."),
        ("Activities", "List the 3 to 5 things you really want to do and their prices."),
        ("Buffer", "Add 10% for transport, tips and surprises. Then log every expense in the planner."),
    ]) + '<div class="note"><span>TIP</span><div>Set the Budget on your trip page. Budget left turns red the moment you go over.</div></div>', ""),
    ("Chapter 03", chap(3, "Full days, not tired days", "Plan the days") + cards([
        ("⭐", "1 big thing a day", "Plan one main activity per day. The rest is free time."),
        ("📍", "Group by area", "Put things that are close together on the same day."),
        ("🍽️", "Book 1 special meal", "Reserve one dinner you'll remember. Find the rest on the spot."),
        ("🌅", "Go early", "Famous places are calm in the morning and crowded at noon."),
        ("🌧️", "Have a rain plan", "Note one museum or café nearby for bad weather."),
        ("😴", "Leave a lazy day", "On longer trips, keep one day with no plans."),
    ]), ""),
    ("Chapter 04", chap(4, "Carry-on only is possible", "Pack light, pack smart") + plist([
        ("👕 The 5-4-3-2-1 rule (1 week)", ["5 tops, socks and underwear", "4 bottoms", "3 pairs of shoes max (wear the biggest)", "2 swimsuits or extra layers", "1 hat or cap"]),
        ("🎒 Always in your carry-on", ["Passport and cards", "Phone, charger, power bank", "Medicine", "1 change of clothes"]),
        ("🧴 Save space", ["Travel-size toiletries", "Roll clothes, don't fold", "Wear your jacket on the plane", "Pack a tote bag for souvenirs"]),
        ("🚫 Leave at home", ["“Just in case” outfits", "Full-size bottles", "Too many books", "Valuables you don't need"]),
    ]), ""),
    ("Chapter 05", chap(5, "Calm from door to door", "Travel day and on the trip") + steps([
        ("Leave early", "2 hours before local flights, 3 hours before international ones."),
        ("Keep bookings offline", "Screenshots of every Confirmation # in case there is no internet."),
        ("Log expenses daily", "Add what you spend each evening. It takes 1 minute and keeps the budget honest."),
        ("Take photos of the moments", "Then write 3 lines in the trip page: best food, best view, funniest moment."),
        ("After the trip", "Change the status to Done and write what you'd do differently next time."),
    ]), ""),
    ("Printable", chap(6, "Keep it in your bag", "My trip sheet") +
        '<p style="margin:-14px 0 12px">Trip: ______________________ &nbsp;&nbsp; Dates: ______________ &nbsp;&nbsp; Budget: $ __________</p>' +
        ws(["Day", "Plan", "Booked?", "Cost"], ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"], "sm") +
        '<div style="height:12px"></div>' +
        ws(["Important", "Details", "", ""], ["✈️ Flight #", "🏨 Hotel address", "🆘 Emergency number", "🛂 Passport #"], "sm"), ""),
]

# ---------------- LIFE ----------------
L = [
    cover("Bonus guide · 90-day workbook", "The 90-Day", "Goal Workbook", "Turn big dreams into small weekly steps you can finish. Use it with your Life Planner.",
          ["Check in with your life", "Pick the right goals", "Break goals into steps", "Your weekly rhythm", "When you fall off track", "Printable 90-day plan"],
          "Block one hour this week. Fill it with a pen, then copy your goals into Notion."),
    ("Chapter 01", chap(1, "Before you set goals", "Check in with your life") +
        ws(["Area", "Score (1-10)", "Why this score?", "+1 idea"], ["💪 Health", "💼 Career", "💰 Money", "❤️ Relationships", "🌱 Growth", "🎉 Fun", "🏠 Home", "🧘 Peace of mind"], "sm") +
        '<div class="note" style="margin-top:14px"><span>TIP</span><div>Circle the 2 lowest scores. Your first goals usually live there.</div></div>', ""),
    ("Chapter 02", chap(2, "Fewer, better goals", "Pick the right goals") + steps([
        ("Only 1 to 3 goals", "Each new goal takes energy from the others. Three is the most most people can keep."),
        ("Make it clear", "“Get fit” is vague. “Run a 10K race on December 13” is clear: you know when it's done."),
        ("Write why it matters", "On hard days, the why is what keeps you going."),
        ("Pick a reward", "Something small and fun you'll get when it's done."),
        ("Choose a date", "90 days is long enough to change something and short enough to stay focused."),
    ]), ""),
    ("Chapter 03", chap(3, "Big goal, small steps", "Break goals into steps") + cards([
        ("🎯", "Start from the end", "What does done look like? Write it as the last milestone."),
        ("🪜", "3 to 5 milestones", "Each one is a clear point on the way, with its own date."),
        ("📅", "1 step per 2-3 weeks", "Spread milestones out so each one feels possible."),
        ("⚡", "First step this week", "Make step one tiny: sign up, buy, call, open."),
        ("👀", "Make it visible", "Your progress bar fills as you tick milestones. Look at it weekly."),
        ("🔁", "Adjust, don't quit", "Move a date if you need to. Keep the goal."),
    ]), ""),
    ("Chapter 04", chap(4, "10 minutes every Sunday", "Your weekly rhythm") + bands([
        ("Look back", "3 min", "👀", ["Tick finished milestones", "Write one win", "Write what got in the way", "Check your progress bars"]),
        ("Plan", "5 min", "🗓️", ["Pick 3 important things", "Put them in your calendar", "Move late steps to new dates", "Say no to one thing"]),
        ("Dream", "2 min", "✨", ["Look at your Vision Board", "Add a new dream if you have one", "Remember your why", "Close the laptop"]),
    ]), ""),
    ("Chapter 05", chap(5, "It happens to everyone", "When you fall off track") + plist([
        ("“I'm too busy”", ["Make the next step smaller", "Do 10 minutes, not an hour", "Put it in your calendar like a meeting"]),
        ("“I lost motivation”", ["Read your why again", "Look at how far you came", "Tell a friend your goal"]),
        ("“It's not working”", ["Change the plan, not the goal", "Ask someone who did it", "Try a different first step"]),
        ("“I missed weeks”", ["Start again this Sunday", "Don't start from zero: continue", "Pause one goal if needed"]),
    ]) + '<div class="quote">Progress, not perfection. A small step today beats a perfect plan tomorrow.</div>', ""),
    ("Printable", chap(6, "Fill it with a pen", "My 90-day plan") +
        "".join(f'<div class="blk" style="padding:12px 18px;margin-bottom:10px"><h4>Goal {n}: ________________________________ &nbsp; by ____________</h4>'
                '<p style="font-size:13px;margin-top:6px">Why: __________________________________________ &nbsp; Reward: ________________</p>'
                '<p style="font-size:13px;margin-top:6px">Steps: ① ______________ ② ______________ ③ ______________ ④ ______________</p></div>' for n in (1, 2, 3)) +
        ws(["Week", "1", "2", "3", "4", "5", "6"], ["Steps done ✓", "Weekly check-in ✓"], "sm"), ""),
]

build("meal", "Meal Planner · Eat Well, Stress Less", "", M, "Eat-Well-Stress-Less-Guide.pdf")
build("travel", "Travel Planner · Plan Trips Like a Pro", "", T, "Plan-Trips-Like-a-Pro-Guide.pdf")
build("life", "Life Planner · The 90-Day Goal Workbook", "", L, "90-Day-Goal-Workbook.pdf")
