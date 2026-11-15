#!/usr/bin/env python3
"""Build Topic #85: Appealing a civil judgment — standalone section on
all 50 state pages.

Inserts one new section per state page (before Misclassification,
newest-first), a contents-list entry, a homepage helper option + topic
card (second grid, after Misclassification), bumps About 83 -> 84, and
appends 50 state entries + 1 helper entry to assets/search-index.json
(10651 -> 10702).

Data: hidden_files/topic-research/appealing-a-civil-judgment/all-states.json
(coordinator-written from browser research on 2026-11-14).

Coordinator verification before the build (Nov 14, 2026):
- HARD GATE — small-claims appeal deadlines verified against official
  court rules / statutes for every state. The buried Small Claims text
  quoted the general civil rule (MN 60 days) for the appeal deadline;
  the 60-day figure is NEVER printed as a small-claims deadline in this
  topic. Minnesota conciliation court is 21 days (Minn. R. Gen. Pract.
  521, eff. July 1, 2026), and the Minnesota card says so plainly and
  flags the buried 60-day figure as the general civil rule.
- Small-claims deadlines (verified): AL 14, AK 30, AZ none, AR 30,
  CA 30, CO 14, CT none, DE 15, FL 30, GA 30, HI none, ID 30, IL 30,
  IN 30 (15 from city/town court), IA 20, KS 14, KY 10 (notice),
  LA 15, ME 30, MD 30, MA 10 (defendant only), MI none if judge /
  7 days if magistrate, MN 21, MS 10 (CORRECTED: the 30-day figure
  came from HB 870 (2023), a bill that never became law), MO 10,
  MT 10, NE 30, NV 7 (+3 if mailed), NH 30, NJ 45, NM 15, NY 30
  (35 if mailed), NC 10, ND none, OH 30, OK 30, OR none from
  circuit court / 10 from justice court, PA 30, RI 2, SC 30, SD
  none, TN 10, TX 21, UT 28 (current statute; older 30-day rule
  PDF is stale), VT 30, VA 10 (notice; perfect within 30), WA 30,
  WV 20, WI 10/15 (commissioner) or 45/90 (judge), WY 30.
- Review type: de novo 21 states, record review 15, split 6 (IN, ME,
  MI, OR, WV, WI), no appeal 5 (AZ, CT, HI, ND, SD), claim-free 2
  (MS, NH — conflicting or silent sources; cards say "ask the clerk").
  WA is "de novo upon the record" (RCW 12.36.055(1)).
- "No appeal" states each have a second official source (AZ §22-519
  + azcourthelp; CT §52-263 + Nolo 2026 book; HI §633-28 + Small
  Claims Rule 12(b) + judiciary brochure; ND ndcourts.gov +
  trysmallclaims/Justia; SD §15-39-57 + FindLaw + Hood v. Hood).
  Alternatives printed where verified: AZ transfer 10 business days
  before hearing; CT motion to open within 4 months; HI motion to
  set aside within 10 days; ND remove within 20 days of service;
  SD remove at least 5 days before appearance.
- Fees left claim-free (single source or conflicting): ME $150/$300,
  FL ~$300, NY $30, SC $150, NV district filing fee ($97 vs $211),
  MO/MT/KS appeal fees, ND $80 removal fee, MS $5 appeal fee.
  VT fee printed as $120 with "confirm the current amount" (VTLawHelp
  Jan 2026, newer than the older Form 291's $100). OK court-reporter
  fee printed as "about $50, ask the clerk" (multiple secondaries
  agree). NJ Appellate Division Clerk phone (609-815-2950) NOT
  printed — the topic does not need it.
- Fallback links (no official URL returned by search): IL Rule 303 —
  illinoiscourts.gov Supreme Court opinion quoting the rule verbatim
  (Huber, 2014 IL 117293); OH App. R. 4 — supremecourt.ohio.gov
  opinion quoting the rule verbatim (Louden, 2009-Ohio-319); KY —
  Justia chapter 24A page; WY — FindLaw page quoting the rule;
  MS/TN/GA/UT/NM — Justia/LawServer pages quoting the statute
  verbatim; NY general (CPLR 5513) — Rosenhouse explainer (official
  nysenate.gov CPLR 5513 URL not returned); NH general (Sup. Ct.
  R. 7) — courts.nh.gov Supreme Court home page (direct Rule 7 text
  URL not returned). ND general link reuses the buried on-site link.
- No new phone numbers printed in this topic.
- Two URLs contain literal spaces exactly as already published in the
  buried links on those pages (CO Appeals Quick Guide PDF, KY RAP 3
  order PDF) — kept verbatim. HI HRS URL contains an apostrophe;
  html.escape handles it. RI D.C.R. 73 URL space percent-encoded.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "appealing-a-civil-judgment" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def review_line(s):
    court = s["sc_court"]
    r = s["sc_review"]
    if r == "de novo":
        return (
            "<strong>New trial (de novo):</strong> the " + esc(court)
            + " hears the case all over again &mdash; new evidence, new "
            "witnesses, as if the first hearing never happened."
        )
    if r == "record":
        return (
            "<strong>Record review:</strong> the " + esc(court)
            + " reads the record of what happened below and looks for "
            "legal errors. No new evidence, no new trial."
        )
    if r == "none":
        return (
            "<strong>There is no appeal from a small-claims judgment in "
            + esc(s["state"])
            + ".</strong> The alternatives are in the card below."
        )
    if r == "split":
        return (
            "<strong>It depends on the court and the case</strong> &mdash; "
            "read the card below."
        )
    if r == "claim-free":
        return (
            "<strong>Ask the clerk</strong> whether the " + esc(court)
            + " retries the case or reviews the record &mdash; the sources "
            "do not settle it."
        )
    if r == "de-novo-record":
        return (
            "<strong>De novo upon the record:</strong> the superior court "
            "re-decides the case from the record, without a new trial."
        )
    raise ValueError(f"unknown review type {r!r}")


def section_html(s):
    state = s["state"]
    slug = s["slug"]
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(f'<h2 id="appealing-a-civil-judgment-in-{slug}">Appealing a civil judgment in {esc(state)}</h2>')
    parts.append(
        "<p>Lost a civil case in " + esc(state) + "? You may be able to "
        "appeal &mdash; ask a higher court to look at the judgment. But "
        "the deadline is the whole ballgame: miss it and the judgment "
        "stands, however strong your argument is. The deadlines below are "
        "the ones the court rules and statutes publish for " + esc(state)
        + ", checked <strong>November 14, 2026</strong>. Small-claims "
        "appeals and general civil appeals run on different clocks in "
        "most states &mdash; do not use one for the other. This is "
        "general information, not legal advice.</p>"
    )
    # --- What appealing means ---
    parts.append('<div class="card">')
    parts.append("<h3>What appealing means</h3>")
    parts.append(
        "<p>An appeal asks a higher court to look at what the court below "
        "did. In a regular civil case, the higher court reads the record "
        "of what already happened and looks for legal errors &mdash; a "
        "wrong rule applied, evidence admitted that should not have been, "
        "a decision no reasonable judge could reach on that record. New "
        "evidence and new arguments you never made below are generally "
        "not allowed. The big exception is small claims and the lowest "
        "courts: in many states those appeals are a genuine fresh start "
        "&mdash; a trial de novo &mdash; where the case is heard all over "
        "again as if the first one never happened. The cards below say "
        "which kind your appeal is in " + esc(state) + ".</p>"
    )
    parts.append(
        "<p><strong>Who can appeal:</strong> the side that lost. In a few "
        "states the plaintiff gives up appeal rights by choosing small "
        "claims in the first place &mdash; the " + esc(state) + " card "
        "below says if that applies here.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Read the two deadline "
        "cards below first. Everything else in an appeal can be figured "
        "out after you file; the deadline cannot.</p>"
    )
    parts.append("</div>")
    # --- Small claims card ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Small claims: the deadline in {esc(state)}</h3>")
    parts.append(
        "<p><strong>Deadline: " + esc(s["sc_deadline"]) + ".</strong> "
        + review_line(s) + "</p>"
    )
    parts.append(f"<p>{esc(s['sc_text'])}</p>")
    if s["sc_review"] == "none":
        parts.append(
            "<p><strong>Okay, so what do I do?</strong> If your hearing "
            "has not happened yet, ask the clerk now about moving the case "
            "out of small claims &mdash; once judgment is entered, it is "
            "too late. If judgment has already been entered, ask the clerk "
            "about the motion described above the same week you learn of "
            "the judgment.</p>"
        )
    else:
        parts.append(
            "<p><strong>Okay, so what do I do?</strong> File the notice of "
            "appeal first, then sort out the bond and the transcript. A "
            "late notice ends the appeal; a late transcript usually does "
            "not.</p>"
        )
    parts.append("</div>")
    # --- General civil card ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Other civil cases: the deadline in {esc(state)}</h3>")
    parts.append(
        "<p><strong>Deadline: " + esc(s["gen_deadline"]) + ".</strong> "
        "Appeal to the " + esc(s["gen_court"]) + ".</p>"
    )
    parts.append(f"<p>{esc(s['gen_text'])}</p>")
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Calendar this deadline "
        "separately from the small-claims one above &mdash; they are "
        "different clocks, and using the wrong one is how appeals are "
        "lost.</p>"
    )
    parts.append("</div>")
    # --- What to file and what it costs ---
    parts.append('<div class="card">')
    parts.append("<h3>What to file and what it costs</h3>")
    parts.append(
        "<p>You start an appeal by filing a notice of appeal with the "
        "clerk of the court that decided your case (in some states, with "
        "the clerk of the court you are appealing to &mdash; the "
        + esc(state) + " cards above say which). The notice is usually a "
        "short form: who you are, what judgment you are appealing, and "
        "which court you want to hear it.</p>"
    )
    parts.append(
        "<p>What it costs: a filing fee, the cost of the transcript or "
        "record (often more than the fee), and sometimes an appeal bond. "
        "A bond &mdash; also called a supersedeas bond &mdash; guarantees "
        "the winner gets paid if you lose again, and in many states it is "
        "the only thing that stops the winner from collecting while the "
        "appeal is pending. Ask the clerk for the current fee and bond "
        "amounts on day one; the " + esc(state) + " cards give the figures "
        "the official sources publish, and where no figure is published "
        "this page says so rather than guessing.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> File the notice first, "
        "then sort out the bond and the transcript. A late notice ends "
        "the appeal; a late transcript usually does not.</p>"
    )
    parts.append("</div>")
    # --- If you won and they appeal ---
    parts.append('<div class="card">')
    parts.append("<h3>If you won and they appeal</h3>")
    parts.append(
        "<p>Filing an appeal does not automatically stop collection. In "
        "most states the winner can keep enforcing the judgment &mdash; "
        "garnishing wages, levying accounts &mdash; unless the loser gets "
        "a stay, usually by posting an appeal bond. In a few states the "
        "appeal pauses enforcement automatically. The " + esc(state)
        + " card above says what happens here.</p>"
    )
    parts.append(
        "<p>Watch for the notice of appeal &mdash; it must be served on "
        "you &mdash; and calendar the deadline to respond. Do not spend "
        "the money yet: if the higher court reverses, you may have to "
        "give it back. Keep the evidence and the judgment paperwork "
        "together; if the appeal is a trial de novo, you will present "
        "your case again.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Ask the clerk whether "
        "the appeal in your case pauses collection, and check whether a "
        "bond was posted. If no bond was posted and collection is not "
        "stayed, you can keep enforcing &mdash; but talk to the clerk or "
        "a lawyer before spending what you collect.</p>"
    )
    parts.append("</div>")
    # --- If you cannot afford the appeal ---
    parts.append('<div class="card">')
    parts.append("<h3>If you lost and cannot afford the appeal</h3>")
    parts.append(
        "<p>Most courts will waive or reduce appeal fees for people who "
        "cannot afford them &mdash; usually by filing a short form (often "
        "called in forma pauperis, a fee-waiver application, or a poverty "
        "affidavit) and showing your income. A waiver covers the filing "
        "fee; a bond is harder to waive, and in some states it cannot be "
        "waived at all. Legal aid and lawyer-referral programs (in the "
        "Free and Low-Cost Legal Help section on this page) can help with "
        "the forms, and a one-hour consultation with an appellate lawyer "
        "before the deadline is the cheapest reality check in law.</p>"
    )
    if s.get("afford_note"):
        parts.append(f"<p>{esc(s['afford_note'])}</p>")
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Ask the clerk for the "
        "fee-waiver form the same day you learn the deadline &mdash; the "
        "waiver does not extend the deadline, so file the notice first "
        "and the waiver with it.</p>"
    )
    parts.append("</div>")
    # --- Official links ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Official links in {esc(state)}</h3>")
    parts.append("<ul>")
    seen = set()
    for key in ("sc_link", "sc_link2", "gen_link"):
        url = s.get(key)
        if not url or url in seen:
            continue
        seen.add(url)
        label_key = key + "_label"
        parts.append(
            f"<li><a href=\"{esc(url)}\" target=\"_blank\" "
            f"rel=\"noopener\">{esc(s[label_key])}</a></li>"
        )
    parts.append("</ul>")
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Find your deadline "
        "in the two cards above and calendar it with days to spare. (2) "
        "File the notice of appeal with the right clerk before that date "
        "&mdash; the notice is what keeps the appeal alive. (3) Ask the "
        "clerk the same day about the filing fee, the bond, and whether "
        "filing pauses collection. (4) If you cannot afford the fee, file "
        "the fee-waiver form with the notice.</p>"
    )
    parts.append(
        "<p><em>Sources: the official " + esc(state) + " sources linked "
        "above, checked November 14, 2026. Where an official source "
        "publishes no figure for a fee, a court, or a deadline, this page "
        "says so instead of guessing. Laws change &mdash; confirm the "
        "current rule in the official source before you rely on a "
        "deadline. This is general information, not legal advice.</em></p>"
    )
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def build_state_pages(data):
    for s in data:
        slug = s["slug"]
        path = STATES / f"{slug}.html"
        text = path.read_text()
        anchor = f"appealing-a-civil-judgment-in-{slug}"
        assert anchor not in text, f"{slug}: anchor already present"
        # --- insert section before Misclassification (newest-first) ---
        h2 = text.find(f'<h2 id="misclassification-in-{slug}">')
        assert h2 != -1, f"{slug}: misclassification h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        new_section = section_html(s)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the misclassification <li> ---
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#misclassification-in-'
            + re.escape(slug)
            + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: misclassification contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#appealing-a-civil-judgment-in-{slug}">'
            f"Appealing a civil judgment in {s['state']}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert "appealing-a-civil-judgment" not in helper_part, "index already has helper option"
    assert 'data-topic="appealing-a-civil-judgment"' not in text, "index already has card"
    opt_old = (
        '<option value="misclassification" data-anchor="misclassification">'
        "Misclassification (1099 vs W-2, contractor vs employee)</option>"
    )
    assert opt_old in text, "misclassification helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="appealing-a-civil-judgment" data-anchor="appealing-a-civil-judgment">'
        "Appealing a civil judgment (deadlines, de novo review, bonds)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="misclassification"'
    idx = text.find(card_anchor)
    assert idx != -1, "misclassification card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="appealing-a-civil-judgment">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-appealing-a-civil-judgment.jpg" alt="Appealing a civil judgment" loading="lazy"></span>
          <h3>Appealing a Civil Judgment</h3>
          <p>Lost a case? The clock starts the day judgment is entered &mdash; your state&rsquo;s small-claims and general civil appeal deadlines, where to file, and what it costs.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 38 topics" in text, "show-all label not found"
    text = text.replace("Show all 38 topics", "Show all 39 topics", 1)
    assert '<span class="count-badge">38 topics</span>' in text
    text = text.replace(
        '<span class="count-badge">38 topics</span>',
        '<span class="count-badge">39 topics</span>',
        1,
    )
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 38->39")


def build_about():
    text = ABOUT.read_text()
    assert "83 legal topics" in text, "about count not found"
    ABOUT.write_text(text.replace("83 legal topics", "84 legal topics", 1))
    print("  about.html: 83 -> 84")


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 10651, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith("appealing-a-civil-judgment-in-") for e in idx)
    for s in data:
        state = s["state"]
        slug = s["slug"]
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"appealing-a-civil-judgment-in-{slug}",
                "h": f"Appealing a civil judgment in {state}",
                "t": (
                    "appealing-a-civil-judgment appeal deadlines "
                    f"Appealing a civil judgment in {state} "
                    f"\u2014 small claims appeal {s['sc_deadline']} to the "
                    f"{s['sc_court']}; general civil appeal "
                    f"{s['gen_deadline']} to the {s['gen_court']}; notice "
                    "of appeal filing fee appeal bond supersedeas stay "
                    "transcript de novo record review fee waiver in forma "
                    f"pauperis {state}"
                ),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Appealing a Civil Judgment",
            "t": (
                "appealing-a-civil-judgment appeal deadlines "
                "Lost a case? The clock starts the day judgment is "
                "entered \u2014 your state's small-claims and general "
                "civil appeal deadlines, where to file, and what it "
                "costs. Notice of appeal filing fee appeal bond "
                "supersedeas stay transcript de novo record review."
            ),
        }
    )
    assert len(idx) == 10702, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 10651 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [states[k] for k in sorted(states)]
    slugs = [s["slug"] for s in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    req = [
        "state", "slug", "sc_deadline", "sc_court", "sc_review",
        "sc_text", "sc_link", "sc_link_label", "gen_deadline",
        "gen_court", "gen_text", "gen_link", "gen_link_label",
    ]
    for s in data:
        for f in req:
            assert s.get(f), f"{s['slug']}: missing {f}"
        assert s["sc_review"] in (
            "de novo", "record", "none", "split", "claim-free",
            "de-novo-record",
        ), f"{s['slug']}: bad review {s['sc_review']}"
        assert "60 days" not in s["sc_deadline"], f"{s['slug']}: 60-day small-claims deadline"
    # hard gate: the 60-day figure must never be a small-claims deadline
    for s in data:
        if s["slug"] != "minnesota":
            assert "60 days" not in s["sc_text"], f"{s['slug']}: 60 days in small-claims text"
    print("building state pages...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
