"""Fix photos on an ADULT WeTravel trip. Only section photos change; everything else is verified untouched.

    python _trips/tools/trip_photos.py <uuid> --set "Day 5 -=1634847403522-8a165b37f35f"
    python _trips/tools/trip_photos.py <uuid> --optimize --warm
    python _trips/tools/trip_photos.py <uuid> --set "Journey Highlights=<id>" --optimize --warm

--set "<section title prefix>=<Unsplash photo id>"  put that Unsplash photo on the section (repeatable).
    The id is the part after "photo-" in an images.unsplash.com address. Find photos with the
    browser snippet in _trips/ADDING-TRIPS.md (Unsplash blocks scripts).
--optimize  swap every photo for a page-ready copy (max 1600 px wide JPEG). Smart import brings in
    1-10 MB originals; this makes pages download about 30% less and first loads much faster.
--warm      open every photo the way the WeTravel page does, so the first real visitor gets cached copies.

A backup of the itinerary is saved to .tmp/wetravel_backups/ before any change. WeTravel replaces
the whole itinerary on every edit, so the script checks afterwards that only photos changed.
"""
import argparse
import copy
from concurrent.futures import ThreadPoolExecutor

from wetravel import CDN, adult_trip, backup_itinerary, call, upload_by_url

SMALL = CDN + "/rotate=deg:exif/resize=fit:max,width:1600/output=format:jpg,quality:70/compress/{}"
UNSPLASH = "https://images.unsplash.com/photo-{}?w=1600&q=70&fm=jpg"
PAGE = CDN + "/rotate=deg:exif/resize=fit:max,width:1920/quality=v:75/compress/cache=expiry:2628000/fallback=file:{0},cache:2628000/{0}"


def without_images(sections):
    s = copy.deepcopy(sections)
    for x in s:
        x.pop("image", None)
    return s


def warm(handles):
    import urllib.request

    def get(h):
        try:
            urllib.request.urlopen(urllib.request.Request(PAGE.format(h), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read()
            return True
        except Exception:
            return False
    with ThreadPoolExecutor(8) as pool:
        ok = sum(pool.map(get, handles))
    print(f"  pre-loaded {ok}/{len(handles)} photos")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("uuid")
    ap.add_argument("--set", action="append", default=[], metavar="PREFIX=UNSPLASH_ID")
    ap.add_argument("--optimize", action="store_true")
    ap.add_argument("--warm", action="store_true")
    args = ap.parse_args()
    entry = adult_trip(args.uuid)                       # refuses anything that is not a registered adult trip

    before = call("GET", f"/trips/{args.uuid}/itinerary")
    secs = copy.deepcopy(before["sections"])
    sources = {}                                        # section index -> URL WeTravel should fetch
    for spec in args.set:
        prefix, _, photo = spec.partition("=")
        idx = [i for i, s in enumerate(secs) if (s.get("title") or "").startswith(prefix.strip())]
        if len(idx) != 1:
            raise SystemExit(f"'{prefix}' matches {len(idx)} sections; use a longer, unique start of the title")
        sources[idx[0]] = UNSPLASH.format(photo.strip())
    if args.optimize:
        for i, s in enumerate(secs):
            h = (s.get("image") or {}).get("handle")
            if h and i not in sources:
                sources[i] = SMALL.format(h)

    if sources:
        print(f"{entry['title']}: backup saved to {backup_itinerary(args.uuid, before)}")
        with ThreadPoolExecutor(6) as pool:
            images = dict(zip(sources, pool.map(upload_by_url, sources.values())))
        for i, img in images.items():
            secs[i]["image"] = {**(secs[i].get("image") or {}), **img}
        call("PATCH", f"/trips/{args.uuid}/itinerary", {"sections": secs})
        after = call("GET", f"/trips/{args.uuid}/itinerary")
        rest_ok = without_images(after["sections"]) == without_images(before["sections"])
        set_ok = all((after["sections"][i].get("image") or {}).get("handle") == img["handle"] for i, img in images.items())
        print(f"  {len(images)} photos changed ({len(args.set)} new); only photos changed: {rest_ok}; all set: {set_ok}")
        if not (rest_ok and set_ok):
            raise SystemExit("  SOMETHING ELSE CHANGED. Restore from the backup above and investigate.")
        before = after
    if args.warm:
        warm([s["image"]["handle"] for s in before["sections"] if (s.get("image") or {}).get("handle")])


if __name__ == "__main__":
    main()
