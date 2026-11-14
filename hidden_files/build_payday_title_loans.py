#!/usr/bin/env python3
"""Build Topic #81: Payday / title loans — standalone section on all 50
state pages.

Inserts one new section per state page (before Manufactured-home parks,
newest-first), a contents-list entry, a homepage helper option + topic
card (second grid, after Manufactured-home parks), bumps About 79 -> 80,
and appends 50 state entries + 1 helper entry to assets/search-index.json
(10447 -> 10498).

Data: hidden_files/topic-research/payday-title-loans/all-states.json
(coordinator-written; see make_dataset.py for the source trail).

Coordinator verification before the build (Nov 14, 2026):
- State payday-law cards, title-loan cards, and the official source link
  are reused verbatim from the buried "Payday loans, title loans, and
  the safer ways out" cluster inside Credit Card & Debt on each state
  page, which was built from official state sources. The buried block
  stays where it is; this section goes further (cost math, cap/ban/
  licensing table, payment-plan rights, getting out, scams) and
  cross-references Credit Card & Debt instead of duplicating it.
- Status map: 12 ban (AZ, AR, CT, GA, MD, MA, NJ, NY, NC, PA, VT, WV),
  11 cap at 36% APR (CO, HI, IL, MN, MT, NE, NH, NM, OR, SD, VA),
  2 reformed (ME ~30% ceiling, OH 28% + 60% total cap, installment),
  25 license fee-based payday lending.
- Headline figures spot-verified against official sources before
  shipping: $15/$100/14 days = 391% APR (computed); PAL I $200-$1,000
  and PAL II up to $2,000 at 28% APR, $20 max fee, no rollovers (NCUA
  rule); VA 36% + fee + 50%/60% total cap (Va. Code 6.2-1817, 6.2-1818.3);
  FL title tiers 30/24/18% (Fla. Stat. 537.011); OK 17%/month,
  $1,500 aggregate principal, 60 days-12 months (Small Lenders Act);
  OH 28%, $1,000 max, 91 days-1 year, 60% total cap (R.C. 1321.40);
  RI deferred-deposit law repealed Jan 1, 2027.
- Extended payment plans verified against OFFICIAL statute or regulator
  text for 16 states (AL, AK, DE, FL, ID, IL, IN, LA, MI, NE, NV, SC,
  UT, WA, WI, WY). Every other state gets a claim-free fallback, not
  an invented EPP. Two secondary-source claims were rejected by that
  verification: Missouri (EPP only in a 2014 bill that never passed)
  and Oklahoma (old EPP died with deferred deposit lending in 2020).
  Hawaii, Ohio, Oklahoma, and Virginia get an installment-by-law note
  instead of an EPP claim.
- No phone numbers are printed anywhere in this topic.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "payday-title-loans" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"

TOPIC = "payday-title-loans"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def cell(v, state, banned):
    if v:
        return esc(v)
    if banned:
        return f"Does not apply &mdash; payday lending is illegal in {esc(state)}."
    return "Not stated in the sources checked."


def epp_block(s):
    state = s["state"]
    if s.get("epp"):
        return (
            "<p><strong>Yes &mdash; state law gives you a payment-plan right in "
            + esc(state) + ".</strong> " + esc(s["epp"]) + "</p>"
            "<p>Ask in writing, before the due date, using the words "
            "&ldquo;I am requesting the Extended Payment Plan under state "
            "law.&rdquo; Get the lender&rsquo;s answer in writing the same "
            "day, sign the new payment schedule, keep a copy, and do not "
            "take out a new loan to pay the plan. While you are current on "
            "the plan, the lender generally cannot start collection "
            "activity on it.</p>"
        )
    if s.get("epp_installment"):
        return (
            "<p><strong>No separate extended payment plan to ask for:</strong> "
            "in " + esc(state) + ", these loans are already installment "
            "loans by law, repaid in monthly installments over months "
            "rather than in one lump sum on payday &mdash; see the "
            + esc(state) + " card above. If you still cannot make an "
            "installment, ask the lender in writing for a hardship "
            "arrangement before you miss the payment, and keep the reply.</p>"
        )
    if s["status"] == "banned":
        return (
            "<p><strong>There is no legal payday loan to put on a payment "
            "plan in " + esc(state) + ":</strong> payday lending is illegal "
            "here, so there is no legal payday loan to put on a payment "
            "plan. If an online lender made you one anyway, the loan may "
            "be void and uncollectible &mdash; see the " + esc(state)
            + " card above &mdash; and complain to the official source "
            "below.</p>"
        )
    return (
        "<p><strong>No extended-payment-plan right is printed for "
        + esc(state) + " in this section</strong> &mdash; in the sources "
        "checked, no verified state-law right to demand an installment "
        "plan on a payday loan was found for " + esc(state) + ". That does "
        "not leave you without options: ask the lender in writing for an "
        "installment plan before the due date anyway &mdash; some lenders, "
        "including members of the CFSA trade group, offer one voluntarily "
        "&mdash; and if the lender refuses, complain to the official "
        "source below.</p>"
    )


def section_html(s):
    state = s["state"]
    slug = s["slug"]
    banned = s["status"] == "banned"
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="payday-title-loans-in-{slug}">Payday / Title Loans in {esc(state)}</h2>'
    )
    parts.append(
        "<p>A payday loan is a small loan due in full on your next payday "
        "&mdash; usually a few hundred dollars, at a fee that looks small "
        "and isn&rsquo;t. A title loan borrows against your car. The rules "
        "are completely different from state to state: some states cap the "
        "cost at 36% APR or ban these loans outright, and others let "
        "lenders charge what they want. This section is the full picture "
        "for " + esc(state) + ": what the loan really costs, where "
        + esc(state) + " stands, title loans and your car, payment-plan "
        "rights, how to get out of a loan you already have, and the scams "
        "to watch for. For the wider debt picture &mdash; collection, "
        "default judgments, and negotiating other debts &mdash; see "
        "Credit Card &amp; Debt on this page. Checked <strong>November 14, "
        "2026</strong>. This is general information, not legal advice.</p>"
    )
    # --- What it really costs ---
    parts.append('<div class="card">')
    parts.append("<h3>What a payday loan really costs</h3>")
    parts.append(
        "<p>The standard pitch is about <strong>$15 for every $100 "
        "borrowed</strong>, due in about two weeks. That sounds like 15%. "
        "Stated the way other loans are priced, it is roughly "
        "<strong>391% APR</strong> &mdash; the math is $15 &divide; $100 = "
        "15% for two weeks, and 15% &times; (365 &divide; 14) &asymp; 391% "
        "a year. A $300 loan at that price costs $45 for two weeks, and "
        "the real damage comes from repeat borrowing: if you cannot pay "
        "the whole amount plus the fee on payday, a new loan (or a "
        "rollover, where allowed) starts the fee clock again, and the "
        "Consumer Financial Protection Bureau has found most payday loans "
        "go to borrowers who take out loan after loan. Price any payday "
        "or title loan by its APR and its total payback amount &mdash; "
        "never by the fee alone.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Before you sign, ask "
        "the lender for the APR and the total amount you will pay back, in "
        "writing. If the APR is in triple digits, treat the loan as a last "
        "resort and price the safer exits below first.</p>"
    )
    parts.append("</div>")
    # --- Two-strike rule ---
    parts.append('<div class="card">')
    parts.append("<h3>Your bank account: the federal two-strike rule</h3>")
    parts.append(
        "<p>Since March 30, 2025, a federal CFPB rule has limited how "
        "payday, title, and similar high-cost lenders can pull payments "
        "from your bank account: after <strong>two consecutive failed "
        "withdrawal attempts</strong>, the lender must get your "
        "<strong>new written authorization</strong> before trying again, "
        "and it must send you payment notices. Know the limits of that "
        "rule, too: the CFPB announced in March 2025 that it is "
        "<strong>not prioritizing enforcement</strong> of these payment "
        "provisions, and the rule never capped prices &mdash; a planned "
        "federal requirement that lenders check you can afford the loan "
        "was repealed in 2020. <strong>The " + esc(state) + " law below is "
        "your main protection.</strong></p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If the lender keeps "
        "debiting your account, revoke the debit authorization: tell the "
        "lender in writing, tell your bank, and keep copies &mdash; the "
        "two-strike rule above also limits repeat failed attempts.</p>"
    )
    parts.append("</div>")
    # --- Military ---
    parts.append('<div class="card">')
    parts.append("<h3>In the military? Federal law caps the cost at 36%</h3>")
    parts.append(
        "<p>The federal Military Lending Act caps <strong>active-duty "
        "servicemembers and their dependents</strong> at a <strong>36% "
        "military annual percentage rate</strong> on payday loans, title "
        "loans, and most other consumer credit &mdash; and a loan made "
        "over that cap to a covered borrower is void. Lenders must check "
        "military status before lending. If a lender charged you more, "
        "complain to the CFPB and your installation legal assistance "
        "office.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you are covered and "
        "were charged over 36%, do not keep paying the overcharge: complain "
        "to the CFPB and your installation legal assistance office, and "
        "keep the loan papers.</p>"
    )
    parts.append("</div>")
    # --- Where the state stands ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Where {esc(state)} stands</h3>")
    parts.append(f"<p><strong>{esc(s['status_line'])}</strong></p>")
    parts.append('<table class="ws-table">')
    parts.append(
        f"<thead><tr><th></th><th>In {esc(state)}</th></tr></thead><tbody>"
    )
    parts.append(
        f"<tr><th scope=\"row\">Status</th><td>{esc(s['status_label'])}</td></tr>"
    )
    parts.append(
        f"<tr><th scope=\"row\">Rate cap</th><td>{cell(s['cap'], state, banned)}</td></tr>"
    )
    parts.append(
        f"<tr><th scope=\"row\">Biggest loan</th><td>{cell(s['max_loan'], state, banned)}</td></tr>"
    )
    parts.append(
        f"<tr><th scope=\"row\">Longest term</th><td>{cell(s['max_term'], state, banned)}</td></tr>"
    )
    parts.append(
        f"<tr><th scope=\"row\">License</th><td>{cell(s['license'], state, banned)}</td></tr>"
    )
    parts.append("</tbody></table>")
    parts.append(f"<p>{esc(s['payday'])}</p>")
    parts.append(
        "<p>Across the country: 12 states ban payday lending outright, 11 "
        "more cap it at 36% APR, Maine and Ohio reformed it into "
        "installment lending, and 25 states still license fee-based payday "
        "loans. Wherever you live, the federal protections in the cards "
        "above apply.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check the row that "
        "matters to you in the table above &mdash; the rate cap first, "
        "then the biggest loan and the license. If a lender offers you "
        "terms that break the cap or the limits, do not sign: complain to "
        "the official source below.</p>"
    )
    parts.append("</div>")
    # --- Title loans ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Title loans in {esc(state)}</h3>")
    parts.append(
        "<p>A title loan is not like a payday loan with a different name "
        "&mdash; you hand the lender a claim on your car&rsquo;s title, "
        "and if you miss payments the lender can <strong>repossess and "
        "sell the car</strong>, often without going to court first. Losing "
        "the car usually means losing the ride to work, which makes the "
        "debt harder, not easier. If a lender has taken or threatens to "
        "take your vehicle, read the <strong>Car Repossession</strong> "
        "section of this page for your rights and the steps to get the car "
        "back.</p>"
    )
    parts.append(f"<p>{esc(s['title'])}</p>")
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Before you pledge a "
        "car title, ask what happens on the first missed payment &mdash; "
        "how many days before repossession, and what fees get added. If "
        "the car is how you get to work, a title loan risks the job that "
        "pays the loan: try the safer exits below first.</p>"
    )
    parts.append("</div>")
    # --- Payment plans ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Can you get more time? Payment plans in {esc(state)}</h3>")
    parts.append(
        "<p>An extended payment plan turns one balloon payment into several "
        "smaller installments timed to your paydays &mdash; usually at no "
        "extra interest or fees. It is not a rollover: a rollover pushes "
        "the due date two weeks in exchange for another full fee, while a "
        "payment plan is designed to pay the loan off. In most states that "
        "require one, you must ask <strong>before the due date</strong> "
        "&mdash; miss that window and the lender can legally refuse.</p>"
    )
    parts.append(epp_block(s))
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> The day you realize "
        "you cannot pay in full, call or visit the lender and use the "
        "exact words: &ldquo;I am requesting the Extended Payment Plan "
        "under state law.&rdquo; Do not say &ldquo;extend&rdquo; or "
        "&ldquo;renew&rdquo; &mdash; those words usually mean a rollover.</p>"
    )
    parts.append("</div>")
    # --- Getting out ---
    parts.append('<div class="card">')
    parts.append("<h3>If you already have one: how to get out</h3>")
    parts.append(
        "<p><strong>(1) Ask for the payment plan above</strong>, in "
        "writing, before the due date. <strong>(2) Do not roll it over or "
        "take a second loan to pay the first</strong> &mdash; that is how "
        "a $300 loan becomes a $1,000 problem. <strong>(3) Stop the "
        "automatic withdrawals</strong> if the lender keeps debiting your "
        "account: revoke the authorization in writing to the lender and "
        "your bank, and keep copies. <strong>(4) Get free help from a "
        "nonprofit credit counselor</strong> (look for NFCC members): they "
        "review your budget for free or nearly free and can negotiate with "
        "creditors for you. <strong>(5) Complain to the official source "
        "below and to the CFPB</strong> if the lender broke the caps, "
        "refused a payment plan the law gives you, or is unlicensed "
        "&mdash; in several states an illegal loan is void and "
        "uncollectible. <strong>(6) If a collector threatens you</strong>, "
        "know this: you cannot be jailed for not paying a payday loan "
        "&mdash; it is a civil debt, not a crime, and a collector who "
        "threatens arrest is breaking the law.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Today: ask for the "
        "payment plan in writing, revoke any automatic withdrawal you do "
        "not want, and call a nonprofit credit counselor. This week: "
        "complain to the regulator if the lender broke the rules.</p>"
    )
    parts.append("</div>")
    # --- Safer exits ---
    parts.append('<div class="card">')
    parts.append("<h3>Safer exits to try first</h3>")
    parts.append(
        "<p><strong>(1) A credit union Payday Alternative Loan (PAL).</strong> "
        "Many federal credit unions offer PALs under National Credit Union "
        "Administration rules: PAL I loans run $200 to $1,000 over 1 to 6 "
        "months (you must have been a member for at least a month), PAL II "
        "loans go up to $2,000 over 1 to 12 months with no waiting period. "
        "Both cap APR at <strong>28%</strong>, cap the application fee at "
        "<strong>$20</strong>, and forbid rollovers &mdash; ask any federal "
        "credit union if it offers them. <strong>(2) Ask your employer for "
        "an advance or early pay.</strong> Many employers will advance a "
        "paycheck or let you draw earned wages early for no fee or a small "
        "one &mdash; far cheaper than a payday loan. <strong>(3) Negotiate "
        "the original bill.</strong> The utility, landlord, or medical "
        "office you actually owe will often take a payment plan for far "
        "less than a payday loan costs &mdash; ask before you borrow. "
        "<strong>(4) Local emergency assistance.</strong> Community action "
        "agencies, churches, and local charities often have one-time "
        "emergency help for rent, utilities, or car repairs &mdash; dial "
        "211 or search your county&rsquo;s community action agency. "
        "<strong>(5)</strong> Be wary of &ldquo;debt settlement&rdquo; "
        "pitches that charge fees to negotiate your debts down; nonprofit "
        "credit counselors (look for NFCC members) review your budget for "
        "free or nearly free.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Before you borrow, "
        "price the PAL and the original creditor&rsquo;s payment plan "
        "first &mdash; both are almost always cheaper than a payday or "
        "title loan.</p>"
    )
    parts.append("</div>")
    # --- Scams and traps ---
    parts.append('<div class="card">')
    parts.append("<h3>Scams and traps</h3>")
    parts.append(
        "<p><strong>Rollovers.</strong> Each rollover charges a new fee "
        "without reducing what you owe &mdash; that is the trap that turns "
        "a two-week loan into months of fees. <strong>Illegal online "
        "lenders.</strong> A website offering payday loans to "
        + esc(state) + " residents must hold a " + esc(state) + " license "
        "to lend here legally; check the lender on the regulator&rsquo;s "
        "license lookup (the official source below) using the company&rsquo;s "
        "exact legal name, not its website name. A loan from an unlicensed "
        "lender may be void &mdash; and the lender may still try to collect "
        "it. <strong>Tribal-lending claims.</strong> Some online lenders "
        "say tribal law exempts them from your state&rsquo;s law. State "
        "regulators and courts have repeatedly treated loans made to state "
        "residents as subject to state law anyway &mdash; if a lender says "
        "state law does not apply to it, treat that as a red flag and "
        "complain to the regulator. <strong>Upfront fees and threats."
        "</strong> A real lender never asks you to pay a fee before you "
        "get the money, and no collector can have you arrested for an "
        "unpaid payday loan.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Before you borrow from "
        "any lender &mdash; storefront or online &mdash; check the license "
        "on the official source below. If the lender is not licensed in "
        + esc(state) + ", walk away and report it.</p>"
    )
    parts.append("</div>")
    # --- Help ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Help in {esc(state)}</h3>")
    parts.append(
        "<p>If a lender breaks the rules above: <strong>(1)</strong> "
        "complain in writing to the lender, keep a copy, and keep every "
        "notice the lender sends you. <strong>(2)</strong> Take the paper "
        "trail to the official source linked below &mdash; that is where "
        "you check whether a lender is licensed and file a complaint. "
        "<strong>(3)</strong> File a complaint with the CFPB as well; it "
        "takes complaints about payday and title lenders online. "
        "<strong>(4)</strong> Get free help from legal aid &mdash; see "
        "the Free Legal Help section on this page &mdash; especially if a "
        "lender is threatening your car or your bank account.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> One call solves most "
        "problems: the lender in writing first, then the official source "
        "below, then legal aid if the lender will not fix it.</p>"
    )
    parts.append("</div>")
    # --- Official links ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Official links in {esc(state)}</h3>")
    parts.append("<ul>")
    parts.append(
        f"<li><a href=\"{esc(s['link'])}\" target=\"_blank\" "
        f"rel=\"noopener\">{esc(s['link_label'])}</a></li>"
    )
    parts.append("</ul>")
    parts.append("</div>")
    # --- Do this now ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) If you are thinking "
        "about one of these loans, price the PAL and the original "
        "creditor&rsquo;s payment plan first &mdash; both are almost always "
        "cheaper. (2) If you already have a payday loan, do not roll it "
        "over or take a second one to pay the first; ask the lender, in "
        "writing, for the payment plan described above if " + esc(state)
        + " gives you one, and keep the reply. (3) If the lender keeps "
        "debiting your account, revoke the debit authorization: tell the "
        "lender in writing, tell your bank, and keep copies. (4) If a "
        "lender here is unlicensed or broke the caps above, complain to "
        "the official source on this page &mdash; in several states an "
        "illegal loan is void and uncollectible. (5) If your car is on the "
        "line, act before the due date, not after: repossession is faster "
        "and cheaper for the lender than it is for you to undo.</p>"
    )
    parts.append(
        "<p><em>Sources: the official " + esc(state) + " source linked "
        "above, checked November 14, 2026, and the payday and title loan "
        "cards in the Credit Card &amp; Debt section on this page, which "
        "were built from official state sources. Laws change &mdash; confirm "
        "the current rule in the official source before you rely on a "
        "deadline. This is general information, not legal advice.</em></p>"
    )
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def build_state_pages(data):
    for s in data:
        slug = s["slug"]
        path = STATES / f"{slug}.html"
        text = path.read_text()
        anchor = f"payday-title-loans-in-{slug}"
        assert anchor not in text, f"{slug}: anchor already present"
        # --- insert section before Manufactured-home parks (newest-first) ---
        h2 = text.find(f'<h2 id="manufactured-home-parks-in-{slug}">')
        assert h2 != -1, f"{slug}: manufactured-home-parks h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        new_section = section_html(s)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the manufactured-home-parks <li> ---
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#manufactured-home-parks-in-'
            + re.escape(slug)
            + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: manufactured-home-parks contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#payday-title-loans-in-{slug}">'
            f"Payday / Title Loans in {s['state']}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert "payday-title-loans" not in helper_part, "index already has helper option"
    assert 'data-topic="payday-title-loans"' not in text, "index already has card"
    opt_old = (
        '<option value="manufactured-home-parks" data-anchor="manufactured-home-parks">'
        "Manufactured-home parks (own the home, rent the lot)</option>"
    )
    assert opt_old in text, "manufactured-home-parks helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="payday-title-loans" data-anchor="payday-title-loans">'
        "Payday / title loans (cost, caps, payment plans)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="manufactured-home-parks"'
    idx = text.find(card_anchor)
    assert idx != -1, "manufactured-home-parks card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="payday-title-loans">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-payday-title-loans.jpg" alt="Payday / Title Loans" loading="lazy"></span>
          <h3>Payday / Title Loans</h3>
          <p>What a $15-per-$100 loan really costs, whether payday lending is banned or capped in your state, title loans and your car, payment plans, and the safer ways out.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 34 topics" in text, "show-all label not found"
    text = text.replace("Show all 34 topics", "Show all 35 topics", 1)
    assert '<span class="count-badge">34 topics</span>' in text
    text = text.replace(
        '<span class="count-badge">34 topics</span>',
        '<span class="count-badge">35 topics</span>',
        1,
    )
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 34->35")


def build_about():
    text = ABOUT.read_text()
    assert "79 legal topics" in text, "about count not found"
    ABOUT.write_text(text.replace("79 legal topics", "80 legal topics", 1))
    print("  about.html: 79 -> 80")


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 10447, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith("payday-title-loans-in-") for e in idx)
    for s in data:
        state = s["state"]
        slug = s["slug"]
        law_kw = " ".join(s["payday"].split()[:25])
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"payday-title-loans-in-{slug}",
                "h": f"Payday / Title Loans in {state}",
                "t": (
                    f"Payday / Title Loans in {state} "
                    f"\u2014 payday loan title loan APR 391 percent fee "
                    f"rollover banned capped 36 percent cap max loan term "
                    f"license payment plan extended payment plan PAL "
                    f"military lending act repossession car title tribal "
                    f"lender unlicensed scam {law_kw} {state}"
                ),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Payday / Title Loans",
            "t": (
                "What a $15-per-$100 loan really costs, whether payday "
                "lending is banned or capped in your state, title loans "
                "and your car, payment plans, and the safer ways out."
            ),
        }
    )
    assert len(idx) == 10498, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 10447 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [states[k] for k in sorted(states)]
    slugs = [s["slug"] for s in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert all(s.get("link") and s.get("link_label") for s in data), "missing link data"
    print("building state pages...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
