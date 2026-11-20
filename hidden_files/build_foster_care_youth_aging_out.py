#!/usr/bin/env python3
"""Build Topic #110: Foster Care & Youth Aging Out — standalone section on
all 50 state pages.

Inserts one new section per state page (before Timeshare Exit,
newest-first), a contents-list entry (before the timeshare-exit <li>),
a homepage helper option + topic card (after Timeshare Exit), bumps
About 108 -> 109, and appends 50 state entries + 1 helper entry to
assets/search-index.json (11926 -> 11977).

Data: hidden_files/topic-research/foster-care-youth-aging-out/all-states.json
(coordinator-merged 2026-11-20 from 5 research batches).

URL/verification work 2026-11-20:
- Oklahoma SB 1806 CONFIRMED by two official sources: OKDHS press
  release (June 1, 2026, oklahoma.gov) and the enrolled bill text
  (oklegislature.gov) — extended foster care to 21, effective
  July 1, 2026.
- Idaho HB 245 (2025) CONFIRMED: BillTrack50 (signed/enacted
  03/24/2025) and the IDHW official page — Continuous Foster Care
  to age 23, Voluntary Post-18 Foster Care re-entry before 23.
- Maine V9 to 23 CONFIRMED by the official maine.gov Youth
  Transition Services page (effective 8/8/23).
- Massachusetts to 22 (23 while finishing an associate's degree or
  higher) CONFIRMED against 110 CMR 23.02.
- Nebraska ages out at 19 CONFIRMED by the Nebraska Supreme Court
  B2i presentation and the B2i Advisory Committee report — Bridge
  to Independence runs 19 to 21 (age of majority is 19).
- "No general program" states (DE, IA, KS, MS, MT, UT, WI): each
  claim is backed in the dataset by Child Welfare Information
  Gateway plus a statute/policy citation; the data states each
  state's alternative plainly instead of leaving a gap.
- Florida agency URL is the DCF page on the development host
  (development.myflfamilies.com) — curl-confirmed live 200; the
  guessed production path 404s, so the live URL stays.
- Connecticut agency URL is DCF's official "Road to Fostering" PDF
  on portal.ct.gov — curl-confirmed live 200.
- Minnesota agency URL is the DHS foster-care licensing overview
  document (edocs.dhs.state.mn.us) — curl-confirmed live 200.
- Maryland agency URL SWAPPED from the researcher's county-specific
  Howard County Ready by 21 page to the statewide DHS Out-of-Home
  Care page https://dhs.maryland.gov/out-of-home-care/ (verified
  live 200).
- Kentucky legal aid SWAPPED to Legal Aid of the Bluegrass
  (https://lablaw.org/, live 200) for consistency with topics
  #108/#109; the researcher had used the Louisville-only Legal Aid
  Society.
- Georgia legal aid SWAPPED to the statewide Georgia Legal Services
  Program (https://www.glsp.org/, live 200) for consistency with
  topics #108/#109; the researcher had used metro-only Atlanta
  Legal Aid.

Headline counts (computed from the dataset): 43 states let a young
person stay in foster care past 18 — most to age 21, Idaho and Maine
to 23, Massachusetts to 22 (23 while finishing an associate's degree
or higher). 7 states have no general extended foster care program to
21 (Delaware, Iowa, Kansas, Mississippi, Montana, Utah, Wisconsin) —
each offers other help instead, stated per state. Youth age out at 18
in most states; at 19 in Nebraska and Alabama. No phone numbers in
the dataset.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "foster-care-youth-aging-out" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-foster-care-youth-aging-out.jpg"

SLUG = "foster-care-youth-aging-out"
TITLE = "Foster Care & Youth Aging Out"
PREV_SLUG = "timeshare-exit"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="foster-care-youth-aging-out-in-{slug}">Foster care &amp; youth aging out in {esc(state)}</h2>'
    )
    parts.append(
        "<p>Every year, thousands of young people turn 18 while in "
        "foster care — and that birthday can mean losing the home, the "
        "caseworker, and the support they have had for years. But "
        "turning 18 does not have to mean being on your own. In "
        "<strong>43 states</strong> a young person who turns 18 in "
        "foster care can choose to stay in care — usually until "
        "<strong>age 21</strong>, and to <strong>age 23</strong> in "
        "Idaho and Maine. In <strong>7 states</strong> (Delaware, "
        "Iowa, Kansas, Mississippi, Montana, Utah, and Wisconsin) "
        "there is no general extended foster care program, but each of "
        "those states offers other help instead, and the card below "
        "says what it is. And even after care ends, former foster "
        "youth can usually keep <strong>Medicaid until age 26</strong> "
        "and get up to <strong>$5,000 a year</strong> in Education and "
        "Training Voucher money for college or job training. The "
        "picture here is as of <strong>November 2026</strong>. This is "
        "general information, not legal advice.</p>"
    )
    # --- Card 1: aging out ---
    parts.append('<div class="card">')
    parts.append("<h3>Aging out: what happens at 18</h3>")
    parts.append(
        "<p>In most states, foster care ends at <strong>age 18</strong> "
        "— the court case closes, the foster home placement ends, and "
        "the young person is legally an adult. Two states are "
        "different: in <strong>Nebraska</strong> the age of majority "
        "is 19, so youth age out at 19, and in <strong>Alabama</strong> "
        "no youth ages out before 19. Before the birthday, the agency "
        "is supposed to build a transition plan with the young person "
        "— housing, health care, school or work, and important "
        "documents like a birth certificate, Social Security card, "
        "state ID, and medical records. If that plan was never made, "
        "ask the caseworker for it now: it is much harder to get "
        "those papers later, after the case is closed.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you are in care "
        "and near 18, ask your caseworker for your transition plan and "
        "for copies of your birth certificate, Social Security card, "
        "ID, and medical records. If you already left care and never "
        "got them, contact the agency linked in the card below — it "
        "can usually still help you get copies.</p>"
    )
    parts.append("</div>")
    # --- Card 2: staying in care longer ---
    parts.append('<div class="card">')
    parts.append("<h3>Staying in care longer: extended foster care</h3>")
    parts.append(
        "<p>In 43 states, a young person who turns 18 in foster care "
        "can <strong>voluntarily stay in care</strong> — usually until "
        "age 21 — by signing a voluntary agreement with the agency. "
        "To stay, the young person generally has to be doing one of "
        "these: finishing high school or a GED, enrolled in college or "
        "job training, in a program that helps them find work, working "
        "at least <strong>80 hours a month</strong>, or unable to do "
        "those things because of a medical condition. Many states also "
        "let a young person who left at 18 <strong>come back</strong> "
        "before 21 and re-enter care. Idaho and Maine go to 23, and "
        "Massachusetts goes to 22 — or 23 while finishing an "
        "associate&rsquo;s degree or higher. The 7 states without a "
        "general program still offer help: aftercare services, "
        "housing support, stipends, or a narrower route to stay in "
        "placement, and the card below spells out each one.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Before you turn "
        "18, tell your caseworker you want to stay in extended care "
        "and sign the voluntary agreement. If you already left and "
        "are still under 21 (under 23 in Idaho and Maine), contact "
        "the agency in the card below and ask about re-entering — "
        "most states allow it.</p>"
    )
    parts.append("</div>")
    # --- Card 3: help after leaving ---
    parts.append('<div class="card">')
    parts.append("<h3>Help after you leave care</h3>")
    parts.append(
        "<p>Leaving care does not cut off all help. A young person who "
        "was in foster care at 18 can usually keep <strong>Medicaid "
        "until age 26</strong>, with no income test. The federal "
        "Education and Training Voucher (ETV) program offers up to "
        "<strong>$5,000 a year</strong> for college or job training. "
        "The Chafee program — called the Independent Living Program "
        "in many states — helps with life skills, education, jobs, "
        "and housing, often up to age 23. Some states add their own "
        "help: tuition waivers at public colleges, Foster Youth to "
        "Independence (FYI) housing vouchers, and monthly stipends. "
        "The exact mix varies by state, and the card below lists what "
        "your state offers.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you were in "
        "foster care at 18, apply for Medicaid in the former-foster-"
        "youth category — you should not need to prove low income. "
        "Ask the agency or your old caseworker about ETV money and "
        "Chafee services before you pay for any class or training "
        "out of pocket.</p>"
    )
    parts.append("</div>")
    # --- Card 4: kinship care ---
    parts.append('<div class="card">')
    parts.append("<h3>Relatives and kinship care</h3>")
    parts.append(
        "<p>When a child has to leave home, every state tries "
        "<strong>relatives first</strong> — grandparents, aunts and "
        "uncles, older siblings, and other family, plus close family "
        "friends (often called fictive kin). Relatives can usually "
        "become licensed foster parents for the child in their family "
        "and receive the same foster care payments as any other foster "
        "parent; several states now have separate, simpler licensing "
        "standards for relatives. Relatives who become the child&rsquo;s "
        "legal guardian can often get guardianship assistance, and "
        "some states pay a subsidy until the young person turns 21. "
        "If you are a relative raising a child, you do not have to "
        "figure this out alone — the agency and the legal aid "
        "organization in the card below can walk you through it.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If a child in "
        "your family is entering care, tell the caseworker right away "
        "that you are willing to take the child — relatives get "
        "priority, but only if the agency knows you exist. Ask about "
        "becoming a licensed kinship foster parent so the placement "
        "comes with financial support.</p>"
    )
    parts.append("</div>")
    # --- Card 5: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Foster care &amp; youth aging out in {esc(state)}</h3>")
    parts.append(f"<p><strong>How foster care works here:</strong> {esc(e['foster_overview'])}</p>")
    parts.append(f"<p><strong>When youth age out:</strong> {esc(e['aging_out_age'])}</p>")
    parts.append(f"<p><strong>Staying in care longer:</strong> {esc(e['extended_care'])}</p>")
    parts.append(f"<p><strong>Help after leaving care:</strong> {esc(e['benefits_after'])}</p>")
    parts.append(f"<p><strong>Becoming a foster parent:</strong> {esc(e['become_foster_parent'])}</p>")
    parts.append(f"<p><strong>Kinship care:</strong> {esc(e['kinship_care'])}</p>")
    parts.append(
        f"<p><strong>State agency:</strong> "
        f'<a href="{esc(e["agency_url"])}" target="_blank" rel="noopener">{esc(e["agency_name"])}</a>. '
        f"Start here for foster care, extended care, and aftercare services.</p>"
    )
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
    )
    parts.append(
        f"<p><strong>What to do:</strong> If you are in care and near "
        f"18, ask your caseworker about staying in extended care and "
        f"get your transition plan and documents now. If you already "
        f"left care, contact the agency above about re-entering, "
        f"Medicaid to 26, and Education and Training Voucher money — "
        f"and get free help from the organization linked above before "
        f"you sign anything or give up on benefits you may be owed.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) If you are in "
        "care and near 18, ask your caseworker about extended foster "
        "care and sign the voluntary agreement before your birthday. "
        "(2) Get your birth certificate, Social Security card, ID, "
        "and medical records while the case is still open. (3) After "
        "care ends, apply for Medicaid as a former foster youth and "
        "ask about Education and Training Voucher money and Chafee "
        "services. (4) If you are a relative, tell the agency you "
        "will take the child and ask about licensed kinship care.</p>"
    )
    parts.append(
        "<p><em>Sources: the official state child welfare agencies, "
        "state statutes, and legal aid organizations linked in the "
        "research for this section, checked November 20, 2026. In 43 "
        "states a young person can stay in foster care past 18 — "
        "usually to 21, to 23 in Idaho and Maine; Delaware, Iowa, "
        "Kansas, Mississippi, Montana, Utah, and Wisconsin have no "
        "general extended foster care program to 21, but offer other "
        "help as described above. Confirm the current law with a "
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
        anchor = f"{SLUG}-in-{slug}"
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
            f"Foster care &amp; youth aging out in {state}</a></li>\n"
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
        r'<option value="timeshare-exit" data-anchor="timeshare-exit">.*?</option>',
        text,
        re.S,
    )
    assert m, "timeshare-exit helper option not found"
    opt_old = m.group(0)
    opt_new = (
        opt_old
        + '\n<option value="foster-care-youth-aging-out" data-anchor="foster-care-youth-aging-out">'
        "Foster care &amp; youth aging out — what happens at 18, staying in care to 21, help after you leave, and becoming a foster or kinship parent</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="timeshare-exit"'
    idx = text.find(card_anchor)
    assert idx != -1, "timeshare-exit card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="foster-care-youth-aging-out">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-foster-care-youth-aging-out.jpg" alt="Foster Care &amp; Youth Aging Out" loading="lazy"></span>
          <h3>Foster Care &amp; Youth Aging Out</h3>
          <p>Turning 18 in foster care? What aging out means, how to stay in care to 21, Medicaid and college help after you leave, and how relatives and foster parents fit in — state by state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 63 topics" in text, "show-all label not found"
    text = text.replace("Show all 63 topics", "Show all 64 topics", 1)
    show_pos = text.find("Show all 64 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">63 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("63 topics", "64 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 63->64")


def build_about():
    text = ABOUT.read_text()
    assert text.count("108 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("108 legal topics", "109 legal topics", 1))
    print("  about.html: 108 -> 109")


def state_index_t(state, slug, e):
    bits = [
        "foster care aging out extended foster care youth transition kinship",
        f"Foster care & youth aging out in {state}",
        f"when youth age out {e['aging_out_age']}",
        f"staying in care longer {e['extended_care']}",
        f"help after leaving care {e['benefits_after']}",
        f"becoming a foster parent {e['become_foster_parent']}",
        f"kinship care {e['kinship_care']}",
        f"{e['agency_name']} {e['legal_aid_name']}",
        "Medicaid to 26 education training voucher Chafee independent living housing transition plan",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11926, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = e["state"]
        slug = e.get("slug") or key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Foster care & youth aging out in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Foster Care & Youth Aging Out",
            "t": (
                "foster-care-youth-aging-out Foster Care & Youth Aging Out? "
                "Turning 18 in foster care? What aging out means, how to stay in care to 21, Medicaid and "
                "college help after you leave, and how relatives and foster parents fit in — state by state. "
                "aging out extended foster care to 21 Medicaid to 26 education training voucher Chafee "
                "independent living kinship care foster parent transition plan."
            ),
        }
    )
    assert len(idx) == 11977, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11926 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    assert len(d) == 50, len(d)
    data = [(k, d[k]) for k in sorted(d)]  # keys already lowercase
    slugs = [(e.get("slug") or k.replace(" ", "-")) for k, e in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "agency_name", "agency_url", "aging_out_age", "become_foster_parent",
        "benefits_after", "extended_care", "foster_overview", "kinship_care",
        "legal_aid_name", "legal_aid_url", "sources", "state",
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
        assert e["agency_name"] and e["agency_url"] and e["aging_out_age"] and e["become_foster_parent"] and e["benefits_after"] and e["extended_care"] and e["foster_overview"] and e["kinship_care"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"] and e["state"], f"{k}: empty required field"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        # OAR rule numbers (e.g. Oregon's OAR 413-030-0220) look like
        # phone numbers to the regex but are statute citations, not
        # phone numbers — strip them before the scan.
        blob = re.sub(r"OAR \d{3}-\d{3}-\d{4}", "OAR RULE", blob)
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before timeshare-exit section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
