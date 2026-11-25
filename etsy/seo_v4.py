# SEO v4 (2026-11-25). Volumes = Google US monthly (OpenSEO), not Etsy.
S = {
'pregnancy': dict(
 title="Pregnancy Planner Notion Template | Pregnancy Journal, Baby Tracker, Appointments, Baby Shopping List | Digital Planner, Expecting Mom Gift",
 tags=["pregnancy planner","pregnancy journal","pregnancy tracker","notion template","digital planner","baby tracker","newborn tracker","expecting mom gift","baby shopping list","pregnancy gift","notion planner","baby log","hospital bag list"],
 gum="Pregnancy & Baby Planner — Notion Template",
 summary="Your week, appointments, baby shopping and budget, then a baby log after the birth. One calm Notion page."),
'cycle': dict(
 title="Period Tracker Notion Template | Cycle Tracker, Menstrual Cycle Log, Mood Tracker, Symptom Log | Digital Wellness Planner",
 tags=["period tracker","cycle tracker","menstrual tracker","notion template","digital planner","mood tracker","symptom tracker","wellness tracker","wellness planner","notion planner","period journal","cycle syncing","self care planner"],
 gum="Cycle & Wellness Tracker — Notion Template",
 summary="Log your day in one minute. See your cycle day, next period estimate, symptoms and patterns."),
'skin': dict(
 title="Skincare Routine Notion Template | Skincare Planner, Skin Care Tracker, Beauty Product Inventory | Digital Planner, Skin Journal",
 tags=["skincare routine","skincare planner","skincare tracker","notion template","digital planner","beauty planner","skincare journal","skin care routine","product inventory","notion planner","self care planner","beauty organizer","skin log"],
 gum="Skincare & Beauty Routine — Notion Template",
 summary="Your morning and evening routine, your products with use-by dates, and how your skin feels."),
'home': dict(
 title="Cleaning Schedule Notion Template | Home Planner, Chore Chart, Cleaning Checklist, Household Organizer | Digital Planner",
 tags=["cleaning schedule","home planner","chore chart","notion template","digital planner","cleaning checklist","cleaning planner","household planner","home management","notion planner","family chore chart","house cleaning","home organizer"],
 gum="Home & Cleaning Planner — Notion Template",
 summary="What to clean today, who does it, home jobs and warranties, and what to buy, on one page."),
'family': dict(
 title="Family Planner Notion Template | Mom Planner, Family Calendar, Chore Chart for Kids, Meal Plan, Reward Chart | Digital Planner",
 tags=["family planner","mom planner","family calendar","notion template","digital planner","chore chart","family chore chart","family organizer","meal planner","notion planner","reward chart","kids chore chart","school planner"],
 gum="Mom & Family Planner — Notion Template",
 summary="Who is where, what’s for dinner and who does which chore. Events, chores, rewards, school and meals."),
'wardrobe': dict(
 title="Capsule Wardrobe Notion Template | Wardrobe Planner, Outfit Planner, Closet Organizer, Cost Per Wear | Digital Planner",
 tags=["capsule wardrobe","wardrobe planner","outfit planner","notion template","digital planner","closet organizer","cost per wear","closet inventory","packing list","notion planner","style planner","fashion planner","minimalist closet"],
 gum="Capsule Wardrobe Planner — Notion Template",
 summary="Your clothes, your outfits and what you really wear, with cost per wear and trip packing."),
'student': dict(
 title="Student Planner Notion Template | Academic Planner, Assignment Tracker, GPA Tracker, Class Schedule, Study Planner | Digital Planner",
 tags=["student planner","academic planner","assignment tracker","notion template","digital planner","study planner","gpa tracker","class schedule","college planner","notion planner","exam planner","homework planner","student budget"],
 gum="Student Planner — Notion Template",
 summary="What’s due this week, your grade in every course, exams coming up and the notes to review."),
'fitness': dict(
 title="Workout Planner Notion Template | Workout Tracker, Gym Log, Fitness Planner, Personal Records, Cardio Log | Digital Planner",
 tags=["workout planner","workout tracker","workout log","notion template","digital planner","fitness planner","gym tracker","gym log","personal records","notion planner","cardio log","strength training","fitness journal"],
 gum="Fitness & Workout Tracker — Notion Template",
 summary="Your workouts this week, personal bests, goals, body log and cardio log on one page."),
'reading': dict(
 title="Reading Journal Notion Template | Reading Log, Book Tracker, Reading Challenge, Book Journal, Book Club | Digital Planner",
 tags=["reading journal","reading log","book tracker","notion template","digital planner","book journal","reading challenge","reading tracker","book club","notion planner","book lover gift","bookshelf tracker","tbr list"],
 gum="Reading Journal — Notion Template",
 summary="The books you’re reading now, your yearly challenge, your bookshelf, quotes and book club."),
'selfcare': dict(
 title="Self Care Planner Notion Template | Wellness Journal, Mood Tracker, Gratitude Journal, Daily Check In | Digital Planner",
 tags=["self care planner","self care journal","wellness journal","notion template","digital planner","mood tracker","gratitude journal","daily check in","wellness planner","notion planner","self care checklist","habit tracker","calm planner"],
 gum="Self-Care & Wellness Planner — Notion Template",
 summary="Check in each day, pick a little care from your menu and look back every Sunday."),
'wedding': dict(
 title="Wedding Planner Notion Template | Wedding Budget, Guest List, Seating Chart, Wedding Checklist, Vendors | Digital Planner",
 tags=["wedding planner","wedding planning","wedding budget","notion template","digital planner","wedding checklist","seating chart","wedding guest list","bride to be gift","notion planner","engagement gift","wedding organizer","wedding binder"],
 gum="Wedding Planner — Notion Template",
 summary="Your countdown, budget, guests, seating, vendors, gifts and honeymoon, all on one page."),
}
if __name__=='__main__':
    bad=0
    for p,d in S.items():
        t=d['title']; tg=d['tags']
        e=[]
        if len(t)>140: e.append(f'title {len(t)}')
        if len(tg)!=13: e.append(f'{len(tg)} tags')
        e+= [f'tag>20:{x}' for x in tg if len(x)>20]
        if len(set(tg))!=13: e.append('dup tag')
        print(p,len(t),'OK' if not e else e); bad+=len(e)
    print('errors',bad)
