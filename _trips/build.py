"""Build the Dream Travel trips library from _trips/data/*.json.

    python _trips/build.py

Every destination page is rebuilt from whatever trips are tagged with that country, so a
new trip shows up everywhere by itself.

Trips built in WeTravel link straight to their WeTravel itinerary: Rene edits there and
the change is live at once, with no second copy to go stale. Only a trip with no WeTravel
"source" (written by hand), or one marked "host_copy": true, gets its own page here.

The library overview and its country pages are PUBLIC: the homepage orbit links to them
and search engines may index them. Hand-made trip pages stay link-only (noindex, random key).
Output (generated, safe to delete and rebuild):

    trips/<trip>-<key>/index.html                   hand-made trips only (share this link)
    trips/<library key>/index.html                  every trip (public, linked from the homepage)
    trips/<library key>/<country>/index.html        one destination's trips as cards
    trips/trips.json                                feed for embed.js, "listed": true trips only

Only trips with "status": "published" are built. Set "draft" to take one offline.
A trip's key lives in its JSON; change it to kill an old link.
Destination intros and hero photos can be set in _trips/destinations.json.

Source lives in _trips/ because GitHub Pages (Jekyll) never publishes folders that
start with an underscore, so the data files cannot leak the private links.
"""
import html
import json
import re
import secrets
import shutil
from datetime import datetime
from pathlib import Path

SRC = Path(__file__).resolve().parent            # _trips/: data + config, never published
OUT = SRC.parent / "trips"                         # trips/: the pages GitHub Pages serves
SITE = "https://adults.dream-travel.net"
BASE = "/trips"
VERSION = datetime.now().strftime("%Y%m%d%H%M")
esc = html.escape


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def safe(fragment):
    """Imported itinerary HTML is Rene's own copy, but strip anything executable."""
    fragment = re.sub(r"<(script|style|iframe)\b.*?</\1>", "", fragment or "", flags=re.S | re.I)
    return re.sub(r"\s+on\w+=(\"[^\"]*\"|'[^']*')", "", fragment)


def img_url(ref):
    return f"{BASE}/{ref['src']}" if ref else ""


def focal(ref):
    return f"object-position:{ref.get('x', 50)}% {ref.get('y', 50)}%" if ref else ""


def new_key():
    return "".join(secrets.choice("abcdefghjkmnpqrstuvwxyz23456789") for _ in range(7))


def config():
    cfg_path = SRC / "config.json"
    return json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.exists() else {}


def library_key():
    """The address of the all-trips listing, created once and kept."""
    cfg_path = SRC / "config.json"
    cfg = config()
    if not cfg.get("library_key"):
        cfg["library_key"] = "library-" + new_key()
        cfg_path.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    return cfg["library_key"]


def load():
    trips = []
    for p in sorted((SRC / "data").glob("*.json")):
        t = json.loads(p.read_text(encoding="utf-8"))
        if not t.get("key"):              # first build: give the trip its private link
            t["key"] = new_key()
            p.write_text(json.dumps(t, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if t.get("status", "published") != "published":
            continue
        t["country_slug"] = slugify(t.get("country") or "elsewhere")
        t["hosted"] = t.get("host_copy") or not t.get("source")
        t["url"] = f"{BASE}/{t['slug']}-{t['key']}/" if t["hosted"] else t["source"]
        trips.append(t)
    trips.sort(key=lambda t: (t.get("sort", 100), t["title"]))
    extra = SRC / "destinations.json"
    dests = json.loads(extra.read_text(encoding="utf-8")) if extra.exists() else {}
    return trips, dests


def duration(t):
    return f"{t['days']} Days" if t.get("days") else "Custom length"


def overnights_line(t):
    return ", ".join(f"{o['place'].split(',')[0]} ({o['nights']})" for o in t.get("overnights", []))


# --- shared chrome -----------------------------------------------------------------

def head(title, description, image="", extra="", public=False):
    robots = "index, follow" if public else "noindex, nofollow, noarchive"
    og = f'<meta property="og:image" content="{SITE}{esc(image)}">' if image else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="{robots}">
  <meta name="referrer" content="strict-origin">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  {og}
  <link rel="icon" href="/images/logo-header.webp">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{BASE}/trips.css?v={VERSION}">
  {extra}
</head>"""


def site_header():
    return f"""  <header class="tl-header">
    <a class="tl-brand" href="/" aria-label="Dream Travel home"><img src="/images/logo-header-2x.webp" alt="" width="75" height="64"><span>Dream Travel</span></a>
    <nav class="tl-header__nav" aria-label="Primary"><a href="{BASE}/{library_key()}/">Sample trips</a><a href="/#hosting">Hosting</a><a href="/#plan">Contact</a></nav>
    <a class="tl-button tl-button--small" href="/planning/">Plan a trip</a>
  </header>"""


def site_footer():
    return """  <footer class="tl-footer">
    <div><a class="tl-brand" href="/"><img src="/images/logo-footer-2x.webp" alt="" width="56" height="48"><span>Dream Travel</span></a><p>Hosted. Private. Custom.</p></div>
    <div class="tl-footer__contact"><a href="mailto:go@dream-travel.net">go@dream-travel.net</a><a href="tel:+15712068949">571 206 8949</a></div>
    <p class="tl-footer__small">&copy; 2026 Dream Travel International Corp. Sample programs. Final details are confirmed with your group.</p>
  </footer>"""


def card(t):
    tags = "".join(f"<span>{esc(x)}</span>" for x in t.get("tags", []))
    nights = overnights_line(t)
    return f"""      <article class="tl-card">
        <a class="tl-card__media" href="{t['url']}"><img src="{img_url(t.get('hero'))}" alt="" loading="lazy" style="{focal(t.get('hero'))}"><span class="tl-card__badge">{esc(duration(t))}</span></a>
        <div class="tl-card__body">
          <h3><a href="{t['url']}">{esc(t['title'])}</a></h3>
          <p class="tl-card__meta"><b>Location(s):</b> {esc(', '.join(t.get('locations', [])[:4]) or t.get('country', ''))}</p>
          {f'<p class="tl-card__tags">{tags}</p>' if tags else ''}
          {f'<p class="tl-card__meta"><b>Overnights:</b> {esc(nights)}</p>' if nights else ''}
          <a class="tl-button tl-button--line" href="{t['url']}">See itinerary</a>
        </div>
      </article>"""


# --- itinerary page ------------------------------------------------------------------

def itinerary(t):
    secs = t["sections"]
    nav = [("overview", "Overview")] + ([("map", "Map")] if t.get("pins") else []) + \
          [(s["id"], s["title"]) for s in secs] + [("about", "About Dream Travel")]
    nav_html = "".join(f'<a href="#{i}">{esc(label)}</a>' for i, label in nav)
    toc = "".join(f'<li><a href="#{i}">{esc(label)}</a></li>' for i, label in nav[1:])

    facts = [("Length", f"{t['days']} days, {t['nights']} nights" if t.get("days") else "Custom"),
             ("Destination", t.get("country", "")),
             ("Places", ", ".join(t.get("locations", []))),
             ("Overnights", overnights_line(t)),
             ("Group size", "From eight travelers")]
    facts_html = "".join(f"<div><dt>{k}</dt><dd>{esc(v)}</dd></div>" for k, v in facts if v)

    def panel(sid, title, image, body, dark_title=True):
        return f"""    <section class="tl-row" id="{sid}">
      <div class="tl-row__media">{f'<img src="{img_url(image)}" alt="" loading="lazy" style="{focal(image)}">' if image else ''}<h2>{esc(title)}</h2></div>
      <div class="tl-row__text">{body}</div>
    </section>"""

    rows = []
    for s in secs:
        gallery = "".join(
            f'<figure><img src="{img_url(g)}" alt="{esc(g.get("caption", ""))}" loading="lazy">'
            f'{f"<figcaption>{esc(g["caption"])}</figcaption>" if g.get("caption") else ""}</figure>'
            for g in s.get("gallery", []))
        body = (f'<p class="tl-kicker">{esc(s["subtitle"])}</p>' if s.get("subtitle") else "") + \
               f'<div class="tl-prose">{safe(s["html"])}</div>' + \
               (f'<div class="tl-gallery">{gallery}</div>' if gallery else "")
        rows.append(panel(s["id"], s["title"], s.get("image"), body))

    pins = t.get("pins", [])
    map_row = ""
    if pins:
        items = "".join(f'<li><b>{chr(65 + i)}.</b> {esc(p["name"])}<small>{esc(p["address"])}</small></li>'
                        for i, p in enumerate(pins))
        map_row = f"""    <section class="tl-row" id="map">
      <div class="tl-row__media tl-row__media--map"><div class="tl-map" data-pins='{esc(json.dumps(pins))}'></div></div>
      <div class="tl-row__text"><p class="tl-kicker">Map</p><ol class="tl-pins">{items}</ol></div>
    </section>"""

    about = f"""    <section class="tl-row tl-row--about" id="about">
      <div class="tl-row__media"><img src="/images/hero-background-r2-1280w.webp" alt="" loading="lazy"><h2>About Dream Travel</h2></div>
      <div class="tl-row__text">
        <p class="tl-kicker">Why travel with us</p>
        <div class="tl-prose">
          <p>Dream Travel builds private journeys for groups that already know each other: clubs, congregations, alumni circles, studios and friends. René Piard founded the company to make travel personal, with an <em>à la carte</em> approach that shapes each trip around the people going.</p>
          <p>Every program here is a starting point. Dates, pace, hotels and activities are adjusted with your group before anything is confirmed.</p>
          <p><strong>René Piard</strong>, Founder &amp; Chief Travel Officer<br><a href="mailto:go@dream-travel.net">go@dream-travel.net</a> &middot; <a href="tel:+15712068949">571 206 8949</a></p>
        </div>
        <div class="tl-cta"><a class="tl-button" href="/planning/">Plan this trip for your group</a></div>
      </div>
    </section>"""

    hero = t.get("hero")
    leaflet = ('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">'
               '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js" defer></script>') if pins else ""
    return f"""{head(f"{t['title']} | Dream Travel", t.get('summary') or t.get('tagline', ''), img_url(hero), leaflet)}
<body class="tl-itinerary">
  <header class="tl-bar">
    <a class="tl-bar__logo" href="/" aria-label="Dream Travel home"><img src="/images/logo-header-2x.webp" alt="" width="75" height="64"></a>
    <nav class="tl-bar__nav" aria-label="Itinerary sections"><a href="#top" class="tl-bar__title">{esc(t['title'])}</a>{nav_html}</nav>
    <div class="tl-bar__actions">
      <button type="button" class="tl-icon" onclick="window.print()" aria-label="Print or save as PDF" title="Print or save as PDF"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9V3h12v6M6 18H4a1 1 0 0 1-1-1v-6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6a1 1 0 0 1-1 1h-2M6 14h12v7H6z"/></svg></button>
      <a class="tl-button tl-button--small" href="/planning/">Plan this trip</a>
    </div>
  </header>
  <main id="top">
    <section class="tl-row tl-row--hero">
      <div class="tl-row__media"><img src="{img_url(hero)}" alt="" style="{focal(hero)}"><h1>{esc(t['title'])}</h1></div>
      <div class="tl-row__text" id="overview">
        <p class="tl-crumbs">{esc(t.get('country', ''))}</p>
        <p class="tl-kicker">Overview</p>
        <p class="tl-lede">{esc(t.get('summary', ''))}</p>
        <dl class="tl-facts">{facts_html}</dl>
        <ol class="tl-toc">{toc}</ol>
      </div>
    </section>
{map_row}
{chr(10).join(rows)}
{about}
  </main>
{site_footer()}
  <script src="{BASE}/trips.js?v={VERSION}" defer></script>
</body>
</html>
"""


# --- listing pages -------------------------------------------------------------------

def destination(slug, name, trips, meta, lib, by_country):
    hero = meta.get("hero") or img_url(trips[0].get("hero"))
    intro = meta.get("intro") or [
        f"Sample programs for private groups traveling to {name}. Each one is a starting point: "
        "we shape the dates, pace, hotels and activities around your group before anything is confirmed.",
        "Programs can also be combined with other countries."]
    intro_html = "".join(f"<p>{esc(p)}</p>" for p in intro)
    cards = "\n".join(card(t) for t in trips)
    others = "".join(f'<a href="{lib}/{s}/">{esc(n)}</a>' for s, (n, _) in by_country.items() if s != slug)
    return f"""{head(f"{name} Group Trips | Dream Travel", intro[0], hero, public=True)}
<body>
{site_header()}
  <main>
    <section class="tl-hero"><img src="{hero}" alt=""><a class="tl-back" href="{lib}/">&larr; All sample trips</a><div><p class="tl-kicker">Group travel destinations</p><h1>{esc(name)}</h1><a class="tl-button" href="#trips">See trips</a></div></section>
    <section class="tl-intro"><h2>Explore our {esc(name)} programs</h2>{intro_html}<p><strong>Let's build your group's trip together.</strong></p></section>
    <section class="tl-grid-wrap" id="trips"><div class="tl-grid">
{cards}
    </div></section>
    <nav class="tl-more" aria-label="More sample trips"><a class="tl-button tl-button--line" href="{lib}/">&larr; See all sample trips</a><p>Or browse another destination:</p><div>{others}</div></nav>
    <section class="tl-closing"><h2>Ready to plan your group's trip?</h2><p>Tell us who is going and what they love. René shapes the rest.</p><a class="tl-button" href="/planning/">Plan a trip</a></section>
  </main>
{site_footer()}
</body>
</html>
"""


def library(by_country, dests, lib):
    blocks = []
    for slug, (name, trips) in by_country.items():
        cards = "\n".join(card(t) for t in trips)
        blocks.append(f"""    <section class="tl-grid-wrap"><div class="tl-grid-head"><h2><a href="{lib}/{slug}/">{esc(name)}</a></h2><a href="{lib}/{slug}/">{len(trips)} trip{'s' if len(trips) != 1 else ''}</a></div><div class="tl-grid">
{cards}
    </div></section>""")
    # Hero slideshow: "hero_rotation" in config.json (paths under trips/), else every trip's cover photo.
    slides = [f"{BASE}/{src}" for src in config().get("hero_rotation", [])]
    if not slides:
        slides = [img_url(t.get("hero")) for _, ts in by_country.values() for t in ts if t.get("hero")]
    slides = list(dict.fromkeys(slides)) or ["/images/hero-background-r2-1920w.webp"]
    hero = slides[0]
    first_attr, rest_attr = ' class="is-active"', ' loading="lazy"'
    hero_imgs = "".join(f'<img src="{esc(src)}" alt=""{first_attr if i == 0 else rest_attr} data-hero-slide>'
                        for i, src in enumerate(slides))
    return f"""{head("Group Trips | Dream Travel", "Sample itineraries for private group travel with Dream Travel.", hero, public=True)}
<body>
{site_header()}
  <main>
    <section class="tl-hero tl-hero--slides">{hero_imgs}<div><p class="tl-kicker">Sample itineraries</p><h1>Where will your group go?</h1><a class="tl-button" href="#all">See trips</a></div></section>
    <section class="tl-intro" id="all"><h2>These are just samples. We can do much more.</h2><p>Any destination, any type of trip. Pick one close to what your people want and we will shape it from there, or tell us where you want to go and we will build it.</p><p><a class="tl-button" href="/planning/">Tell us what you have in mind</a></p></section>
{chr(10).join(blocks)}
    <section class="tl-closing"><h2>Don't see your trip?</h2><p>Most of what we run is built from scratch.</p><a class="tl-button" href="/planning/">Plan a custom trip</a></section>
  </main>
{site_footer()}
  <script src="{BASE}/trips.js?v={VERSION}" defer></script>
</body>
</html>
"""


def main():
    trips, dests = load()
    lib_dir = OUT / library_key()
    lib = f"{BASE}/{lib_dir.name}"
    # Wipe previously generated pages so a removed, drafted or re-keyed trip disappears too.
    for d in OUT.iterdir():
        if d.is_dir() and (d / "index.html").exists() and d.name != "images":
            shutil.rmtree(d)
    (OUT / "index.html").unlink(missing_ok=True)   # there is deliberately no public /trips/ page

    by_country = {}
    for t in trips:
        by_country.setdefault(t["country_slug"], (t.get("country") or "Elsewhere", []))[1].append(t)
        if t["hosted"]:
            out = OUT / f"{t['slug']}-{t['key']}" / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(itinerary(t), encoding="utf-8")

    for slug, (name, group) in by_country.items():
        (lib_dir / slug).mkdir(parents=True, exist_ok=True)
        (lib_dir / slug / "index.html").write_text(destination(slug, name, group, dests.get(slug, {}), lib, by_country), encoding="utf-8")
    (lib_dir / "index.html").write_text(library(by_country, dests, lib), encoding="utf-8")

    feed = [{"title": t["title"], "url": SITE + t["url"] if t["hosted"] else t["url"], "country": t.get("country"), "country_slug": t["country_slug"],
             "days": t.get("days"), "duration": duration(t), "image": SITE + img_url(t.get("hero")),
             "locations": t.get("locations", []), "tags": t.get("tags", []), "overnights": overnights_line(t),
             "summary": t.get("summary", "")} for t in trips if t.get("listed")]
    (OUT / "trips.json").write_text(json.dumps({"updated": VERSION, "trips": feed}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Built {len(trips)} trip(s). Links:")
    for t in trips:
        print(f"  {t['title']}: {SITE + t['url'] if t['hosted'] else t['url'] + '  (WeTravel)'}")
    print(f"  All trips (public): {SITE}{lib}/")


if __name__ == "__main__":
    main()
