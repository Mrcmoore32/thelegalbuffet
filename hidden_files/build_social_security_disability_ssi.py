#!/usr/bin/env python3
"""Build Topic #88: Social Security Disability & SSI (SSDI/SSI) — standalone
section on all 50 state pages.

Inserts one new section per state page (before Pensions & retirement benefits,
newest-first), a contents-list entry (before the pensions <li>), a homepage
helper option + topic card (after Pensions & retirement benefits), bumps About
86 -> 87, and appends 50 state entries + 1 helper entry to
assets/search-index.json (10804 -> 10855).

Data: hidden_files/topic-research/social-security-disability-ssi/all-states.json
(coordinator-built 2026-11-20 from 5 research batches; verification notes
in this docstring).

Coordinator verification before the build (Nov 20, 2026):
- Federal core vs official sources: 2026 work credit $1,890 (Federal Register
  2025-19763; $1,810 is the 2025 figure); 40 credits / 20 in last 10 years for
  age 31+; SGA 2026 $1,690/mo non-blind, $2,830 blind (SSA Ticket to Work 2026
  checklist); trial work period 2026 $1,210/mo; SSI federal benefit rate 2026
  $994 individual / $1,491 couple (Federal Register + CRS); SSI asset limits
  $2,000 / $3,000 (unchanged since 1989); disability attorney fee 25% of back
  pay, capped at $9,200 (since Nov 30, 2024); 60-day appeal deadline at every
  stage (ssa.gov); SSA phone 1-800-772-1213; SSDI 5-month waiting period;
  2026 COLA 2.8%.
- Phones: every printed DDS phone was checked against SSA's own
  Disability Determination Services directory
  (ssa.gov/disability/professionals/procontacts.htm, read Nov 20, 2026).
  9 researcher phones CONFLICTED with the SSA directory and were dropped
  (GA, MD, NY, NM, OH's 1-800-282-2695, OK, PA, RI, SC). 4 phones were ADDED
  because the SSA directory agreed with a single-source candidate (ND
  855-953-9654, TN 866-776-3193 — also printed on tn.gov's DDS page, UT
  800-221-3493, WA 800-562-6074). MI changed to 844-671-9165 (SSA directory
  lists it for all four MI offices; SSA's Chicago regional page still prints
  the older per-office 1-800-366-3404 — both are SSA-published; directory
  wins as the current master list). OH phone is 800-282-4536 (OOD toll-free,
  on the SSA Chicago regional page AND the OOD fact sheet). AL 800-292-8106
  kept (SSA SORN + two independent directories agree). NJ phone 1-888-576-5529
  is the Legal Services of New Jersey hotline (verified on nj.gov + LSNJ
  brochure) — labeled as such, NOT as a DDS number. 28 phones print.
- URLs: all 85 non-null DDS + legal-aid URLs curl-checked Nov 20. 26
  non-200: 15x403 + 3x406 are bot filters on official .gov / legal-aid
  domains — 8 confirmed alive via live browser text fetch (ssa.gov/chicago
  DDS page, ood.ohio.gov, otda.ny.gov, ors.ri.gov, lawyoming.org,
  lonestarlegal.org, mass.gov DDS, tn.gov DDS), same pattern as #87's 12x403.
  4 real problems fixed: AR legal aid http://arkansaslegal.org/ 404 ->
  https://www.arlegalservices.org (org's current site per AR National Guard
  official PDF Jul 2025 + arlegalaid.org); OH DDS ood.ohio.gov/help-center
  404 -> https://ood.ohio.gov/ (agency homepage, verified alive in browser);
  IL DDS dhs.state.il.us page.aspx 000/empty -> https://www.ssa.gov/chicago/dds.html
  (SSA regional page naming IL's DDS, verified alive); RI DDS URL stripped of
  junk "?ref=carefully.org" query -> https://ors.ri.gov/programs/disability-determination-services
  (verified alive); WY legal aid -> https://lawyoming.org/ (verified alive).
  IL DHS and NY OTDA pages return empty/000 to curl but the OTDA page was
  verified alive in browser and names the DDS program; IL now uses the SSA
  regional page instead.
- Nulls stay claim-free: 10 states have no verifiable standalone DDS webpage
  (AL, AZ, CA, HI, ID, IA, NH, NJ, SD, TX) — section routes those through SSA;
  5 states have no verifiable legal-aid URL (FL, GA, VT, WA, WI) — name only,
  no link; GA has no verified legal-aid org at all (name + URL null) — the
  legal-aid line is omitted for GA. CA has no DDS phone (sources disagreed).
- Online application link is secure.ssa.gov/iClaim/dib and the office locator
  is secure.ssa.gov/ICON/main.jsp — both taken verbatim from Lone Star Legal
  Aid's live SSI/SSDI page (read Nov 20, 2026), not guessed.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "social-security-disability-ssi" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-social-security-disability-ssi.jpg"

SLUG = "social-security-disability-ssi"
TITLE = "Social Security Disability & SSI"

SSA_PHONE = "1-800-772-1213"
SSA_APPLY_URL = "https://secure.ssa.gov/iClaim/dib"
SSA_OFFICE_URL = "https://secure.ssa.gov/ICON/main.jsp"

# Phone labels that are NOT the DDS office number.
PHONE_LABEL = {"new jersey": "Legal Services of New Jersey hotline"}
# DDS links that are not the DDS's own page.
DDS_HOMEPAGE_NOTE = {"ohio": "agency homepage"}


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="social-security-disability-ssi-in-{slug}">Social Security Disability &amp; SSI in {esc(state)}</h2>'
    )
    parts.append(
        "<p>If a health problem keeps you from working, Social Security has two programs "
        "that may pay you monthly benefits: SSDI and SSI. They have different rules, and "
        "you can apply for both at the same time. Most people are turned down the first "
        "time &mdash; that is normal, and it is not the end of the road. This section is "
        "the " + esc(state) + " picture as of <strong>November 2026</strong> &mdash; which "
        "program fits you, the five-step test Social Security uses, how to apply, what to "
        "do if you are denied, and where to get free help. This is general information, "
        "not legal advice.</p>"
    )
    # --- Card 1: SSDI vs SSI ---
    parts.append('<div class="card">')
    parts.append("<h3>SSDI vs SSI: which one fits you?</h3>")
    parts.append(
        "<p><strong>SSDI (Social Security Disability Insurance)</strong> is for people who "
        "worked and paid Social Security taxes. You need enough <strong>work credits</strong> "
        "&mdash; in 2026, one credit is $1,890 of earnings, and you can earn at most 4 "
        "credits a year. Most adults need 40 credits, with 20 of them earned in the last "
        "10 years. Your monthly amount depends on your earnings record. There is a "
        "<strong>five-month waiting period</strong> after Social Security says you are "
        "disabled before payments start, and Medicare starts 24 months after that.</p>"
    )
    parts.append(
        "<p><strong>SSI (Supplemental Security Income)</strong> is for people with limited "
        "income and few assets &mdash; no work history needed. In 2026 the limits are "
        "<strong>$2,000 in countable assets for one person, $3,000 for a couple</strong> "
        "(your home and one car usually do not count). The most SSI pays in 2026 is "
        "<strong>$994 a month for one person, $1,491 for a couple</strong> &mdash; your "
        "state may add a small supplement on top. SSI usually comes with Medicaid right "
        "away.</p>"
    )
    parts.append(
        "<p>You can get both at the same time if you qualify for both. Apply for both "
        "&mdash; Social Security will sort out which ones you qualify for.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you worked for years and then had to "
        "stop, start with SSDI. If you have little income and few savings, start with SSI. "
        "If you are not sure, apply for both &mdash; the application covers both programs.</p>"
    )
    parts.append("</div>")
    # --- Card 2: the 5-step test ---
    parts.append('<div class="card">')
    parts.append("<h3>The five-step test Social Security uses</h3>")
    parts.append(
        "<p>Every claim goes through the same five questions, in order. A &ldquo;no&rdquo; "
        "at step 5 means you are approved.</p>"
    )
    parts.append(
        "<p><strong>Step 1 &mdash; Are you working?</strong> If you earn more than "
        "<strong>$1,690 a month in 2026</strong> ($2,830 if you are blind), Social Security "
        "says you are doing &ldquo;substantial gainful activity&rdquo; and stops there.</p>"
    )
    parts.append(
        "<p><strong>Step 2 &mdash; Is your condition severe?</strong> It must significantly "
        "limit basic work activities &mdash; walking, standing, lifting, remembering, "
        "concentrating, getting along with people &mdash; and be expected to last at least "
        "12 months or result in death.</p>"
    )
    parts.append(
        "<p><strong>Step 3 &mdash; Does it meet a listing?</strong> Social Security has a "
        "book of conditions (&ldquo;the listings&rdquo;). If yours matches one, you are "
        "approved. Most conditions do not match a listing exactly, so most claims move on.</p>"
    )
    parts.append(
        "<p><strong>Step 4 &mdash; Can you do your past work?</strong> If you can still do "
        "any job you held in the last 15 years, you are denied. If not, on to step 5.</p>"
    )
    parts.append(
        "<p><strong>Step 5 &mdash; Can you do any other work?</strong> Social Security looks "
        "at your age, education, work history, and what you can still do, and asks whether "
        "any job exists in the national economy that you could do. If the answer is no, you "
        "are approved. Older workers with limited education and a long work history have the "
        "best odds at this step.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> When you describe your condition, "
        "describe what you <em>cannot do</em> &mdash; not just the diagnosis. &ldquo;I have "
        "a bad back&rdquo; is weak. &ldquo;I cannot sit for more than 20 minutes, I cannot "
        "lift a gallon of milk, and I have to lie down twice a day&rdquo; is what the "
        "examiner needs.</p>"
    )
    parts.append("</div>")
    # --- Card 3: how to apply ---
    parts.append('<div class="card">')
    parts.append("<h3>How to apply, and what evidence to gather</h3>")
    parts.append(
        "<p><strong>Three ways to apply:</strong> online at "
        f'<a href="{SSA_APPLY_URL}" target="_blank" rel="noopener">SSA&rsquo;s online disability application</a>, '
        f"by phone at {SSA_PHONE} (weekdays, 8 a.m. to 7 p.m. local time), or in person at "
        f'your local Social Security office (find it at <a href="{SSA_OFFICE_URL}" target="_blank" rel="noopener">SSA&rsquo;s office locator</a>). '
        "You apply to Social Security first. Social Security checks the non-medical rules "
        "(work credits for SSDI, income and assets for SSI), then sends your file to your "
        "state&rsquo;s Disability Determination Services office, which makes the medical "
        "decision.</p>"
    )
    parts.append(
        "<p><strong>Gather this before you apply:</strong> the names, addresses, and phone "
        "numbers of every doctor, clinic, and hospital that treated you; the dates you were "
        "seen; a list of your medicines; your work history for the last 15 years; and your "
        "most recent W-2 or tax return. Social Security will ask for your medical records "
        "directly, but it is faster if you bring copies of the most important ones yourself.</p>"
    )
    parts.append(
        "<p><strong>Two things that help a lot:</strong> a short written statement from your "
        "doctor describing your limits (not just your diagnosis), and your own notes about a "
        "typical day &mdash; what hurts, what you cannot finish, how often you have to rest. "
        "If Social Security sends you to one of its own doctors for an exam, go &mdash; "
        "missing it can get your claim denied.</p>"
    )
    parts.append(
        "<p><strong>Can I try working?</strong> Yes. In 2026 you can earn up to "
        "<strong>$1,210 a month</strong> for up to 9 months (the &ldquo;trial work "
        "period&rdquo;) without losing SSDI. Tell Social Security before you start.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Apply as soon as you stop working &mdash; "
        "do not wait until your savings run out, because the process takes months and the "
        "five-month SSDI waiting period only starts once you are found disabled.</p>"
    )
    parts.append("</div>")
    # --- Card 4: if denied ---
    parts.append('<div class="card">')
    parts.append("<h3>If you are denied: appeal, don&rsquo;t give up</h3>")
    parts.append(
        "<p>Most first applications are denied. That is the normal path, not a final answer. "
        "There are four appeal stages, and you have <strong>60 days</strong> to appeal at "
        "<strong>every</strong> stage. Miss the deadline and you have to start over.</p>"
    )
    parts.append(
        "<p><strong>1. Reconsideration.</strong> A different examiner looks at your file "
        "fresh. Send in any new medical records with it.</p>"
    )
    parts.append(
        "<p><strong>2. Hearing before an administrative law judge (ALJ).</strong> This is "
        "where most people win. You can testify, bring witnesses, and have a representative. "
        "Hearings are usually by phone or video now. It can take a year or more to get a "
        "hearing date &mdash; appeal anyway, and keep seeing your doctors while you wait.</p>"
    )
    parts.append(
        "<p><strong>3. Appeals Council.</strong> It reviews the judge&rsquo;s decision for "
        "legal mistakes. It can deny review, send the case back, or decide it itself.</p>"
    )
    parts.append(
        "<p><strong>4. Federal court.</strong> The last step &mdash; a federal judge reviews "
        "whether Social Security followed the law. You will almost certainly want a lawyer "
        "for this stage.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> The day a denial letter arrives, mark "
        "the 60-day deadline on your calendar and appeal in writing. Do not file a brand-new "
        "application instead of appealing &mdash; you lose your back-pay start date if you do.</p>"
    )
    parts.append("</div>")
    # --- Card 5: free help ---
    parts.append('<div class="card">')
    parts.append("<h3>Free help: legal aid and disability lawyers</h3>")
    parts.append(
        "<p><strong>Legal aid</strong> (free, in the state card below) helps low-income "
        "people apply and appeal. Many legal aid offices handle Social Security cases.</p>"
    )
    parts.append(
        "<p><strong>Disability lawyers work on contingency</strong> &mdash; you pay nothing "
        "up front and nothing at all unless you win. If you win, the fee comes out of your "
        "back pay: <strong>25%, capped at $9,200</strong>. The fee has to be approved by "
        "Social Security. A lawyer is most useful at the hearing stage, but many will take a "
        "case earlier.</p>"
    )
    parts.append(
        "<p><strong>Social Security itself</strong> answers questions for free at "
        f"{SSA_PHONE} &mdash; including TTY at 1-800-325-0778.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you were denied, call the legal aid "
        "office below or a disability lawyer before your 60 days run out. The first "
        "consultation is free &mdash; ask exactly that before you give anyone your information.</p>"
    )
    parts.append("</div>")
    # --- Card 6: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Disability decisions and free help in {esc(state)}</h3>")
    parts.append(
        "<p>Your claim starts with Social Security, but the medical decision is made by "
        "your state&rsquo;s Disability Determination Services (DDS) office &mdash; the "
        "state agency that decides whether you meet Social Security&rsquo;s medical rules.</p>"
    )
    if e["dds_url"]:
        dds_label = esc(e["dds_name"])
        note = DDS_HOMEPAGE_NOTE.get(slug, "")
        if slug == "illinois":
            parts.append(
                f"<p><strong>Disability Determination Services:</strong> "
                f'<a href="{esc(e["dds_url"])}" target="_blank" rel="noopener">{dds_label}</a> '
                "&mdash; this link goes to Social Security&rsquo;s regional page, which names "
                "Illinois&rsquo; DDS office and its phone number.</p>"
            )
        elif note:
            parts.append(
                f"<p><strong>Disability Determination Services:</strong> "
                f'<a href="{esc(e["dds_url"])}" target="_blank" rel="noopener">{dds_label}</a> '
                "&mdash; this link goes to the agency&rsquo;s homepage; the Division of "
                "Disability Determination is part of the agency.</p>"
            )
        else:
            parts.append(
                f"<p><strong>Disability Determination Services:</strong> "
                f'<a href="{esc(e["dds_url"])}" target="_blank" rel="noopener">{dds_label}</a>.</p>'
            )
    else:
        parts.append(
            f"<p><strong>Disability Determination Services:</strong> {esc(e['dds_name'])} "
            "&mdash; no standalone DDS webpage could be verified, so apply through Social "
            f"Security ({SSA_PHONE} or the online application above) and Social Security "
            "will send your file to the DDS office.</p>"
        )
    if e["phone"]:
        label = PHONE_LABEL.get(slug, "Disability Determination Services phone")
        parts.append(f"<p><strong>{esc(label)}:</strong> {esc(e['phone'])}.</p>")
    if e["legal_aid_name"]:
        if e["legal_aid_url"]:
            parts.append(
                f"<p><strong>Free legal help:</strong> "
                f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
            )
        else:
            parts.append(
                f"<p><strong>Free legal help:</strong> {esc(e['legal_aid_name'])} "
                "&mdash; no website link could be verified; search the name to find its "
                "current contact information.</p>"
            )
    parts.append(
        f"<p><strong>About {esc(state)}:</strong> {esc(e['state_note'])}</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Apply through Social Security first "
        f"&mdash; {SSA_PHONE} or the online application &mdash; then watch for mail from "
        "the DDS office. Answer every DDS letter and form quickly: the DDS decides your "
        "case on the records it has, and silence looks like you got better.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Apply for both SSDI and SSI through "
        "Social Security as soon as you stop working. (2) Gather your doctors&rsquo; names "
        "and your medical records, and describe what you cannot do &mdash; not just your "
        "diagnosis. (3) If you are denied, appeal within 60 days at every stage; do not file "
        "a new application instead. (4) Get free help before the deadline &mdash; legal aid "
        "or a disability lawyer who only gets paid if you win.</p>"
    )
    parts.append(
        "<p><em>Sources: Social Security Administration (2026 work credit, substantial "
        "gainful activity, trial work period, SSI federal benefit rate and asset limits, "
        "60-day appeal deadlines, DDS directory), Federal Register, and the official "
        + esc(state) + " agencies linked above, checked November 20, 2026. Benefit amounts "
        "and limits change each year &mdash; confirm the current figures with Social "
        "Security before you decide. This is general information, not legal advice.</em></p>"
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
        # --- insert section before Pensions & retirement benefits ---
        h2 = text.find(f'<h2 id="pensions-and-retirement-benefits-in-{slug}">')
        assert h2 != -1, f"{slug}: pensions h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        before = text
        new_section = section_html(state, slug, e)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the pensions <li> ---
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#pensions-and-retirement-benefits-in-'
            + re.escape(slug)
            + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: pensions contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#{SLUG}-in-{slug}">'
            f"Social Security Disability &amp; SSI in {state}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        # --- structural assertions ---
        assert text.count(f'id="{SLUG}-in-{slug}"') == 1, f"{slug}: anchor count"
        assert text.count("<div") - before.count("<div") == 6, f"{slug}: div open delta"
        assert text.count("</div>") - before.count("</div>") == 6, f"{slug}: div close delta"
        assert text.count("<div") == text.count("</div>"), f"{slug}: div imbalance"
        h2s = re.findall(r'<h2 id="([^"]+)">', text)
        assert h2s.index(f"{SLUG}-in-{slug}") == h2s.index(f"pensions-and-retirement-benefits-in-{slug}") - 1, f"{slug}: h2 order"
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
        '<option value="pensions-and-retirement-benefits" data-anchor="pensions-and-retirement-benefits">'
        "Pensions &amp; retirement benefits (vesting, company sale, PBGC, 401(k) rollover, appealing a denial)</option>"
    )
    assert opt_old in text, "pensions helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="social-security-disability-ssi" data-anchor="social-security-disability-ssi">'
        "Social Security Disability &amp; SSI (SSDI vs SSI, the five-step test, how to apply, appealing a denial)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="pensions-and-retirement-benefits"'
    idx = text.find(card_anchor)
    assert idx != -1, "pensions card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="social-security-disability-ssi">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-social-security-disability-ssi.jpg" alt="Social Security Disability &amp; SSI" loading="lazy"></span>
          <h3>Social Security Disability &amp; SSI</h3>
          <p>Health problems keeping you from work? SSDI vs SSI, the five-step test, how to apply, what to do if you&rsquo;re denied, and free help in your state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 41 topics" in text, "show-all label not found"
    text = text.replace("Show all 41 topics", "Show all 42 topics", 1)
    assert text.count('<span class="count-badge">41 topics</span>') == 1, "main-grid badge count"
    text = text.replace(
        '<span class="count-badge">41 topics</span>',
        '<span class="count-badge">42 topics</span>',
        1,
    )
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 41->42")


def build_about():
    text = ABOUT.read_text()
    assert text.count("86 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("86 legal topics", "87 legal topics", 1))
    print("  about.html: 86 -> 87")


def state_index_t(state, slug, e):
    bits = [
        "social-security-disability-ssi ssdi ssi disability benefits social security",
        f"Social Security Disability and SSI in {state}",
        "SSDI vs SSI work credits $1,890 40 credits 20 in last 10 years",
        "SSI asset limits $2,000 $3,000 federal benefit rate $994 $1,491 month 2026",
        "five-step sequential evaluation substantial gainful activity SGA $1,690 $2,830 blind",
        "how to apply online phone 1-800-772-1213 in person medical evidence",
        "denied appeal reconsideration ALJ hearing Appeals Council federal court 60 days every stage",
        "trial work period $1,210 month five-month waiting period",
        "disability lawyer contingency 25 percent back pay capped $9,200 free legal aid",
        f"{e['dds_name']}",
        f"{state} disability determination services DDS {e['state_note']}",
    ]
    return " — ".join(bits)


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 10804, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Social Security Disability & SSI in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Social Security Disability & SSI",
            "t": (
                "social-security-disability-ssi ssdi ssi disability benefits social security "
                "Health problems keeping you from work? SSDI vs SSI, the five-step test, how "
                "to apply, what to do if you're denied, and free help in your state. "
                "Work credits $1,890 40 credits SSI $994 $1,491 asset limits $2,000 $3,000 "
                "SGA $1,690 $2,830 trial work period $1,210 appeal 60 days reconsideration "
                "ALJ hearing Appeals Council federal court disability lawyer 25 percent "
                "capped $9,200 SSA 1-800-772-1213."
            ),
        }
    )
    assert len(idx) == 10855, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 10804 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [(k, states[k]) for k in sorted(states)]
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "dds_name", "dds_url", "legal_aid_name", "legal_aid_url",
        "state_note", "phone", "sources",
    ]
    phone_re = re.compile(r"\(\d{3}\)\s*\d{3}[-.]\d{4}|\b\d{3}[-.]\d{3}[-.]\d{4}\b|1-800-\d{3}-\d{4}|1-866-\d{3}-\d{4}|1-888-\d{3}-\d{4}|877-\d{3}-\d{4}|800-\d{3}-\d{4}|844-\d{3}-\d{4}|866-\d{3}-\d{4}")
    for k, e in data:
        for f in req:
            assert f in e, f"{k}: missing {f}"
        assert e["dds_name"] and e["state_note"] and e["sources"], f"{k}: empty required field"
        # legal_aid_name may be null only for Georgia (no verified org)
        assert e["legal_aid_name"] or k == "georgia", f"{k}: legal aid name missing"
        # phones appear only in the phone field (plus the SSA number in template)
        blob = json.dumps({f: e[f] for f in req if f != "phone"})
        assert not phone_re.search(blob), f"{k}: phone-like string outside phone field: {blob[:200]}"
        if e["phone"]:
            assert phone_re.search(e["phone"]), f"{k}: phone format {e['phone']!r}"
    print("building state pages (insert before pensions section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
