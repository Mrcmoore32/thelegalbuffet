#!/usr/bin/env python3
"""Build Topic #86: Carry permit reciprocity & travel — standalone section
on all 50 state pages.

Inserts one new section per state page (before Appealing a civil
judgment, newest-first), a contents-list entry, a homepage helper
option + topic card (second grid, after Appealing a civil judgment),
bumps About 84 -> 85, and appends 50 state entries + 1 helper entry
to assets/search-index.json (10702 -> 10753).

MERGE: every state page already carries a buried
<div class="reciprocity-detail"> inside Gun Laws plus a stub
"Reciprocity" resource card (~12 words). This build PROMOTES the
buried content into the new standalone section and REMOVES both the
buried div and the stub card from Gun Laws. Other buried divs in Gun
Laws (permit-renewal, private-transfer) stay untouched. Because of
the merge, validate_topic.py check 3 (zero tokens lost vs HEAD) will
FAIL by design; the loss must be confined to exactly those two
blocks (verified separately by check_merge.py).

Data: hidden_files/topic-research/carry-permit-reciprocity/all-states.json
(coordinator-built 2026-11-14 from the buried divs on disk + web
research; verification notes in build_dataset.py).

Coordinator verification before the build (Nov 14, 2026):
- Headline figures spot-verified: 29 permitless states; 10 states
  honor no out-of-state permits (CA, CT, HI, IL, MD, MA, NJ, NY, OR,
  RI); 3 permit-required states honor every state's permit (MI
  resident-only, NC, VA); 8 states publish a named list (CO 34, DE
  21, MN 33, NV 28, NM 20, PA 31, WA 10, WI 45). Honored-in counts
  cross-checked against the buried lists (list length == count).
- WV permitless age corrected 21 -> 18 (HB 4106, eff. June 12,
  2026; official WV AG handbook, July 2026). The buried WV div's
  "21" is outdated.
- NC still permit-required: SB 50 vetoed June 2025, Senate
  overrode, House never voted (last chances Nov 16 / Nov 30, 2026).
  The "took effect Dec 1, 2025" claim is wrong.
- VA SB 115 (Chapter 879, 2026 Acts of Assembly): AG/State Police
  must drop non-"substantially similar" states by Dec 1, 2026; from
  July 1, 2027 VA residents can no longer carry on another state's
  permit. The VSP page still listed all 50 states when checked
  Oct 8, 2026. VA card carries a dated CHANGING SOON callout.
- MT non-resident NO confirmed (MT DOJ; MCA 45-8-321). GA WCLs
  residents-only + military stationed. MS standard permits for
  non-residents holding another state's permit or military stationed;
  Enhanced is residents-only. NY source link replaced: the buried
  DEC FAQ link is off-topic; dataset uses https://gunsafety.ny.gov/
  (verified 200, already linked elsewhere on the NY page).
- The MS buried watch-out phone number (662)842-1572 is NOT carried
  into the new section (single source, not needed). No phone numbers
  are printed in this topic at all.
- Duty-to-inform buckets follow the statute-based classification,
  not the Pulled Over topic's buckets. Conflicts (CA, OK, MN, MO,
  MS, NV, TN, VA, WA, WI, WY, FL, KY, NY, OR, PA) are flagged to
  the parent for a separate Pulled Over correction; this build does
  not silently rewrite Pulled Over.
- All 50 prohibited-places lists and non-resident statuses researched
  Nov 14, 2026 against statute cites (see dataset builder). Where a
  state publishes no official source for a field, the card says so
  instead of guessing.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "carry-permit-reciprocity" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-carry-permit-reciprocity.jpg"

PERMITLESS_29 = ("Alabama, Alaska, Arizona, Arkansas, Florida, Georgia, "
    "Idaho, Indiana, Iowa, Kansas, Kentucky, Louisiana, Maine, "
    "Mississippi, Missouri, Montana, Nebraska, New Hampshire, "
    "North Dakota, Ohio, Oklahoma, South Carolina, South Dakota, "
    "Tennessee, Texas, Utah, Vermont, West Virginia, Wyoming")
HONOR_NONE_10 = ("California, Connecticut, Hawaii, Illinois, Maryland, "
    "Massachusetts, New Jersey, New York, Oregon, Rhode Island")

FOPA = ("Federal law (18 U.S.C. &sect; 926A) protects transporting a "
    "firearm through a state where you can&rsquo;t carry &mdash; if it "
    "is unloaded, locked in a container, with ammunition kept separate "
    "and not within ready reach, and you may legally possess it where "
    "your trip starts and where it ends. Treat it as pass-through "
    "protection only: keep stops to what is necessary, because a few "
    "states enforce transport rules strictly.")

DUTY_LABEL = {
    "must": "tell them right away",
    "hybrid-permitless": "it depends on whether you have a permit",
    "if-asked": "only if asked",
    "none": "no law requires you to volunteer it",
}


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def join_list(items):
    return ", ".join(items)


def section_html(s, links):
    state = s["state"]
    slug = s["slug"]
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(f'<h2 id="carry-permit-reciprocity-in-{slug}">Carry permit reciprocity &amp; travel in {esc(state)}</h2>')
    parts.append(
        "<p>Carrying a handgun across state lines is where the law gets "
        "complicated: your permit may be good in one state and worthless "
        "in the next, and the rules change without much notice. This "
        "section is the " + esc(state) + " picture as of <strong>November "
        "2026</strong> &mdash; which states honor a " + esc(state)
        + " permit, which states&rsquo; permits " + esc(state)
        + " honors, whether you can carry here without a permit, and "
        "where you still can&rsquo;t carry even with one. The lists "
        "below are dated, because reciprocity lists change: check the "
        "attorney general&rsquo;s current list for every state on your "
        "route before you travel. This is general information, not "
        "legal advice.</p>"
    )
    if s["special"]:
        parts.append(f"<p><strong>{esc(s['special'])}</strong></p>")
    # --- Card 1: which states honor your permit ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Which states honor your permit</h3>")
    kind = s["inbound_kind"]
    if kind == "permitless":
        parts.append(
            "<p><strong>No permit needed.</strong> " + esc(state)
            + " lets anyone " + esc(s["permitless_age"])
            + " or older who can legally possess a firearm carry a "
            "concealed handgun here &mdash; resident or visitor, no "
            "permit required."
            + (f" {esc(s['permitless_note'])}" if s["permitless_note"] else "")
            + (f" {esc(s['inbound_note'])}" if s["inbound_note"] else "")
            + "</p>"
        )
    elif kind == "every":
        parts.append(f"<p>{esc(s['inbound_note'])}</p>")
    elif kind == "none":
        extra = ""
        if slug == "new-york":
            extra = (" Carrying a handgun here requires a New York "
                "license, and New York licenses are tied to a New York "
                "county of residence or employment &mdash; in practice, "
                "visitors cannot carry.")
        parts.append(
            "<p><strong>" + esc(state) + " honors no out-of-state carry "
            "permits at all.</strong>" + extra + " Leave the gun home, "
            "or use the locked-transport rules below.</p>"
        )
    else:  # list
        parts.append(
            "<p><strong>" + esc(state) + " honors carry permits from "
            "these " + str(s["honors_count"]) + " states:</strong></p>"
        )
        parts.append(f"<p>{esc(join_list(s['honors_list']))}.</p>")
        if s["honors_fine_print"]:
            parts.append(
                "<p><strong>Fine print:</strong> "
                + esc(s["honors_fine_print"]) + "</p>"
            )
    if s["honored_in_count"] is None:
        parts.append(
            "<p>Vermont has never issued carry permits, so there is no "
            "Vermont permit for other states to honor. If you live in "
            "Vermont and want to carry while travelling, the usual route "
            "is a nonresident permit from a state that issues them "
            "&mdash; check that state&rsquo;s page for its rules. In "
            "the permitless states listed below, you need no permit at "
            "all.</p>"
        )
    else:
        parts.append(
            "<p><strong>Honored in " + str(s["honored_in_count"])
            + " states:</strong> " + esc(join_list(s["honored_in_list"]))
            + ".</p>"
        )
        if s["honored_in_fine_print"]:
            parts.append(
                "<p><strong>Watch the fine print:</strong> "
                + esc(s["honored_in_fine_print"]) + "</p>"
            )
    parts.append(
        "<p>Lists above assume a permit issued by your home state "
        "&mdash; some states honor only resident permits, and if you "
        "move, your new state will expect you to get its permit.</p>"
    )
    parts.append(
        "<p><strong>No permit needed in 29 states:</strong> "
        + PERMITLESS_29 + " &mdash; these states let any eligible adult "
        "carry concealed without a permit. Age and eligibility rules "
        "differ from state to state, so check the state before you go.</p>"
    )
    parts.append(
        "<p><strong>These states honor no out-of-state permits:</strong> "
        + HONOR_NONE_10 + ". Leave the gun home, or use the "
        "locked-transport rules below.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Before you travel, "
        "check the attorney general&rsquo;s current list for every "
        "state on your route &mdash; the lists on this page are dated "
        "November 2026, and a state can drop recognition with little "
        "notice.</p>"
    )
    parts.append("</div>")
    # --- Card 2: permitless carry ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Permitless carry in {esc(state)}</h3>")
    if s["permitless"]:
        parts.append(
            "<p><strong>Yes &mdash; no permit needed.</strong> Anyone "
            + esc(s["permitless_age"]) + " or older who can legally "
            "possess a firearm may carry a concealed handgun in "
            + esc(state) + " without a permit, resident or visitor."
            + (f" {esc(s['permitless_note'])}" if s["permitless_note"] else "")
            + "</p>"
        )
        parts.append(
            "<p><strong>Okay, so what do I do?</strong> You still have "
            "to follow " + esc(state) + "&rsquo;s rules on where you "
            "can&rsquo;t carry (the cards below) &mdash; permitless "
            "does not mean carry-anywhere. And a permit is still worth "
            "having: it is what other states recognize when you travel, "
            "and it exempts you from the federal Gun-Free School Zones "
            "Act near schools.</p>"
        )
    else:
        parts.append(
            "<p><strong>No &mdash; a permit is required.</strong> "
            + esc(s["permitless_note"]) + "</p>"
        )
        parts.append(
            "<p><strong>Okay, so what do I do?</strong> Carry on a "
            "permit " + esc(state) + " issues or honors &mdash; "
            "carrying without one is a crime here.</p>"
        )
    parts.append("</div>")
    # --- Card 3: traveling with a firearm ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Traveling with a firearm</h3>")
    parts.append(f"<p><strong>Passing through a state where you can&rsquo;t carry?</strong> {FOPA}</p>")
    if s["vehicle"]:
        parts.append(
            "<p><strong>A handgun in your vehicle:</strong> "
            + esc(s["vehicle"]) + "</p>"
        )
    parts.append(
        "<p><strong>Telling an officer &mdash; "
        + DUTY_LABEL[s["duty_bucket"]] + ":</strong> "
        + esc(s["duty_note"]) + "</p>"
    )
    if s["watch_out"]:
        parts.append(
            "<p><strong>Watch out:</strong> " + esc(s["watch_out"]) + "</p>"
        )
    parts.append(
        "<p>For the full rules on a traffic stop &mdash; what to say, "
        "what to show, and your rights &mdash; see "
        f"<a href=\"#pulled-over-in-{slug}\">Pulled Over: Your Rights in "
        f"{esc(state)}</a> on this page.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you are stopped "
        "in another state, tell the officer you are carrying if that "
        "state&rsquo;s law requires it (check that state&rsquo;s page "
        "before you go), keep your hands visible, and do not reach for "
        "the firearm unless the officer tells you to.</p>"
    )
    parts.append("</div>")
    # --- Card 4: where you cannot carry ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Where you cannot carry even with a permit</h3>")
    parts.append(
        "<p>Even a valid permit does not open every door in "
        + esc(state) + ". The list below is the state-law list; federal "
        "law adds its own (federal buildings, post offices, secure "
        "airport areas, military installations).</p>"
    )
    parts.append("<ul>")
    for item in s["prohibited"]:
        parts.append(f"<li>{esc(item)}</li>")
    parts.append("</ul>")
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check the door "
        "before you walk in &mdash; if a place is posted or on the list "
        "above, leave the firearm locked in the vehicle (where the law "
        "allows that) or leave it home. When in doubt, ask the property "
        "owner or the staff.</p>"
    )
    parts.append("</div>")
    # --- Card 5: non-resident permit ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Getting a non-resident permit</h3>")
    status = s["nonres_status"]
    if status == "yes":
        parts.append("<p><strong>Yes.</strong> " + esc(s["nonres_note"]) + "</p>")
    elif status == "no":
        parts.append("<p><strong>No.</strong> " + esc(s["nonres_note"]) + "</p>")
    elif status == "limited":
        parts.append(
            "<p><strong>Only in limited cases.</strong> "
            + esc(s["nonres_note"]) + "</p>"
        )
    else:  # na (Vermont: no permit system at all)
        parts.append(f"<p>{esc(s['nonres_note'])}</p>")
    parts.append(
        "<p>If your home state&rsquo;s permit doesn&rsquo;t travel "
        "well, a non-resident permit from Utah, Arizona, or Florida is "
        "the usual workaround &mdash; all three issue to non-residents "
        "and are honored in dozens of states. Utah&rsquo;s permit is "
        "honored in about 36 states. Check each state&rsquo;s official "
        "reciprocity page before you rely on it.</p>"
    )
    parts.append("<ul>")
    parts.append(
        f"<li><a href=\"{esc(links['utah'])}\" target=\"_blank\" "
        f"rel=\"noopener\">Utah&rsquo;s permit-recognition page</a></li>"
    )
    parts.append(
        f"<li><a href=\"{esc(links['florida'])}\" target=\"_blank\" "
        f"rel=\"noopener\">Florida&rsquo;s permit-recognition page</a></li>"
    )
    parts.append(
        f"<li><a href=\"{esc(links['arizona'])}\" target=\"_blank\" "
        f"rel=\"noopener\">Arizona&rsquo;s permit law (A.R.S. &sect; "
        f"13-3112)</a></li>"
    )
    parts.append("</ul>")
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you live in a "
        "state whose permit travels poorly, get a non-resident Utah, "
        "Arizona, or Florida permit &mdash; but check first that the "
        "states you actually visit honor it.</p>"
    )
    parts.append("</div>")
    # --- Official links ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Official links in {esc(state)}</h3>")
    parts.append("<ul>")
    parts.append(
        f"<li><a href=\"{esc(s['source_url'])}\" target=\"_blank\" "
        f"rel=\"noopener\">{esc(s['source_label'])}</a></li>"
    )
    parts.append("</ul>")
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Check the "
        "attorney general&rsquo;s current list for every state on your "
        "route before you travel &mdash; the lists here are dated "
        "November 2026. (2) If you carry without a permit, make sure "
        "every state on your route allows it. (3) In the car, follow "
        "the vehicle rule above, and for pass-through states use the "
        "federal locked-transport rule. (4) Know where you can&rsquo;t "
        "carry before you walk in.</p>"
    )
    parts.append(
        "<p><em>Sources: the official " + esc(state) + " source linked "
        "above, checked November 14, 2026. Reciprocity lists change "
        "&mdash; the lists on this page are dated November 2026. Where "
        "an official source publishes no figure or list, this page says "
        "so instead of guessing. Laws change &mdash; confirm the "
        "current rule in the official source before you travel with a "
        "firearm. This is general information, not legal advice.</em></p>"
    )
    parts.append("</section>")
    return "\n".join(parts) + "\n"


DIV_RE = re.compile(r'<div class="reciprocity-detail">.*?</div>[ \t]*\n?', re.S)
CARD_RE = re.compile(
    r'<div class="resource">\s*<span class="r-tag">Out-of-state permits</span>\s*'
    r"<h3>Reciprocity</h3>\s*<p>.*?</p>\s*</div>",
    re.S,
)


def build_state_pages(data, links):
    for s in data:
        slug = s["slug"]
        path = STATES / f"{slug}.html"
        text = path.read_text()
        anchor = f"carry-permit-reciprocity-in-{slug}"
        assert anchor not in text, f"{slug}: anchor already present"
        # --- merge: remove the buried reciprocity-detail div ---
        divs = DIV_RE.findall(text)
        assert len(divs) == 1, f"{slug}: reciprocity-detail div count {len(divs)}"
        assert divs[0].count("<div") == 1, f"{slug}: nested div in buried block"
        text = DIV_RE.sub("", text, count=1)
        # --- merge: remove the stub Reciprocity resource card ---
        cards = CARD_RE.findall(text)
        assert len(cards) == 1, f"{slug}: stub card count {len(cards)}"
        text = CARD_RE.sub("", text, count=1)
        assert "reciprocity-detail" not in text, f"{slug}: buried div remains"
        assert "<h3>Reciprocity</h3>" not in text, f"{slug}: stub h3 remains"
        # --- insert section before Appealing a civil judgment ---
        h2 = text.find(f'<h2 id="appealing-a-civil-judgment-in-{slug}">')
        assert h2 != -1, f"{slug}: appealing h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        new_section = section_html(s, links)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the appealing <li> ---
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#appealing-a-civil-judgment-in-'
            + re.escape(slug)
            + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: appealing contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#carry-permit-reciprocity-in-{slug}">'
            f"Carry permit reciprocity &amp; travel in {s['state']}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        path.write_text(text)
        print(f"  {slug}: buried div + stub removed, section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert "carry-permit-reciprocity" not in helper_part, "index already has helper option"
    assert 'data-topic="carry-permit-reciprocity"' not in text, "index already has card"
    opt_old = (
        '<option value="appealing-a-civil-judgment" data-anchor="appealing-a-civil-judgment">'
        "Appealing a civil judgment (deadlines, de novo review, bonds)</option>"
    )
    assert opt_old in text, "appealing helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="carry-permit-reciprocity" data-anchor="carry-permit-reciprocity">'
        "Carry permit reciprocity &amp; travel (which states honor your permit, permitless carry, travel rules)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="appealing-a-civil-judgment"'
    idx = text.find(card_anchor)
    assert idx != -1, "appealing card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="carry-permit-reciprocity">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-carry-permit-reciprocity.jpg" alt="Carry permit reciprocity &amp; travel" loading="lazy"></span>
          <h3>Carry Permit Reciprocity &amp; Travel</h3>
          <p>Taking your handgun across state lines? Which states honor your permit, where you can carry without one, the federal transport rule, and where you still can&rsquo;t carry.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 39 topics" in text, "show-all label not found"
    text = text.replace("Show all 39 topics", "Show all 40 topics", 1)
    assert '<span class="count-badge">39 topics</span>' in text
    text = text.replace(
        '<span class="count-badge">39 topics</span>',
        '<span class="count-badge">40 topics</span>',
        1,
    )
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 39->40")

def build_about():
    text = ABOUT.read_text()
    assert "84 legal topics" in text, "about count not found"
    ABOUT.write_text(text.replace("84 legal topics", "85 legal topics", 1))
    print("  about.html: 84 -> 85")


def state_index_t(s):
    state = s["state"]
    slug = s["slug"]
    if s["inbound_kind"] == "list":
        inbound = f"{state} honors {s['honors_count']} states' permits"
    elif s["inbound_kind"] == "every":
        inbound = f"{state} honors every state's permit"
    elif s["inbound_kind"] == "none":
        inbound = f"{state} honors no out-of-state permits"
    else:
        inbound = f"no permit needed to carry in {state}"
    honored_in = (
        "Vermont issues no permits"
        if s["honored_in_count"] is None
        else f"honored in {s['honored_in_count']} states"
    )
    permitless = (
        f"permitless carry in {state}: yes, age {s['permitless_age']}"
        if s["permitless"]
        else f"permitless carry in {state}: no, permit required"
    )
    return (
        "carry-permit-reciprocity reciprocity "
        f"Carry permit reciprocity & travel in {state} "
        f"\u2014 {inbound}; {honored_in}; {permitless}; "
        f"duty to inform {s['duty_bucket']}; FOPA federal "
        "transport unloaded locked container ammunition "
        "separate; where you cannot carry schools "
        "courthouses bars government buildings posted "
        f"private property; non-resident permit "
        f"{s['nonres_status']} {state}"
    )


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 10702, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith("carry-permit-reciprocity-in-") for e in idx)
    for s in data:
        state = s["state"]
        slug = s["slug"]
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"carry-permit-reciprocity-in-{slug}",
                "h": f"Carry permit reciprocity & travel in {state}",
                "t": state_index_t(s),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Carry Permit Reciprocity & Travel",
            "t": (
                "carry-permit-reciprocity reciprocity "
                "Taking your handgun across state lines? Which states "
                "honor your permit, where you can carry without one, "
                "the federal transport rule, and where you still can't "
                "carry. Permitless carry FOPA duty to inform "
                "non-resident permit honored states travel rules."
            ),
        }
    )
    assert len(idx) == 10753, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 10702 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [states[k] for k in sorted(states)]
    slugs = [s["slug"] for s in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    links = {
        "utah": states["utah"]["source_url"],
        "florida": states["florida"]["source_url"],
        "arizona": states["arizona"]["source_url"],
    }
    req = [
        "state", "slug", "inbound_kind", "honors_list", "honors_fine_print",
        "honored_in_count", "honored_in_list", "honored_in_fine_print",
        "permitless", "permitless_age", "permitless_note", "duty_bucket",
        "duty_note", "vehicle", "watch_out", "prohibited", "nonres_status",
        "nonres_note", "special", "source_url", "source_label",
    ]
    phone_re = re.compile(r"\(\d{3}\)\s*\d{3}[-.]\d{4}|\b\d{3}[-.]\d{3}[-.]\d{4}\b")
    for s in data:
        for f in req:
            assert f in s, f"{s['slug']}: missing {f}"
        assert s["duty_bucket"] in ("must", "if-asked", "none", "hybrid-permitless")
        assert s["nonres_status"] in ("yes", "no", "limited", "na")
        assert s["prohibited"], f"{s['slug']}: empty prohibited list"
        assert not phone_re.search(json.dumps(s)), f"{s['slug']}: phone number in data"
    print("building state pages (merge buried div + stub, insert new section)...")
    build_state_pages(data, links)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
