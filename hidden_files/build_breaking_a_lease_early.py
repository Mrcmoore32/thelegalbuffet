#!/usr/bin/env python3
"""Build Topic #107: Breaking a Lease Early / Roommate Disputes / Rent
Control — standalone section on all 50 state pages.

Inserts one new section per state page (before Digital Assets After
Death, newest-first), a contents-list entry (before the
digital-assets <li>), a homepage helper option + topic card (after
Digital Assets), bumps About 105 -> 106, and appends 50 state
entries + 1 helper entry to assets/search-index.json (11773 -> 11824).

Data: hidden_files/topic-research/breaking-a-lease-early/all-states.json
(coordinator-merged 2026-11-20 from 5 research batches recovered from
the researchers' session files).

URL verification 2026-11-20: 68/85 curl 200; 4 curl 403 bot filters
(ID/MA/TN legal aid, LA LawHelp) + CA AG PDF curl 500 + 12 curl 000
— ALL confirmed alive by text fetch with real content. 1 real fix:
West Virginia legal aid lawv.net is defunct (confirmed in #105/#106)
-> legalaidwv.org (curl 200); WV tenant-help link dropped (same
defunct domain).

Dataset corrections by the coordinator (all verified Nov 20 against
Nolo's duty-to-rerent chart, updated Nov 18, 2026, and the statutes):
- MINNESOTA mitigation "no" -> "yes", Minn. Stat. 504B.154 (live on
  the Revisor site, curl 200).
- FLORIDA "no" -> "yes", Fla. Stat. 85.595 (duty most of the time;
  liquidated-damages-addendum exception noted).
- MASSACHUSETTS "no" -> "unsettled" (Edmands v. Rust & Richardson,
  191 Mass. 123 (1906) — case law leans yes, never squarely decided).
- GEORGIA "no" -> "unsettled" (Ga. Code 44-7-34; Peterson v. Midas
  Realty, 287 S.E.2d 61 (Ga. Ct. App. 1981)).
- MISSISSIPPI "no" -> "unsettled" (2022 commercial-lease case
  restated no duty; residential context undecided).
- MISSOURI "no" -> "limited" (Mo. Rev. Stat. 535.300 — duty only if
  the landlord uses the deposit for future rent).
- NEW HAMPSHIRE "yes" -> "unsettled" (no statute; no residential
  case on point).
- SOUTH DAKOTA "yes" -> "unsettled" (no statute or case; a court
  would likely require mitigation, undecided).
- TENNESSEE "yes" -> "limited" (URLTA counties over 75,000 only,
  Tenn. Code 66-28-507(c)).
- KENTUCKY "yes" -> "limited" (only where local gov adopted URLTA,
  Ky. Rev. Stat. 383.670).
- Cites filled for NV (118.175), NJ (Sommer v. Kridel), NC (Isbey v.
  Crews), OH (Stern v. Taft; Dennis v. Morgan).
- LOUISIANA rent control "limited" -> "no" (no statewide cap, no
  local ordinance in force, no statute expressly on point).
Headline counts (computed from the corrected dataset): landlord must
make reasonable efforts to re-rent in 39 states; no duty in 3
(Arkansas, Pennsylvania, Vermont); duty only sometimes in 3
(Kentucky, Missouri, Tennessee); unsettled in 5 (Georgia,
Massachusetts, Mississippi, New Hampshire, South Dakota). Rent
control: statewide cap in 3 (California, Oregon, Washington); local
rules in 9; no rent control in 38.
No phone numbers in the dataset.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "breaking-a-lease-early" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-breaking-a-lease-early.jpg"

SLUG = "breaking-a-lease-early"
TITLE = "Breaking a Lease Early, Roommate Disputes & Rent Control"
PREV_SLUG = "digital-assets-after-death"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def mitigation_line(e):
    v = e["landlord_mitigation"]
    cite = e.get("mitigation_cite")
    note = e.get("mitigation_note")
    if v == "yes":
        line = "<strong>Yes — the landlord must make reasonable efforts to re-rent the place</strong>, so you usually owe rent only until a new tenant moves in, not for the whole rest of the term."
    elif v == "no":
        line = "<strong>No — the landlord has no duty to look for a new tenant.</strong> You can owe rent for the rest of the term even if the place sits empty."
    elif v == "limited":
        line = "<strong>Only sometimes — the duty to re-rent applies in limited situations.</strong>"
    else:  # unsettled
        line = "<strong>The law is unsettled — no court has squarely decided whether the landlord must try to re-rent.</strong>"
    if cite:
        line += f" ({esc(cite)})"
    if note:
        line += f" {esc(note)}"
    return line


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="breaking-a-lease-early-in-{slug}">Breaking a lease early, roommate disputes, and rent control in {esc(state)}</h2>'
    )
    parts.append(
        "<p>Leaving a lease early is usually a money question, not a "
        "permission question: you can almost always leave, but the "
        "question is how much rent you still owe. In <strong>39 "
        "states</strong> the landlord has to make reasonable efforts to "
        "find a new tenant, so you usually owe rent only until someone "
        "else moves in. In <strong>3 states</strong> — Arkansas, "
        "Pennsylvania, and Vermont — the landlord has no duty to "
        "re-rent at all. In <strong>3 more</strong> the duty applies "
        "only sometimes, and in <strong>5</strong> the law is unsettled. "
        "A few situations let you leave without paying for the rest of "
        "the term at all: military orders, domestic violence, and a home "
        "that is unsafe to live in. And rent control is rare: only "
        "<strong>3 states</strong> cap rent increases statewide — "
        "California, Oregon, and Washington — while <strong>9</strong> "
        "have local rent rules and <strong>38</strong> have none. The "
        "picture here is as of <strong>November 2026</strong>. This is "
        "general information, not legal advice.</p>"
    )
    # --- Card 1: the money question ---
    parts.append('<div class="card">')
    parts.append("<h3>Leaving early: what you actually owe</h3>")
    parts.append(
        "<p>When you break a lease, the landlord&rsquo;s claim is "
        "usually the rent for the rest of the term — minus whatever the "
        "landlord collects by re-renting, and minus any early-"
        "termination fee the lease sets instead. Some leases charge a "
        "flat fee, often one to two months&rsquo; rent, and that fee is "
        "usually enforceable if you signed it. What the landlord cannot "
        "do in most states is sit on an empty apartment and bill you "
        "for every month until the term ends: the duty to mitigate — to "
        "make reasonable efforts to re-rent — cuts the bill off when a "
        "new tenant moves in. The landlord does not have to show your "
        "unit before its other empty units, and it can charge a new "
        "tenant a different rent if the market changed.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Read your lease "
        "first — look for an early-termination clause and its fee. "
        "Then give written notice, keep a copy, and keep paying rent "
        "until the day you leave so the landlord cannot add late fees "
        "to the bill. Take dated photos of the empty, clean unit when "
        "you hand back the keys. If the landlord sues for the rest of "
        "the term, the re-renting question in your state&rsquo;s card "
        "below is the first thing to raise.</p>"
    )
    parts.append("</div>")
    # --- Card 2: legal ways out ---
    parts.append('<div class="card">')
    parts.append("<h3>Ways to leave without paying for the rest of the term</h3>")
    parts.append(
        "<p><strong>Military service.</strong> Active-duty service "
        "members can end a lease under the federal Servicemembers Civil "
        "Relief Act, 50 U.S.C. 3955, with deployment or "
        "permanent-change-of-station orders — the lease ends 30 days "
        "after the next rent due date, and no early-termination fee "
        "applies. <strong>Domestic violence.</strong> Nearly every "
        "state lets a victim of domestic violence, sexual assault, or "
        "stalking end a lease early with written notice and proof such "
        "as a protection order or police report; the exact deadline and "
        "paperwork vary by state. <strong>Unlivable home.</strong> If "
        "the landlord will not fix serious health or safety problems "
        "after written notice — no heat, no water, sewage, vermin, a "
        "broken lock — the tenant may be able to leave and claim "
        "constructive eviction, though the notice period and the proof "
        "required differ by state. <strong>Landlord harassment.</strong> "
        "Lockouts and utility shutoffs are illegal in most states and "
        "can support ending the lease. Some states add more exits, "
        "such as a senior moving into care or a job transfer — see your "
        "state&rsquo;s card below.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Put everything in "
        "writing: the problem, the date, and what you asked the "
        "landlord to do, and keep copies of every notice and reply. "
        "For domestic violence, bring your proof to the landlord with "
        "the notice — do not wait for the next incident. For unlivable "
        "conditions, report the problem to the local housing or code "
        "inspector as well as the landlord, so there is an official "
        "record. Get free legal help from the organization in your "
        "state&rsquo;s card below before you stop paying rent — "
        "stopping payment first can turn a strong exit into an eviction "
        "case.</p>"
    )
    parts.append("</div>")
    # --- Card 3: roommates ---
    parts.append('<div class="card">')
    parts.append("<h3>Roommates: who owes what when someone leaves</h3>")
    parts.append(
        "<p>When two or more people sign one lease, each of them is "
        "usually liable for the <strong>whole rent</strong>, not just "
        "their share — that is called joint and several liability, and "
        "it is the rule in nearly every state. If your roommate stops "
        "paying or moves out, the landlord can collect the full rent "
        "from you, and you would have to chase the roommate separately. "
        "One roommate leaving does not end the lease for the others, "
        "and adding or removing a name from the lease needs the "
        "landlord&rsquo;s written agreement. A tenant cannot evict a "
        "roommate — only the landlord can end a tenancy, through court. "
        "If you are the one leaving, get the landlord&rsquo;s written "
        "release, or you can still be on the hook for rent after "
        "you&rsquo;re gone.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Before you move in "
        "together, write a simple roommate agreement: who pays what, "
        "what happens if someone leaves early, and who covers a "
        "missing share. If a roommate leaves, tell the landlord in "
        "writing right away and ask — in writing — for a new lease or "
        "a replacement roommate, and keep paying the full rent on time "
        "so the landlord has no reason to evict everyone. If a "
        "roommate will not pay, the free legal help in your state&rsquo;s "
        "card below can tell you whether small claims court against "
        "the roommate is worth it.</p>"
    )
    parts.append("</div>")
    # --- Card 4: rent control ---
    parts.append('<div class="card">')
    parts.append("<h3>Rent control: where it exists and where it does not</h3>")
    parts.append(
        "<p>Only <strong>three states cap rent increases statewide</strong>: "
        "California (5% plus inflation, max 10% a year), Oregon (7% "
        "plus inflation, max 10%), and Washington (7% plus inflation, "
        "max 10%, since May 2025). <strong>Nine more states</strong> "
        "have local rent rules — for example New York City&rsquo;s rent "
        "stabilization, Montgomery County in Maryland, Portland in "
        "Maine, St. Paul in Minnesota, and fair rent commissions in "
        "Connecticut. The other <strong>38 states have no rent control "
        "at all</strong>, and most of them ban cities from creating it. "
        "Even where a cap exists, it usually does not cover new "
        "buildings, single-family homes, or small landlords, and the "
        "landlord can still raise the rent between tenants or when a "
        "lease renews within the cap.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check your "
        "city&rsquo;s rules, not just the state&rsquo;s — the cap that "
        "matters is usually the local one. If an increase looks too "
        "big, ask the landlord in writing which cap it falls under and "
        "keep the notice. In fair-rent-commission states, the "
        "commission can hear a complaint that an increase is excessive. "
        "And remember: a landlord cannot raise the rent in the middle "
        "of a fixed-term lease unless the lease itself allows it.</p>"
    )
    parts.append("</div>")
    # --- Card 5: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Breaking a lease in {esc(state)}</h3>")
    parts.append(f"<p><strong>Early-termination fee:</strong> {esc(e['early_break_fee'])}</p>")
    parts.append(f"<p><strong>Must the landlord try to re-rent?</strong> {mitigation_line(e)}</p>")
    if e["break_rights"]:
        parts.append("<p><strong>Legal ways out in this state:</strong></p><ul>")
        for r in e["break_rights"]:
            parts.append(f"<li>{esc(r)}</li>")
        parts.append("</ul>")
    parts.append(f"<p><strong>Roommates:</strong> {esc(e['roommate_rules'])}</p>")
    rc = e["rent_control"]
    rc_word = {"yes": "Yes — statewide cap", "limited": "Limited — local rules only", "no": "No"}[rc]
    parts.append(f"<p><strong>Rent control:</strong> {rc_word}. {esc(e['rent_control_note'])}</p>")
    if e.get("tenant_help_url"):
        parts.append(
            f"<p><strong>State tenant-rights page:</strong> "
            f'<a href="{esc(e["tenant_help_url"])}" target="_blank" rel="noopener">Tenant rights in {esc(state)}</a>.</p>'
        )
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
    )
    parts.append(
        f"<p><strong>What to do:</strong> Read your lease for an "
        f"early-termination clause and fee before you give notice. Give "
        f"notice in writing, keep a copy, keep paying rent until you "
        f"leave, and photograph the clean, empty unit when you hand "
        f"back the keys. If the landlord claims rent for the rest of "
        f"the term, the re-renting rule above is the first thing to "
        f"raise — and get free help from the organization linked above "
        f"before you stop paying anything.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Read the lease "
        "for an early-termination clause and fee. (2) Give written "
        "notice and keep a copy. (3) If the home is unsafe or you are "
        "leaving for domestic violence or military orders, gather your "
        "proof and give notice with it. (4) Keep paying rent until you "
        "leave, photograph the empty unit, and hand back the keys in "
        "writing. (5) If the landlord bills you for the rest of the "
        "term, check the re-renting rule in your state&rsquo;s card "
        "above and get free legal help before you pay or stop paying.</p>"
    )
    parts.append(
        "<p><em>Sources: the official state landlord-tenant statutes, "
        "state attorneys general and legal aid organizations linked in "
        "the research for this section, checked November 20, 2026. "
        "Thirty-nine states require the landlord to make reasonable "
        "efforts to re-rent; Arkansas, Pennsylvania, and Vermont do "
        "not; Kentucky, Missouri, and Tennessee apply the duty only "
        "sometimes; and Georgia, Massachusetts, Mississippi, New "
        "Hampshire, and South Dakota are unsettled. Only California, "
        "Oregon, and Washington cap rent increases statewide. Confirm "
        "the current law with a local attorney before you rely on it. "
        "This is general information, not legal advice.</em></p>"
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
            f"Breaking a lease in {state}</a></li>\n"
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
    m = re.search(
        r'<option value="digital-assets-after-death" data-anchor="digital-assets-after-death">.*?</option>',
        text,
        re.S,
    )
    assert m, "digital-assets helper option not found"
    opt_old = m.group(0)
    opt_new = (
        opt_old
        + '\n<option value="breaking-a-lease-early" data-anchor="breaking-a-lease-early">'
        "Breaking a lease early — what you owe when you leave, legal ways out, roommate disputes, and rent control</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="digital-assets-after-death"'
    idx = text.find(card_anchor)
    assert idx != -1, "digital-assets card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="breaking-a-lease-early">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-breaking-a-lease-early.jpg" alt="Breaking a Lease Early, Roommate Disputes &amp; Rent Control" loading="lazy"></span>
          <h3>Breaking a Lease Early, Roommate Disputes &amp; Rent Control</h3>
          <p>Leaving a lease early is usually a money question: how much rent do you still owe, and does your landlord have to try to re-rent? Plus the legal ways out, what happens when a roommate leaves, and where rent control actually exists.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 60 topics" in text, "show-all label not found"
    text = text.replace("Show all 60 topics", "Show all 61 topics", 1)
    show_pos = text.find("Show all 61 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">60 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("60 topics", "61 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 60->61")


def build_about():
    text = ABOUT.read_text()
    assert text.count("105 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("105 legal topics", "106 legal topics", 1))
    print("  about.html: 105 -> 106")


def state_index_t(state, slug, e):
    bits = [
        "breaking a lease early termination fee roommate disputes rent control",
        f"Breaking a lease early in {state}",
        f"early termination fee {e['early_break_fee']}",
        f"landlord must try to re-rent {e['landlord_mitigation']} {e.get('mitigation_cite') or ''}",
        f"legal ways out {' '.join(e['break_rights'])}",
        f"roommates {e['roommate_rules']}",
        f"rent control {e['rent_control']} {e['rent_control_note']}",
        f"{e['legal_aid_name']}",
        "military SCRA domestic violence uninhabitable constructive eviction joint and several liability",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11773, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Breaking a lease early in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Breaking a Lease Early, Roommate Disputes & Rent Control",
            "t": (
                "breaking-a-lease-early Breaking a Lease Early, Roommate Disputes & Rent Control? "
                "Leaving a lease early is usually a money question: how much rent do you still owe, and does your "
                "landlord have to try to re-rent? Plus the legal ways out, what happens when a roommate leaves, "
                "and where rent control actually exists. "
                "early termination fee mitigation re-rent SCRA domestic violence constructive eviction roommate "
                "joint and several liability rent control California Oregon Washington 39 states."
            ),
        }
    )
    assert len(idx) == 11824, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11773 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    assert len(d) == 50, len(d)
    data = [(k, d[k]) for k in sorted(d)]  # keys already lowercase
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "early_break_fee", "landlord_mitigation", "mitigation_cite",
        "mitigation_note", "break_rights", "roommate_rules",
        "rent_control", "rent_control_note", "legal_aid_name",
        "legal_aid_url", "tenant_help_url", "sources",
    ]
    phone_re = re.compile(
        r"\(\d{3}\)\s*\d{3}[-.]\d{4}|\b\d{3}[-.]\d{3}[-.]\d{4}\b|"
        r"1-800-\d{3}-\d{4}|1-866-\d{3}-\d{4}|1-888-\d{3}-\d{4}|1-855-\d{3}-\d{4}|"
        r"877-\d{3}-\d{4}|800-\d{3}-\d{4}|844-\d{3}-\d{4}|866-\d{3}-\d{4}|855-\d{3}-\d{4}|"
        r"1-877-\d{3}-\d{4}|1-833-[A-Z0-9]{7}"
    )
    for k, e in data:
        e.setdefault("mitigation_note", None)
        for f in req:
            assert f in e, f"{k}: missing {f}"
        assert e["early_break_fee"] and e["roommate_rules"] and e["rent_control"] and e["rent_control_note"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"] and e["break_rights"], f"{k}: empty required field"
        assert e["landlord_mitigation"] in ("yes", "no", "limited", "unsettled"), f"{k}: bad mitigation value"
        assert e["rent_control"] in ("yes", "no", "limited"), f"{k}: bad rent_control value"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before digital-assets-after-death section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
