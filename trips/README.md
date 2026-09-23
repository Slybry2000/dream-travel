# Trips library

Our own version of WeTravel's "trips auto-appear on your website" feature, without the
$500 WeTravel website.

**Add or update a trip** (Rene keeps building itineraries in WeTravel as he does today):

    python trips/import_wetravel.py https://dream-travel.wetravel.com/i/<id>
    python trips/build.py

Then commit and push. The trip gets its own page, and every listing that should show
it (its destination page, the all-trips page, and any dream-travel.net page with the
snippet below) picks it up by itself.

- Itinerary: `/trips/<country>/<trip>/` (split photo/text layout, like WeTravel's)
- Destination: `/trips/<country>/` (card grid, like dream-travel.net's France page)
- All trips: `/trips/`

**Without WeTravel:** copy any `data/*.json` file, edit the text, drop photos in
`images/<slug>/`, run `build.py`.

**Hide a trip:** set `"status": "draft"` in its JSON. **Tag cards** (Classic, Small
Group...): fill `"tags"`; re-imports keep your tags. **Destination intro copy:** add
`destinations.json` like `{"costa-rica": {"intro": ["...", "..."]}}`.

**Show trips on dream-travel.net** (WordPress, paste once into a Custom HTML block):

    <div data-dream-trips="costa-rica"></div>
    <script src="https://adults.dream-travel.net/trips/embed.js" async></script>

Use `all` instead of a country slug to show every trip.
