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

  function urlFor(e) {
    var samePage = e.u.split('/').pop() === curPage;
    return samePage
      ? (e.a ? '#' + e.a : curPage)
      : (prefix + e.u + (e.a ? '#' + e.a : ''));
  }

  /* Ordered matches for a query: real content first. Entries that only
     point at the homepage helper (#helper) are last-resort — on the
     homepage itself they used to outrank every content page, so picking
     the top "Divorce" result just dropped the visitor back at the
     helper box on the same page. */
  function runSearch(q) {
    q = (q || '').trim();
    if (q.length < 2) return Promise.resolve([]);
    return load().then(function (idx) {
      var words = norm(q).split(/\s+/);
      var content = [];
      var helper = [];
      for (var i = 0; i < idx.length; i++) {
        var s = score(idx[i], words);
        if (s <= 0) continue;
        if (idx[i].e.a === 'helper') {
          helper.push({ e: idx[i].e, s: s });
          continue;
        }
        // boost results from the page the visitor is already on
        if (idx[i].e.u.split('/').pop() === curPage) s += 10;
        content.push({ e: idx[i].e, s: s });
      }
      content.sort(function (a, b) { return b.s - a.s; });
      helper.sort(function (a, b) { return b.s - a.s; });
      return content.concat(helper);
    });
  }

  function render(matches, q) {
    lastMatches = matches;
    lastQuery = q;
    if (!matches.length) {
      results.innerHTML = '<div class="ss-empty">No results for &ldquo;' +
        q.replace(/</g, '&lt;') + '&rdquo;. Try a state name or topic.</div>';
    } else {
      results.innerHTML = matches.slice(0, 12).map(function (m) {
        var e = m.e;
        var url = urlFor(e);
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
  var lastQuery = '';
  box.addEventListener('input', function () {
    clearTimeout(t);
    var q = box.value.trim();
    if (q.length < 2) { results.hidden = true; results.innerHTML = ''; lastMatches = []; lastQuery = ''; return; }
    t = setTimeout(function () {
      runSearch(q).then(function (matches) { render(matches, q); });
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
    if (ev.key === 'Enter') {
      ev.preventDefault();
      clearTimeout(t);
      var q = box.value.trim();
      /* Fast path: results for exactly this query are already shown. */
      if (lastMatches.length && lastQuery === q) {
        results.hidden = true;
        location.href = urlFor(lastMatches[0].e);
        return;
      }
      /* Slow path: Enter beat the debounce or the index is still
         loading — search now instead of doing nothing. */
      runSearch(q).then(function (matches) {
        if (matches.length) {
          results.hidden = true;
          location.href = urlFor(matches[0].e);
        } else {
          render(matches, q);
        }
      });
    }
  });
})();
