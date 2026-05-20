# Dream Travel

Single-page site for community leaders who host custom group trips with Dream Travel. Image-first hero with the host as subject; the partnership (host fills the seats, Dream Travel carries the trip) is the visible center of the page.

Served at the repository root via GitHub Pages (`main` branch, `/`).

Live: https://slybry2000.github.io/perseid-echo-demos/

## Structure

- `index.html` — landing page
- `styles.css` — site stylesheet
- `ART-BIBLE.md` — binding design spec for future sections
- `images/` — hero photos (art-directed desktop + mobile crops) and logos
- Legacy URLs (`about.html`, `adult-travel.html`, `ambassador.html`, `contact.html`, `experiences.html`, `journeys.html`, `private-custom-group-tours.html`) redirect to the matching anchor on `index.html`

## Notes

- No build step. Hand-authored HTML/CSS.
- GitHub Pages publishes from the `main` branch root.
- Contact flows use direct `mailto:` and `tel:` — no fake form submission.
- The previous multi-demo index (Perseid Echo demos + Riley Lawns) is preserved on the `archive/demos-index` branch.

## Local preview

Serve the repo root with any static server:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/`.
