"""SVG/PNG covers (1500x600) for every sample row of the Job Application Tracker (Gumroad original).
Same warm style as mini_covers.py. Writes covers/job/<page_id>.png
Usage: python3 generator/job_covers.py"""
import os, asyncio
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, 'mini_covers.py')).read().split('# ================= PROPOSAL TRACKER')[0]
exec(_src)
C = {}
ST = {'Wishlist': GRAY, 'Applied': BLUE, 'Interviewing': ACC, 'Offer': SAGE, 'Rejected': RED, 'Ghosted': '#B07A57'}

APPS = [  # id, role, company, status, salary
    ('412727ea08a4818ba47bdec400cea785', 'Product Marketing Manager', 'Cobalt Labs', 'Interviewing', '$105,000'),
    ('412727ea08a481bd9f8cecd3ac960862', 'Marketing Manager', 'Lumen Health', 'Applied', '$95,000'),
    ('412727ea08a48132ad96f8fa534bd65d', 'Content Marketing Lead', 'Kitebird Media', 'Applied', '$82,000'),
    ('412727ea08a481c8b845f097f1b2a990', 'Social Media Manager', 'Kitebird Media', 'Applied', '$72,000'),
    ('412727ea08a481a98968f7a57bb58c4f', 'Growth Marketing Manager', 'Fernway Finance', 'Offer', '$118,000'),
    ('412727ea08a481238afac48d9901cdc0', 'Brand Marketing Manager', 'Harbor & Pine', 'Rejected', '$90,000'),
    ('412727ea08a4815a804cc8bb993a4b45', 'Email Marketing Manager', 'Lumen Health', 'Ghosted', '$88,000'),
    ('412727ea08a4814f8dc9df96ada93521', 'Marketing Specialist', 'Brightpath Learning', 'Wishlist', '$78,000'),
]
for i, (pid, role, comp, st, sal) in enumerate(APPS):
    lines = [role] if len(role) <= 18 else role.rsplit(' ', 1)
    C[pid] = base(i, title_block('APPLICATION', lines, [(comp, INK), (st, ST[st])], size=56) + ticket(comp.upper().replace(' LEARNING',''), sal, st, ST[st]))

INTS = [  # id, title lines, type, when, status
    ('412727ea08a4819bb669e33683583456', ['Cobalt Labs', 'Recruiter call'], 'Phone screen', 'Oct 24', ('Thank-you sent', SAGE)),
    ('412727ea08a48192b773c79b93e75b42', ['Cobalt Labs', 'Hiring manager'], 'Hiring manager', 'Nov 6', ('Send thank-you', ACC)),
    ('412727ea08a48178b7b5d8adbfe42d82', ['Cobalt Labs', 'Final round'], 'Final round', 'Nov 12', ('Prep first', ACC)),
    ('412727ea08a481bab10ec36e10748c0c', ['Fernway Finance', 'Final round'], 'Final round', 'Oct 20', ('Thank-you sent', SAGE)),
    ('412727ea08a481c58ab5ea840f3f21a8', ['Harbor & Pine', 'Phone screen'], 'Phone screen', 'Oct 9', ('Thank-you sent', SAGE)),
]
for i, (pid, lines, typ, when, badge) in enumerate(INTS):
    C[pid] = base(i + 1, title_block('INTERVIEW', lines, [(typ, INK), (when, ACC)], size=56)
                  + doc('CHECKLIST', [('Read the job post', SAGE), ('Pick 3 STAR stories', SAGE), ('3 questions to ask', SAGE), ('Thank-you email', badge[1])]))

COMPS = [
    ('412727ea08a48124af1dcf9173de2687', 'Lumen Health', 'Health'), ('412727ea08a48182adb8cd6a3d623262', 'Cobalt Labs', 'Tech'),
    ('412727ea08a481aa9100f01bee55d296', 'Harbor & Pine', 'Retail'), ('412727ea08a481369fd7fcb4d4811827', 'Fernway Finance', 'Finance'),
    ('412727ea08a481d095f6e1f367c255f3', 'Kitebird Media', 'Media'), ('412727ea08a481dd97b0e9f0f5c00351', 'Brightpath Learning', 'Education'),
]
for i, (pid, name, ind) in enumerate(COMPS):
    lines = [name] if len(name) <= 16 else name.split(' ', 1)
    C[pid] = base(i + 2, title_block('COMPANY', lines, [(ind, INK)], size=58) + person(i, name[0], ind))

PEOPLE = [
    ('412727ea08a4812384e3d2df357fe61f', 'Priya Shah', 'Recruiter', 'Lumen Health'),
    ('412727ea08a4817db957e3cd0c8a78b2', 'Tom Becker', 'Recruiter', 'Cobalt Labs'),
    ('412727ea08a481fa8753d29cf181e406', 'Maya Chen', 'Hiring manager', 'Cobalt Labs'),
    ('412727ea08a481deb685c2c668ed8b92', 'Emma Lopez', 'Referral', 'Brightpath'),
    ('412727ea08a4817c938cc1759e2de27c', 'Jordan Blake', 'Hiring manager', 'Fernway Finance'),
    ('412727ea08a48172abf1c205e683353c', 'Marcus Lee', 'Former colleague', 'Kitebird Media'),
]
for i, (pid, name, typ, comp) in enumerate(PEOPLE):
    ini = ''.join(w[0] for w in name.split())
    C[pid] = base(i, title_block('CONTACT', [name], [(typ, INK)], size=58) + person(i, ini, comp))

STORIES = [
    ('412727ea08a48166a537cd34485c277a', ['Launched a product', 'in 6 weeks'], 'Leadership', '+30%'),
    ('412727ea08a4811fb63ed360bd8bcfde', ['Fixed falling', 'sign-ups'], 'Problem solving', '+32%'),
    ('412727ea08a48193a3e8c40e797a5779', ['Two teams,', 'one launch date'], 'Conflict', 'Both said yes'),
    ('412727ea08a481b99331d960ea38990d', ['A campaign that', 'did not work'], 'Failure & learning', 'Half the cost'),
]
for i, (pid, lines, skill, res) in enumerate(STORIES):
    C[pid] = base(i, title_block('STAR STORY', lines, [(skill, INK)], size=56)
                  + doc('STAR', [('Situation', SAGE), ('Task', SAGE), ('Action', ACC), ('Result: ' + res, ACC)]))


async def main():
    from playwright.async_api import async_playwright
    out = os.path.join(os.path.dirname(HERE), 'covers', 'job'); os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1500, 'height': 600})
        for k, svg in C.items():
            await pg.set_content(f"<html><body style='margin:0'>{svg}</body></html>")
            await pg.screenshot(path=os.path.join(out, k + '.png'))
        await b.close()
    print(len(C))

asyncio.run(main())
