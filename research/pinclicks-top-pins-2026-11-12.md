# PinClicks top pins — 2026-11-12

Keywords checked (Top Pins, Pinterest search): habit tracker (632K/mo), budget planner (226K), notion template (127K), notion budget template (3.3K).

## What the top pins share
- **The page itself fills the pin.** A tall printable / a tall Notion page screenshot, big and readable. No laptop or desk scene with a small screen (our v3/v4 style).
- **Light, clean background:** white, cream, soft pink or sage. Thin lines, lots of white space.
- **Big keyword title on the image:** script or elegant serif ("Habit Tracker", "Monthly Budget", "Monthly Bills"), or bold caps ("FREE PRINTABLE HABIT TRACKER", "50+ Free Notion Templates").
- **One promise:** a number or a bonus ("52 pages", "11 free printables", "30+ free PDF templates", "The Ultimate Monthly Budget Tracker").
- **Pin titles start with the keyword**, then a number or "Free" or "Template": "Monthly Budget Planners - 25 FREE Printables", "Printable Habit Trackers | 30+ Free PDF Templates", "Free Budget Planner Printable PDF (52 Pages)", "Habit Tracker Template Free Printable for Monthly…".
- **Old pins keep ranking:** many top pins are from 2018-2023. Pinterest is slow; a good pin works for months.
- "Free" + printable dominates habit/budget. Notion-only keywords are small but closer to us (Notion page screenshots in pastel, "Notion Template" label, Notion logo).

## What we changed
- `generator/v3/top_pins.py` → `pins/v5/`: page-first pins (style a: script keyword title + 2 real page cards; style b: serif caps band "MONTHLY ... for Notion" + big page crops + "Bonus PDF" badge).
- 6 pins (habit ×3, budget ×3) at the front of `etsy-pins.json` and `pins.json`.

## Next ideas
- Offer the bonus PDFs (30-Day Habit Reset, Money Reset in 7 Days) as a free printable on Gumroad ($0) to catch "free printable" searches, with an upsell to the Notion template.
- Re-check saves/outbound clicks per v5 pin after 14 days; keep the style that gets saves.
