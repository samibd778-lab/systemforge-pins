# SystemForge pins

Pinterest pin images (1000×1500) used by the n8n auto-poster.

- `pins.json` is the posting order. The workflow reads it on every run.
- To add a pin: upload the PNG, then add `{"id": "<file name without .png>", "p": "fco" or "ccs", "angle": "<what the image shows>"}` to the end of `pins.json`.
- `fco` = Freelancer Client OS, `ccs` = Content Creator Studio.


## Generator (real Notion screenshots)

All pins are now built from real screenshots of the templates (`shots/`) by `generator/gen.py`.

- `generator/pins-spec.json` lists every pin: id, product (`fco`/`ccs`), layout, screenshots, title, subtitle, chips and `angle` (what the image shows, used by the AI captions).
- Layouts: `laptop`, `combo` (laptop + phone), `phones`, `zoom` (only the columns that matter, glued together), `stack` (3 pages).
- Run `python3 generator/gen.py` to rebuild every PNG and `pins.json`. Add a pin = add one entry to the spec and run it.
