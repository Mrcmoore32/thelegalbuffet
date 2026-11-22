#!/usr/bin/env python3
"""Phase 1 pilot — split timeshare exit into its own page per state.

Reads the design doc's Phase 1 definition:
- URL: /states/<state>/timeshare-exit/  (file states/<state>/timeshare-exit/index.html)
- State pages stay as hubs: the timeshare-exit section is replaced by a stub
  linking to the new page, the contents-list entry points at the new page,
  and an anchor-catch script redirects old #timeshare-exit-in-<state> bookmarks.
- Search index: the 50 timeshare entries get u=new page, a='', p=new title.
- Helper: helperUrl sends timeshare-exit lookups to the new page.
- Sitemaps: sitemap.xml becomes an index over sitemap-pages.xml + 50 per-state
  sitemaps (one new URL each for the pilot).
- No national topic pages, no analytics (both still open questions for Craig).

Source of truth for content is the LIVE state page: the timeshare section is
transplanted verbatim (minus its h2, whose id moves to the new page's h1).
The dataset (hidden_files/topic-research/timeshare-exit/all-states.json) is
used only for the meta description window phrase, and the section regenerated
from it must match the live section exactly or the state is skipped.

Run from the site repo root, on branch pilot/timeshare-exit-split.
Idempotency: refuses to run twice (asserts no new page / stub / script exists).
"""
import html as htmlmod
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "timeshare-exit" / "all-states.json"
STATES_DIR = ROOT / "states"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
INDEX_HTML = ROOT / "index.html"
SEARCH_JS = ROOT / "assets" / "js" / "search.js"
SITEMAP = ROOT / "sitemap.xml"

SLUG = "timeshare-exit"
TITLE = "Timeshare Exit"
SEARCH_JS_VERSION = "20261122a"  # new code for split-page depth; old pages keep 20261113a

ABBR = {'Minn', 'Ala', 'Alaska', 'Ariz', 'Ark', 'Cal', 'Colo', 'Conn', 'Del',
        'Fla', 'Ga', 'Ill', 'Ind', 'Kan', 'Ky', 'La', 'Me', 'Md', 'Mass',
        'Mich', 'Miss', 'Mo', 'Mont', 'Neb', 'Nev', 'N.H', 'N.J', 'N.M',
        'N.Y', 'N.C', 'N.D', 'Okla', 'Or', 'Pa', 'R.I', 'S.C', 'S.D',
        'Tenn', 'Tex', 'Vt', 'Va', 'Wash', 'W.Va', 'Wis', 'Wyo', 'Stat',
        'Rev', 'Code', 'Ch', 'Art', 'U.S', 'No', 'Sec'}


def cap_description(desc, limit=160):
    """Meta descriptions display ~155-160 chars. Keep state + topic + the
    window's lead (always the day-count) and cut at a word boundary."""
    if len(desc) <= limit:
        return desc
    return desc[:limit - 1].rsplit(" ", 1)[0] + "…"


def first_sentence(s):
    """First sentence, without splitting on abbreviations like 'Minn.' or 'A.R.S.'."""
    for m in re.finditer(r'\.\s+(?=[A-Z])', s):
        prev = s[:m.start()].split()
        word = prev[-1].strip('()') if prev else ''
        if word not in ABBR:
            return s[:m.start() + 1]
    return s


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def load_dataset():
    data = json.loads(DATA.read_text())
    assert len(data) == 50, f"dataset has {len(data)} states, expected 50"
    return data


def extract_timeshare_section(text, slug):
    """The live timeshare-exit <section>...</section>, exactly as shipped."""
    m = re.search(
        r'<section class="block"[^>]*>\s*<h2 id="timeshare-exit-in-'
        + re.escape(slug) + r'".*?</section>',
        text, re.DOTALL)
    assert m, f"{slug}: timeshare section not found"
    return m.group(0)


def check_section(state, slug, section):
    """Structural gates: full section, 5 cards, one h2, one id, no leaked markers."""
    assert section.count(f'id="timeshare-exit-in-{slug}"') == 1, f"{slug}: h2 id count"
    assert len(re.findall(r'<h3>', section)) == 5, f"{slug}: h3 count"
    assert section.count('<div') == 5 and section.count('</div>') == 5, f"{slug}: div count"
    assert section.count('<section') == 1, f"{slug}: section count"
    assert 'TODO' not in section and 'FIXME' not in section, f"{slug}: leaked marker"
    assert re.search(r'\bNone\b', section) is None, f"{slug}: leaked None"
    assert '<strong>Cooling-off window:</strong>' in section, f"{slug}: no window line"
    assert 'checked November 20, 2026' in section, f"{slug}: no sources line"


def shell_pieces():
    """Header + footer shell from Alabama (the majority template variant)."""
    text = (STATES_DIR / "alabama.html").read_text()
    s = text.find('<body>')
    e = text.find('</header>', s)
    assert s != -1 and e != -1
    body_top = text[s:e + len('</header>')]
    s = text.find('<footer class="site-footer">')
    e = text.find('</html>', s)
    assert s != -1 and e != -1
    foot = text[s:e + len('</html>')]
    # One level deeper: ../ becomes ../../../ (three levels up to root).
    def deeper(chunk):
        chunk = re.sub(r'((?:href|src)=")\.\./', r'\1../../../', chunk)
        return chunk
    body_top = deeper(body_top)
    foot = deeper(foot)
    # New search.js (depth-aware) on the new pages only.
    foot = foot.replace('search.js?v=20261113a', f'search.js?v={SEARCH_JS_VERSION}')
    assert '../../../assets/js/site.js' in foot, "shell rewrite missed site.js"
    assert f'search.js?v={SEARCH_JS_VERSION}' in foot, "shell rewrite missed search.js"
    assert re.search(r'"\.\/(?!\.\/)', body_top) is None, "shell still has one-level paths"
    assert re.search(r'"\.\/(?!\.\/)', foot) is None, "shell still has one-level paths"
    return body_top, foot


def head_html(state, slug, description):
    """New page <head>, modelled on the state-page head with split-page values."""
    al = (STATES_DIR / "alabama.html").read_text()
    head = al[al.find('<!DOCTYPE html>'):al.find('</head>') + len('</head>')]
    title = f"Timeshare Exit in {state} — The Legal Buffet"
    canon = f"https://thelegalbuffet.com/states/{slug}/timeshare-exit/"
    head = re.sub(r'<title>[^<]*</title>', f'<title>{esc(title)}</title>', head, count=1)
    head = re.sub(r'(<meta name="description" content=")[^"]*(">)',
                  lambda m: m.group(1) + esc(description) + m.group(2), head, count=1)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*(">)',
                  lambda m: m.group(1) + canon + m.group(2), head, count=1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*(">)',
                  lambda m: m.group(1) + esc(title) + m.group(2), head, count=1)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*(">)',
                  lambda m: m.group(1) + esc(description) + m.group(2), head, count=1)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*(">)',
                  lambda m: m.group(1) + canon + m.group(2), head, count=1)
    head = head.replace('../assets/css/styles.css', '../../../assets/css/styles.css', 1)
    assert f'{state} Legal Resources' not in head, "head still has old state title"
    assert f'states/{slug}.html' not in head, "head still has old state canonical"
    assert canon in head and esc(title) in head, "head values missing"
    # BreadcrumbList schema, after the WebSite block.
    crumbs = ('<script type="application/ld+json">\n'
              '{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ['
              '{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://thelegalbuffet.com/"}, '
              '{"@type": "ListItem", "position": 2, "name": "' + esc(state) + '", "item": "https://thelegalbuffet.com/states/' + slug + '.html"}, '
              '{"@type": "ListItem", "position": 3, "name": "Timeshare exit", "item": "' + canon + '"}]}\n'
              '</script>')
    assert '</script>\n</head>' in head, "head script tail not found"
    head = head.replace('</script>\n</head>', '</script>\n' + crumbs + '\n</head>', 1)
    return head


def related_card(state, slug, prev_id, prev_text, next_id, next_text):
    return (
        '<div class="card">\n'
        f'<h3>More help in {esc(state)}</h3>\n'
        f'<p><strong>All topics:</strong> <a href="../../{slug}.html">{esc(state)} legal help — the full guide</a></p>\n'
        f'<p><strong>Previous topic:</strong> <a href="../../{slug}.html#{prev_id}">{prev_text}</a>'
        f' &nbsp;|&nbsp; <strong>Next topic:</strong> <a href="../../{slug}.html#{next_id}">{next_text}</a></p>\n'
        f'<p><strong>Related:</strong> <a href="../../{slug}.html#consumer-protection-in-{slug}">Consumer protection in {esc(state)}</a>'
        f' &middot; <a href="../../{slug}.html#financial-scams-in-{slug}">Financial scams in {esc(state)}</a></p>\n'
        '</div>'
    )


def build_new_page(state, slug, section, description, body_top, foot):
    """Assemble states/<slug>/timeshare-exit/index.html."""
    # The h1 carries the old anchor id; drop the section's h2 line.
    h2_line = re.search(r'<h2 id="timeshare-exit-in-' + re.escape(slug) + r'">.*?</h2>\n?', section)
    assert h2_line, f"{slug}: section h2 line not found"
    body = section[:h2_line.start()] + section[h2_line.end():]
    assert f'id="timeshare-exit-in-{slug}"' not in body, f"{slug}: h2 id still in section"
    h2s = re.findall(r'<h2 id="([^"]+)">', body)
    assert not h2s, f"{slug}: unexpected h2 left in section: {h2s}"
    # Neighbour + related titles from the live hub page.
    hub = (STATES_DIR / f"{slug}.html").read_text()
    all_h2 = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', hub)
    by_id = dict(all_h2)
    prev_id = f"foster-care-youth-aging-out-in-{slug}"
    next_id = f"life-insurance-claim-denials-in-{slug}"
    assert prev_id in by_id and next_id in by_id, f"{slug}: neighbours missing"
    assert f"consumer-protection-in-{slug}" in by_id, f"{slug}: consumer protection missing"
    assert f"financial-scams-in-{slug}" in by_id, f"{slug}: financial scams missing"
    head = head_html(state, slug, description)
    main = (
        '<main id="main">\n'
        '  <div class="wrap">\n'
        '    <div class="page-head">\n'
        f'      <p class="crumbs"><a href="../../../">Home</a> &rsaquo; <a href="../../{slug}.html">{esc(state)}</a> &rsaquo; Timeshare exit</p>\n'
        f'      <h1 id="timeshare-exit-in-{slug}">Timeshare exit in {esc(state)}</h1>\n'
        f'      <p class="lede">How to get out of a timeshare in {esc(state)} — the cooling-off window, deed-back and resale options, and the exit scams to avoid.</p>\n'
        '    </div>\n'
        '\n'
        '    <p class="deadline-notice"><strong>Heads up:</strong> filing deadlines and fees change. Double-check them with your local court before you file.</p>\n'
        f'{body}\n'
        f'{related_card(state, slug, prev_id, by_id[prev_id], next_id, by_id[next_id])}\n'
        '  </div>\n'
        '</main>\n'
    )
    page = head + '\n' + body_top + '\n' + main + '\n' + foot + '\n'
    assert page.count(f'id="timeshare-exit-in-{slug}"') == 1, f"{slug}: anchor id count on new page"
    assert page.count('<div') == page.count('</div>'), f"{slug}: div imbalance on new page"
    assert re.search(r'"\.\/(?!\.\/)', page) is None, f"{slug}: one-level relative path left on new page"
    assert 'timeshare-exit-in-' in page, f"{slug}: anchor text missing"
    return page

def hub_stub(state, slug):
    return (
        '<section class="block" style="padding-block:0 2.5rem">\n'
        f'<h2 id="timeshare-exit-in-{slug}">Timeshare exit in {esc(state)}</h2>\n'
        f'<p>Timeshare exit in {esc(state)} now has its own page: '
        f'<a href="/states/{slug}/timeshare-exit/">read the full guide &rarr;</a></p>\n'
        '</section>'
    )


def anchor_catch_script(slug):
    return (
        '<script>\n'
        '/* Split-pages pilot: timeshare exit moved to its own page. Catch old\n'
        '   #timeshare-exit-in-<state> bookmarks and send the reader on. */\n'
        '(function () {\n'
        f"  var moved = {{ '#timeshare-exit-in-{slug}': '/states/{slug}/timeshare-exit/' }};\n"
        '  var dest = moved[window.location.hash];\n'
        '  if (dest) window.location.replace(dest);\n'
        '})();\n'
        '</script>'
    )


def modify_hub(state, slug, section):
    """Replace the section with a stub, point the contents entry at the new
    page, and add the anchor-catch script. Returns the new hub text."""
    path = STATES_DIR / f"{slug}.html"
    text = path.read_text()
    assert text.count(f'href="#timeshare-exit-in-{slug}"') == 1, f"{slug}: contents href count"
    assert text.count(f'id="timeshare-exit-in-{slug}"') == 1, f"{slug}: h2 id count on hub"
    assert f'/states/{slug}/timeshare-exit/' not in text, f"{slug}: hub already has split links"
    assert 'var moved' not in text, f"{slug}: hub already has catch script"
    # 1. Contents-list entry -> new page.
    text = text.replace(f'href="#timeshare-exit-in-{slug}"', f'href="/states/{slug}/timeshare-exit/"', 1)
    # 2. Section -> stub.
    assert text.count(section) == 1, f"{slug}: live section occurs != 1x on hub"
    text = text.replace(section, hub_stub(state, slug), 1)
    # 3. Anchor-catch script before </body>.
    assert text.count('</body>') == 1, f"{slug}: </body> count"
    text = text.replace('</body>', anchor_catch_script(slug) + '</body>', 1)
    assert text.count(f'id="timeshare-exit-in-{slug}"') == 1, f"{slug}: stub id count"
    assert text.count(f'href="/states/{slug}/timeshare-exit/"') == 2, f"{slug}: new-page links on hub"
    assert text.count(f"'/states/{slug}/timeshare-exit/'") == 1, f"{slug}: catch-script dest count"
    assert text.count('<div') == text.count('</div>'), f"{slug}: div imbalance on hub"
    return text


def rebuild_search_index(data):
    """Regenerate the 50 timeshare entries from the dataset (same construction
    as build_timeshare_exit.state_index_t), with the new p/u/a. The rebuilt
    h/t must match the live index exactly, or the state is skipped."""
    spec = importlib.util.spec_from_file_location(
        "bte", str(ROOT / "hidden_files" / "build_timeshare_exit.py"))
    bte = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bte)
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 12028, f"unexpected index size {len(idx)}"
    targets = [i for i, e in enumerate(idx)
               if e.get("a", "").startswith("timeshare-exit-in-")]
    assert len(targets) == 50, f"timeshare entries found: {len(targets)}"
    skipped = []
    for pos in targets:
        old = idx[pos]
        slug = old["a"][len("timeshare-exit-in-"):]
        e = data.get(slug)
        if e is None:
            skipped.append((slug, "not in dataset"))
            continue
        state = e["state"]
        new = {
            "p": f"Timeshare Exit in {state} — The Legal Buffet",
            "u": f"states/{slug}/timeshare-exit/",
            "a": "",
            "h": f"Timeshare exit in {state}",
            "t": bte.state_index_t(state, slug, e),
        }
        if new["h"] != old["h"] or new["t"] != old["t"]:
            skipped.append((slug, "rebuilt h/t differs from live index"))
            continue
        assert set(new.keys()) == {"p", "u", "a", "h", "t"}
        idx[pos] = new
    assert not any(e.get("a", "").startswith("timeshare-exit-in-") for e in idx), \
        "old timeshare anchors remain"
    assert len(idx) == 12028, "index size changed"
    for e in idx:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    return skipped


def patch_helper():
    """helperUrl: split topics get states/<state>/<slug>/ instead of an anchor."""
    text = INDEX_HTML.read_text()
    old_fn = (
        '  function helperUrl(topicOpt, stateSlug) {\n'
        '    var url = "states/" + stateSlug + ".html";\n'
        '    var exact = topicOpt ? topicOpt.getAttribute("data-anchor-exact") : null;\n'
        '    if (exact) return url + "#" + exact;\n'
        '    var anchor = topicOpt ? (topicOpt.getAttribute("data-anchor") || "") : "";\n'
        '    if (anchor) url += "#" + anchor + "-in-" + stateSlug;\n'
        '    return url;\n'
        '  }'
    )
    assert text.count(old_fn) == 1, "helperUrl not found exactly once"
    new_fn = (
        '  /* Topics with their own page per state (split-pages pilot). Add a slug\n'
        '     here when its topic splits; the helper then links straight to it. */\n'
        '  var SPLIT_TOPICS = { "timeshare-exit": true };\n'
        '\n'
        '  function helperUrl(topicOpt, stateSlug) {\n'
        '    var url = "states/" + stateSlug + ".html";\n'
        '    var exact = topicOpt ? topicOpt.getAttribute("data-anchor-exact") : null;\n'
        '    if (exact) return url + "#" + exact;\n'
        '    var anchor = topicOpt ? (topicOpt.getAttribute("data-anchor") || "") : "";\n'
        '    if (anchor && SPLIT_TOPICS[anchor]) return "states/" + stateSlug + "/" + anchor + "/";\n'
        '    if (anchor) url += "#" + anchor + "-in-" + stateSlug;\n'
        '    return url;\n'
        '  }'
    )
    INDEX_HTML.write_text(text.replace(old_fn, new_fn, 1))
    print("  index.html: helperUrl gains SPLIT_TOPICS (timeshare-exit)")


def patch_search_js():
    """Depth-aware relative prefix + pageFile so search works on split pages
    (3 levels deep) while behaving identically on root and hub pages."""
    text = SEARCH_JS.read_text()
    old_prefix = ("  var prefix = location.pathname.indexOf('/states/') !== -1 ? '../' : '';\n"
                  "  var curPage = location.pathname.split('/').pop() || 'index.html';")
    assert text.count(old_prefix) == 1, "search.js prefix block not found"
    new_prefix = (
        "  /* Relative prefix from the current page back to the site root. Pages live\n"
        "     at the root (0 levels), one level down (states/*.html) or three levels\n"
        "     down (states/<state>/<topic>/ split pages). */\n"
        "  var pathParts = location.pathname.split('/').filter(function (s) { return s !== ''; });\n"
        "  if (pathParts.length && /\\.html?$/.test(pathParts[pathParts.length - 1])) pathParts.pop();\n"
        "  var prefix = pathParts.map(function () { return '../'; }).join('');\n"
        "\n"
        "  /* Last path segment of a page URL; a trailing slash means the directory's\n"
        "     own index page (e.g. 'timeshare-exit' for states/<state>/timeshare-exit/). */\n"
        "  function pageFile(u) {\n"
        "    var p = u.split('/').filter(function (s) { return s !== ''; });\n"
        "    return p.length ? p[p.length - 1] : 'index.html';\n"
        "  }\n"
        "  var curPage = pageFile(location.pathname);"
    )
    text = text.replace(old_prefix, new_prefix, 1)
    old_urlfor = (
        "  function urlFor(e) {\n"
        "    var samePage = e.u.split('/').pop() === curPage;\n"
        "    return samePage\n"
        "      ? (e.a ? '#' + e.a : curPage)\n"
        "      : (prefix + e.u + (e.a ? '#' + e.a : ''));\n"
        "  }"
    )
    assert text.count(old_urlfor) == 1, "search.js urlFor not found"
    new_urlfor = (
        "  function urlFor(e) {\n"
        "    var samePage = pageFile(e.u) === curPage;\n"
        "    return samePage\n"
        "      ? (e.a ? '#' + e.a : (location.pathname.charAt(location.pathname.length - 1) === '/' ? './' : curPage))\n"
        "      : (prefix + e.u + (e.a ? '#' + e.a : ''));\n"
        "  }"
    )
    text = text.replace(old_urlfor, new_urlfor, 1)
    old_boost = "        if (idx[i].e.u.split('/').pop() === curPage) s += 10;"
    assert text.count(old_boost) == 1, "search.js boost line not found"
    text = text.replace(old_boost, "        if (pageFile(idx[i].e.u) === curPage) s += 10;", 1)
    SEARCH_JS.write_text(text)
    print("  assets/js/search.js: depth-aware prefix + pageFile")


def build_sitemaps(state_slugs):
    """sitemap.xml becomes an index over sitemap-pages.xml + 50 per-state sitemaps."""
    current = SITEMAP.read_text()
    locs = re.findall(r'<loc>([^<]+)</loc>', current)
    assert len(locs) == 60, f"sitemap has {len(locs)} locs, expected 60"
    assert not any('/timeshare-exit/' in u for u in locs), "sitemap already lists split pages"
    pages = ('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
             + ''.join(f'  <url><loc>{u}</loc></url>\n' for u in locs)
             + '</urlset>\n')
    (ROOT / "sitemap-pages.xml").write_text(pages)
    for slug in state_slugs:
        (ROOT / f"sitemap-{slug}.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f'  <url><loc>https://thelegalbuffet.com/states/{slug}/timeshare-exit/</loc></url>\n'
            '</urlset>\n')
    index = ('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
             '  <sitemap><loc>https://thelegalbuffet.com/sitemap-pages.xml</loc></sitemap>\n'
             + ''.join(f'  <sitemap><loc>https://thelegalbuffet.com/sitemap-{s}.xml</loc></sitemap>\n'
                       for s in state_slugs)
             + '</sitemapindex>\n')
    SITEMAP.write_text(index)
    print(f"  sitemaps: index + sitemap-pages.xml (60) + 50 per-state sitemaps (1 each)")


def main():
    data = load_dataset()
    body_top, foot = shell_pieces()
    # Import the original builder to cross-check live sections against the dataset.
    spec = importlib.util.spec_from_file_location(
        "bte", str(ROOT / "hidden_files" / "build_timeshare_exit.py"))
    bte = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bte)
    built, skipped = [], []
    for key in sorted(data):
        e = data[key]
        state = e["state"]
        slug = e.get("slug") or key.replace(" ", "-")
        hub_path = STATES_DIR / f"{slug}.html"
        new_path = STATES_DIR / slug / "timeshare-exit" / "index.html"
        if new_path.exists():
            print(f"  SKIP {slug}: new page already exists")
            skipped.append((slug, "new page already exists"))
            continue
        hub_text = hub_path.read_text()
        try:
            section = extract_timeshare_section(hub_text, slug)
            check_section(state, slug, section)
            regen = bte.section_html(state, slug, e).rstrip("\n")
            assert section.rstrip("\n") == regen, "live section differs from dataset rebuild"
            window = first_sentence(e["rescission_period"])
            description = cap_description(
                f"Timeshare exit in {state}: {window} "
                "Deed-back, resale, and exit-scam warnings — verified against official sources.")
            page = build_new_page(state, slug, section, description, body_top, foot)
            new_path.parent.mkdir(parents=True, exist_ok=True)
            new_path.write_text(page)
            hub_path.write_text(modify_hub(state, slug, section))
            built.append(slug)
            print(f"  {slug}: page + hub done")
        except AssertionError as exc:
            print(f"  SKIP {slug}: {exc}")
            skipped.append((slug, str(exc)))
            if new_path.exists():
                new_path.unlink()
    print(f"built: {len(built)}  skipped: {len(skipped)}")
    if skipped:
        print("  skipped states:", skipped)
        print("  STOPPING before index/helper/search/sitemap steps (pilot must be whole)")
        return 1
    skipped_idx = rebuild_search_index(data)
    print(f"  search-index.json: 50 timeshare entries -> new p/u/a (skipped {skipped_idx})")
    patch_helper()
    patch_search_js()
    build_sitemaps([data[k].get("slug") or k.replace(" ", "-") for k in sorted(data)])
    print("DONE — run hidden_files/verify_pilot_timeshare_exit_split.py next")
    return 0


def patch_descriptions():
    """Apply cap_description() to the 50 built pages (both meta tags).
    One-off repair for pages built before the cap existed: asserts the
    on-disk description is exactly the uncapped computation, so the patch
    only truncates, never changes a fact."""
    data = load_dataset()
    changed = 0
    for key in sorted(data):
        e = data[key]
        state = e["state"]
        slug = e.get("slug") or key.replace(" ", "-")
        p = STATES_DIR / slug / "timeshare-exit" / "index.html"
        text = p.read_text()
        window = first_sentence(e["rescission_period"])
        full = (f"Timeshare exit in {state}: {window} "
                "Deed-back, resale, and exit-scam warnings — verified against official sources.")
        capped = cap_description(full)
        for tag in ('<meta name="description" content="', '<meta property="og:description" content="'):
            if capped == full:
                assert text.count(tag + esc(full) + '">') == 1, f"{slug}: description tag not found"
            else:
                assert text.count(tag + esc(full) + '">') == 1, f"{slug}: full description not on page"
                assert text.count(tag + esc(capped) + '">') == 0, f"{slug}: already capped?"
                text = text.replace(tag + esc(full) + '">', tag + esc(capped) + '">', 1)
        assert len(capped) <= 160, f"{slug}: capped description still {len(capped)}"
        assert capped.startswith(f"Timeshare exit in {state}:"), f"{slug}: capped description lost state"
        if capped != full:
            p.write_text(text)
            changed += 1
            print(f"  {slug}: {len(full)} -> {len(capped)}")
    print(f"descriptions capped on {changed} pages")


if __name__ == "__main__":
    sys.exit(main())
