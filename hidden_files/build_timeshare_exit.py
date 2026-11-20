#!/usr/bin/env python3
"""Build Topic #109: Timeshare Exit — standalone section on all 50 state
pages.

Inserts one new section per state page (before Life Insurance Claim
Denials, newest-first), a contents-list entry (before the
life-insurance-claim-denials <li>), a homepage helper option + topic
card (after Life Insurance Claim Denials), bumps About 107 -> 108, and
appends 50 state entries + 1 helper entry to
assets/search-index.json (11875 -> 11926).

Data: hidden_files/topic-research/timeshare-exit/all-states.json
(coordinator-merged 2026-11-20 from 5 research batches).

URL/verification work 2026-11-20:
- Illinois repeal CONFIRMED by a second official source: Justia's
  2025 Illinois Compiled Statutes Ch. 765 lists "765 ILCS 101/ -
  Real Estate Timeshare Act of 1999. (Repealed by P.A. 100-534)";
  Wesley Financial Group agrees. Researcher said "repealed in 2017"
  — corrected to cite P.A. 100-534 with no year claim.
- Montana repeal confirmed by two independent sources (candidyak,
  eazy-out): § 37-53-304 repealed by SB 455 (2023), Ch. 482.
- Arizona 10 days confirmed against current statute text
  (A.R.S. § 32-2197.03, 2019 amendment from 7 to 10 days).
- New Mexico complaint URL confirmed live by text fetch
  (nmag.gov "Submit a Complaint").
- Alabama complaint URL could NOT be live-confirmed (curl 000 and
  text fetch both network errors, not 404s) -> pointed at the AG
  homepage https://www.alabamaag.gov/ (verified live).
- Virginia complaint URL: stripped the ?ref=munwalker.com tracker
  the researcher reproduced verbatim; clean base path kept.
- South Dakota 200, Arizona AG 200 by curl.

Headline counts (computed from the dataset): 45 states give a
statutory window to cancel a new timeshare purchase, from 72 hours
(Indiana) to 15 days (Alaska); 5 states have no statutory cooling-off
right at all (Illinois, Kansas, Montana, North Dakota, Wyoming) —
there your contract is all you have. Ohio has only a 3-business-day
home-solicitation right. 12 states have no dedicated timeshare
statute. No phone numbers in the dataset.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "timeshare-exit" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-timeshare-exit.jpg"

SLUG = "timeshare-exit"
TITLE = "Timeshare Exit"
PREV_SLUG = "life-insurance-claim-denials"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(state, slug, e):
    law = e["state_law"] or (
        f"{state} has no dedicated timeshare statute — the rules that "
        "apply come from the cancellation and consumer-protection "
        "provisions cited in this section."
    )
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="timeshare-exit-in-{slug}">Timeshare exit in {esc(state)}</h2>'
    )
    parts.append(
        "<p>A timeshare can feel like a trap: the maintenance fees keep "
        "rising, you cannot use the weeks you bought, and the resort "
        "will not take it back. Getting out is possible, but the route "
        "depends on <strong>when</strong> you bought it. If you just "
        "signed, most states give you a short window — usually "
        "<strong>3 to 15 days</strong> — to cancel the purchase for a "
        "full refund, no reason needed. In <strong>45 states</strong> "
        "that window exists by law; in <strong>5 states</strong> "
        "(Illinois, Kansas, Montana, North Dakota, and Wyoming) there "
        "is no statutory cooling-off right at all, and your contract "
        "is all you have. After the window closes, the realistic exits "
        "are a deed-back to the resort, a resale or giveaway, or — as "
        "a last resort — stopping payments and facing foreclosure. And "
        "the exit industry is full of scams: any company that demands "
        "a large fee up front to sell or transfer your timeshare, "
        "especially one that claims a buyer is already waiting, is a "
        "red flag. The picture here is as of <strong>November "
        "2026</strong>. This is general information, not legal advice.</p>"
    )
    # --- Card 1: the cooling-off window ---
    parts.append('<div class="card">')
    parts.append("<h3>The cooling-off window: your best exit, and it is short</h3>")
    parts.append(
        "<p>Almost every state that regulates timeshares gives a new "
        "buyer a brief right to cancel — the rescission or cooling-off "
        "period. It runs from <strong>72 hours</strong> (Indiana) to "
        "<strong>15 days</strong> (Alaska), and most states land at 5, "
        "7, or 10 days. The clock usually starts when you sign, or "
        "when you receive the disclosure documents, whichever is later. "
        "Cancel inside the window and you get a full refund. Miss it "
        "by a day and the right is gone — there is no second window "
        "for regret or rising fees. Five states have no statutory "
        "window at all, and a few more only give one in narrow cases "
        "(Ohio&rsquo;s 3-business-day right, for example, applies only "
        "if the sale was a home solicitation sale). Check your "
        "contract too: it must disclose the cancellation right, and "
        "some contracts give you more time than the statute does.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Find the date you "
        "signed and the date you received the disclosure documents, "
        "then count the days against your state&rsquo;s window in the "
        "card below. If you are still inside it, cancel "
        "<strong>today</strong> — do not wait for the resort to call "
        "you back.</p>"
    )
    parts.append("</div>")
    # --- Card 2: how to cancel ---
    parts.append('<div class="card">')
    parts.append("<h3>How to cancel in time</h3>")
    parts.append(
        "<p>Cancellation must be <strong>in writing</strong>, sent to "
        "the developer at the address in your contract, before the "
        "deadline runs out. In most states a mailed notice counts on "
        "the postmark date, so certified mail with return receipt "
        "requested is the safest way to prove you cancelled on time. "
        "Some states also allow hand delivery or email. Keep a copy "
        "of the notice and the mailing receipt, and expect your refund "
        "within 15 to 45 days depending on the state — the developer "
        "must return all the money you paid. The right to cancel "
        "cannot be waived in most states, so a contract clause that "
        "says otherwise does not bind you.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Write a short "
        "cancellation letter today, name the contract and the date you "
        "signed, and send it by certified mail to the address in your "
        "contract. Photograph the letter and the receipt, and keep "
        "both. If the refund does not arrive on time, file a complaint "
        "with the agency linked in the card below.</p>"
    )
    parts.append("</div>")
    # --- Card 3: after the window ---
    parts.append('<div class="card">')
    parts.append("<h3>After the window closes: your real options</h3>")
    parts.append(
        "<p>Once the cooling-off period ends, there is no legal right "
        "to cancel just because you changed your mind. The realistic "
        "exits, in order of safety, are: <strong>(1) a deed-back or "
        "surrender</strong> — ask the resort in writing to take the "
        "timeshare back, and get any release in writing before you "
        "stop paying; many resorts run such programs quietly. "
        "<strong>(2) Resale or giveaway</strong> — you can sell or "
        "give the timeshare away, but only after the loan is paid off "
        "and the fees are current, and resale prices are usually very "
        "low, sometimes near zero. <strong>(3) Stop paying</strong> — "
        "the resort can foreclose and report the missed payments, "
        "which can damage your credit for years, so talk to a lawyer "
        "before you do this. Paying off the loan first makes every "
        "other option easier.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Write to the "
        "resort and ask about a deed-back or surrender program — put "
        "it in writing and keep the reply. If they say no, ask again "
        "in a few months; programs change. Do not sign anything that "
        "promises an exit for a fee until you have checked the company "
        "with your attorney general.</p>"
    )
    parts.append("</div>")
    # --- Card 4: scams ---
    parts.append('<div class="card">')
    parts.append("<h3>Exit scams: the upfront-fee trap</h3>")
    parts.append(
        "<p>The timeshare exit business is one of the most "
        "scam-ridden corners of consumer law. The classic pattern: a "
        "company cold-calls you, claims a buyer is already waiting for "
        "your timeshare at a high price, and demands a large fee up "
        "front — thousands of dollars — before any sale. Once you pay, "
        "the buyer never appears and the company disappears. A "
        "legitimate resale broker is paid a commission <strong>only "
        "after a sale actually closes</strong>. Several states ban "
        "resale brokers from charging advance fees at all. Other scams "
        "sell you a worthless &ldquo;transfer&rdquo; that never "
        "actually moves the deed out of your name, leaving you still "
        "on the hook for the fees.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Never pay a large "
        "fee in advance for a promised sale or transfer. Check any "
        "exit company with your attorney general or consumer "
        "protection office before you sign or pay, and get any promise "
        "in writing. If a company already took your money and did "
        "nothing, file a complaint with the agency in the card below "
        "and report it to the FTC at ReportFraud.ftc.gov.</p>"
    )
    parts.append("</div>")
    # --- Card 5: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Timeshare exit in {esc(state)}</h3>")
    parts.append(f"<p><strong>Cooling-off window:</strong> {esc(e['rescission_period'])}</p>")
    parts.append(f"<p><strong>How to cancel:</strong> {esc(e['rescission_how'])}</p>")
    parts.append(f"<p><strong>After the window closes:</strong> {esc(e['exit_options'])}</p>")
    parts.append(f"<p><strong>Scam warning:</strong> {esc(e['resale_scam_warning'])}</p>")
    parts.append(f"<p><strong>State law:</strong> {esc(law)}</p>")
    parts.append(
        f"<p><strong>Where to complain:</strong> "
        f'<a href="{esc(e["complaint_agency_url"])}" target="_blank" rel="noopener">{esc(e["complaint_agency_name"])}</a>. '
        f"File a complaint there if a resort or exit company misled you or took your money and did nothing.</p>"
    )
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
    )
    parts.append(
        f"<p><strong>What to do:</strong> Check the dates against the "
        f"cooling-off window above. If you are still inside it, cancel "
        f"in writing today by certified mail. If the window has "
        f"closed, ask the resort in writing about a deed-back, and get "
        f"free help from the organization linked above before you stop "
        f"paying or sign any exit contract.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Check the "
        "dates: are you still inside your state&rsquo;s cooling-off "
        "window? If yes, cancel in writing today by certified mail. "
        "(2) If the window has closed, ask the resort in writing "
        "about a deed-back or surrender program. (3) Never pay a large "
        "fee in advance to any exit or resale company — check it with "
        "your attorney general first. (4) If a company took your money "
        "and did nothing, file a complaint with the agency above and "
        "report it to the FTC at ReportFraud.ftc.gov.</p>"
    )
    parts.append(
        "<p><em>Sources: the official state timeshare statutes, state "
        "attorneys general and consumer protection agencies, and legal "
        "aid organizations linked in the research for this section, "
        "checked November 20, 2026. In 45 states a new timeshare "
        "purchase can be cancelled within a short statutory window "
        "(72 hours to 15 days); Illinois, Kansas, Montana, North "
        "Dakota, and Wyoming have no statutory cooling-off right. "
        "Confirm the current law with a local attorney before you rely "
        "on it. This is general information, not legal advice.</em></p>"
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
            f"Timeshare exit in {state}</a></li>\n"
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
        r'<option value="life-insurance-claim-denials" data-anchor="life-insurance-claim-denials">.*?</option>',
        text,
        re.S,
    )
    assert m, "life-insurance-claim-denials helper option not found"
    opt_old = m.group(0)
    opt_new = (
        opt_old
        + '\n<option value="timeshare-exit" data-anchor="timeshare-exit">'
        "Timeshare exit — the cooling-off window to cancel a new purchase, deed-backs, resale, and exit scams</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="life-insurance-claim-denials"'
    idx = text.find(card_anchor)
    assert idx != -1, "life-insurance-claim-denials card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="timeshare-exit">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-timeshare-exit.jpg" alt="Timeshare Exit" loading="lazy"></span>
          <h3>Timeshare Exit</h3>
          <p>Stuck with a timeshare you can't use? The short cooling-off window to cancel a new purchase, what to do after it closes, deed-backs, resale, and how to spot the upfront-fee exit scams — state by state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 62 topics" in text, "show-all label not found"
    text = text.replace("Show all 62 topics", "Show all 63 topics", 1)
    show_pos = text.find("Show all 63 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">62 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("62 topics", "63 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 62->63")


def build_about():
    text = ABOUT.read_text()
    assert text.count("107 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("107 legal topics", "108 legal topics", 1))
    print("  about.html: 107 -> 108")


def state_index_t(state, slug, e):
    law = e["state_law"] or f"{state} has no dedicated timeshare statute"
    bits = [
        "timeshare exit cancel rescission cooling-off deed-back resale scam",
        f"Timeshare exit in {state}",
        f"cooling-off window {e['rescission_period']}",
        f"how to cancel {e['rescission_how']}",
        f"after the window {e['exit_options']}",
        f"scam warning {e['resale_scam_warning']}",
        f"{law}",
        f"{e['complaint_agency_name']} {e['legal_aid_name']}",
        "cancel purchase refund certified mail deed-back surrender foreclosure upfront fee",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11875, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = e["state"]
        slug = e.get("slug") or key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Timeshare exit in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Timeshare Exit",
            "t": (
                "timeshare-exit Timeshare Exit? "
                "Stuck with a timeshare you can't use? The short cooling-off window to cancel a new purchase, "
                "what to do after it closes, deed-backs, resale, and how to spot the upfront-fee exit scams — "
                "state by state. "
                "cooling-off rescission cancel purchase refund certified mail deed-back surrender foreclosure "
                "upfront fee scam resale transfer."
            ),
        }
    )
    assert len(idx) == 11926, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11875 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    assert len(d) == 50, len(d)
    data = [(k, d[k]) for k in sorted(d)]  # keys already lowercase
    slugs = [(e.get("slug") or k.replace(" ", "-")) for k, e in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "complaint_agency_name", "complaint_agency_url", "exit_options",
        "legal_aid_name", "legal_aid_url", "rescission_how",
        "rescission_period", "resale_scam_warning", "sources", "state",
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
        assert e["complaint_agency_name"] and e["complaint_agency_url"] and e["exit_options"] and e["legal_aid_name"] and e["legal_aid_url"] and e["rescission_how"] and e["rescission_period"] and e["resale_scam_warning"] and e["sources"] and e["state"], f"{k}: empty required field"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before life-insurance-claim-denials section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
