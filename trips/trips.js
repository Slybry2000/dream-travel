// Itinerary pages: highlight the section link in view, and draw the pin map.
(() => {
  const links = [...document.querySelectorAll('.tl-bar__nav a[href^="#"]:not(.tl-bar__title)')];
  const byId = new Map(links.map((a) => [a.getAttribute('href').slice(1), a]));
  const sections = [...byId.keys()].map((id) => document.getElementById(id)).filter(Boolean);

  if ('IntersectionObserver' in window && sections.length) {
    const seen = new Set();
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((e) => (e.isIntersecting ? seen.add(e.target.id) : seen.delete(e.target.id)));
      const current = sections.find((s) => seen.has(s.id));
      links.forEach((a) => a.classList.remove('is-active'));
      const link = current && byId.get(current.id);
      if (link) {
        link.classList.add('is-active');
        link.scrollIntoView({ block: 'nearest', inline: 'center' });
      }
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach((s) => observer.observe(s));
  }

  const mapEl = document.querySelector('.tl-map');
  if (!mapEl) return;
  const draw = () => {
    if (!window.L) return;
    const pins = JSON.parse(mapEl.dataset.pins);
    const map = L.map(mapEl, { scrollWheelZoom: false });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 17,
      attribution: '&copy; OpenStreetMap contributors',
    }).addTo(map);
    const points = pins.map((p, i) => {
      const icon = L.divIcon({ html: `<div class="tl-pin"><span>${String.fromCharCode(65 + i)}</span></div>`, iconSize: [30, 30], iconAnchor: [15, 30] });
      L.marker([p.lat, p.lng], { icon, title: p.name }).addTo(map).bindPopup(`<b>${p.name}</b>`);
      return [p.lat, p.lng];
    });
    map.fitBounds(points, { padding: [48, 48], maxZoom: 11 });
  };
  // Leaflet loads with defer, so it is ready by the time this deferred script runs.
  if (window.L) draw(); else window.addEventListener('load', draw);
})();
