#!/usr/bin/env python3
"""Build Topic #92: Social Security Retirement & Survivors Benefits — standalone
section on all 50 state pages.

Inserts one new section per state page (before Wrongful Death, newest-first),
a contents-list entry (before the wrongful-death <li>), a homepage helper
option + topic card (after Wrongful Death), bumps About 90 -> 91, and appends
50 state entries + 1 helper entry to assets/search-index.json (11008 -> 11059).

Data: hidden_files/topic-research/social-security-retirement-survivors/all-states.json
(coordinator-built 2026-11-20 from 5 research batches; all 100 SHIP + legal-aid
URLs curl/browser-verified alive; all 49 SHIP phones two-source confirmed,
Maine phone null by design).
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "social-security-retirement-survivors" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-social-security-retirement-survivors.jpg"

SLUG = "social-security-retirement-survivors"
TITLE = "Social Security Retirement & Survivors Benefits"
PREV_SLUG = "wrongful-death"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="social-security-retirement-survivors-in-{slug}">Social Security retirement &amp; survivors benefits in {esc(state)}</h2>'
    )
    parts.append(
        "<p>Social Security pays a monthly benefit to retired workers and to the "
        "families of workers who have died. This section covers two kinds of "
        "benefits: <strong>retirement benefits</strong> from your own work record, "
        "and <strong>survivors benefits</strong> from the work record of a spouse, "
        "parent, or ex-spouse who has died. It also covers whether " + esc(state) +
        " taxes those benefits, and what to do if the Social Security "
        "Administration (SSA) says no. This is the picture as of "
        "<strong>November 2026</strong>. This is general information, not legal "
        "advice. The money is yours by law once you qualify &mdash; the hard part "
        "is usually knowing when to claim and what to do when something goes wrong.</p>"
    )
    # --- Card 1: retirement benefits ---
    parts.append('<div class="card">')
    parts.append("<h3>Retirement benefits: when can you claim?</h3>")
    parts.append(
        "<p>You qualify for retirement benefits once you have earned <strong>40 work "
        "credits</strong> &mdash; roughly 10 years of work. Your <strong>full "
        "retirement age</strong> is 66 or 67, depending on the year you were born. "
        "You can start as early as age 62, but the check is smaller for life. You "
        "can also wait past full retirement age, up to age 70, and the check grows "
        "each month you wait. There is no one right answer: claiming early means "
        "more checks but smaller ones; waiting means fewer checks but bigger ones.</p>"
    )
    parts.append(
        "<p>Apply online at <strong>ssa.gov</strong>, by phone at "
        "<strong>1-800-772-1213</strong>, or at a local Social Security office. You "
        "can check your own estimated benefit any time by opening a "
        "<strong>my Social Security</strong> account at ssa.gov/myaccount &mdash; "
        "it shows your earnings record and what you would get at 62, at full "
        "retirement age, and at 70. Check that your earnings record is correct: "
        "a missing year of earnings lowers your check.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Open your my Social Security "
        "account and look at the three estimates. Then decide: do you need the "
        "money now, or can you afford to wait for a bigger check? If you are "
        "unsure, the free SHIP counselors in the state card below can walk through "
        "the trade-off with you.</p>"
    )
    parts.append("</div>")
    # --- Card 2: survivors benefits ---
    parts.append('<div class="card">')
    parts.append("<h3>Survivors benefits: who can get them</h3>")
    parts.append(
        "<p>When a worker dies, Social Security can pay monthly benefits to their "
        "family from that worker&rsquo;s record. A <strong>widow or widower</strong> "
        "can claim at 60 (or 50 if disabled), or at any age while caring for the "
        "worker&rsquo;s child under 16. <strong>Unmarried children</strong> can "
        "claim under 18, or under 19 if still in high school. A <strong>dependent "
        "parent</strong> age 62 or older can claim. A <strong>divorced spouse</strong> "
        "can also claim on an ex-spouse&rsquo;s record if the marriage lasted at "
        "least 10 years.</p>"
    )
    parts.append(
        "<p>There is also a one-time <strong>lump-sum death payment of $255</strong> "
        "to a surviving spouse, or to a child if there is no surviving spouse. "
        "Survivors usually have to <strong>apply</strong> &mdash; the benefits do "
        "not always start on their own. Apply as soon as you can: SSA can only "
        "backdate payments a few months, so a late application can cost you "
        "money. Call 1-800-772-1213 or visit a local office; survivors claims "
        "generally cannot be finished online.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If your spouse or parent has "
        "died, call SSA promptly and ask about survivors benefits on their record. "
        "Bring the death certificate, your marriage certificate or birth "
        "certificate, and the worker&rsquo;s Social Security number.</p>"
    )
    parts.append("</div>")
    # --- Card 3: how much ---
    parts.append('<div class="card">')
    parts.append("<h3>How much will you get?</h3>")
    parts.append(
        "<p>The amount is based on the worker&rsquo;s earnings record &mdash; the "
        "longer and higher-paid the work, the bigger the check. Your my Social "
        "Security account shows your own estimate. A spouse can also claim a "
        "spousal benefit on their partner&rsquo;s record, and a widow or widower "
        "can switch between their own benefit and the survivors benefit, taking "
        "whichever is bigger. You cannot collect two full benefits at once &mdash; "
        "SSA pays the higher of the two.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check your estimate at "
        "ssa.gov/myaccount, and check your spouse&rsquo;s too if you are married. "
        "If you are a widow or widower, ask SSA to compare your own benefit with "
        "the survivors benefit before you pick one.</p>"
    )
    parts.append("</div>")
    # --- Card 4: working while collecting ---
    parts.append('<div class="card">')
    parts.append("<h3>Working while you collect</h3>")
    parts.append(
        "<p>If you claim before full retirement age and keep working, there is a "
        "yearly earnings limit: earn over it and SSA withholds part of your "
        "benefits. Once you reach full retirement age there is no limit &mdash; "
        "you can earn as much as you want with no reduction. The withheld money "
        "is not lost: when you reach full retirement age, SSA recalculates and "
        "raises your monthly check to give it back over time.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you claim early and keep "
        "working, tell SSA about your earnings so the withholding is right. If "
        "you can wait until full retirement age to claim, the earnings limit "
        "stops mattering.</p>"
    )
    parts.append("</div>")
    # --- Card 5: taxes ---
    parts.append('<div class="card">')
    parts.append("<h3>Are the benefits taxed?</h3>")
    parts.append(
        "<p>At the <strong>federal</strong> level, yes, for many people: depending "
        "on your total income, up to 85% of your benefits can count as taxable "
        "income. At the <strong>state</strong> level, most states do not tax "
        "Social Security benefits at all, and a few tax only part of them. Your "
        "state&rsquo;s rule is in the state card below.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check the state card below for "
        "your state&rsquo;s rule. If your state taxes benefits only above an income "
        "limit, that limit is in the note &mdash; and a tax preparer or the free "
        "SHIP counselors can help you plan around it.</p>"
    )
    parts.append("</div>")
    # --- Card 6: if SSA says no ---
    parts.append('<div class="card">')
    parts.append("<h3>If SSA says no, or says you were overpaid</h3>")
    parts.append(
        "<p>If SSA denies your claim, you have <strong>60 days</strong> to appeal "
        "at every stage: first a reconsideration, then a hearing before a judge, "
        "then the Appeals Council, then federal court. Do not miss the 60 days "
        "&mdash; a late appeal can end the claim. If SSA says you were overpaid "
        "and wants the money back, you can ask for a <strong>waiver</strong> if the "
        "overpayment was not your fault and you cannot afford to repay it, or ask "
        "to repay it in small monthly amounts.</p>"
    )
    parts.append(
        "<p>If the denial is about <strong>disability</strong>, see the "
        f'<a href="#social-security-disability-ssi-in-{slug}">Social Security Disability &amp; SSI</a> '
        "section on this page &mdash; it walks through the disability appeal "
        "steps. The legal-aid office in the state card below can help with any "
        "of these appeals, usually for free.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Read the denial letter for the "
        "deadline, file the appeal within 60 days, and call legal aid or the SHIP "
        "counselors below for help. Do not just re-apply &mdash; appeal instead, "
        "or you lose your place in line.</p>"
    )
    parts.append("</div>")
    # --- Card 7: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Social Security retirement &amp; survivors benefits in {esc(state)}</h3>")
    if e["taxes_benefits"] == "no":
        parts.append(
            f"<p><strong>Does {esc(state)} tax Social Security benefits?</strong> No. {esc(e['tax_note'])}</p>"
        )
    elif e["taxes_benefits"] == "partial":
        parts.append(
            f"<p><strong>Does {esc(state)} tax Social Security benefits?</strong> Partly. {esc(e['tax_note'])}</p>"
        )
    else:
        parts.append(
            f"<p><strong>Does {esc(state)} tax Social Security benefits?</strong> Yes. {esc(e['tax_note'])}</p>"
        )
    if e["state_note"]:
        parts.append(f"<p>{esc(e['state_note'])}</p>")
    if e["ship_url"]:
        parts.append(
            f"<p><strong>Free Medicare and benefits counseling:</strong> "
            f'<a href="{esc(e["ship_url"])}" target="_blank" rel="noopener">{esc(e["ship_name"])}</a> '
            "&mdash; free, one-on-one help with Medicare and Social Security questions from trained counselors who do not sell insurance.</p>"
        )
    if e["ship_phone"]:
        parts.append(
            f"<p><strong>{esc(e['ship_name'])} phone:</strong> {esc(e['ship_phone'])}.</p>"
        )
    if e["legal_aid_url"]:
        parts.append(
            f"<p><strong>Free legal help:</strong> "
            f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
        )
    else:
        parts.append(
            f"<p><strong>Free legal help:</strong> {esc(e['legal_aid_name'])} &mdash; no "
            "website link could be verified; search the name to find their intake line.</p>"
        )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check your own benefit estimate "
        "at ssa.gov/myaccount, check whether your state taxes benefits above, "
        "and call the free counseling line or legal aid if SSA denies a claim or "
        "says you were overpaid.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Open your my Social Security "
        "account at ssa.gov/myaccount and check your earnings record and your "
        "estimates at 62, full retirement age, and 70. (2) If a spouse or parent "
        "has died, call SSA at 1-800-772-1213 promptly about survivors benefits "
        "&mdash; do not wait. (3) Check the state card above for whether your "
        "state taxes benefits. (4) If SSA denies a claim or claims an overpayment, "
        "appeal within 60 days and get free help from legal aid or the SHIP "
        "counselors above. (5) If the claim is about disability, see the Social "
        "Security Disability &amp; SSI section on this page.</p>"
    )
    parts.append(
        "<p><em>Sources: the Social Security Administration (ssa.gov), the official "
        + esc(state) +
        " revenue and SHIP sources linked above, checked November 20, 2026. "
        "Benefit amounts and tax thresholds change &mdash; confirm the current "
        "numbers with SSA or your state revenue department before you decide. "
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
            f"Social Security retirement &amp; survivors benefits in {state}</a></li>\n"
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
        '<option value="wrongful-death" data-anchor="wrongful-death">'
        "Wrongful death (who can file, the deadline, what can be recovered, what to do first)</option>"
    )
    assert opt_old in text, "wrongful-death helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="social-security-retirement-survivors" data-anchor="social-security-retirement-survivors">'
        "Social Security retirement &amp; survivors benefits (when to claim, survivors benefits, taxes on benefits, appeals)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="wrongful-death"'
    idx = text.find(card_anchor)
    assert idx != -1, "wrongful-death card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="social-security-retirement-survivors">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-social-security-retirement-survivors.jpg" alt="Social Security retirement and survivors benefits" loading="lazy"></span>
          <h3>Social Security Retirement &amp; Survivors Benefits</h3>
          <p>Retirement and survivors benefits from Social Security: when to claim, what survivors can get, whether your state taxes benefits, and what to do if SSA says no.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 45 topics" in text, "show-all label not found"
    text = text.replace("Show all 45 topics", "Show all 46 topics", 1)
    show_pos = text.find("Show all 46 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">45 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("45 topics", "46 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 45->46")


def build_about():
    text = ABOUT.read_text()
    assert text.count("90 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("90 legal topics", "91 legal topics", 1))
    print("  about.html: 90 -> 91")


def state_index_t(state, slug, e):
    tax_bit = (
        "does not tax social security benefits" if e["taxes_benefits"] == "no"
        else "taxes part of social security benefits"
    )
    bits = [
        "social security retirement survivors benefits",
        f"Social Security retirement & survivors benefits in {state}",
        "retirement benefits work credits full retirement age claim at 62 wait to 70",
        "survivors benefits widow widower children dependent parents lump sum death payment 255",
        "how much benefit estimate my social security account",
        "working while collecting earnings limit full retirement age",
        f"taxes on benefits {tax_bit}",
        f"{e['tax_note']}",
        "appeal denied claim overpayment waiver 60 days reconsideration hearing",
        f"{e['ship_name']}",
        f"{e['state_note'] or ''}",
        f"{e['legal_aid_name']}",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11008, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Social Security retirement & survivors benefits in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Social Security Retirement & Survivors Benefits",
            "t": (
                "social-security-retirement-survivors social security retirement "
                "survivors benefits Social Security retirement & survivors benefits? "
                "When to claim, what survivors can get, whether your state taxes "
                "benefits, and what to do if SSA says no. Work credits full "
                "retirement age claim at 62 wait to 70 widow widower children "
                "dependent parents lump sum death payment 255 appeal denied claim "
                "overpayment waiver 60 days reconsideration hearing my social "
                "security account ssa.gov SHIP free counseling."
            ),
        }
    )
    assert len(idx) == 11059, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11008 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [(k, states[k]) for k in sorted(states)]
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "taxes_benefits", "tax_note", "ship_name", "ship_url", "ship_phone",
        "legal_aid_name", "legal_aid_url", "state_note", "sources",
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
        assert e["taxes_benefits"] in ("no", "partial", "yes"), f"{k}: bad taxes_benefits"
        assert e["tax_note"] and e["ship_name"] and e["ship_url"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"], f"{k}: empty required field"
        blob = json.dumps({f: e[f] for f in req if f not in ("ship_phone",)})
        assert not phone_re.search(blob), f"{k}: phone-like string outside phone field"
        if e["ship_phone"]:
            assert phone_re.search(e["ship_phone"]), f"{k}: phone format {e['ship_phone']!r}"
    print("building state pages (insert before wrongful-death section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
