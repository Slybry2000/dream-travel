/* Journey path tracking.
   Remembers where a visitor first came from (for example the journey email)
   and which of our pages they looked at on the way, then hands that to the
   planner form so each form that comes in shows its route, e.g.
   "journey-email:autoreply-trips  ->  trips > kit".

   Usage: <script src="/journey-path.js" data-page="trips|kit|home|planning"></script>
   Params passed to the planner: dt_src (first source) and dt_path (pages seen).
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

  if (page && page !== 'planning' && state.path[state.path.length - 1] !== page) state.path.push(page);
  state.path = state.path.slice(-8);
  state.t = Date.now();
  try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {}

  function params() {
    return { dt_src: state.src || 'direct', dt_path: state.path.join('>') || 'none' };
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
