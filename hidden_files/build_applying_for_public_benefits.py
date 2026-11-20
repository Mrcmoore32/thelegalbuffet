#!/usr/bin/env python3
"""Build Topic #97: Applying for Public Benefits (Medicaid & SNAP) —
standalone section on all 50 state pages.

Inserts one new section per state page (before Non-Compete Agreements,
newest-first), a contents-list entry (before the non-compete <li>), a
homepage helper option + topic card (after Non-Compete Agreements), bumps
About 95 -> 96, and appends 50 state entries + 1 helper entry to
assets/search-index.json (11263 -> 11314).

Data: hidden_files/topic-research/applying-for-public-benefits/all-states.json
(coordinator-merged 2026-11-20 from 5 research batches; flat dict keyed by
lowercase state name. All 50 apply-portal + legal-aid URLs checked:
78 curl 200, 14 more confirmed live via text fetch, 3 more (LawHelpCA,
Idaho Legal Aid, Legal Aid of West Virginia) confirmed live via text fetch
during the #95 verification the same day, Utah myCase confirmed correct
against the state's own DWS application form 61APP (jobs.utah.gov /
medicaid.utah.gov). 4 portal URLs rest on researcher verification against
official agency pages only — curl returned 000/403 and a live fetch was
refused/failed once (CO peak.colorado.gov, ME mymaineconnection.gov, WY
wesystem.wyo.gov, NH nheasy.nh.gov) — all four are the states' official
portals. Coordinator swaps for statewide coverage: CA LAAC -> LawHelpCA,
MS Mississippi Center -> Mississippi Legal Services (mslegalservices.org).
Headline counts: 40 states expanded Medicaid (adults to 138% FPL), 10
have not (AL, FL, GA, KS, MS, SC, TN, TX, WI, WY). SSI is excluded by
design — covered by #88 Social Security Disability & SSI, cross-linked
from this section. Work/community-engagement rules start Jan 1, 2027 in
several states (AZ, AR, IN, NH, SD, VA, WV) — noted per state.)
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "applying-for-public-benefits" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-applying-for-public-benefits.jpg"

SLUG = "applying-for-public-benefits"
TITLE = "Applying for Public Benefits"
PREV_SLUG = "non-compete-agreements"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def expanded_word(v):
    return {"yes": "Yes — expanded", "no": "No — not expanded"}.get(v, v)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="applying-for-public-benefits-in-{slug}">Applying for public benefits in {esc(state)}</h2>'
    )
    parts.append(
        "<p><strong>Medicaid</strong> pays for health care and "
        "<strong>SNAP</strong> (Supplemental Nutrition Assistance Program, "
        "the food stamps program) helps buy groceries. Both are for people "
        "with low income, and both are applied for through your state &mdash; "
        "usually online, in one application that can cover both. This section "
        "explains who qualifies, where to apply, what happens after you "
        "apply, and what to do if you are denied. The picture here is as of "
        "<strong>November 2026</strong>. This is general information, not "
        "legal advice.</p>"
    )
    parts.append(
        "<p><strong>SSI is a different program.</strong> Supplemental Security "
        "Income (SSI) is cash help for people 65 or older, blind, or with a "
        "disability who have very low income and few assets. It is run by the "
        "federal Social Security Administration, not your state, and you apply "
        "for it separately &mdash; see "
        f'<a href="#social-security-disability-ssi-in-{slug}">Social Security '
        "Disability &amp; SSI</a> on this page.</p>"
    )
    # --- Card 1: what the two programs are ---
    parts.append('<div class="card">')
    parts.append("<h3>What Medicaid and SNAP are</h3>")
    parts.append(
        "<p><strong>Medicaid</strong> is health coverage paid for jointly by "
        "the federal government and your state. It covers doctor visits, "
        "hospital care, prescriptions, and more, usually with little or no "
        "cost to you. Each state runs its own Medicaid program and gives it "
        "its own name &mdash; Medi-Cal in California, Apple Health in "
        "Washington, BadgerCare Plus in Wisconsin, and so on &mdash; but it "
        "is the same program underneath. <strong>SNAP</strong> is monthly "
        "money for groceries, loaded onto an EBT card you use like a debit "
        "card at grocery stores and farmers markets. SNAP is a federal "
        "program, but your state decides your application and the amount.</p>"
    )
    parts.append(
        "<p>You can get one without the other, and applying for one does not "
        "hurt your chances for the other. Many states use a single "
        "application for both, plus cash help and child care, so one form can "
        "open several doors at once.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Start with the state card "
        "below &mdash; it names your state&rsquo;s online portal and the "
        "agency that runs it. That portal is where you apply.</p>"
    )
    parts.append("</div>")
    # --- Card 2: who qualifies / the expansion split ---
    parts.append('<div class="card">')
    parts.append("<h3>Who qualifies: the expansion split</h3>")
    parts.append(
        "<p>Children, pregnant people, parents with very low income, seniors, "
        "and people with disabilities can qualify for Medicaid in every "
        "state. The big split is over <strong>other adults</strong>: in the "
        "<strong>40 states that expanded Medicaid</strong>, most adults under "
        "65 with income up to 138% of the federal poverty level qualify, "
        "whether or not they have children. In the <strong>10 states that "
        "have not expanded</strong> &mdash; Alabama, Florida, Georgia, "
        "Kansas, Mississippi, South Carolina, Tennessee, Texas, Wisconsin, "
        "and Wyoming &mdash; most adults without children do not qualify for "
        "Medicaid at any income, and parents qualify only at very low "
        "incomes. Wisconsin is the partial exception: its BadgerCare Plus "
        "covers childless adults up to 100% of the poverty level under a "
        "federal waiver.</p>"
    )
    parts.append(
        "<p>SNAP does not have that split: it is available in all 50 states "
        "for households with low income, based on household size, income, and "
        "some expenses like rent and child care. Citizens and many lawfully "
        "present immigrants can qualify; some immigration statuses are "
        "excluded, and the rules differ between Medicaid and SNAP, so check "
        "the program&rsquo;s own page if that question applies to you.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check your state&rsquo;s "
        "answer in the card below. If your state has not expanded Medicaid "
        "and you do not qualify, check HealthCare.gov for a subsidized "
        "private plan &mdash; and still apply for SNAP, which has no "
        "expansion gap.</p>"
    )
    parts.append("</div>")
    # --- Card 3: how to apply ---
    parts.append('<div class="card">')
    parts.append("<h3>How to apply</h3>")
    parts.append(
        "<p>Most people apply <strong>online</strong> through the portal in "
        "the state card below. You can also apply <strong>by phone</strong>, "
        "<strong>on paper</strong> (print the form or pick one up at a local "
        "office), or <strong>in person</strong> at your county or local "
        "benefits office. A few states split the application in two &mdash; "
        "one portal for food and cash help, another for health coverage "
        "&mdash; and the state card below says so when that is the case.</p>"
    )
    parts.append(
        "<p>You do not need a complete application to start. For both SNAP "
        "and Medicaid, an application with just your <strong>name, address, "
        "and signature</strong> counts as filed that day &mdash; and the date "
        "matters, because SNAP benefits start on the day you apply. Send the "
        "rest of the information later; do not wait until everything is "
        "perfect.</p>"
    )
    parts.append(
        "<p>Have ready if you can: ID for everyone applying, proof of income "
        "(pay stubs, benefit letters), proof of rent or mortgage, and proof "
        "of household size. If you do not have a document, apply anyway and "
        "tell the agency &mdash; it can often verify income directly or give "
        "you time to send it.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Go to the portal in the "
        "state card below and start the application with your name, address, "
        "and signature. That locks in your application date.</p>"
    )
    parts.append("</div>")
    # --- Card 4: what happens after you apply ---
    parts.append('<div class="card">')
    parts.append("<h3>What happens after you apply</h3>")
    parts.append(
        "<p>Most states will call you for a <strong>phone interview</strong> "
        "&mdash; usually for SNAP, sometimes for Medicaid too. Answer the "
        "call or call back promptly; a missed interview is one of the most "
        "common reasons applications stall. The agency may ask for documents "
        "to verify income, identity, or expenses, and will tell you how to "
        "send them (upload, fax, mail, or drop off).</p>"
    )
    parts.append(
        "<p><strong>Deadlines the agency must meet:</strong> SNAP decisions "
        "are due within <strong>30 days</strong> of your application, and "
        "households with very little money or no income can get "
        "<strong>expedited SNAP within 7 days</strong> &mdash; ask for it "
        "when you apply if that is your situation. Medicaid decisions take "
        "longer and the timeline varies by state; if a disability decision is "
        "involved it can take up to 90 days.</p>"
    )
    parts.append(
        "<p>You will get the decision in writing. If you are approved, the "
        "letter says what you get and when it starts. If you are denied, the "
        "letter must say why &mdash; keep it, because it is the key to "
        "appealing (see the next card).</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Answer the interview "
        "call, send any documents they ask for right away, and keep copies of "
        "everything you send. If 30 days pass on a SNAP application with no "
        "decision, call the agency and ask where it stands.</p>"
    )
    parts.append("</div>")
    # --- Card 5: if you're denied ---
    parts.append('<div class="card">')
    parts.append("<h3>If you are denied: appeal, and appeal fast</h3>")
    parts.append(
        "<p>A denial is not the end of it. You have the right to a "
        "<strong>fair hearing</strong> &mdash; a review by someone who was "
        "not involved in the first decision &mdash; and many denials are "
        "overturned because of a missing document, a math error, or income "
        "counted the wrong way. For SNAP you usually have <strong>90 days "
        "from the date of the notice</strong> to ask for a hearing, and "
        "Medicaid appeals work on a similar window &mdash; but do not wait: "
        "ask as soon as you get the letter.</p>"
    )
    parts.append(
        "<p>If your benefits are being <strong>cut off or reduced</strong>, "
        "asking for a hearing quickly &mdash; usually within about 10 to 15 "
        "days of the notice, depending on the state &mdash; can keep your "
        "benefits going at the old level while the appeal is decided. The "
        "notice itself tells you the exact deadline and how to ask; read it "
        "the day it arrives.</p>"
    )
    parts.append(
        "<p>You can bring someone to help you at the hearing, including a "
        "legal aid lawyer, and you can ask for an interpreter if you need "
        "one. Legal aid programs help with benefits appeals, often for free "
        "&mdash; the link in the state card below is a good place to start.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Read the denial letter "
        "the day it arrives, note the appeal deadline, and ask for a fair "
        "hearing in writing before that date. Keep a copy of your request.</p>"
    )
    parts.append("</div>")
    # --- Card 6: keeping your benefits ---
    parts.append('<div class="card">')
    parts.append("<h3>Keeping your benefits: renewals and changes</h3>")
    parts.append(
        "<p>Benefits are not forever &mdash; you have to <strong>renew</strong> "
        "them. Medicaid is usually renewed once a year; SNAP is usually "
        "recertified every 6 to 12 months. The agency will send you a renewal "
        "form &mdash; fill it out and return it by the deadline, or your "
        "benefits stop even if you still qualify. If you move, tell the "
        "agency your new address, or the renewal form will go to the wrong "
        "place.</p>"
    )
    parts.append(
        "<p>Also <strong>report changes</strong> when they happen: a new job, "
        "a raise, someone moving in or out, a change in rent. Reporting late "
        "can mean an overpayment you have to pay back, so report promptly "
        "even if you think the change is small.</p>"
    )
    parts.append(
        "<p><strong>Watch for new work rules.</strong> Several states are "
        "adding <strong>work or community-engagement requirements</strong> for "
        "some adults on expanded Medicaid, starting <strong>January 1, "
        "2027</strong>. Your state&rsquo;s note below says if yours is one "
        "of them &mdash; and if it is, check what counts and what proof you "
        "need before the rules start.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Put the renewal deadline "
        "on your calendar the day the letter arrives, report changes as they "
        "happen, and keep your address current with the agency.</p>"
    )
    parts.append("</div>")
    # --- Card 7: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Applying for public benefits in {esc(state)}</h3>")
    parts.append(
        f"<p><strong>Medicaid expanded?</strong> {expanded_word(e['medicaid_expanded'])}. {esc(e['medicaid_note'])}</p>"
    )
    parts.append(
        f"<p><strong>Where to apply:</strong> "
        f'<a href="{esc(e["apply_url"])}" target="_blank" rel="noopener">{esc(e["apply_url"])}</a> &mdash; {esc(e["apply_note"])}</p>'
    )
    parts.append(
        f"<p><strong>Agency:</strong> {esc(e['agency_name'])}.</p>"
    )
    if e["state_note"]:
        parts.append(f"<p>{esc(e['state_note'])}</p>")
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a> &mdash; legal aid programs help with benefits applications and appeals, often for free.</p>'
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Apply at the portal "
        "above &mdash; even an application with just your name, address, and "
        "signature starts the clock. Answer the interview call, send any "
        "documents they ask for, and if you are denied, ask for a fair "
        "hearing before the deadline on the letter.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Check whether your "
        "state expanded Medicaid in the card above. (2) Apply at your "
        "state&rsquo;s portal &mdash; name, address, and signature is enough "
        "to start. (3) Answer the interview call and send any documents they "
        "ask for. (4) If you are denied, ask for a fair hearing before the "
        "deadline on the notice. (5) Renew on time and report changes as they "
        "happen. For SSI, see Social Security Disability &amp; SSI on this "
        "page instead &mdash; that program runs through Social Security, not "
        "your state.</p>"
    )
    parts.append(
        "<p><em>Sources: the official state benefits portals and agency pages "
        "linked in the research for this section, checked November 20, 2026. "
        "Eligibility rules and work requirements are changing in several "
        "states in 2027 &mdash; confirm the current rules with your state "
        "agency before you rely on them. This is general information, not "
        "legal advice.</em></p>"
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
            f"Applying for public benefits in {state}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        assert text.count(f'id="{SLUG}-in-{slug}"') == 1, f"{slug}: anchor count"
        assert text.count("<div") - before.count("<div") == 7, f"{slug}: div open delta"
        assert text.count("</div>") - before.count("</div>") == 7, f"{slug}: div close delta"
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
        '<option value="non-compete-agreements" data-anchor="non-compete-agreements">'
        "Non-compete agreements (is yours enforceable, pay thresholds, bans, what to do before you sign or leave)</option>"
    )
    assert opt_old in text, "non-compete helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="applying-for-public-benefits" data-anchor="applying-for-public-benefits">'
        "Applying for public benefits (Medicaid, SNAP food help — who qualifies, where to apply online, appeals, renewals)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="non-compete-agreements"'
    idx = text.find(card_anchor)
    assert idx != -1, "non-compete card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="applying-for-public-benefits">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-applying-for-public-benefits.jpg" alt="Applying for public benefits" loading="lazy"></span>
          <h3>Applying for Public Benefits</h3>
          <p>Medicaid and SNAP: who qualifies in your state, where to apply online, and what to do if you're denied or cut off.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 49 topics" in text, "show-all label not found"
    text = text.replace("Show all 49 topics", "Show all 50 topics", 1)
    show_pos = text.find("Show all 50 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">49 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("49 topics", "50 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 49->50")


def build_about():
    text = ABOUT.read_text()
    assert text.count("95 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("95 legal topics", "96 legal topics", 1))
    print("  about.html: 95 -> 96")


def state_index_t(state, slug, e):
    bits = [
        "applying for public benefits medicaid snap food stamps",
        f"Applying for public benefits in {state}",
        f"medicaid expanded {e['medicaid_expanded']} {e['medicaid_note']}",
        f"apply online {e['apply_url']} {e['apply_note']}",
        f"agency {e['agency_name']}",
        "phone interview verification documents 30 days snap decision expedited 7 days",
        "denied fair hearing appeal 90 days keep benefits while appealing",
        "renewal once a year recertification report changes work requirements January 1 2027",
        "ssi supplemental security income separate program social security disability",
        f"{e['state_note'] or ''}",
        f"{e['legal_aid_name']}",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11263, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Applying for public benefits in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Applying for Public Benefits",
            "t": (
                "applying-for-public-benefits applying for public benefits "
                "Applying for Public Benefits? Medicaid and SNAP: who qualifies "
                "in your state, where to apply online, and what to do if you "
                "are denied or cut off. Medicaid expansion 138 percent federal "
                "poverty level SNAP food stamps EBT fair hearing appeal "
                "renewal work requirements."
            ),
        }
    )
    assert len(idx) == 11314, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11263 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d
    assert len(states) == 50, len(states)
    data = [(k, states[k]) for k in sorted(states)]
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "medicaid_expanded", "medicaid_note", "apply_url", "apply_note",
        "agency_name", "legal_aid_name", "legal_aid_url", "state_note",
        "sources",
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
        assert e["medicaid_expanded"] in ("yes", "no"), f"{k}: bad medicaid_expanded"
        assert e["medicaid_note"] and e["apply_url"] and e["apply_note"] and e["agency_name"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"], f"{k}: empty required field"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before non-compete-agreements section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
