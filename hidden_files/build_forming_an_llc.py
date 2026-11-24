#!/usr/bin/env python3
"""Build Topic #113: Forming an LLC — standalone section on
all 50 state pages.

Inserts one new section per state page (before Protecting Kids Online,
newest-first), a contents-list entry (before the protecting-kids-online
<li>), a homepage helper option + topic card (after Protecting Kids
Online), bumps About 111 -> 112, and appends 50 state entries + 1
helper entry to assets/search-index.json (12079 -> 12130).

Data: hidden_files/topic-research/forming-an-llc/all-states.json
(coordinator-merged 2026-11-24 from 5 research batches; see
merge_forming_an_llc.py for the fixes applied at merge).

RELATIONSHIP TO SMALL BUSINESS BASICS (decision): the new topic is the
one canonical home for LLC formation steps, fees, and forms. In Small
Business Basics the structure-pick comparison ("Pick a structure
first") STAYS, and the full "Forming an LLC in [State]: the general
steps" resource block is REPLACED with a short pointer resource to the
new topic (same r-tag, same slot in the list). The Small Business
Basics closing sentence "This page does not print a single [State] LLC
filing fee..." is updated to point at the new section, since the page
now DOES print the verified fee there. The next-steps checklist and
everything else in Small Business Basics is untouched.

Spot verifications 2026-11-24 (second sources, all confirmed):
- VT formation $155 / annual $45 — 11 V.S.A. sec. 4012 (Act 77, 2023).
- NJ formation $100 — DORES fee schedule, P.L. 2026 c.24 (eff. 7/1/2026).
- MO formation $50 online / $105 paper — SOS Schedule of Fees.
- DE annual LLC tax $400, tax year 2026 onward (HB 400; first $400
  payment due June 1, 2027).
- WV series LLCs — SB 670 (2026), W. Va. Code sec. 31B-14-101 et seq.,
  eff. June 12, 2026; Form LLD-11, $25 per protected series.
- UT series LLCs — Utah Code sec. 48-3a-1201.
- FL series LLCs — Fla. Stat. 605.2101-605.2802, eff. July 1, 2026;
  $25 per protected series, online only.
- KS formation $85 online / $90 paper — SOS Form DL (Rev. 2/27/26).
- IN biennial report $32 online / $50 paper; formation $95/$100.
- MT series LLCs — MCA secs. 35-8-202, 35-8-304; formation $35;
  annual report waived for on-time filings 2026-2027.
- NE series LLCs — Neb. Rev. Stat. secs. 21-501 to 21-542 (LB1121).
- OH series LLCs — Ohio Rev. Code secs. 1706.76-1706.7613.
- LA formation $125 / annual $35 / foreign $185 — Act 921 of 2026,
  SOS fee schedule eff. Oct 1, 2026.
- AR formation $45 online / $50 paper (Form LL-01) — SOS fee table.
- Foreign LLC fees added at merge: ID $100/$120, IN $105/$125,
  KS $115, TN $300 minimum, UT $59, VT $155, WY $150.
- WI series citation corrected at merge to Wis. Stat. sec. 183.0504.

Claim-free fields (gap rule — line omitted, field never removed):
series_llc empty in HI, ID, KY, LA, ME, NM, RI, SC (published lists
conflict; no verified answer — the section says so plainly).
single_member empty in 17 states — the builder uses the national line
"a single person can form an LLC in every state" (true in all 50).

No phone numbers in the state dataset; none are printed. The two
national links in the shared template (IRS EIN page, SBA launch guide
via the Small Business Basics cross-link) are URLs already used on
the site.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "forming-an-llc" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-forming-an-llc.jpg"

SLUG = "forming-an-llc"
TITLE = "Forming an LLC"
PREV_SLUG = "protecting-kids-online"
SBB_SLUG = "small-business-basics"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def cap(s):
    """Capitalize the first letter of a data sentence for mid-text use."""
    s = (s or "").strip()
    return s[:1].upper() + s[1:] if s else s


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="forming-an-llc-in-{slug}">Forming an LLC in {esc(state)}</h2>'
    )
    parts.append(
        "<p>An LLC — a limited liability company — is the most common way "
        "small businesses get legal protection without the paperwork of a "
        "corporation. It creates a separate legal person: the business can "
        "own things, sign contracts, and be sued, and your personal house "
        "and savings are usually shielded from the business&rsquo;s debts. "
        "That shield is not magic — it does not protect you from debts you "
        "personally guaranteed, from harm you caused yourself, or from "
        "taxes, and a court can strip it away if you treat the LLC like "
        "your personal wallet (lawyers call that &ldquo;piercing the "
        "corporate veil&rdquo;). This section covers what an LLC does and "
        "does not do, the steps to form one in "
        f"{esc(state)}, what it costs, and the traps first-timers fall "
        "into. This is general information, not legal advice.</p>"
    )
    # --- Card 1: what an LLC is ---
    parts.append('<div class="card">')
    parts.append("<h3>What an LLC is — and what it does not do</h3>")
    parts.append(
        "<p><strong>What it does:</strong> it separates your personal "
        "assets from the business. If the business is sued or cannot pay "
        "a supplier, the creditor generally goes after the business&rsquo;s "
        "money, not your house, car, or personal bank account. It also "
        "gives the business credibility — customers, landlords, and banks "
        "take a registered LLC more seriously than a name on a handshake — "
        "and it lets you choose how the business is taxed.</p>"
    )
    parts.append(
        "<p><strong>What it does not do:</strong> it does not protect "
        "you from your own actions — if you personally hurt someone or "
        "commit fraud, you are still liable. It does not cover debts you "
        "personally guaranteed (most small-business loans and commercial "
        "leases ask for one). It does not pay your taxes or keep the "
        "business legal on its own — you still have to file the annual "
        "report, keep licenses current, and keep business money separate. "
        "And the shield only holds if you treat the LLC as a real, "
        "separate business: its own bank account, its own records, and no "
        "mixing personal and business spending.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you want the "
        "protection, form the LLC before you take on customers, debt, or "
        "a lease — and open the business bank account the same week you "
        "file, so the separation is real from day one.</p>"
    )
    parts.append("</div>")
    # --- Card 2: LLC vs the others ---
    parts.append('<div class="card">')
    parts.append("<h3>LLC vs. sole proprietorship vs. partnership vs. corporation</h3>")
    parts.append(
        "<p><strong>Sole proprietorship:</strong> the simplest — you and "
        "the business are the same legal person, so you are personally "
        "liable for its debts. <strong>Partnership:</strong> two or more "
        "owners sharing the business, and sharing the liability unless it "
        "is a limited partnership. <strong>LLC:</strong> liability "
        "protection with simpler paperwork and fewer formalities than a "
        "corporation. <strong>Corporation:</strong> the strongest "
        "separation, but the most formalities — directors, bylaws, annual "
        "meetings and filings.</p>"
    )
    parts.append(
        "<p>There is no universally best choice: liability, taxes, and "
        "how many owners you have should drive it. The fuller comparison "
        "— and the rest of starting a business, from tax IDs to licenses "
        "to contracts — is in the "
        f'<a href="#small-business-basics-in-{slug}">Small business basics '
        f"section for {esc(state)}</a> on this page.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you are choosing "
        "between structures, read the comparison in Small business basics "
        "first, then come back here for the filing steps. If you already "
        "know you want an LLC, keep reading.</p>"
    )
    parts.append("</div>")
    # --- Card 3: how to form one in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>How to form an LLC in {esc(state)}</h3>")
    parts.append(f"<p><strong>How it works here:</strong> {esc(e['overview'])}</p>")
    parts.append(
        "<p><strong>The steps:</strong> (1) Pick a name and check it "
        "against the state&rsquo;s business registry so it is not already "
        "taken — the name has to include &ldquo;LLC,&rdquo; "
        "&ldquo;L.L.C.,&rdquo; or &ldquo;limited liability company.&rdquo; "
        f"(2) Name a registered agent. {esc(cap(e['registered_agent']))}. "
        f"(3) File the formation document with the {esc(e['filing_office'])} "
        f"— the filing fee is <strong>{esc(e['filing_fee'])}</strong>. "
        f"File through the filing office&rsquo;s own site: "
        f'<a href="{esc(e["filing_url"])}" target="_blank" rel="noopener">'
        f"{esc(e['filing_office'])}</a>, not a paid middleman site that "
        "charges extra for the same filing. (4) Get an EIN — a free "
        "Employer Identification Number from the IRS — at "
        '<a href="https://www.irs.gov/businesses/employer-identification-number" '
        'target="_blank" rel="noopener">irs.gov</a>; you need one if you '
        "hire employees, open a business bank account, or file certain "
        "tax returns, and any site charging a fee for an EIN is selling "
        "you a free government service. (5) Register for state taxes if "
        f"{esc(state)} requires it — if you sell taxable goods or hire "
        "workers, you will almost always need a state tax account, handled "
        "by the state tax or revenue department, not the filing office. "
        "(6) Check licenses at three levels — state, city or county, and "
        "your industry board — and check zoning before you sign a lease.</p>"
    )
    parts.append(
        f"<p><strong>Operating agreement:</strong> {esc(cap(e['operating_agreement']))}.</p>"
    )
    parts.append(
        f"<p><strong>Staying in good standing:</strong> {esc(cap(e['annual_report']))}.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check the name, name "
        "the agent, file with the filing office linked above, get the EIN "
        "free from the IRS, and write the operating agreement — even when "
        "the state does not require one — before money starts moving.</p>"
    )
    parts.append("</div>")
    # --- Card 4: single vs multi-member, series LLCs ---
    parts.append('<div class="card">')
    parts.append("<h3>One owner or several — and series LLCs</h3>")
    if e.get("single_member"):
        parts.append(
            f"<p><strong>Single-member vs. multi-member:</strong> {esc(cap(e['single_member']))}.</p>"
        )
    else:
        parts.append(
            "<p><strong>Single-member vs. multi-member:</strong> a single "
            "person can form an LLC — every state allows single-member "
            "LLCs. One owner or many, the steps are the same in "
            f"{esc(state)}.</p>"
        )
    if e.get("series_llc"):
        parts.append(
            f"<p><strong>Series LLCs:</strong> {esc(cap(e['series_llc']))}</p>"
        )
    else:
        parts.append(
            "<p><strong>Series LLCs:</strong> a series LLC is one LLC "
            "with internal compartments, each holding its own assets and "
            "liabilities — popular with landlords who hold several "
            "properties. We could not verify from an official source "
            f"whether {esc(state)} allows series LLCs, so this page does "
            "not say either way. If separate compartments matter to you, "
            "check with the filing office or a local business attorney "
            "before you file — and in the meantime, separate LLCs for "
            "separate properties get the same result at a higher filing "
            "cost.</p>"
        )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you are solo, a "
        "single-member LLC is fine — just keep the business account "
        "separate, because a one-person LLC is the easiest one for a "
        "court to treat as a personal wallet. If you have partners, put "
        "the ownership split, decision rules, and exit terms in the "
        "operating agreement before the first dollar comes in.</p>"
    )
    parts.append("</div>")
    # --- Card 5: foreign LLCs ---
    parts.append('<div class="card">')
    parts.append("<h3>Doing business in another state</h3>")
    parts.append(
        "<p>If your LLC was formed in one state but you do business in "
        "another — an office, employees, or regular sales there — the "
        "second state usually wants you to register as a &ldquo;foreign "
        "LLC&rdquo; before you operate. Doing business without "
        "registering can mean fines, back fees, and not being able to sue "
        "in that state&rsquo;s courts until you register.</p>"
    )
    parts.append(
        f"<p><strong>In {esc(state)}:</strong> {esc(cap(e['foreign_llc']))}</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you are expanding "
        "into another state, register there before you open, hire, or "
        "sign a lease — and budget for a registered agent and an annual "
        "report in every state where you are registered, not just your "
        "home state.</p>"
    )
    parts.append("</div>")
    # --- Card 6: first-timer traps ---
    parts.append('<div class="card">')
    parts.append("<h3>Common first-timer traps</h3>")
    parts.append(
        "<p><strong>Mixing money.</strong> Paying personal bills from the "
        "business account — or the reverse — is the fastest way to lose "
        "the liability shield. Open a business account and pay yourself "
        "properly. <strong>No operating agreement.</strong> Even where "
        "the state does not require one, skipping it leaves ownership, "
        "decisions, and what happens if an owner leaves up to the "
        "state&rsquo;s default rules — which may not be what you would "
        "choose. <strong>Forgetting the annual report.</strong> Miss it "
        "and the state can dissolve the LLC or fine you, and reinstating "
        "costs more than filing on time. <strong>Paying a middleman for a "
        "free filing.</strong> The EIN is free from the IRS, and the "
        "formation filing goes through the state&rsquo;s own site — "
        "services that charge hundreds of dollars are mostly charging for "
        "filling in the same form. <strong>Thinking the LLC shields you "
        "from everything.</strong> It does not cover personal guarantees, "
        "your own wrongdoing, or taxes — and it does not replace "
        "insurance. <strong>Skipping licenses.</strong> The state filing "
        "does not license your business; your city, county, and industry "
        "board each have their own requirements.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Separate the money "
        "from day one, write the operating agreement, put the annual "
        "report deadline on a calendar the week you file, and get "
        "liability insurance — the LLC and the insurance protect you in "
        "different ways, and you want both.</p>"
    )
    parts.append("</div>")
    # --- Card 7: where to file ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Where to file in {esc(state)}</h3>")
    parts.append(
        f"<p><strong>File with:</strong> "
        f'<a href="{esc(e["filing_url"])}" target="_blank" rel="noopener">'
        f"{esc(e['filing_office'])}</a> — the filing fee is "
        f"<strong>{esc(e['filing_fee'])}</strong>. "
        f"Fee verified against the filing office&rsquo;s own fee schedule: "
        f'<a href="{esc(e["fee_verified_url"])}" target="_blank" rel="noopener">'
        "fee schedule</a>.</p>"
    )
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">'
        f"{esc(e['legal_aid_name'])}</a>.</p>"
    )
    parts.append(
        "<p><strong>What to do:</strong> file through the filing "
        "office&rsquo;s own site, save every confirmation and receipt, "
        "and confirm the current fee on the filing page before you pay — "
        "fees change, and the number on this page is from November 2026.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Pick the "
        "structure — LLC if you want liability protection without "
        "corporate formalities. (2) Check the name, name a registered "
        "agent, and file with your state&rsquo;s filing office at the fee "
        "above. (3) Get the EIN free from the IRS and open a business "
        "bank account the same week. (4) Write the operating agreement, "
        "even if your state does not require one. (5) Put the annual "
        "report deadline on a calendar now — missing it is the most "
        "common way a good LLC goes bad.</p>"
    )
    parts.append(
        "<p><em>Sources: the Secretary of State (or equivalent filing "
        "office) for each state, the Internal Revenue Service, and the "
        "official state statutes linked in the research for this section, "
        "checked November 24, 2026. Filing fees change — confirm the "
        "current fee on the filing office&rsquo;s own page before you "
        "file. This is general information, not legal advice.</em></p>"
    )
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def build_state_pages(data):
    for key, e in data:
        state = e["state"]
        slug = e.get("slug") or key.replace(" ", "-")
        path = STATES / f"{slug}.html"
        text = path.read_text()
        before = text
        anchor = f'id="{SLUG}-in-{slug}"'
        assert anchor not in text, f"{slug}: anchor already present"
        # --- insert new section before Protecting Kids Online ---
        h2 = text.find(f'<h2 id="{PREV_SLUG}-in-{slug}">')
        assert h2 != -1, f"{slug}: {PREV_SLUG} h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
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
            f"Forming an LLC in {state}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        # --- Small Business Basics: replace the LLC-steps resource ---
        sbb_pat = re.compile(
            r'[ \t]*<div class="resource">\s*'
            r'<span class="r-tag">LLC formation</span>\s*'
            r'<h3>Forming an LLC in ' + re.escape(state) + r': the general steps</h3>\s*'
            r'<p>.*?</p>\s*</div>',
            re.S,
        )
        sbb_m = sbb_pat.search(text)
        assert sbb_m, f"{slug}: SBB LLC-steps resource not found"
        assert len(sbb_pat.findall(text)) == 1, f"{slug}: SBB LLC-steps resource count != 1"
        block = sbb_m.group(0)
        div_indent = block[: len(block) - len(block.lstrip())]
        span_m = re.search(r"\n([ \t]*)<span", block)
        inner_indent = span_m.group(1) if span_m else div_indent + "  "
        pointer = (
            f'{div_indent}<div class="resource">\n'
            f'{inner_indent}<span class="r-tag">LLC formation</span>\n'
            f'{inner_indent}<h3>Forming an LLC in {esc(state)}: the steps, fees, and forms</h3>\n'
            f'{inner_indent}<p>Forming an LLC now has its own section on this '
            "page, with "
            f"{esc(state)}&rsquo;s filing fee, filing office, registered-agent "
            "rule, operating-agreement rule, annual report, and series-LLC "
            "rules — all verified against the filing office. See "
            f'<a href="#{SLUG}-in-{slug}">Forming an LLC in {esc(state)}</a>.</p>\n'
            f"{div_indent}</div>"
        )
        text = text[: sbb_m.start()] + pointer + text[sbb_m.end():]
        assert f"Forming an LLC in {state}: the general steps" not in text, f"{slug}: old SBB h3 still present"
        assert f'href="#{SLUG}-in-{slug}"' in text, f"{slug}: SBB pointer link missing"
        # --- SBB closing sentence: fee now lives in the new section ---
        old_close = (
            f"This page does not print a single {state} LLC filing fee, "
            "form number, or license list because those vary by state and "
            "by city, county, and industry"
        )
        assert text.count(old_close) == 1, f"{slug}: SBB closing sentence not found exactly once"
        new_close = (
            f"The {state} LLC filing fee and form are in the "
            f'<a href="#{SLUG}-in-{slug}">Forming an LLC in {state}</a> '
            "section on this page. License lists vary by city, county, "
            "and industry"
        )
        text = text.replace(old_close, new_close, 1)
        # --- assertions ---
        assert text.count(f'id="{SLUG}-in-{slug}"') == 1, f"{slug}: anchor count"
        assert text.count("<div") - before.count("<div") == 7, f"{slug}: div open delta"
        assert text.count("</div>") - before.count("</div>") == 7, f"{slug}: div close delta"
        assert text.count("<div") == text.count("</div>"), f"{slug}: div imbalance"
        h2s = re.findall(r'<h2 id="([^"]+)">', text)
        assert h2s.index(f"{SLUG}-in-{slug}") == h2s.index(f"{PREV_SLUG}-in-{slug}") - 1, f"{slug}: h2 order"
        assert h2s.index(f"{SLUG}-in-{slug}") < h2s.index(f"{SBB_SLUG}-in-{slug}"), f"{slug}: new section should sit above SBB (newest-first)"
        assert not re.search(r"\bNone\b", new_section), f"{slug}: leaked None in new section"
        assert "TODO" not in new_section and "FIXME" not in new_section, f"{slug}: leaked marker"
        assert f'href="#{SBB_SLUG}-in-{slug}"' in new_section, f"{slug}: SBB cross-link missing"
        assert f'href="#{SLUG}-in-{slug}"' in text, f"{slug}: pointer anchor missing"
        path.write_text(text)
        print(f"  {slug}: section + contents entry + SBB pointer inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert SLUG not in helper_part, "index already has helper option"
    assert f'data-topic="{SLUG}"' not in text, "index already has card"
    m = re.search(
        r'<option value="protecting-kids-online" data-anchor="protecting-kids-online">.*?</option>',
        text,
        re.S,
    )
    assert m, "protecting-kids-online helper option not found"
    opt_old = m.group(0)
    opt_new = (
        opt_old
        + '\n<option value="forming-an-llc" data-anchor="forming-an-llc">'
        "Forming an LLC — what an LLC protects, the filing fee and steps in your state, registered agents, operating agreements, and annual reports</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="protecting-kids-online"'
    idx = text.find(card_anchor)
    assert idx != -1, "protecting-kids-online card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="forming-an-llc">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-forming-an-llc.jpg" alt="Forming an LLC" loading="lazy"></span>
          <h3>Forming an LLC</h3>
          <p>What an LLC protects (and what it doesn&rsquo;t), the filing fee and steps in your state, registered agents, operating agreements, annual reports, and series LLCs — state by state.</p>
          <span class="go">Learn more about Forming an LLC &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 111 topics" in text, "show-all label not found"
    text = text.replace("Show all 111 topics", "Show all 112 topics", 1)
    show_pos = text.find("Show all 112 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">111 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("111 topics", "112 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 111->112")


def build_about():
    text = ABOUT.read_text()
    assert text.count("111 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("111 legal topics", "112 legal topics", 1))
    print("  about.html: 111 -> 112")


def state_index_t(state, slug, e):
    bits = [
        "forming an LLC limited liability company articles of organization "
        "certificate of formation registered agent operating agreement EIN "
        "annual report series LLC foreign LLC single-member LLC",
        f"Forming an LLC in {state}",
        f"{e['overview']}",
        f"filing fee {e['filing_fee']} {e['filing_office']}",
        f"registered agent {e['registered_agent']}",
        f"operating agreement {e['operating_agreement']}",
        f"annual report {e['annual_report']}",
        f"series LLC {e.get('series_llc', '')}",
        f"foreign LLC {e['foreign_llc']}",
        f"single member LLC {e.get('single_member', '')}",
        f"{e['legal_aid_name']}",
        "form LLC cost fee steps file state protect assets veil piercing traps",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 12079, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = e["state"]
        slug = e.get("slug") or key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Forming an LLC in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Forming an LLC",
            "t": (
                "forming-an-llc Forming an LLC? "
                "What an LLC protects (and what it doesn't), the filing fee and steps in your state, "
                "registered agents, operating agreements, annual reports, and series LLCs — state by state. "
                "LLC limited liability company articles of organization certificate of formation registered agent "
                "operating agreement EIN annual report series LLC foreign LLC single-member LLC veil piercing traps."
            ),
        }
    )
    assert len(idx) == 12130, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
        assert "llc" in (e["h"] + " " + e["t"]).lower(), "new entry lacks LLC token"
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 12079 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    assert len(d) == 50, len(d)
    data = [(k, d[k]) for k in sorted(d)]  # keys already lowercase slugs
    slugs = [(e.get("slug") or k.replace(" ", "-")) for k, e in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req_core = ["state", "overview", "filing_fee", "fee_verified_url",
                "filing_office", "filing_url", "registered_agent",
                "operating_agreement", "annual_report", "foreign_llc",
                "legal_aid_name", "legal_aid_url", "sources"]
    req_maybe_empty = ["series_llc", "single_member"]
    phone_re = re.compile(
        r"\(\d{3}\)\s*\d{3}[-.]\d{4}|\b\d{3}[-.]\d{3}[-.]\d{4}\b|"
        r"1-800-\d{3}-\d{4}|1-866-\d{3}-\d{4}|1-888-\d{3}-\d{4}|1-855-\d{3}-\d{4}|"
        r"877-\d{3}-\d{4}|800-\d{3}-\d{4}|844-\d{3}-\d{4}|866-\d{3}-\d{4}|855-\d{3}-\d{4}|"
        r"1-877-\d{3}-\d{4}|1-833-[A-Z0-9]{7}"
    )
    for k, e in data:
        for f in req_core + req_maybe_empty:
            assert f in e, f"{k}: missing {f}"
        assert all(e[f] for f in req_core if f != "sources"), f"{k}: empty core field"
        assert e["sources"] and len(e["sources"]) >= 1, f"{k}: fewer than 1 source"
        blob = json.dumps({f: e[f] for f in req_core + req_maybe_empty if f != "sources"})
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before protecting-kids-online; SBB pointer)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
