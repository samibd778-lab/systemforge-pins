"""SVG/PNG covers (1500x600) for the Meal Plan and Grocery List sample rows of the Meal Planner (Gumroad original).
Recipes use real food photos. Writes covers/meal/<page_id>.png. Usage: python3 generator/meal_covers.py"""
import os, asyncio
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, 'mini_covers.py')).read().split('# ================= PROPOSAL TRACKER')[0]
exec(_src)
C = {}
TY = {'Breakfast': ('#E0B04F', '🌅'), 'Lunch': (SAGE, '🥪'), 'Dinner': (BLUE, '🍝'), 'Snack': (PINK, '🍎')}
MEALS = [  # id, title, type, recipe, date, cooked
    ('412727ea08a4819da338f6a8a7ddca5b', 'Saturday dinner', 'Dinner', 'Sheet-Pan Chicken', 'Nov 7', True),
    ('412727ea08a481c1a768cca6c33e8549', 'Sunday lunch', 'Lunch', 'Sheet-Pan Chicken', 'Nov 8', True),
    ('412727ea08a481cd82b6e3f9f849d854', 'Monday breakfast', 'Breakfast', 'Overnight Oats', 'Nov 9', False),
    ('412727ea08a481d9b65dfa82ba67a360', 'Monday lunch', 'Lunch', 'Chickpea Veggie Bowl', 'Nov 9', False),
    ('412727ea08a481da9fdbe6f39ac4c1aa', 'Monday dinner', 'Dinner', 'Salmon Rice Bowl', 'Nov 9', False),
    ('412727ea08a4813b8312d8e4fd349cf1', 'Tuesday breakfast', 'Breakfast', 'Overnight Oats', 'Nov 10', False),
    ('412727ea08a481cd85fdcb22407cd40e', 'Tuesday lunch', 'Lunch', 'Salmon Rice Bowl', 'Nov 10', False),
    ('412727ea08a4814bb1ffe17a70206a40', 'Tuesday dinner', 'Dinner', 'Pesto Pasta', 'Nov 10', False),
    ('412727ea08a48105b743eb2e025e09c2', 'Wednesday breakfast', 'Breakfast', 'Eggs and Veggies', 'Nov 11', False),
    ('412727ea08a4814592fdd3c9217af37f', 'Wednesday lunch', 'Lunch', 'Greek Salad', 'Nov 11', False),
    ('412727ea08a481c29737d59438344be3', 'Wednesday dinner', 'Dinner', 'Chicken Noodle Bowl', 'Nov 11', False),
    ('412727ea08a481f784f5fdea520f51a6', 'Wednesday snack', 'Snack', 'Fruit Snack Plate', 'Nov 11', False),
    ('412727ea08a48190a907c3ecc2a4fa73', 'Thursday breakfast', 'Breakfast', 'Overnight Oats', 'Nov 12', False),
    ('412727ea08a48144ac14de3420e8d8a2', 'Thursday lunch', 'Lunch', 'Chicken Noodle Bowl', 'Nov 12', False),
    ('412727ea08a48186bf11ee18efe0259d', 'Thursday dinner', 'Dinner', 'Sheet-Pan Chicken', 'Nov 12', False),
    ('412727ea08a481a2b712ca2543324c1e', 'Friday breakfast', 'Breakfast', 'Eggs and Veggies', 'Nov 13', False),
    ('412727ea08a4819bb666cbae62136c4a', 'Friday lunch', 'Lunch', 'Egg Salad Sandwich', 'Nov 13', False),
    ('412727ea08a481e1b86cf5b732efa899', 'Friday dinner', 'Dinner', 'Pesto Pasta', 'Nov 13', False),
    ('412727ea08a481699b84c79ac0c60e82', 'Saturday dinner', 'Dinner', 'Salmon Rice Bowl', 'Nov 14', False),
    ('412727ea08a4816e8ba2cdf6e58c831e', 'Sunday lunch', 'Lunch', 'Chickpea Veggie Bowl', 'Nov 15', False),
]
def recipe_card(kicker, rec, badge, col):
    out = f"<rect x='980' y='120' width='300' height='360' rx='18' fill='{PAPER}'/><text x='1010' y='170' font-family='{SANS}' font-size='18' font-weight='700' fill='{MUT}' letter-spacing='3'>{esc(kicker)}</text>"
    for j, w in enumerate((200, 160, 220)):
        out += f"<rect x='1010' y='{200+j*30}' width='{w}' height='12' rx='6' fill='{LINE}'/>"
    words = rec.split(' '); l1, l2 = '', ''
    for w in words:
        if len(l1 + ' ' + w) <= 13 and not l2: l1 = (l1 + ' ' + w).strip()
        else: l2 = (l2 + ' ' + w).strip()
    out += f"<text x='1010' y='330' font-family='{SERIF}' font-size='30' font-weight='700' fill='{INK}'>{esc(l1)}</text>"
    if l2: out += f"<text x='1010' y='368' font-family='{SERIF}' font-size='30' font-weight='700' fill='{INK}'>{esc(l2)}</text>"
    bw = tw(badge, 18) + 40
    out += f"<rect x='1010' y='410' width='{bw}' height='38' rx='19' fill='{col}'/><text x='1030' y='435' font-family='{SANS}' font-size='18' font-weight='700' fill='{PAPER}'>{esc(badge)}</text>"
    return out


for i, (pid, title, ty, rec, d, cooked) in enumerate(MEALS):
    col, _ = TY[ty]
    lines = title.split(' ', 1)
    C[pid] = base(i, title_block('MEAL PLAN', lines, [(d, INK), (ty, col)], size=56)
                  + recipe_card(ty.upper(), rec, 'Cooked' if cooked else 'Planned', SAGE if cooked else col))

AI = {'Produce': SAGE, 'Dairy & eggs': '#E0B04F', 'Meat & fish': RED, 'Pantry': ACC, 'Bakery': '#B07A57', 'Frozen': BLUE, 'Other': GRAY}
GROC = [  # id, item, aisle, qty, got
    ('412727ea08a481b89831ed817b6a7a40', 'Salmon fillets', 'Meat & fish', '4 fillets', False),
    ('412727ea08a48195be70d43356194278', 'Chicken thighs', 'Meat & fish', '4', False),
    ('412727ea08a48184a576c9349ab77055', 'Chicken breasts', 'Meat & fish', '2', True),
    ('412727ea08a48145b7c1e6ea761f0c7e', 'Eggs', 'Dairy & eggs', '1 dozen', False),
    ('412727ea08a481eda649c9915907a707', 'Greek yogurt', 'Dairy & eggs', '32 oz tub', False),
    ('412727ea08a4818db88dc7afb744a25f', 'Feta', 'Dairy & eggs', '4 oz', False),
    ('412727ea08a4815da037e54756b034bc', 'Berries', 'Produce', '2 boxes', False),
    ('412727ea08a48193b883f522cb8859ef', 'Broccoli', 'Produce', '1 head', True),
    ('412727ea08a481beb521edf1ba0db5f9', 'Sweet potatoes', 'Produce', '2', False),
    ('412727ea08a48145844cc0d13c9b4d56', 'Avocado', 'Produce', '2', False),
    ('412727ea08a481f9a0a1dcf09365eadf', 'Cherry tomatoes', 'Produce', '2 pints', False),
    ('412727ea08a48151bf07c15223f0cdfa', 'Cucumbers', 'Produce', '2', False),
    ('412727ea08a481b8944fdd8839cd41c2', 'Chickpeas', 'Pantry', '2 cans', False),
    ('412727ea08a481c9875ae5720124f700', 'Pasta', 'Pantry', '1 lb', True),
    ('412727ea08a4814dac27ca127bcfe5d3', 'Pesto', 'Pantry', '1 jar', False),
    ('412727ea08a481f3a5f6f4f3a8b1855c', 'Rolled oats', 'Pantry', '1 bag', True),
    ('412727ea08a4810381f0f4fa8f5cabfb', 'Whole grain bread', 'Bakery', '1 loaf', False),
    ('412727ea08a4819ba974cfbc25244c4e', 'Frozen peas', 'Frozen', '1 bag', False),
    ('412727ea08a481bcbd64e664bc78c0fd', 'Dish soap', 'Other', '1', False),
]
for i, (pid, item, aisle, qty, got) in enumerate(GROC):
    lines = [item] if len(item) <= 16 else item.rsplit(' ', 1)
    C[pid] = base(i, title_block('GROCERY LIST', lines, [(aisle, AI[aisle]), (qty, INK)], size=58)
                  + doc('SHOPPING', [(item, AI[aisle]), ('Check the pantry', SAGE), ('Got it' if got else 'Still to buy', SAGE if got else ACC)]))


async def main():
    from playwright.async_api import async_playwright
    out = os.path.join(os.path.dirname(HERE), 'covers', 'meal'); os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1500, 'height': 600})
        for k, svg in C.items():
            await pg.set_content(f"<html><body style='margin:0'>{svg}</body></html>")
            await pg.screenshot(path=os.path.join(out, k + '.png'))
        await b.close()
    print(len(C))

asyncio.run(main())
