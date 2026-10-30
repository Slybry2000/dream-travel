"""Read-only quality check for adult WeTravel trips. Changes nothing.

    python _trips/tools/trip_qa.py                  # every bookable trip in adult_trips.json
    python _trips/tools/trip_qa.py 3976367699 ...   # specific trip uuids (new ones may be unregistered)

Checks: name follows "Country: Theme"; private, group 1-25, no dates; every real day has a photo;
no photo is used twice on the page (compared by how it looks, because WeTravel's smart import often
uploads the same photo twice under different names); no photo over 800 KB; possible client names
(an "ABOUT ..." section other than Dream Travel's own, or a year / "with First Last" in a heading);
the short link opens. Exit code 1 if anything needs fixing.
"""
import io
import re
import sys
import urllib.request

from PIL import Image

from wetravel import CDN, call, get_trip, registry, title_problems

OWN_SECTIONS = re.compile(r"about (dream[- ]?travel|the price)|insurance", re.I)
DAY = re.compile(r"day\s*\d+", re.I)


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60) as r:
        return r.read()


def look(handle):
    """Perceptual hash: near-identical photos give near-identical numbers."""
    im = Image.open(io.BytesIO(fetch(f"{CDN}/resize=width:64/{handle}"))).convert("L").resize((17, 16))
    px = im.tobytes()
    return sum(1 << i for i in range(256) if px[(i // 16) * 17 + i % 16] > px[(i // 16) * 17 + i % 16 + 1])


def size_kb(handle):
    import json
    return json.loads(fetch(f"{CDN}/{handle}/metadata?size=true")).get("size", 0) // 1024


def check(uuid, link=None):
    issues = []
    t = get_trip(uuid)
    issues += [f"name: {p}" for p in title_problems(t["title"])]
    if t.get("visibility") != "private":
        issues.append(f"visibility is {t.get('visibility')}, Rene's trips are private")
    if (t.get("min_people"), t.get("max_people")) != (1, 25):
        issues.append(f"group size is {t.get('min_people')}-{t.get('max_people')}, expected 1-25")
    if t.get("departures"):
        issues.append("has departure dates; sample trips use Dates Not Decided")

    secs = call("GET", f"/trips/{uuid}/itinerary").get("sections", [])
    photos = []
    for s in secs:
        title = (s.get("title") or "").strip()
        handle = (s.get("image") or {}).get("handle")
        has_content = bool(s.get("items"))
        if DAY.match(title) and has_content and not handle:
            issues.append(f"no photo: {title}")
        if title.lower().startswith("about ") and not OWN_SECTIONS.search(title):
            issues.append(f"possible client name, check before publishing: section '{title}'")
        if re.search(r"\b20\d\d\b", title) or re.search(r"\bwith [A-Z][a-z]+ [A-Z][a-z]+", title):
            issues.append(f"possible client name or date in heading: '{title}'")
        if handle:
            photos.append((title, handle))

    hashes = [(title, handle, look(handle)) for title, handle in photos]
    for i in range(len(hashes)):
        for j in range(i + 1, len(hashes)):
            if bin(hashes[i][2] ^ hashes[j][2]).count("1") <= 12:
                issues.append(f"same photo twice: '{hashes[i][0]}' and '{hashes[j][0]}'")
    big = [(title, kb) for title, handle in photos if (kb := size_kb(handle)) > 800]
    if big:
        issues.append(f"{len(big)} photos over 800 KB (slow pages); run trip_photos.py {uuid} --optimize --warm")

    if link:
        try:
            fetch(link)
        except Exception as e:
            issues.append(f"link {link} does not open: {e}")
    return t["title"], len(photos), issues


def main():
    targets = sys.argv[1:] or [e["uuid"] for e in registry() if e.get("uuid")]
    links = {e["uuid"]: e.get("link") for e in registry() if e.get("uuid")}
    bad = 0
    for uuid in targets:
        title, n, issues = check(uuid, links.get(uuid))
        bad += bool(issues)
        print(f"{'OK  ' if not issues else 'FIX '} {title}  ({uuid}, {n} photos)")
        for i in issues:
            print(f"       - {i}")
    print(f"\n{len(targets) - bad} of {len(targets)} trips pass.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
