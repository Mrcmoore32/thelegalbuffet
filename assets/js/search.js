/* Site-wide search for The Legal Buffet */
(function () {
  var box = document.getElementById('site-search');
  var results = document.getElementById('site-search-results');
  if (!box || !results) return;

  /* Let screen readers announce results as they appear. */
  results.setAttribute('role', 'status');
  results.setAttribute('aria-live', 'polite');

  var prefix = location.pathname.indexOf('/states/') !== -1 ? '../' : '';
  var curPage = location.pathname.split('/').pop() || 'index.html';
  var index = null;

  function norm(s) {
    return (s || '').toLowerCase().replace(/[^a-z0-9\s]/g, ' ');
  }

  function load() {
    if (index) return Promise.resolve(index);
    return fetch(prefix + 'assets/search-index.json')
      .then(function (r) { return r.json(); })
      .then(function (data) {
        index = data.map(function (e) {
          return { e: e, h: norm(e.h), t: norm(e.t), p: norm(e.p) };
        });
        return index;
      })
      .catch(function () { return []; });
  }

  function score(entry, words) {
    var s = 0;
    for (var i = 0; i < words.length; i++) {
      var w = words[i];
      if (!w) continue;
      if (entry.h.indexOf(w) !== -1) s += 5;
      else if (entry.p.indexOf(w) !== -1) s += 2;
      else if (entry.t.indexOf(w) !== -1) s += 1;
      else return -1;
    }
    return s;
  }

  function render(matches, q) {
    lastMatches = matches;
    if (!matches.length) {
      results.innerHTML = '<div class="ss-empty">No results for &ldquo;' +
        q.replace(/</g, '&lt;') + '&rdquo;. Try a state name or topic.</div>';
    } else {
      results.innerHTML = matches.slice(0, 12).map(function (m) {
        var e = m.e;
        var samePage = e.u.split('/').pop() === curPage;
        var url = samePage
          ? (e.a ? '#' + e.a : curPage)
          : (prefix + e.u + (e.a ? '#' + e.a : ''));
        var page = e.p.replace(/ \| The Legal Buffet| — The Legal Buffet| - The Legal Buffet/, '');
        return '<a class="ss-hit" href="' + url + '">' +
          '<span class="ss-h">' + e.h.replace(/</g, '&lt;') + '</span>' +
          '<span class="ss-p">' + page.replace(/</g, '&lt;') + '</span></a>';
      }).join('');
    }
    results.hidden = false;
  }

  var t = null;
  var lastMatches = [];
  box.addEventListener('input', function () {
    clearTimeout(t);
    var q = box.value.trim();
    if (q.length < 2) { results.hidden = true; results.innerHTML = ''; return; }
    t = setTimeout(function () {
      load().then(function (idx) {
        var words = norm(q).split(/\s+/);
        var scored = [];
        for (var i = 0; i < idx.length; i++) {
          var s = score(idx[i], words);
          if (s > 0) {
            // boost results from the page the visitor is already on
            if (idx[i].e.u.split('/').pop() === curPage) s += 10;
            scored.push({ e: idx[i].e, s: s });
          }
        }
        scored.sort(function (a, b) { return b.s - a.s; });
        render(scored, q);
      });
    }, 180);
  });

  document.addEventListener('click', function (ev) {
    if (!ev.target.closest('.site-search')) { results.hidden = true; }
  });
  /* Same-page anchor results don't reload the page, so the dropdown would
     otherwise stay open over the section it just jumped to. */
  results.addEventListener('click', function (ev) {
    if (ev.target.closest('.ss-hit')) results.hidden = true;
  });
  box.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') { results.hidden = true; box.blur(); return; }
    if (ev.key === 'ArrowDown' || ev.key === 'ArrowUp') {
      var hits = results.querySelectorAll('.ss-hit');
      if (!hits.length) return;
      ev.preventDefault();
      var idx = Array.prototype.indexOf.call(hits, document.activeElement);
      if (ev.key === 'ArrowDown') idx = idx < hits.length - 1 ? idx + 1 : 0;
      else idx = idx > 0 ? idx - 1 : hits.length - 1;
      hits[idx].focus();
      return;
    }
    if (ev.key === 'Enter' && lastMatches.length) {
      // jump straight to the top result (same URL logic as the rendered links)
      var e = lastMatches[0].e;
      var samePage = e.u.split('/').pop() === curPage;
      var url = samePage
        ? (e.a ? '#' + e.a : curPage)
        : (prefix + e.u + (e.a ? '#' + e.a : ''));
      ev.preventDefault();
      results.hidden = true;
      location.href = url;
    }
  });
})();
