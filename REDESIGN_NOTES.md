# Son Redesign Preview — Notes

**Branch:** `son-redesign-preview` (isolated worktree; `main` untouched, never pushed)
**Basis:** the son's "MASTER PROMPT — THE LEGAL BUFFET COMPLETE UI/UX OVERHAUL"
(Phase 1 audit spirit + Phase 2 presentation-only redesign), applied within Craig's
constraint: **navy-and-gold branding is kept exactly as-is.**

**Safety verification:** an automated diff of every `id`, `href`, `src`, `for`,
`aria-labelledby`, `data-anchor`, and `data-topic` across all 59 pages shows
**zero changes** — every route, URL, anchor, link destination, and JS hook is
identical to `main`. No JavaScript files were modified. No content text was changed.

---

## What changed, per page family

### Homepage (`index.html`)
- **Hero restructure:** the 8 featured topic cards were sitting *inside* the
  `.state-picker` flex container (select + button + cards all as flex children).
  They now live in their own `.topics-grid.hero-topics` grid with tighter,
  hero-appropriate card sizing — the state picker is just the select + button again.
- **Hero rhythm:** clearer spacing between hero sub-blocks (picker → cards →
  helper → trust note).
- **Headline bug fixed:** `.hero h1 em` ("shouldn't be a secret.") was rendering
  in near-black navy (`--accent-dark`) on the dark navy hero — effectively
  invisible. It now renders in gold as originally intended.
- **Guided helper:** gold top-border for brand tie-in, roomier fields, and the
  submit button is full-width on phones (thumb-friendly) while staying
  auto-width on desktop.

### All 32 topic cards (site-wide)
- **Hover refinement:** image gently zooms, a gold underline sweeps in along the
  card's bottom edge, and the "Explore →" link deepens to navy. Calm, not flashy.
- Card banners, titles, copy, and destinations are untouched.

### State guides (`states/*.html` — all 50)
- **"What to do next" is now a distinct action block:** all 750 instances were
  wrapped in `.next-steps` — a warm gold-tinted card with a gold left rule and
  an uppercase kicker label. This is the site's core promise ("okay, so what do
  I do?") and it now *looks* like the most important thing on the page.
- **Consistent section rhythm:** sections previously alternated between
  `padding-block: 0` and `padding-block: 0 2.5rem` inline styles, giving uneven
  rhythm down these very long pages. All guide sections now get even 2.5rem
  rhythm with a hairline separator between topics.
- **Scannable section headers:** every topic `h2` gets a short gold rule above
  it — on a 29-section page, the eye can now hop topic to topic.
- **Topic menu:** gold top-border tying it to the brand; pills and behavior unchanged.

### Checklists (`checklists.html`)
- Inherits the guide-section rhythm, gold h2 rules, and separators automatically.
- Print buttons and print stylesheet untouched.

### Class Actions (`class-actions.html`)
- Same inherited section rhythm and header treatment. Content and links untouched.

### Constitution (`constitution.html`)
- Long-document rhythm: article/amendment headings get the gold rule treatment
  plus generous top spacing and hairline separators, so the document scans like
  chapters instead of one wall of text.

### Global
- `::selection` is now a soft gold tint (brand-consistent text highlighting).
- Resource cards: subtle border + deeper shadow on hover, editorial feel.
- How-it-works steps: airier padding, slightly larger gold numerals.
- Topic menu, header, footer, search, language picker, Quick Exit, emergency
  banner: visually unchanged apart from the refinements above.

---

## Deliberately left alone

- **Brand colors, banners, graphics:** navy/gold palette, topic-card photo banners,
  and the hero brand graphic are exactly as Craig approved.
- **All links, routes, anchors, and JS behavior:** verified identical to `main`
  (see safety check above). Search, helper logic, state picker, language picker,
  mobile nav, Quick Exit, and print behavior all work as before.
- **All copy:** no headlines, paragraphs, labels, or button text were changed.
- **Sticky in-page nav:** considered for the long state guides (the son's prompt
  calls out in-page navigation), but a 29-pill sticky bar would eat ~200px of
  viewport. Deferred — the gold section rules + topic menu serve scannability
  without it.
- **No new features, pages, or tracking.**

## How to preview

This branch is not deployed. To see it: serve the worktree locally
(e.g. `python3 -m http.server` in the worktree root) or diff
`assets/css/styles.css` against `main` — nearly all changes live there plus the
small `index.html` hero/helper refinements.
