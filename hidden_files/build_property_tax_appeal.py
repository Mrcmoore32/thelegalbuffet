#!/usr/bin/env python3
"""Build Topic #76: Property Tax Assessment Appeal — all 50 pages.

Inserts one new section per state page (before the Naturalization
section, newest-first), a contents-list entry, a homepage helper option
+ topic card (second grid, after Naturalization), bumps About 74 -> 75,
and appends 50 state entries + 1 helper entry to
assets/search-index.json (10192 -> 10243).

Data: hidden_files/topic-research/property-tax-appeal/all-states.json
(coordinator-written from the researcher's full JSON payload).

Coordinator verification before the build:
- Headline deadlines spot-checked against official sources: TX (May 15
  or 30 days after notice, Form 50-132, Comptroller), CA (July 2-Sept 15
  / Nov 30, BOE-305-AH, BOE Rule 305), FL (25 days after TRIM, DR-486,
  $15, Fla. Stat. 194.011/194.013), NY (Grievance Day 4th Tuesday May,
  RP-524, SCAR $30, tax.ny.gov), MN (matches the MN DOR Fact Sheet 3
  already linked on the site), NH ($65 BTLA fee + Sept 1, RSA 76:16-a).
- All 37 dataset URLs curl-swept: 30x 200. Idaho's BTA form URL
  (bta.idaho.gov/?p=847) 404'd -> repointed to the verified-live BTA
  homepage https://bta.idaho.gov/, which links the appeal form and
  confirms the 4th-Monday-of-June / 30-day rules. Oregon's
  stage.oregon.gov PDF 401'd (staging host) -> form URL dropped to
  null; the official DOR appeals page (200) says PVAB forms come from
  the county clerk. NY, RI, AK, MA, NJ pages confirmed live via text
  fetch (curl 403/000 were bot filters). NH btla.nh.gov 403'd to both
  curl and text fetch (nh.gov blocks this crawler); the domain is the
  official BTLA site and the $65/Sept 1 facts are corroborated by
  RSA 76:16-a, so the link is kept and flagged here.
- No phone numbers in the dataset, so no phone second-sourcing was
  needed. No "state has no X" claims are printed.
- The buried Foreclosure Defense block stays in place; the new section
  goes further (per-state deadline, where to file, steps, evidence,
  fees, form URLs, next appeal) and cross-references it.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "property-tax-appeal" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"

TOPIC = "property-tax-appeal"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(s):
    state = s["state"]
    slug = s["slug"]
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="property-tax-appeal-in-{slug}">Appealing Your Property '
        f"Tax Assessment in {esc(state)}</h2>"
    )
    parts.append(
        f"<p>The value on your assessment notice decides your tax bill, and "
        f"you have the right to challenge it if you think it is too high. "
        f"Appeals are local: they start with the assessor or a local board "
        f"of review or equalization, with a further appeal to a state board "
        f"or tax court if you still disagree. This section gives you "
        f"{esc(state)}'s deadline, where to file, what to bring, what it "
        f"costs, and what happens if the board says no. The Foreclosure "
        f"Defense section on this page has a shorter version of this "
        f"process. This is general information, not legal advice.</p>"
    )
    # --- Deadline ---
    parts.append('<div class="card">')
    parts.append(f"<h3>The deadline &mdash; read it the day the notice arrives</h3>")
    parts.append(f"<p>{esc(s['appeal_deadline'])}</p>")
    parts.append(
        "<p>Appeal windows are short and they are enforced. Miss the window "
        "and you usually wait until next year, paying the higher bill in "
        "the meantime. Read the date on your notice the day it arrives and "
        "calendar it.</p>"
    )
    parts.append("</div>")
    # --- Where to file ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Where to file</h3>")
    parts.append(f"<p>{esc(s['appeal_where'])}</p>")
    parts.append("</div>")
    # --- How to file ---
    parts.append('<div class="card">')
    parts.append(f"<h3>How to file, step by step</h3>")
    parts.append(f"<p>{esc(s['appeal_how'])}</p>")
    parts.append("</div>")
    # --- Evidence ---
    parts.append('<div class="card">')
    parts.append(f"<h3>What evidence wins</h3>")
    parts.append(f"<p>{esc(s['appeal_evidence'])}</p>")
    parts.append(
        "<p>Get your property record card from the assessor and check every "
        "line for errors. Bring copies to the hearing and keep your "
        "originals.</p>"
    )
    parts.append("</div>")
    # --- Fee ---
    parts.append('<div class="card">')
    parts.append(f"<h3>What it costs</h3>")
    if s.get("appeal_fee"):
        parts.append(f"<p>{esc(s['appeal_fee'])}</p>")
    else:
        parts.append(
            f"<p>We could not confirm a filing fee from an official source "
            f"for {esc(state)}. Ask the board or your assessor before you "
            f"file &mdash; do not assume it is free, and do not assume a "
            f"fee quoted by a third-party site is current.</p>"
        )
    parts.append("</div>")
    # --- After the board ---
    parts.append('<div class="card">')
    parts.append(f"<h3>If the board says no</h3>")
    parts.append(f"<p>{esc(s['after_appeal'])}</p>")
    parts.append(
        "<p>Keep paying your property taxes on time while you appeal. An "
        "appeal does not pause the bill, and unpaid taxes can draw "
        "penalties or a lien even while your case is pending.</p>"
    )
    parts.append("</div>")
    # --- Official form / help ---
    links = []
    if s.get("appeal_form_url"):
        links.append(
            f'<li><a href="{esc(s["appeal_form_url"])}" target="_blank" '
            f'rel="noopener">Official appeal form or guide</a></li>'
        )
    if s.get("assessor_url"):
        links.append(
            f'<li><a href="{esc(s["assessor_url"])}" target="_blank" '
            f'rel="noopener">Official assessment appeals information</a></li>'
        )
    if links:
        parts.append('<div class="card">')
        parts.append(f"<h3>Official form and help in {esc(state)}</h3>")
        parts.append("<ul>")
        parts.extend(links)
        parts.append("</ul>")
        parts.append("</div>")
    else:
        parts.append('<div class="card">')
        parts.append(f"<h3>Official form and help in {esc(state)}</h3>")
        parts.append(
            "<p>Your county assessor's office has the appeal form for your "
            "county &mdash; ask for it by name and confirm the deadline in "
            "writing.</p>"
        )
        parts.append("</div>")
    # --- Do this now ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Find the appeal deadline "
        "on your assessment notice and calendar it today. Then pull your "
        "property record card, check it line by line for errors, gather "
        "recent sales of comparable homes, and file the appeal this section "
        "describes &mdash; in writing, and keep proof you filed on time.</p>"
    )
    parts.append(
        "<p><em>Sources: official state and county assessment-appeal pages "
        "listed above. Checked against official sources in November 2026. "
        "Deadlines and fees change &mdash; confirm the date on your own "
        "assessment notice before you file. This is general information, "
        "not legal advice.</em></p>"
    )
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def build_state_pages(data):
    for s in data:
        slug = s["slug"]
        path = STATES / f"{slug}.html"
        text = path.read_text()
        anchor = f"property-tax-appeal-in-{slug}"
        assert anchor not in text, f"{slug}: anchor already present"
        # --- insert section before Naturalization section (newest-first) ---
        h2 = text.find(f'<h2 id="naturalization-in-{slug}">')
        assert h2 != -1, f"{slug}: naturalization h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        new_section = section_html(s)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the naturalization <li> ---
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#naturalization-in-'
            + re.escape(slug)
            + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: naturalization contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#property-tax-appeal-in-{slug}">'
            f"Appealing Your Property Tax Assessment in {s['state']}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert "property-tax-appeal" not in helper_part, "index already has helper option"
    assert 'data-topic="property-tax-appeal"' not in text, "index already has card"
    opt_old = (
        '<option value="naturalization" data-anchor="naturalization">'
        "Becoming a U.S. citizen</option>"
    )
    assert opt_old in text, "naturalization helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="property-tax-appeal" data-anchor="property-tax-appeal">'
        "Appealing your property tax assessment</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="naturalization"'
    idx = text.find(card_anchor)
    assert idx != -1, "naturalization card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="property-tax-appeal">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-property-tax-appeal.jpg" alt="Appealing Your Property Tax Assessment" loading="lazy"></span>
          <h3>Appealing Your Property Tax Assessment</h3>
          <p>Think your home is assessed too high? Your state's appeal deadline, where to file, what evidence wins, and what happens if the board says no.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 29 topics" in text, "show-all label not found"
    text = text.replace("Show all 29 topics", "Show all 30 topics", 1)
    assert '<span class="count-badge">29 topics</span>' in text
    text = text.replace(
        '<span class="count-badge">29 topics</span>',
        '<span class="count-badge">30 topics</span>',
        1,
    )
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 29->30")


def build_about():
    text = ABOUT.read_text()
    assert "74 legal topics" in text, "about count not found"
    ABOUT.write_text(text.replace("74 legal topics", "75 legal topics", 1))
    print("  about.html: 74 -> 75")


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 10192, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith("property-tax-appeal-in-") for e in idx)
    for s in data:
        state = s["state"]
        slug = s["slug"]
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"property-tax-appeal-in-{slug}",
                "h": f"Appealing Your Property Tax Assessment in {state}",
                "t": (
                    f"Appealing Your Property Tax Assessment in {state} "
                    f"\u2014 property tax assessment appeal assessed value too "
                    f"high board of equalization board of review protest "
                    f"grievance abatement deadline comparable sales {state}"
                ),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Appealing Your Property Tax Assessment",
            "t": (
                "Think your home is assessed too high? Your state's appeal "
                "deadline, where to file, what evidence wins, and what "
                "happens if the board says no."
            ),
        }
    )
    assert len(idx) == 10243, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 10192 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [states[k] for k in sorted(states)]
    slugs = [s["slug"] for s in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert all(s.get("appeal_deadline") for s in data), "missing deadline"
    print("building state pages...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
