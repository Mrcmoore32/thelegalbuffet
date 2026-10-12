/* Site-wide search for The Legal Buffet */
(function () {
  var box = document.getElementById('site-search');
  var results = document.getElementById('site-search-results');
  if (!box || !results) return;

  var prefix = location.pathname.indexOf('/states/') !== -1 ? '../' : '';
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
    if (!matches.length) {
      results.innerHTML = '<div class="ss-empty">No results for &ldquo;' +
        q.replace(/</g, '&lt;') + '&rdquo;. Try a state name or topic.</div>';
    } else {
      results.innerHTML = matches.slice(0, 8).map(function (m) {
        var e = m.e;
        var url = prefix + e.u + (e.a ? '#' + e.a : '');
        var page = e.p.replace(/ \| The Legal Buffet| — The Legal Buffet| - The Legal Buffet/, '');
        return '<a class="ss-hit" href="' + url + '">' +
          '<span class="ss-h">' + e.h.replace(/</g, '&lt;') + '</span>' +
          '<span class="ss-p">' + page.replace(/</g, '&lt;') + '</span></a>';
      }).join('');
    }
    results.hidden = false;
  }

  var t = null;
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
          if (s > 0) scored.push({ e: idx[i].e, s: s });
        }
        scored.sort(function (a, b) { return b.s - a.s; });
        render(scored, q);
      });
    }, 180);
  });

  document.addEventListener('click', function (ev) {
    if (!ev.target.closest('.site-search')) { results.hidden = true; }
  });
  box.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') { results.hidden = true; box.blur(); }
  });
})();
