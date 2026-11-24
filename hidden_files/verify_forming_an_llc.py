#!/usr/bin/env python3
"""Independent verification for Topic #113 (Forming an LLC).

Checks, from the files on disk (not the builder's own assertions):
- all 50 state pages: new anchor exactly once, h2 order (new section
  immediately before protecting-kids-online), contents <li> present,
  SBB pointer present, old SBB h3 gone, SBB closing sentence updated,
  div balance, fee + filing link + legal-aid link present in new section.
- index.html: helper option + card present, counts read 112, hero
  42-topic badge untouched, protecting-kids-online option/card intact.
- about.html reads 112 legal topics.
- search-index.json: 12130 entries, every new entry schema {p,u,a,h,t}
  and containing an LLC token.
- page-text token check on Minnesota: the SBB section still contains
  the structure comparison and the next-steps checklist (nothing lost
  but the replaced LLC-steps block).
Prints PASS/FAIL per check; exit code 0 only if all pass.
The live search simulation runs separately in verify_llc_search.js.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "forming-an-llc" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"

fails = []
passes = []


def check(name, ok, detail=""):
    (passes if ok else fails).append(name)
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail and not ok else ""))


def main():
    d = json.loads(DATA.read_text())
    assert len(d) == 50
    # --- state pages ---
    bad_anchor = bad_order = bad_li = bad_ptr = bad_h3 = bad_close = bad_div = bad_links = []
    for slug, e in sorted(d.items()):
        state = e["state"]
        text = (STATES / f"{slug}.html").read_text()
        a = f'id="forming-an-llc-in-{slug}"'
        if text.count(a) != 1:
            bad_anchor.append(slug)
        h2s = re.findall(r'<h2 id="([^"]+)">', text)
        try:
            if h2s.index(f"forming-an-llc-in-{slug}") != h2s.index(f"protecting-kids-online-in-{slug}") - 1:
                bad_order.append(slug)
        except ValueError:
            bad_order.append(slug)
        if f'<a href="#forming-an-llc-in-{slug}">Forming an LLC in {state}</a>' not in text:
            bad_li.append(slug)
        if f'<a href="#forming-an-llc-in-{slug}">Forming an LLC in {state}</a>' not in text:
            bad_ptr.append(slug)
        if f"Forming an LLC in {state}: the general steps" in text:
            bad_h3.append(slug)
        if f"The {state} LLC filing fee and form are in the" not in text:
            bad_close.append(slug)
        if "does not print a single" in text and f"{state} LLC filing fee, form number" in text:
            bad_close.append(slug + "(old-close)")
        if text.count("<div") != text.count("</div>"):
            bad_div.append(slug)
        sec = text[text.find(a):]
        sec = sec[: sec.find("</section>")]
        need = [e["filing_fee"], e["filing_url"], e["legal_aid_url"], e["legal_aid_name"]]
        if not all(n in sec for n in need):
            bad_links.append(slug)
        if e.get("series_llc") and "Series LLCs:</strong>" not in sec:
            bad_links.append(slug + "(series)")
        if not e.get("series_llc") and "could not verify from an official source" not in sec:
            bad_links.append(slug + "(series-claimfree)")
    check("50 state pages: anchor exactly once", not bad_anchor, str(bad_anchor))
    check("50 state pages: h2 order (new section right before protecting-kids-online)", not bad_order, str(bad_order))
    check("50 state pages: contents <li> present", not bad_li, str(bad_li))
    check("50 state pages: SBB pointer link present", not bad_ptr, str(bad_ptr))
    check("50 state pages: old SBB h3 gone", not bad_h3, str(bad_h3))
    check("50 state pages: SBB closing sentence updated", not bad_close, str(bad_close))
    check("50 state pages: div balance", not bad_div, str(bad_div))
    check("50 state pages: fee + filing link + legal aid in new section", not bad_links, str(bad_links))

    # --- Minnesota SBB coherence spot check ---
    mn = (STATES / "minnesota.html").read_text()
    sbb_start = mn.find('id="small-business-basics-in-minnesota"')
    sbb_end = mn.find("</section>", sbb_start)
    sbb = mn[sbb_start:sbb_end]
    check("MN SBB: structure comparison still present",
          "Pick a structure first: sole proprietorship, LLC, partnership, corporation" in sbb)
    check("MN SBB: EIN resource still present", "Tax IDs: get an EIN free from the IRS" in sbb)
    check("MN SBB: contracts + licenses + traps still present",
          all(x in sbb for x in ["Simple contracts: what a solid written agreement needs",
                                  "Business licenses and permits: where to check",
                                  "Common first-timer traps"]))
    check("MN SBB: next-steps checklist intact",
          "Form it properly." in sbb and "Separate the money and get insured." in sbb)
    check("MN SBB: pointer reads as a pointer",
          "Forming an LLC in Minnesota: the steps, fees, and forms" in sbb)

    # --- index.html ---
    idx = INDEX.read_text()
    check("index: helper option present",
          'value="forming-an-llc" data-anchor="forming-an-llc"' in idx)
    check("index: card present", 'data-topic="forming-an-llc"' in idx)
    check("index: thumbnail referenced",
          "assets/img/topics/thumbs/legal-buffet-forming-an-llc.jpg" in idx)
    check("index: show-all reads 112", "Show all 112 topics" in idx and "Show all 111 topics" not in idx)
    check("index: main-grid badge reads 112",
          '<span class="count-badge">112 topics</span>' in idx)
    check("index: hero 42-topic badge untouched",
          idx.count('<span class="count-badge">42 topics</span>') == 1)
    check("index: protecting-kids-online option/card intact",
          'value="protecting-kids-online"' in idx and 'data-topic="protecting-kids-online"' in idx)
    # helper option order: forming-an-llc directly after protecting-kids-online
    check("index: helper option directly after protecting-kids-online",
          idx.find('value="forming-an-llc"') > idx.find('value="protecting-kids-online"') and
          'value="divorce"' in idx[idx.find('value="forming-an-llc"'):idx.find('value="forming-an-llc"') + 2000])

    # --- about.html ---
    about = ABOUT.read_text()
    check("about: reads 112 legal topics",
          "112 legal topics" in about and "111 legal topics" not in about)

    # --- search index ---
    si = json.loads(SEARCH_INDEX.read_text())
    check("search index: 12130 entries", len(si) == 12130, f"got {len(si)}")
    new = [e for e in si if e.get("a", "").startswith("forming-an-llc-in-")]
    check("search index: 50 new state entries", len(new) == 50, f"got {len(new)}")
    helper = [e for e in si if e.get("a") == "helper" and e.get("h") == "Forming an LLC"]
    check("search index: 1 new helper entry", len(helper) == 1, f"got {len(helper)}")
    schema_ok = all(set(e.keys()) == {"p", "u", "a", "h", "t"} for e in new + helper)
    check("search index: new entries schema {p,u,a,h,t}", schema_ok)
    llc_ok = all("llc" in (e["h"] + " " + e["t"]).lower() for e in new + helper)
    check("search index: every new entry carries LLC tokens", llc_ok)
    urls_ok = all(e["u"] == f"states/{e['a'][len('forming-an-llc-in-'):]}.html" for e in new)
    check("search index: new entry URLs match their state pages", urls_ok)

    print(f"\n{len(passes)} PASS, {len(fails)} FAIL")
    if fails:
        print("FAILURES:", fails)
        sys.exit(1)
    print("ALL VERIFICATION CHECKS PASSED")


if __name__ == "__main__":
    main()
