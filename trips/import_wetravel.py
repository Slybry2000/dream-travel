"""Import a WeTravel itinerary link into the Dream Travel trips library.

    python trips/import_wetravel.py https://dream-travel.wetravel.com/i/<id> [--country "Costa Rica"]

WeTravel server-renders the whole itinerary into the page as Next.js flight data, so
one plain GET is enough: no login, no browser. This writes:

    trips/data/<slug>.json        the trip, in our own format
    trips/images/<slug>/*.webp    every photo, copied locally so we never depend on WeTravel

Re-importing the same link refreshes the itinerary but keeps any hand-edited fields
listed in KEEP (tags, country, status...). Run trips/build.py afterwards.
"""
import argparse
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
IMAGES = ROOT / "images"
UA = {"User-Agent": "Mozilla/5.0 (Dream Travel trip importer)"}
# Fields a person may edit by hand; a re-import never overwrites them.
KEEP = ("slug", "country", "tags", "status", "summary", "sort", "hero_position", "overnights")
SKIP_SECTIONS = ("about dream-travel", "about dream travel", "about us")


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def flight_data(html):
    """Join the self.__next_f.push chunks back into one flight payload (as bytes)."""
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)</script>', html, re.S)
    return "".join(json.loads('"' + c + '"') for c in chunks).encode("utf-8")


def text_rows(payload):
    """Flight 'T' rows hold long strings: <id>:T<hex byte length>,<bytes>.

    A T row has no trailing newline, so the next row can start right after its last
    byte. Walk the payload row by row instead of searching for newlines."""
    rows, pos, head = {}, 0, re.compile(rb"([0-9a-f]+):(T([0-9a-f]+),)?")
    while pos < len(payload):
        m = head.match(payload, pos)
        if m and m.group(2):
            start, size = m.end(), int(m.group(3), 16)
            rows["$" + m.group(1).decode()] = payload[start:start + size].decode("utf-8", "replace")
            pos = start + size
            continue
        nl = payload.find(b"\n", pos)
        pos = len(payload) if nl < 0 else nl + 1
    return rows


def resolve(value, rows):
    if isinstance(value, str) and value in rows:
        return rows[value]
    if isinstance(value, list):
        return [resolve(v, rows) for v in value]
    if isinstance(value, dict):
        return {k: resolve(v, rows) for k, v in value.items()}
    return value


def extract_itinerary(page):
    payload = flight_data(page)
    text = payload.decode("utf-8", "replace")
    at = text.find('{"itinerary":')
    if at < 0:
        sys.exit("No itinerary data found. Is the link a public WeTravel itinerary (/i/...)?")
    obj, _ = json.JSONDecoder().raw_decode(text, at)
    return resolve(obj["itinerary"], text_rows(payload))


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def image_ref(img, slug):
    """Copy one Filestack image locally; return its site path and focal point."""
    if not img or img.get("provider") != "filestack" or not img.get("handle"):
        return None
    handle = img["handle"]
    out = IMAGES / slug / f"{handle}.webp"
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://cdn.filestackcontent.com/rotate=deg:exif/resize=fit:max,width:1800/output=format:webp/quality=v:78/{handle}"
        out.write_bytes(fetch(url))
    pos = (img.get("metadata") or {}).get("position") or {"x": 50, "y": 50}
    return {"src": f"images/{slug}/{handle}.webp", "x": pos.get("x", 50), "y": pos.get("y", 50)}


def clean_html(h):
    h = (h or "").replace(" ", " ")
    h = re.sub(r"<p>\s*</p>", "", h)
    return h.strip()


def overnights(sections):
    """Count 'Overnight at X' lines, e.g. {'Arenal Lodge, Arenal Volcano Area': 5}."""
    counts = {}
    for s in sections:
        m = re.search(r"Overnight (?:at|in) ([^<.]+)", s.get("html", ""))
        if m:
            place = m.group(1).strip()
            counts[place] = counts.get(place, 0) + 1
    return [{"place": p, "nights": n} for p, n in counts.items()]


def convert(it, url, country_arg):
    raw_title = it["title"]
    code, _, name = raw_title.partition(" - ")
    if not name or len(code) > 8:
        code, name = "", raw_title
    slug = slugify(name)

    trip = {"slug": slug, "title": name.strip(), "code": code.strip(), "source": url,
            "updated_at": it.get("updated_at"), "status": "published"}
    sections, pins = [], []
    for sec in it.get("sections", []):
        kind, title = sec.get("type"), (sec.get("title") or "").strip()
        if sec.get("hidden_from_traveler") or title.lower() in SKIP_SECTIONS:
            continue
        if kind == "map":
            pins = [{"name": p["title"], "address": p["location"]["address"],
                     "lat": p["location"]["lat"], "lng": p["location"]["long"]} for p in sec.get("pins", [])]
            continue
        if kind != "general":
            continue
        body, gallery = [], []
        for item in sec.get("items", []):
            if item.get("hidden_from_traveler"):
                continue
            if item.get("title"):
                body.append(f"<h4>{item['title']}</h4>")
            body.append(clean_html(item.get("description")))
            for g in item.get("images", []):
                ref = image_ref(g.get("image", g) if isinstance(g, dict) else None, slug)
                if ref:
                    ref["caption"] = (g.get("caption") or g.get("description") or "").strip() if isinstance(g, dict) else ""
                    gallery.append(ref)
        sections.append({"id": slugify(title) or sec["id"][:8], "title": title,
                         "subtitle": (sec.get("subtitle") or "").strip(),
                         "image": image_ref(sec.get("image"), slug),
                         "html": "\n".join(b for b in body if b), "gallery": gallery})

    if sections and not sections[0]["html"]:
        cover = sections.pop(0)          # the title card: its photo becomes the hero
        trip["hero"] = cover["image"]
    else:
        trip["hero"] = sections[0]["image"] if sections else None

    days = [s for s in sections if re.match(r"day\s*\d+", s["title"], re.I)]
    trip["days"] = len(days)
    trip["nights"] = max(len(days) - 1, 0)
    trip["country"] = country_arg or (pins[0]["address"].split(",")[-1].strip() if pins else "")
    trip["locations"] = [p["name"] for p in pins]
    trip["tags"] = []
    first_text = next((s for s in sections if s["html"] and not re.match(r"day\s*\d+", s["title"], re.I)), None)
    trip["tagline"] = first_text["title"] if first_text else ""
    # Summary = first real paragraph of the intro (the intro often repeats the title first).
    paras = re.findall(r"<p>(.*?)</p>", first_text["html"], re.S) if first_text else []
    paras = [html.unescape(re.sub(r"<[^>]+>", "", p)).strip() for p in paras]
    trip["summary"] = next((p for p in paras if len(p) > 80), "")
    trip["pins"] = pins
    trip["sections"] = sections
    trip["overnights"] = overnights(days)
    return trip


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--country", help="override the country read from the map pins")
    args = ap.parse_args()

    url = args.url.split("#")[0]
    page = fetch(url).decode("utf-8", "replace")
    trip = convert(extract_itinerary(page), url, args.country)

    DATA.mkdir(exist_ok=True)
    # Match an earlier import of the same link, even if its slug was edited by hand.
    existing = next((p for p in DATA.glob("*.json")
                     if json.loads(p.read_text(encoding="utf-8")).get("source") == url), None)
    if existing:
        old = json.loads(existing.read_text(encoding="utf-8"))
        for k in KEEP:
            if old.get(k):
                trip[k] = old[k]
    out = existing or DATA / f"{trip['slug']}.json"
    out.write_text(json.dumps(trip, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{'Updated' if existing else 'Imported'} {trip['title']} ({trip['country']}, {trip['days']} days, "
          f"{len(trip['sections'])} sections) -> {out.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
