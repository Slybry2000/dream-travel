# Dream Travel

Single-page GitHub Pages site focused on one audience: community leaders who want to host custom group trips with Dream Travel.

Live site: https://slybry2000.github.io/dream-travel/

## Current structure

- `index.html`: ambassador-first landing page
- legacy URLs (`about.html`, `journeys.html`, `contact.html`, etc.): redirects into relevant sections of `index.html`
- `backup/2026-04-14-pre-ambassador-pivot/`: full backup of the previous multi-page site before the repositioning

## Notes

- No build step required
- Designed to publish directly from the `main` branch on GitHub Pages
- Contact is intentionally direct via `mailto:` and phone instead of a fake form submission flow

## Local preview

Use any static server from the repo root, for example:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/`.
