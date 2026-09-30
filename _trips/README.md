# Trips library

Our own version of WeTravel's itinerary pages, without the $500 WeTravel website.

**Add or update a trip** (Rene keeps building itineraries in WeTravel as he does today):

    python _trips/import_wetravel.py https://dream-travel.wetravel.com/i/<id>
    python _trips/build.py

Then commit and push. The trip's card appears on Rene's private list and its country
page, and clicking it opens the trip on WeTravel. WeTravel stays the one place the
itinerary lives, so Rene's edits there show immediately. Re-import only when the title,
photo, days or places on the card change. (Set `"host_copy": true` on a trip to host
our own copy of the itinerary instead.)

**The overview is public (changed 2026-09-30).** The all-trips page and its country pages
are linked from the homepage orbit ("See all sample trips" plus one card per destination)
and search engines may index them. Hand-made trip pages (`/trips/<trip>-<random key>/`)
are still link-only: noindex, unguessable address, never linked from other trips.

- One trip: `/trips/<trip>-<key>/` (split photo/text layout, like WeTravel's). Share this.
- Overview of every trip: `/trips/<library key>/` (key in `config.json`), with a card page
  per country like dream-travel.net's France page. Its hero crossfades through the photos
  listed in `config.json` `"hero_rotation"` (paths under `trips/`); delete that list to
  rotate through every trip's cover photo instead. Each country page rotates its own
  photos from `config.json` `"country_heroes"` (keyed by country slug); a country with no
  list there rotates its trips' cover photos.
- **New country?** Add a matching card to the orbit in `/index.html` by hand.
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
