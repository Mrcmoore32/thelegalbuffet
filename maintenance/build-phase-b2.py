#!/usr/bin/env python3
"""Phase B batch B2 build script (idempotent — safe to re-run).

B2-2: inserts a WebSite JSON-LD block before </head> on every content page.
      FAQ schema is deliberately NOT added: an audit of all pages found no
      genuine on-page FAQ section or question/answer list (question-style
      headings are resource-card titles, and the only "FAQ" hits are links
      to other sites' FAQ pages, not visible Q&A on this site). Per the
      task rules, WebSite schema alone is correct where there is no
      genuine FAQ content — never invent questions/answers.
B2-3: inserts the eviction-timeline strip into the Tenant Rights section
      of every state page (see build_timeline() below).

Usage: python3 maintenance/build-phase-b2.py [--jsonld] [--timeline]
       (no flags = both; already-inserted blocks are left untouched)
"""
import glob
import json
import re
import sys

WEBSITE_JSONLD = (
    '<script type="application/ld+json">\n'
    '{"@context": "https://schema.org", "@type": "WebSite", '
    '"name": "The Legal Buffet", "url": "https://thelegalbuffet.com"}\n'
    '</script>\n'
)

CONTENT_PAGES = sorted(
    [p for p in glob.glob("*.html") if not p.startswith("google")]
    + glob.glob("states/*.html")
)


def add_jsonld(path):
    txt = open(path).read()
    if "application/ld+json" in txt:
        return False
    if "</head>" not in txt:
        print(f"  SKIP (no </head>): {path}")
        return False
    txt = txt.replace("</head>", WEBSITE_JSONLD + "</head>", 1)
    open(path, "w").write(txt)
    return True


def main():
    do_jsonld = "--timeline" not in sys.argv
    do_timeline = "--jsonld" not in sys.argv
    if do_jsonld:
        changed = sum(add_jsonld(p) for p in CONTENT_PAGES)
        print(f"JSON-LD: added to {changed} pages, "
              f"{len(CONTENT_PAGES) - changed} already had it")
    if do_timeline:
        try:
            from timeline import build_timeline
        except ImportError:
            print("Timeline module not present yet (added in B2-3); skipping.")
            return
        build_timeline()


if __name__ == "__main__":
    main()
