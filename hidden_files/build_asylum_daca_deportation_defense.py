#!/usr/bin/env python3
"""Build Topic #94: Asylum, DACA & Deportation Defense — standalone section
on all 50 state pages.

Inserts one new section per state page (before Self-Defense & Use of Force,
newest-first), a contents-list entry (before the self-defense <li>), a
homepage helper option (after Self-Defense & Use of Force), bumps About
92 -> 93, and appends 50 state entries + 1 helper entry to
assets/search-index.json (11110 -> 11161).

The homepage topic CARD is deferred: the thumbnail
legal-buffet-asylum-daca-deportation-defense.jpg does not exist yet (image
generation failed in this session and must be re-run by the parent agent).
When the thumbnail lands, add the card + bump "Show all 47" -> 48 and the
grid badge 47 -> 48. Until then the topic is reachable from every state
page, the helper, and search — the grid counts stay at 47 so the grid stays
self-consistent.

Data: hidden_files/topic-research/asylum-daca-deportation-defense/all-states.json
(coordinator-validated 2026-11-20; all 50 legal-aid URLs curl/browser-verified
alive; the 5 phone numbers printed in state notes are second-source verified:
UT 801-382-9027, MN (651) 641-1011, NE 1-855-307-6730, WI 1-800-427-0213,
NY 1-800-566-7636. Kentucky KRM is FEE-BASED — never called "free legal
help". Delaware CLASI Immigration Unit takes victim-based cases only, so an
extra line points to Catholic Charities of Wilmington. National DACA/asylum
facts checked against uscis.gov 2026-11-20.)
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "asylum-daca-deportation-defense" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-asylum-daca-deportation-defense.jpg"

SLUG = "asylum-daca-deportation-defense"
TITLE = "Asylum, DACA & Deportation Defense"
PREV_SLUG = "self-defense-use-of-force"

# Delaware extra: CLASI's Immigration Unit takes victim-based cases only
# (U/T visas, VAWA, Special Immigrant Juvenile cases), so point readers to
# Catholic Charities of Wilmington for broader immigration help.
# (ccwilm.org verified HTTP 200, 2026-11-20.)
EXTRAS = {
    "delaware": ("Catholic Charities of Wilmington Immigration Services",
                 "https://ccwilm.org/",
                 "immigration services including DACA, family petitions, TPS, "
                 "U-visa, VAWA, and naturalization"),
}

# Phone numbers allowed anywhere in the dataset. Every one was confirmed by
# a second official source on 2026-11-20; no other phone may ship.
ALLOWED_PHONES = {
    "801-382-9027",       # UT Utah Immigration Collaborative hotline
    "(651) 641-1011",     # MN ILCM detention line
    "1-855-307-6730",     # NE Nebraska Immigration Legal Assistance Hotline
    "1-800-427-0213",     # WI Voces de la Frontera ICE hotline
    "1-800-566-7636",     # NY State Office for New Americans hotline
}


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="asylum-daca-deportation-defense-in-{slug}">Asylum, DACA &amp; deportation defense in {esc(state)}</h2>'
    )
    parts.append(
        "<p>Every year, people come to the United States seeking safety from "
        "persecution, and others who have lived here for years find themselves "
        "facing removal. This section explains the three situations most people "
        "ask about &mdash; <strong>asylum</strong>, <strong>DACA</strong>, and "
        "<strong>deportation defense</strong> &mdash; plus your rights if "
        "immigration officers come to your door, and what happens if someone is "
        "detained. Immigration law changes fast and the deadlines are strict, so "
        "treat this as a starting point: the picture here is as of "
        "<strong>November 2026</strong>, and a lawyer should check anything "
        "before you file or sign it. This is general information, not legal "
        "advice.</p>"
    )
    # --- Card 1: asylum ---
    parts.append('<div class="card">')
    parts.append("<h3>Asylum: protection from persecution</h3>")
    parts.append(
        "<p><strong>Asylum</strong> protects people who are in the United States "
        "and were persecuted &mdash; or fear they will be &mdash; because of "
        "their <strong>race, religion, nationality, membership in a particular "
        "social group, or political opinion</strong>. You apply on Form I-589, "
        "Application for Asylum and for Withholding of Removal. There are two "
        "paths: <strong>affirmative</strong> asylum, where you apply to U.S. "
        "Citizenship and Immigration Services (USCIS) and are interviewed by an "
        "asylum officer, and <strong>defensive</strong> asylum, where you ask an "
        "immigration judge for asylum as a defense in removal proceedings.</p>"
    )
    parts.append(
        "<p>The deadline matters more than almost anything else: you must file "
        "Form I-589 <strong>within one year of arriving</strong> in the United "
        "States. There are narrow exceptions for changed circumstances and "
        "extraordinary circumstances, but they are hard to win &mdash; do not "
        "count on them. If you are granted asylum, you may stay in the United "
        "States, you are authorized to work right away, you can petition to bring "
        "your spouse and unmarried children under 21 (Form I-730, within two "
        "years of the grant), and you can apply for a green card one year after "
        "the grant.</p>"
    )
    parts.append(
        "<p>While your asylum case is pending, you can apply for a work permit "
        "(Form I-765) <strong>150 days</strong> after you file for asylum, but "
        "you cannot receive it until your case has been pending <strong>180 "
        "days</strong> &mdash; the 180-day asylum clock. Delays that you cause, "
        "like asking to reschedule an interview, stop the clock.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you fear persecution, file "
        "Form I-589 within a year of arrival and keep proof of the date you "
        "arrived. Get a lawyer before you file &mdash; a mistake on the "
        "application, or a detail left out, can hurt the case. Do not travel "
        "outside the United States while your case is pending unless a lawyer "
        "says it is safe: leaving can end your case.</p>"
    )
    parts.append("</div>")
    # --- Card 2: DACA ---
    parts.append('<div class="card">')
    parts.append("<h3>DACA: where it stands</h3>")
    parts.append(
        "<p><strong>DACA</strong> (Deferred Action for Childhood Arrivals) is for "
        "people who were brought to the United States as children and meet "
        "specific guidelines: they came before their 16th birthday, were under "
        "31 on June 15, 2012, have lived here continuously since June 15, 2007, "
        "are in school, graduated, have a GED, or are honorably discharged "
        "veterans, and have no felony, significant misdemeanor, or three or more "
        "other misdemeanors. DACA is <strong>not lawful status</strong> &mdash; "
        "it is a two-year pause on removal, plus permission to work.</p>"
    )
    parts.append(
        "<p>As of <strong>November 2026</strong>, the courts have left DACA in a "
        "split state: USCIS is <strong>accepting and processing renewal "
        "requests</strong>, but it is <strong>accepting but not processing "
        "first-time requests</strong>, because of a 2021 Texas court order that "
        "was extended to the DACA rule and upheld on appeal in January 2025. "
        "Current DACA grants stay valid until they expire unless they are "
        "individually terminated. About 436,000 people held DACA as of "
        "mid-2026. Renewal waits have grown from weeks to months during 2026, "
        "so file early: USCIS says to renew <strong>120 to 150 days before "
        "your DACA expires</strong>.</p>"
    )
    parts.append(
        "<p>The court fight is not over, so the rules can change. Check the "
        'current status on the <a href="https://www.uscis.gov/humanitarian/'
        'consideration-of-deferred-action-for-childhood-arrivals-daca" '
        'target="_blank" rel="noopener">USCIS DACA page</a> before you act, and '
        "do not pay anyone who promises they can get you DACA now &mdash; if you "
        "have never had it, USCIS is not processing new grants.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you have DACA, renew 120 "
        "to 150 days before it expires and never let it lapse &mdash; a gap can "
        "mean losing your work authorization. If you have never had DACA, you can "
        "file a first-time request, but USCIS will not process it right now; talk "
        "to a lawyer about whether filing makes sense for you.</p>"
    )
    parts.append("</div>")
    # --- Card 3: deportation defense ---
    parts.append('<div class="card">')
    parts.append("<h3>Deportation defense: removal proceedings</h3>")
    parts.append(
        "<p>Removal proceedings usually start with a <strong>Notice to Appear</strong> "
        "(NTA) &mdash; a paper that says why the government believes you should "
        "be removed. Your first hearing is a <strong>master calendar "
        "hearing</strong>: it is usually short, the judge explains the charges, "
        "asks whether you have a lawyer, and sets dates. The later "
        "<strong>individual hearing</strong> is where you present your case and "
        "your evidence.</p>"
    )
    parts.append(
        "<p>The defenses a judge can grant include asylum, <strong>withholding of "
        "removal</strong> (harder to win than asylum, and no path to a green "
        "card), protection under the <strong>Convention Against Torture</strong> "
        "for people likely to be tortured if returned, <strong>cancellation of "
        "removal</strong> for long-time residents with U.S. citizen or lawful "
        "permanent resident family who would suffer exceptional hardship, "
        "<strong>adjustment of status</strong> to a green card through a family "
        "member or employer if you qualify, and <strong>voluntary "
        "departure</strong> &mdash; leaving on your own instead of being ordered "
        "removed.</p>"
    )
    parts.append(
        "<p><strong>Never miss a hearing.</strong> If you do not show up, the "
        "judge can order you removed in your absence, without hearing your side. "
        "And keep your address updated with the immigration court <em>and</em> "
        "with USCIS every time you move &mdash; if a hearing notice goes to an "
        "old address, you can be ordered removed without ever knowing a hearing "
        "was scheduled. You have the right to a lawyer in immigration court, but "
        "the government does <strong>not</strong> provide one for free &mdash; "
        "you must find one yourself or through the free legal help in the state "
        "card below.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Read the Notice to Appear "
        "carefully and write down every court date. Get a lawyer before your "
        "first hearing if you possibly can. Never miss a date, and update your "
        "address with the court every time you move.</p>"
    )
    parts.append("</div>")
    # --- Card 4: know your rights with ICE ---
    parts.append('<div class="card">')
    parts.append("<h3>Know your rights with ICE</h3>")
    parts.append(
        "<p>You have the <strong>right to remain silent</strong>. You do not have "
        "to answer questions about where you were born or your immigration "
        "status, and you can say, &ldquo;I want to speak to a lawyer.&rdquo; You "
        "do not have to open your door unless immigration officers show a "
        "warrant <strong>signed by a judge</strong>. An ICE administrative "
        "warrant (Form I-200 or I-205) does <strong>not</strong> authorize entry "
        "into your home &mdash; ask them to slide the paper under the door and "
        "look for a judge&rsquo;s signature and your correct name and address.</p>"
    )
    parts.append(
        "<p><strong>Do not sign anything</strong> without a lawyer. Signing can "
        "mean giving up your right to a hearing or agreeing to leave the country. "
        "You do not have to consent to a search of your home, car, or phone. If "
        "you are stopped, stay calm, do not run, do not lie, and do not hand "
        "over false documents. You can ask, &ldquo;Am I free to go?&rdquo;</p>"
    )
    parts.append(
        "<p>Memorize two things: your lawyer&rsquo;s phone number and your "
        "&ldquo;A-number&rdquo; (alien number, on your immigration papers). Keep "
        "copies of your immigration papers with a trusted person, not only at "
        "home, and make a plan now &mdash; who to call, where your papers are, "
        "and who picks up your children &mdash; before anything happens.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Make the plan today: write "
        "down your lawyer&rsquo;s number and your A-number, keep copies of your "
        "papers somewhere safe, and tell your family the plan. If officers come "
        "to the door, ask for a judge-signed warrant, say you want a lawyer, and "
        "do not sign anything.</p>"
    )
    parts.append("</div>")
    # --- Card 5: detention & bond ---
    parts.append('<div class="card">')
    parts.append("<h3>Detention &amp; bond</h3>")
    parts.append(
        "<p>If immigration officers detain someone, you can find where they are "
        'held with the <a href="https://locator.ice.gov/odls/" target="_blank" '
        'rel="noopener">ICE Online Detainee Locator</a> &mdash; you need their '
        "A-number and country of birth. Many detained people can ask an "
        "immigration judge for a <strong>bond hearing</strong> to be released "
        "while their case continues; the judge sets an amount, and family or a "
        "bond company can post it. Some people are subject to mandatory "
        "detention because of certain criminal convictions and cannot get bond.</p>"
    )
    parts.append(
        "<p>Detention can last months. The first days matter most: getting a "
        "lawyer quickly, and asking for a bond hearing, can change the whole "
        "case. Do not sign voluntary departure papers in detention without a "
        "lawyer &mdash; signing can end the chance to fight the case.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If someone you love is "
        "detained, find them on the locator, call the free legal help in the "
        "state card below right away (several states have hotlines for detained "
        "people), and get a lawyer to request a bond hearing. Do not let them "
        "sign anything first.</p>"
    )
    parts.append("</div>")
    # --- Card 6: what it does not cover ---
    parts.append('<div class="card">')
    parts.append("<h3>What this topic does not cover</h3>")
    parts.append(
        "<p>Asylum and DACA are <strong>not a path to citizenship by "
        "themselves</strong> &mdash; only a green card leads to citizenship, and "
        "for people granted asylum that means applying one year after the grant. "
        "Immigration court is <strong>civil, not criminal</strong>, so there is "
        "no free public defender. And a removal order is not the end of every "
        "case &mdash; appeals to the Board of Immigration Appeals and, in some "
        "situations, to a federal court exist, but they have short deadlines, "
        "sometimes 30 days.</p>"
    )
    parts.append(
        "<p><strong>Watch out for notario fraud.</strong> In many Latin American "
        "countries a &ldquo;notario&rdquo; is a lawyer. In the United States a "
        "notary public is <strong>not</strong> a lawyer and cannot give "
        "immigration legal advice. Only a licensed attorney or a "
        "Department of Justice&ndash;accredited representative may represent you "
        "in immigration court or before USCIS. Never pay someone who guarantees "
        "a result, says they have a special connection inside USCIS, or asks you "
        "to lie on a form.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Get help only from a licensed "
        "immigration lawyer or an accredited representative &mdash; the free "
        "legal help in the state card below can check credentials. Keep a copy "
        "of everything you file and every paper you receive.</p>"
    )
    parts.append("</div>")
    # --- Card 7: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Asylum, DACA &amp; deportation defense in {esc(state)}</h3>")
    if e["has_court_in_state"]:
        parts.append(
            f"<p><strong>Immigration court:</strong> the {esc(e['immigration_court'])} "
            f"in {esc(e['court_city'])} hears removal cases for {esc(state)}.</p>"
        )
    elif slug == "new-mexico":
        parts.append(
            "<p><strong>Immigration court:</strong> New Mexico has no "
            "non-detained immigration court &mdash; hearings for New Mexico "
            "residents take place at the El Paso Immigration Court in El Paso, "
            "Texas. (A detained-only court sits at Otero in Chaparral.)</p>"
        )
    else:
        parts.append(
            f"<p><strong>Immigration court:</strong> {esc(state)} has no "
            f"immigration court of its own &mdash; cases are heard at the "
            f"{esc(e['immigration_court'])} in {esc(e['court_city'])}.</p>"
        )
    fee_based = "fee-based" in (e["state_note"] or "")
    label = "Legal help" if fee_based else "Free legal help"
    parts.append(
        f"<p><strong>{label}:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
    )
    if fee_based:
        parts.append(
            "<p>This program charges fees for its immigration legal services "
            "&mdash; ask about the cost up front before you start.</p>"
        )
    extra = EXTRAS.get(slug)
    if extra:
        parts.append(
            f"<p><strong>Also:</strong> "
            f'<a href="{esc(extra[1])}" target="_blank" rel="noopener">{esc(extra[0])}</a> '
            f"&mdash; {esc(extra[2])}. Note: the legal aid above (CLASI) takes "
            "victim-based immigration cases only (U/T visas, VAWA, and Special "
            "Immigrant Juvenile cases).</p>"
        )
    if e["state_note"]:
        parts.append(f"<p>{esc(e['state_note'])}</p>")
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Call the legal help above "
        "&mdash; most of these programs help with asylum, DACA renewals, and "
        "removal defense, and they can tell you whether you qualify for free "
        "help. If someone is detained, say so on the first call: detention "
        "cases move fastest. For the step after a green card, see the "
        f'<a href="#naturalization-in-{slug}">Becoming a U.S. citizen</a> '
        "section on this page.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) If you fear persecution, "
        "file Form I-589 within one year of arriving &mdash; that deadline is "
        "strict. (2) If you have DACA, renew 120 to 150 days before it expires. "
        "(3) If you get a Notice to Appear, write down every court date, never "
        "miss one, and get a lawyer before the first hearing. (4) If immigration "
        "officers come to your door, ask for a judge-signed warrant, say you want "
        "a lawyer, and do not sign anything. (5) If someone is detained, find "
        "them on the ICE locator and call the legal help above right away. "
        "(6) Get help only from a licensed immigration lawyer or an accredited "
        "representative &mdash; never a notario. (7) If you are arrested, see the "
        f'<a href="#what-to-do-if-youre-arrested-in-{slug}">What to do if '
        "you&rsquo;re arrested</a> section on this page.</p>"
    )
    parts.append(
        "<p><em>Sources: U.S. Citizenship and Immigration Services (USCIS) asylum "
        "and DACA pages, the Executive Office for Immigration Review court list, "
        "and the legal-aid organizations linked in the research for this section, "
        "checked November 20, 2026. Immigration law and court orders change "
        "quickly &mdash; confirm the current rules with a lawyer before you rely "
        "on them. This is general information, not legal advice.</em></p>"
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
            f"Asylum, DACA &amp; deportation defense in {state}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        assert text.count(f'id="{SLUG}-in-{slug}"') == 1, f"{slug}: anchor count"
        assert text.count("<div") - before.count("<div") == 7, f"{slug}: div open delta"
        assert text.count("</div>") - before.count("</div>") == 7, f"{slug}: div close delta"
        assert text.count("<div") == text.count("</div>"), f"{slug}: div imbalance"
        h2s = re.findall(r'<h2 id="([^"]+)">', text)
        assert h2s.index(f"{SLUG}-in-{slug}") == h2s.index(f"{PREV_SLUG}-in-{slug}") - 1, f"{slug}: h2 order"
        assert not re.search(r"\bNone\b", new_section), f"{slug}: leaked None in new section"
        assert "TODO" not in new_section and "FIXME" not in new_section, f"{slug}: leaked marker"
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index(card=True):
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert SLUG not in helper_part, "index already has helper option"
    assert f'data-topic="{SLUG}"' not in text, "index already has card"
    opt_old = (
        '<option value="self-defense-use-of-force" data-anchor="self-defense-use-of-force">'
        "Self-defense &amp; use of force (stand your ground, castle doctrine, duty to retreat, what to do after)</option>"
    )
    assert opt_old in text, "self-defense helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="asylum-daca-deportation-defense" data-anchor="asylum-daca-deportation-defense">'
        "Asylum, DACA &amp; deportation defense (asylum deadline, DACA renewals, removal hearings, your rights with ICE, detention and bond)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    if card:
        card_anchor = 'data-topic="self-defense-use-of-force"'
        idx = text.find(card_anchor)
        assert idx != -1, "self-defense card not found"
        card_end = text.find("</a>", idx)
        assert card_end != -1
        card_end += len("</a>")
        card_html = """
        <a class="topic-card" href="#helper" data-topic="asylum-daca-deportation-defense">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-asylum-daca-deportation-defense.jpg" alt="Asylum, DACA and deportation defense" loading="lazy"></span>
          <h3>Asylum, DACA &amp; Deportation Defense</h3>
          <p>Seeking asylum, renewing DACA, fighting a removal case, or dealing with ICE &mdash; the deadlines, the hearings, and your rights.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
        text = text[:card_end] + card_html + text[card_end:]
        assert "Show all 47 topics" in text, "show-all label not found"
        text = text.replace("Show all 47 topics", "Show all 48 topics", 1)
        show_pos = text.find("Show all 48 topics")
        assert show_pos != -1
        badge = '<span class="count-badge">47 topics</span>'
        badge_pos = text.find(badge, show_pos)
        assert badge_pos != -1, "main-grid badge not found after show-label"
        text = text[:badge_pos] + badge.replace("47 topics", "48 topics") + text[badge_pos + len(badge):]
        assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
        print("  index.html: helper option + card + counts 47->48")
    else:
        print("  index.html: helper option only — CARD DEFERRED (thumbnail missing); grid counts stay 47")
    INDEX.write_text(text)


def build_about():
    text = ABOUT.read_text()
    assert text.count("92 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("92 legal topics", "93 legal topics", 1))
    print("  about.html: 92 -> 93")


def state_index_t(state, slug, e):
    court_line = (
        f"{e['immigration_court']} in {e['court_city']}"
        if e["has_court_in_state"]
        else f"no immigration court in state nearest {e['immigration_court']} {e['court_city']}"
    )
    bits = [
        "asylum daca deportation defense removal proceedings immigration court",
        f"Asylum, DACA & deportation defense in {state}",
        "asylum Form I-589 within one year of arrival race religion nationality particular social group political opinion affirmative defensive",
        "DACA renewals processed first time requests accepted not processed renew 120 to 150 days before expiry not lawful status",
        "Notice to Appear master calendar hearing individual hearing never miss a hearing asylum withholding cancellation of removal voluntary departure",
        "know your rights ICE remain silent judge signed warrant do not sign anything right to a lawyer",
        "detention bond ICE locator A-number bond hearing",
        "notario fraud only licensed attorney or accredited representative",
        court_line,
        f"{e['state_note'] or ''}",
        f"{e['legal_aid_name']}",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11110, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Asylum, DACA & deportation defense in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Asylum, DACA & Deportation Defense",
            "t": (
                "asylum-daca-deportation-defense asylum DACA deportation defense "
                "Asylum, DACA & Deportation Defense? Seeking asylum, renewing "
                "DACA, fighting a removal case, or dealing with ICE — the "
                "deadlines, the hearings, and your rights. Form I-589 one year "
                "deadline DACA renewals removal hearings Notice to Appear judge "
                "signed warrant detention bond ICE locator notario fraud."
            ),
        }
    )
    assert len(idx) == 11161, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11110 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [(k, states[k]) for k in sorted(states)]
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    thumb_exists = THUMB.exists()
    if not thumb_exists:
        print("WARNING: thumbnail missing — homepage card deferred until "
              "legal-buffet-asylum-daca-deportation-defense.jpg is generated")
    req = [
        "immigration_court", "court_city", "has_court_in_state",
        "legal_aid_name", "legal_aid_url", "state_note", "sources",
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
        assert e["immigration_court"] and e["court_city"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"], f"{k}: empty required field"
        assert isinstance(e["has_court_in_state"], bool), f"{k}: has_court_in_state not bool"
        assert e["state_note"], f"{k}: empty state_note"
        for m in phone_re.findall(json.dumps(e)):
            assert m in ALLOWED_PHONES, f"{k}: unverified phone {m}"
        # KY fee-based flag must stay attached to its note
        if k == "kentucky":
            assert "fee-based" in e["state_note"], "kentucky: fee-based note lost"
    print("building state pages (insert before self-defense-use-of-force section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index(card=thumb_exists)
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
