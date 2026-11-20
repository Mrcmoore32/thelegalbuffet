#!/usr/bin/env python3
"""Build Topic #108: Life Insurance Claim Denials — standalone section on
all 50 state pages.

Inserts one new section per state page (before Breaking a Lease Early,
newest-first), a contents-list entry (before the breaking-a-lease-early
<li>), a homepage helper option + topic card (after Breaking a Lease
Early), bumps About 106 -> 107, and appends 50 state entries + 1 helper
entry to assets/search-index.json (11824 -> 11875).

Data: hidden_files/topic-research/life-insurance-claim-denials/all-states.json
(coordinator-merged 2026-11-20 from 5 research batches recovered from
the researchers' session files).

URL verification 2026-11-20: 73/100 curl 200; 17 curl 403 bot filters
+ 6 curl 000 + 3 curl 406 — ALL confirmed alive by text fetch with
real content. 1 real fix: Ohio dept complaint page
insurance.ohio.gov/consumer/file-a-complaint is 404 (confirmed by
curl AND text fetch) -> the ODI's live gateway complaint form
gateway.insurance.ohio.gov/UI/ODI.CS.Public.UI/Complaint.mvc/DisplayConsumerComplaintForm
(verified by text fetch with real form content).

Dataset fixes by the coordinator (all verified Nov 20):
- Delaware dept complaint URL (was null) ->
  insurance.delaware.gov/filecomplaint (per the DOI's own Consumer
  Services trifold; CMS confirms services/filecomplaint/ also live).
- Kansas dept URL was the dead insurance.ks.gov/consumers/file-a-
  complaint (404) -> insurance.kansas.gov/about/file-a-complaint
  (verified by text fetch).
- Hawaii dept URL was the dead cca.hawaii.gov/ins/consumer/complaints
  (404) -> cca.hawaii.gov/file-a-complaint/ (DCCA's own complaint
  page, verified).
- Vermont legal aid URL (was null) -> vtlegalaid.org (verified).
- West Virginia legal aid lawv.net is defunct (confirmed in #105/#106/
  #107) -> legalaidwv.org (verified).
- Massachusetts legal aid: researcher gave Greater Boston Legal
  Services (gbls.org, Boston-area only); swapped to the statewide
  MassLegalHelp, masslegalhelp.org (verified, consistent with #107).
- Iowa grace period (was null) -> 31 days (Iowa Code 509.2 for group
  life; 31 days is the standard provision; Loyd v. Federal Kemper,
  518 N.W.2d 374 (Iowa 1994)).
- Mississippi grace period (was null) -> 31 days for most policies,
  7 days weekly-premium / 10 days monthly-premium (Miss. Code Ann.
  83-9-5(1)(c)).
- South Dakota bad faith (was null) -> first-party bad-faith claim
  recognized: no reasonable basis + knowledge/reckless disregard
  (Champion v. United States Fidelity & Guaranty Co., 399 N.W.2d 320
  (S.D. 1987)); SDCL 58-12-3 attorney's fees for vexatious refusal.

Headline counts (computed from the corrected dataset): the
contestability period is two years in ALL 50 states. 40 states
recognize a first-party bad-faith claim; 10 have no standalone
bad-faith lawsuit (Delaware, Kansas, Maine, Maryland, Michigan,
Minnesota, New York, Oregon, Vermont, Virginia) — most of those still
ban unfair claim settlement practices or offer a statutory remedy.
Grace periods are 30 days or one month in most states; California and
Connecticut give at least 60 days. Suicide within the exclusion period
is listed among the common denial reasons in 38 states.
No phone numbers in the dataset.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "life-insurance-claim-denials" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-life-insurance-claim-denials.jpg"

SLUG = "life-insurance-claim-denials"
TITLE = "Life Insurance Claim Denials"
PREV_SLUG = "breaking-a-lease-early"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="life-insurance-claim-denials-in-{slug}">Life insurance claim denials in {esc(state)}</h2>'
    )
    parts.append(
        "<p>When a life insurance company denies a claim, the family "
        "that was counting on that money is left with a denial letter "
        "and a deadline. The denial is not always the last word: "
        "insurers deny claims for reasons the law does not allow, and "
        "every state gives you a way to push back. Three rules shape "
        "almost every case. First, the insurer has only <strong>two "
        "years</strong> — in all 50 states — to challenge the "
        "application for misstatements; after that, the policy is "
        "incontestable. Second, a missed premium does not end a policy "
        "right away: most states give a <strong>30-day or one-month "
        "grace period</strong>, and California and Connecticut give at "
        "least <strong>60 days</strong>. Third, <strong>40 states</strong> "
        "let you sue your own insurer for bad faith if it denies a "
        "claim without a reasonable basis; the other <strong>10</strong> "
        "have no standalone bad-faith lawsuit, though most still ban "
        "unfair claim practices or offer a statutory remedy. The "
        "picture here is as of <strong>November 2026</strong>. This is "
        "general information, not legal advice.</p>"
    )
    # --- Card 1: why claims get denied ---
    parts.append('<div class="card">')
    parts.append("<h3>Why life insurance claims get denied</h3>")
    parts.append(
        "<p>The most common lawful reasons are a material misstatement "
        "on the application discovered within the two-year "
        "contestability period, the policy having lapsed for nonpayment "
        "after the grace period ran out, suicide within the "
        "policy&rsquo;s exclusion period (usually the first one or two "
        "years — listed among the common reasons in 38 states), and a "
        "death that falls under a coverage exclusion in the policy. A "
        "death inside the contestability period alone is <strong>not</strong> "
        "a lawful reason to deny — the insurer needs actual proof the "
        "misstatement mattered to issuing the policy. And some denials "
        "are simply wrong: the insurer misread the policy, lost "
        "paperwork, or applied an exclusion that does not fit the "
        "facts. A denial letter that quotes no policy language, or "
        "that leans on a misstatement the insurer cannot show was "
        "material, is worth challenging.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Ask the insurer in "
        "writing for the exact reason for the denial and the exact "
        "policy language it relied on, and keep a copy of everything. "
        "Get the full policy — not just the summary — and check the "
        "denial against it yourself. Do not accept a phone-only "
        "explanation; a written denial with the policy language is "
        "what the regulator and a lawyer will want to see.</p>"
    )
    parts.append("</div>")
    # --- Card 2: contestability ---
    parts.append('<div class="card">')
    parts.append("<h3>The two-year contestability period</h3>")
    parts.append(
        "<p>In <strong>all 50 states</strong>, a life insurance policy "
        "becomes incontestable after it has been in force for "
        "<strong>two years</strong> during the insured&rsquo;s "
        "lifetime. During those two years the insurer can void the "
        "policy if it finds a material misstatement on the application "
        "— something that mattered to its decision to issue the "
        "policy, like a hidden serious illness. After the two years "
        "run, the insurer cannot contest the policy over application "
        "statements at all, except for nonpayment of premiums — and in "
        "some states, fraud or violations of the policy&rsquo;s "
        "military-service conditions. California is notable: it has no "
        "fraud exception once the two years have run. Each increase in "
        "the death benefit usually starts its own two-year period from "
        "the date of the increase.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Work out the dates: "
        "when was the policy issued, and when did the insured die? If "
        "more than two years passed, the insurer generally cannot deny "
        "over the application — say so in writing, and cite your "
        "state&rsquo;s rule in the card below. If the death was inside "
        "the two years, the question is whether the misstatement was "
        "actually material; a small error that would not have changed "
        "the insurer&rsquo;s decision is not enough.</p>"
    )
    parts.append("</div>")
    # --- Card 3: grace period ---
    parts.append('<div class="card">')
    parts.append("<h3>The grace period: a missed premium does not always end the policy</h3>")
    parts.append(
        "<p>Every state requires a grace period after a premium due "
        "date, during which the policy stays in full force — so if the "
        "insured dies during the grace period, the insurer still pays "
        "the benefit, minus the overdue premium. In most states the "
        "grace period is <strong>30 days or one month</strong>; "
        "California and Connecticut give at least <strong>60 "
        "days</strong>. California also requires the insurer to mail a "
        "lapse notice at least 30 days before the policy can end for "
        "nonpayment. The grace period only helps if the policy was "
        "still inside it when the insured died — once it runs out "
        "without payment, the policy lapses, and the insurer can deny "
        "on that ground.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Find the premium due "
        "date and the date of death, and count the days between them "
        "against your state&rsquo;s grace period in the card below. "
        "Ask the insurer for its payment records — a payment the "
        "insurer received but did not post on time still counts. If "
        "the policy had an automatic premium loan or a "
        "nonforfeiture option, ask whether that kept the policy in "
        "force.</p>"
    )
    parts.append("</div>")
    # --- Card 4: bad faith ---
    parts.append('<div class="card">')
    parts.append("<h3>Can you sue the insurer for bad faith?</h3>")
    parts.append(
        "<p>In <strong>40 states</strong>, yes. If the insurer denied "
        "the claim without a reasonable basis — and knew it had no "
        "basis, or recklessly disregarded that fact — you can sue for "
        "bad faith and recover damages beyond the policy benefits, "
        "sometimes including emotional-distress damages and, for "
        "oppressive, fraudulent, or malicious conduct, punitive "
        "damages. In <strong>10 states</strong> — Delaware, Kansas, "
        "Maine, Maryland, Michigan, Minnesota, New York, Oregon, "
        "Vermont, and Virginia — there is no standalone bad-faith "
        "lawsuit against your own insurer. That does not mean you have "
        "no remedy there: most of those states ban unfair claim "
        "settlement practices, which the insurance regulator enforces, "
        "and Minnesota has a statutory remedy that can add up to "
        "$250,000 in costs plus up to $100,000 in attorney&rsquo;s "
        "fees. Everywhere, the ordinary remedy is a breach-of-contract "
        "suit for the policy benefits themselves.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> File a complaint "
        "with your state insurance regulator first — it costs nothing, "
        "and the regulator can press the insurer for an explanation "
        "and sanction a company that broke the law. Keep a dated log "
        "of every call and letter, because a bad-faith case turns on "
        "what the insurer knew and when. And talk to a lawyer before "
        "any deadline in the policy runs out: policies often set their "
        "own time limit for suing, and it can be shorter than the "
        "state&rsquo;s.</p>"
    )
    parts.append("</div>")
    # --- Card 5: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Life insurance claim denials in {esc(state)}</h3>")
    parts.append(f"<p><strong>The two-year rule:</strong> {esc(e['contestability_period'])}</p>")
    parts.append(f"<p><strong>Grace period:</strong> {esc(e['grace_period'])}</p>")
    parts.append(f"<p><strong>Common denial reasons:</strong> {esc(e['common_denial_reasons'])}</p>")
    parts.append(f"<p><strong>Bad faith:</strong> {esc(e['bad_faith'])}</p>")
    parts.append(f"<p><strong>How to appeal:</strong> {esc(e['appeal_rights'])}</p>")
    parts.append(f"<p><strong>How to complain:</strong> {esc(e['complaint_process'])}</p>")
    parts.append(
        f"<p><strong>State insurance regulator:</strong> "
        f'<a href="{esc(e["insurance_dept_url"])}" target="_blank" rel="noopener">{esc(e["insurance_dept_name"])}</a>. '
        f"File a complaint there if the insurer will not reconsider — it is free, and the regulator can investigate and sanction a company that broke the law.</p>"
    )
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
    )
    parts.append(
        f"<p><strong>What to do:</strong> Get the denial in writing "
        f"with the policy language it relies on. Check the dates "
        f"against the two-year rule and the grace period above. File a "
        f"complaint with the regulator linked above, and get free help "
        f"from the organization linked above before any deadline in "
        f"the policy runs out.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Get the denial "
        "in writing, with the exact policy language the insurer "
        "relied on. (2) Check the dates: was the death more than two "
        "years after the policy was issued, or inside the grace period "
        "after a missed premium? Either can defeat the denial. (3) Ask "
        "the insurer in writing to reconsider, with any supporting "
        "evidence. (4) File a complaint with your state insurance "
        "regulator — it is free. (5) If the insurer still will not "
        "pay, get free legal help before any deadline in the policy "
        "runs out.</p>"
    )
    parts.append(
        "<p><em>Sources: the official state insurance statutes, state "
        "insurance departments, and legal aid organizations linked in "
        "the research for this section, checked November 20, 2026. In "
        "all 50 states a life insurance policy becomes incontestable "
        "two years after issue; 40 states recognize a first-party "
        "bad-faith claim; California and Connecticut give at least a "
        "60-day grace period. Confirm the current law with a local "
        "attorney before you rely on it. This is general information, "
        "not legal advice.</em></p>"
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
            f"Life insurance claim denials in {state}</a></li>\n"
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
        r'<option value="breaking-a-lease-early" data-anchor="breaking-a-lease-early">.*?</option>',
        text,
        re.S,
    )
    assert m, "breaking-a-lease-early helper option not found"
    opt_old = m.group(0)
    opt_new = (
        opt_old
        + '\n<option value="life-insurance-claim-denials" data-anchor="life-insurance-claim-denials">'
        "Life insurance claim denials — why claims get denied, the two-year contestability period, grace periods, bad faith, and how to appeal or complain</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="breaking-a-lease-early"'
    idx = text.find(card_anchor)
    assert idx != -1, "breaking-a-lease-early card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="life-insurance-claim-denials">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-life-insurance-claim-denials.jpg" alt="Life Insurance Claim Denials" loading="lazy"></span>
          <h3>Life Insurance Claim Denials</h3>
          <p>When a life insurer denies a claim, the denial is not always the last word. Why claims get denied, the two-year contestability period, grace periods that keep a policy alive after a missed premium, when you can sue for bad faith, and how to appeal or file a complaint in your state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 61 topics" in text, "show-all label not found"
    text = text.replace("Show all 61 topics", "Show all 62 topics", 1)
    show_pos = text.find("Show all 62 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">61 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("61 topics", "62 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 61->62")


def build_about():
    text = ABOUT.read_text()
    assert text.count("106 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("106 legal topics", "107 legal topics", 1))
    print("  about.html: 106 -> 107")


def state_index_t(state, slug, e):
    bits = [
        "life insurance claim denial denied beneficiary appeal complaint",
        f"Life insurance claim denials in {state}",
        f"contestability period {e['contestability_period']}",
        f"grace period {e['grace_period']}",
        f"common denial reasons {e['common_denial_reasons']}",
        f"bad faith {e['bad_faith']}",
        f"appeal {e['appeal_rights']}",
        f"complaint {e['complaint_process']}",
        f"{e['insurance_dept_name']} {e['legal_aid_name']}",
        "two years incontestable material misstatement suicide exclusion lapse nonpayment",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11824, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = e["state"]
        slug = e.get("slug") or key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Life insurance claim denials in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Life Insurance Claim Denials",
            "t": (
                "life-insurance-claim-denials Life Insurance Claim Denials? "
                "When a life insurer denies a claim, the denial is not always the last word. Why claims get denied, "
                "the two-year contestability period, grace periods that keep a policy alive after a missed premium, "
                "when you can sue for bad faith, and how to appeal or file a complaint in your state. "
                "contestability two years incontestable grace period 30 days 60 days bad faith appeal complaint "
                "material misstatement suicide exclusion lapse nonpayment regulator."
            ),
        }
    )
    assert len(idx) == 11875, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11824 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    assert len(d) == 50, len(d)
    data = [(k, d[k]) for k in sorted(d)]  # keys already lowercase
    slugs = [(e.get("slug") or k.replace(" ", "-")) for k, e in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "appeal_rights", "bad_faith", "common_denial_reasons",
        "complaint_process", "contestability_period", "grace_period",
        "insurance_dept_name", "insurance_dept_url", "legal_aid_name",
        "legal_aid_url", "sources", "state",
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
        assert e["appeal_rights"] and e["bad_faith"] and e["common_denial_reasons"] and e["complaint_process"] and e["contestability_period"] and e["grace_period"] and e["insurance_dept_name"] and e["insurance_dept_url"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"] and e["state"], f"{k}: empty required field"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before breaking-a-lease-early section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
