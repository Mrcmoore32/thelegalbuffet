# The Legal Buffet — Phase 1 Audit (read-only)
**Date:** 2026-10-15 · **Scope:** 59 HTML pages + `assets/css/styles.css` + `assets/js/` · **Design frozen:** no visual changes proposed
**Method:** static source inspection (structure, links, anchors, IDs, ARIA, CSS). No live-browser testing. Content/factual verification out of scope (done separately).

**Totals: 14 findings — 1 bug · 3 inconsistencies · 3 UX gaps · 7 accessibility**

---

## (1) Bugs

### B1. "Abortion laws" topic-menu link is dead on all 50 state pages
Every state page's "Pick a topic" menu links to `#abortion-laws-{state}`, but the section's actual ID is `abortion-laws-in-{state}`. Clicking the menu item scrolls nowhere.
- Link: `states/minnesota.html:114` → `<a href="#abortion-laws-minnesota">`
- Actual section: `states/minnesota.html:720` → `<h2 id="abortion-laws-in-minnesota">`
- Affects all 50 `states/*.html` files (verified programmatically: every other one of the 29 menu anchors resolves correctly — this is the only broken one).
- Fix: change the menu href to `#abortion-laws-in-{state}` in all 50 files (or rename the section IDs).

---

## (2) Inconsistencies

### I1. Homepage footer is missing the Constitution page link
The footer "Site" nav on 58 of 59 pages includes `constitution.html`. `index.html`'s footer does not (it lists Home, Start Here, States, About, Checklists, Class Actions, Privacy — no Constitution).
- `index.html` footer nav, ~lines 487–510 (compare `about.html` footer).

### I2. Sitemap omits two public pages
`sitemap.xml` lists 56 URLs. Of the 58 real public pages (59 files minus the Google verification file), `class-actions.html` and `privacy.html` are missing. (`404.html` is correctly excluded.)
- `sitemap.xml` — add both URLs.

### I3. Dead code in shared JS
`assets/js/site.js:25` defines a `READY` object listing only 26 states. It is never referenced anywhere in the file. It is also stale (all 50 states now have content). Harmless but confusing to the next person who reads the code.

---

## (3) UX gaps

### U1. All 32 homepage topic cards lead to the same generic page
Every topic card ("Divorce & Family", "Tax Help", …) links to `states.html`, the states directory — yet the section copy says "Each topic page points you to your state's resources." There are no topic pages, so a visitor who taps "Tax Help" lands on "Pick your state" with no topic context. The guided helper on the same page *does* deep-link to state sections (verified: all 13 helper anchors resolve on all 50 states), so the routing capability exists — the cards just don't use it.
- `index.html`, `.topics-grid` (~lines 155–205).

### U2. Checklists page says "print one out" but offers no way to print
`checklists.html:85` tells visitors to "print one out or pull it up on your phone," and a print stylesheet exists (`assets/css/print.css`, linked `media="print"`), but nothing on the page triggers printing — no button, no link. On phones especially, finding print in the browser menu is non-obvious. A "Print this checklist" button per section (or one at the top) would close the loop.
- `checklists.html:85`; no `window.print()` anywhere in HTML/JS.

### U3. Helper drops 3 topics at the top of the state page
Three helper topics have empty `data-anchor` — Child custody (`index.html:226`), Foreclosure (`:233`), Identity theft (`:234`). Picking one routes to `states/{state}.html` with no anchor, i.e. the top of a very long page, instead of the relevant section. Either add anchors (sections exist for these topics) or route to the closest section.

---

## (4) Accessibility

### A1. No skip-to-content link on any page
No page has a "Skip to main content" link. Keyboard users must tab through the emergency banner, brand, search box, language picker, menu toggle, and nav on every single page load. One link + a `:focus` style (the `:focus-visible` system already exists in `styles.css:45`) would fix it site-wide.

### A2. Search results are invisible to screen readers and keyboard-limited
- `#site-search-results` (`index.html:91`, present on all pages) has no `role`/`aria-live`, so injected results are never announced.
- Results support Enter (jump to top hit) and Escape, but there is no arrow-key navigation through the result list — mouse/touch users can pick any result, keyboard users cannot.
- `assets/js/search.js` (`render`, keydown handler).

### A3. Skipped heading levels in the footer, site-wide
Footer headings "Site" and "National resources" are `<h4>` on all 59 pages while page content tops out at h1–h3 (`index.html:488,500`; same pattern everywhere; `404.html:101,114`; `states.html:156,169`; `checklists.html:271,284`; `privacy.html:132,145`). Screen-reader users navigating by headings hit a level jump. Making them `<h2>`s would be structurally correct.

### A4. Mobile menu button label never updates
`.nav-toggle` (`index.html:120`) keeps `aria-label="Open menu"` permanently; `site.js` toggles `aria-expanded` but not the label, so a screen-reader user hearing "Open menu" while the menu is open gets the wrong instruction.

### A5. Emergency banner uses `role="alert"` on every page
`<div class="lb-emergency" role="alert">` (`index.html:70`, all pages) is announced by screen readers on *every* page load/navigation. Alerts are meant for dynamic, urgent changes; a static banner repeated 59 times becomes noise that trains users to ignore the very emergency numbers it carries. Consider `role="note"` or plain content.

### A6. Helper validation error may not be announced
`#helper-error` (`index.html:254`) is a plain `<p hidden>` toggled by JS with no `role="alert"`, so screen-reader users who submit the helper without picking a topic/state may never hear the error message.

### A7. Small touch targets + overlapping fixed elements (minor)
- Topic-menu pills (`styles.css:442-446`: padding `.45rem .8rem`) render ~32px tall, under the 44px recommended touch target.
- `.trans-note` and `.quick-exit` are both `position: fixed; bottom: ~1rem; z-index: 200` (`styles.css:372,469`) — when a translation is active, the toast can sit on top of the Quick Exit button on narrow screens.

---

## Things checked and found clean
- Exactly one `<h1>`, one `lang` attribute, one viewport meta per page (59/59).
- No duplicate element IDs within any page; no images missing `alt`; no `href="#"` dead links (the one instance is JS-populated); all external links carry `rel="noopener"`.
- All 13 guided-helper anchors resolve on all 50 state pages; all topic-menu anchors resolve except B1; all Constitution/Class Actions/Checklists in-page nav links resolve.
- Header nav identical across all pages (modulo `../` path depth); footer link sets identical except I1.
- Search index (`assets/search-index.json`) is comprehensive: 5,129 entries across 57 pages.
- Text contrast ratios all pass WCAG AA (muted 5.6–6.0:1, body 13.3:1, gold-on-navy 6.3:1, danger button 5.7:1).
- 404 page carries full site chrome (header, nav, search, footer, quick exit).

## Suggested fix order (no design changes required)
1. **B1** — one-line fix × 50 files (scriptable): the only outright broken control on the site.
2. **U1** — point topic cards at `states.html` → state sections, or at minimum the helper; biggest visitor-facing dead end.
3. **I2** — add the two sitemap URLs (Search Console discoverability).
4. **U2** — add print buttons to checklists.
5. **I1** — add the Constitution link to the homepage footer.
6. **A1–A6** — accessibility pass: skip link, search-result live region + arrow keys, footer heading levels, toggle label, alert roles.
7. **U3, I3, A7** — small cleanups when convenient.
