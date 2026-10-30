"""Add a newly built ADULT trip to adult_trips.json, the allowlist the other tools rely on.

    python _trips/tools/trip_register.py <uuid> --country France --category "Art & Culture" --link https://tri.ps/xxxxx

Refuses student-looking and pickleball names. Run trip_rename.py first if the name is not yet
"Country: Theme". Standalone itineraries (no uuid) are added by hand to adult_trips.json.
"""
import argparse

from wetravel import call, get_trip, registry, save_registry, title_problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("uuid")
    ap.add_argument("--country", required=True)
    ap.add_argument("--category", required=True, help='"Art & Culture", "Wellness", ...')
    ap.add_argument("--link", required=True, help="the tri.ps short link from Manage Trip > Promote > Shorten URL")
    args = ap.parse_args()
    t = get_trip(args.uuid)
    if problems := title_problems(t["title"]):
        raise SystemExit(f"'{t['title']}' cannot be registered: " + "; ".join(problems))
    entries = registry()
    if any(e.get("uuid") == args.uuid for e in entries):
        raise SystemExit("Already registered.")
    it = call("GET", f"/trips/{args.uuid}/itinerary")
    entries.append({"title": t["title"], "kind": "trip", "uuid": args.uuid, "itinerary_id": it["id"],
                    "country": args.country, "category": args.category, "link": args.link, "on_website": False})
    entries.sort(key=lambda e: (e["category"], e["title"]))
    save_registry(entries)
    print(f"Registered {t['title']} (itinerary {it['id']}). Website import link: "
          f"https://dream-travel.wetravel.com/i/{it['id']}")


if __name__ == "__main__":
    main()
