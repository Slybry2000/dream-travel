# Dream Travel — Luxury Bespoke Journeys

A elegant, cinematic website for Dream Travel International Corp — crafting transformative travel experiences for discerning individuals and high-net-worth travelers.

## 🌍 Live Site

Visit the site at: **https://slybry2000.github.io/dream-travel/**

(See [GitHub Pages Setup](#github-pages-setup) below)

## 📑 Pages

| Page | File | Purpose |
|------|------|---------|
| **Homepage** | `index.html` | Top-of-funnel inspirational entry — hero parallax, differentiators, journey cards, testimonials, newsletter CTA |
| **Bespoke Journeys** | `journeys.html` | Core offering — flip cards for 6 journey types, sticky stack process, spotlight border themes, group info |
| **Experiences** | `experiences.html` | Curated destinations — curtain reveal hero, destination grid, featured Tuscany itinerary, testimonials |
| **Our Story** | `about.html` | Brand philosophy — split layout, sticky stack values, promise grid, trust-building stats |
| **Book Consultation** | `contact.html` | Conversion page — 2-column layout, elegant booking form, destination visual grid |
| **Ambassador** | `ambassador.html` | Referral program — 4-step process, 3 reward tiers (Explorer/Navigator/Luminary), application form |

## 🎨 Design System

- **Palette**: Warm ivory `#FDFBF7` / deep navy `#0C1015` with burnished gold `#C8922A` and forest sage accents
- **Fonts**: Playfair Display (serif headings) + Inter (body text)
- **Framework**: No build step — pure HTML/CSS/JavaScript with GSAP 3.12.5 for animations
- **Responsive**: Mobile-first, breakpoints at 1024px and 768px
- **Images**: Unsplash photography throughout

## ✨ Key Features

### Cinematic Animations
- **Scroll-Driven**: Text mask reveal, sticky stack, zoom parallax, curtain reveal, destination parallax
- **Click/Form**: Elegant form inputs with validation feedback, button state transitions
- **Auto-Play**: Kinetic marquee loops, text scramble effects

### Navigation
- Fixed header with glassmorphism effect
- Hamburger menu on mobile (< 768px)
- Unified footer across all pages
- All local page links (no external references)

### Performance
- CDN-hosted GSAP + ScrollTrigger
- Google Fonts via CDN
- Optimized Unsplash image URLs
- Single-file HTML per page (~300-450 lines each)

## 🚀 Quick Start

### Local Development
1. Clone the repository:
   ```bash
   git clone https://github.com/Slybry2000/dream-travel.git
   cd dream-travel
   ```

2. Open any `.html` file in your browser:
   - Use a local server for best results: `python -m http.server 8000`
   - Or use VS Code Live Server extension

3. Navigate using the header menu or footer links

### File Structure
```
dream-travel/
├── index.html                      # Homepage
├── journeys.html                   # Bespoke Journeys
├── experiences.html                # Curated Experiences
├── about.html                      # Our Story
├── contact.html                    # Book Consultation
├── ambassador.html                 # Ambassador Program
├── logo-footer.webp               # Logo asset
├── logo-header.webp               # Logo asset (alt)
├── Dream-Travel.code-workspace    # VS Code workspace config
└── README.md                       # This file
```

## 📋 GitHub Pages Setup

This site is ready to be hosted on GitHub Pages. To enable live deployment:

1. **Repository Settings** (https://github.com/Slybry2000/dream-travel/settings):
   - Go to **Pages** (left sidebar)
   - **Source**: Select "Deploy from a branch"
   - **Branch**: Select `main` / root folder
   - **Save**

2. **Wait for deployment** (~1-2 minutes)

3. **Visit your live site**: `https://slybry2000.github.io/dream-travel/`

### Important Notes
- GitHub Pages automatically deploys from the `main` branch
- The site is publicly accessible once enabled
- HTML files are served directly (no build step needed)
- Custom domain setup available in settings if needed

## 🔧 Customization

### Brands & Colors
Edit the CSS custom properties in any `.html` file's `<style>` block:
```css
:root {
  --bg: #FDFBF7;           /* Main background */
  --bg-dark: #0C1015;      /* Dark sections */
  --accent: #C8922A;       /* Gold accent */
  --accent2: #5B7C5E;      /* Sage accent */
  /* ...more properties... */
}
```

### Fonts
Replace Google Fonts import in the `<head>`:
```html
<link href="https://fonts.googleapis.com/css2?family=YourFont:wght@400;500;600&display=swap" rel="stylesheet">
```

### Images
All images use Unsplash CDN URLs. Replace with your own hosted images:
```html
<!-- Current format -->
<img src="https://images.unsplash.com/photo-1234567890123-1234567890?w=800&h=600&fit=crop" alt="Description">

<!-- Update with your images -->
<img src="your-image-url-or-path" alt="Description">
```

### GSAP Animations
Each page uses GSAP ScrollTrigger for scroll-driven animations. Modify in the `<script>` section of any page.

## 📧 Contact Links

- **Email**: `clients@dream-travel.net`
- **Phone**: `571 206 8949`
- **Social**: Instagram [@dreamtravel_adventures](https://www.instagram.com/dreamtravel_adventures/), Facebook [@dreamtravelinternationalcorp](https://www.facebook.com/dreamtravelinternationalcorp)

## 📜 License

All site content and design © 2026 Dream Travel International Corp

## 🤝 Contributing

To make changes:
1. Create a new branch: `git checkout -b feature/your-feature`
2. Make your edits
3. Commit: `git commit -m "Add feature"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

## 📱 Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Android)

## ⚡ Performance Tips

- Minify CSS/JS for production
- Optimize images further with image compression tools
- Consider lazy-loading for below-fold images
- CDN-hosted assets already optimized

---

**Built with ❤️ for luxury travel experiences**

For questions or support, contact: clients@dream-travel.net
