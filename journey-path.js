/* Journey path tracking.
   Remembers where a visitor first came from (for example the journey email)
   and which of our pages they looked at on the way, then hands that to the
   planner form so each form that comes in shows its route, e.g.
   "journey-email:autoreply-trips  ->  trips > kit".

   Usage: <script src="/journey-path.js" data-page="trips|kit|home|planning"></script>
   Params passed to the planner: dt_src (first source), dt_path (pages seen) and audience (trip type, if a link named one).
   Calendly links get the same route in utm_term, because Calendly only keeps utm_* fields. */
(function () {
  var KEY = 'dt_journey';
  var TTL = 30 * 24 * 3600 * 1000;
  var me = document.currentScript;
  var page = (me && me.getAttribute('data-page')) || '';
  var q = new URLSearchParams(location.search);

  var state = null;
  try { state = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) {}
  if (!state || Date.now() - (state.t || 0) > TTL) state = { src: '', path: [], t: Date.now() };

  /* A new arrival from a tagged link starts a fresh route. */
  var src = q.get('utm_source');
  if (src && src !== 'leader-kit') {
    var label = src + (q.get('utm_content') ? ':' + q.get('utm_content') : '');
    if (label !== state.src) state = { src: label, path: [], t: Date.now() };
  }
  /* Carry a route handed over in the URL (e.g. the planner page). */
  if (q.get('dt_src') && !state.src) state.src = q.get('dt_src');
  if (q.get('dt_path') && !state.path.length) state.path = q.get('dt_path').split('>');

  /* Trip type (audience): a link like ?audience=beer is remembered with the route, so a person who arrives from a
     beer email and comes back through the site on their own still gets the beer planner. A new tagged link
     without an audience starts a fresh route above, which clears it (old wellness links stay wellness). */
  var aud = (q.get('audience') || '').toLowerCase();
  if (/^[a-z]{2,20}$/.test(aud)) state.aud = aud;

  if (page && page !== 'planning' && state.path[state.path.length - 1] !== page) state.path.push(page);
  state.path = state.path.slice(-8);
  state.t = Date.now();
  try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {}

  /* Visitor code (dt_t): a private 16-character code the journey emails carry for each person. It is made on
     the Dream Travel server from the address, so it holds no email. Remembered for 90 days so later visits to
     the site are recognised, and every page view is reported to the planner site's visit log (no IP, no user
     agent, no cookies) so the customer-journey view can show what each person actually looked at. */
  var VKEY = 'dt_visitor';
  var visitor = '';
  try {
    var saved = JSON.parse(localStorage.getItem(VKEY) || 'null');
    if (saved && saved.id && Date.now() - (saved.t || 0) < 90 * 24 * 3600 * 1000) visitor = saved.id;
    var fresh = q.get('dt_t');
    if (fresh && /^[0-9a-f]{16}$/.test(fresh)) { visitor = fresh; localStorage.setItem(VKEY, JSON.stringify({ id: fresh, t: Date.now() })); }
  } catch (e) { var f2 = q.get('dt_t'); if (f2 && /^[0-9a-f]{16}$/.test(f2)) visitor = f2; }
  if (visitor) {
    try {
      var beacon = JSON.stringify({ t: visitor, p: page || location.pathname.replace(/^\/|\/$/g, '') || 'home', s: state.src || '' });
      var endpoint = 'https://dream-travel-planner.perseidechocreations.workers.dev/api/track';
      if (!(navigator.sendBeacon && navigator.sendBeacon(endpoint, beacon))) fetch(endpoint, { method: 'POST', body: beacon, keepalive: true, mode: 'no-cors' });
    } catch (e) {}
  }

  function params() {
    var out = { dt_src: state.src || 'direct', dt_path: state.path.join('>') || 'none' };
    if (state.aud) out.audience = state.aud;
    if (visitor) out.dt_t = visitor;
    return out;
  }
  window.dtJourneyParams = params;

  function decorate(a) {
    var href = a.getAttribute('href') || '';
    var p = params();
    try {
      if (/(^|adults\.dream-travel\.net)\/planning\/?/.test(href) || href.indexOf('../planning/') === 0 || href === 'planning/') {
        var u = new URL(a.href, location.href);
        u.searchParams.set('dt_src', p.dt_src);
        u.searchParams.set('dt_path', p.dt_path);
        if (p.audience && !u.searchParams.get('audience')) u.searchParams.set('audience', p.audience);
        if (p.dt_t) u.searchParams.set('dt_t', p.dt_t);
        a.href = u.toString();
      } else if (href.indexOf('calendly.com/') > -1) {
        var c = new URL(a.href);
        if (!c.searchParams.get('utm_term')) c.searchParams.set('utm_term', p.dt_src + '|' + p.dt_path);
        a.href = c.toString();
      }
    } catch (e) {}
  }

  function run() { document.querySelectorAll('a[href]').forEach(decorate); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
  /* Catch links changed later (e.g. the kit page's A/B and done-mode script). */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (a) decorate(a);
  }, true);
})();
