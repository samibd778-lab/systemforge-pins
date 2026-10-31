"""Second Brain OS listing images in the v3 lifestyle style (same look as the other SystemForge listings).
Shots: shots/hd/sb-*.png (real 2x captures, 2170 px wide). Coordinates below are on the 2000 scale.
Usage: python3 generator/v3/sb_listing_v3.py [labels...]   (no labels = all pages)"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_listing as L
B = L.B
B.CROPS.update({
    'sb-lap': ('sb-home', (95, 0, 1945, 1100)),
    'c-sb-widget': ('sb-home', (166, 968, 1382, 1456)),
    'c-sb-goals': ('sb-goals', (180, 330, 1330, 850)),
    'c-sb-journal': ('sb-journal', (180, 330, 820, 1000)),
})
B.COMPOSITE.update({
    'c-sb-projects': ('sb-projects', [(396, 940)], [(192, 700), (1253, 1751)]),
    'c-sb-habits': ('sb-habits', [(387, 922)], [(185, 1065)]),
})
L.P['sb'] = dict(name='Second Brain OS', kicker='NOTION LIFE PLANNER · PARA METHOD', color='#E3E8DC', accent='#7A8B6F',
    scene='s-sb-r.png', screens=['sb-lap'],
    sub='Goals, projects, notes, habits<br>and journal in one calm place.',
    features=['Goals &amp; projects with progress', 'Habit tracker + daily journal', 'Notes inbox (PARA method)', 'Bonus: Notion for beginners'],
    cards=[('Start every day clear', 'A live Today widget: clock, how much of the week, month and year is left, and a thought for the day.', 'c-sb-widget'),
           ('Goals with real progress', 'Link projects to a goal. Its bar fills up as the projects are done.', 'c-sb-goals'),
           ('Every project on one board', 'Progress bar from ticked tasks, plus days left or late.', 'c-sb-projects'),
           ('Small habits, every day', 'One row per day. Tick what you did. Rename the 5 habits.', 'c-sb-habits')],
    inside=['Home dashboard + Today widget', 'Goals with progress bars', 'Projects board + Tasks', 'Next 7 days + calendar',
            'Notes inbox + Quick capture', 'Areas + Resources (PARA)', 'Habit tracker', 'Daily journal + mood board',
            'Reading list + weekly, monthly, yearly reviews', 'Bonus PDF: Notion for beginners'])
if __name__ == '__main__':
    want = sys.argv[1:]
    os.makedirs(os.path.join(L.OUT, 'sb'), exist_ok=True); os.makedirs(os.path.join(L.OUT, 'final', 'sb'), exist_ok=True)
    for pg in L.build('sb', 'file://' + os.path.join(L.ROOT, 'canva', 'v3') + '/LOCALMARK/'):
        pg2 = pg.replace('/LOCALMARK/crops/', '/crops/').replace('/LOCALMARK/', '/etsy/')
        lab = re.search(r'data-label="([^"]+)"', pg2).group(1)
        if want and not any(w in lab for w in want):
            continue
        L.render_png(pg2, os.path.join(L.OUT, 'final', 'sb', lab + '.png')); print('ok', lab)
