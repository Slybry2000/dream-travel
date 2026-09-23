# Trips library

Our own version of WeTravel's itinerary pages, without the $500 WeTravel website.

**Add or update a trip** (Rene keeps building itineraries in WeTravel as he does today):

    python _trips/import_wetravel.py https://dream-travel.wetravel.com/i/<id>
    python _trips/build.py

Then commit and push. The build prints the trip's private link.

**Link-only, on purpose.** Nobody can browse these pages. Each trip lives at an
unguessable address (`/trips/<trip>-<random key>/`), every page tells search engines
not to index it, nothing on the public site links here, and a trip page never links
to other trips. Only people Rene sends a link to can see it.

- One trip: `/trips/<trip>-<key>/` (split photo/text layout, like WeTravel's). Share this.
- Rene's overview of every trip: `/trips/<library key>/` (key in `config.json`), with a
  card page per country like dream-travel.net's France page. Do not share it.
- **Revoke a link:** change the trip's `"key"` in its JSON and rebuild. The old link dies.
- **Take a trip offline:** set `"status": "draft"` and rebuild.

This source folder starts with `_`, which GitHub Pages never publishes, so the data
files (which contain the keys) cannot be downloaded from the website.

**Without WeTravel:** copy any `data/*.json` file, delete its `"key"` and `"source"`,
edit the text, drop photos in `trips/images/<slug>/`, run `build.py`.

**Tag cards** (Classic, Small Group...): fill `"tags"`; re-imports keep your tags.
**Destination intro copy:** add `destinations.json` like `{"costa-rica": {"intro": ["..."]}}`.

**Show trips publicly on dream-travel.net** (only trips marked `"listed": true`, so
nothing appears there until Rene decides a trip should be public). Paste once into a
WordPress Custom HTML block:

    <div data-dream-trips="costa-rica"></div>
    <script src="https://adults.dream-travel.net/trips/embed.js" async></script>

Use `all` instead of a country slug to show every listed trip.
