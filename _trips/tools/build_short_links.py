"""Build the short-link redirect pages: adults.dream-travel.net/g/<code>/ -> the real sample-trip page.

Why: emails and texts carry a tracked link per person (?t=<16-hex visitor code>&s=email). The real trip pages live
at /trips/library-9mqqye8/wellness/costa-rica/, which makes a long, ugly link. /g/w-costa-rica/ is the same page.
The redirect keeps the whole query string, so journey-path.js still sees the visitor code and the source.

Run from the repo root:  python _trips/tools/build_short_links.py
Writes g/<code>/index.html for every trip page and g/map.json ({real path: code}). Re-run whenever trips are added,
then publish the g/ folder. The Command Center's shortlinks.js reads a copy of map.json.
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LIB = "trips/library-9mqqye8"
PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dream Travel</title><meta name="robots" content="noindex, nofollow"><meta name="referrer" content="strict-origin">
<meta http-equiv="refresh" content="1;url={dest}">
<script>location.replace({dest_js} + location.search + location.hash);</script></head>
<body><p><a href="{dest}">Continue to Dream Travel</a></p></body></html>
"""


def code_for(rel):
    parts = [p for p in rel.split("/") if p]
    if not parts:
        return "trips"
    if parts[0] == "wellness":
        return "wellness" if len(parts) == 1 else "w-" + parts[1]
    if parts[0] == "art-culture":
        return "art" if len(parts) == 1 else "a-" + parts[1]
    return parts[0]


def main():
    lib = os.path.join(ROOT, LIB)
    if not os.path.isdir(lib):
        sys.exit("Cannot find " + lib)
    mapping, seen = {}, {}
    for dirpath, _, files in os.walk(lib):
        if "index.html" not in files:
            continue
        rel = os.path.relpath(dirpath, lib).replace("\\", "/")
        rel = "" if rel == "." else rel
        code = code_for(rel)
        if code in seen:
            sys.exit("Two pages want the short code %r: %r and %r" % (code, seen[code], rel))
        seen[code] = rel
        dest = "/" + LIB + "/" + (rel + "/" if rel else "")
        mapping["/" + LIB + "/" + (rel + "/" if rel else "")] = code
        out = os.path.join(ROOT, "g", code)
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, "index.html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(PAGE.format(dest=dest, dest_js=json.dumps(dest)))
    with open(os.path.join(ROOT, "g", "map.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(dict(sorted(mapping.items())), f, indent=2)
        f.write("\n")
    print("Wrote %d short links in g/" % len(mapping))


main()
