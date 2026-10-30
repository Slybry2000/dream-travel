---
name: add-wetravel-trips
description: Add Rene's new adult trip PDFs (art, wellness) from Google Drive to WeTravel, check and fix them, tag them, log them in the TRIPS ON WETRAVEL sheet, move the PDFs to ON WETRAVEL, and publish them on adults.dream-travel.net. Also renames adult trips and fixes their photos. Use when Bryan says "add the new trips", "upload the trip PDFs", "put the new art/wellness trips on WeTravel", "check the trips", "fix the trip photos", or "rename the trips". Never for student or pickleball trips.
---

# Add WeTravel trips

Follow `_trips/ADDING-TRIPS.md` in this repo exactly, top to bottom. It is the standard
procedure; this skill only points to it.

Before starting:
1. Read `_trips/ADDING-TRIPS.md` in full, and `_trips/adult_trips.json` (the adult allowlist).
2. Confirm `WETRAVEL_API_KEY` exists in `.env` (do not print it).
3. List what is waiting in the Drive SOME PDF folder and tell Bryan the batch in one line
   (trip names in the "Country: Theme" format) before building. Publishing trips to Rene's
   WeTravel and to the public website is his request when he asks for this skill; anything
   beyond the procedure (deleting, changing student trips, emailing anyone) needs a separate yes.

While working:
- Keep the task list current; run `python _trips/tools/trip_qa.py` after building and again at the end.
- If a trip names a client, hold it back and say so; never commit a client's name.
- If a step's screen differs from the procedure, adapt, then update `_trips/ADDING-TRIPS.md`
  with what changed (self-annealing).

Finish with: what is live (WeTravel short links and the website page), what was held back and why,
and anything Rene or Bryan must decide.
