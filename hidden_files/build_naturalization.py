#!/usr/bin/env python3
"""Build Topic #75: Naturalization / Becoming a U.S. Citizen — all 50 pages.

Inserts one new section per state page (before the Stalking section,
newest-first), a contents-list entry, a homepage helper option + topic
card (second grid, after Stalking), bumps About 73 -> 74, and appends
50 state entries + 1 helper entry to assets/search-index.json
(10141 -> 10192).

Data: hidden_files/topic-research/naturalization/all-states.json
(coordinator-written from the researcher's full JSON payload).
Federal core verified by the coordinator against uscis.gov before the
build: N-400 fee $710 online / $760 paper, reduced fee $380, fee waiver
Form I-912 (N-400 is on the waiver-eligible list; H.R.-1 non-waivable
fees do not cover it), 150% poverty guideline $21,870 for household of
1 (contiguous US, effective Jan. 13, 2026), 2025 civics test (128
questions, 20 asked, 12 to pass) for filings on/after Oct 20, 2025.
Phones printed only where second-sourced: AK (907) 279-2457 (akijp.org
+ immigrationadvocates.org), AR (501) 664-0340 (dolr.org + arkansas-
catholic.org); USCIS Contact Center 1-800-375-5283 as listed on
multiple uscis.gov field-office pages. Org URLs were curl-swept for
liveness before the build; dead ones were removed from the dataset.
Field office city "New Jersey Central" verified as the official USCIS
office name (Cranbury, NJ).
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "naturalization" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"

TOPIC = "naturalization"
ANCHOR = "naturalization-in-{}"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(s, fed):
    state = s["state"]
    slug = s["slug"]
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="naturalization-in-{slug}">Becoming a U.S. Citizen in {esc(state)}</h2>'
    )
    parts.append(
        f"<p>Naturalization is how a green-card holder becomes a U.S. citizen. "
        f"This section is the full step-by-step: who can apply, the form and "
        f"the fee, the English and civics tests, what happens after you are "
        f"approved, and free help in {esc(state)}. The Immigration Help section "
        f"on this page has a shorter version of this process. This is general "
        f"information, not legal advice.</p>"
    )
    # --- Who can apply ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Who can apply in {esc(state)}</h3>")
    parts.append(f"<p>{esc(fed['eligibility'])}</p>")
    parts.append("</div>")
    # --- Steps ---
    parts.append('<div class="card">')
    parts.append(f"<h3>The steps, in order</h3>")
    parts.append("<ol>")
    for step in fed["steps"].split("  "):
        step = step.strip()
        if not step:
            continue
        m = re.match(r"^\d+\)\s*(.*)$", step)
        parts.append(f"<li>{esc(m.group(1) if m else step)}</li>")
    parts.append("</ol>")
    parts.append("</div>")
    # --- Form and fee ---
    parts.append('<div class="card">')
    parts.append(f"<h3>The form and the fee</h3>")
    parts.append(
        f"<p>You apply on <strong>Form N-400</strong>, online or on paper. "
        f"The fee is <strong>${fed['fee_n400_online']} filed online</strong> or "
        f"<strong>${fed['fee_n400_paper']} on paper</strong>, with biometrics "
        f"included. Fees change: confirm the current amount on the "
        f'<a href="https://www.uscis.gov/n-400" target="_blank" '
        f'rel="noopener">USCIS N-400 page</a> before you file, because a '
        f"wrong fee means a rejected application.</p>"
    )
    parts.append(f"<p>{esc(fed['fee_waiver'])}</p>")
    parts.append(f"<p>{esc(fed['reduced_fee'])}</p>")
    parts.append("</div>")
    # --- Tests ---
    parts.append('<div class="card">')
    parts.append(f"<h3>The two tests &mdash; and who is excused from them</h3>")
    parts.append(f"<p>{esc(fed['tests'])}</p>")
    parts.append(f"<p>{esc(fed['exemptions'])}</p>")
    parts.append(
        "<p>Free study materials &mdash; including the civics questions and "
        "practice tests &mdash; are on the "
        '<a href="https://www.uscis.gov/citizenship/find-study-materials-and-resources/study-for-the-test" '
        'target="_blank" rel="noopener">USCIS study page</a>.</p>'
    )
    parts.append("</div>")
    # --- Timeline ---
    parts.append('<div class="card">')
    parts.append(f"<h3>How long it takes</h3>")
    parts.append(f"<p>{esc(fed['timeline'])}</p>")
    parts.append(
        "<p>Check your own field office in the "
        '<a href="https://egov.uscis.gov/processing-times/" target="_blank" '
        'rel="noopener">USCIS Case Processing Times tool</a>.</p>'
    )
    parts.append("</div>")
    # --- After approval ---
    parts.append('<div class="card">')
    parts.append(f"<h3>After you are approved</h3>")
    parts.append(f"<p>{esc(fed['after_approval'])}</p>")
    parts.append("</div>")
    # --- Help in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Free and low-cost help in {esc(state)}</h3>")
    parts.append("<ul>")
    orgs = s.get("help_orgs") or []
    for o in orgs:
        phone = ""
        if o.get("phone"):
            digits = re.sub(r"\D", "", o["phone"])
            phone = (
                f' &mdash; <a href="tel:{digits}">{esc(o["phone"])}</a>'
            )
        parts.append(
            f'<li><a href="{esc(o["url"])}" target="_blank" '
            f'rel="noopener">{esc(o["name"])}</a>{phone}</li>'
        )
    parts.append("</ul>")
    cities = s.get("field_office_cities") or []
    if cities:
        parts.append(
            "<p>USCIS field offices in "
            f"{esc(state)} where interviews and oath ceremonies happen: "
            f"{esc(', '.join(cities))}. Field offices do not take walk-ins "
            "&mdash; go only with an appointment on your notice. Find your "
            "assigned office in the "
            '<a href="https://www.uscis.gov/about-us/find-a-uscis-office/field-offices" '
            'target="_blank" rel="noopener">USCIS office locator</a>.</p>'
        )
    else:
        parts.append(
            "<p>There is no USCIS field office in "
            f"{esc(state)}; your interview will be scheduled at the nearest "
            "office in another state. Your notice tells you where to go.</p>"
        )
    parts.append(
        "<p>Questions for USCIS: the USCIS Contact Center at "
        '<a href="tel:18003755283">1-800-375-5283</a> (TTY 1-800-767-1833). '
        "Beware of immigration-services scams: only a licensed attorney or a "
        "DOJ-accredited representative may give you legal advice about your "
        "case.</p>"
    )
    parts.append("</div>")
    parts.append(
        f'<p><em>Sources: <a href="{esc(fed["fee_source_url"])}" '
        f'target="_blank" rel="noopener">USCIS &mdash; Application for '
        f"Naturalization (Form N-400)</a>. Checked against official sources "
        f"in November 2026. Fees and processing times change &mdash; confirm "
        f"the current fee on the USCIS fee schedule before you file. This is "
        f"general information, not legal advice.</em></p>"
    )
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def build_state_pages(data, fed):
    for s in data:
        slug = s["slug"]
        path = STATES / f"{slug}.html"
        text = path.read_text()
        anchor = ANCHOR.format(slug)
        assert anchor not in text, f"{slug}: anchor already present"
        # --- insert section before Stalking section (newest-first) ---
        h2 = text.find(f'<h2 id="stalking-in-{slug}">')
        assert h2 != -1, f"{slug}: stalking h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        new_section = section_html(s, fed)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the stalking <li> ---
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#stalking-in-'
            + re.escape(slug)
            + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: stalking contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#naturalization-in-{slug}">'
            f"Becoming a U.S. Citizen in {s['state']}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert "naturalization" not in helper_part, "index already has helper option"
    assert 'data-topic="naturalization"' not in text, "index already has card"
    opt_old = (
        '<option value="stalking" data-anchor="stalking">Stalking</option>'
    )
    assert opt_old in text, "stalking helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="naturalization" data-anchor="naturalization">'
        "Becoming a U.S. citizen</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="stalking"'
    idx = text.find(card_anchor)
    assert idx != -1, "stalking card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="naturalization">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-naturalization.jpg" alt="Becoming a U.S. Citizen" loading="lazy"></span>
          <h3>Becoming a U.S. Citizen</h3>
          <p>How a green-card holder becomes a U.S. citizen: who can apply, the N-400 form and fee, the English and civics tests, and free help in your state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 28 topics" in text, "show-all label not found"
    text = text.replace("Show all 28 topics", "Show all 29 topics", 1)
    assert '<span class="count-badge">28 topics</span>' in text
    text = text.replace(
        '<span class="count-badge">28 topics</span>',
        '<span class="count-badge">29 topics</span>',
        1,
    )
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 28->29")


def build_about():
    text = ABOUT.read_text()
    assert "73 legal topics" in text, "about count not found"
    ABOUT.write_text(text.replace("73 legal topics", "74 legal topics", 1))
    print("  about.html: 73 -> 74")


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 10141, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith("naturalization-in-") for e in idx)
    for s in data:
        state = s["state"]
        slug = s["slug"]
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"naturalization-in-{slug}",
                "h": f"Becoming a U.S. Citizen in {state}",
                "t": (
                    f"Becoming a U.S. Citizen in {state} \u2014 naturalization "
                    f"N-400 green card citizenship interview English civics test "
                    f"oath ceremony fee waiver {state}"
                ),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Becoming a U.S. Citizen",
            "t": (
                "How a green-card holder becomes a U.S. citizen: who can "
                "apply, the N-400 form and fee, the English and civics tests, "
                "and free help in your state."
            ),
        }
    )
    assert len(idx) == 10192, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 10141 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    fed = d["federal"]
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [states[k] for k in sorted(states)]
    slugs = [s["slug"] for s in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert all(s.get("help_orgs") for s in data), "a state has no help orgs"
    assert fed.get("fee_n400_online") == 710 and fed.get("fee_n400_paper") == 760
    print("building state pages...")
    build_state_pages(data, fed)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
