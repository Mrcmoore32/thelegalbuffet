#!/usr/bin/env python3
"""Build Topic #84: Misclassification — standalone section on all 50
state pages.

Inserts one new section per state page (before Eviction Records,
newest-first), a contents-list entry, a homepage helper option + topic
card (second grid, after Eviction Records), bumps About 82 -> 83, and
appends 50 state entries + 1 helper entry to assets/search-index.json
(10600 -> 10651).

Data: hidden_files/topic-research/misclassification/all-states.json
(coordinator-written from hidden_files/topic-research/misclassification/
buried-extract.json, which reuses verbatim the per-state "How {State}
decides it" cards and the official-source links from the buried
misclassification cluster inside Workplace Rights on each state page —
those were built from official state sources. The buried block stays
where it is; this section is the full topic and cross-references
Workplace Rights instead of duplicating it.)

Coordinator verification before the build (Nov 14, 2026):
- Per-state test text reused verbatim from the buried cards (49 states).
  The "In short" line under each card is a plain-language summary of
  that same card, not a new claim. Where the buried card does not state
  the test (North Carolina, Washington), the card says so; where no
  official Wyoming source was found at all (searched Nov 14, 2026 —
  only non-official roundups, which disagreed with each other), the
  Wyoming card states no state test and no state link is printed.
- Headline federal facts spot-verified live Nov 14, 2026:
  * DOL Wage and Hour Division, "Misclassification of Employees as
    Independent Contractors Under the FLSA" (dol.gov): misclassified
    workers may miss minimum wage and overtime under the FLSA; the
    Jan 10, 2024 final rule (eff. Mar 11, 2024) is at 29 CFR Part 795.
  * DOL Fact Sheet 13 (revised March 2024): the FLSA economic-reality
    test uses six factors — opportunity for profit or loss depending
    on managerial skill; investments by worker and employer;
    permanence of the work relationship; nature and degree of control;
    whether the work is integral to the employer's business; skill
    and initiative. No single factor decides; the label, a 1099, and
    a signed contractor agreement do not decide. The fact sheet notes
    the 2024 rule's legality is in litigation and points to Field
    Assistance Bulletin 2025-1 for WHD's current enforcement position.
  * IRS, "Independent contractor (self-employed) or employee?"
    (irs.gov): common-law rules in three categories — behavioral
    control, financial control, type of relationship; Form SS-8 may
    be filed by the business or the worker and "may take at least
    six months"; an employer with no reasonable basis for treating
    an employee as a contractor may be liable for employment taxes
    (IRC section 3509); Form 8919 lets a misclassified worker
    report wages and pay only the employee share of Social Security
    and Medicare tax. IRS "Completing Form SS-8" page confirms the
    at-least-6-months wait.
  * WHD phone 1-866-487-9243: printed in the footer of the DOL
    misclassification page fetched live Nov 14, 2026, and already
    printed site-wide in the buried cluster. It is the only phone
    number in this topic.
- "Fourteen states use the ABC test" is counted from this dataset's
  own per-state cards (AK, CA, CT, HI, IL, LA, MD, MA, NE, NV, NH,
  NJ, NM, VT). The differ-by-program examples (OR, ME, VT, WV) are
  all stated in those states' buried cards.
- No new state link is introduced: every state link is the buried
  cluster's official link, reused verbatim. The one new federal link
  (IRS "Completing Form SS-8") was returned by search and is an
  irs.gov page. No phone numbers beyond the WHD number above.
- Retaliation wording matches the site's existing Workplace Rights
  retaliation card (firing/demoting/cutting hours for filing a wage
  claim is illegal; tell the agency right away).
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "misclassification" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"

DOL_URL = "https://www.dol.gov/agencies/whd/flsa/misclassification"
DOL_LABEL = (
    "Misclassification of Employees as Independent Contractors "
    "Under the Fair Labor Standards Act | U.S. Department of Labor"
)
IRS_URL = (
    "https://www.irs.gov/businesses/small-businesses-self-employed/"
    "independent-contractor-self-employed-or-employee"
)
IRS_LABEL = "Independent contractor (self-employed) or employee? | IRS"
SS8_URL = (
    "https://www.irs.gov/businesses/small-businesses-self-employed/"
    "completing-form-ss-8"
)
SS8_LABEL = "Completing Form SS-8 | IRS"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(s):
    state = s["state"]
    slug = s["slug"]
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(f'<h2 id="misclassification-in-{slug}">Misclassification in {esc(state)}</h2>')
    parts.append(
        "<p>You were hired as a &ldquo;contractor&rdquo; and paid on a 1099, "
        "but the boss sets your hours, hands you the tools, and tells you "
        "exactly how to do the job. That is <strong>misclassification</strong> "
        "&mdash; being called an independent contractor while being treated "
        "like an employee &mdash; and the label does not decide. What "
        "decides is how the work actually works, and the tests, the costs, "
        "and the ways to challenge it are in this section. A shorter version "
        "of this lived inside Workplace Rights on this page; this is the "
        "complete section. Checked <strong>November 14, 2026</strong>. This "
        "is general information, not legal advice.</p>"
    )
    # --- What it is and what it costs you ---
    parts.append('<div class="card">')
    parts.append("<h3>What misclassification is and what it costs you</h3>")
    parts.append(
        "<p>Whether you are an employee or an independent contractor turns "
        "on the real working relationship &mdash; who controls how, when, "
        "and where the work is done, how central the work is to the "
        "business, how you are paid, and how permanent the arrangement is. "
        "A 1099 form, a job title, or a signed &ldquo;independent "
        "contractor agreement&rdquo; does not settle it, and neither does "
        "the fact that you agreed to it.</p>"
    )
    parts.append(
        "<p>Classified as a contractor, you usually get no unemployment "
        "benefits when the work ends, no workers&rsquo; compensation if "
        "you are hurt on the job, no minimum-wage or overtime protection, "
        "and no employer share of payroll taxes &mdash; you owe "
        "self-employment tax on both halves of Social Security and "
        "Medicare. If the label is wrong, those protections were yours "
        "all along.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Start with the job as "
        "it really works, not the paperwork: who sets your schedule, who "
        "provides the tools, whether you can work for anyone else, and how "
        "you are paid. Write it down now, while it is fresh &mdash; that "
        "list is the evidence every route below asks for.</p>"
    )
    parts.append("</div>")
    # --- The tests ---
    parts.append('<div class="card">')
    parts.append("<h3>The tests: which one applies depends on the law</h3>")
    parts.append(
        "<p>There is no single national test. Three frameworks cover most "
        "cases, and the one that matters depends on which law you are "
        "claiming under &mdash; wage law, tax law, unemployment, or "
        "workers&rsquo; compensation &mdash; and the same state can use "
        "different tests for different programs.</p>"
    )
    parts.append(
        "<p><strong>1. The FLSA economic-reality test (federal wage law).</strong> "
        "Under the Fair Labor Standards Act, the question is whether you "
        "are economically dependent on the employer or in business for "
        "yourself. The Labor Department&rsquo;s Fact Sheet 13 lists six "
        "factors: (1) opportunity for profit or loss depending on "
        "managerial skill; (2) investments by the worker and the employer; "
        "(3) permanence of the work relationship; (4) nature and degree of "
        "control; (5) whether the work is integral to the employer&rsquo;s "
        "business; and (6) skill and initiative. No single factor decides, "
        "and the totality of the relationship is what counts. The rule is "
        "at 29 CFR Part 795 (effective March 11, 2024). Note: the Labor "
        "Department says the 2024 rule&rsquo;s legality is the subject of "
        "current litigation and points to its Field Assistance Bulletin "
        "2025-1 for its current enforcement position &mdash; the six "
        "factors above are the test as the fact sheet states it.</p>"
    )
    parts.append(
        "<p><strong>2. The IRS common-law test (federal tax law).</strong> "
        "The IRS weighs all the facts about control and independence in "
        "three categories: behavioral control (does the company control "
        "what you do and how you do it), financial control (who controls "
        "the business side &mdash; how you are paid, whether expenses are "
        "reimbursed, who provides tools and supplies), and the type of "
        "relationship (written contracts, employee-type benefits, whether "
        "the work continues and is a key aspect of the business). There is "
        "no set number of factors that makes someone an employee.</p>"
    )
    parts.append(
        "<p><strong>3. The ABC test (many states).</strong> Under the ABC "
        "test, you are an employee unless the employer proves all three: "
        "(A) you are free from the employer&rsquo;s control and direction, "
        "(B) the work is outside the employer&rsquo;s usual course of "
        "business (or outside all its places of business), and (C) you are "
        "customarily engaged in an independently established trade, "
        "occupation, or business of the same nature. Fail any one part and "
        "you are an employee. Fourteen states use the ABC test for at "
        "least one program, and a few more use ABC-style two- or "
        "three-part tests &mdash; the " + esc(state) + " card below says "
        "which one applies here.</p>"
    )
    parts.append(
        "<p><strong>One state, different tests.</strong> Oregon applies the "
        "economic-reality test to wage-and-hour claims and a four-factor "
        "right-to-control test to civil rights disputes. Maine uses one "
        "common standard across workers&rsquo; compensation, unemployment "
        "insurance, and wage and hour. Vermont uses the ABC test for "
        "unemployment compensation and Health Care Fund contributions, "
        "while withholding uses the same definitions as the IRS. West "
        "Virginia uses one statutory test across unemployment, workers&rsquo; "
        "compensation, human rights, and wage payment laws. Always check "
        "which test your claim falls under &mdash; winning under one does "
        "not automatically mean winning under another.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Figure out what you "
        "lost before you pick a test: unpaid overtime points to the FLSA "
        "test, a tax bill points to the IRS test, and denied unemployment "
        "or workers&rsquo; comp points to your state&rsquo;s test in the "
        "card below.</p>"
    )
    parts.append("</div>")
    # --- State test card (verbatim buried card) ---
    parts.append('<div class="card">')
    parts.append(f"<h3>How {esc(state)} decides it</h3>")
    if s.get("state_card"):
        parts.append(f"<p>{esc(s['state_card'])}</p>")
        parts.append(
            "<p><strong>In short:</strong> " + esc(state) + " uses the "
            + esc(s["test_short"]) + " for " + esc(s["test_area"])
            + ", as the official source linked below describes it.</p>"
        )
    else:
        parts.append(
            "<p>No official Wyoming source stating which test Wyoming uses "
            "was found, so this page states no Wyoming test. The federal "
            "tests and filing routes above still apply in Wyoming.</p>"
        )
    if s.get("link"):
        parts.append(
            "<p><strong>Okay, so what do I do?</strong> Open the official "
            + esc(state) + " source linked below and read the test in its own "
            "words before you file anything &mdash; the wording is what the "
            "agency will hold you to.</p>"
        )
    else:
        parts.append(
            "<p><strong>Okay, so what do I do?</strong> Use the federal "
            "tests and filing routes above as your starting point &mdash; "
            "there is no state source linked on this page because none "
            "was verified.</p>"
        )
    parts.append("</div>")
    # --- What you can recover / what it costs the employer ---
    parts.append('<div class="card">')
    parts.append("<h3>What you can get back &mdash; and what it costs the employer</h3>")
    parts.append(
        "<p>If you were really an employee, the rights you lost were yours "
        "all along. What you can recover depends on the route: back pay "
        "for minimum wage and overtime you should have been paid under the "
        "FLSA; the employer&rsquo;s share of Social Security and Medicare "
        "taxes it should have paid; unemployment benefits and workers&rsquo; "
        "compensation coverage for the period you were misclassified; and "
        "in some cases, benefits you were denied, such as paid leave or "
        "health coverage the employer offered its employees.</p>"
    )
    parts.append(
        "<p>For the employer, the bill runs the other way: back wages and "
        "overtime, back payroll taxes, and unemployment and workers&rsquo; "
        "compensation premiums it should have paid. The IRS says an "
        "employer that treats an employee as an independent contractor "
        "with no reasonable basis for doing so may be held liable for "
        "employment taxes for that worker. State agencies can also assess "
        "back taxes plus penalties and interest.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Add up what the label "
        "cost you before you file: unpaid overtime hours, the extra tax "
        "you paid, and any medical bill or lost week of pay from an injury "
        "or layoff. That total is what your claim is actually worth, and "
        "it tells you which agency to start with.</p>"
    )
    parts.append("</div>")
    # --- How to challenge it ---
    parts.append('<div class="card">')
    parts.append("<h3>How to challenge it, step by step</h3>")
    parts.append(
        "<p><strong>(1) Gather the evidence.</strong> Who sets your "
        "schedule and hours? Who provides the tools, materials, and "
        "workplace? How are you paid &mdash; by the hour, by the job, or "
        "by salary? Can you work for anyone else, set your own rates, or "
        "hire help? How long has the arrangement lasted, and is the work "
        "central to the business? Keep pay stubs, schedules, messages, "
        "and the contractor agreement in one folder, somewhere your "
        "employer cannot delete them.</p>"
    )
    parts.append(
        "<p><strong>(2) File a wage claim if you lost pay.</strong> If the "
        "label cost you minimum wage or overtime, file a wage claim with "
        "the U.S. Department of Labor&rsquo;s Wage and Hour Division "
        "(free help at 1-866-487-9243) or with your state labor agency "
        "&mdash; the " + esc(state) + " source linked below is the place "
        "to start. State unemployment agencies also audit classification "
        "because it decides who pays unemployment tax &mdash; a report "
        "there can trigger a review of your whole workplace.</p>"
    )
    parts.append(
        "<p><strong>(3) Ask the IRS to rule: Form SS-8.</strong> A worker "
        "or a firm can file Form SS-8 and ask the IRS to rule on the "
        "worker&rsquo;s status for federal tax purposes. It is free, "
        "though the IRS says it can take at least six months. File it "
        "before you file Form 8919, or at the same time.</p>"
    )
    parts.append(
        "<p><strong>(4) Fix the tax bill: Form 8919.</strong> If you were "
        "paid as a contractor but believe you were an employee, Form 8919 "
        "lets you report the wages and pay only the employee share of "
        "Social Security and Medicare tax instead of the full "
        "self-employment tax. Attach it to your tax return.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Pick the route that "
        "matches what you lost &mdash; wage claim for lost pay, SS-8 for "
        "a federal ruling, Form 8919 for the tax bill, your state "
        "unemployment agency if benefits were denied &mdash; and file "
        "before any deadline runs. You can use more than one route; they "
        "do not cancel each other out.</p>"
    )
    parts.append("</div>")
    # --- Retaliation ---
    parts.append('<div class="card">')
    parts.append("<h3>Punished for raising it?</h3>")
    parts.append(
        "<p>It is illegal for an employer to fire, demote, or cut the hours "
        "of a worker for filing a wage claim, reporting misclassification, "
        "or asking about unpaid wages. If that happens, tell the agency "
        "you filed with right away &mdash; retaliation is its own "
        "violation, with its own deadline, and it does not depend on "
        "whether your original claim succeeds.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Write down exactly what "
        "happened, when, and who was there, the same day it happens. Keep "
        "any message, schedule change, or write-up that shows the timing "
        "&mdash; retaliation cases often turn on how soon the punishment "
        "followed the complaint.</p>"
    )
    parts.append("</div>")
    # --- Official links ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Official links in {esc(state)}</h3>")
    parts.append("<ul>")
    parts.append(
        f"<li><a href=\"{esc(DOL_URL)}\" target=\"_blank\" "
        f"rel=\"noopener\">{esc(DOL_LABEL)}</a></li>"
    )
    parts.append(
        f"<li><a href=\"{esc(IRS_URL)}\" target=\"_blank\" "
        f"rel=\"noopener\">{esc(IRS_LABEL)}</a></li>"
    )
    parts.append(
        f"<li><a href=\"{esc(SS8_URL)}\" target=\"_blank\" "
        f"rel=\"noopener\">{esc(SS8_LABEL)}</a></li>"
    )
    if s.get("link"):
        parts.append(
            f"<li><a href=\"{esc(s['link'])}\" target=\"_blank\" "
            f"rel=\"noopener\">{esc(s['link_label'])}</a></li>"
        )
    parts.append("</ul>")
    parts.append("</div>")
    # --- Do this now ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Write down how the "
        "job actually works &mdash; who sets your schedule, who provides "
        "the tools, whether you can work for anyone else, and how you are "
        "paid. (2) Add up what the label cost you: unpaid overtime, extra "
        "tax, lost benefits. (3) Pick your route: a wage claim with the "
        "Labor Department or your state agency for lost pay, Form SS-8 for "
        "a federal ruling, Form 8919 for the tax bill. (4) If you are "
        "fired or punished for raising it, tell the agency right away "
        "&mdash; retaliation is its own violation.</p>"
    )
    parts.append(
        "<p><em>Sources: the official " + esc(state) + " source linked "
        "above (where one is listed), the U.S. Department of Labor pages "
        "linked above, and the IRS pages linked above, checked November "
        "14, 2026, and the misclassification cards in the Workplace "
        "Rights section on this page, which were built from official "
        "state sources. Federal law cited: the Fair Labor Standards Act, "
        "29 U.S.C. 201 et seq. (minimum wage and overtime; economic-"
        "reality test at 29 CFR Part 795); Internal Revenue Code section "
        "3509 (employer liability for employment taxes). Laws change "
        "&mdash; confirm the current rule in the official source before "
        "you rely on a deadline. This is general information, not legal "
        "advice.</em></p>"
    )
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def build_state_pages(data):
    for s in data:
        slug = s["slug"]
        path = STATES / f"{slug}.html"
        text = path.read_text()
        anchor = f"misclassification-in-{slug}"
        assert anchor not in text, f"{slug}: anchor already present"
        # --- insert section before Eviction Records (newest-first) ---
        h2 = text.find(f'<h2 id="eviction-records-in-{slug}">')
        assert h2 != -1, f"{slug}: eviction-records h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        new_section = section_html(s)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the eviction-records <li> ---
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#eviction-records-in-'
            + re.escape(slug)
            + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: eviction-records contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#misclassification-in-{slug}">'
            f"Misclassification in {s['state']}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert "misclassification" not in helper_part, "index already has helper option"
    assert 'data-topic="misclassification"' not in text, "index already has card"
    opt_old = (
        '<option value="eviction-records" data-anchor="eviction-records">'
        "Eviction records (sealing, screening reports, disputes)</option>"
    )
    assert opt_old in text, "eviction-records helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="misclassification" data-anchor="misclassification">'
        "Misclassification (1099 vs W-2, contractor vs employee)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="eviction-records"'
    idx = text.find(card_anchor)
    assert idx != -1, "eviction-records card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="misclassification">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-misclassification.jpg" alt="Misclassification" loading="lazy"></span>
          <h3>Misclassification</h3>
          <p>Called a contractor, treated like an employee? The label doesn&rsquo;t decide &mdash; the tests, what it costs you, and how to challenge it in your state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 37 topics" in text, "show-all label not found"
    text = text.replace("Show all 37 topics", "Show all 38 topics", 1)
    assert '<span class="count-badge">37 topics</span>' in text
    text = text.replace(
        '<span class="count-badge">37 topics</span>',
        '<span class="count-badge">38 topics</span>',
        1,
    )
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 37->38")


def build_about():
    text = ABOUT.read_text()
    assert "82 legal topics" in text, "about count not found"
    ABOUT.write_text(text.replace("82 legal topics", "83 legal topics", 1))
    print("  about.html: 82 -> 83")


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 10600, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith("misclassification-in-") for e in idx)
    for s in data:
        state = s["state"]
        slug = s["slug"]
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"misclassification-in-{slug}",
                "h": f"Misclassification in {state}",
                "t": (
                    f"Misclassification in {state} "
                    f"\u2014 misclassification 1099 vs W-2 independent "
                    f"contractor employee ABC test economic reality test "
                    f"IRS common law test Form SS-8 Form 8919 wage claim "
                    f"overtime minimum wage unemployment workers "
                    f"compensation retaliation self-employment tax "
                    f"{s['test_short']} {state}"
                ),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Misclassification",
            "t": (
                "Called a contractor, treated like an employee? The label "
                "doesn't decide \u2014 the tests, what it costs you, and "
                "how to challenge it in your state. Misclassification "
                "1099 vs W-2 independent contractor employee ABC test "
                "Form SS-8 Form 8919."
            ),
        }
    )
    assert len(idx) == 10651, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 10600 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [states[k] for k in sorted(states)]
    slugs = [s["slug"] for s in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert all(s.get("link") and s.get("link_label") for s in data if s["slug"] != "wyoming"), "missing link data"
    assert all(s.get("state_card") for s in data if s["slug"] != "wyoming"), "missing state card"
    assert all(s.get("test_short") and s.get("test_area") for s in data), "missing test labels"
    print("building state pages...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
