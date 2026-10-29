"""SVG/PNG covers (1500x600) for every page and sample row of Second Brain OS (Gumroad original).
Same warm style as mini_covers.py. Writes covers/sb/<page_id>.png
Usage: python3 generator/sb_covers.py"""
import os, asyncio
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, 'mini_covers.py')).read().split('# ================= PROPOSAL TRACKER')[0]
exec(_src)
C = {}
K = 'SECOND BRAIN OS'

# pages
C['408727ea08a4819392b7fc08c7c10b92'] = base(0, title_block(K, ['Capture it.', 'Find it again.']) + steps(786, ['Capture', 'Organize', 'Distill', 'Express'], [ACC, SAGE, '#B07A57', GRAY]))
C['408727ea08a481b4b465cdca54a32510'] = base(1, title_block(K, ['Start here'], [('5 minutes', SAGE), ('6 steps', ACC)]) + doc('SET UP', [('Clean the sample data', SAGE), ('Add your areas', SAGE), ('Add your projects', SAGE), ('Capture into Notes', ACC), ('Sort once a week', ACC)]))
C['408727ea08a481dfa351f41f1423bba6'] = base(2, title_block(K, ['Weekly review'], [('15 minutes', SAGE)]) + doc('EVERY WEEK', [('Clear the inbox', SAGE), ('Check projects', SAGE), ('Plan the week', ACC), ('Distill 3 notes', ACC)]))
C['408727ea08a4810d95f2c9025a3c8fc0'] = base(0, title_block(K, ['How PARA works']) + doc('4 PLACES', [('Projects', ACC), ('Areas', SAGE), ('Resources', '#B07A57'), ('Archive', GRAY)]))
C['408727ea08a481309cdbda07956240b3'] = base(1, title_block(K, ['Archive'], [('Done', SAGE), ('Paused', GRAY)]) + doc('KEPT FOR LATER', [('Finished projects', SAGE), ('Old areas', GRAY), ('Old resources', GRAY)]))

AREAS = [('408727ea08a4819d94a2d2bbb97788b6', 'Work', 'Weekly'), ('408727ea08a481aeb5bfd15a6121ad89', 'Money', 'Monthly'),
         ('408727ea08a481189b67ddb8a1acdeb9', 'Health', 'Weekly'), ('408727ea08a481ddad24efd45b2fe502', 'Home', 'Monthly'),
         ('408727ea08a481569493d5a696aa36e8', 'Learning', 'Monthly'), ('408727ea08a48102bb3dfd3d0b6aa486', 'Family & friends', 'Weekly')]
for i, (pid, name, rev) in enumerate(AREAS):
    C[pid] = base(i, title_block('AREA', [name], [(rev + ' review', INK)], size=58) + person(i, name[0], name))

PROJECTS = [('408727ea08a481969db3ecf76f588ecd', 'Portfolio website', 'Nov 15', 'In progress', ACC),
            ('408727ea08a48155b156d90b82d35827', 'Run a 10K', 'Dec 6', 'In progress', ACC),
            ('408727ea08a481848cd9f67821d7db08', 'Lisbon trip', 'Nov 20', 'Next up', '#B07A57'),
            ('408727ea08a481a2a304f553ed63576b', 'Tax receipts', 'Nov 30', 'Next up', '#B07A57'),
            ('408727ea08a481f6b2dfda7bc4d9f2c5', 'Figma basics', 'Oct 20', 'On hold', GRAY),
            ('408727ea08a48194b2c4ce98bb1e6c5a', 'Home office', 'Oct 10', 'Done', SAGE),
            ('408727ea08a481ecaad7e824c8389ead', 'New apartment', 'Aug 31', 'Archived', GRAY)]
for i, (pid, name, due, st, col) in enumerate(PROJECTS):
    C[pid] = base(i, title_block('PROJECT', [name], [(st, col)], size=56) + ticket('DEADLINE', due, st, col))

TASKS = [('408727ea08a481f8bd63dd5609990e3b', 'Case study #1', 'Done', SAGE), ('408727ea08a481318e5cf356b9f0599f', 'Case study #2', 'High', ACC),
         ('408727ea08a4812a9849c8630447757f', 'Domain name', 'Done', SAGE), ('408727ea08a481d39b72fc2aad3a510c', 'Client quotes', 'This week', '#B07A57'),
         ('408727ea08a481a29eaec04e5d7b5416', 'Publish the site', 'High', ACC), ('408727ea08a4812faa13f52fcc7b4fe3', 'Running shoes', 'Done', SAGE),
         ('408727ea08a48192a7aeea8633cdf744', 'Run 3 times', 'This week', '#B07A57'), ('408727ea08a481c58d10de986988abd7', 'Sign up for the race', 'High', ACC),
         ('408727ea08a481e68d8fce07b463f802', 'Book the flights', 'High', ACC), ('408727ea08a4815487cbdc4571599c8f', 'Places to see', 'No date', GRAY),
         ('408727ea08a4812c905ffacf23f257fc', 'Pull receipts', 'Soon', '#B07A57'), ('408727ea08a48187b326cb4dd2ee2ce8', 'Finish lesson 3', 'Late', RED),
         ('408727ea08a481799aabf5ad48eafd6e', 'Desk lamp', 'Done', SAGE), ('408727ea08a4814ca771ef5b0144d525', 'New chair', 'Done', SAGE)]
for i, (pid, name, badge, col) in enumerate(TASKS):
    C[pid] = base(i, title_block('TASK', [name], [(badge, col)], size=54) + doc('NEXT ACTION', [(name, col), ('Tick it when done', SAGE), ('Linked to a project', GRAY)]))

RES = [('408727ea08a481a4880ffcafd2a0d420', 'Building a Second Brain', 'Book', 'Finished'), ('408727ea08a481409481ec50a7848580', 'Atomic Habits', 'Book', 'To read'),
       ('408727ea08a4814cb02dd1f18bd79601', 'Web design', 'Topic', 'Reference'), ('408727ea08a481ca9214e0056998e02c', 'Running plans', 'Topic', 'Reference'),
       ('408727ea08a481a3aeaec60ad19c06bf', 'Design basics', 'Course', 'In progress'), ('408727ea08a481c6b350ca7b97fd0991', 'Weeknight recipes', 'Topic', 'Reference'),
       ('408727ea08a48123a832e2283aa24e09', 'Money podcasts', 'Podcast', 'To read')]
for i, (pid, name, typ, st) in enumerate(RES):
    C[pid] = base(i, title_block('RESOURCE', [name], [(typ, INK), (st, SAGE)], size=50) + doc(typ.upper(), [('Saved notes', SAGE), ('Key takeaways', ACC), ('Linked to an area', GRAY)]))

NOTES = [('408727ea08a4817a9debf0f987334504', 'Client newsletter', 'Idea', 'Sort me'), ('408727ea08a4813a83eeec7faf788370', 'Gift ideas', 'Idea', 'Sort me'),
         ('408727ea08a481f6b0edd6474d5473c3', 'Leaking tap', 'Note', 'Sort me'), ('408727ea08a4813aabe0c431819d988b', 'Case study outline', 'Note', 'Project'),
         ('408727ea08a481bd8730d61de50d8a95', 'Call with Maya', 'Meeting', 'Project'), ('408727ea08a48120b9c1e3444addbf22', 'Interval workout', 'Note', 'Project'),
         ('408727ea08a4818d9f42ff1e0d67edec', 'Lisbon cafes', 'Link', 'Project'), ('408727ea08a48157b840c07030a8fc9d', 'Pricing a website', 'Link', 'Resource'),
         ('408727ea08a481cf9518cf66337a61f7', 'Capture what resonates', 'Highlight', 'Resource'), ('408727ea08a481d8bba1cfb353fe6630', 'Monthly money check', 'Note', 'Area')]
for i, (pid, name, typ, home) in enumerate(NOTES):
    col = ACC if home == 'Sort me' else SAGE
    C[pid] = base(i, title_block('NOTE', [name], [(typ, INK), (home, col)], size=50) + doc('DISTILL', [('Capture', SAGE), ('Give it a home', col), ('Key takeaway', ACC)]))


async def main():
    from playwright.async_api import async_playwright
    out = os.path.join(os.path.dirname(HERE), 'covers', 'sb'); os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1500, 'height': 600})
        for k, svg in C.items():
            await pg.set_content(f"<html><body style='margin:0'>{svg}</body></html>")
            await pg.screenshot(path=os.path.join(out, k + '.png'))
        await b.close()
    print(len(C))

asyncio.run(main())
