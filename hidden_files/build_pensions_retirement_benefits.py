#!/usr/bin/env python3
"""Build Topic #87: Pensions & Retirement Benefits — standalone section
on all 50 state pages.

Inserts one new section per state page (before Carry permit reciprocity,
newest-first), a contents-list entry (before the carry-permit <li>),
a homepage helper option + topic card (after Carry permit reciprocity),
bumps About 85 -> 86, and appends 50 state entries + 1 helper entry
to assets/search-index.json (10753 -> 10804).

Data: hidden_files/topic-research/pensions-and-retirement-benefits/all-states.json
(coordinator-built 2026-11-17 from 5 research batches; verification notes
in this docstring).

Coordinator verification before the build (Nov 17, 2026):
- Federal core vs official sources: ERISA vesting schedules (dol.gov FAQ);
  ERISA claim/appeal deadlines, 29 CFR 2560.503-1 (dol.gov) — re-verified
  by coordinator Nov 17 via independent search: 90 days initial decision
  (+90 extension), at least 60 days to appeal, 60 days review (+60).
  PBGC 2026 maximum $7,789.77/mo at age 65, single-employer plan,
  straight-life annuity (pbgc.gov tables; re-verified Nov 17 via three
  independent sources quoting the PBGC table). PBGC phone 1-800-400-7242
  (pbgc.gov) and EBSA phone 1-866-444-3272 (dol.gov/agencies/ebsa, which
  prints the number on the page — verified live Nov 17).
  401(k) cash-out: 10% additional tax under 59 1/2 (26 U.S.C. 72(t),
  IRS Topic 558); 20% mandatory withholding; 60-day rollover window;
  direct rollover avoids withholding and tax; rule-of-55 exception.
- All 100 state URLs (labor + AG) curl-checked Nov 17: 83x200, 12x403
  (bot filters on official .gov domains — confirmed alive via live
  browser text fetch for AZ labor, MT AG, SD AG), 1x404 fixed (Nebraska
  labor -> https://dol.nebraska.gov/LaborStandards/wages/WageComplaint,
  verified 200), 1x404 fixed (Ohio labor -> Ohio AG Labor Relations FAQ,
  which names the Bureau of Wage and Hour Administration and its phone
  614-644-2239; phone second-sourced on the AG FAQ + Legal Aid brochure).
  Tennessee labor + AG returned 200 on retry (transient 000s).
- Phones: 28 printed (27 from research + Ohio's 614-644-2239 added by
  coordinator). Spot-verified second sources: NC 1-800-625-2267 (labor.nc.gov),
  MN 651-284-5075 (dli.mn.gov), PA 1-800-932-0665 (pa.gov), TX 800-832-9243
  (twc.texas.gov, per researchers). All 28 are the state LABOR agency's
  number, and are labeled as such.
- States with no state wage-claim intake (AL, FL, GA): their labor URLs are
  department homepages/service directories. The section does NOT present
  them as claim-filing pages — it routes private-pension complaints to
  federal EBSA. Same treatment for LA (LWC homepage) and NM (nm.gov
  services directory). Mississippi has no state wage-hour agency (labor
  fields null by design) — the section says so and routes to EBSA.
  Iowa labor URL is the DIAL wage-complaint form PDF; West Virginia labor
  URL is a Division fact-sheet PDF expressly covering pensions as wages.
  Both are labeled accurately as PDFs.
- Wisconsin state note: the researchers' "about 704,000 workers" headcount
  was dropped (unverifiable) — the note now carries no headcount.
- North Carolina: NCDOL's own "Promised Wages" page says NCDOL does not
  handle pension/retirement/401(k) plans. The NC section carries that as
  a callout, since Craig's friend (the reason for this topic) is in NC.
- No phone numbers appear anywhere except the verified phone field and
  the two verified federal numbers. No "this state has no X" claim ships
  except Mississippi's (verified: no state wage-hour agency).
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "pensions-and-retirement-benefits" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-pensions-and-retirement-benefits.jpg"

SLUG = "pensions-and-retirement-benefits"
TITLE = "Pensions & retirement benefits"

EBSA_PHONE = "1-866-444-3272"
EBSA_URL = "https://www.dol.gov/agencies/ebsa"
PBGC_PHONE = "1-800-400-7242"
PBGC_URL = "https://www.pbgc.gov/"

# Labor links that are department homepages / service directories, NOT a
# claim-filing page. The section says so and routes pension complaints to EBSA.
HOMEPAGE_LABOR = {"alabama", "florida", "georgia", "louisiana", "new mexico"}


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="pensions-and-retirement-benefits-in-{slug}">Pensions &amp; retirement benefits in {esc(state)}</h2>'
    )
    parts.append(
        "<p>Your pension is money you already earned. If your employer is sold, merges, "
        "or goes out of business, the benefits you have already earned &mdash; and vested in "
        "&mdash; generally cannot be taken away from you. Federal law (ERISA, the Employee "
        "Retirement Income Security Act of 1974) protects them. What can change is the future: "
        "a new owner can freeze the plan so nobody earns more benefits going forward. This "
        "section is the " + esc(state) + " picture as of <strong>November 2026</strong> &mdash; "
        "what vesting means, what a sale can and can&rsquo;t change, what the federal pension "
        "insurer covers, what to do with a 401(k), and where to complain. This is general "
        "information, not legal advice.</p>"
    )
    # --- Card 1: sale / merger ---
    parts.append('<div class="card">')
    parts.append("<h3>Your pension after a sale or merger</h3>")
    parts.append(
        "<p>When a company is sold, the buyer usually takes over the pension plan along with "
        "the business. Your earned benefits stay yours &mdash; a sale does not erase them.</p>"
    )
    parts.append(
        "<p><strong>What can change:</strong> the new owner can <strong>freeze</strong> the plan, "
        "so nobody earns more benefits after the freeze date. Benefits already earned stay "
        "earned. If the plan ends entirely, the federal PBGC (below) may take over and pay "
        "benefits up to its limits.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Get your Summary Plan Description (SPD) "
        "and your latest benefit statement <strong>in writing</strong> &mdash; from HR or the "
        "plan administrator &mdash; and keep copies. Write down the plan&rsquo;s name and the "
        "administrator&rsquo;s contact information. Do not sign anything about your pension "
        "until you have read it &mdash; and if it is a buyout or a waiver, talk it through "
        "with someone you trust first (see the buyout card below).</p>"
    )
    parts.append("</div>")
    # --- Card 2: vesting ---
    parts.append('<div class="card">')
    parts.append("<h3>Vesting: when the pension is really yours</h3>")
    parts.append(
        "<p><strong>Vesting</strong> is the point where the employer&rsquo;s contributions to "
        "your pension become yours to keep, even if you leave the job.</p>"
    )
    parts.append(
        "<p><strong>Traditional pension (defined benefit):</strong> either a &ldquo;cliff&rdquo; "
        "&mdash; nothing until 5 years, then 100% vested &mdash; or &ldquo;graded&rdquo; &mdash; "
        "20% after 3 years, rising to 100% after 7 years. Cash-balance plans use a 3-year "
        "cliff.</p>"
    )
    parts.append(
        "<p><strong>401(k) and other defined-contribution plans:</strong> money you put in "
        "yourself is always 100% yours. Employer matching money vests on a 3-year cliff or "
        "graded over 2 to 6 years.</p>"
    )
    parts.append(
        "<p>Once you are vested, those benefits generally cannot be taken away &mdash; even if "
        "the company is sold.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check your benefit statement or SPD for "
        "your vesting date. If you are close to vesting, know the date before you make any "
        "job decision.</p>"
    )
    parts.append("</div>")
    # --- Card 3: PBGC ---
    parts.append('<div class="card">')
    parts.append("<h3>Is your pension insured? The PBGC</h3>")
    parts.append(
        "<p>The Pension Benefit Guaranty Corporation (PBGC), a federal agency, insures most "
        "private-sector traditional (defined-benefit) pensions. It does <strong>not</strong> "
        "insure 401(k)s, profit-sharing plans, IRAs, church plans, or government pensions.</p>"
    )
    parts.append(
        "<p>If a covered plan ends without enough money, the PBGC takes over and pays benefits "
        "up to a legal maximum. For plans ending in 2026, the maximum is <strong>$7,789.77 a "
        "month</strong> for a 65-year-old taking a straight-life annuity (about $93,477 a "
        "year) &mdash; less if you retire younger or choose a survivor benefit. Only benefits "
        "you were vested in are covered, and amounts above the cap can be lost.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If your plan ends, the PBGC will contact "
        "you &mdash; but keep your address updated with the plan and with the PBGC. PBGC: "
        f'<a href="{PBGC_URL}" target="_blank" rel="noopener">pbgc.gov</a>, {PBGC_PHONE}.</p>'
    )
    parts.append("</div>")
    # --- Card 4: 401(k) ---
    parts.append('<div class="card">')
    parts.append("<h3>Your 401(k) after a job loss or a sale</h3>")
    parts.append(
        "<p>A 401(k) is yours &mdash; the money sits in your account, not the company&rsquo;s. "
        "A sale does not take it.</p>"
    )
    parts.append(
        "<p><strong>Your options:</strong> leave it where it is, roll it into your new "
        "employer&rsquo;s plan, or roll it into an IRA. A <strong>direct rollover</strong> "
        "(plan to plan, or plan to IRA) has no tax and no withholding.</p>"
    )
    parts.append(
        "<p><strong>Cashing out is the expensive option:</strong> if you are under 59&frac12;, "
        "you pay income tax on the money <strong>plus a 10% additional tax</strong>, and the "
        "plan must withhold 20% for taxes up front. A $10,000 cash-out can leave you with "
        "roughly $6,000 to $7,000 after taxes and the penalty, depending on your tax bracket. "
        "Exception: if you leave your job in or after the year you turn 55, the 10% penalty "
        "usually does not apply (the &ldquo;rule of 55&rdquo;). If you do get a check, you "
        "have 60 days to roll it into an IRA or another plan to avoid the tax hit.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Do not cash out in a panic. A direct "
        "rollover keeps the full amount working for you and costs nothing in tax.</p>"
    )
    parts.append("</div>")
    # --- Card 5: buyout / waiver ---
    parts.append('<div class="card">')
    parts.append("<h3>Don&rsquo;t sign a buyout or waiver in a hurry</h3>")
    parts.append(
        "<p>After a sale, some employers offer a lump-sum buyout (&ldquo;take $X now instead of "
        "$Y a month for life&rdquo;) or ask you to sign a waiver giving up benefits.</p>"
    )
    parts.append(
        "<p>A lump sum can look big and still be worth less than the monthly checks over your "
        "lifetime. And once you take it, PBGC insurance no longer applies to that money.</p>"
    )
    parts.append(
        "<p>If you are married, your pension&rsquo;s default payout is a joint-and-survivor "
        "annuity &mdash; it keeps paying your spouse after you die. Waiving it usually "
        "requires your spouse&rsquo;s written, notarized consent.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Get any offer in writing, ask for the "
        "numbers behind it (what monthly benefit it replaces), and do not sign on the spot. "
        "EBSA&rsquo;s free benefits advisors (below) can walk through an offer with you "
        "before you decide.</p>"
    )
    parts.append("</div>")
    # --- Card 6: appealing a denial ---
    parts.append('<div class="card">')
    parts.append("<h3>If the plan says no: appealing a denial</h3>")
    parts.append(
        "<p>If the plan denies your claim or says you get less than you expected, ask for the "
        "denial <strong>in writing</strong> &mdash; it must explain why and how to appeal.</p>"
    )
    parts.append(
        "<p><strong>Federal deadlines (ERISA, 29 CFR 2560.503-1):</strong> the plan has "
        "<strong>90 days</strong> to decide a pension claim (it can extend once, by up to 90 "
        "more days, if it tells you in writing). You then have <strong>at least 60 days</strong> "
        "to appeal. The plan has <strong>60 days</strong> to decide the appeal (again, one "
        "extension of up to 60 days).</p>"
    )
    parts.append(
        "<p>Miss the appeal deadline and you can lose the right to fight it &mdash; mark the "
        "date the day the letter arrives.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Appeal in writing, keep copies of "
        "everything, and call EBSA&rsquo;s free benefits advisors &mdash; "
        f"{EBSA_PHONE} &mdash; if the plan will not answer or the deadline is near. You can "
        "also sue under ERISA after the appeal, but that is the last step, not the first.</p>"
    )
    parts.append("</div>")
    # --- Card 7: where to complain in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Where to complain in {esc(state)}</h3>")
    parts.append(
        "<p><strong>Federal help, free:</strong> EBSA benefits advisors help with plan "
        "problems &mdash; call "
        f"{EBSA_PHONE} or visit "
        f'<a href="{EBSA_URL}" target="_blank" rel="noopener">dol.gov/agencies/ebsa</a>. '
        "For a failed pension plan, the PBGC: "
        f'<a href="{PBGC_URL}" target="_blank" rel="noopener">pbgc.gov</a>, {PBGC_PHONE}.</p>'
    )
    if slug == "north-carolina":
        parts.append(
            "<p><strong>North Carolina note:</strong> the North Carolina Department of Labor "
            "&mdash; Wage and Hour Bureau says it does <strong>not</strong> handle pension, "
            "retirement, or 401(k) plans. For a private pension, start with the federal EBSA "
            "benefits advisors above.</p>"
        )
    if e["labor_agency_url"] is None:
        parts.append(
            "<p><strong>No state labor office:</strong> Mississippi has no state wage-hour "
            "agency, so there is no state office to file a pension complaint with &mdash; "
            "start with the federal EBSA benefits advisors above.</p>"
        )
    else:
        labor_label = esc(e["labor_agency_name"])
        if slug in HOMEPAGE_LABOR:
            parts.append(
                f"<p><strong>State labor office:</strong> "
                f'<a href="{esc(e["labor_agency_url"])}" target="_blank" rel="noopener">{labor_label}</a> '
                "&mdash; this link goes to the department&rsquo;s site, not a pension-complaint "
                "form. For a private pension problem, start with the federal EBSA benefits "
                "advisors above &mdash; pension law for private employers is federal.</p>"
            )
        elif slug == "iowa":
            parts.append(
                f"<p><strong>State labor office:</strong> "
                f'<a href="{esc(e["labor_agency_url"])}" target="_blank" rel="noopener">{labor_label}</a> '
                "&mdash; wage-complaint form (PDF).</p>"
            )
        elif slug == "west-virginia":
            parts.append(
                f"<p><strong>State labor office:</strong> "
                f'<a href="{esc(e["labor_agency_url"])}" target="_blank" rel="noopener">{labor_label}</a> '
                "&mdash; fact sheet (PDF) that covers pensions as wages.</p>"
            )
        elif slug == "ohio":
            parts.append(
                f"<p><strong>State labor office:</strong> "
                f'<a href="{esc(e["labor_agency_url"])}" target="_blank" rel="noopener">{labor_label}</a> '
                "&mdash; the Ohio Attorney General&rsquo;s labor FAQ names the Bureau and its "
                "phone number; the Bureau takes complaints by phone and by mail.</p>"
            )
        else:
            parts.append(
                f"<p><strong>State labor office:</strong> "
                f'<a href="{esc(e["labor_agency_url"])}" target="_blank" rel="noopener">{labor_label}</a>.</p>'
            )
        if e["phone"]:
            parts.append(
                f"<p><strong>State labor office phone:</strong> {esc(e['phone'])}.</p>"
            )
    parts.append(
        f"<p><strong>State attorney general:</strong> "
        f'<a href="{esc(e["ag_url"])}" target="_blank" rel="noopener">{esc(e["ag_name"])}</a>.</p>'
    )
    parts.append(
        f"<p><strong>Public-sector pensions in {esc(state)}:</strong> {esc(e['state_note'])}</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> For a private pension, start with EBSA "
        f"&mdash; {EBSA_PHONE}, free. For a public-employee pension, start with the retirement "
        "system named above.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Get your Summary Plan Description and "
        "latest benefit statement in writing and keep copies. (2) Check your vesting date "
        "before you make any job decision. (3) Do not sign a buyout or waiver on the spot, and "
        "do not cash out a 401(k) in a panic &mdash; a direct rollover costs nothing in tax. "
        "(4) If the plan denies you, appeal in writing before the deadline, and call EBSA&rsquo;s "
        f"free benefits advisors at {EBSA_PHONE} if you need help.</p>"
    )
    parts.append(
        "<p><em>Sources: U.S. Department of Labor (ERISA vesting and claims rules), Pension "
        "Benefit Guaranty Corporation (2026 maximum guarantee table), IRS Topic 558, and the "
        "official " + esc(state) + " agencies linked above, checked November 17, 2026. Pension "
        "maximums and plan rules change &mdash; confirm the current figures with the plan "
        "administrator or EBSA before you decide. This is general information, not legal "
        "advice.</em></p>"
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
        # --- insert section before Carry permit reciprocity ---
        h2 = text.find(f'<h2 id="carry-permit-reciprocity-in-{slug}">')
        assert h2 != -1, f"{slug}: carry-permit h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        before = text
        new_section = section_html(state, slug, e)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the carry-permit <li> ---
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#carry-permit-reciprocity-in-'
            + re.escape(slug)
            + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: carry-permit contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#{SLUG}-in-{slug}">'
            f"Pensions &amp; retirement benefits in {state}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        # --- structural assertions ---
        assert text.count(f'id="{SLUG}-in-{slug}"') == 1, f"{slug}: anchor count"
        assert text.count("<div") - before.count("<div") == 7, f"{slug}: div open delta"
        assert text.count("</div>") - before.count("</div>") == 7, f"{slug}: div close delta"
        assert text.count("<div") == text.count("</div>"), f"{slug}: div imbalance"
        h2s = re.findall(r'<h2 id="([^"]+)">', text)
        assert h2s.index(f"{SLUG}-in-{slug}") == h2s.index(f"carry-permit-reciprocity-in-{slug}") - 1, f"{slug}: h2 order"
        assert "None" not in new_section, f"{slug}: leaked None in new section"
        assert "TODO" not in new_section and "FIXME" not in new_section, f"{slug}: leaked marker"
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert SLUG not in helper_part, "index already has helper option"
    assert f'data-topic="{SLUG}"' not in text, "index already has card"
    opt_old = (
        '<option value="carry-permit-reciprocity" data-anchor="carry-permit-reciprocity">'
        "Carry permit reciprocity &amp; travel (which states honor your permit, permitless carry, travel rules)</option>"
    )
    assert opt_old in text, "carry-permit helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="pensions-and-retirement-benefits" data-anchor="pensions-and-retirement-benefits">'
        "Pensions &amp; retirement benefits (vesting, company sale, PBGC, 401(k) rollover, appealing a denial)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="carry-permit-reciprocity"'
    idx = text.find(card_anchor)
    assert idx != -1, "carry-permit card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="pensions-and-retirement-benefits">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-pensions-and-retirement-benefits.jpg" alt="Pensions &amp; retirement benefits" loading="lazy"></span>
          <h3>Pensions &amp; Retirement Benefits</h3>
          <p>Company sold and worried about your pension? Vesting, what a sale can and can&rsquo;t change, PBGC insurance, 401(k) rollovers, and appealing a denial.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 40 topics" in text, "show-all label not found"
    text = text.replace("Show all 40 topics", "Show all 41 topics", 1)
    assert text.count('<span class="count-badge">40 topics</span>') == 1, "main-grid badge count"
    text = text.replace(
        '<span class="count-badge">40 topics</span>',
        '<span class="count-badge">41 topics</span>',
        1,
    )
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 40->41")


def build_about():
    text = ABOUT.read_text()
    assert text.count("85 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("85 legal topics", "86 legal topics", 1))
    print("  about.html: 85 -> 86")


def state_index_t(state, slug, e):
    bits = [
        "pensions-and-retirement-benefits pensions retirement vesting ERISA PBGC",
        f"Pensions and retirement benefits in {state}",
        "company sale merger freeze earned benefits cannot be taken away",
        "vesting cliff graded 5 years 7 years 401(k) employer match",
        "PBGC insures traditional pensions not 401(k) maximum $7,789.77 month age 65",
        "401k 401(k) rollover direct rollover cash-out 10 percent penalty under 59 1/2 20 percent withholding 60 days rule of 55",
        "buyout lump sum waiver spouse consent joint-and-survivor annuity",
        "appeal denial 90 days decide 60 days appeal 60 days review EBSA benefits advisors 1-866-444-3272",
        f"{e['labor_agency_name'] if e['labor_agency_name'] else 'no state labor agency'} {e['ag_name']}",
        f"{state} public pension {e['state_note']}",
    ]
    return " — ".join(bits)


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 10753, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Pensions & retirement benefits in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Pensions & Retirement Benefits",
            "t": (
                "pensions-and-retirement-benefits pensions retirement vesting ERISA PBGC "
                "Company sold and worried about your pension? Vesting, what a sale can and "
                "can't change, PBGC insurance, 401k 401(k) rollovers, and appealing a denial. "
                "Sale merger freeze buyout lump sum waiver appeal denial 90 days 60 days "
                "EBSA benefits advisors 1-866-444-3272 PBGC 1-800-400-7242."
            ),
        }
    )
    assert len(idx) == 10804, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 10753 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [(k, states[k]) for k in sorted(states)]
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "labor_agency_name", "labor_agency_url", "ag_name", "ag_url",
        "state_note", "phone", "sources",
    ]
    phone_re = re.compile(r"\(\d{3}\)\s*\d{3}[-.]\d{4}|\b\d{3}[-.]\d{3}[-.]\d{4}\b|1-800-\d{3}-\d{4}|1-866-\d{3}-\d{4}|1-888-\d{3}-\d{4}|877-\d{3}-\d{4}|800-\d{3}-\d{4}")
    for k, e in data:
        for f in req:
            assert f in e, f"{k}: missing {f}"
        assert e["ag_url"] and e["ag_name"] and e["state_note"] and e["sources"], f"{k}: empty required field"
        assert e["labor_agency_url"] or k == "mississippi", f"{k}: labor URL missing"
        # phones appear only in the phone field (plus the two federal numbers in template)
        blob = json.dumps({f: e[f] for f in req if f != "phone"})
        assert not phone_re.search(blob), f"{k}: phone-like string outside phone field"
        if e["phone"]:
            assert phone_re.search(e["phone"]), f"{k}: phone format {e['phone']!r}"
    print("building state pages (insert before carry-permit section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
