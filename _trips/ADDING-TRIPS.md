# Adding adult trips: Drive PDF → WeTravel → sheet → website

The standard operating procedure for turning Rene's trip PDFs into published WeTravel trips,
logging them, and showing them on adults.dream-travel.net. Follow it top to bottom for every
batch. Proven end to end on 2026-10-23 (8 art trips). Start it in Claude with `/add-wetravel-trips`.

## Golden rules

1. **Adult trips only.** Never touch student trips (school names, "HS", "Exchange", years) or
   pickleball trips (their own brand, named "Pickleball <Country>: ..."). The tools refuse any
   trip that is not in `_trips/adult_trips.json`; never add a student or pickleball trip to it.
2. **Same result as Rene's own process.** WeTravel's Smart Import (PDF → itinerary, with its own
   Unsplash photos) only exists in the WeTravel screens, so trips are built there; the API is used
   afterwards to check and fix them.
3. **No client names in public.** If a trip names a client (an "ABOUT <their business>" section,
   "with First Last" or a year in a heading), do not put it on the website. Ask Rene first.
   The repo is public: never commit a client's name, even in notes.
4. **Every trip is private, group 1-25, Dates Not Decided**, like Rene's.
5. **Read before writing shared things.** Other Claude sessions edit this repo; commit only your
   own paths and never another session's uncommitted changes.

## Where everything is

| What | Where |
|---|---|
| New PDFs | Drive (open as Google account `/u/2`): DREAM-TRAVEL ADULTS > ART RELATED TRIPS > **SOME PDF** (folder `1MhvCDpFsM5Roqr2dp6G-VHo1LMoboKaK`). Wellness PDFs live in WELLNESS PROGRAMS. |
| Done PDFs | the **ON WETRAVEL** folder inside SOME PDF |
| Tracking sheet | "TRIPS ON WETRAVEL", sheet `1l3t8Dn-thlJSgEzYjbMzS3i1vGroNQy4zRKQYa0Oj_E`, columns Type, Country, Name on WeTravel, Company/partner, Code (no longer used), Link |
| WeTravel | dream-travel.wetravel.com, Bryan's login (bryan@dream-travel.net) in the Chrome profile Claude in Chrome uses |
| API key | `WETRAVEL_API_KEY` in `Dream-Travel/.env` (Rene's Partner API key, Pro plan). Never print or commit it. |
| Adult trip list | `_trips/adult_trips.json`, the allowlist every tool checks |
| Tools | `_trips/tools/` (below) and `_trips/import_wetravel.py`, `_trips/build.py` |
| Website | adults.dream-travel.net (GitHub Pages, repo Slybry2000/dream-travel, deploys from `main`) |

## Naming rule: `Country: Theme`

Country first, colon, space, then what the trip is about, e.g. `France: Provence Art, Culture & Heritage`,
`Italy & Slovenia: Art & Mosaic Discovery`, `Costa Rica: Yoga Retreat in Arenal`.
No day counts, no codes (CRW1, BoW1), no "Itinerary"/"WeTravel", no years. The area (Provence,
Algarve, Arenal) goes after the colon. Use the trip's own headline from the PDF for the theme.
`wetravel.title_problems()` enforces this; the same name goes in WeTravel, the sheet and the website.

## Tools (`_trips/tools/`, run from the Dream-Travel folder)

| Command | What it does |
|---|---|
| `python _trips/tools/trip_qa.py [uuid ...]` | Read-only check of every adult trip (or the ones given): name, private/1-25/no dates, a photo on every day, same photo twice (by look), photos over 800 KB, possible client names, short link opens. Exit 1 if anything needs fixing. |
| `python _trips/tools/trip_photos.py <uuid> --set "Day 5 -=<unsplash id>" --optimize --warm` | Puts chosen Unsplash photos on days, swaps all photos for page-ready copies, pre-loads them. Backs up first, then proves only photos changed. |
| `python _trips/tools/trip_rename.py <uuid> "Country: Theme"` | Renames a bookable trip via the API; rejects bad names and non-adult trips. |
| `python _trips/tools/trip_register.py <uuid> --country X --category "Art & Culture" --link https://tri.ps/xxxxx` | Adds a new trip to the allowlist. Refuses student/pickleball names. |
| `python _trips/import_wetravel.py https://dream-travel.wetravel.com/i/<itinerary id> --country X --category "Art & Culture"` | Copies a trip onto the website library (card data + photos). |
| `python _trips/build.py` | Rebuilds the website's trip pages. |

On Windows set `PYTHONIOENCODING=utf-8` first so accented names print.

## The procedure

### 1. Collect the PDFs
- Open the SOME PDF folder in Chrome. Anything still in SOME PDF (not in ON WETRAVEL) is to do.
- Select all new PDFs (click first, shift-click last) > Download. Drive zips them.
- Chrome may leave the file as `*.crdownload`; it is complete. Copy it to `.tmp/pdfs/batch.zip`
  and unzip with Python (`zipfile`). Read each PDF's first lines (pypdf) to confirm the trip.
- Name each trip now (rule above) from the PDF's headline, plus country, category and length.

### 2. Build each trip in WeTravel (Claude in Chrome)
Run 2-3 trips in parallel tabs: Smart Import builds on WeTravel's servers (about 2 minutes).
Finish each trip in the front tab; background tabs freeze and time out.

1. Open `https://dream-travel.wetravel.com/itinerary_builder/new?skipPaymentLinkValidation=yes`.
2. **Trip Title:** the standard name. **Destination:** type the country, pick the plain country suggestion.
3. **Trip is Offered:** it is a native select; set "Dates Not Decided" with form_input, then set
   **Trip Length** (click it, ctrl+a, type the days).
4. **Cover photo:** Search Photos Online > search the trip's best-known sight > pick a wide shot >
   Upload > **Save** on the "Re-center photo" box.
5. **Group size is prefilled 1 / 25. Do not type in it** (typing appends: "11" / "2525"). If it
   happened: click the box, ctrl+a, Backspace, retype.
6. Leave **Private**. Next.
7. **Trip Page:** Smart Import > Upload PDF file. This opens a Filestack picker; find its
   `input type=file` and use file_upload with the PDF path (clicking the button only opens
   Windows' picker). Upload > **Create Itinerary**. Wait about 2 minutes; the tab moves to the editor.
8. Back to the builder: open `https://dream-travel.wetravel.com/itinerary_builder/<trip number>#/builder/packages`.
   **Packages and pricing: No.** **eSignature: No.** Add-ons, carbon offset, traveler form and
   settings stay as they are. **Publish.**
9. On "Your trip is ready to share": **Shorten URL**, read the tri.ps link. Letters like `I`/`l`
   look alike: confirm with `curl -sI https://tri.ps/<code>` (the right one redirects to the trip).
10. Note the trip number (in the builder URL) and the short link.

### 3. Register, check and fix (API)
```
python _trips/tools/trip_register.py <uuid> --country <Country> --category "Art & Culture" --link https://tri.ps/<code>
python _trips/tools/trip_qa.py <uuid> ...
```
For each "no photo" or "same photo twice": find a fitting Unsplash photo (snippet below), then
```
python _trips/tools/trip_photos.py <uuid> --set "Day 7 -=<id>" --set "Journey Highlights=<id>" --optimize --warm
```
Always run `--optimize --warm` once per new trip, even with nothing to replace. Re-run
`trip_qa.py` until the trip is OK (a "possible client name" flag means stop and ask Rene).

**Finding Unsplash photos.** Unsplash blocks scripts, so search from the browser: open
`https://unsplash.com/` in the Chrome tab and run in javascript_tool:
```js
const r = await fetch('/napi/search/photos?per_page=8&orientation=landscape&query=' + encodeURIComponent('Pont-Aven Brittany')).then(r => r.json());
r.results.filter(x => !x.premium && !x.plus).slice(0, 4).map(x => new URL(x.urls.raw).pathname.slice(7) + ' ' + (x.alt_description || '')).join('\n')
```
The printed id (after `photo-`) is what `--set` takes. Look at candidates before using them
(download `https://images.unsplash.com/photo-<id>?w=300` and view), and make sure the pick is not
already used on that trip; the QA check catches it if it is.

### 4. Tags (WeTravel > Trips > Upcoming Trips)
Hover the trip > **Add tags**: `ADULTS TRIP`, the type tag (`ART` for art trips) and the country
tag (`France`, `IRELAND`, `PORTUGAL`, `Spain`, `Italy`...). Search the tag; pick the existing one,
never "Create new" unless the country has no tag yet (Slovenia was created this way).

### 5. Sheet (TRIPS ON WETRAVEL)
Add one row per trip under the matching block (ART rows at the bottom): `Type | COUNTRY | Name |
(partner) | (code, leave blank) | https://tri.ps/<code>`. Art rows use an UPPERCASE country
(`ITALY & SLOVENIA`). Wellness rows use "Wellness" and Title Case countries.
- Jump to the cell with the Name Box (top-left), type a cell, press **Delete** (kills Google's
  autocomplete, which turned "PORTUGAL" into "PORTUGAL & SPAIN" once), then Tab to the next cell.
  Never type tab characters inside one text.
- Check by reading `.../htmlview`: every new row and link correct.

### 6. Move the PDFs
In SOME PDF select the done PDFs > right-click > Organize > Move > **ON WETRAVEL** > Move > Move
again on Drive's "Change who has access?" notice (same shared folder, nothing changes for anyone).
SOME PDF should then hold only the ON WETRAVEL folder and anything still to do. Never delete PDFs.

### 7. Website
```
python _trips/import_wetravel.py https://dream-travel.wetravel.com/i/<itinerary id> --country <Country> --category "Art & Culture"
python _trips/build.py
```
- The itinerary id is printed by `trip_register.py`. The importer skips WeTravel's empty
  placeholder days, fills the summary, and keeps hand edits (category, summary, tags) on re-import.
- Scan for client names: `grep -il "<anything suspicious>" _trips/data/*.json`. A client trip gets
  `"status": "draft"` in its JSON and is **not committed**.
- **New country?** Add a Destination card to the homepage orbit in `/index.html` (copy an existing
  `orbit-card--dest` line; use the trip's hero photo path).
- Photos over 600 KB in `trips/images/<slug>/` can be shrunk with Pillow (WEBP quality 74).
- Preview: `preview_start adults-site` (port 8765), check `/trips/library-9mqqye8/art-culture/`,
  the new country page, and the homepage cards; no broken images.
- Publish: `git status` first. Commit only your paths (`_trips/data/<new>.json`,
  `trips/images/<new>/`, `trips/library-9mqqye8`, `trips/trips.json`, `index.html`), never another
  session's changes. Push over HTTPS (the SSH remote has no key on this PC):
  `git push https://github.com/Slybry2000/dream-travel.git main`. Check GitHub's latest commit
  first with `gh api repos/Slybry2000/dream-travel/commits/main --jq .sha` (the local
  `origin/main` is stale). Live in about a minute; confirm with curl.

### 8. Finish
- `trip_qa.py` on the whole list: everything OK except trips on hold.
- Set `"on_website": true` in `adult_trips.json` for trips now on the site.
- Tell Bryan in plain words: what is live (links), anything held back and why.

## Renaming existing trips
- Bookable trips (have a uuid): `trip_rename.py`. Then re-import them to the website
  (`import_wetravel.py <link>`), rebuild, and update the sheet's Name column.
- Standalone wellness itineraries (no uuid; the API cannot reach them): open
  `https://dream-travel.wetravel.com/i/editor/<itinerary id>` > **Settings** (top right) >
  **Itinerary name** > ctrl+a, type, Tab. It saves on its own; re-importing confirms it went live.

## Things that went wrong once (and the fix)
- Browser tools time out with a 0×0 window: the Chrome window is minimized. Ask Bryan to restore
  it, or open a fresh tab (`tabs_create_mcp`) in the visible window.
- Two Chrome profiles are connected; use the one signed in to Drive `/u/2` and WeTravel
  (its label "Browser 1/2" can swap between sessions).
- Filestack refuses to convert some originals (HTTP 400): the importer falls back to a plain resize.
- Smart Import reuses the same photo under different file names; only `trip_qa.py`'s look-based
  check catches it.
- WeTravel replaces the whole itinerary on every API edit: always back up and verify (the photo
  tool does both).
