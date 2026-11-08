"""SVG/PNG covers (1500x600) for Itinerary, Expenses and Packing List sample rows of the Travel Planner (Gumroad original).
Trips use real destination photos. Writes covers/travel/<page_id>.png. Usage: python3 generator/travel_covers.py"""
import os, asyncio
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, 'mini_covers.py')).read().split('# ================= PROPOSAL TRACKER')[0]
exec(_src)
C = {}
TY = {'Flight': BLUE, 'Stay': PURP, 'Activity': SAGE, 'Food': ACC, 'Transport': GRAY}


def info_card(kicker, big, sub, badge, col):
    out = f"<rect x='980' y='120' width='300' height='360' rx='18' fill='{PAPER}'/><text x='1010' y='170' font-family='{SANS}' font-size='18' font-weight='700' fill='{MUT}' letter-spacing='3'>{esc(kicker)}</text>"
    for j, w in enumerate((200, 160, 220)):
        out += f"<rect x='1010' y='{200+j*30}' width='{w}' height='12' rx='6' fill='{LINE}'/>"
    out += f"<text x='1010' y='335' font-family='{SERIF}' font-size='34' font-weight='700' fill='{INK}'>{esc(big)}</text>"
    out += f"<text x='1010' y='370' font-family='{SANS}' font-size='17' fill='{MUT}'>{esc(sub)}</text>"
    bw = tw(badge, 18) + 40
    out += f"<rect x='1010' y='410' width='{bw}' height='38' rx='19' fill='{col}'/><text x='1030' y='435' font-family='{SANS}' font-size='18' font-weight='700' fill='{PAPER}'>{esc(badge)}</text>"
    return out


def lines_of(t):
    if len(t) <= 17: return [t]
    w = t.split(' '); best = None
    for k in range(1, len(w)):
        a, b = ' '.join(w[:k]), ' '.join(w[k:])
        sc = max(len(a), len(b))
        if best is None or sc < best[0]: best = (sc, [a, b])
    return best[1]

ITIN = [  # id, plan, trip, type, when, booked, cost
    ('412727ea08a481d8bfb4ce9f48362d03', 'Flight to Lisbon', 'Lisbon', 'Flight', 'Dec 10', True, '$980'),
    ('412727ea08a48152a6edc150208b8332', 'Hotel in Alfama', 'Lisbon', 'Stay', 'Dec 11', True, '$760'),
    ('412727ea08a4812baa20fc49c5aad6d5', 'Tram 28 ride', 'Lisbon', 'Transport', 'Dec 11', False, '$14'),
    ('412727ea08a48174adbdedc43482b428', 'São Jorge Castle', 'Lisbon', 'Activity', 'Dec 11', True, '$36'),
    ('412727ea08a481658f88e75d7ed75a59', 'Dinner at a fado house', 'Lisbon', 'Food', 'Dec 11', False, '$120'),
    ('412727ea08a48143878cfc82c81890e4', 'Belém and pastel de nata', 'Lisbon', 'Activity', 'Dec 12', False, '$40'),
    ('412727ea08a481559f87d3d19e9d1eba', 'Day trip to Sintra', 'Lisbon', 'Transport', 'Dec 13', False, '$12'),
    ('412727ea08a4817b813adeee391929d4', 'Pena Palace tickets', 'Lisbon', 'Activity', 'Dec 13', True, '$40'),
    ('412727ea08a481fd957bca1b93c8aeca', 'Food tour in Baixa', 'Lisbon', 'Food', 'Dec 14', True, '$150'),
    ('412727ea08a48105961ecb9b7fac578b', 'Flight home', 'Lisbon', 'Flight', 'Dec 15', True, ''),
    ('412727ea08a4810eaa0bd5ea75d08f81', 'Hotel in Shinjuku', 'Tokyo', 'Stay', 'Apr 2', False, '$1,800'),
    ('412727ea08a48101bd74d7902a09b751', 'Ueno Park cherry blossoms', 'Tokyo', 'Activity', 'Apr 4', False, ''),
    ('412727ea08a481079585f9d220001343', 'Bullet train to Kyoto', 'Tokyo', 'Transport', 'Apr 7', False, '$240'),
]
for i, (pid, plan, trip, ty, when, booked, cost) in enumerate(ITIN):
    C[pid] = base(i, title_block('ITINERARY', lines_of(plan), [(trip, INK), (when, TY[ty])], size=54)
                  + info_card(ty.upper(), cost or when, trip, 'Booked' if booked else 'Book it', SAGE if booked else ACC))

CAT = {'Flights': BLUE, 'Stay': PURP, 'Food': ACC, 'Activities': SAGE, 'Transport': GRAY, 'Other': '#B07A57'}
EXP = [
    ('412727ea08a4815ea470cc2cf2912e84', 'Round-trip flights', 'Lisbon', 'Flights', '$980', 'Alex'),
    ('412727ea08a481e59195d807a9aab281', 'Hotel (4 nights)', 'Lisbon', 'Stay', '$760', 'Sam'),
    ('412727ea08a4812fb1a5fd96692b2410', 'Castle and palace tickets', 'Lisbon', 'Activities', '$76', 'Alex'),
    ('412727ea08a4811d93baf6d2ae0d03ab', 'Food tour', 'Lisbon', 'Food', '$150', 'Sam'),
    ('412727ea08a481c68e72e9f84c7f1d88', 'Rental car (6 days)', 'Banff', 'Transport', '$540', 'Jordan'),
    ('412727ea08a481fabaf4f7c183cc6a72', 'Cabin near Banff', 'Banff', 'Stay', '$1,380', 'Alex'),
    ('412727ea08a481b59212c404410f8382', 'Flights to Calgary', 'Banff', 'Flights', '$860', 'Sam'),
    ('412727ea08a481908b16ee13e3a835dc', 'Groceries and restaurants', 'Banff', 'Food', '$420', 'Jordan'),
    ('412727ea08a481ed8c16c30d1a2cd338', 'Canoe rental', 'Banff', 'Activities', '$140', 'Alex'),
    ('412727ea08a481559122e7432706ea58', 'Parks pass', 'Banff', 'Other', '$75', 'Sam'),
]
for i, (pid, name, trip, cat, amt, who) in enumerate(EXP):
    C[pid] = base(i + 1, title_block('EXPENSE', lines_of(name), [(trip, INK), (cat, CAT[cat])], size=54)
                  + info_card(cat.upper(), amt, 'Paid by ' + who, trip, CAT[cat]))

PC = {'Documents': RED, 'Clothes': BLUE, 'Toiletries': PINK, 'Tech': PURP, 'Health': SAGE, 'Other': GRAY}
PACK = [
    ('412727ea08a4813fb64cdc59ad890da6', 'Passports', 'Documents', True), ('412727ea08a481458447feaf5029c310', 'Printed bookings', 'Documents', True),
    ('412727ea08a481398f89cd6a73bac2a3', 'Travel card + cash', 'Documents', False), ('412727ea08a48150b6cfd3618eec4c0d', 'Warm jacket', 'Clothes', True),
    ('412727ea08a48141bfb7e041e95d3ab9', 'Walking shoes', 'Clothes', False), ('412727ea08a481f0b3b1e6186b8788f7', 'T-shirts', 'Clothes', False),
    ('412727ea08a481d3a1b6d2b93e30a880', 'Dinner outfit', 'Clothes', False), ('412727ea08a481d3a8f1ed6559ed73dd', 'Small umbrella', 'Other', False),
    ('412727ea08a4811d94b4cd9757f358f3', 'Toothbrush', 'Toiletries', False), ('412727ea08a481d2b10ee04425abed66', 'Travel toiletries', 'Toiletries', True),
    ('412727ea08a481c9ad7bf23d1418ac58', 'Plug adapter', 'Tech', True), ('412727ea08a4818cafe3e1abdc383204', 'Power bank', 'Tech', False),
    ('412727ea08a48135a4e8d6b749638907', 'Headphones', 'Tech', False), ('412727ea08a481958bdfd312a2403475', 'First aid kit', 'Health', False),
]
for i, (pid, item, cat, packed) in enumerate(PACK):
    C[pid] = base(i, title_block('PACKING LIST', [item], [(cat, PC[cat]), ('Lisbon', INK)], size=58)
                  + doc('SUITCASE', [(item, PC[cat]), ('Check the weather', SAGE), ('Packed' if packed else 'Still to pack', SAGE if packed else ACC)]))


async def main():
    from playwright.async_api import async_playwright
    out = os.path.join(os.path.dirname(HERE), 'covers', 'travel'); os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1500, 'height': 600})
        for k, svg in C.items():
            await pg.set_content(f"<html><body style='margin:0'>{svg}</body></html>")
            await pg.screenshot(path=os.path.join(out, k + '.png'))
        await b.close()
    print(len(C))

asyncio.run(main())
