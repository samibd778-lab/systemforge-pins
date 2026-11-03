"""Second Brain OS Pinterest pins in the v3 lifestyle style (2x, 2000x3000), value hooks from marketing/pinterest-trends-2026-11.md.
Run: python3 generator/v3/sb_pins_v3.py -> pins/v3sb/<id>.png"""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sb_listing_v3  # registers the sb crops
L = sb_listing_v3.L; B = L.B
from PIL import Image
for n in ['habits', 'journal', 'mhome', 'tasks', 'capture']:
    B.CROPS[f'ph-sb-{n}'] = (f'sbph-{n}', (0, 0, 2000, 3657))
B.NAMES['sb'] = 'Second Brain OS'
LAP, PH = 'sb-lap', 'ph-sb-mhome'
S = [
 dict(id='sb-desk-layout', p='sb', style='desk', screens=[LAP, PH], title='Notion Layout Ideas', sub='One calm page for your whole life', chips=['Goals', 'Habits', 'Journal']),
 dict(id='sb-zoom-homepage', p='sb', style='zoom', screens=[LAP, PH], kicker='AESTHETIC NOTION HOMEPAGE', title='Steal this<br>Notion layout.', label='Today widget', cards=[['🌿 Your day at a glance', 'c-sb-widget'], ['🎯 Goals that fill up', 'c-sb-goals']]),
 dict(id='sb-hand-habits', p='sb', style='hand', screens=['ph-sb-habits'], kicker='HABIT TRACKER IDEAS', title='The habit tracker<br>I finally stuck to.', sub='Tick it on your phone in 10 seconds. Your score fills in by itself.'),
 dict(id='sb-studio-productive', p='sb', style='studio', screens=[LAP], title='Productive<br>aesthetic', sub='Goals, projects and habits in one Notion page', chips=['Goals', 'Projects', 'Habits']),
 dict(id='sb-flat-ideas', p='sb', style='flat', screens=[LAP, 'c-sb-habits'], kicker='NOTION TEMPLATE IDEAS', title=['Notion template<br>ideas for your', 'whole life.']),
 dict(id='sb-steps-secondbrain', p='sb', style='steps', screens=[], title='Build a second brain<br>in Notion', sub='4 steps. One calm page.', steps=[['Start your day', 'c-sb-widget'], ['Set a goal', 'c-sb-goals'], ['Plan the project', 'c-sb-projects'], ['Track the habit', 'c-sb-habits']]),
 dict(id='sb-hand-journal', p='sb', style='hand', screens=['ph-sb-journal'], kicker='JOURNAL IDEAS', title='A 2-minute<br>bedtime journal.', sub='Mood, one win and one thank you. On your phone.'),
 dict(id='sb-desk-digital', p='sb', style='desk', screens=[LAP, 'ph-sb-tasks'], title='Digital Planner', sub='I switched from paper to this', chips=['Next 7 days', 'Goals', 'Habits'], size=96),
 dict(id='sb-zoom-week', p='sb', style='zoom', screens=[LAP, 'ph-sb-tasks'], kicker='TIME MANAGEMENT AESTHETIC', title='Plan your week<br>in 15 minutes.', label='Every project', cards=[['🚀 Projects with progress', 'c-sb-projects'], ['✔️ Habits this week', 'c-sb-habits']]),
 dict(id='sb-studio-template', p='sb', style='studio', screens=[LAP], title='Second Brain<br>Notion Template', sub='Goals, notes, habits and journal', chips=['PARA method', 'Habit tracker', 'Journal']),
]
OUT = os.path.join(L.ROOT, 'pins', 'v3sb'); os.makedirs(OUT, exist_ok=True)
html_path = os.path.join(B.OUT, 'pins-sb.html')
B.build(S, html_path)
html = open(html_path).read().replace(B.RAW, 'file://' + B.OUT + '/')
F = os.path.join(L.ROOT, 'generator', 'remotion', 'public')
head = L.HEAD.replace('</head>', L.FONTS % (F, F, F) + '</head>')
for m in re.finditer(r'(<div data-document-role="page" data-label="([^"]+)".*?)(?=<div data-document-role="page"|</body>)', html, re.S):
    lab = m.group(2); h = os.path.join(OUT, '_p.html')
    open(h, 'w').write(head + m.group(1) + '</body></html>')
    shot = h + '.png'
    subprocess.run([B.CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=2', '--window-size=1000,1700', f'--screenshot={shot}', 'file://' + h], check=True, capture_output=True)
    Image.open(shot).crop((0, 0, 2000, 3000)).convert('RGB').save(os.path.join(OUT, lab + '.png'), optimize=True)
    os.remove(h); os.remove(shot); print('png', lab)
