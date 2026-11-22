#!/usr/bin/env python3
"""Verify the Phase 1 pilot (timeshare-exit split) before it ships.

Checks, all against the main branch as the baseline:
1. New pages: 50 exist; h1 text+id; self-canonical; og:url; title/description
   naming the state; 3-level breadcrumbs; 5 cards; window + sources lines;
   footer / quick-exit / emergency strip present; every relative link resolves
   to a file that exists; no one-level ../ paths.
2. Hub pages: stub present; timeshare section content gone; all other h2 ids
   intact; div balance unchanged vs main; text-token diff vs main is exactly
   the removed section (minus stub/script tokens); contents li points at the
   new page; anchor-catch script present with the right hash + destination.
3. Search index: still 12,028 entries, valid schema; the 50 timeshare entries
   point at the new pages (u=new, a='', p=new title); no old timeshare anchors.
4. Search behaviour (real search.js code, run in node): prefix/curPage/urlFor
   correct at root, hub, and split-page depths; ranking for timeshare queries
   puts the new pages on top.
5. Helper (real helperUrl code, run in node): all topics x all states — only
   timeshare-exit destinations changed vs the old logic.
6. Anchor-catch (real script from 3 hub pages, run in node): matching hash
   redirects to '/states/<state>/timeshare-exit/', anything else does not.
7. Sitemaps: sitemap.xml is an index listing 51 sitemaps; every per-state
   sitemap lists its new page; sitemap-pages.xml lists the original 60;
   robots.txt still points at sitemap.xml.
8. search.js parses (node --check).

Exit 0 only if every check passes. Run from the site repo root.
"""
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAIL = []


def check(name, ok, detail=""):
    print(("  PASS " if ok else "  FAIL ") + name + (f" — {detail}" if detail else ""))
    if not ok:
        FAIL.append(name + (f": {detail}" if detail else ""))


def tokens(t):
    return sorted(re.sub(r'<[^>]+>', ' ', t).split())


def git_main(path):
    return subprocess.run(['git', 'show', f'main:{path}'],
                          capture_output=True, text=True, cwd=ROOT).stdout


def main():
    data = json.loads((ROOT / "hidden_files" / "topic-research" / "timeshare-exit" / "all-states.json").read_text())
    slugs = sorted(data[k].get("slug") or k.replace(" ", "-") for k in data)
    assert len(slugs) == 50

    # ---------- 1. new pages ----------
    new_ok = 0
    for slug in slugs:
        state = data[slug]["state"]
        p = ROOT / "states" / slug / "timeshare-exit" / "index.html"
        if not p.exists():
            check(f"new page {slug}", False, "missing")
            continue
        t = p.read_text()
        canon = f"https://thelegalbuffet.com/states/{slug}/timeshare-exit/"
        title = f"Timeshare Exit in {state} — The Legal Buffet"
        problems = []
        if f'<h1 id="timeshare-exit-in-{slug}">Timeshare exit in {state}</h1>' not in t:
            problems.append("h1")
        if f'<link rel="canonical" href="{canon}">' not in t:
            problems.append("canonical")
        if f'<meta property="og:url" content="{canon}">' not in t:
            problems.append("og:url")
        if f'<title>{title}</title>' not in t:
            problems.append("title")
        if 'name="description" content="Timeshare exit in ' + state not in t:
            problems.append("description")
        dm = re.search(r'<meta name="description" content="([^"]*)">', t)
        om = re.search(r'<meta property="og:description" content="([^"]*)">', t)
        if not dm or len(dm.group(1)) > 160:
            problems.append("description >160")
        if not om or (dm and om.group(1) != dm.group(1)):
            problems.append("og:description mismatch")
        if f'<a href="../../../">Home</a> &rsaquo; <a href="../../{slug}.html">{state}</a> &rsaquo; Timeshare exit</p>' not in t:
            problems.append("breadcrumbs")
        if len(re.findall(r'<h3>', t)) != 6:  # 5 section cards + related card
            problems.append(f"h3 count {len(re.findall(r'<h3>', t))}")
        if '<strong>Cooling-off window:</strong>' not in t:
            problems.append("window line")
        if 'checked November 20, 2026' not in t:
            problems.append("sources line")
        if 'class="site-footer"' not in t or 'data-quick-exit' not in t or 'lb-emergency' not in t:
            problems.append("shell")
        if re.search(r'"\.\/(?!\.\/)', t):
            problems.append("one-level path")
        if t.count('<div') != t.count('</div>'):
            problems.append("div imbalance")
        # every relative link must resolve to an existing file
        bad_links = []
        for m in set(re.findall(r'(?:href|src)="([^"#][^"]*)"', t)):
            if m.startswith(('http', 'mailto:', 'tel:', 'data:')):
                continue
            clean = m.split('#')[0].split('?')[0]
            if not clean:
                continue
            target = (p.parent / clean).resolve()
            if clean.endswith('/'):
                target = target / 'index.html'
            if not target.exists():
                bad_links.append(m)
        if bad_links:
            problems.append(f"unresolved links {bad_links[:3]}")
        if problems:
            check(f"new page {slug}", False, ", ".join(problems))
        else:
            new_ok += 1
    check("new pages 50/50", new_ok == 50, f"{new_ok}/50 clean")

    # ---------- 2. hub pages ----------
    hub_ok = 0
    for slug in slugs:
        state = data[slug]["state"]
        new = (ROOT / "states" / f"{slug}.html").read_text()
        old = git_main(f"states/{slug}.html")
        problems = []
        if f'Timeshare exit in {state} now has its own page: <a href="/states/{slug}/timeshare-exit/">read the full guide &rarr;</a>' not in new:
            problems.append("stub link")
        if f'href="/states/{slug}/timeshare-exit/"' not in new:
            problems.append("contents li")
        if 'The cooling-off window: your best exit' in new:
            problems.append("section content still present")
        if f"'#timeshare-exit-in-{slug}': '/states/{slug}/timeshare-exit/'" not in new:
            problems.append("catch script")
        # Resolve the hub's timeshare links against the hub's REAL url
        # (states/<slug>.html, base /states/) — a bare 'timeshare-exit/'
        # would land on /states/timeshare-exit/ and 404 (bug found live
        # 2026-11-22). Absolute paths must survive urljoin unchanged.
        from urllib.parse import urljoin
        base = f"https://thelegalbuffet.com/states/{slug}.html"
        want = f"https://thelegalbuffet.com/states/{slug}/timeshare-exit/"
        for href in re.findall(r'href="([^"]*timeshare-exit/[^"]*)"', new):
            if urljoin(base, href) != want:
                problems.append(f"hub link resolves wrong: {href}")
        m = re.search(r"'#timeshare-exit-in-" + re.escape(slug) + r"': '([^']+)'", new)
        if not m or urljoin(base, m.group(1)) != want:
            problems.append("catch dest resolves wrong")
        old_h2 = set(re.findall(r'<h2 id="([^"]+)">', old))
        new_h2 = set(re.findall(r'<h2 id="([^"]+)">', new))
        # On the old hub the timeshare id lives on the <section> tag, not the h2;
        # the stub puts it on its h2, so the new hub gains exactly that one id.
        if new_h2 != old_h2 | {f'timeshare-exit-in-{slug}'}:
            problems.append(f"h2 ids differ: lost {sorted(old_h2 - new_h2)[:2]} gained {sorted(new_h2 - old_h2)[:2]}")
        if new.count('<h2') != old.count('<h2'):
            problems.append("h2 count changed")
        if new.count('<div') - new.count('</div>') != old.count('<div') - old.count('</div>'):
            problems.append("div balance vs main")
        # token diff must come only from the removed section / added stub+script
        lost = Counter(tokens(old)) - Counter(tokens(new))
        gained = Counter(tokens(new)) - Counter(tokens(old))
        sec = re.search(r'<section class="block"[^>]*>\s*<h2 id="timeshare-exit-in-'
                        + re.escape(slug) + r'".*?</section>', old, re.DOTALL).group(0)
        stub = re.search(r'<section class="block"[^>]*>\s*<h2 id="timeshare-exit-in-'
                         + re.escape(slug) + r'".*?</section>', new, re.DOTALL).group(0)
        script = re.search(r'<script>\n/\* Split-pages pilot.*?</script>', new, re.DOTALL).group(0)
        old_script = re.search(r'<script>\n/\* Split-pages pilot.*?</script>', old, re.DOTALL).group(0)
        allowed_lost = Counter(tokens(sec)) + Counter(tokens(old_script))
        allowed_gained = Counter(tokens(stub)) + Counter(tokens(script))
        extra_lost = [k for k in lost if lost[k] > allowed_lost.get(k, 0)]
        extra_gained = [k for k in gained if gained[k] > allowed_gained.get(k, 0)]
        if extra_lost:
            problems.append(f"unexpected lost tokens {extra_lost[:5]}")
        if extra_gained:
            problems.append(f"unexpected gained tokens {extra_gained[:5]}")
        if problems:
            check(f"hub {slug}", False, ", ".join(problems))
        else:
            hub_ok += 1
    check("hub pages 50/50", hub_ok == 50, f"{hub_ok}/50 clean")

    # ---------- 3. search index ----------
    idx = json.loads((ROOT / "assets" / "search-index.json").read_text())
    check("index size 12028", len(idx) == 12028, f"got {len(idx)}")
    check("index schema", all(set(e.keys()) == {"p", "u", "a", "h", "t"} for e in idx))
    te = [e for e in idx if e.get("u", "").endswith("/timeshare-exit/")]
    check("index timeshare entries 50", len(te) == 50, f"got {len(te)}")
    check("index no old timeshare anchors",
          not any(e.get("a", "").startswith("timeshare-exit-in-") for e in idx))
    check("index timeshare entries shape",
          all(e["a"] == "" and e["h"].startswith("Timeshare exit in ")
              and e["p"].startswith("Timeshare Exit in ") for e in te))
    # ---------- 4. search.js behaviour (real code, run in node) ----------
    node_search(slugs)
    # ---------- 5. helper (real helperUrl, run in node) ----------
    node_helper()
    # ---------- 6. anchor-catch (real script from 3 hub pages, run in node) ----------
    node_anchor_catch()
    # ---------- 7. sitemaps ----------
    sitemap_checks(slugs)
    # ---------- 8. search.js parses ----------
    r = subprocess.run(['node', '--check', str(ROOT / 'assets' / 'js' / 'search.js')],
                       capture_output=True, text=True)
    check("search.js parses (node --check)", r.returncode == 0, r.stderr.strip()[:200])

    # probe temp files are throwaway; don't leave them in the tree
    for tmp in (ROOT / "hidden_files").glob("_verify_*.js"):
        tmp.unlink()

    print("DONE part 1" if not FAIL else "PART 1 FAILURES: " + "; ".join(FAIL))
    return 0 if not FAIL else 1


def extract_fn(src, name):
    """Extract `function name(...) {...}` by brace counting (regexes truncate)."""
    i = src.index(f"function {name}(")
    j = src.index("{", i)
    depth = 0
    for k in range(j, len(src)):
        if src[k] == "{":
            depth += 1
        elif src[k] == "}":
            depth -= 1
            if depth == 0:
                return src[i:k + 1]
    raise AssertionError(f"unbalanced braces in {name}")


def node_search(slugs):
    js = (ROOT / "assets" / "js" / "search.js").read_text()
    norm = extract_fn(js, "norm")
    load = extract_fn(js, "load")
    score = extract_fn(js, "score")
    run_search = extract_fn(js, "runSearch")
    url_for = extract_fn(js, "urlFor")
    page_file = extract_fn(js, "pageFile")
    lines = js.splitlines(keepends=True)
    start = next(i for i, l in enumerate(lines) if l.strip().startswith("var pathParts"))
    end = next(i for i, l in enumerate(lines) if l.strip().startswith("var curPage"))
    prefix_block = "".join(lines[start:end + 1])
    snippets = "\n".join([page_file, prefix_block, "var index = null;",
                          norm, load, score, run_search, url_for])
    probe = r"""
const fs = require('fs');
const IDX = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const SNIPPETS = fs.readFileSync(process.argv[3], 'utf8');
function fetch(url) { return Promise.resolve({ json: () => Promise.resolve(IDX) }); }
const CASES = {
  '/': [
    [{u: 'index.html', a: 'helper'}, '#helper'],
    [{u: 'states/minnesota.html', a: 'timeshare-exit-in-minnesota'}, 'states/minnesota.html#timeshare-exit-in-minnesota'],
    [{u: 'states/minnesota/timeshare-exit/', a: ''}, 'states/minnesota/timeshare-exit/'],
  ],
  '/states/minnesota.html': [
    [{u: 'states/minnesota/timeshare-exit/', a: ''}, '../states/minnesota/timeshare-exit/'],
    [{u: 'states/minnesota.html', a: 'divorce-in-minnesota'}, '#divorce-in-minnesota'],
    [{u: 'states/texas/timeshare-exit/', a: ''}, '../states/texas/timeshare-exit/'],
  ],
  '/states/minnesota/timeshare-exit/': [
    [{u: 'states/minnesota/timeshare-exit/', a: ''}, './'],
    [{u: 'states/minnesota.html', a: 'divorce-in-minnesota'}, '../../../states/minnesota.html#divorce-in-minnesota'],
    [{u: 'states/texas/timeshare-exit/', a: ''}, '../../../states/texas/timeshare-exit/'],
    [{u: 'index.html', a: ''}, '../../../index.html'],
  ],
};
(async () => {
  let fails = 0;
  for (const [pathname, cases] of Object.entries(CASES)) {
    const loc = { pathname };
    const fns = eval(SNIPPETS.replace(/location\.pathname/g, 'loc.pathname') +
      '\n;({ urlFor, runSearch })');
    for (const [entry, want] of cases) {
      const got = fns.urlFor(entry);
      if (got !== want) { console.log('URLFAIL ' + pathname + ' ' + JSON.stringify(entry) + ' -> ' + got + ' want ' + want); fails++; }
    }
    const r1 = await fns.runSearch('timeshare exit minnesota');
    if (!r1.length || r1[0].e.u !== 'states/minnesota/timeshare-exit/') {
      console.log('RANKFAIL ' + pathname + ' top=' + (r1[0] ? r1[0].e.u : 'none')); fails++;
    }
    const r2 = await fns.runSearch('timeshare');
    if (!r2.slice(0, 10).every(x => x.e.u.endsWith('/timeshare-exit/'))) {
      console.log('RANKFAIL ' + pathname + ' timeshare top10'); fails++;
    }
    const firstUrl = r1.length ? fns.urlFor(r1[0].e) : '';
    console.log(pathname + ' top-url=' + firstUrl);
  }
  console.log(fails === 0 ? 'SEARCHJS OK' : 'SEARCHJS FAILS ' + fails);
  process.exit(fails === 0 ? 0 : 1);
})().catch(e => { console.log('PROBE ERROR ' + e.message); process.exit(2); });
"""
    (ROOT / "hidden_files" / "_verify_search_probe.js").write_text(probe)
    (ROOT / "hidden_files" / "_verify_search_snippets.js").write_text(snippets + "\n")
    r = subprocess.run(['node', str(ROOT / "hidden_files" / "_verify_search_probe.js"),
                        str(ROOT / "assets" / "search-index.json"),
                        str(ROOT / "hidden_files" / "_verify_search_snippets.js")],
                       capture_output=True, text=True)
    print(r.stdout.strip())
    check("search.js node simulation", r.returncode == 0, r.stderr.strip()[:300] or r.stdout.strip()[:200])



def node_helper():
    # Test the CURRENT helperUrl directly (no baseline: main already has the
    # pilot, so an old-vs-new diff can no longer show the change). For every
    # topic option x every state, the destination must follow helperUrl's
    # rules: exact-anchor topics to states/<s>.html#<exact>, split topics to
    # states/<s>/<slug>/, the rest to states/<s>.html#<slug>-in-<s>.
    html = (ROOT / "index.html").read_text()
    m = re.search(r'var SPLIT_TOPICS = \{[^}]*\};\s*\n\s*function helperUrl\(topicOpt, stateSlug\) \{[\s\S]*?\n  \}', html)
    if not m:
        check("helperUrl extract", False)
        return
    (ROOT / "hidden_files" / "_verify_helper_new.js").write_text(
        m.group(0) + "\nmodule.exports = helperUrl;\n")
    # options from the helper select
    opts = re.findall(r'<option value="([^"]+)"(?: data-anchor="([^"]+)")?(?: data-anchor-exact="([^"]+)")?', html)
    script = r'''
const newFn = require(process.argv[2]);
const opts = JSON.parse(process.argv[3]);
const states = JSON.parse(process.argv[4]);
function opt(o) { return { getAttribute: n => n === 'data-anchor' ? (o[1] || null) : n === 'data-anchor-exact' ? (o[2] || null) : null }; }
let split = 0, bad = [];
for (const o of opts) for (const s of states) {
  const b = newFn(opt(o), s);
  const want = o[2] ? 'states/' + s + '.html#' + o[2]
    : o[1] === 'timeshare-exit' ? 'states/' + s + '/timeshare-exit/'
    : o[1] ? 'states/' + s + '.html#' + o[1] + '-in-' + s
    : 'states/' + s + '.html';
  if (o[1] === 'timeshare-exit') split++;
  if (b !== want) bad.push([o[0], s, b, want]);
}
console.log('HELPER split=' + split + ' bad=' + bad.length);
if (bad.length) console.log(JSON.stringify(bad.slice(0, 5)));
process.exit(split === 50 && bad.length === 0 ? 0 : 1);
'''
    (ROOT / "hidden_files" / "_verify_helper_probe.js").write_text(script)
    # state slugs from the helper's JS state list (the select is JS-populated)
    states = sorted(set(re.findall(r'\["[^"]+", "([a-z-]+)"\]', html)))
    assert len(states) == 50, f"state list has {len(states)} entries"
    r = subprocess.run(['node', str(ROOT / "hidden_files" / "_verify_helper_probe.js"),
                        str(ROOT / "hidden_files" / "_verify_helper_new.js"),
                        json.dumps(opts),
                        json.dumps(states)],
                       capture_output=True, text=True)
    print(r.stdout.strip())
    check("helper simulation: only timeshare-exit split (50 states)", r.returncode == 0,
          r.stderr.strip()[:200] or r.stdout.strip()[:300])


def node_anchor_catch():
    script = r'''
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const m = html.match(/<script>\n\/\* Split-pages pilot[\s\S]*?<\/script>/);
if (!m) { console.log('NO CATCH SCRIPT'); process.exit(2); }
const code = m[0].replace(/^<script>/, '').replace(/<\/script>$/, '');
function run(hash) {
  let dest = null;
  const window = { location: { hash, replace: d => { dest = d; } } };
  eval(code);
  return dest;
}
const slug = process.argv[3];
const good = run('#timeshare-exit-in-' + slug) === '/states/' + slug + '/timeshare-exit/';
const noOther = run('#divorce-in-' + slug) === null && run('') === null;
console.log(slug + ' match=' + good + ' other=' + noOther);
process.exit(good && noOther ? 0 : 1);
'''
    (ROOT / "hidden_files" / "_verify_catch_probe.js").write_text(script)
    ok = True
    for slug in ("minnesota", "texas", "wyoming"):
        r = subprocess.run(['node', str(ROOT / "hidden_files" / "_verify_catch_probe.js"),
                            str(ROOT / "states" / f"{slug}.html"), slug],
                           capture_output=True, text=True)
        print("  " + r.stdout.strip())
        if r.returncode != 0:
            ok = False
    check("anchor-catch simulation (MN, TX, WY)", ok)


def sitemap_checks(slugs):
    NS = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    try:
        idx = ET.parse(ROOT / "sitemap.xml").getroot()
        smaps = [e.find('sm:loc', NS).text for e in idx.findall('sm:sitemap', NS)]
        check("sitemap.xml is an index of 51", len(smaps) == 51, f"got {len(smaps)}")
        check("sitemap index lists sitemap-pages.xml",
              'https://thelegalbuffet.com/sitemap-pages.xml' in smaps)
        missing = [s for s in slugs if f'https://thelegalbuffet.com/sitemap-{s}.xml' not in smaps]
        check("sitemap index lists all 50 per-state sitemaps", not missing, str(missing[:3]))
        pages = ET.parse(ROOT / "sitemap-pages.xml").getroot()
        locs = [e.find('sm:loc', NS).text for e in pages.findall('sm:url', NS)]
        check("sitemap-pages.xml lists original 60", len(locs) == 60, f"got {len(locs)}")
        check("sitemap-pages.xml has no split pages",
              not any('/timeshare-exit/' in u for u in locs))
        bad = []
        for s in slugs:
            doc = ET.parse(ROOT / f"sitemap-{s}.xml").getroot()
            urls = [e.find('sm:loc', NS).text for e in doc.findall('sm:url', NS)]
            if urls != [f'https://thelegalbuffet.com/states/{s}/timeshare-exit/']:
                bad.append(s)
        check("per-state sitemaps list their new page", not bad, str(bad[:3]))
    except ET.ParseError as e:
        check("sitemaps parse as XML", False, str(e))
    robots = (ROOT / "robots.txt").read_text() if (ROOT / "robots.txt").exists() else ""
    check("robots.txt still points at sitemap.xml", "sitemap.xml" in robots)


def esc(s):
    import html as htmlmod
    return htmlmod.escape(s or "", quote=True)


if __name__ == "__main__":
    sys.exit(main())
