"""Shared helpers for the WeTravel Partner API (v3) and the adult-trip registry.

The API key lives in Dream-Travel/.env as WETRAVEL_API_KEY (Rene's Partner API key, a refresh
token). It is never printed. Access tokens last 1 hour; one is fetched per run.

The registry (_trips/adult_trips.json) is the allowlist of ADULT trips. Every tool that changes
anything in WeTravel refuses a trip that is not in it, so student and pickleball trips can never
be touched by accident.
"""
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

TRIPS_DIR = Path(__file__).resolve().parent.parent          # _trips/
REPO = TRIPS_DIR.parent                                      # Dream-Travel/
REGISTRY = TRIPS_DIR / "adult_trips.json"
BACKUPS = REPO / ".tmp" / "wetravel_backups"
API = "https://api.wetravel.com/v3"
CDN = "https://cdn.filestackcontent.com"
_token = None


def _env():
    env = {}
    for line in (REPO / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    if not env.get("WETRAVEL_API_KEY"):
        raise SystemExit("WETRAVEL_API_KEY is missing from Dream-Travel/.env")
    return env


def _request(method, url, token, data=None):
    req = urllib.request.Request(url, method=method, data=data, headers={
        "Authorization": "Bearer " + token, "Accept": "application/json",
        "Content-Type": "application/json", "User-Agent": "DreamTravel/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method} {url} -> {e.code}: {e.read().decode('utf-8', 'replace')[:600]}")


def call(method, path, body=None):
    """Call the Partner API, e.g. call("GET", "/trips/123/itinerary")."""
    global _token
    if _token is None:
        _token = _request("POST", API + "/auth/tokens/access", _env()["WETRAVEL_API_KEY"], b"")["access_token"]
    data = json.dumps(body).encode() if body is not None else None
    out = _request(method, API + path, _token, data)
    return out.get("data", out) if isinstance(out, dict) and set(out) == {"data"} else out


def get_trip(uuid):
    t = call("GET", f"/trips/{uuid}")
    return t.get("data", t)


def all_trips():
    trips, page = [], 1
    while True:
        r = call("GET", f"/trips?per_page=50&page={page}")
        trips += r["data"]
        if not r["pagination"]["has_next"]:
            return trips
        page += 1


def upload_by_url(url):
    """Have WeTravel fetch an image from a public URL; returns {"provider": "filestack", "handle": ...}."""
    job = call("POST", "/images/by_url", {"url": url})
    for _ in range(40):
        if job.get("status") == "completed":
            return job["image"]
        if job.get("status") == "failed":
            raise RuntimeError("image upload failed: " + str(job.get("error")))
        time.sleep(3)
        job = call("GET", f"/images/jobs/{job['job_id']}")
    raise RuntimeError("image upload timed out")


def backup_itinerary(uuid, itinerary):
    BACKUPS.mkdir(parents=True, exist_ok=True)
    path = BACKUPS / f"{uuid}-{time.strftime('%Y%m%d-%H%M%S')}.json"
    path.write_text(json.dumps(itinerary, ensure_ascii=False, indent=1), encoding="utf-8")
    return path


# --- naming ---------------------------------------------------------------------------------

STUDENT_MARKERS = re.compile(r"\b(HS|high school|exchange|students?|school|academy|homestay)\b", re.I)


def title_problems(title):
    """Why a title breaks the adult naming rule "Country: Theme" (empty list = fine)."""
    problems = []
    if not re.match(r"^[A-Z][^:]{1,40}: \S", title):
        problems.append('should be "Country: Theme" (country, colon, space, theme)')
    if re.search(r"\d+[\s-]*(day|night)", title, re.I):
        problems.append("no day/night counts (the website shows the length)")
    if re.search(r"\bitinerary\b|\bwetravel\b", title, re.I):
        problems.append('no "Itinerary" or "WeTravel" in the name')
    if re.match(r"^[A-Za-z]{2,5}\d+\s*-", title):
        problems.append("no internal codes like CRW1 -")
    if re.search(r"\b20\d\d\b", title):
        problems.append("no years in the name")
    if title.lower().startswith("pickleball"):
        problems.append("pickleball trips are a separate brand; never treat them as adult trips here")
    if STUDENT_MARKERS.search(title):
        problems.append("looks like a student trip; never touch student trips")
    return problems


# --- registry -------------------------------------------------------------------------------

def registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def save_registry(entries):
    REGISTRY.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def adult_trip(uuid):
    """The registry entry for a bookable adult trip, or exit. This is the safety gate."""
    entry = next((e for e in registry() if e.get("uuid") == uuid), None)
    if not entry:
        raise SystemExit(f"Refusing: trip {uuid} is not in _trips/adult_trips.json. "
                         "Only registered ADULT trips may be changed (never student or pickleball trips).")
    return entry
