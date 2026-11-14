#!/usr/bin/env python3
"""Build Topic #79: Student loans — standalone section on all 50 state pages.

Inserts one new section per state page (before the Mental-health crisis
holds section, newest-first), a contents-list entry, a homepage helper
option + topic card (second grid, after Mental-health crisis holds),
bumps About 77 -> 78, and appends 50 state entries + 1 helper entry to
assets/search-index.json (10345 -> 10396).

Data: hidden_files/topic-research/student-loans/all-states.json
(coordinator-written; see make_dataset.py for the source trail).

Coordinator verification before the build (Nov 14, 2026):
- Federal repayment (RAP/IDR): studentaid.gov "Top FAQs About
  Income-Driven Repayment Plans" — RAP 1-10% of AGI, $50 less per
  dependent, $10 minimum, 30-year term / 360 payments; PAYE and ICR
  retire no later than July 1, 2028; loans first disbursed on/after
  July 1, 2026 get RAP or Tiered Standard only.
- Default: 270 days without a payment (Direct/FFEL); garnishment up
  to 15% of disposable pay without a court order; 30 days to request
  a garnishment hearing; 65 days to dispute a Treasury offset;
  rehabilitation = nine voluntary, reasonable, affordable payments
  within 10 consecutive months (as low as $5), once per loan today,
  twice from July 1, 2027; consolidation leaves the default on the
  credit history. Default Resolution Group 1-800-621-3115 and FSA
  Information Center 1-800-433-3243 re-confirmed in current sources.
- Collections pause: Department delayed involuntary collections Jan 16,
  2026; no restart announced as of Nov 14, 2026. October 2026 news
  reports of an imminent restart were denied by a Department
  spokesperson — the section says so and tells borrowers not to count
  on the pause lasting.
- PSLF: 120 qualifying monthly payments, Direct Loans only, full-time
  work for government or a 501(c)(3) nonprofit; payments need not be
  consecutive; RAP is PSLF-qualifying; SAVE wound down after a court
  ruling in March 2026. Teacher Loan Forgiveness: five consecutive
  years in a low-income school, up to $17,500 (math, science, special
  education) or $5,000 (other teachers); the same years cannot count
  toward PSLF.
- Fresh Start ended October 2, 2024 (application deadline Sept 30,
  2024). Defaulted Loans Support Center on StudentAid.gov launched
  September 30, 2026.
- State servicer laws / ombudsmen: reused verbatim from the buried
  "Student loans" block in Credit Card & Debt on each state page
  (Batch 6), which was built from official state sources. FL/GA "has
  no servicer licensing law" lines are carried over as published;
  states with no law paragraph get a claim-free sentence about this
  section, not a claim about the law.
- State Loan Repayment Program: HRSA/NHSC SLRP contacts page, read
  Nov 14, 2026 — a funded program office is named for 42 states; the
  other 8 (AL, FL, IA, NH, NJ, NC, SC, SD) are not on that list and
  the section says so instead of inventing a program.
- Links: all 50 state links re-swept Nov 14, 2026 (200/202, or 403
  from official .gov bot filters — kept per precedent; CT and TN
  curl-000s confirmed live by text fetch the same day). No other
  phone number is printed besides the two federal numbers above.
- The buried block in Credit Card & Debt stays where it is (as with
  the Guardianship cards under Topic #78); this section cross-references
  it for bankruptcy and debt settlement instead of duplicating it.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "student-loans" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"

TOPIC = "student-loans"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(s):
    state = s["state"]
    slug = s["slug"]
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="student-loans-in-{slug}">Student Loans in {esc(state)}</h2>'
    )
    parts.append(
        "<p>Student loans split into two worlds. <strong>Federal</strong> "
        "loans come with repayment plans based on your income, official "
        "ways out of default, and free help from the U.S. Department of "
        "Education. <strong>Private</strong> loans are just a contract "
        "with a lender \u2014 the federal options do not apply. The "
        "federal rules changed on <strong>July 1, 2026</strong> under "
        "the 2025 law, and this section follows what the Department of "
        "Education itself publishes now, checked "
        "<strong>November 14, 2026</strong>. This area is still moving, "
        "so confirm your own status in your StudentAid.gov account "
        "before you act. Bankruptcy and debt settlement are covered in "
        "the Credit Card &amp; Debt section on this page \u2014 this "
        "section is about the loans themselves: repayment, forgiveness, "
        "default, your state's servicer rules, and state programs. "
        "This is general information, not legal advice.</p>"
    )
    # --- Federal or private ---
    parts.append('<div class="card">')
    parts.append("<h3>Federal or private? How to tell</h3>")
    parts.append(
        "<p>Log in at StudentAid.gov: every federal loan you owe is "
        "listed there, with its type, balance, servicer, and repayment "
        "plan. A loan that is <em>not</em> listed is private \u2014 "
        "contact that lender directly about your options. Everything "
        "below about repayment plans, forgiveness, default, and getting "
        "out of default applies to <strong>federal</strong> loans only. "
        "For a private loan, your rights are the contract you signed, "
        "plus " + esc(state) + " law (see the " + esc(state) + " rules "
        "card below) \u2014 private lenders generally do not have to "
        "offer income-based payments, deferment, or forgiveness.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Before you call "
        "anyone or pay anyone, log in at StudentAid.gov and write down "
        "each loan, whether it is federal or private, who services it, "
        "and whether any loan is in default \u2014 a red warning box "
        "shows on the dashboard for defaulted loans.</p>"
    )
    parts.append("</div>")
    # --- Repayment ---
    parts.append('<div class="card">')
    parts.append("<h3>Can't afford the payment? Income-driven plans</h3>")
    parts.append(
        "<p>Ask about an income-driven plan <em>before</em> you miss "
        "payments. The Department's current plans are "
        "<strong>Income-Based Repayment (IBR)</strong> and the new "
        "<strong>Repayment Assistance Plan (RAP)</strong>, which "
        "started July 1, 2026. The older PAYE and ICR plans are being "
        "phased out under the 2025 law; borrowers in them with loans "
        "from before July 1, 2026 have until <strong>July 1, "
        "2028</strong> to choose RAP, the new Tiered Standard plan, or "
        "IBR. Under RAP, payments run between <strong>1% and 10% of "
        "your adjusted gross income</strong> depending on what you "
        "earn, reduced by $50 a month for each dependent; on-time "
        "payments get leftover monthly interest waived plus a matching "
        "principal payment of up to $50, and a remaining balance can "
        "be discharged after 360 qualifying payments (30 years). "
        "Loans first taken out on or after July 1, 2026 use RAP or "
        "the Tiered Standard plan (fixed terms of 10, 15, 20, or 25 "
        "years depending on the amount borrowed) \u2014 and if you "
        "never choose, the servicer will place a new loan on Tiered "
        "Standard. Applying takes about 10 minutes in your "
        "StudentAid.gov account. The SAVE plan is gone \u2014 wound "
        "down after a court ruling in March 2026; if you were in "
        "SAVE, check your account for your loans' current status. "
        "One thing to check before you count on forgiveness at the "
        "end of an income-driven plan: under the 2025 law, a balance "
        "forgiven that way counts as taxable income for discharges "
        "after 2025 \u2014 PSLF and Teacher Loan Forgiveness stay "
        "tax-free.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Behind but not yet "
        "in default? Apply for IBR or RAP now \u2014 getting onto a "
        "plan beats every cure for default.</p>"
    )
    parts.append("</div>")
    # --- PSLF + Teacher ---
    parts.append('<div class="card">')
    parts.append(
        "<h3>Public Service Loan Forgiveness \u2014 and Teacher Loan Forgiveness</h3>"
    )
    parts.append(
        "<p><strong>Public Service Loan Forgiveness (PSLF)</strong> "
        "cancels the remaining balance on your Direct Loans after "
        "<strong>120 qualifying monthly payments</strong> made under a "
        "qualifying repayment plan while you work full-time for a "
        "government or not-for-profit employer. The 120 payments do "
        "not need to be consecutive, and RAP counts as a qualifying "
        "plan. FFEL and Perkins loans count only if consolidated into "
        "a Direct Consolidation Loan first, and private loans never "
        "qualify. Use the <strong>PSLF Help Tool</strong> on "
        "StudentAid.gov to check your employer and submit the form "
        "\u2014 do not rely on your servicer's say-so alone \u2014 and "
        "certify your employment every year and whenever you change "
        "jobs, so errors get caught while they are still fixable.</p>"
    )
    parts.append(
        "<p><strong>Teacher Loan Forgiveness</strong> is the faster, "
        "smaller route for teachers: teach full-time for "
        "<strong>five complete and consecutive academic years</strong> "
        "in a low-income school or educational service agency, and up "
        "to <strong>$17,500</strong> can be forgiven if you teach "
        "math, science, or special education (up to $5,000 for other "
        "teachers). You cannot count the same years toward both "
        "Teacher Loan Forgiveness and PSLF \u2014 pick the one that "
        "pays more for your situation.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you work for "
        "government or a nonprofit, open the PSLF Help Tool today and "
        "check whether your employer qualifies and how many payments "
        "you already have. If you teach, check whether your school is "
        "on the federal low-income schools list.</p>"
    )
    parts.append("</div>")
    # --- Default ---
    parts.append('<div class="card">')
    parts.append("<h3>What default means \u2014 and why to avoid it</h3>")
    parts.append(
        "<p>A federal Direct or FFEL loan goes into default after "
        "<strong>270 days</strong> without a scheduled payment. The "
        "consequences the Department lists: the entire unpaid balance "
        "becomes due at once; tax refunds and federal benefit payments "
        "can be taken through <strong>Treasury offset</strong>; wages "
        "can be garnished; you lose deferment, forbearance, and your "
        "choice of repayment plan; you lose eligibility for more "
        "federal student aid; and the default is reported to the "
        "credit bureaus. Even before default, a delinquency of 90 "
        "days or more is reported. One warning: \u201cFresh Start,"
        "\u201d the temporary program you may have heard about, "
        "<strong>ended on October 2, 2024</strong> \u2014 anyone "
        "offering to enroll you in it now is offering a program that "
        "no longer exists.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you are behind, "
        "act before day 270: an income-driven plan, a deferment, or a "
        "forbearance arranged now is far easier than getting out of "
        "default later.</p>"
    )
    parts.append("</div>")
    # --- Two ways out ---
    parts.append('<div class="card">')
    parts.append("<h3>In default? The two ways out</h3>")
    parts.append(
        "<p>The Department names two main exits (paying in full is a "
        "third, impractical for most people). <strong>(1) "
        "Rehabilitation \u2014 usually the better deal.</strong> You "
        "agree in writing to make <strong>nine voluntary, reasonable, "
        "and affordable payments</strong> \u2014 they can be as low as "
        "$5 \u2014 during a period of 10 consecutive months. Finish, "
        "and the default status is removed, garnishment and offset "
        "stop, and the record of default is removed from your credit "
        "history (late payments from before the default stay). "
        "Rehabilitation is a one-time opportunity per loan today; "
        "starting July 1, 2027, you will be able to rehabilitate the "
        "same loan twice. <strong>(2) Consolidation \u2014 the faster "
        "exit.</strong> Roll the defaulted loan into a new Direct "
        "Consolidation Loan after three consecutive, voluntary, "
        "on-time, full payments, or by applying with an income-driven "
        "plan. The catches: unpaid interest is added to your "
        "principal, and the record of default stays on your credit "
        "history. Compare both at StudentAid.gov/default-support \u2014 "
        "the Defaulted Loans Support Center, open since September 30, "
        "2026 \u2014 or call the Default Resolution Group at "
        "<strong>1-800-621-3115</strong>.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Already in "
        "default? Start at StudentAid.gov/default-support or call "
        "the Default Resolution Group (1-800-621-3115), and choose "
        "rehabilitation unless you need consolidation's faster exit.</p>"
    )
    parts.append("</div>")
    # --- Garnishment ---
    parts.append('<div class="card">')
    parts.append(
        "<h3>Wage garnishment: no court order needed \u2014 and a current pause</h3>"
    )
    parts.append(
        "<p>On a defaulted federal loan, the Department can order your "
        "employer to withhold up to <strong>15% of your disposable "
        "pay</strong> \u2014 this is called administrative wage "
        "garnishment, and it does not require taking you to court. "
        "You have rights first: request a hearing in writing, "
        "postmarked within <strong>30 days</strong> of the garnishment "
        "notice, and the garnishment pauses until after the hearing; "
        "Treasury offset likewise comes with a written notice and a "
        "<strong>65-day</strong> window to dispute it. "
        "<strong>Current status:</strong> in January 2026 the "
        "Department announced it was <strong>delaying involuntary "
        "collections</strong> \u2014 wage garnishment and Treasury "
        "offset \u2014 while the new repayment plans roll out, and no "
        "restart date has been announced as of November 14, 2026. "
        "News reports in October 2026 said a restart could come soon; "
        "a Department spokesperson denied those reports. Defaults are "
        "still reported to the credit bureaus during the delay. Check "
        "StudentAid.gov for the current status, and do not count on "
        "the pause lasting.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If a garnishment "
        "or offset notice arrives, do not ignore it: the 30-day and "
        "65-day windows run from the notice, and asking for a hearing "
        "in writing is what pauses the garnishment.</p>"
    )
    parts.append("</div>")
    # --- Private loans ---
    parts.append('<div class="card">')
    parts.append("<h3>Private loans: fewer protections</h3>")
    parts.append(
        "<p>A private student loan is a contract with a bank, credit "
        "union, or other lender. There is no income-driven plan, no "
        "PSLF, no federal rehabilitation, and no 270-day rule: your "
        "contract sets when the loan defaults, and it is usually much "
        "sooner than a federal loan. The lender can sue you for the "
        "balance, and a court judgment can lead to garnishment under "
        "state law \u2014 unlike a federal loan, the lender cannot "
        "garnish your wages without going to court first. Student "
        "loans are also very hard to wipe out in bankruptcy: most "
        "survive unless you prove undue hardship, a high bar \u2014 "
        "see the bankruptcy card in the Credit Card &amp; Debt "
        "section on this page.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you cannot pay "
        "a private loan, ask the lender <em>in writing</em> what "
        "hardship options exist \u2014 a temporary lower payment, "
        "interest-only payments, or a modified term \u2014 and keep a "
        "copy of everything. If the lender breaks " + esc(state) +
        " rules, use the " + esc(state) + " office linked below.</p>"
    )
    parts.append("</div>")
    # --- State rules ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Your state's rules in {esc(state)}</h3>")
    if s.get("state_law"):
        for p in s["state_law"]:
            parts.append(f"<p>{esc(p)}</p>")
    else:
        parts.append(
            f"<p>No statewide student-loan servicer licensing law is "
            f"printed for {esc(state)} in this section \u2014 federal "
            f"servicing rules still apply to your federal loans, and "
            f"the official {esc(state)} page linked below is where to "
            f"start if a servicer breaks its promises.</p>"
        )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If your servicer "
        "misapplies a payment, gives you wrong information about "
        "repayment options, or will not fix an error, complain to the "
        "servicer in writing first and keep a copy \u2014 then take "
        "that letter to the " + esc(state) + " office linked below.</p>"
    )
    parts.append("</div>")
    # --- State programs ---
    parts.append('<div class="card">')
    parts.append("<h3>State loan repayment and forgiveness programs</h3>")
    if s.get("slrp_office"):
        parts.append(
            "<p>For health professionals: the federal "
            "Health Resources and Services Administration (HRSA) "
            "State Loan Repayment Program funds state-run programs "
            "that repay loans for doctors, nurses, dentists, and other "
            "clinicians who work in shortage areas. In the 2026 "
            "funding cycle the program in " + esc(state) + " is run "
            "by the <strong>" + esc(s["slrp_office"]) + "</strong> "
            "\u2014 the HRSA contact list linked below has the "
            "details. Eligibility, the length of service required, "
            "and the amount repaid vary by state.</p>"
        )
    else:
        parts.append(
            "<p>For health professionals: the federal "
            "Health Resources and Services Administration (HRSA) "
            "State Loan Repayment Program funds state-run programs "
            "that repay loans for doctors, nurses, dentists, and other "
            "clinicians who work in shortage areas \u2014 but "
            "HRSA's current contact list names no funded program "
            "office for " + esc(state) + ". Check with your state's "
            "health department or higher-education agency before "
            "assuming there is no program: funding cycles change.</p>"
        )
    parts.append(
        "<p>Teachers have the federal Teacher Loan Forgiveness program "
        "in the card above. Beyond that, states run their own "
        "repayment programs for particular jobs \u2014 teachers, "
        "nurses, public defenders, rural doctors \u2014 and they open, "
        "close, and change amounts often. No other state program is "
        "named here because none was verified against an official "
        "source for " + esc(state) + " in this build: check the "
        "official " + esc(state) + " page linked below and your "
        "state's higher-education agency before you apply, and never "
        "pay anyone to apply for you.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you work in "
        "health care, teaching, or another public-service job, ask "
        "your employer and your state's higher-education agency "
        "which repayment programs you qualify for \u2014 and apply "
        "through the official program, not through a company that "
        "found you online.</p>"
    )
    parts.append("</div>")
    # --- Scams ---
    parts.append('<div class="card">')
    parts.append("<h3>Scams: never pay for free federal help</h3>")
    parts.append(
        "<p>Help with your federal loans is <strong>free</strong>. A "
        "company charging \u201cenrollment,\u201d "
        "\u201csubscription,\u201d or \u201cmaintenance\u201d fees to "
        "get you out of default, into a repayment plan, or onto "
        "forgiveness is running a scam \u2014 walk away. Red flags: "
        "they ask for your FSA ID or password (your servicer and the "
        "Department will never ask for it by phone or email), they "
        "promise instant forgiveness or a specific payment before "
        "seeing your loans, they tell you to stop paying your servicer "
        "and pay them instead, or they pressure you to act today. "
        "The same companies often call themselves \u201cstudent loan "
        "rescue\u201d or \u201cdebt relief\u201d services \u2014 "
        "everything they offer is something you can do yourself, "
        "free, at StudentAid.gov.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If a company took "
        "your money or your FSA ID, change your StudentAid.gov "
        "password at once, report it through the FSA Feedback Center "
        "on StudentAid.gov, report it to the FTC at "
        '<a class="r-link" href="https://reportfraud.ftc.gov" '
        'target="_blank" rel="noopener">ReportFraud.ftc.gov</a>, and '
        "tell your state attorney general \u2014 start with the "
        "official " + esc(state) + " page linked below.</p>"
    )
    parts.append("</div>")
    # --- Help ---
    parts.append('<div class="card">')
    parts.append("<h3>Help</h3>")
    parts.append(
        "<p>Your servicer is the company that bills you. Find yours "
        "by logging in at StudentAid.gov, or call the Federal Student "
        "Aid Information Center at <strong>1-800-433-3243</strong>. "
        "If the servicer will not fix a problem, submit it through "
        "the <strong>FSA Feedback Center</strong> on StudentAid.gov "
        "\u2014 and if the answer looks wrong or incomplete, you can "
        "add information to your case and ask for escalation to the "
        "Office of the Ombudsman.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> One call solves "
        "most problems: your servicer first, then the FSA Feedback "
        "Center if the servicer will not fix it, then the "
        + esc(state) + " office linked below.</p>"
    )
    parts.append("</div>")
    # --- Official links ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Official links in {esc(state)}</h3>")
    parts.append("<ul>")
    parts.append(
        "<li><a href=\"https://studentaid.gov/articles/faqs-idr-plan/\" "
        "target=\"_blank\" rel=\"noopener\">Federal Student Aid "
        "\u2014 Top FAQs About Income-Driven Repayment Plans "
        "(studentaid.gov)</a></li>"
    )
    parts.append(
        "<li><a href=\"https://nhsc.hrsa.gov/loan-repayment/state-loan-repayment-program/contacts\" "
        "target=\"_blank\" rel=\"noopener\">HRSA \u2014 State Loan "
        "Repayment Program contacts (find your state's program "
        "office)</a></li>"
    )
    parts.append(
        f"<li><a href=\"{esc(s['link'])}\" target=\"_blank\" "
        f"rel=\"noopener\">{esc(s['link_label'])}</a></li>"
    )
    parts.append("</ul>")
    parts.append("</div>")
    # --- Do this now ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Log in at "
        "StudentAid.gov and confirm what you owe, who services it, "
        "and whether any loan is in default. (2) Behind but not yet in "
        "default? Ask about IBR or RAP now. (3) Already in default? "
        "Start at StudentAid.gov/default-support or call the Default "
        "Resolution Group (1-800-621-3115), and choose rehabilitation "
        "unless you need consolidation's faster exit. (4) Work for "
        "government or a nonprofit? Open the PSLF Help Tool and certify "
        "your employment. (5) Never pay a company to do any of this "
        "\u2014 every step above is free. (6) If your loan is private, "
        "read your contract, ask the lender in writing what hardship "
        "options exist, and use the " + esc(state) + " office linked "
        "above if the lender breaks state rules.</p>"
    )
    parts.append(
        "<p><em>Sources: Federal Student Aid (studentaid.gov) income-"
        "driven repayment FAQs and default, rehabilitation, and "
        "forgiveness guidance, checked November 14, 2026; the U.S. "
        "Department of Education's January 16, 2026 announcement "
        "delaying involuntary collections; HRSA / National Health "
        "Service Corps State Loan Repayment Program contacts; and "
        "the official " + esc(state) + " source linked above. "
        "Federal figures change \u2014 confirm the current rules "
        "in your StudentAid.gov account before you rely on them. This "
        "is general information, not legal advice.</em></p>"
    )
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def build_state_pages(data):
    for s in data:
        slug = s["slug"]
        path = STATES / f"{slug}.html"
        text = path.read_text()
        anchor = f"student-loans-in-{slug}"
        assert anchor not in text, f"{slug}: anchor already present"
        # --- insert section before Mental-health crisis holds (newest-first) ---
        h2 = text.find(f'<h2 id="mental-health-crisis-holds-in-{slug}">')
        assert h2 != -1, f"{slug}: mental-health-crisis-holds h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        new_section = section_html(s)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the mental-health <li> ---
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#mental-health-crisis-holds-in-'
            + re.escape(slug)
            + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: mental-health contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#student-loans-in-{slug}">'
            f"Student Loans in {s['state']}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert "student-loans" not in helper_part, "index already has helper option"
    assert 'data-topic="student-loans"' not in text, "index already has card"
    opt_old = (
        '<option value="mental-health-crisis-holds" data-anchor="mental-health-crisis-holds">'
        "Mental-health crisis hold (someone in crisis)</option>"
    )
    assert opt_old in text, "mental-health helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="student-loans" data-anchor="student-loans">'
        "Student loans (repayment, default, forgiveness)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="mental-health-crisis-holds"'
    idx = text.find(card_anchor)
    assert idx != -1, "mental-health card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="student-loans">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-student-loans.jpg" alt="Student Loans" loading="lazy"></span>
          <h3>Student Loans</h3>
          <p>Federal or private, income-driven repayment, PSLF and teacher forgiveness, what default really does, the two ways out, your state's servicer rules, and state repayment programs.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 32 topics" in text, "show-all label not found"
    text = text.replace("Show all 32 topics", "Show all 33 topics", 1)
    assert '<span class="count-badge">32 topics</span>' in text
    text = text.replace(
        '<span class="count-badge">32 topics</span>',
        '<span class="count-badge">33 topics</span>',
        1,
    )
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 32->33")


def build_about():
    text = ABOUT.read_text()
    assert "77 legal topics" in text, "about count not found"
    ABOUT.write_text(text.replace("77 legal topics", "78 legal topics", 1))
    print("  about.html: 77 -> 78")


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 10345, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith("student-loans-in-") for e in idx)
    for s in data:
        state = s["state"]
        slug = s["slug"]
        law_kw = " ".join(s["state_law"])[:200] if s.get("state_law") else ""
        slrp_kw = "State Loan Repayment Program SLRP " + s["slrp_office"] if s.get("slrp_office") else "State Loan Repayment Program SLRP"
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"student-loans-in-{slug}",
                "h": f"Student Loans in {state}",
                "t": (
                    f"Student Loans in {state} "
                    f"\u2014 student loans federal private loans "
                    f"studentaid.gov income-driven repayment RAP IBR "
                    f"Repayment Assistance Plan Public Service Loan "
                    f"Forgiveness PSLF 120 payments teacher loan "
                    f"forgiveness default 270 days rehabilitation "
                    f"consolidation wage garnishment Treasury offset "
                    f"servicer {slrp_kw} student loan scams debt relief "
                    f"{law_kw} {state}"
                ),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Student Loans",
            "t": (
                "Federal or private, income-driven repayment, PSLF and "
                "teacher forgiveness, what default really does, the two "
                "ways out, your state's servicer rules, and state "
                "repayment programs."
            ),
        }
    )
    assert len(idx) == 10396, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 10345 -> {len(idx)} (+51)")


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
