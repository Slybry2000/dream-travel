# Dream Travel — reference-format redesign ledger

## Confirmed source content

- Brand: Dream Travel.
- Offering: customized adult group travel for clubs and organizations, hosted by trusted community leaders.
- Journeys: Taste Italy, Create in Greece, Experience France, Discover Portugal.
- Group size: 10–25 guests for the example journeys.
- Hosting returns: travel free, earn a share, or give it back.
- Contact: go@dream-travel.net; call or text 571 206 8949; existing conversation form and Calendly links retained.
- Testimonials and operating copy are preserved from the local homepage.

## Confirmed visual assets

- Dream Travel header and footer logos from `images/`.
- Existing desktop and mobile hero photography and responsive AVIF/WebP variants.
- Local Story Script font supplied by Dream Travel; Poppins loaded at weights 400, 500, 600, and 700.
- Ten distinct generated editorial photographs in `images/generated/`, optimized to 1024px WebP: six group types and four example trips.
- Font Awesome Free provides the five reassurance icons and the Facebook/Instagram marks; no reference-site assets, logos, claims, or copy are reused.

## Reference format translated

- Full-height image hero with transparent navigation and centered two-action lockup.
- Centered editorial introduction, horizontal testimonial proof, group discovery carousel, dark example-trip carousel, buffered text/media story cards, five reassurance points, closing action field, and columnar dark footer.
- Dream Travel deep green, peach, mint, off-white, terracotta closing field, Story Script display type, and Poppins body/UI type.
- Experimental discovery mode combines the six groups and four example trips in a lightweight DOM/CSS 3D sphere. Peach frames identify groups; mint frames identify example trips. Change `data-discovery-layout="orbit"` to `"rails"` on `<body>` to restore the previous carousels.
- Experimental editorial type mode uses Newsreader for major headings and testimonials, Story Script only for emotional accents and destination/group names, and Poppins for practical UI and body copy. It is enabled with `data-type-system="journal"`.
- Six original inline SVG flourishes provide a restrained hand-drawn route language across the homepage. They contain no text or third-party artwork, are hidden from assistive technology, draw once on entry, and remain static for reduced-motion users. The layer is enabled with `data-flourishes="on"`.
- The discovery sphere now has an optional human-centered motion layer. The group closest to the viewer selects one of six locally hosted background clips; the sphere control pauses both rotations and playback. The preview is enabled with `data-motion-preview="on"` and can be removed without changing the sphere or content.

## Scope and visual thesis

- One responsive homepage at 1440, 1024, 768, 430, and 390 pixels; keyboard, reduced-motion, and mobile menu states included.
- Thesis: the existing Mediterranean host-and-table hero introduces an image-led sequence of distinct group and destination scenes. Story Script supplies warmth while Poppins, deep green fields, peach actions, and mint buffers keep the visual system recognizably Dream Travel.
- Forbidden: reference-site trademarks or copy, unverified awards or service claims, invented destinations, fake press logos, visible horizontal scrollbars, glass effects, autoplay audio, and unlicensed production media.

## Asset ledger

- Generated assets: `art-groups.webp`, `wellness-groups.webp`, `history-book-groups.webp`, `empty-nesters.webp`, `midlife-women.webp`, `culinary-groups.webp`, `trip-italy.webp`, `trip-greece.webp`, `trip-france.webp`, and `trip-portugal.webp`. All were generated as text-free photographic plates with mature adult groups, authentic group activity, warm natural light, and Dream Travel peach/mint/deep-green color cues.
- Generation mode: built-in image generation. Files were converted to 1024px WebP for local delivery; no remote generated-image dependency remains.
- Substituted assets: Font Awesome Free replaces the former numbered reassurance circles; the live Dream Travel Facebook and Instagram URLs were verified and added.
- Placeholder motion assets: six free Pexels SD preview clips and six matching local WebP posters in `videos/preview/`. They are visibly labeled on the page, documented in `VIDEO-ASSET-LEDGER.md`, and are not presented as final production footage.
