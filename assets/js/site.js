/* The Legal Buffet — shared behavior. No dependencies. */
(function () {
  "use strict";

  /* All 50 states. `ready: true` only for states with researched content. */
  var STATES = [
    ["Alabama", "alabama"], ["Alaska", "alaska"], ["Arizona", "arizona"],
    ["Arkansas", "arkansas"], ["California", "california"], ["Colorado", "colorado"],
    ["Connecticut", "connecticut"], ["Delaware", "delaware"], ["Florida", "florida"],
    ["Georgia", "georgia"], ["Hawaii", "hawaii"], ["Idaho", "idaho"],
    ["Illinois", "illinois"], ["Indiana", "indiana"], ["Iowa", "iowa"],
    ["Kansas", "kansas"], ["Kentucky", "kentucky"], ["Louisiana", "louisiana"],
    ["Maine", "maine"], ["Maryland", "maryland"], ["Massachusetts", "massachusetts"],
    ["Michigan", "michigan"], ["Minnesota", "minnesota"], ["Mississippi", "mississippi"],
    ["Missouri", "missouri"], ["Montana", "montana"], ["Nebraska", "nebraska"],
    ["Nevada", "nevada"], ["New Hampshire", "new-hampshire"], ["New Jersey", "new-jersey"],
    ["New Mexico", "new-mexico"], ["New York", "new-york"], ["North Carolina", "north-carolina"],
    ["North Dakota", "north-dakota"], ["Ohio", "ohio"], ["Oklahoma", "oklahoma"],
    ["Oregon", "oregon"], ["Pennsylvania", "pennsylvania"], ["Rhode Island", "rhode-island"],
    ["South Carolina", "south-carolina"], ["South Dakota", "south-dakota"],
    ["Tennessee", "tennessee"], ["Texas", "texas"], ["Utah", "utah"],
    ["Vermont", "vermont"], ["Virginia", "virginia"], ["Washington", "washington"],
    ["West Virginia", "west-virginia"], ["Wisconsin", "wisconsin"], ["Wyoming", "wyoming"]
  ];

  /* Populate any <select data-state-picker> with the 50 states. */
  document.querySelectorAll("select[data-state-picker]").forEach(function (sel) {
    if (sel.options.length > 1) return;
    STATES.forEach(function (s) {
      var o = document.createElement("option");
      o.value = s[1];
      o.textContent = s[0];
      sel.appendChild(o);
    });
    sel.addEventListener("change", function () {
      if (sel.value) window.location.href = "states/" + sel.value + ".html";
    });
  });


  /* ZIP code prefix (first 3 digits) -> state slug. Covers all 50 states. */
  var ZIP_RANGES = [
    [5, 5, "new-york"], [10, 27, "massachusetts"], [28, 29, "rhode-island"],
    [30, 38, "new-hampshire"], [39, 49, "maine"], [50, 54, "vermont"],
    [55, 55, "massachusetts"], [56, 59, "vermont"], [60, 69, "connecticut"],
    [70, 89, "new-jersey"], [100, 149, "new-york"], [150, 191, "pennsylvania"],
    [193, 196, "pennsylvania"], [197, 199, "delaware"], [201, 201, "virginia"],
    [206, 212, "maryland"], [214, 219, "maryland"], [220, 246, "virginia"],
    [247, 268, "west-virginia"], [270, 289, "north-carolina"], [290, 299, "south-carolina"],
    [300, 319, "georgia"], [320, 342, "florida"], [344, 344, "florida"],
    [346, 347, "florida"], [349, 349, "florida"], [350, 352, "alabama"],
    [354, 369, "alabama"], [370, 385, "tennessee"], [386, 397, "mississippi"],
    [398, 398, "georgia"], [400, 418, "kentucky"], [420, 427, "kentucky"],
    [430, 458, "ohio"], [460, 479, "indiana"], [480, 499, "michigan"],
    [500, 528, "iowa"], [530, 532, "wisconsin"], [534, 535, "wisconsin"],
    [537, 549, "wisconsin"], [550, 551, "minnesota"], [553, 567, "minnesota"],
    [570, 577, "south-dakota"], [580, 588, "north-dakota"], [590, 599, "montana"],
    [600, 620, "illinois"], [622, 629, "illinois"], [630, 631, "missouri"],
    [633, 641, "missouri"], [644, 648, "missouri"], [650, 658, "missouri"],
    [660, 662, "kansas"], [664, 679, "kansas"], [680, 681, "nebraska"],
    [683, 693, "nebraska"], [700, 701, "louisiana"], [703, 708, "louisiana"],
    [710, 714, "louisiana"], [716, 729, "arkansas"], [730, 731, "oklahoma"],
    [733, 733, "texas"], [734, 741, "oklahoma"], [743, 749, "oklahoma"],
    [750, 799, "texas"], [800, 816, "colorado"], [820, 831, "wyoming"],
    [832, 838, "idaho"], [840, 841, "utah"], [843, 847, "utah"],
    [850, 853, "arizona"], [855, 857, "arizona"], [859, 860, "arizona"],
    [863, 865, "arizona"], [870, 871, "new-mexico"], [873, 875, "new-mexico"],
    [877, 884, "new-mexico"], [885, 889, "texas"], [890, 891, "nevada"],
    [893, 895, "nevada"], [897, 898, "nevada"], [900, 908, "california"],
    [910, 928, "california"], [930, 961, "california"], [967, 968, "hawaii"],
    [970, 979, "oregon"], [980, 986, "washington"], [988, 994, "washington"],
    [995, 999, "alaska"]
  ];

  function stateForZip(zip) {
    var digits = String(zip).replace(/\D/g, "").slice(0, 5);
    if (digits.length < 3) return null;
    var prefix = parseInt(digits.slice(0, 3), 10);
    for (var i = 0; i < ZIP_RANGES.length; i++) {
      if (prefix >= ZIP_RANGES[i][0] && prefix <= ZIP_RANGES[i][1]) {
        return ZIP_RANGES[i][2];
      }
    }
    return null;
  }

  /* ZIP search forms: jump to the matching state page. */
  document.querySelectorAll("form[data-zip-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var input = form.querySelector("input[data-zip-input]");
      var msg = form.querySelector("[data-zip-msg]");
      var slug = stateForZip(input.value);
      if (slug) {
        window.location.href = "states/" + slug + ".html";
      } else if (msg) {
        msg.textContent = "Hmm, we couldn't match that zip — try choosing your state from the list.";
        msg.hidden = false;
        input.focus();
      }
    });
  });

  /* States index: live search filter. */
  var search = document.getElementById("state-search");
  var grid = document.getElementById("states-grid");
  var statesCollapse = document.getElementById("states-collapse");
  if (search && grid) {
    search.addEventListener("input", function () {
      var q = search.value.trim().toLowerCase();
      var visible = 0;
      grid.querySelectorAll(".state-link").forEach(function (a) {
        var hit = a.dataset.name.toLowerCase().indexOf(q) !== -1;
        a.style.display = hit ? "" : "none";
        if (hit) visible++;
      });
      var empty = document.getElementById("states-empty");
      if (empty) empty.style.display = visible ? "none" : "";
      /* The state list is folded by default (Option A): open it when the
         filter matches something, so results are visible. */
      if (q && visible && statesCollapse) statesCollapse.open = true;
    });
  }

  /* Mobile nav toggle. */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
  }

  /* Quick exit: immediately leave for a neutral page (safety feature). */
  document.querySelectorAll("[data-quick-exit]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      window.location.replace("https://www.google.com/");
    });
  });

  /* Deep links: some mobile browsers land at the top instead of the anchor
     when the page is still settling (fonts, translate widget). Once the
     page has loaded, scroll to the fragment target again so the link
     lands where it should. Harmless when the browser already got it right. */
  function scrollToFragment() {
    var id = window.location.hash ? window.location.hash.slice(1) : "";
    if (!id) return;
    var el = document.getElementById(decodeURIComponent(id));
    if (el) el.scrollIntoView();
  }
  window.addEventListener("load", function () {
    setTimeout(scrollToFragment, 150);
  });

  /* Footer year. */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* Language picker: drive Google Translate via the googtrans cookie. */
  var langSel = document.getElementById("lang-select");
  if (langSel) {
    try {
      var gm = document.cookie.match(/(?:^|;)\s*googtrans=\/en\/([a-zA-Z-]+)/);
      langSel.value = (gm && gm[1]) ? gm[1] : "";
    } catch (e) {}
    langSel.addEventListener("change", function () {
      var lang = this.value || "en";
      var c = "googtrans=/en/" + lang;
      var host = location.hostname.replace(/^www\./, "");
      document.cookie = c + ";path=/";
      document.cookie = c + ";path=/;domain=." + host;
      try { location.hash = "googtrans(en/" + lang + ")"; } catch (e) {}
      location.reload();
    });
  }

  /* Translation note: Google fills in long pages progressively as you scroll.
     Show a one-time hint per session while a translation is active. */
  try {
    var tgm = document.cookie.match(/(?:^|;)\s*googtrans=\/en\/([a-zA-Z-]+)/);
    var tActive = tgm && tgm[1] && tgm[1] !== "en";
    if (tActive && !sessionStorage.getItem("lb-trans-note")) {
      sessionStorage.setItem("lb-trans-note", "1");
      var tnote = document.createElement("div");
      tnote.className = "trans-note";
      tnote.textContent = "Translating this page \u2014 scroll down and each section flips over as you go.";
      document.body.appendChild(tnote);
      tnote.addEventListener("click", function () { tnote.remove(); });
      setTimeout(function () { tnote.classList.add("show"); }, 800);
      setTimeout(function () {
        tnote.classList.remove("show");
        setTimeout(function () { tnote.remove(); }, 600);
      }, 8000);
    }
  } catch (e) {}

  /* Share this page: native share sheet on mobile, fallback menu on desktop.
     Plain share-intent links only — no third-party SDKs, no trackers.
     The share block is rendered in the page HTML; this fills in the current
     page's share URLs and wires up the button/menu. If a page has no block
     (e.g. an older cached copy), build one exactly like the static markup. */
  try {
    var pageUrl = location.href.split("#")[0];
    var pageTitle = document.title || "The Legal Buffet";
    var encUrl = encodeURIComponent(pageUrl);
    var encTitle = encodeURIComponent(pageTitle);

    var block = document.querySelector("[data-share-block]");
    if (!block) {
      var footerBrand = document.querySelector(".site-footer .footer-brand");
      if (footerBrand) {
        block = document.createElement("div");
        block.className = "share-block";
        block.setAttribute("data-share-block", "1");
        block.innerHTML =
          '<p class="share-label">Know someone who could use this? Pass it on.</p>' +
          '<button type="button" class="btn btn-primary btn-share" data-share-btn>' +
          '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.6" y1="10.5" x2="15.4" y2="6.5"/><line x1="8.6" y1="13.5" x2="15.4" y2="17.5"/></svg>' +
          "Share this page</button>" +
          '<div class="share-menu" data-share-menu hidden>' +
          '<a data-share-fb target="_blank" rel="noopener">Facebook</a>' +
          '<a data-share-x target="_blank" rel="noopener">X</a>' +
          '<a data-share-email>Email</a>' +
          '<button type="button" data-copy-link>Copy link</button>' +
          "</div>" +
          '<p class="share-copied" data-share-copied hidden>Link copied.</p>';
        footerBrand.appendChild(block);
      }
    }

    if (block) {
      /* Fill in the share URLs (the static block ships without hrefs). */
      var fbLink = block.querySelector("[data-share-fb]");
      if (fbLink) fbLink.href = "https://www.facebook.com/sharer/sharer.php?u=" + encUrl;
      var xLink = block.querySelector("[data-share-x]");
      if (xLink) xLink.href = "https://twitter.com/intent/tweet?url=" + encUrl + "&text=" + encTitle;
      var emailLink = block.querySelector("[data-share-email]");
      if (emailLink) emailLink.href = "mailto:?subject=" + encTitle + "&body=" + encUrl;

      var shareBtn = block.querySelector("[data-share-btn]");
      var shareMenu = block.querySelector("[data-share-menu]");
      var copiedMsg = block.querySelector("[data-share-copied]");

      function showCopied() {
        copiedMsg.hidden = false;
        setTimeout(function () { copiedMsg.hidden = true; }, 2500);
      }

      shareBtn.addEventListener("click", function () {
        if (navigator.share) {
          navigator.share({ title: pageTitle, url: pageUrl }).catch(function () {});
        } else {
          shareMenu.hidden = !shareMenu.hidden;
        }
      });

      document.addEventListener("click", function (ev) {
        if (!shareMenu.hidden && !block.contains(ev.target)) shareMenu.hidden = true;
      });

      block.querySelector("[data-copy-link]").addEventListener("click", function () {
        function done() { shareMenu.hidden = true; showCopied(); }
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(pageUrl).then(done, function () { fallbackCopy(); });
        } else { fallbackCopy(); }
        function fallbackCopy() {
          var ta = document.createElement("textarea");
          ta.value = pageUrl;
          ta.style.position = "fixed"; ta.style.opacity = "0";
          document.body.appendChild(ta); ta.select();
          try { document.execCommand("copy"); } catch (e) {}
          document.body.removeChild(ta); done();
        }
      });
    }
  } catch (e) {}
})();

/* Letter templates: copy/print one letter (added 2026-10-28). Nothing is stored or sent. */
(function () {
  "use strict";
  document.querySelectorAll("[data-copy-letter]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var letter = btn.closest(".letter");
      var body = letter && letter.querySelector(".letter-body");
      if (!body) return;
      var text = body.innerText || body.textContent;
      var done = function () { var t = btn.textContent; btn.textContent = "Copied!"; setTimeout(function () { btn.textContent = t; }, 2000); };
      if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(text).then(done, function () {}); }
    });
  });
  document.querySelectorAll("[data-print-letter]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var letter = btn.closest(".letter");
      if (!letter) return;
      document.body.classList.add("printing-letter");
      letter.classList.add("letter-print-target");
      var cleanup = function () { document.body.classList.remove("printing-letter"); letter.classList.remove("letter-print-target"); window.removeEventListener("afterprint", cleanup); };
      window.addEventListener("afterprint", cleanup);
      window.print();
    });
  });
})();
