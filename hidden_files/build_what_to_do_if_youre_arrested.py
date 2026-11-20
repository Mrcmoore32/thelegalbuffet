#!/usr/bin/env python3
"""Build Topic #89: What to Do If You're Arrested — standalone section on all
50 state pages.

Inserts one new section per state page (before Social Security Disability &
SSI, newest-first), a contents-list entry (before the disability <li>), a
homepage helper option + topic card (after Social Security Disability & SSI),
bumps About 87 -> 88, and appends 50 state entries + 1 helper entry to
assets/search-index.json (10855 -> 10906).

Data: hidden_files/topic-research/what-to-do-if-youre-arrested/all-states.json
(coordinator-built 2026-11-20 from 5 research batches + 2 follow-up rounds;
verification notes in this docstring).

Coordinator verification before the build (Nov 20, 2026):
- Federal core vs official sources: Miranda v. Arizona (1966) — the five
  Miranda rights (ABA, Bill of Rights Institute); Gideon v. Wainwright
  (unanimous, March 18, 1963) — right to appointed counsel for those who
  cannot afford one.
- Bail/diversion notes: every state verified against official statute, court,
  or prosecutor sources. Two follow-up rounds filled the rate-limited gaps:
  batch-1 bail+diversion (10 states) and the consolidated round (17 diversion
  + 5 bail notes). Only Alaska diversion stays null BY DESIGN — the researcher
  verified there is no statewide general pretrial diversion statute (only a
  municipal Anchorage program and a proposed, not enacted, DUI bill); the
  section says so plainly and routes readers to the prosecutor.
- URLs: all 92 non-null PD + legal-aid URLs curl-checked Nov 20. 10x403 +
  2x406 are bot filters on official .gov / legal-aid domains — 7 confirmed
  alive via live browser text fetch (mass.gov/cpcs, legalaidok.org,
  mslegalservices.org, nevadalegalservices.org, lawyoming.org,
  lonestarlegal.org, plus #88's checks), same pattern as #87/#88.
  3 real problems fixed: OH PD opd.ohio.gov/wps/portal/gov/opd/home 404 ->
  https://opd.ohio.gov/ (verified alive); KS PD link was a job-openings page
  (ksbids.gov/jobopenings) -> https://www.ksbids.gov/ (agency homepage,
  verified alive); SC PD link was a Horry-County-only page ->
  https://sccid.sc.gov/ (commission homepage with Find a Defender, verified
  alive). MS/NV legal-aid 000s confirmed alive in browser.
- Phones: 24 print. Researchers verified each against a second official
  source except where noted null (batch-4 researcher: only OK (405) 801-2601
  verified on two oklahoma.gov pages; batch-2: AL/AR/CT/FL null, no second
  source; batch-5: SD/TN/TX/UT/WY null, single or conflicting sources only).
  No phone-like strings outside the phone field (asserted in main()).
- Structural notes in the data: MI (SADO) and IL (OSAD) are appellate offices
  — trial defense is county-based; NY is an oversight agency with county-based
  defense; PA has no statewide office (county PDs); TX has no statewide PD
  (county-appointed under the Fair Defense Act, TIDC oversees); AZ has no
  statewide office (Maricopa County office listed as the largest example); NE
  Commission on Public Advocacy handles serious felonies, most trial defense
  is county PDs. PD_NOTE below carries these. 8 states have no verifiable PD
  homepage URL (AZ, NY, ND, PA, SD, TN, TX, UT) — name printed without a
  link, never a guessed URL.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "what-to-do-if-youre-arrested" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-what-to-do-if-youre-arrested.jpg"

SLUG = "what-to-do-if-youre-arrested"
TITLE = "What to Do If You're Arrested"
PREV_SLUG = "social-security-disability-ssi"

# Extra context for states whose PD entry needs explaining.
PD_NOTE = {
    "arizona": "Arizona has no single statewide public defender office \u2014 defense is county-based. The Maricopa County office above is the state\u2019s largest.",
    "illinois": "The Office of the State Appellate Defender handles appeals. Trial-level public defenders in Illinois are county-based \u2014 ask the judge for appointed counsel at your first appearance.",
    "michigan": "The State Appellate Defender Office handles appeals. Trial-level defense in Michigan is county-based, under the Michigan Indigent Defense Commission \u2014 ask the judge for appointed counsel at your first appearance.",
    "nebraska": "The Commission on Public Advocacy handles serious felonies; most trial defense in Nebraska is by county public defenders. Ask the judge for appointed counsel at your first appearance.",
    "texas": "Texas has no statewide public defender office. Each county appoints counsel under the Fair Defense Act, overseen by the Texas Indigent Defense Commission. Ask the judge for appointed counsel at your first appearance.",
}


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="what-to-do-if-youre-arrested-in-{slug}">What to do if you&rsquo;re arrested in {esc(state)}</h2>'
    )
    parts.append(
        "<p>Getting arrested is frightening, and the first hour matters more than most "
        "people realize. What you say &mdash; and what you don&rsquo;t say &mdash; in those "
        "first minutes can follow your case all the way to trial. This section is the "
        + esc(state) + " picture as of <strong>November 2026</strong> &mdash; your rights "
        "in the first minutes, booking, bail, arraignment, pleas, diversion, and how to get "
        "a public defender. This is general information, not legal advice. If you are "
        "arrested right now, the short version is: <strong>stay silent, ask for a lawyer, "
        "and do not consent to searches.</strong></p>"
    )
    # --- Card 1: first minutes ---
    parts.append('<div class="card">')
    parts.append("<h3>The first minutes: stay silent, ask for a lawyer</h3>")
    parts.append(
        "<p>You have the right to remain silent (<em>Miranda v. Arizona</em>, 1966). "
        "Anything you say can and will be used against you in court. You do not have to "
        "explain yourself, apologize, or talk your way out of it &mdash; and trying usually "
        "makes things worse.</p>"
    )
    parts.append(
        "<p><strong>Say this, out loud and clearly:</strong> &ldquo;I am exercising my right "
        "to remain silent. I want a lawyer.&rdquo; Then stop talking &mdash; to the police, "
        "to other people in the cell, and on the jail phone, which is usually recorded. "
        "Repeat the request if you are questioned again.</p>"
    )
    parts.append(
        "<p><strong>Do not consent to searches.</strong> Police can search you and the area "
        "within your reach when they arrest you, and they can search with a warrant or in a "
        "genuine emergency. For anything else, they need your permission or a warrant. "
        "&ldquo;I do not consent to a search&rdquo; is a sentence worth knowing. Say it "
        "calmly, and do not physically resist if they search anyway &mdash; your lawyer can "
        "challenge an illegal search in court later.</p>"
    )
    parts.append(
        "<p><strong>Do not resist, run, or fight.</strong> Even if the arrest is wrong, "
        "resisting adds charges and can get you hurt. Stay calm, keep your hands visible, "
        "and remember names, badge numbers, and what happened &mdash; write it down as soon "
        "as you can.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Say the two sentences above, then say "
        "nothing else about the case until a lawyer is with you.</p>"
    )
    parts.append("</div>")
    # --- Card 2: booking and phone call ---
    parts.append('<div class="card">')
    parts.append("<h3>Booking and the phone call</h3>")
    parts.append(
        "<p>After arrest, police take you to be <strong>booked</strong>: photo, fingerprints, "
        "a record of your belongings, and a check for warrants. You will be held until your "
        "first court appearance, until bail is posted, or until you are released on your own "
        "recognizance (a signed promise to come back to court).</p>"
    )
    parts.append(
        "<p><strong>The phone call.</strong> You generally get to make calls to reach a "
        "lawyer or family &mdash; but jail calls are usually recorded, so do not discuss the "
        "facts of your case on the phone. Use the call to get a lawyer, tell someone where "
        "you are, and ask them to bring your ID and any medicine you need.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Call a lawyer first if you have one. If "
        "not, call a family member and ask them to find one &mdash; or wait for the public "
        "defender at your first court appearance (next card). Do not talk about the case on "
        "a recorded line.</p>"
    )
    parts.append("</div>")
    # --- Card 3: bail, arraignment, pleas ---
    parts.append('<div class="card">')
    parts.append("<h3>Bail, arraignment, and your plea</h3>")
    parts.append(
        "<p><strong>Bail</strong> is money or a promise that gets you out of jail while your "
        "case is pending. A judge sets it &mdash; or releases you without money &mdash; based "
        "on the charge, your ties to the community, your record, and whether you are likely "
        "to come back to court. How bail works in your state is in the state card below. "
        f"More detail is in <a href=\"#bail-and-bail-bondsmen-in-{slug}\">Bail &amp; bail "
        "bondsmen</a> on this page.</p>"
    )
    parts.append(
        "<p><strong>Arraignment</strong> is your first court appearance. The judge reads the "
        "charges, makes sure you have a lawyer, and asks for your plea. You will usually be "
        "arraigned within a day or two of arrest.</p>"
    )
    parts.append(
        "<p><strong>Your plea options:</strong> <strong>not guilty</strong> (the usual first "
        "plea &mdash; it keeps every option open and does not mean you are lying); "
        "<strong>guilty</strong> (you admit the charge and accept the sentence); or "
        "<strong>no contest</strong> (you do not admit guilt, but you accept the punishment "
        "&mdash; not available everywhere). Never plead guilty at arraignment just to get it "
        "over with. Plead not guilty, get a lawyer, and decide with them.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> At arraignment, plead not guilty and ask "
        "for a lawyer if you do not have one. Write down your next court date before you "
        "leave &mdash; missing it can mean a warrant for your arrest.</p>"
    )
    parts.append("</div>")
    # --- Card 4: public defender ---
    parts.append('<div class="card">')
    parts.append("<h3>Getting a public defender</h3>")
    parts.append(
        "<p>If you cannot afford a lawyer, the court must appoint one for you "
        "(<em>Gideon v. Wainwright</em>, 1963, decided unanimously by the U.S. Supreme "
        "Court). This is not a favor &mdash; it is a constitutional right, and it applies "
        "whether the charge is a felony or a misdemeanor that could put you in jail.</p>"
    )
    parts.append(
        "<p><strong>How to get one:</strong> at your first court appearance, tell the judge "
        "you cannot afford a lawyer and ask for appointed counsel. The court will ask about "
        "your income, job, and expenses to decide if you qualify. Be honest &mdash; lying "
        "about your finances can be a separate problem. If you qualify, a public defender is "
        "assigned, usually that same day.</p>"
    )
    parts.append(
        "<p><strong>Who qualifies:</strong> anyone who cannot afford a private lawyer. The "
        "exact income line varies by state and county. If you are turned down and you still "
        "cannot afford a lawyer, say so and ask what the appeal or review process is &mdash; "
        "and check the free legal help in the state card below.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Ask the judge at your first appearance. "
        "Do not wait until trial to ask &mdash; the earlier a lawyer is on your case, the "
        "more they can do for you.</p>"
    )
    parts.append("</div>")
    # --- Card 5: diversion ---
    parts.append('<div class="card">')
    parts.append("<h3>Diversion: a way to avoid a conviction</h3>")
    parts.append(
        "<p><strong>Diversion</strong> (also called deferred prosecution or pretrial "
        "intervention) lets some people &mdash; usually first-time, non-violent offenders "
        "&mdash; complete conditions like community service, counseling, classes, or "
        "restitution instead of going to trial. Finish the conditions and the charge is "
        "dismissed, usually with no conviction on your record.</p>"
    )
    parts.append(
        "<p>Every state runs it differently: some have a statewide program, some leave it to "
        "each county&rsquo;s prosecutor, and some only offer it for certain charges (often "
        "drug possession or first-time misdemeanors). Whether it is available for your charge "
        "is in the state card below.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Ask your lawyer &mdash; or the prosecutor, "
        "if you do not have a lawyer yet &mdash; whether diversion is available for your "
        "charge, and ask early: some programs have short application deadlines. Do not admit "
        "anything to get into a program without a lawyer&rsquo;s advice.</p>"
    )
    parts.append("</div>")
    # --- Card 6: what NOT to do ---
    parts.append('<div class="card">')
    parts.append("<h3>What NOT to do</h3>")
    parts.append(
        "<p><strong>Do not talk to the police about the case without a lawyer</strong> &mdash; "
        "not to explain, not to apologize, not to &ldquo;clear things up.&rdquo;</p>"
    )
    parts.append(
        "<p><strong>Do not post about it on social media.</strong> Posts, photos, messages, "
        "and even deleted posts can be used as evidence.</p>"
    )
    parts.append(
        "<p><strong>Do not contact the alleged victim or witnesses</strong> &mdash; a text "
        "meant as an apology can become a new charge (witness tampering or violating a "
        "no-contact order).</p>"
    )
    parts.append(
        "<p><strong>Do not miss court.</strong> A missed date usually means a bench warrant "
        "and possibly losing your bail. If you cannot make a date, call the court and your "
        "lawyer before the date, not after.</p>"
    )
    parts.append(
        "<p><strong>Do not leave the state, skip town, or lie to your lawyer.</strong> Your "
        "lawyer can only help you with the truth, and they cannot tell the police what you "
        "tell them.</p>"
    )
    parts.append(
        "<p>Related guides on this page: "
        f"<a href=\"#pulled-over-in-{slug}\">Pulled over</a> (traffic stops), "
        f"<a href=\"#dui-dwi-in-{slug}\">DUI / DWI</a>, and "
        f"<a href=\"#probation-in-{slug}\">Probation</a>.</p>"
    )
    parts.append("</div>")
    # --- Card 7: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Public defender, bail, and diversion in {esc(state)}</h3>")
    if e["pd_url"]:
        parts.append(
            f"<p><strong>Public defender:</strong> "
            f'<a href="{esc(e["pd_url"])}" target="_blank" rel="noopener">{esc(e["pd_name"])}</a>.</p>'
        )
    else:
        parts.append(
            f"<p><strong>Public defender:</strong> {esc(e['pd_name'])} "
            "&mdash; no office website link could be verified; ask the judge for appointed "
            "counsel at your first court appearance.</p>"
        )
    if slug in PD_NOTE:
        parts.append(f"<p>{esc(PD_NOTE[slug])}</p>")
    if e["pd_phone"]:
        parts.append(f"<p><strong>Public defender phone:</strong> {esc(e['pd_phone'])}.</p>")
    if e["bail_note"]:
        parts.append(f"<p><strong>Bail in {esc(state)}:</strong> {esc(e['bail_note'])}</p>")
    if e["diversion_note"]:
        parts.append(
            f"<p><strong>Diversion in {esc(state)}:</strong> {esc(e['diversion_note'])}</p>"
        )
    else:
        parts.append(
            "<p><strong>Diversion in " + esc(state) + ":</strong> no statewide pretrial "
            "diversion program could be verified &mdash; diversion, if any, is handled "
            "locally. Ask your lawyer or the prosecutor whether a local option exists for "
            "your charge.</p>"
        )
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you are arrested, say you want a "
        "lawyer and stay silent. At your first court appearance, ask the judge for a public "
        "defender if you cannot afford a lawyer, plead not guilty, and ask about diversion "
        "before any deadlines pass.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Say &ldquo;I am exercising my right "
        "to remain silent. I want a lawyer.&rdquo; Then stop talking about the case. "
        "(2) Do not consent to searches and do not resist. (3) At your first court "
        "appearance, ask for a public defender if you cannot afford a lawyer, and plead not "
        "guilty. (4) Ask about diversion early. (5) Go to every court date, and do not post "
        "about the case or contact victims or witnesses.</p>"
    )
    parts.append(
        "<p><em>Sources: U.S. Supreme Court (Miranda v. Arizona, 1966; Gideon v. "
        "Wainwright, 1963), and the official " + esc(state) + " statutes, court rules, and "
        "agencies linked above, checked November 20, 2026. Bail and diversion rules change "
        "&mdash; confirm the current rules with your lawyer or the court before you decide. "
        "This is general information, not legal advice.</em></p>"
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
        # --- insert section before Social Security Disability & SSI ---
        h2 = text.find(f'<h2 id="{PREV_SLUG}-in-{slug}">')
        assert h2 != -1, f"{slug}: {PREV_SLUG} h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        before = text
        new_section = section_html(state, slug, e)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the disability <li> ---
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
            f"What to do if you&rsquo;re arrested in {state}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        # --- structural assertions ---
        assert text.count(f'id="{SLUG}-in-{slug}"') == 1, f"{slug}: anchor count"
        assert text.count("<div") - before.count("<div") == 7, f"{slug}: div open delta"
        assert text.count("</div>") - before.count("</div>") == 7, f"{slug}: div close delta"
        assert text.count("<div") == text.count("</div>"), f"{slug}: div imbalance"
        h2s = re.findall(r'<h2 id="([^"]+)">', text)
        assert h2s.index(f"{SLUG}-in-{slug}") == h2s.index(f"{PREV_SLUG}-in-{slug}") - 1, f"{slug}: h2 order"
        assert "None" not in new_section, f"{slug}: leaked None in new section"
        assert "TODO" not in new_section and "FIXME" not in new_section, f"{slug}: leaked marker"
        # cross-links resolve on this page
        for target in ("bail-and-bail-bondsmen", "pulled-over", "dui-dwi", "probation"):
            assert f'id="{target}-in-{slug}"' in text, f"{slug}: cross-link target {target} missing"
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert SLUG not in helper_part, "index already has helper option"
    assert f'data-topic="{SLUG}"' not in text, "index already has card"
    opt_old = (
        '<option value="social-security-disability-ssi" data-anchor="social-security-disability-ssi">'
        "Social Security Disability &amp; SSI (SSDI vs SSI, the five-step test, how to apply, appealing a denial)</option>"
    )
    assert opt_old in text, "disability helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="what-to-do-if-youre-arrested" data-anchor="what-to-do-if-youre-arrested">'
        "What to do if you&rsquo;re arrested (stay silent, ask for a lawyer, bail, arraignment, diversion, public defender)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="social-security-disability-ssi"'
    idx = text.find(card_anchor)
    assert idx != -1, "disability card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="what-to-do-if-youre-arrested">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-what-to-do-if-youre-arrested.jpg" alt="What to do if you&rsquo;re arrested" loading="lazy"></span>
          <h3>What to Do If You&rsquo;re Arrested</h3>
          <p>Arrested? Stay silent, ask for a lawyer, don&rsquo;t consent to searches. Bail, arraignment, pleas, diversion, and getting a public defender in your state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 42 topics" in text, "show-all label not found"
    text = text.replace("Show all 42 topics", "Show all 43 topics", 1)
    # Two badges both read "42 topics" now (hero grid + main grid). The main-grid
    # badge is the one AFTER the show-label line; the hero badge stays untouched.
    show_pos = text.find("Show all 43 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">42 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("42 topics", "43 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 42->43")


def build_about():
    text = ABOUT.read_text()
    assert text.count("87 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("87 legal topics", "88 legal topics", 1))
    print("  about.html: 87 -> 88")


def state_index_t(state, slug, e):
    bits = [
        "what-to-do-if-youre-arrested arrested arrest miranda public defender",
        f"What to do if you're arrested in {state}",
        "stay silent ask for a lawyer do not consent to searches Miranda Gideon",
        "booking phone call bail arraignment plea not guilty guilty no contest",
        "public defender appointed counsel cannot afford a lawyer Gideon v Wainwright 1963",
        "diversion deferred prosecution pretrial intervention dismissal no conviction",
        "what not to do social media contact victim witness miss court",
        f"{e['pd_name']}",
        f"bail in {state}: {e['bail_note']}" if e.get("bail_note") else "",
        f"diversion in {state}: {e['diversion_note']}" if e.get("diversion_note") else "",
        f"{e['legal_aid_name']}",
    ]
    return " — ".join(b for b in bits if b)


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 10855, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"What to do if you're arrested in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "What to Do If You're Arrested",
            "t": (
                "what-to-do-if-youre-arrested arrested arrest miranda public defender "
                "Arrested? Stay silent, ask for a lawyer, don't consent to searches. Bail, "
                "arraignment, pleas, diversion, and getting a public defender in your state. "
                "Miranda v Arizona 1966 Gideon v Wainwright 1963 booking phone call bail "
                "arraignment plea not guilty diversion deferred prosecution pretrial "
                "intervention what not to do social media miss court."
            ),
        }
    )
    assert len(idx) == 10906, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 10855 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [(k, states[k]) for k in sorted(states)]
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "pd_name", "pd_url", "pd_phone", "bail_note", "diversion_note",
        "legal_aid_name", "legal_aid_url", "sources",
    ]
    phone_re = re.compile(r"\(\d{3}\)\s*\d{3}[-.]\d{4}|\b\d{3}[-.]\d{3}[-.]\d{4}\b|1-800-\d{3}-\d{4}|1-866-\d{3}-\d{4}|1-888-\d{3}-\d{4}|877-\d{3}-\d{4}|800-\d{3}-\d{4}|844-\d{3}-\d{4}|866-\d{3}-\d{4}|1-877-\d{3}-\d{4}|\(\d{3}\)\s*\d{3}-\d{4}")
    for k, e in data:
        for f in req:
            assert f in e, f"{k}: missing {f}"
        assert e["pd_name"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"], f"{k}: empty required field"
        assert e["bail_note"], f"{k}: bail note missing"
        # diversion may be null only for Alaska (verified: no statewide program)
        assert e["diversion_note"] or k == "alaska", f"{k}: diversion note missing"
        # phones appear only in the phone field (plus no federal phone in template)
        blob = json.dumps({f: e[f] for f in req if f != "pd_phone"})
        assert not phone_re.search(blob), f"{k}: phone-like string outside phone field"
        if e["pd_phone"]:
            assert phone_re.search(e["pd_phone"]), f"{k}: phone format {e['pd_phone']!r}"
    print("building state pages (insert before disability section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
