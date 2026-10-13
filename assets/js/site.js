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
  var READY = { minnesota: true, wisconsin: true, iowa: true, "north-dakota": true, "south-dakota": true, illinois: true, california: true, texas: true, florida: true, "new-york": true, michigan: true, pennsylvania: true, ohio: true, georgia: true, "north-carolina": true, "new-jersey": true, virginia: true, washington: true, arizona: true, massachusetts: true, tennessee: true, maryland: true, colorado: true, "south-carolina": true, alabama: true, louisiana: true };

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

  /* States index: live search filter. */
  var search = document.getElementById("state-search");
  var grid = document.getElementById("states-grid");
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
    });
  }

  /* Mobile nav toggle. */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* Quick exit: immediately leave for a neutral page (safety feature). */
  document.querySelectorAll("[data-quick-exit]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      window.location.replace("https://www.google.com/");
    });
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
      if (gm && gm[1]) langSel.value = gm[1];
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
})();
