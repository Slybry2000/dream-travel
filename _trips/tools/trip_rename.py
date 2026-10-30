"""Rename an ADULT WeTravel trip (bookable trips only) and keep the registry in step.

    python _trips/tools/trip_rename.py <uuid> "Country: Theme"

Refuses names that break the "Country: Theme" rule and trips not in adult_trips.json. Only the
title changes; the script checks that afterwards. Old links and tri.ps short links keep working.
Standalone wellness itineraries have no API: rename those in the WeTravel editor (see ADDING-TRIPS.md).
"""
import sys

from wetravel import adult_trip, call, get_trip, registry, save_registry, title_problems

# Fields WeTravel recomputes on any save; a change there is not caused by the rename.
DERIVED = {"title", "updated_at", "url", "checkout_url", "published_at", "editor", "next_departure_date", "overall_end_date"}


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    uuid, title = sys.argv[1], sys.argv[2].strip()
    adult_trip(uuid)
    if problems := title_problems(title):
        raise SystemExit("Name rejected: " + "; ".join(problems))
    before = get_trip(uuid)
    call("PATCH", f"/trips/{uuid}", {"title": title})
    after = get_trip(uuid)
    other = sorted(k for k in set(before) | set(after) if k not in DERIVED and before.get(k) != after.get(k))
    print(f"{before['title']}  ->  {after['title']}   (other fields changed: {other or 'none'})")
    entries = registry()
    for e in entries:
        if e.get("uuid") == uuid:
            e["title"] = after["title"]
    save_registry(entries)


if __name__ == "__main__":
    main()
