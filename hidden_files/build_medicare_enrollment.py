#!/usr/bin/env python3
"""Build Topic #77: Medicare enrollment — all 50 pages.

Inserts one new section per state page (before the Property Tax Appeal
section, newest-first), a contents-list entry, a homepage helper option
+ topic card (second grid, after Property Tax Appeal), bumps About
75 -> 76, and appends 50 state entries + 1 helper entry to
assets/search-index.json (10243 -> 10294).

Data: hidden_files/topic-research/medicare-enrollment/all-states.json
(coordinator-written from the SHIP name/phone/link already published on
the live site in each state's buried Public Benefits Appeals Medicare
block, plus Medigap notes for the six states with verified differences).

Coordinator verification before the build:
- Federal 2026 figures vs CMS MM14279 (CY 2026 update) and
  medicare.gov: Part B standard premium $202.90/mo, Part B deductible
  $283/yr, Part A inpatient deductible $1,736 per benefit period,
  Part A premium $0 with 40+ quarters and $565/mo base premium with
  fewer than 30 quarters. The 30-39-quarter Part A premium ($311) was
  only single-sourced, so it is NOT printed — the text says only that
  the premium is lower with 30-39 quarters and to check the exact
  amount. Part D 2026 parameters ($615 max deductible, $2,100
  out-of-pocket cap, $38.99 base premium) corroborated by multiple
  sources citing the CMS CY2026 Rate Announcement.
- Penalties vs medicare.gov "Avoid late enrollment penalties": Part B
  +10% per full 12-month period, for as long as you have Part B;
  Part D +1% per month after 63+ days without creditable coverage.
- Enrollment windows: IEP 7 months around the 65th-birthday month,
  GEP Jan 1-Mar 31 with coverage the month after enrolling, SEP 8
  months after job coverage ends (COBRA does not count), AEP
  Oct 15-Dec 7 for plan changes.
- Medigap: MA/MN/WI use their own standardized plans instead of the
  lettered A-N plans (multiple sources, incl. medicare.gov-based
  guides); CT/NY year-round guaranteed issue, MA annual Feb 1-Mar 31
  window, ME switch-to-equal-or-lesser + annual Plan A window
  (KFF Oct 2026 review cited by multiple sources).
- SHIP phones: carried over from the buried Medicare block already
  live on every state page; 10 spot-checked against a second official
  source (CA aging.ca.gov + CMS, FL/OH/PA via Consumer Reports and
  the Oklahoma DOI official SHIP table, IN in.gov, MI MDHHS, MD
  govdelivery, NJ nj.gov, NY npidashboard/CMS). National SHIP line
  877-839-2675 from shiphelp.org (SHIP TA Center).
- SHIP program URLs curl-swept: 37x 200 on first pass (OH 404 then
  200 on retry with a browser UA; TN 000 then 200). 10x 403 are
  official .gov bot filters (AZ, CO, KS, KY, ME, MI, NH, RI, VT, VA)
  — kept, as the URLs are already live on the site. LA (ldi.la.gov)
  and NM (aging.nm.gov) returned 000 from this VM on every attempt —
  kept, as they are already live on the site; flagged here.
- No "this state has no X" claims are printed. Maine has no statewide
  SHIP phone in the buried block, so no phone is printed for Maine —
  the text routes readers to the program page for a local counselor.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "medicare-enrollment" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"

TOPIC = "medicare-enrollment"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def tel(phone):
    return re.sub(r"\D", "", phone or "")


def section_html(s):
    state = s["state"]
    slug = s["slug"]
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="medicare-enrollment-in-{slug}">Signing Up for Medicare '
        f"in {esc(state)}</h2>"
    )
    parts.append(
        f"<p>Medicare is the federal health insurance program for people "
        f"65 and older (and some younger people with disabilities). The "
        f"part that trips people up is not the coverage — it is the "
        f"calendar. Sign up in the wrong window, or late, and you can "
        f"wait months for coverage and pay a higher premium for the rest "
        f"of your life. This section covers when to sign up, what each "
        f"part covers and costs in 2026, the late penalties, Medigap "
        f"versus Medicare Advantage, free help in {esc(state)}, and how "
        f"to enroll. If Medicare denies a claim or cuts a benefit you "
        f"already have, that is an appeal — see the Public Benefits "
        f"Appeals section on this page. This is general information, "
        f"not legal advice.</p>"
    )
    # --- When to sign up ---
    parts.append('<div class="card">')
    parts.append("<h3>When to sign up — three windows</h3>")
    parts.append(
        "<p><strong>Your first window (Initial Enrollment Period):</strong> "
        "7 months — the 3 months before the month you turn 65, that "
        "month, and the 3 months after. Sign up in the 3 months before "
        "your birthday month and coverage can start the first day of "
        "your birthday month; sign up during or after it and coverage "
        "usually starts the first day of the next month.</p>"
    )
    parts.append(
        "<p><strong>If you miss it (General Enrollment Period):</strong> "
        "January 1 to March 31 every year. Coverage starts the first "
        "day of the month after you sign up, and a late penalty may "
        "apply (below).</p>"
    )
    parts.append(
        "<p><strong>Still working at 65 (Special Enrollment Period):</strong> "
        "if you or your spouse are still working with health coverage "
        "from that job, you can usually sign up later without a "
        "penalty — but the clock is strict: the special window ends "
        "8 months after the job or the job coverage ends, whichever "
        "comes first. Two traps: COBRA does not count as job coverage "
        "and does not extend the 8 months, and retiree coverage ending "
        "does not start a new window. If the employer has fewer than "
        "20 workers, Medicare is expected to pay first — ask your "
        "state's free counselors below before you delay Part B.</p>"
    )
    parts.append(
        "<p><strong>Already on Medicare and want to change plans:</strong> "
        "the Annual Enrollment Period runs October 15 to December 7 "
        "each year, with changes taking effect January 1.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Mark your 7-month "
        "window on a calendar the day you turn 64 and a half, and "
        "sign up in the first 3 months of it if you can.</p>"
    )
    parts.append("</div>")
    # --- Parts and costs ---
    parts.append('<div class="card">')
    parts.append("<h3>What each part covers — and what it costs in 2026</h3>")
    parts.append(
        "<p><strong>Part A (hospital insurance):</strong> inpatient "
        "hospital stays, skilled nursing care, hospice, and some home "
        "health care. Most people pay no Part A premium — you qualify "
        "if you or your spouse paid Medicare taxes for 40 quarters "
        "(10 years). With fewer than 30 quarters the premium is "
        "$565 a month in 2026; with 30 to 39 quarters it is lower — "
        "check the exact amount at medicare.gov or with your SHIP "
        "counselor. The Part A deductible is $1,736 for each benefit "
        "period in 2026 (a benefit period is not the same as a "
        "calendar year).</p>"
    )
    parts.append(
        "<p><strong>Part B (medical insurance):</strong> doctors, "
        "outpatient care, medical equipment, and many preventive "
        "services. The standard premium is $202.90 a month in 2026, "
        "and the yearly deductible is $283. After the deductible you "
        "usually pay 20% of the Medicare-approved amount for most "
        "services, and Original Medicare has no yearly cap on what "
        "you can owe. Higher earners pay an extra amount (called "
        "IRMAA) on top of the Part B and Part D premiums, based on a "
        "tax return from 2 years ago.</p>"
    )
    parts.append(
        "<p><strong>Part D (prescription drugs):</strong> sold by "
        "private companies Medicare approves. Premiums vary by plan. "
        "In 2026 a plan can charge a deductible of no more than "
        "$615 a year, and your out-of-pocket spending on covered "
        "drugs is capped at $2,100 for the year — after that you pay "
        "nothing more for covered drugs until January.</p>"
    )
    parts.append(
        "<p><strong>Part C (Medicare Advantage):</strong> a private "
        "plan Medicare approves that bundles Parts A and B, usually "
        "with drug coverage too — see the Medigap card below before "
        "you choose.</p>"
    )
    parts.append(
        "<p>Lower income? Medicare Savings Programs, run through "
        "your state Medicaid office, can help pay Part A and B costs "
        "like premiums — and getting one also gives you Extra Help "
        "with drug costs automatically.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Budget for the "
        "2026 Part B premium ($202.90 a month) plus the $283 "
        "deductible, and compare drug plans on their total yearly "
        "cost for your prescriptions — not just the monthly premium.</p>"
    )
    parts.append("</div>")
    # --- Penalties ---
    parts.append('<div class="card">')
    parts.append("<h3>Late sign-up penalties — they last</h3>")
    parts.append(
        "<p><strong>Part B:</strong> your premium goes up an extra "
        "10% for each full 12-month period you could have had Part B "
        "but did not — and you usually pay that higher premium for as "
        "long as you have Part B. Two full years late means 20% more, "
        "every month. (On the 2026 standard premium of $202.90, one "
        "12-month delay adds about $20.30 a month.)</p>"
    )
    parts.append(
        "<p><strong>Part D:</strong> if you go 63 days or more without "
        "a drug plan or other creditable drug coverage, you pay an "
        "extra 1% for each month you went without it — also for as "
        "long as you have drug coverage. The 1% is figured on the "
        "national base premium ($38.99 a month in 2026).</p>"
    )
    parts.append(
        "<p><strong>Part A (if you pay a premium for it):</strong> "
        "signing up late can raise your premium by 10% for twice as "
        "many years as you waited.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If your first "
        "window has already passed, do not wait for January — check "
        "today whether a Special Enrollment Period applies to you, "
        "because every full 12 months of delay adds another 10% to "
        "Part B.</p>"
    )
    parts.append("</div>")
    # --- Medigap vs Advantage ---
    parts.append('<div class="card">')
    parts.append("<h3>Original Medicare + Medigap, or a Medicare Advantage plan?</h3>")
    parts.append(
        "<p><strong>Path one: Original Medicare plus a Medigap "
        "policy.</strong> Medigap is extra private insurance that "
        "helps pay your share of Original Medicare costs, and you can "
        "see any doctor who takes Medicare. Your best time to buy is "
        "the 6-month window that starts the month you have Part B and "
        "are 65 or older — during it, insurers cannot turn you down "
        "for health problems; later, they usually can. In most states "
        "Medigap plans are sold as standardized lettered plans (A, B, "
        "D, G, K, L, M, N — Plans C and F are closed to anyone who "
        "became eligible for Medicare on or after January 1, 2020); "
        "the same letter means the same benefits no matter which "
        "company sells it, so compare on price and service.</p>"
    )
    if s.get("medigap_note"):
        parts.append(f"<p><strong>In {esc(state)}:</strong> {esc(s['medigap_note'])}</p>")
    parts.append(
        "<p><strong>Path two: a Medicare Advantage plan.</strong> One "
        "private plan instead of Original Medicare, usually with a "
        "doctor network, approvals for some care, a yearly cap on "
        "out-of-pocket costs, and extras like dental, vision, or "
        "hearing. You cannot use a Medigap policy with an Advantage "
        "plan. Neither path is right for everyone — that is what the "
        "free counselors below are for.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Decide the path "
        "before you buy anything: if you want Medigap, buy inside "
        "your 6-month window at 65 — after it closes, your health "
        "history can shut the door in most states.</p>"
    )
    parts.append("</div>")
    # --- Free help ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Free Medicare counseling in {esc(state)}</h3>")
    if s.get("ship_phone"):
        parts.append(
            f"<p>{esc(state)}'s free Medicare counseling program is "
            f"{esc(s['ship_name'])}. Call "
            f"<a href=\"tel:{tel(s['ship_phone'])}\">{esc(s['ship_phone'])}</a>. "
            f"SHIP counselors do not sell insurance and do not get paid "
            f"by any plan, so their only job is to help you choose."
            + (f" {esc(s['ship_note'])}" if s.get("ship_note") else "")
            + "</p>"
        )
    else:
        parts.append(
            f"<p>{esc(state)}'s free Medicare counseling program is "
            f"{esc(s['ship_name'])}. "
            + (f"{esc(s['ship_note'])} " if s.get("ship_note") else "")
            + "SHIP counselors do not sell insurance and do not get "
            "paid by any plan, so their only job is to help you choose.</p>"
        )
    parts.append(
        "<p>Anywhere in the country, you can also find your local SHIP "
        "through the national SHIP line at "
        "<a href=\"tel:8778392675\">1-877-839-2675</a> (say "
        "&ldquo;Medicare&rdquo; when prompted), or call 1-800-MEDICARE "
        "(<a href=\"tel:18006334227\">1-800-633-4227</a>), 24 hours a day.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Before you pick "
        "any plan, call your state's free counseling program above — "
        "a 20-minute call can save you a lifetime penalty or a "
        "Medigap door closing.</p>"
    )
    parts.append("</div>")
    # --- How to enroll ---
    parts.append('<div class="card">')
    parts.append("<h3>How to enroll, step by step</h3>")
    parts.append(
        "<p>If you are already getting Social Security benefits at "
        "least 4 months before you turn 65, Parts A and B start "
        "automatically and your Medicare card comes in the mail — "
        "check that it arrived and that the start date is right. "
        "Everyone else signs up through Social Security: online at "
        "ssa.gov, by phone, or at a local Social Security office. "
        "Have your Social Security number, date of birth, and proof "
        "of age and citizenship or lawful residence ready, plus your "
        "work history if you are claiming premium-free Part A through "
        "a spouse. You can sign up for Part D drug coverage, or a "
        "Medicare Advantage plan, at medicare.gov or by calling "
        "1-800-MEDICARE.</p>"
    )
    parts.append(
        "<p>Watch out for scams: real Medicare and Social Security "
        "will not call you out of the blue asking for money, gift "
        "cards, or your bank details to enroll you. Enroll only "
        "through the official sites and numbers above.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Sign up through "
        "Social Security in the first 3 months of your 7-month "
        "window, then check your Medicare card the day it arrives "
        "and confirm the coverage start date.</p>"
    )
    parts.append("</div>")
    # --- Official links ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Official links in {esc(state)}</h3>")
    parts.append("<ul>")
    if s.get("ship_url"):
        parts.append(
            f"<li><a href=\"{esc(s['ship_url'])}\" target=\"_blank\" "
            f"rel=\"noopener\">{esc(s['ship_name'])} ({esc(state)})</a></li>"
        )
    parts.append(
        "<li><a href=\"https://www.medicare.gov\" target=\"_blank\" "
        "rel=\"noopener\">Medicare.gov — the official Medicare site "
        "(or call 1-800-MEDICARE, 1-800-633-4227)</a></li>"
    )
    parts.append("</ul>")
    parts.append("</div>")
    # --- Do this now ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Turning 65 in the "
        "next few months? Mark your 7-month window on a calendar "
        "today, sign up in the first 3 months of it, and before you "
        "pick any plan, call your state's free counseling program "
        "above — SHIP counselors do not sell insurance, so their "
        "only job is to help you choose. If a benefit is denied or "
        "cut, the Public Benefits Appeals section on this page covers "
        "how to appeal.</p>"
    )
    parts.append(
        "<p><em>Sources: CMS 2026 Medicare Parts A &amp; B premiums "
        "and deductibles (announced November 2025) and the CMS "
        "CY2026 Part D benefit parameters; medicare.gov enrollment "
        "and penalty pages; your state's SHIP program page linked "
        "above. All dollar figures are for 2026 and change every "
        "year — confirm the current numbers at medicare.gov before "
        "you enroll. This is general information, not legal advice.</em></p>"
    )
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def build_state_pages(data):
    for s in data:
        slug = s["slug"]
        path = STATES / f"{slug}.html"
        text = path.read_text()
        anchor = f"medicare-enrollment-in-{slug}"
        assert anchor not in text, f"{slug}: anchor already present"
        # --- insert section before Property Tax Appeal section (newest-first) ---
        h2 = text.find(f'<h2 id="property-tax-appeal-in-{slug}">')
        assert h2 != -1, f"{slug}: property-tax-appeal h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        new_section = section_html(s)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the property-tax-appeal <li> ---
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#property-tax-appeal-in-'
            + re.escape(slug)
            + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: property-tax-appeal contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#medicare-enrollment-in-{slug}">'
            f"Signing Up for Medicare in {s['state']}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert "medicare-enrollment" not in helper_part, "index already has helper option"
    assert 'data-topic="medicare-enrollment"' not in text, "index already has card"
    opt_old = (
        '<option value="property-tax-appeal" data-anchor="property-tax-appeal">'
        "Appealing your property tax assessment</option>"
    )
    assert opt_old in text, "property-tax-appeal helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="medicare-enrollment" data-anchor="medicare-enrollment">'
        "Signing up for Medicare</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="property-tax-appeal"'
    idx = text.find(card_anchor)
    assert idx != -1, "property-tax-appeal card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="medicare-enrollment">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-medicare-enrollment.jpg" alt="Signing Up for Medicare" loading="lazy"></span>
          <h3>Signing Up for Medicare</h3>
          <p>Turning 65? Your sign-up windows, what each part covers and costs in 2026, the late penalties to avoid, Medigap vs. Medicare Advantage, and free help in your state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 30 topics" in text, "show-all label not found"
    text = text.replace("Show all 30 topics", "Show all 31 topics", 1)
    assert '<span class="count-badge">30 topics</span>' in text
    text = text.replace(
        '<span class="count-badge">30 topics</span>',
        '<span class="count-badge">31 topics</span>',
        1,
    )
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 30->31")


def build_about():
    text = ABOUT.read_text()
    assert "75 legal topics" in text, "about count not found"
    ABOUT.write_text(text.replace("75 legal topics", "76 legal topics", 1))
    print("  about.html: 75 -> 76")


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 10243, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith("medicare-enrollment-in-") for e in idx)
    for s in data:
        state = s["state"]
        slug = s["slug"]
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"medicare-enrollment-in-{slug}",
                "h": f"Signing Up for Medicare in {state}",
                "t": (
                    f"Signing Up for Medicare in {state} "
                    f"\u2014 medicare enrollment sign up initial enrollment "
                    f"period general enrollment period special enrollment "
                    f"period part a part b part c part d advantage medigap "
                    f"ship free counseling late penalty turning 65 {state}"
                ),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Signing Up for Medicare",
            "t": (
                "Turning 65? Your sign-up windows, what each part covers "
                "and costs in 2026, the late penalties to avoid, Medigap "
                "vs. Medicare Advantage, and free help in your state."
            ),
        }
    )
    assert len(idx) == 10294, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 10243 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [states[k] for k in sorted(states)]
    slugs = [s["slug"] for s in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert all(s.get("ship_name") and s.get("ship_url") for s in data), "missing SHIP data"
    assert all(s.get("medigap_note") is not None or True for s in data)
    print("building state pages...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
