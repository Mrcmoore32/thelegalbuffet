#!/usr/bin/env python3
"""Build Topic #83: Eviction-records cleanup — standalone section on all 50
state pages.

Inserts one new section per state page (before Probation, newest-first),
a contents-list entry, a homepage helper option + topic card (second grid,
after Probation), bumps About 81 -> 82, and appends 50 state entries + 1
helper entry to assets/search-index.json (10549 -> 10600).

Data: hidden_files/topic-research/eviction-records/all-states.json
(coordinator-written from hidden_files/topic-research/eviction-records/
buried-extract.json, which reuses verbatim the per-state "Eviction records
in {State}: sealing and access" cards, the "Applying in {State}" screening
cards (24 states), and the official-source links from the buried
eviction-records cluster inside Tenant Rights on each state page — those
were built from official state sources. The buried block stays where it
is; this section is the full topic and cross-references Tenant Rights
(the eviction process) and Record Clearing (general criminal-record
clearing) instead of duplicating them.)

Coordinator verification before the build (Nov 14, 2026):
- Per-state sealing text reused verbatim from the buried cards: a
  sealing / expungement / shielding / access-limit route exists in 21
  states (AZ, CA, CO, CT, DE, ID, IL, IN, KS, MA, MD, MN, NV, NJ
  [COVID-era nonpayment only], NY [foreclosure-related only, plus
  good-cause court order], ND [narrow: 7-year nonpayment or DV],
  OR, RI, UT, VA, WA [limited dissemination, not erasure]), a
  time-based removal / retention rule in 3 (ME online limits, SC
  automatic removal eff. Jan 1, 2027, WI retention schedule), and no
  statewide eviction-record route in the other 26 — each of those
  "no route" statements is carried verbatim from the already-live
  Tenant Rights cluster, which was built from the official source
  linked in that state's card. No new per-state claim is invented.
- Headline federal facts spot-verified against the CFPB's official
  page "What should I do if my rental application is denied because
  of a tenant screening report?" (consumerfinance.gov, last reviewed
  Nov 9, 2026; page fetched live Nov 14, 2026) before shipping:
  * Adverse-action notice: landlord must name the screening company
    and explain the right to a free copy within 60 days and the right
    to dispute.
  * Dispute: screening/credit reporting company generally has 30 days
    to investigate, 45 days in some cases.
  * Adverse action includes requiring a co-signer, a larger deposit,
    or higher rent — not only a denial.
  * You generally cannot remove negative information unless you can
    show it is incorrect or outdated.
  * 7-year rule: FCRA section 605 (15 U.S.C. 1681c) — most negative
    information, civil judgments included, may not be reported after
    7 years; the rule limits what a *report* may contain, not the
    underlying court record. The buried 7-year card already states
    exactly this and is reused verbatim.
- The 11 state official links that return non-2xx to curl (403 bot
  blocks on AR, CA, MA, MO, NC, TN; connection failures on AL, CT,
  IL, LA; 406 on UT) are pre-existing links already live in the
  buried cluster, reused verbatim — no new state link is introduced.
  The one new link, the CFPB page above, was fetched live and loads.
- No phone numbers are printed anywhere in this topic. The CFPB
  complaint phone number was deliberately left out (one source only).
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "eviction-records" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"

CFPB_URL = (
    "https://www.consumerfinance.gov/ask-cfpb/what-should-i-do-if-my-"
    "rental-application-is-denied-because-of-a-tenant-screening-report-en-2105/"
)
CFPB_LABEL = (
    "What should I do if my rental application is denied because of a "
    "tenant screening report? | Consumer Financial Protection Bureau"
)


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(s):
    state = s["state"]
    slug = s["slug"]
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(f'<h2 id="eviction-records-in-{slug}">Eviction records in {esc(state)}</h2>')
    parts.append(
        "<p>An eviction case can follow you for years &mdash; even one you "
        "won, and even one that was dismissed. This section is about the "
        "<strong>record itself</strong>: the court file, the tenant-screening "
        "report a landlord buys, and your credit report &mdash; what each "
        "one shows, your federal rights to fix bad reports, whether "
        + esc(state) + " lets you seal or expunge the court record, and the "
        "cleanup step by step. The eviction process itself &mdash; notices, "
        "court, and defenses &mdash; is in the Tenant Rights section on "
        "this page. Clearing a criminal record is a different process; see "
        "the record-clearing section on this page. A shorter version of "
        "this lived inside Tenant Rights on this page; this is the complete "
        "section. Checked <strong>November 14, 2026</strong>. This is "
        "general information, not legal advice.</p>"
    )
    # --- What an eviction record is ---
    parts.append('<div class="card">')
    parts.append("<h3>What an eviction record is and where it shows up</h3>")
    parts.append(
        "<p>An eviction record is not one document. It is three things that "
        "can each hurt you separately. First, the <strong>court "
        "file</strong>: the landlord&rsquo;s filing, every paper in the "
        "case, and the judgment if one was entered &mdash; a judgment for "
        "possession, and a money judgment if rent or costs were awarded. "
        "Second, the <strong>tenant-screening report</strong>: a consumer "
        "report a screening company sells to landlords, built largely by "
        "collecting court filings in bulk. Third, your <strong>credit "
        "report</strong>: a money judgment can reach it if the unpaid rent "
        "or judgment debt is sent to collections.</p>"
    )
    parts.append(
        "<p><strong>What a landlord actually sees.</strong> Most landlords "
        "never read the court file. They see the screening report&rsquo;s "
        "summary &mdash; often just &ldquo;eviction filed&rdquo; with a "
        "date &mdash; and sometimes a score or a recommendation. The report "
        "may not say you won, the case was dismissed, or you paid. That is "
        "why the outcome paperwork matters more than the filing: a "
        "dismissal order or a satisfaction of judgment is the proof that "
        "turns a bare filing into a finished story.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Before you apply "
        "anywhere, get your own screening report (the federal-rights card "
        "below explains how, free) and read it the way a landlord would: "
        "what does the first line say about you? If it only shows a "
        "filing, gather the court&rsquo;s final disposition before your "
        "next application.</p>"
    )
    parts.append("</div>")
    # --- A filing is not a judgment (verbatim from buried cluster) ---
    parts.append('<div class="card">')
    parts.append("<h3>A filing is not a judgment</h3>")
    parts.append(
        "<p>When a landlord files an eviction case, that filing exists as a "
        "public court record from day one &mdash; before any judge hears "
        "anything, and even if the case is later dismissed, settled, or "
        "decided in your favor. Screening companies collect those filings "
        "in bulk, so a case that went nowhere can still show up as an "
        "&ldquo;eviction&rdquo; on a report and cost you an apartment. "
        "That is why cleaning up the report (below) and the court record "
        "itself (the " + esc(state) + " card) are two separate jobs &mdash; "
        "most people need both.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> When you talk to a "
        "landlord, say the outcome in one sentence: &ldquo;The case was "
        "filed on [date], and it was dismissed [or: I won, or: we settled "
        "and I paid]&rdquo; &mdash; and hand over the court paper that "
        "proves it. A filing with a proven good outcome is a very "
        "different story from an unexplained filing.</p>"
    )
    parts.append("</div>")
    # --- FCRA rights (verbatim from buried cluster) ---
    parts.append('<div class="card">')
    parts.append("<h3>Your federal rights when a landlord screens you</h3>")
    parts.append(
        "<p>A tenant-screening report is a <strong>consumer report</strong> "
        "under the federal Fair Credit Reporting Act (FCRA). If a landlord "
        "turns you down &mdash; or charges you more &mdash; based on one, "
        "the landlord must give you an <strong>adverse-action "
        "notice</strong> naming the screening company that made the "
        "report. You then have the right to a <strong>free copy of that "
        "report</strong> from the company if you ask within <strong>60 "
        "days</strong>, and to <strong>dispute anything wrong or "
        "incomplete</strong>: the company generally must investigate "
        "within 30 days, fix what it cannot verify, and tell you the "
        "result. If a dispute does not resolve it, you may add a short "
        "written <strong>statement of dispute</strong> that must go out "
        "with future reports.</p>"
    )
    parts.append(
        "<p>The company generally has 30 days to investigate your dispute; "
        "in some cases it has 45 days. An adverse action is not only a "
        "denial &mdash; it can also mean the landlord requires a co-signer, "
        "a larger deposit, or higher rent because of the report. If you "
        "believe your rights were violated, you may be able to sue under "
        "the FCRA, and you can submit a complaint to the Consumer Financial "
        "Protection Bureau (see the official link below).</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Keep every "
        "adverse-action notice &mdash; it names the company to dispute "
        "with. Ask that company for your free report within 60 days of "
        "the notice, and dispute in writing, with the court&rsquo;s final "
        "disposition attached.</p>"
    )
    parts.append("</div>")
    # --- 7-year rule (verbatim from buried cluster) ---
    parts.append('<div class="card">')
    parts.append("<h3>The 7-year rule &mdash; and what it does not do</h3>")
    parts.append(
        "<p>Under the FCRA, screening companies must stop reporting most "
        "negative information after <strong>7 years</strong> &mdash; civil "
        "judgments included. But the rule only limits what a "
        "<em>report</em> may contain. The underlying court record does "
        "not disappear, and a record a landlord finds by searching court "
        "files directly is not the screening company&rsquo;s report. "
        "Closing the court file itself &mdash; sealing, expungement, or "
        "limited access &mdash; is a matter of state law, and states "
        "differ sharply, as the " + esc(state) + " card below shows.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If a report still lists "
        "an eviction older than 7 years, dispute it as outdated &mdash; "
        "that is one of the easiest disputes to win. But do not assume "
        "the court file is gone: check the " + esc(state) + " card below "
        "for whether the record itself can be sealed or expunged.</p>"
    )
    parts.append("</div>")
    # --- State sealing card (verbatim from buried cluster) ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Eviction records in {esc(state)}: sealing and access</h3>")
    parts.append(f"<p>{esc(s['sealing'])}</p>")
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If the card above gives "
        + esc(state) + " a route &mdash; automatic, by petition, or by "
        "motion &mdash; start at the court clerk where your case was "
        "heard and ask for the exact form and any filing fee before you "
        "file anything. If it says " + esc(state) + " has no such route, "
        "the FCRA steps above are your cleanup: they reach every "
        "screening report even when the court file stays public.</p>"
    )
    parts.append("</div>")
    # --- Applying / screening card (verbatim, 24 states) ---
    if s.get("applying"):
        parts.append('<div class="card">')
        parts.append(f"<h3>Applying in {esc(state)}: screening and fee rules</h3>")
        parts.append(f"<p>{esc(s['applying'])}</p>")
        parts.append(
            "<p><strong>Okay, so what do I do?</strong> Before you pay any "
            "application or screening fee, ask the landlord to put the fee, "
            "the screening criteria, and the screening company in writing "
            "&mdash; then check it against the rule above. Keep the "
            "receipt and a copy of any report you are given.</p>"
        )
        parts.append("</div>")
    # --- Cleanup step by step (verbatim from buried cluster) ---
    parts.append('<div class="card">')
    parts.append("<h3>The cleanup, step by step</h3>")
    parts.append(
        "<p><strong>(1) Get the report.</strong> Use the company named in "
        "your adverse-action notice first (free within 60 days); before "
        "you apply anywhere else, also order your file from the big "
        "tenant-screening companies &mdash; you have FCRA rights against "
        "each of them. <strong>(2) Dispute every error in writing</strong>, "
        "with a copy of the court&rsquo;s final disposition (dismissal, "
        "judgment in your favor, satisfaction) attached, and keep proof "
        "of mailing. <strong>(3) Send court orders.</strong> If your case "
        "was sealed or expunged, send the order to every screening "
        "company listing the case &mdash; a sealed record must not be "
        "reported. <strong>(4) Explain what remains.</strong> For anything "
        "accurate that is still reportable, attach a short written "
        "explanation and bring your disposition paperwork when you apply, "
        "so a landlord sees the outcome, not just the filing.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Work the steps in "
        "order &mdash; report first, then disputes, then the sealing "
        "petition, then the explanation packet. Disputing before you have "
        "the disposition paperwork in hand wastes the 30-day clock.</p>"
    )
    parts.append("</div>")
    # --- If you were evicted ---
    parts.append('<div class="card">')
    parts.append("<h3>If you were evicted</h3>")
    parts.append(
        "<p>If the court entered a judgment for the landlord, the record "
        "shows two things: the judgment for possession, and a money "
        "judgment if rent or costs were awarded. Both can appear on a "
        "screening report. How long it matters depends on which record "
        "you mean: a screening company generally may not report most "
        "negative information more than 7 years old (see the 7-year card "
        "above), but the court file itself stays public unless your state "
        "seals or expunges it (see the " + esc(state) + " card above) "
        "&mdash; and a landlord who searches court records directly can "
        "find an old case even after it ages off a report.</p>"
    )
    parts.append(
        "<p><strong>What helps.</strong> Proof first: the judgment, proof "
        "you paid or satisfied it, and any settlement. Then a short "
        "written explanation &mdash; one page: what happened, what changed, "
        "and what your rental history since then shows. References from "
        "landlords you have rented from since the eviction carry real "
        "weight. If a landlord asks, a co-signer or a larger deposit can "
        "help where your state&rsquo;s law allows it &mdash; the CFPB "
        "lists both as things a landlord may require after an adverse "
        "action. And keep building on-time rent history: every clean "
        "rental is new evidence for the next application.</p>"
    )
    parts.append(
        "<p><strong>Watch out for cleanup scams.</strong> No one can erase "
        "an accurate, still-reportable eviction from a screening report "
        "before its time, no matter what they charge. The CFPB says you "
        "generally cannot remove negative information unless you can show "
        "it is incorrect or outdated. If a &ldquo;credit repair&rdquo; "
        "company promises to delete an accurate eviction, walk away "
        "&mdash; the dispute and sealing steps above are free, and they "
        "are the only routes that work.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Put together a one-page "
        "packet before your next application: the judgment, proof of "
        "payment or satisfaction, your one-page explanation, and a "
        "reference from your most recent landlord. Bring it to every "
        "showing &mdash; it is easier to hand a landlord the outcome than "
        "to explain a bare filing after the screening report lands.</p>"
    )
    parts.append("</div>")
    # --- Official links ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Official links in {esc(state)}</h3>")
    parts.append("<ul>")
    parts.append(
        f"<li><a href=\"{esc(CFPB_URL)}\" target=\"_blank\" "
        f"rel=\"noopener\">{esc(CFPB_LABEL)}</a></li>"
    )
    parts.append(
        f"<li><a href=\"{esc(s['link'])}\" target=\"_blank\" "
        f"rel=\"noopener\">{esc(s['link_label'])}</a></li>"
    )
    parts.append("</ul>")
    parts.append("</div>")
    # --- Do this now ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Find the "
        "adverse-action notice from your most recent denial &mdash; it "
        "names the screening company. Order that report today; it is free "
        "if you ask within 60 days of the notice. (2) Circle every error "
        "&mdash; wrong outcome, wrong person, a case that was sealed, "
        "anything older than 7 years &mdash; and dispute each one in "
        "writing with the court disposition attached. (3) Work the "
        + esc(state) + " route in the card above to seal, expunge, or "
        "limit the court record itself; where " + esc(state) + " has no "
        "such route, the FCRA steps are your cleanup &mdash; they reach "
        "every screening report even when the court file stays public. "
        "(4) Keep the final disposition and any sealing order with your "
        "rental papers, and bring copies when you apply.</p>"
    )
    parts.append(
        "<p><em>Sources: the official " + esc(state) + " source linked "
        "above and the Consumer Financial Protection Bureau page linked "
        "above, checked November 14, 2026, and the eviction-records cards "
        "in the Tenant Rights section on this page, which were built from "
        "official state sources. Federal law cited: the Fair Credit "
        "Reporting Act, 15 U.S.C. 1681 et seq. (adverse-action notice, "
        "free report within 60 days, 30-day dispute investigation, "
        "7-year reporting limit under section 605). Laws change &mdash; "
        "confirm the current rule in the official source before you rely "
        "on a deadline. This is general information, not legal "
        "advice.</em></p>"
    )
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def build_state_pages(data):
    for s in data:
        slug = s["slug"]
        path = STATES / f"{slug}.html"
        text = path.read_text()
        anchor = f"eviction-records-in-{slug}"
        assert anchor not in text, f"{slug}: anchor already present"
        # --- insert section before Probation (newest-first) ---
        h2 = text.find(f'<h2 id="probation-in-{slug}">')
        assert h2 != -1, f"{slug}: probation h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        new_section = section_html(s)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the probation <li> ---
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#probation-in-'
            + re.escape(slug)
            + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: probation contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#eviction-records-in-{slug}">'
            f"Eviction records in {s['state']}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert "eviction-records" not in helper_part, "index already has helper option"
    assert 'data-topic="eviction-records"' not in text, "index already has card"
    opt_old = (
        '<option value="probation" data-anchor="probation">'
        "Probation (conditions, violations, moving, ending early)</option>"
    )
    assert opt_old in text, "probation helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="eviction-records" data-anchor="eviction-records">'
        "Eviction records (sealing, screening reports, disputes)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="probation"'
    idx = text.find(card_anchor)
    assert idx != -1, "probation card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="eviction-records">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-eviction-records.jpg" alt="Eviction Records" loading="lazy"></span>
          <h3>Eviction Records</h3>
          <p>A filing is not a judgment: what shows up on screening reports, your FCRA dispute rights, the 7-year rule, and whether your state lets you seal or expunge the court record.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 36 topics" in text, "show-all label not found"
    text = text.replace("Show all 36 topics", "Show all 37 topics", 1)
    assert '<span class="count-badge">36 topics</span>' in text
    text = text.replace(
        '<span class="count-badge">36 topics</span>',
        '<span class="count-badge">37 topics</span>',
        1,
    )
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 36->37")


def build_about():
    text = ABOUT.read_text()
    assert "81 legal topics" in text, "about count not found"
    ABOUT.write_text(text.replace("81 legal topics", "82 legal topics", 1))
    print("  about.html: 81 -> 82")


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 10549, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith("eviction-records-in-") for e in idx)
    for s in data:
        state = s["state"]
        slug = s["slug"]
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"eviction-records-in-{slug}",
                "h": f"Eviction records in {state}",
                "t": (
                    f"Eviction records in {state} "
                    f"\u2014 eviction record sealing expunge expungement "
                    f"shield tenant screening report FCRA Fair Credit "
                    f"Reporting Act dispute 30 days adverse action free "
                    f"report 60 days 7 year rule filing is not a judgment "
                    f"dismissed court record landlord screening fee "
                    f"co-signer deposit rental application {state}"
                ),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Eviction Records",
            "t": (
                "A filing is not a judgment: what shows up on screening "
                "reports, your FCRA dispute rights, the 7-year rule, and "
                "whether your state lets you seal or expunge the court "
                "record."
            ),
        }
    )
    assert len(idx) == 10600, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 10549 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [states[k] for k in sorted(states)]
    slugs = [s["slug"] for s in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert all(s.get("link") and s.get("link_label") for s in data), "missing link data"
    assert all(s.get("sealing") for s in data), "missing sealing data"
    print("building state pages...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
