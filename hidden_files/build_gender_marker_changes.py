#!/usr/bin/env python3
"""Build Topic #111: Gender Marker Changes — standalone section on
all 50 state pages.

Inserts one new section per state page (before Foster Care & Youth
Aging Out, newest-first), a contents-list entry (before the
foster-care-youth-aging-out <li>), a homepage helper option + topic
card (after Foster Care & Youth Aging Out), bumps About 109 -> 110,
and appends 50 state entries + 1 helper entry to
assets/search-index.json (11977 -> 12028).

Data: hidden_files/topic-research/gender-marker-changes/all-states.json
(coordinator-merged 2026-11-20 from 5 research batches).

Spot verifications 2026-11-20 (second sources, all confirmed):
- Florida: DHSMV memo Jan 26, 2024 rescinded the license gender-change
  policy (Equality Florida FAQ; Southern Legal Counsel memo) and Vital
  Statistics is not processing birth-certificate marker changes
  (family-law reporting; NameRight Nov 2026 check).
- Kansas SB 244, effective Feb 26, 2026: invalidates licenses and birth
  certificates not matching sex assigned at birth (kslegislature.gov
  supplemental note; CNN Mar 5, 2026; Williams Institute Oct 2026).
- Oklahoma Fowler v. Stitt, 2026 OK 68 (Sept 29, 2026): state law never
  permitted changing the sex designation on a birth certificate, even
  with a court order (Oklahoma Supreme Court opinion; Oklahoma Voice).
- Idaho: 2018 injunction dissolved Jan 8, 2026, so Idaho Code
  39-245A is enforced again (Idaho AG press release).
- Indiana: BMV stopped changing license gender markers Feb 12, 2026
  under amended 140 IAC 7-1.1-3 (NCTE; Indiana Capital Chronicle);
  Dept. of Health not processing birth-certificate changes since
  March 2025 under EO 25-36.
- Iowa SF 418, effective July 1, 2025: repealed the birth-certificate
  sex-designation amendment process (legis.iowa.gov enrolled bill;
  Cedar Rapids Gazette).
- Texas: DPS stopped accepting gender-marker court orders Aug 20,
  2024 (Texas State Law Library guide; ACLU-TX Oct 2026 fact sheet).
- South Dakota: Nielsen, 2026 S.D. 12 (Mar 4, 2026) — ARSD
  44:09:05:02 allows only correction of data wrong at birth
  (Justia opinion summary; Rapid City Post).
- Wyoming: emergency rule Nov 19, 2025, permanent Mar 13, 2026 —
  Chapter 10 s.4(e) no longer accepts a court order reflecting a sex
  change (wyoleg.gov official rule filings; Transitics).
- Montana: Kalarchik v. State, 2026 MT 76 (Apr 14, 2026) — MT Supreme
  Court affirmed the preliminary injunction against SB 458, the 2022
  DPHHS rule, and the MVD policy, so affidavit/license changes work
  while the injunction stands (Justia; ACLU).
- Ohio: BMV stopped accepting the Declaration of Gender Change form
  (BMV 2369) around Aug 18, 2026, citing ORC 9.05 (Ohio Capital
  Journal via Cincinnati.com / The Post).
- Mississippi SB 2322, effective July 1, 2026: licenses must show
  sex determined at birth; a court order to the contrary has no
  effect (billstatus.ls.state.ms.us official bill text).
- Arizona: Roe v. Johnston, 9th Cir. (filed Oct 6, 2026) — court-order
  route under A.R.S. 36-337(A)(4) requires no specific medical
  treatment (9th Cir. opinion; NCLR).
- Colorado HB 25-1312 (2025): repealed the one-time birth-certificate
  limit; license limit 1 -> 3 effective Oct 1, 2026
  (leg.colorado.gov bill summary).
- Minnesota: MDH change-a-birth-record page confirms the payload
  exactly — physician letter or court order, $40 amendment fee, $26
  certificate (live text fetch; curl 403 was a bot filter).
- Mississippi MSDH vital-records Q&A page confirmed live by text
  fetch (curl 000 was a network error, not a 404).
- Ohio agency URL kept: the ODH adoption-file-information page is a
  Bureau of Vital Statistics page confirmed live by search crawl
  Nov 2026 (curl 404 is a bot filter, same pattern as Minnesota).

Dataset fixes applied 2026-11-20 before building:
- Kentucky legal aid swapped to Legal Aid of the Bluegrass
  (https://lablaw.org/, live 200) for consistency with #108/#109.
- Oklahoma agency URL swapped from the aem-prod host to the
  production https://www.oklahoma.gov/health/services/birth-and-death-certificates/amendments.html
  (both curl 200; production preferred).
- Delaware legal aid URL upgraded http -> https://www.declasi.org
  (https curl 200).

Headline counts (computed from the dataset): 15 states require a court
order for at least one document; 10 states require proof of surgery
(or a medical statement attesting to the change) on the birth-
certificate route (Alabama, Arkansas, Georgia, Kentucky, Louisiana,
Mississippi, Missouri, Nebraska, North Dakota, Wisconsin); 34 states
need neither a court order nor surgery; 10 states effectively block
gender-marker changes on both documents (Florida, Idaho, Indiana,
Iowa, Kansas, Oklahoma, South Dakota, Tennessee, Texas, Wyoming).
Montana's rules are set by litigation (injunction in effect). No phone
numbers in the dataset.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "gender-marker-changes" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-gender-marker-changes.jpg"

SLUG = "gender-marker-changes"
TITLE = "Gender Marker Changes"
PREV_SLUG = "foster-care-youth-aging-out"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="gender-marker-changes-in-{slug}">Gender marker changes in {esc(state)}</h2>'
    )
    parts.append(
        "<p>The letter on your birth certificate or driver&rsquo;s license "
        "— M, F, or X — is called a gender marker, and in most states "
        "you can change it so your ID matches who you are. But the "
        "rules are different in every state, and they have changed "
        "fast in 2025 and 2026. In <strong>34 states</strong> you need "
        "neither a court order nor surgery. In <strong>15 states</strong> "
        "a court order is required for at least one document. In "
        "<strong>10 states</strong> (Florida, Idaho, Indiana, Iowa, "
        "Kansas, Oklahoma, South Dakota, Tennessee, Texas, and Wyoming) "
        "a gender-marker change is effectively blocked on both "
        "documents right now. And in Montana, the rules are set by a "
        "court injunction that could change. The picture here is as of "
        "<strong>November 2026</strong>. This is general information, "
        "not legal advice.</p>"
    )
    # --- Card 1: birth certificates ---
    parts.append('<div class="card">')
    parts.append("<h3>Birth certificates</h3>")
    parts.append(
        "<p>Your birth certificate is the foundation document — a "
        "driver&rsquo;s license change often depends on it, so start "
        "here. In the easiest states you change it with a sworn "
        "statement of your own, no doctor and no judge involved. In "
        "middle-ground states you need a letter from a doctor or other "
        "health care provider saying you have had appropriate "
        "clinical treatment, or a court order. In the strictest states "
        "you need a court order plus proof of surgery. And in 10 "
        "states there is currently no working route at all — the "
        "agency simply will not process the change, even with a court "
        "order. Where you were born matters more than where you live "
        "now: a birth certificate is always changed through the state "
        "where the birth happened.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Find the vital "
        "records office of the state where you were born — the agency "
        "linked in the card below — and check its current form before "
        "you file anything. Rules changed in several states during "
        "2025 and 2026, and old guides online still describe routes "
        "that no longer work.</p>"
    )
    parts.append("</div>")
    # --- Card 2: driver's licenses ---
    parts.append('<div class="card">')
    parts.append("<h3>Driver&rsquo;s licenses and state IDs</h3>")
    parts.append(
        "<p>The license or state ID is the document you show every "
        "day, and its rules are separate from the birth certificate. "
        "In many states you can pick M, F, or X on a license by "
        "self-designation — just tell the DMV what marker you want, "
        "no paperwork beyond the usual ID application. In other "
        "states you need a doctor&rsquo;s letter, a court order, or "
        "an amended birth certificate showing the new marker. In the "
        "10 blocking states, the license marker cannot be changed to "
        "reflect gender identity at all right now — usually because "
        "the DMV now takes the marker from your birth certificate or "
        "passport and will not accept a gender-change request. A few "
        "states offer no X marker: only M or F.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Change the birth "
        "certificate first if your state&rsquo;s DMV requires an "
        "amended birth certificate — that is the most common reason a "
        "license change gets stuck. If you only need the license "
        "changed, check whether your DMV accepts a doctor&rsquo;s "
        "letter on its own; in several states that is the fastest "
        "route.</p>"
    )
    parts.append("</div>")
    # --- Card 3: court orders and surgery ---
    parts.append('<div class="card">')
    parts.append("<h3>Court orders and surgery: when they are needed</h3>")
    parts.append(
        "<p>A court order is the most common extra requirement: "
        "<strong>15 states</strong> require one for at least one "
        "document, usually the birth certificate. Getting one means "
        "filing a petition in court — often the same court that "
        "handles name changes — and a judge signs an order directing "
        "the agency to amend the record. Surgery is required far less "
        "often than people think: only <strong>10 states</strong> "
        "still require proof of surgery (or a doctor&rsquo;s "
        "statement that the change happened) on the birth-certificate "
        "route — Alabama, Arkansas, Georgia, Kentucky, Louisiana, "
        "Mississippi, Missouri, Nebraska, North Dakota, and Wisconsin. "
        "In the other 40 states, no surgery is required for either "
        "document. And a court order does not fix everything: in the "
        "blocking states, agencies are refusing to honor gender-marker "
        "court orders entirely.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If your state "
        "needs a court order, ask the legal aid organization in the "
        "card below — many help with these petitions for free. Do not "
        "assume you need surgery: check your state&rsquo;s card "
        "below first, because in most states you do not.</p>"
    )
    parts.append("</div>")
    # --- Card 4: what to do first ---
    parts.append('<div class="card">')
    parts.append("<h3>Before you start: three things to know</h3>")
    parts.append(
        "<p><strong>First, a name change is a separate process.</strong> "
        "Changing your legal name goes through a court in the state "
        "where you live, and it is covered in the Name Changes "
        "section. You can often do the name and the marker together, "
        "but they are different filings. <strong>Second, federal "
        "documents have their own rules.</strong> A state change does "
        "not automatically change your U.S. passport or your Social "
        "Security record — those are federal, and you update them "
        "separately with the State Department and the Social Security "
        "Administration. <strong>Third, keep copies of everything.</strong> "
        "Save the court order, the doctor&rsquo;s letter, and the old "
        "and new documents: if a rule changes again, you may need to "
        "prove what was already approved.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Decide which "
        "document to change first — usually the birth certificate, "
        "since the license often follows it. (2) Gather the proof "
        "your state asks for, using the card below. (3) File with "
        "the agency listed, and keep a copy of everything you send.</p>"
    )
    parts.append("</div>")
    # --- Card 5: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Gender marker changes in {esc(state)}</h3>")
    parts.append(f"<p><strong>How it works here:</strong> {esc(e['marker_overview'])}</p>")
    parts.append(f"<p><strong>Birth certificate:</strong> {esc(e['birth_certificate'])}</p>")
    parts.append(f"<p><strong>Driver&rsquo;s license or state ID:</strong> {esc(e['drivers_license'])}</p>")
    parts.append(f"<p><strong>Court order required?</strong> {esc(e['court_order_required'])}</p>")
    parts.append(f"<p><strong>Surgery required?</strong> {esc(e['surgery_required'])}</p>")
    parts.append(
        f"<p><strong>State agency:</strong> "
        f'<a href="{esc(e["agency_url"])}" target="_blank" rel="noopener">{esc(e["agency_name"])}</a>. '
        f"Start here for the current forms and fees.</p>"
    )
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
    )
    parts.append(
        f"<p><strong>What to do:</strong> Check the agency&rsquo;s "
        f"current form before you file — several states changed "
        f"their rules in 2025 and 2026. If a court order is needed, "
        f"get free help from the organization linked above before "
        f"you file, and keep copies of everything you submit.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Work out "
        "which state issued your birth certificate — that state&rsquo;s "
        "rules control the birth-certificate change. (2) Check the "
        "card above for what proof your state wants: a sworn "
        "statement, a doctor&rsquo;s letter, a court order, or "
        "proof of surgery. (3) File with the agency linked above, "
        "then update your license, and separately update your "
        "passport and Social Security record. (4) If your state is "
        "one of the 10 blocking states, talk to the legal aid "
        "organization linked above before you spend money on a court "
        "filing — a court order may not help there right now.</p>"
    )
    parts.append(
        "<p><em>Sources: the official state vital records and motor "
        "vehicle agencies, state statutes, and court decisions linked "
        "in the research for this section, checked November 20, 2026. "
        "In 34 states you need neither a court order nor surgery; 15 "
        "states require a court order for at least one document; 10 "
        "states require proof of surgery on the birth-certificate "
        "route; and 10 states effectively block gender-marker changes "
        "on both documents. Montana&rsquo;s rules are set by a court "
        "injunction that could change. Confirm the current law with a "
        "local attorney before you rely on it. This is general "
        "information, not legal advice.</em></p>"
    )
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def build_state_pages(data):
    for key, e in data:
        state = e["state"]
        slug = e.get("slug") or key.replace(" ", "-")
        path = STATES / f"{slug}.html"
        text = path.read_text()
        anchor = f'id="{SLUG}-in-{slug}"'
        assert anchor not in text, f"{slug}: anchor already present"
        h2 = text.find(f'<h2 id="{PREV_SLUG}-in-{slug}">')
        assert h2 != -1, f"{slug}: {PREV_SLUG} h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        before = text
        new_section = section_html(state, slug, e)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#' + re.escape(PREV_SLUG) + r'-in-'
            + re.escape(slug)
            + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: {PREV_SLUG} contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#{SLUG}-in-{slug}">'
            f"Gender marker changes in {state}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        assert text.count(f'id="{SLUG}-in-{slug}"') == 1, f"{slug}: anchor count"
        assert text.count("<div") - before.count("<div") == 5, f"{slug}: div open delta"
        assert text.count("</div>") - before.count("</div>") == 5, f"{slug}: div close delta"
        assert text.count("<div") == text.count("</div>"), f"{slug}: div imbalance"
        h2s = re.findall(r'<h2 id="([^"]+)">', text)
        assert h2s.index(f"{SLUG}-in-{slug}") == h2s.index(f"{PREV_SLUG}-in-{slug}") - 1, f"{slug}: h2 order"
        assert not re.search(r"\bNone\b", new_section), f"{slug}: leaked None in new section"
        assert "TODO" not in new_section and "FIXME" not in new_section, f"{slug}: leaked marker"
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert SLUG not in helper_part, "index already has helper option"
    assert f'data-topic="{SLUG}"' not in text, "index already has card"
    m = re.search(
        r'<option value="foster-care-youth-aging-out" data-anchor="foster-care-youth-aging-out">.*?</option>',
        text,
        re.S,
    )
    assert m, "foster-care helper option not found"
    opt_old = m.group(0)
    opt_new = (
        opt_old
        + '\n<option value="gender-marker-changes" data-anchor="gender-marker-changes">'
        "Gender marker changes — how to change the M, F, or X on your birth certificate and driver&rsquo;s license, when a court order or surgery is needed, and which states block the change</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="foster-care-youth-aging-out"'
    idx = text.find(card_anchor)
    assert idx != -1, "foster-care card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="gender-marker-changes">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-gender-marker-changes.jpg" alt="Gender Marker Changes" loading="lazy"></span>
          <h3>Gender Marker Changes</h3>
          <p>How to change the M, F, or X on your birth certificate and driver&rsquo;s license — when a court order or surgery is needed, and which states block the change — state by state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 64 topics" in text, "show-all label not found"
    text = text.replace("Show all 64 topics", "Show all 65 topics", 1)
    show_pos = text.find("Show all 65 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">64 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("64 topics", "65 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 64->65")


def build_about():
    text = ABOUT.read_text()
    assert text.count("109 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("109 legal topics", "110 legal topics", 1))
    print("  about.html: 109 -> 110")


def state_index_t(state, slug, e):
    bits = [
        "gender marker change birth certificate driver's license M F X",
        f"Gender marker changes in {state}",
        f"{e['marker_overview']}",
        f"birth certificate {e['birth_certificate']}",
        f"driver's license {e['drivers_license']}",
        f"court order {e['court_order_required']}",
        f"surgery {e['surgery_required']}",
        f"{e['agency_name']} {e['legal_aid_name']}",
        "self-attestation court order surgery vital records DMV name change passport Social Security",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11977, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = e["state"]
        slug = e.get("slug") or key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Gender marker changes in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Gender Marker Changes",
            "t": (
                "gender-marker-changes Gender Marker Changes? "
                "How to change the M, F, or X on your birth certificate and driver's license — when a court "
                "order or surgery is needed, and which states block the change — state by state. "
                "birth certificate driver's license M F X self-attestation court order surgery vital records "
                "DMV name change passport Social Security."
            ),
        }
    )
    assert len(idx) == 12028, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11977 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    assert len(d) == 50, len(d)
    data = [(k, d[k]) for k in sorted(d)]  # keys already lowercase
    slugs = [(e.get("slug") or k.replace(" ", "-")) for k, e in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "agency_name", "agency_url", "birth_certificate", "court_order_required",
        "drivers_license", "legal_aid_name", "legal_aid_url", "marker_overview",
        "sources", "state", "surgery_required",
    ]
    phone_re = re.compile(
        r"\(\d{3}\)\s*\d{3}[-.]\d{4}|\b\d{3}[-.]\d{3}[-.]\d{4}\b|"
        r"1-800-\d{3}-\d{4}|1-866-\d{3}-\d{4}|1-888-\d{3}-\d{4}|1-855-\d{3}-\d{4}|"
        r"877-\d{3}-\d{4}|800-\d{3}-\d{4}|844-\d{3}-\d{4}|866-\d{3}-\d{4}|855-\d{3}-\d{4}|"
        r"1-877-\d{3}-\d{4}|1-833-[A-Z0-9]{7}"
    )
    for k, e in data:
        for f in req:
            assert f in e, f"{k}: missing {f}"
        assert all(e[f] for f in req if f != "sources"), f"{k}: empty required field"
        assert e["sources"] and len(e["sources"]) >= 2, f"{k}: fewer than 2 sources"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before foster-care-youth-aging-out section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
