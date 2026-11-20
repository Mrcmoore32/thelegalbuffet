#!/usr/bin/env python3
"""Build Topic #103: Adverse Possession & Easements — standalone section on
all 50 state pages.

Inserts one new section per state page (before Data Breach Response,
newest-first), a contents-list entry (before the data-breach-response
<li>), a homepage helper option + topic card (after Data Breach
Response), bumps About 101 -> 102, and appends 50 state entries + 1
helper entry to assets/search-index.json (11569 -> 11620).

Data: hidden_files/topic-research/adverse-possession-easements/all-states.json
(coordinator-merged 2026-11-20 from 5 research batches; one transcription
fix: Colorado easement_by_necessity_note restored from the researcher's
payload. Two URL fixes by the coordinator 2026-11-20: PA agency URL
replaced (old pabar.org/lrsblurb.asp 404s; new Find-a-Lawyer page curl
200) and ME agency URL replaced (old /page/AttorneyRequest 403s even to
the text fetcher; new /page/LawyerReferralService confirmed live with
real content).
URL verification 2026-11-20: 84/100 curl 200; 6 curl 000 confirmed
alive by text fetch (CA LawHelpCA x2, NY Legal Aid Society, OR bar,
RI bar, WV Legal Aid); 8 curl 403 confirmed alive by text fetch (AZ
CLS, ID Legal Aid, MD courts, MA mass.gov AP page, MA GBLS, MN courts,
MT statute PDF, NH courts); ME + PA replaced as above. No phone
numbers in the dataset.
Headline counts (computed from the merged dataset): adverse possession
standard period 5 years 3 states (CA, MT, NV) / 7 years 3 (AR, FL, UT)
/ 10 years 16 / 15 years 8 / 18 years 1 (CO) / 20 years 15 / 21 years
2 (OH, PA) / 30 years 2 (LA standard acquisitive prescription, NJ).
Prescriptive easement 20 years in 20 states (most common); in 5 states
the easement clock is LONGER than the ownership clock: FL 7->20,
IN 10->20, SC 10->20, UT 7->20, VA 15->20. Every state recognizes
easements by necessity in some form (Louisiana's civil-law equivalent
is the enclosed-estate right of passage, CC art. 689; North Dakota's
note flags that no ND-specific statute or case was verified).
Spot-verifications (coordinator, Nov 20, 2026): IN prescriptive
easement 20 years (IC 32-23-1-1, Justia text); UT prescriptive
easement 20 years (Van Denburgh v. Sweeney Land Co., 2013 UT App 265;
Utah Code 78B-2-206); MT 5 years + full tax payment (Mont. Code Ann.
70-19-411, statute text read); NJ 30 years (J & M Land Co. v. First
Union, 166 N.J. 493 (2001), as researched).
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "adverse-possession-easements" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-adverse-possession-easements.jpg"

SLUG = "adverse-possession-easements"
TITLE = "Adverse Possession & Easements"
PREV_SLUG = "data-breach-response"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="adverse-possession-easements-in-{slug}">Adverse possession &amp; easements in {esc(state)}</h2>'
    )
    parts.append(
        "<p>Someone has been using a piece of your land for years — "
        "mowing it, parking on it, driving across it to reach their own "
        "place. In every state, long enough use can change the legal "
        "picture: in <strong>3 states the clock for taking ownership is "
        "only 5 years</strong>, in <strong>16 states it is 10 years</strong>, "
        "and in <strong>15 states it is 20 years</strong>. But using land "
        "is not the same as owning it — a driveway used for decades can "
        "become a permanent right to keep using it, without ever changing "
        "who owns the land. And if your own land has no road to it at "
        "all, every state has some path to get access. The picture here "
        "is as of <strong>November 2026</strong>. This is general "
        "information, not legal advice.</p>"
    )
    # --- Card 1: what is adverse possession? ---
    parts.append('<div class="card">')
    parts.append("<h3>What is adverse possession?</h3>")
    parts.append(
        "<p>Adverse possession is how someone can gain ownership of land "
        "they do not hold the deed to, by using it as if it were theirs "
        "for a long time. The use has to meet five tests in almost every "
        "state: <strong>actual</strong> (they really use it), "
        "<strong>open and notorious</strong> (visible, not hidden), "
        "<strong>hostile</strong> (without the owner&rsquo;s permission — "
        "&ldquo;hostile&rdquo; means without permission, not angry), "
        "<strong>exclusive</strong> (they treat it as their own), and "
        "<strong>continuous</strong> (unbroken for the whole period). "
        "Failing even one test defeats the claim.</p>"
    )
    parts.append(
        "<p>Permission is the killer of these claims: if the owner ever "
        "said &ldquo;go ahead,&rdquo; the use was not hostile, and the "
        "clock never ran. Ownership also does not change by itself — the "
        "person claiming the land usually has to go to court and win a "
        "case called a quiet title action. And land owned by the "
        "government generally cannot be taken this way at all.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If someone is using "
        "your land without permission, do not wait: give them written "
        "permission (which stops the clock), put up a fence or a "
        "&ldquo;no trespassing&rdquo; sign, or talk to a lawyer before "
        "the years run out. If you are the one using the land, keep "
        "records — photos, tax receipts, dates — and talk to a lawyer "
        "before assuming the land is yours.</p>"
    )
    parts.append("</div>")
    # --- Card 2: how long is the clock? ---
    parts.append('<div class="card">')
    parts.append("<h3>How long is the clock?</h3>")
    parts.append(
        "<p>The standard period for taking ownership is <strong>5 years "
        "in 3 states</strong> (California, Montana, and Nevada), "
        "<strong>7 years in 3</strong> (Arkansas, Florida, and Utah), "
        "<strong>10 years in 16</strong>, <strong>15 years in 8</strong>, "
        "<strong>18 years in 1</strong> (Colorado), <strong>20 years in "
        "15</strong>, <strong>21 years in 2</strong> (Ohio and "
        "Pennsylvania), and <strong>30 years in 2</strong> (Louisiana, "
        "under its civil-law acquisitive prescription, and New "
        "Jersey).</p>"
    )
    parts.append(
        "<p>The headline number is rarely the whole story. In many "
        "states a flawed deed (called &ldquo;color of title&rdquo;) or "
        "paying the property taxes can shorten the clock — for example, "
        "Texas drops from 10 years to 3 with a deed, and Illinois from "
        "20 to 7 with a deed plus taxes. In other states the taxes are "
        "mandatory: California, Montana, Nevada, Utah, New Mexico, "
        "Idaho, and Indiana all require the claimant to have paid the "
        "taxes, and a claim can fail on that alone. Colorado added a "
        "good-faith rule in 2008: a claimant who knew the land was not "
        "theirs cannot win, and may have to pay the former owner the "
        "land&rsquo;s value.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check your "
        "state&rsquo;s card below for the exact number and the extras "
        "that apply — a deed, tax payments, or good faith can change "
        "everything. Do not count on the shortest number you have heard; "
        "it usually comes with a condition.</p>"
    )
    parts.append("</div>")
    # --- Card 3: prescriptive easements ---
    parts.append('<div class="card">')
    parts.append("<h3>Prescriptive easements: use without ownership</h3>")
    parts.append(
        "<p>A prescriptive easement is a permanent right to keep using "
        "someone else&rsquo;s land for one purpose — a driveway, a path, "
        "a road — without owning any of it. The use has to be open, "
        "continuous, and without permission for the state&rsquo;s "
        "period, which is <strong>20 years in 20 states</strong>, the "
        "most common number. Unlike adverse possession, the use does not "
        "usually have to be exclusive: the owner can keep using the land "
        "too.</p>"
    )
    parts.append(
        "<p>In <strong>5 states the easement clock is longer than the "
        "ownership clock</strong>: Florida (7 years to own, 20 to use), "
        "Indiana (10 to own, 20 to use), South Carolina (10 to own, 20 "
        "to use), Utah (7 to own, 20 to use), and Virginia (15 to own, "
        "20 to use). So a neighbor can win ownership of a strip faster "
        "than they can win a right to drive over it — the two clocks run "
        "separately.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If a neighbor has "
        "been crossing your land for years, a written permission letter "
        "stops the easement clock — permission can never ripen into a "
        "right. If you are the one crossing, keep a record of when the "
        "use started and whether anyone ever objected.</p>"
    )
    parts.append("</div>")
    # --- Card 4: landlocked / easements by necessity ---
    parts.append('<div class="card">')
    parts.append("<h3>Landlocked? Easements by necessity</h3>")
    parts.append(
        "<p>If your land has no road to it, you are not stuck forever. "
        "Every state recognizes some form of easement by necessity: when "
        "one owner splits a piece of land and leaves one part with no "
        "access, the law implies a right to cross the other part to "
        "reach a public road. The usual requirements are that the two "
        "parcels were once owned by the same person, and that the need "
        "for access existed when they were split.</p>"
    )
    parts.append(
        "<p>The easement lasts only while the necessity lasts — if a new "
        "road reaches your land later, it can end. Some states also have "
        "a statutory route: a landlocked owner can ask a court or county "
        "board to lay out a private road, usually paying the neighbor "
        "for the strip taken. Louisiana reaches the same result through "
        "its civil law: the owner of an &ldquo;enclosed estate&rdquo; "
        "may claim a right of passage, but must pay the neighbor for "
        "it.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you cannot reach "
        "your own land, start with your deed and the history of how the "
        "land was split — that history is what the court looks at. The "
        "legal aid or bar referral linked in your state&rsquo;s card can "
        "tell you whether your state&rsquo;s court route or statutory "
        "road process fits.</p>"
    )
    parts.append("</div>")
    # --- Card 5: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Adverse possession &amp; easements in {esc(state)}</h3>")
    parts.append(
        f"<p><strong>How long to claim ownership:</strong> {e['adverse_possession_years']} years. {esc(e['adverse_possession_note'])}</p>"
    )
    parts.append(
        f"<p><strong>How long for a prescriptive easement:</strong> {e['prescriptive_easement_years']} years. {esc(e['prescriptive_easement_note'])}</p>"
    )
    parts.append(
        f"<p><strong>Landlocked land:</strong> {esc(e['easement_by_necessity_note'])}</p>"
    )
    parts.append(
        f"<p><strong>The law:</strong> {esc(e['statute_name'])} — {esc(e['statute_cite'])}</p>"
    )
    parts.append(
        f"<p><strong>Where to get help:</strong> "
        f'<a href="{esc(e["agency_url"])}" target="_blank" rel="noopener">{esc(e["agency_name"])}</a>.</p>'
    )
    if e["state_note"]:
        parts.append(f"<p>{esc(e['state_note'])}</p>")
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If someone is using "
        "your land, act before the clock runs out: written permission, a "
        "fence, or a lawyer&rsquo;s letter. If you need access to your "
        "own land, gather your deed and the history of the split, then "
        "talk to the legal aid above before any deadline passes.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) If someone uses "
        "your land without permission, give written permission or stop "
        "the use — do not let years pass silently. (2) If you use a "
        "neighbor&rsquo;s land, write down when it started and keep "
        "proof. (3) If your land has no road, pull your deed and the "
        "history of the split. (4) For a boundary fight or a claim of "
        "ownership, talk to a lawyer before the clock in your state runs "
        "out — these cases are won and lost on the details.</p>"
    )
    parts.append(
        "<p><em>Sources: the official state adverse possession and "
        "easement statutes, state courts, state bars, and legal aid "
        "organizations linked in the research for this section, checked "
        "November 20, 2026. Property laws change — confirm the current "
        "law with a local attorney before you rely on it. This is general "
        "information, not legal advice.</em></p>"
    )
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def build_state_pages(data):
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
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
            f"Adverse possession &amp; easements in {state}</a></li>\n"
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
    opt_old = (
        '<option value="data-breach-response" data-anchor="data-breach-response">'
        "Data breach response (notice deadlines, attorney general notice, credit monitoring, can you sue)</option>"
    )
    assert opt_old in text, "data breach helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="adverse-possession-easements" data-anchor="adverse-possession-easements">'
        "Adverse possession &amp; easements (how long use can take land, prescriptive easements, landlocked access)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="data-breach-response"'
    idx = text.find(card_anchor)
    assert idx != -1, "data breach card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="adverse-possession-easements">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-adverse-possession-easements.jpg" alt="Adverse possession &amp; easements" loading="lazy"></span>
          <h3>Adverse Possession &amp; Easements</h3>
          <p>Someone has been using your land for years &mdash; or you have no way to reach your own land. When long use can change ownership, when a driveway becomes a legal right, and how landlocked owners get access &mdash; state by state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 56 topics" in text, "show-all label not found"
    text = text.replace("Show all 56 topics", "Show all 57 topics", 1)
    show_pos = text.find("Show all 57 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">56 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("56 topics", "57 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 56->57")


def build_about():
    text = ABOUT.read_text()
    assert text.count("101 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("101 legal topics", "102 legal topics", 1))
    print("  about.html: 101 -> 102")


def state_index_t(state, slug, e):
    bits = [
        "adverse possession easements prescriptive easement easement by necessity landlocked property boundary",
        f"Adverse possession & easements in {state}",
        f"adverse possession {e['adverse_possession_years']} years {e['adverse_possession_note']}",
        f"prescriptive easement {e['prescriptive_easement_years']} years {e['prescriptive_easement_note']}",
        f"easement by necessity landlocked {e['easement_by_necessity_note']}",
        f"{e['statute_name']} {e['statute_cite']}",
        f"{e['agency_name']}",
        f"{e['state_note'] or ''}",
        f"{e['legal_aid_name']}",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11569, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Adverse possession & easements in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Adverse Possession & Easements",
            "t": (
                "adverse-possession-easements Adverse Possession & Easements? "
                "Someone has been using your land for years — or you have no way to reach your own land. "
                "When long use can change ownership, when a driveway becomes a legal right, "
                "and how landlocked owners get access — state by state. "
                "adverse possession prescriptive easement easement by necessity landlocked boundary quiet title."
            ),
        }
    )
    assert len(idx) == 11620, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11569 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    assert len(d) == 50, len(d)
    data = [(k, d[k]) for k in sorted(d)]  # keys already lowercase
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "adverse_possession_years", "adverse_possession_note",
        "prescriptive_easement_years", "prescriptive_easement_note",
        "easement_by_necessity_note", "statute_name", "statute_cite",
        "agency_name", "agency_url", "legal_aid_name", "legal_aid_url",
        "state_note", "sources",
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
        assert isinstance(e["adverse_possession_years"], int), f"{k}: bad AP years"
        assert isinstance(e["prescriptive_easement_years"], int), f"{k}: bad PE years"
        assert e["adverse_possession_note"] and e["prescriptive_easement_note"] and e["easement_by_necessity_note"] and e["statute_name"] and e["statute_cite"] and e["agency_name"] and e["agency_url"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"], f"{k}: empty required field"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before data-breach-response section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
