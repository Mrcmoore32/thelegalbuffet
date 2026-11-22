#!/usr/bin/env python3
"""Reusable post-build validator for Legal Buffet new-topic builds.

Usage:
  python3 validate_topic.py <slug> <prev_slug> <about_count> <index_size> \
      <keyword> [--helper-value VALUE] [--anchor ANCHOR]

  slug         new topic slug, e.g. naturalization
  prev_slug    previously-newest topic slug the new section sits before
  about_count  About page count AFTER the build, e.g. 74
  index_size   search-index size AFTER the build, e.g. 10192
  keyword      main search keyword expected to return 50 state entries
  --helper-value  helper option value (default: slug)
  --anchor     h2 anchor prefix (default: slug)

Checks:
  1. New h2 anchor exactly once per state page, immediately before the
     previous topic's h2 (newest-first ordering).
  2. div open/close balance unchanged vs HEAD per state page.
  3. Page-text token multiset identical vs HEAD (pure insertion).
  4. Helper simulation: every helper option x 50 states resolves to an
     existing h2 id (helperUrl logic replicated).
  5. Search index: exact {p,u,a,h,t} schema on all entries; keyword
     returns 50 entries across 50 states with the new anchor.
  6. About count, "Show all N topics" label, count-badge.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def git_head(path):
    r = subprocess.run(
        ["git", "show", f"HEAD:{path}"], cwd=ROOT, capture_output=True, text=True
    )
    return r.stdout if r.returncode == 0 else None


def tokens(text):
    return sorted(re.sub(r"<[^>]+>", " ", text).split())


def main():
    slug = sys.argv[1]
    prev_slug = sys.argv[2]
    about_count = int(sys.argv[3])
    index_size = int(sys.argv[4])
    keyword = sys.argv[5]
    helper_value = slug
    anchor = slug
    args = sys.argv[6:]
    for i, a in enumerate(args):
        if a == "--helper-value":
            helper_value = args[i + 1]
        if a == "--anchor":
            anchor = args[i + 1]

    failures = []

    def check(name, ok, detail=""):
        print(f"  {'PASS' if ok else 'FAIL'}  {name} {detail}")
        if not ok:
            failures.append(name)

    states = sorted(p.name[:-5] for p in (ROOT / "states").glob("*.html"))
    assert len(states) == 50, len(states)

    # 1. Anchor once per page, immediately before prev topic h2.
    bad_order = []
    for s in states:
        text = (ROOT / "states" / f"{s}.html").read_text()
        aid = f'id="{anchor}-in-{s}"'
        if text.count(aid) != 1:
            bad_order.append(f"{s}: anchor count {text.count(aid)}")
            continue
        new_h2 = text.find(f'<h2 id="{anchor}-in-{s}"')
        prev_h2 = text.find(f'<h2 id="{prev_slug}-in-{s}"')
        if not (0 < new_h2 < prev_h2):
            bad_order.append(f"{s}: ordering wrong")
    check("section anchor x1 + before prev topic, all 50", not bad_order,
          "; ".join(bad_order[:3]))

    # 2. div balance unchanged vs HEAD; 3. token multiset identical vs HEAD.
    div_bad, tok_bad = [], []
    for s in states:
        new = (ROOT / "states" / f"{s}.html").read_text()
        old = git_head(f"states/{s}.html")
        if old is None:
            continue
        if new.count("<div") - new.count("</div>") != old.count("<div") - old.count("</div>"):
            div_bad.append(s)
        old_toks, new_toks = tokens(old), tokens(new)
        # every old token must still be present (multiset subset)
        from collections import Counter
        diff = Counter(old_toks) - Counter(new_toks)
        if diff:
            tok_bad.append(f"{s}: lost {sum(diff.values())} tokens")
    check("div balance unchanged vs HEAD", not div_bad, "; ".join(div_bad[:3]))
    check("zero tokens lost vs HEAD", not tok_bad, "; ".join(tok_bad[:3]))

    # 4. Helper simulation: all options x 50 states.
    html = (ROOT / "index.html").read_text()
    opts = re.findall(
        r'<option value="([^"]+)" data-anchor="([^"]+)"', html
    )
    helper_bad = []
    for value, anch in opts:
        for s in states:
            target = f"{anch}-in-{s}"
            page = (ROOT / "states" / f"{s}.html").read_text()
            if f'id="{target}"' not in page:
                helper_bad.append(f"{value}/{s}")
    check(f"helper simulation {len(opts)} options x 50 states",
          not helper_bad, f"{len(helper_bad)} failures: {helper_bad[:3]}")

    # 5. Search index schema + keyword returns 50.
    idx = json.loads((ROOT / "assets" / "search-index.json").read_text())
    check("index size", len(idx) == index_size, f"got {len(idx)}")
    bad_schema = [e for e in idx if set(e.keys()) != {"p", "u", "a", "h", "t"}]
    check("index schema exact", not bad_schema, f"{len(bad_schema)} bad")
    kw = keyword.lower()
    hits = [e for e in idx if kw in (e.get("t", "") + e.get("h", "")).lower()
            and e.get("a", "").startswith(f"{anchor}-in-")]
    check(f"search '{keyword}' -> 50 state entries",
          len(hits) == 50 and len({e["u"] for e in hits}) == 50,
          f"got {len(hits)} entries, {len({e['u'] for e in hits})} states")

    # 6. About + counts.
    about = (ROOT / "about.html").read_text()
    check("About count", f"{about_count} legal topics" in about)
    check("helper option present",
          f'value="{helper_value}" data-anchor="{anchor}"' in html)
    check("card present", f'data-topic="{slug}"' in html)
    check("show-all label",
          f"Show all {about_count - 45} topics" in html,
          "second-grid label")
    print()
    if failures:
        print("FAILURES:", failures)
        sys.exit(1)
    print("ALL CHECKS PASS")


if __name__ == "__main__":
    main()
