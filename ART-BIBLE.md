# Art Bible — Dream Travel

## 1. Voice & Feel
Hosted, considered, intimate. The brand voice sounds like a trusted host writing to a small circle of guests, not a travel-agency brochure. Read like a quiet villa terrace just after the meal — generous, unhurried, photographic. Restraint is the baseline; every element earns its place.

## 2. Palette

| Token | Hex | Usage rule | Forbidden combos |
|---|---|---|---|
| `--ink` | `#14100c` | Page background outside hero, footer fill, body text on cream surfaces | Never paired with pure black; never as text on the dark hero |
| `--cream` | `#f1e8d8` | Primary text on dark surfaces, secondary surface mid-tones | Never below 60% opacity for body copy |
| `--cream-strong` | `#faf3e6` | Headline text on dark, secondary surface background | Never as a small UI fill (looks like SaaS surface) |
| `--paper` | `#ece2cf` | Section-flip surface, card backgrounds | Never gradiented |
| `--terracotta` | `#b85c38` | Single accent — underlines, filled CTA, italic word emphasis | NEVER as a gradient; NEVER as a glow; NEVER as a stroke wider than 4px; max ~3% of page pixels |
| `--terracotta-deep` | `#984a2c` | Fill of the single `.cta--filled`, and hover / pressed state of `--terracotta` | Never as a large background field; never as a second accent |
| `--terracotta-press` | `#7d3c23` | Hover / pressed state of the filled CTA only | Never as a default state, never as text |
| `--terracotta-text` | `#984a2c` light, `#c96a44` on ink, `#d3764e` / `#e69a77` on dark surfaces | Terracotta used as *text* (kickers, step numbers, slot fields, compare titles) | Accessibility tint only. `#b85c38` stays the accent for rules, borders and large italic display words |
| `--muted-ink` | `#4a3b30` | Body copy on cream surfaces | Never as a primary headline color |

**Forbidden combos:** terracotta + sage green together (looks Christmas); terracotta over cream-strong with a drop shadow (looks 2014 flat-design); any two-color gradient anywhere; any cyan/blue/violet/neon.

## 3. Typography

**Families**
- Display: **Fraunces** (variable serif, opsz 9–144). SemiBold weight; italic reserved for the closing word of a headline.
- Body: **Inter** 400 / 500 / 600. No italic in body copy.
- Meta / index: **JetBrains Mono** 500 all caps.

**Scale (responsive clamp())**
- Display: `clamp(48px, 7vw, 88px)` — cap is 88px (LESSONS §2). Line-height 0.94, tracking -0.025em, optical size 96 (144 for italic).
- Sub-display: `clamp(28px, 3.6vw, 44px)`.
- Body large: `clamp(18px, 1.4vw, 20px)`, line-height 1.6.
- Body: 16px, line-height 1.65.
- Meta / mono: 11px, letter-spacing 0.22em, uppercase.

**Treatment rules**
- The display closes a thought with a period and an italic emphasis word (e.g. `people.`, `place.`, `together.`). One italic word per headline, never more.
- No exclamation marks anywhere on the site.
- No em dashes in copy. Use periods and short sentences. (Em dashes allowed only in the `INDEX / 01 — TERRACE` style metadata marker.)
- ALL CAPS only in mono labels (meta, nav, index, kicker), never in headlines or body copy.

**Banned words/phrases:** `unlock`, `transform`, `ultimate`, `world-class`, `next-generation`, `cutting-edge`, `bucket-list`, `dream destination`, `seamless` (overused), `curated experiences`, `unforgettable journey`.

**Preferred verbs:** `host`, `plan`, `gather`, `travel`, `build`, `shape`, `keep`, `share`. The brand operates on hosting; the verbs should sound human, not aspirational.

## 4. Spacing & Layout

**Base unit:** 4px. All paddings/margins land on a 4px grid.

**Tokens**
- `--gutter`: `clamp(24px, 5vw, 72px)` — left/right page gutter and the right anchor for hero content + CTA.
- Section vertical rhythm: `clamp(96px, 14vh, 160px)` between major sections on the dark surface; `clamp(80px, 12vh, 132px)` on cream.

**Container widths**
- Headline column: `max-width: min(560px, 60vw)` (LESSONS §2 — never raise display cap past 88px without widening this).
- Body text column: `max-width: 56ch`.
- Wide editorial list column: `max-width: 880px`.

**Composition principle (load-bearing):**
> **One loud move per section.** Each section has exactly one element of high contrast — a terracotta accent rule, an italic display word, a single full-bleed photograph, or one editorial pull-quote. Every other element submits to the photograph or to whitespace.

Hero composition rule (LESSONS §1): content top-right, CTA bottom-right, index marker bottom-left. Apply to every dark section.

Rhythm-flip rule: alternate dark hero-style surfaces with cream `--paper` surfaces. Every other section flips. The anchor corner of the headline also flips (top-right ↔ top-left) so the eye travels diagonally down the page.

## 5. Components

**Wordmark** — Fraunces SemiBold 13px, `letter-spacing: 0.24em`, uppercase, `--cream` on dark / `--ink` on cream. No icon. No tagline. Top-left of any hero-type section.

**Nav** — Fraunces 500 12px, `letter-spacing: 0.24em`, uppercase, 72% opacity, hover-to-100%. No active-state pill, no underline. Right-aligned next to the wordmark. Hidden below 768px (no hamburger drawer — the page is single-flow, the user scrolls).

**Ghost CTA (default)** — 1px `--cream` border on dark / 1px `--ink` border on cream. Fraunces 500 12px caps, `letter-spacing: 0.22em`. Right-arrow SVG (`5 12 → 18 12`) on the end, translates +4px on hover. Used in hero and at every section CTA *except* the final.

**Filled CTA (final only)** — `--terracotta-deep` (`#984a2c`) fill, `--cream-strong` text, same typography as ghost CTA. Hover → `--terracotta-press` (`#7d3c23`). The deep tone is the CTA's default fill by exception, so that white-on-terracotta clears AA at body size; `--terracotta` `#b85c38` does not. Used **once per page**, on the final-CTA section.

**Meta line** — JetBrains Mono 11px caps, `letter-spacing: 0.22em`, 66% opacity. Period-separated. Examples: `HOSTED. PRIVATE. CUSTOM.` / `LISBON. PUGLIA. MARRAKECH.` / `04 NIGHTS. 12 GUESTS.`

**Section divider** — Either a 64px × 3px `--terracotta` rule or a single hairline of `--line` (`rgba(241,232,216,0.18)` on dark / `rgba(20,16,12,0.10)` on cream). Never both in the same section.

**Editorial service list item** — Numbered `01 / Lisbon Table`, name in Fraunces SemiBold 24–28px, two-line body in Inter 16/1.65. Use the LESSONS §3 explicit grid placement (`grid-column` + `grid-row`) — never auto-flow.

## 6. Imagery & Motion

**Crop logic:** Architectural detail crops only (LESSONS §10). The hero is a table corner, not a panoramic terrace. Every supporting photograph follows the same rule: hand-folded itinerary on a knee, terracotta jug spout, a single empty chair at the head of a table. **Never** an establishing shot. **Never** a face. **Never** a person in the frame.

**Color grade:** Warm tungsten undertone. Shadows pulled to `#3a2a1f`, highlights softly clipped at honey-cream. No cool cast, no blue shadow.

**Grain:** 35mm-feel grain at ~6% opacity, applied via a CSS `mix-blend-mode: overlay` noise layer when needed. Never as a heavy texture overlay.

**Motion budget:** Sub-5% of the frame at any moment. Hover transforms ≤ 4px translate, ≤ 220ms. No parallax. No scroll-jacking. The Seedance hero MP4 (if added) is a locked-off camera with ambient micro-motion only.

**Reduced-motion fallback:** All transitions ≤ 0.001ms; the still PNG poster paints in place of any video.

## 7. Forbidden Patterns

1. **Centered hero + two buttons** (the median travel-agency homepage).
2. **Left-text / right-image split** with a card and a CTA bar.
3. **World map with pushpins** or a globe spinning anywhere on the page.
4. **Floating polaroids** or destination cards that "scatter" across a hero.
5. **Plane-window photo** of a wing over clouds.
6. **Beach sunset with two silhouettes** or any sunset stock photo.
7. **Compass + passport + camera flatlay.**
8. **Crowd photographs**, tourist clusters, raised wine glasses, "cheers" moments, group selfies.
9. **Gradient blob** behind a headline — terracotta or otherwise.
10. **Glassmorphism cards** with backdrop-blur.
11. **Trusted-by logo carousel** of partner airlines or "as seen in" media badges.
12. **Em dashes in copy** (allowed in index meta only).
13. **Stat counters that tick up** ("500+ trips planned", "1200 happy travelers") — these signal a marketing template.
14. **"Book now"** or **"Reserve your spot"** CTA copy. The site is hosted, not transactional. Use "Begin a journey", "Plan together", "Start a conversation".
15. **Drop shadows** on cards, buttons, or images. The page works on warm light, not depth-layering.
16. **A second accent color.** Terracotta is alone. Sage and gold from the previous palette are explicitly retired in this redesign.

---

## 2026 Reference-Format Addendum

This addendum governs the current homepage and supersedes the earlier rules above where they conflict. The source content remains Dream Travel's; the page format follows the supplied luxury-travel reference without reusing its trademarks, copy, claims, or media.

- **Voice:** direct, assured, editorial. Verified Dream Travel copy stays human and specific.
- **Palette:** verified Dream Travel deep green `#00120b`, peach `#fba676`, mint `#95cdb8`, off-white `#fcfcfc`, and slate body text `#233744`. Terracotta `#b96d55` is reserved for the closing action field.
- **Type:** Newsreader 400/500/600 is the editorial voice for major headlines, section titles, reassurance titles, testimonial copy, and large hosting numerals. Locally hosted Story Script Regular is reserved for the emotional hero phrase and trip/group names. Poppins 400/500/600/700 handles body copy, navigation, buttons, forms, links, kickers, and practical metadata. Change `data-type-system="journal"` to another value to remove the Newsreader overrides and restore the prior Story Script/Poppins hierarchy.
- **Composition:** full-height centered hero; centered narrative block; horizontal proof rail; one combined 3D discovery sphere for group types and example trips; buffered alternating story cards; five icon-pack reassurance points; terracotta closing field; dense deep-green footer. The former dual rails remain available through the reversible layout flag.
- **Imagery:** the verified Dream Travel hero remains responsive AVIF/WebP with its original PNG fallback. Ten distinct, locally optimized WebP photographs were generated specifically for the six group types and four example trips; supporting story cards reuse three of these contextual plates.
- **Graphic flourishes:** six bespoke, line-only marks act as visual punctuation: hero loop, introductory swoop, incomplete sphere orbit, hosting route with waypoints, story arrow, and closing sunburst. Use rounded imperfect strokes in peach, mint, or terracotta; never place them over faces or essential text. `data-flourishes="off"` removes the full layer.
- **Motion:** the discovery sphere auto-rotates slowly, responds to horizontal touch drag and two-axis mouse drag with restrained inertia, and exposes pause and reset controls. Its ambient background is a progressive enhancement: one muted group-specific clip at a time, crossfaded only when another group comes forward. The current free Pexels clips are visibly labeled previews and must be replaced or approved before production. Posters remain the first paint and the fallback for reduced motion, data saving, playback failure, or disabled motion. The sphere pause control also pauses video. Custom flourish paths draw once as they enter view; reduced-motion paints them statically. The former carousels retain their controls when rail mode is restored.
- **Motion art direction:** show the human heartbeat of a group, not a generic destination reel. Favor conversation, shared attention, hands making or tasting, relaxed walking, laughter, and small arrival moments. Avoid drone establishing shots, rapid cuts, timelapses, camera-whip transitions, visible logos, staged pointing, and model-release ambiguity. Keep clips silent, 6–12 seconds, H.264 MP4, and locally hosted. `data-motion-preview="off"` removes the complete preview layer.
- **Forbidden:** reference-site branding or copy, unverified awards, invented destinations or claims, visible horizontal scrollbars, fake forms, tracker scripts, glass effects, autoplay audio, generic travel clip art, airplanes, luggage, passports, stock doodle packs, and decorative marks without narrative meaning.
