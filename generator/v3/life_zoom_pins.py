"""'Zoom' pins for the Life templates, in the style of the best Etsy pin (v3-ccs-zoom: 330 impressions).
Warm desk scene + real Notion screens, big serif headline, 2 big readable cards, clay label, CTA.

Writes:
  canva/v3/bg/<id>.jpg            backgrounds (scene + real screens)
  canva/v3/crops/*.png            card crops
  canva/v3/pins-life-zoom.html    Canva-importable design, one page per pin (editable text)
  canva/v3/preview/<id>.jpg       local preview renders (same layout)
Usage: python3 generator/v3/life_zoom_pins.py
"""
import json, os, re
import build_pins as B

HD = os.path.join(B.ROOT, 'shots', 'hd')
_orig_src = B.src


CARD_W = 0.6  # keep the left 60% of a card screenshot so its text is big enough to read on a phone
CARDS = set()
CARD_TOP = {}  # share of the screenshot height to skip (section title + description)


def src(name):
    for ext in ('.jpg', '.png'):
        p = os.path.join(HD, name + ext)
        if os.path.exists(p):
            if name in CARDS:
                from PIL import Image
                im = Image.open(p).convert('RGB')
                c = im.crop((0, int(im.height * CARD_TOP.get(name, 0.26)), int(im.width * CARD_W), im.height))
                out = os.path.join(B.OUT, 'crops', name + '-left.png')
                c.save(out)
                return out
            return p
    return _orig_src(name)


B.src = src

SPEC = [
    dict(id='v5-habit-zoom', p='habit', name='Habit Tracker', screens=['habit-top', 'habit-calendar'], kicker='NOTION HABIT TRACKER',
         title='Habits that<br>finally stick.', label='Your score fills in by itself',
         cards=[('✅ Tick today’s habits', 'habit-week'), ('📈 Your month at a glance', 'habit-monthly')]),
    dict(id='v5-budget-zoom', p='budget', name='Budget Planner', screens=['budget-top', 'budget-widget'], kicker='NOTION BUDGET PLANNER',
         title='Know where your<br>money goes.', label='What’s left in every category',
         cards=[('💸 Budget by category', 'budget-categories'), ('🧾 Bills this month', 'budget-bills')]),
    dict(id='v5-journal-zoom', p='journal', name='Daily Journal', screens=['journal-top', 'journal-calendar'], kicker='NOTION DAILY JOURNAL',
         title='Two minutes<br>a day.', label='Mood, one win, one thank you',
         cards=[('📝 Today’s entry', 'journal-entries'), ('🙏 Gratitude jar', 'journal-gratitude')]),
    dict(id='v5-life-zoom', p='life', name='Life Planner', screens=['life-top', 'life-wheel'], kicker='NOTION LIFE PLANNER',
         title='Make 2027<br>your year.', label='Goals fill up as you go',
         cards=[('🎯 Goals with progress', 'life-goals'), ('🪜 Your next steps', 'life-steps')]),
    dict(id='v5-meal-zoom', p='meal', name='Meal Planner', screens=['meal-top', 'meal-recipe'], kicker='NOTION MEAL PLANNER',
         title='Dinner,<br>already planned.', label='Your whole week of meals',
         cards=[('🍽️ This week', 'meal-week'), ('🛒 Grocery list by aisle', 'meal-buy')]),
    dict(id='v5-travel-zoom', p='travel', name='Travel Planner', screens=['travel-top', 'travel-pack'], kicker='NOTION TRAVEL PLANNER',
         title='Your whole trip,<br>one page.', label='A countdown to every trip',
         cards=[('✈️ Your trips', 'travel-trips'), ('📌 Still to book', 'travel-book')]),
    dict(id='v5-job-zoom', p='job', name='Job Application Tracker', screens=['job-top', 'job-emails'], kicker='NOTION JOB APPLICATION TRACKER',
         title='Never miss<br>a follow-up.', label='No answer in 7 days? Follow up',
         cards=[('🔔 Follow up today', 'job-followup'), ('🗂️ Job pipeline', 'job-pipeline')]),
    dict(id='v5-sb-zoom', p='sb', name='Second Brain OS', screens=['sb-home', 'sb-journal'], kicker='NOTION SECOND BRAIN',
         title='Your whole life,<br>one calm page.', label='Goals, habits and journal, linked',
         cards=[('🎯 Goals that fill up', 'sb-goals'), ('✅ Habits', 'sb-habits')]),
]

if __name__ == '__main__':
    for p in SPEC:
        p['style'] = 'zoom'
        B.NAMES[p['p']] = p['name']
        CARDS.update(c for _, c in p['cards'])
    out_html = os.path.join(B.OUT, 'pins-life-zoom.html')
    B.build(SPEC, out_html)
    # local previews: same HTML, GitHub URLs swapped for local files
    os.makedirs(os.path.join(B.OUT, 'preview'), exist_ok=True)
    html = open(out_html).read().replace(B.RAW, 'file://' + B.OUT + '/')
    head, body = html.split('<body>', 1)
    pages = re.findall(r'(<div data-document-role="page".*?)(?=<div data-document-role="page"|</body>)', body, re.S)
    for p, pg in zip(SPEC, pages):
        B.render(head + '<body>' + pg + '</body></html>', os.path.join(B.OUT, 'preview', p['id'] + '.jpg'))
        print('preview', p['id'])
    json.dump(SPEC, open(os.path.join(B.HERE, 'pins-life-zoom-spec.json'), 'w'), indent=1, ensure_ascii=False)
