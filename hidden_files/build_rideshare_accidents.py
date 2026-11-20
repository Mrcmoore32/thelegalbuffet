#!/usr/bin/env python3
"""Build Topic #104: Rideshare Accidents (Uber & Lyft) — standalone section
on all 50 state pages.

Inserts one new section per state page (before Adverse Possession &
Easements, newest-first), a contents-list entry (before the
adverse-possession-easements <li>), a homepage helper option + topic
card (after Adverse Possession & Easements), bumps About 102 -> 103,
and appends 50 state entries + 1 helper entry to
assets/search-index.json (11620 -> 11671).

Data: hidden_files/topic-research/rideshare-accidents/all-states.json
(coordinator-merged 2026-11-20 from 5 research batches).
URL verification 2026-11-20: 86/100 curl 200; 14 confirmed alive by
text fetch (AL agency, AK agency, AZ agency, AZ legal aid, CA legal
aid, ID legal aid, MA agency, MA legal aid, MS legal aid, MT agency,
PA legal aid [palawhelp.org root live, crawled 5h before], RI agency,
WV legal aid, WY statute page). No phone numbers in the dataset.
Headline counts (computed from the merged dataset): trip-period
(Periods 2-3) statutory liability floor is $1,000,000 in 39 states;
non-standard in 11 — higher in 4 (MN, NJ, RI $1,500,000; NY
$1,250,000 + $1,250,000 SUM), lower in 4 (PA $500,000; KY statutory
floor $100,000/$300,000/$50,000; MD flat $50,000/$100,000/$25,000
for all periods; NH $300,000), split in 2 (AZ Period 2 $250,000 /
Period 3 $1,000,000; TX Period 2 drops to $50,000/$100,000/$25,000
for policies renewed on/after Jan 1, 2026 under HB 3520), and Oregon
has no statewide tiered liability law (Portland City Code model).
Personal-injury SOL: 1 year 1 (TN), 2 years 25, 3 years 17, 4 years 3
(NE, UT, WY), 5 years 1 (MO), 6 years 3 (MN, ME, ND).
Spot-verifications (coordinator, Nov 20, 2026, statute text read):
PA $500,000 (66 Pa.C.S. § 2603.1(a)(3)); NY $1,250,000 + $1,250,000
SUM (DFS FAQ Q12, VTL Art. 44-B; NYC-origin trips excluded);
CA SB 371 cut passenger-period UM/UIM from $1,000,000 to
$60,000/$300,000, effective Jan 1, 2026 (Pub. Util. Code § 5433(b)(2));
TX HB 3520 moved Period 2 to $50,000/$100,000/$25,000, application
prospective Jan 1, 2026 (Tex. Ins. Code §§ 1954.052-1954.053);
MD § 10-405 flat $50,000/$100,000/$25,000 for all periods;
AZ HB 2729 Period 2 $250,000 / Period 3 $1,000,000, Period 1
$25,000/$50,000/$20,000 (A.R.S. § 28-4038); MN $1,500,000 P2/P3
plus a separate driver personal-injury policy (Minn. Stat.
§ 65B.472(c)-(d)); RI $1,500,000 (R.I. Gen. Laws § 39-14.2-14(c));
KY prearranged-ride floor is the subsection (4) table
$100,000/$300,000/$50,000 (KRS 281.655(12)); NH $300,000 (RSA
359-U:8(IV)). NH citation corrected by the coordinator: RSA ch.
376-A was repealed and replaced by RSA ch. 359-U effective July 1,
2023 — the $300,000 floor is confirmed in current RSA 359-U:8(IV),
and all NH citations in the dataset were updated from 376-A to 359-U.
WY figures confirmed in the Justia fetch of Wyo. Stat. § 31-20-107
(Period 1 $50,000/$100,000/$25,000 + UM; prearranged ride
$1,000,000 + UM).
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "rideshare-accidents" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-rideshare-accidents.jpg"

SLUG = "rideshare-accidents"
TITLE = "Rideshare Accidents (Uber & Lyft)"
PREV_SLUG = "adverse-possession-easements"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="rideshare-accidents-in-{slug}">Rideshare accidents (Uber &amp; Lyft) in {esc(state)}</h2>'
    )
    parts.append(
        "<p>You were hurt in an Uber or a Lyft — as a passenger, as "
        "another driver, or as a pedestrian. Which insurance pays "
        "depends on what the rideshare driver was doing in the app when "
        "the crash happened: logged off, waiting for a ride, on the way "
        "to a pickup, or carrying a passenger. In <strong>39 states the "
        "trip-period floor is $1,000,000</strong>, but in <strong>11 "
        "states the state floor is different</strong> — higher in 4 "
        "(Minnesota, New Jersey, and Rhode Island at $1,500,000; New "
        "York at $1,250,000), lower in 4 (Pennsylvania at $500,000; "
        "Kentucky, Maryland, and New Hampshire lower still), split "
        "between the drive to the pickup and the ride itself in 2 "
        "(Arizona and Texas), and Oregon has no statewide tiered law at "
        "all. The deadline to file is also short in most states — "
        "<strong>2 years in 25 states and 3 years in 17</strong>, and "
        "just <strong>1 year in Tennessee</strong>. The picture here is "
        "as of <strong>November 2026</strong>. This is general "
        "information, not legal advice.</p>"
    )
    # --- Card 1: the three periods ---
    parts.append('<div class="card">')
    parts.append("<h3>The three periods decide whose insurance pays</h3>")
    parts.append(
        "<p>Every rideshare trip is split into periods, and the coverage "
        "changes with each one. <strong>App off:</strong> the driver is "
        "off duty, and only their personal auto policy applies. "
        "<strong>Period 1 — app on, waiting for a ride:</strong> the "
        "thinnest coverage, usually $50,000 per person / $100,000 per "
        "accident for injuries and $25,000 for property damage. "
        "<strong>Period 2 — ride accepted, driving to the pickup:</strong> "
        "the bigger policy switches on. <strong>Period 3 — passenger in "
        "the car:</strong> the same big policy, usually $1,000,000. "
        "Periods 2 and 3 are usually covered by one policy, so the "
        "moment that matters most is whether a ride had been accepted "
        "yet.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Write down the "
        "exact time of the crash and screenshot the ride in the app — "
        "the trip status, the driver&rsquo;s name and photo, and the "
        "car&rsquo;s plate. That screenshot is what proves which period "
        "you were in. Report the crash in the app the same day, get "
        "medical care even if you feel okay, and keep every bill and "
        "receipt.</p>"
    )
    parts.append("</div>")
    # --- Card 2: when the floor is not $1M ---
    parts.append('<div class="card">')
    parts.append("<h3>When the state floor is NOT $1,000,000</h3>")
    parts.append(
        "<p>Most people have heard &ldquo;a million dollars&rdquo; — and "
        "in 39 states that is the law once a ride is accepted. But the "
        "exceptions are big. <strong>Higher:</strong> Minnesota, New "
        "Jersey, and Rhode Island require $1,500,000 on a trip, and New "
        "York requires $1,250,000 plus another $1,250,000 in "
        "uninsured-motorist coverage. <strong>Lower:</strong> "
        "Pennsylvania&rsquo;s trip minimum is only $500,000; New "
        "Hampshire&rsquo;s is $300,000; Kentucky&rsquo;s statutory floor "
        "for a ride is $100,000/$300,000/$50,000; and Maryland&rsquo;s "
        "law never rises above $50,000/$100,000/$25,000 at all — the "
        "$1,000,000 you hear about there is the companies&rsquo; own "
        "policy, not the law. <strong>Split:</strong> in Arizona the "
        "drive to the pickup is $250,000 and only the passenger ride is "
        "$1,000,000, and in Texas the en-route period drops to "
        "$50,000/$100,000/$25,000 for policies renewed on or after "
        "January 1, 2026. <strong>Oregon</strong> has no statewide "
        "tiered law — the tiers come from city rules, with Portland as "
        "the model.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Do not assume the "
        "$1,000,000 figure. Check your state&rsquo;s card below for the "
        "real floor — and remember the crash date decides which version "
        "of the law applies, because several of these limits changed in "
        "2025 and 2026.</p>"
    )
    parts.append("</div>")
    # --- Card 3: your own policy probably won't help ---
    parts.append('<div class="card">')
    parts.append("<h3>Your own policy probably won&rsquo;t help — and that&rsquo;s normal</h3>")
    parts.append(
        "<p>Most personal auto policies exclude driving for hire. That "
        "means the rideshare driver&rsquo;s own insurer can deny the "
        "claim outright once the app was on — and that is exactly what "
        "the rideshare policy is for. In nearly every state the "
        "rideshare coverage is <strong>primary</strong> (it pays first, "
        "not as a backup) and <strong>first-dollar</strong> (it pays "
        "from the first dollar if the driver&rsquo;s own coverage lapsed "
        "or does not cover the crash). In most states it also does not "
        "wait for the personal insurer to deny the claim first.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you are the "
        "passenger, file the claim with the rideshare company — Uber and "
        "Lyft both have in-app crash reporting — and do not let anyone "
        "tell you to wait for the driver&rsquo;s personal insurer. If "
        "you are the other driver, get the rideshare driver&rsquo;s "
        "insurance information at the scene, the same as any crash, and "
        "report it to your own insurer too.</p>"
    )
    parts.append("</div>")
    # --- Card 4: uninsured drivers and the deadline ---
    parts.append('<div class="card">')
    parts.append("<h3>Uninsured drivers and the deadline</h3>")
    parts.append(
        "<p>Uninsured and underinsured motorist coverage — the coverage "
        "that pays when the driver who hit you has no insurance or not "
        "enough — varies more than the liability limits do. Delaware and "
        "Vermont require $1,000,000 of it during a ride. California cut "
        "theirs from $1,000,000 to $60,000 per person / $300,000 per "
        "incident on January 1, 2026. In Louisiana, Uber&rsquo;s written "
        "waiver of that coverage has been upheld in court, so do not "
        "count on company UM coverage there. In Tennessee, a company can "
        "opt out of it in Period 1, leaving a real gap.</p>"
    )
    parts.append(
        "<p>The filing deadline is just as uneven. Most states give you "
        "<strong>2 or 3 years</strong> from the crash, but Tennessee "
        "gives only <strong>1 year</strong>, Missouri gives 5, and "
        "Minnesota, Maine, and North Dakota give 6. Some states add "
        "shorter clocks on top: in New York a no-fault claim must be "
        "filed within 30 days of the crash, and claims against a city or "
        "other government body often need a written notice in 90 days or "
        "less.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Do not wait to see "
        "how you feel. Get checked the same day, keep the records, and "
        "find out your state&rsquo;s deadline from the card below — in "
        "Tennessee and in no-fault states, the clock that matters may be "
        "weeks, not years.</p>"
    )
    parts.append("</div>")
    # --- Card 5: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Rideshare accidents in {esc(state)}</h3>")
    parts.append(
        f"<p><strong>Waiting for a ride (Period 1):</strong> {esc(e['period1_limits'])}</p>"
    )
    parts.append(
        f"<p><strong>On the way to you / passenger in the car (Periods 2–3):</strong> {esc(e['period2_3_limits'])}</p>"
    )
    parts.append(
        f"<p><strong>Uninsured / underinsured motorist coverage:</strong> {esc(e['um_uim_note'])}</p>"
    )
    parts.append(
        f"<p><strong>Who pays:</strong> {esc(e['who_pays_note'])}</p>"
    )
    parts.append(
        f"<p><strong>The law:</strong> {esc(e['tnc_statute'])}</p>"
    )
    parts.append(
        f"<p><strong>Deadline to file:</strong> {e['sol_years']} year{'s' if e['sol_years'] != 1 else ''}. {esc(e['sol_note'])}</p>"
    )
    parts.append(
        f"<p><strong>Who regulates rideshare:</strong> "
        f'<a href="{esc(e["agency_url"])}" target="_blank" rel="noopener">{esc(e["agency_name"])}</a>.</p>'
    )
    if e["state_note"]:
        parts.append(f"<p>{esc(e['state_note'])}</p>")
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Screenshot the ride "
        "and the driver&rsquo;s details before you leave the scene, "
        "report the crash in the app the same day, get medical care, and "
        "check the deadline above — in some states the clock that matters "
        "is measured in days, not years.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Screenshot the "
        "ride, the driver, and the car before you leave the scene. (2) "
        "Report the crash in the app the same day. (3) Get medical care "
        "even if you feel fine, and keep every bill. (4) Find your "
        "state&rsquo;s deadline in the card above and do not let it "
        "pass. (5) If the company or an insurer denies the claim, talk "
        "to the free legal aid linked above before you accept it.</p>"
    )
    parts.append(
        "<p><em>Sources: the official state transportation network "
        "company statutes, state regulators, and legal aid organizations "
        "linked in the research for this section, checked November 20, "
        "2026. Insurance laws change — several limits in this section "
        "changed in 2025 and 2026, so the crash date decides which "
        "version applies. Confirm the current law with a local attorney "
        "before you rely on it. This is general information, not legal "
        "advice.</em></p>"
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
            f"Rideshare accidents in {state}</a></li>\n"
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
        '<option value="adverse-possession-easements" data-anchor="adverse-possession-easements">'
        "Adverse possession &amp; easements (how long use can take land, prescriptive easements, landlocked access)</option>"
    )
    assert opt_old in text, "adverse possession helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="rideshare-accidents" data-anchor="rideshare-accidents">'
        "Rideshare accidents (Uber/Lyft) — whose insurance pays, the three app periods, and your state's deadline</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="adverse-possession-easements"'
    idx = text.find(card_anchor)
    assert idx != -1, "adverse possession card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="rideshare-accidents">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-rideshare-accidents.jpg" alt="Rideshare accidents (Uber &amp; Lyft)" loading="lazy"></span>
          <h3>Rideshare Accidents (Uber &amp; Lyft)</h3>
          <p>Hurt in an Uber or Lyft? Which insurance pays depends on what the driver was doing in the app when the crash happened &mdash; and the limit changes state by state. The three periods, the exceptions, and the deadline to file.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 57 topics" in text, "show-all label not found"
    text = text.replace("Show all 57 topics", "Show all 58 topics", 1)
    show_pos = text.find("Show all 58 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">57 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("57 topics", "58 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 57->58")


def build_about():
    text = ABOUT.read_text()
    assert text.count("102 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("102 legal topics", "103 legal topics", 1))
    print("  about.html: 102 -> 103")


def state_index_t(state, slug, e):
    bits = [
        "rideshare accidents uber lyft transportation network company TNC insurance periods",
        f"Rideshare accidents (Uber & Lyft) in {state}",
        f"waiting for a ride Period 1 {e['period1_limits']}",
        f"on the way passenger in the car Periods 2-3 {e['period2_3_limits']}",
        f"uninsured underinsured motorist {e['um_uim_note']}",
        f"who pays {e['who_pays_note']}",
        f"{e['tnc_statute']}",
        f"deadline to file {e['sol_years']} years {e['sol_note']}",
        f"{e['agency_name']}",
        f"{e['state_note'] or ''}",
        f"{e['legal_aid_name']}",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11620, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Rideshare accidents (Uber & Lyft) in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Rideshare Accidents (Uber & Lyft)",
            "t": (
                "rideshare-accidents Rideshare Accidents (Uber & Lyft)? "
                "Hurt in an Uber or Lyft? Which insurance pays depends on what the driver was doing in the app "
                "when the crash happened — and the limit changes state by state. The three periods, the "
                "exceptions, and the deadline to file. "
                "rideshare uber lyft TNC transportation network company insurance period 1 period 2 period 3 "
                "uninsured motorist deadline statute of limitations."
            ),
        }
    )
    assert len(idx) == 11671, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11620 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    assert len(d) == 50, len(d)
    data = [(k, d[k]) for k in sorted(d)]  # keys already lowercase
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "period1_limits", "period2_3_limits", "um_uim_note",
        "who_pays_note", "tnc_statute", "sol_years", "sol_note",
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
        assert isinstance(e["sol_years"], int), f"{k}: bad sol_years"
        assert e["period1_limits"] and e["period2_3_limits"] and e["um_uim_note"] and e["who_pays_note"] and e["tnc_statute"] and e["sol_note"] and e["agency_name"] and e["agency_url"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"], f"{k}: empty required field"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before adverse-possession-easements section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
