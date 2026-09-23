/* Dream Travel trip cards for any other website (e.g. the WordPress site at dream-travel.net).

   Paste once into a Custom HTML block:

     <div data-dream-trips="costa-rica"></div>
     <script src="https://adults.dream-travel.net/trips/embed.js" async></script>

   data-dream-trips takes a destination slug (costa-rica, france...) or "all".
   Cards are read live from trips.json, so new trips appear without touching the page. */
(() => {
  const script = document.currentScript;
  const feedUrl = new URL('trips.json', script ? script.src : 'https://adults.dream-travel.net/trips/');
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  const css = `
    .dt-trips{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr));gap:24px;font-family:Poppins,system-ui,sans-serif}
    .dt-trip{display:flex;flex-direction:column;overflow:hidden;border-radius:10px;background:#fff;box-shadow:0 10px 30px rgba(0,18,11,.08);color:#233744;text-align:left}
    .dt-trip__media{position:relative;display:block;aspect-ratio:4/3.4;overflow:hidden;background:#0b2a20}
    .dt-trip__media img{width:100%;height:100%;object-fit:cover;margin:0}
    .dt-trip__badge{position:absolute;top:0;right:0;padding:7px 14px;background:#95cdb8;color:#00120b;font-size:13px;border-bottom-left-radius:8px}
    .dt-trip__body{flex:1;display:flex;flex-direction:column;gap:8px;padding:20px 22px 24px}
    .dt-trip h3{margin:0 0 4px;font:400 22px/1.2 Newsreader,Georgia,serif;color:#00120b}
    .dt-trip h3 a{color:inherit;text-decoration:none}
    .dt-trip p{margin:0;font-size:14px;line-height:1.5}
    .dt-trip__cta{margin-top:auto;align-self:flex-start;padding:10px 18px;border:1px solid #00120b;border-radius:6px;color:#00120b;font-size:12px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;text-decoration:none}
    .dt-trip__cta:hover{background:#00120b;color:#fff}`;

  const card = (t) => `
    <article class="dt-trip">
      <a class="dt-trip__media" href="${esc(t.url)}"><img src="${esc(t.image)}" alt="" loading="lazy"><span class="dt-trip__badge">${esc(t.duration)}</span></a>
      <div class="dt-trip__body">
        <h3><a href="${esc(t.url)}">${esc(t.title)}</a></h3>
        <p><b>Location(s):</b> ${esc((t.locations || []).slice(0, 4).join(', ') || t.country)}</p>
        ${t.tags && t.tags.length ? `<p>${esc(t.tags.join(' | '))}</p>` : ''}
        ${t.overnights ? `<p><b>Overnights:</b> ${esc(t.overnights)}</p>` : ''}
        <a class="dt-trip__cta" href="${esc(t.url)}">See itinerary</a>
      </div>
    </article>`;

  fetch(feedUrl).then((r) => r.json()).then(({ trips }) => {
    if (!document.getElementById('dt-trips-css')) {
      const style = document.createElement('style');
      style.id = 'dt-trips-css';
      style.textContent = css;
      document.head.appendChild(style);
    }
    document.querySelectorAll('[data-dream-trips]').forEach((el) => {
      const want = (el.dataset.dreamTrips || 'all').toLowerCase();
      const list = trips.filter((t) => want === 'all' || t.country_slug === want);
      el.innerHTML = list.length
        ? `<div class="dt-trips">${list.map(card).join('')}</div>`
        : '';
    });
  }).catch(() => {});
})();
