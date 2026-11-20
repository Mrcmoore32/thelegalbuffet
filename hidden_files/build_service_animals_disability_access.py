#!/usr/bin/env python3
"""Build Topic #105: Service Animals & Disability Access (ADA public
access) — standalone section on all 50 state pages.

Inserts one new section per state page (before Rideshare Accidents,
newest-first), a contents-list entry (before the rideshare-accidents
<li>), a homepage helper option + topic card (after Rideshare
Accidents), bumps About 103 -> 104, and appends 50 state entries +
1 helper entry to assets/search-index.json (11671 -> 11722).

Data: hidden_files/topic-research/service-animals-disability-access/all-states.json
(coordinator-merged 2026-11-20 from 5 research batches; session files
recovered from the researchers' agent dirs after the handoff carried
only 2 of 5 payloads in full).
URL verification 2026-11-20: 83/100 curl 200; 17 confirmed alive by
text fetch or search-result verification (AL agency, AR agency, ID
legal aid, IA legal aid, KS agency, LA agency, MA agency, MA legal
aid, NV agency, NH agency, NY agency, OR legal aid, SC legal aid,
TN agency, TX agency, WV legal aid, WY agency). No phone numbers in
the dataset (Oregon's "839-006-0345" is OAR 839-006-0345, a rule
citation, not a phone number).
Dataset corrections by the coordinator (all verified Nov 20):
- ALABAMA agency was fabricated by the researcher ("Alabama Human
  Rights Commission", hrc.alabama.gov — domain does not resolve).
  Alabama has NO state agency that accepts discrimination charges
  (confirmed by multiple sources); entry now follows the Mississippi
  pattern, pointing to the federal ADA service-animals page.
- LOUISIANA agency moved to humanrights.la.gov (old lchrgov.com
  domain no longer resolves; new site confirmed live).
- WEST VIRGINIA legal aid moved to legalaidwv.org (old lawv.net is
  defunct; current site confirmed live).
- WYOMING agency swapped to the verified parent page
  dws.wyo.gov/dws-division/labor-standards/workers-and-job-seekers/
  (deep link 403s to curl; parent confirmed live in search results).
- TEXAS agency URL stripped of a tracking query string (base URL
  verified live by text fetch).
Headline counts (computed from the merged dataset): 37 states have a
penalty for faking a service animal — 26 criminal (misdemeanor) and
11 civil/forfeiture/fine — and 13 have no specific penalty (AK, CT,
DE, IL, IN, MD, MA, MS, NE, NJ, OH, OR, VT). 28 states cover service
animals in training. 39 states name miniature horses in the
definition. 2 states have no state human-rights agency (AL, MS).
Spot-verifications (coordinator, Nov 20, 2026, official sources):
GA HB 668 "Mara Jade Act" enacted as Act 440, eff. July 1, 2026 —
O.C.G.A. 30-4-4(b), misdemeanor of a high and aggravated nature,
fine up to $2,000 / up to 30 days (mypetcerts Nov 2026 review +
Georgia service-dog guide agree; GA hedges trimmed); WI AB 366 is a
2025 Wisconsin Act (enrolled text on docs.legis.wisconsin.gov) —
Wis. Stat. 106.52(6), forfeiture $200 first / $500 later, 20 hrs
community service option (WI hedge trimmed); SD SB 82 signed Mar 9,
2026, eff. July 1, 2026 — Class 2 misdemeanor, SDCL 22-35-9; OK HB
1178 eff. Nov 1, 2025 — misdemeanor, 4 Okla. Stat. 801(E)-(F); DE
SB 219 (2024) did NOT pass (died in committee; official bill record
shows no passage); MS Support Animal Act is Miss. Code Ann.
43-6-151 to 43-6-155 only — no 43-6-157 exists (HB 1130, 2000);
NE LB 491 (2017) was introduced but never enacted — current
28-1009.01 covers only violence/interference; ID 56-704B (eff.
July 1, 2018) is the public-access misrepresentation law (fine up
to $500 first offense) while 18-5811A is the separate false
disability-benefits-claim offense — Idaho entry rewritten to say so.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "service-animals-disability-access" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-service-animals-disability-access.jpg"

SLUG = "service-animals-disability-access"
TITLE = "Service Animals & Disability Access"
PREV_SLUG = "rideshare-accidents"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="service-animals-disability-access-in-{slug}">Service animals &amp; disability access in {esc(state)}</h2>'
    )
    parts.append(
        "<p>A service animal is a dog trained to do work or perform tasks "
        "for a person with a disability — guiding, alerting, pulling a "
        "wheelchair, interrupting a PTSD episode, and more. Under the "
        "federal Americans with Disabilities Act (ADA), a business may "
        "ask you only <strong>two questions</strong> about it, may "
        "<strong>never demand papers, a vest, or a demonstration</strong>, "
        "and may <strong>never charge extra</strong>. An emotional "
        "support animal is <strong>not</strong> a service animal and has "
        "no right to enter public places — in any state. State law adds "
        "its own layers: <strong>37 states punish faking a service "
        "animal</strong> (26 as a crime, 11 with a civil fine or "
        "forfeiture) and <strong>13 have no specific penalty at all</strong>. "
        "<strong>28 states</strong> also protect service animals still "
        "in training. The picture here is as of <strong>November "
        "2026</strong>. This is general information, not legal advice.</p>"
    )
    # --- Card 1: what counts ---
    parts.append('<div class="card">')
    parts.append("<h3>What counts as a service animal — and what doesn&rsquo;t</h3>")
    parts.append(
        "<p>Under the ADA, a service animal is a <strong>dog individually "
        "trained to do work or perform tasks</strong> directly related to "
        "a person&rsquo;s disability. The task is what matters, not the "
        "breed, the size, or a vest. Miniature horses can also qualify in "
        "limited cases, as a reasonable modification. Some states write a "
        "wider definition of their own — Illinois and Michigan, for "
        "example, name miniature horses in state law, and a few states "
        "cover other trained animals — but the ADA floor is dogs.</p>"
    )
    parts.append(
        "<p>What does <strong>not</strong> count: an emotional support "
        "animal, a therapy animal, or a comfort animal. If the animal "
        "only provides comfort, companionship, or crime deterrence, it is "
        "not a service animal, no matter what a vest, a certificate, or a "
        "letter bought online says. There is no official service-animal "
        "registry, no required ID card, and no certification a business "
        "can ask to see.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If your dog is trained "
        "to do a specific task for your disability, that is what makes it "
        "a service animal — be ready to name the task, not to show a "
        "document. If your animal only comforts you, do not present it as "
        "a service animal in a store or restaurant; the housing rules "
        "below are different.</p>"
    )
    parts.append("</div>")
    # --- Card 2: the two questions ---
    parts.append('<div class="card">')
    parts.append("<h3>The two questions — the only ones a business may ask</h3>")
    parts.append(
        "<p>When it is not obvious what service the animal provides, staff "
        "may ask only two questions: <strong>(1) Is this a service animal "
        "required because of a disability?</strong> and <strong>(2) What "
        "work or task has the animal been trained to perform?</strong> "
        "They may not ask about your disability, demand medical "
        "documentation, require a special ID or vest, ask the animal to "
        "demonstrate its task, or charge a fee or deposit. A service "
        "animal can be asked to leave only if it is out of control and "
        "the handler does not control it, it is not housebroken, or it "
        "poses a direct threat — and even then, the person must be "
        "allowed back without the animal. You are liable for any damage "
        "the animal causes.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If a business asks for "
        "papers or a vest, say plainly: &ldquo;Under the ADA you may only "
        "ask whether this is a service animal and what task it performs. "
        "I am not required to show documentation.&rdquo; Note the date, "
        "the place, and who refused you, and contact the agency in your "
        "state&rsquo;s card below — in many states, denying access is "
        "itself a crime or a civil violation with a fine.</p>"
    )
    parts.append("</div>")
    # --- Card 3: emotional support animals ---
    parts.append('<div class="card">')
    parts.append("<h3>Emotional support animals: no public access — but housing is different</h3>")
    parts.append(
        "<p>An emotional support animal (ESA) has <strong>no right to enter "
        "restaurants, stores, hotels, planes, or other public "
        "places</strong>, in any state. That is the single most "
        "misunderstood rule in this area, and it is the same everywhere: "
        "comfort and emotional support are not trained tasks.</p>"
    )
    parts.append(
        "<p>Housing is the exception. Under the federal Fair Housing Act "
        "and most state fair-housing laws, an ESA can be a "
        "<strong>reasonable accommodation</strong> to a no-pets rule — a "
        "landlord must allow the animal if you need it because of a "
        "disability, with no pet deposit or extra fee, though you are "
        "liable for damage it causes. The landlord may ask for reliable "
        "documentation of the disability-related need when it is not "
        "obvious. Several states have cracked down on fake ESA letters: "
        "Louisiana&rsquo;s 2024 law requires a real therapeutic "
        "relationship, and Kentucky and Indiana fine people who fake ESA "
        "documentation in housing.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Do not buy an online "
        "ESA letter or vest and expect it to get your animal into a "
        "restaurant — it will not, and in some states presenting one is "
        "itself penalized. For housing, ask your treating clinician for "
        "documentation of the need, keep it, and make the request to your "
        "landlord in writing.</p>"
    )
    parts.append("</div>")
    # --- Card 4: faking one ---
    parts.append('<div class="card">')
    parts.append("<h3>Faking a service animal: the penalties, state by state</h3>")
    parts.append(
        "<p><strong>37 states</strong> punish passing a pet off as a "
        "service animal. In <strong>26</strong> it is a crime, usually a "
        "misdemeanor — Kansas allows up to a year in jail and a $2,500 "
        "fine, New Hampshire up to $2,000 and a year, and Michigan up to "
        "90 days and $500. In <strong>11</strong> it is a civil fine or "
        "forfeiture — Wisconsin&rsquo;s new 2025 law sets $200 for a first "
        "violation and $500 after that, and Maine fines up to $1,000 per "
        "occurrence. <strong>13 states have no specific penalty at "
        "all</strong> — Alaska, Connecticut, Delaware, Illinois, Indiana, "
        "Maryland, Massachusetts, Mississippi, Nebraska, New Jersey, "
        "Ohio, Oregon, and Vermont — though general fraud laws can still "
        "apply. Several of these laws are brand new: Georgia&rsquo;s "
        "&ldquo;Mara Jade Act&rdquo; and South Dakota&rsquo;s law both "
        "took effect July 1, 2026, and Oklahoma&rsquo;s took effect "
        "November 1, 2025. Montana is the outlier the other way: you can "
        "only be charged after a written warning.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you see someone "
        "faking a service animal, the practical step is to tell the "
        "business — it is the business that can ask the animal to leave "
        "if it is disruptive. Do not confront the person yourself, and do "
        "not buy a fake vest or certificate: in most states that is the "
        "offense itself.</p>"
    )
    parts.append("</div>")
    # --- Card 5: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Service animals in {esc(state)}</h3>")
    parts.append(f"<p><strong>What counts:</strong> {esc(e['service_animal_def'])}</p>")
    parts.append(f"<p><strong>Going into public places:</strong> {esc(e['public_access_note'])}</p>")
    parts.append(f"<p><strong>Emotional support animals:</strong> {esc(e['esa_note'])}</p>")
    parts.append(f"<p><strong>Faking a service animal:</strong> {esc(e['misrepresentation_penalty'])}</p>")
    parts.append(f"<p><strong>In housing:</strong> {esc(e['housing_note'])}</p>")
    parts.append(f"<p><strong>The law:</strong> {esc(e['state_statute'])}</p>")
    parts.append(
        f"<p><strong>Who to complain to:</strong> "
        f'<a href="{esc(e["agency_url"])}" target="_blank" rel="noopener">{esc(e["agency_name"])}</a>.</p>'
    )
    if e["state_note"]:
        parts.append(f"<p>{esc(e['state_note'])}</p>")
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you are denied "
        "entry, stay calm, state the two-question rule, and write down "
        "the date, place, and who refused you — then contact the agency "
        "above. If you are a business owner, train staff on the two "
        "questions and never ask for papers: that is where most "
        "violations happen.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Know the two "
        "questions — they are the whole test for a business. (2) Never "
        "pay for a service-animal certificate, registry, or vest: none is "
        "required, and using one to fake it is a crime in 26 states. (3) "
        "If you are denied access, write down the date, place, and who "
        "refused you, and contact the agency in your state&rsquo;s card "
        "above. (4) For housing, make the request in writing with your "
        "clinician&rsquo;s documentation. (5) If the animal is a "
        "legitimate service animal in training, check your state&rsquo;s "
        "card — 28 states protect trainers too.</p>"
    )
    parts.append(
        "<p><em>Sources: the official state service-animal statutes, "
        "state civil-rights agencies, and legal aid organizations linked "
        "in the research for this section, checked November 20, 2026. "
        "Several of these laws changed in 2025 and 2026, so the date "
        "decides which version applies. Two states — Alabama and "
        "Mississippi — have no state human-rights agency, so complaints "
        "there go to the U.S. Department of Justice. Confirm the current "
        "law with a local attorney before you rely on it. This is general "
        "information, not legal advice.</em></p>"
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
            f"Service animals in {state}</a></li>\n"
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
    opt_old = (
        '<option value="rideshare-accidents" data-anchor="rideshare-accidents">'
        "Rideshare accidents (Uber/Lyft) — whose insurance pays, the three app periods, and your state's deadline</option>"
    )
    assert opt_old in text, "rideshare helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="service-animals-disability-access" data-anchor="service-animals-disability-access">'
        "Service animals &amp; disability access (ADA) — what counts as a service animal, the two questions a business may ask, emotional support animals, and faking one</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="rideshare-accidents"'
    idx = text.find(card_anchor)
    assert idx != -1, "rideshare card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="service-animals-disability-access">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-service-animals-disability-access.jpg" alt="Service Animals &amp; Disability Access" loading="lazy"></span>
          <h3>Service Animals &amp; Disability Access</h3>
          <p>Can a restaurant ask for your service dog&rsquo;s papers? (No.) What counts as a service animal, what an emotional support animal can and can&rsquo;t do, the two questions a business may ask, and what happens if someone fakes one &mdash; state by state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 58 topics" in text, "show-all label not found"
    text = text.replace("Show all 58 topics", "Show all 59 topics", 1)
    show_pos = text.find("Show all 59 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">58 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("58 topics", "59 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 58->59")


def build_about():
    text = ABOUT.read_text()
    assert text.count("103 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("103 legal topics", "104 legal topics", 1))
    print("  about.html: 103 -> 104")


def state_index_t(state, slug, e):
    bits = [
        "service animals disability access ADA emotional support animals ESA public access",
        f"Service animals & disability access in {state}",
        f"what counts as a service animal {e['service_animal_def']}",
        f"public access {e['public_access_note']}",
        f"emotional support animals {e['esa_note']}",
        f"faking a service animal misrepresentation penalty {e['misrepresentation_penalty']}",
        f"housing {e['housing_note']}",
        f"{e['state_statute']}",
        f"{e['agency_name']}",
        f"{e['state_note'] or ''}",
        f"{e['legal_aid_name']}",
        "two questions business may ask no documentation no vest no extra charge",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11671, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Service animals & disability access in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Service Animals & Disability Access",
            "t": (
                "service-animals-disability-access Service Animals & Disability Access? "
                "Can a restaurant ask for your service dog's papers? (No.) What counts as a service animal, "
                "what an emotional support animal can and can't do, the two questions a business may ask, and "
                "what happens if someone fakes one — state by state. "
                "service animal ADA disability access emotional support animal ESA public access two questions "
                "misrepresentation penalty housing reasonable accommodation miniature horse service dog in training."
            ),
        }
    )
    assert len(idx) == 11722, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11671 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    assert len(d) == 50, len(d)
    data = [(k, d[k]) for k in sorted(d)]  # keys already lowercase
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "service_animal_def", "public_access_note", "esa_note",
        "misrepresentation_penalty", "housing_note", "state_statute",
        "agency_name", "agency_url", "legal_aid_name", "legal_aid_url",
        "state_note", "sources",
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
        assert e["service_animal_def"] and e["public_access_note"] and e["esa_note"] and e["misrepresentation_penalty"] and e["housing_note"] and e["state_statute"] and e["agency_name"] and e["agency_url"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"], f"{k}: empty required field"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        # Oregon Admin. Rule 839-006-0345 is a rule citation, not a phone number.
        blob = blob.replace("839-006-0345", "OAR-CITATION")
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before rideshare-accidents section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
