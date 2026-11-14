#!/usr/bin/env python3
"""Build Topic #82: Probation — standalone section on all 50 state pages.

Inserts one new section per state page (before Payday / title loans,
newest-first), a contents-list entry, a homepage helper option + topic
card (second grid, after Payday / title loans), bumps About 80 -> 81,
and appends 50 state entries + 1 helper entry to assets/search-index.json
(10498 -> 10549).

Data: hidden_files/topic-research/probation/all-states.json
(coordinator-written from hidden_files/topic-research/probation/
buried-extract.json, which reuses verbatim the per-state "Probation in
{State}" cards and official-source links from the buried probation
cluster inside Wrongly Accused on each state page — those were built
from official state sources. The buried block stays where it is; this
section is the full topic and cross-references Wrongly Accused instead
of duplicating it.)

Coordinator verification before the build (Nov 14, 2026):
- Per-state delivery / violations / early-termination / fee text reused
  verbatim from the buried cards: violations for 17 states, early
  termination for 19, fees for 11. Every other state gets a claim-free
  fallback for that field, not an invented rule.
- Headline general facts spot-verified against official / primary
  sources before shipping:
  * Violation hearings: due process (notice, hearing, present evidence)
    under Gagnon v. Scarpelli, 411 U.S. 778 (1973); standard is
    preponderance of the evidence — "more likely than not" — in most
    states (confirmed in the buried cards for MA, NJ, and WA).
  * Searches: Griffin v. Wisconsin, 483 U.S. 868 (1987) — warrantless
    probation search on "reasonable grounds" under a valid regulation;
    United States v. Knights, 534 U.S. 112 (2001) — reasonable
    suspicion for a search of a probationer.
  * Can't-pay: Bearden v. Georgia, 461 U.S. 660 (1983) — a court
    cannot revoke probation solely because a person cannot pay a fine
    or restitution despite bona fide efforts; it must inquire into the
    reasons and consider alternatives.
  * Interstate Compact: all 50 states plus DC, PR, and VI are members
    (ICAOS); Rule 4.107 lets the sending state charge a transfer
    application fee and the receiving state a supervision fee. Verified
    fee examples from official sources only: Oregon $50 (OAR
    291-180-0274), Louisiana $150 (La. R.S. 15:574.45), Wisconsin $150
    (Wisconsin DOC, doc.wi.gov). No other per-state transfer fee is
    printed.
- No phone numbers are printed anywhere in this topic.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "probation" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def violations_block(s):
    state = s["state"]
    if s.get("violations"):
        return (
            "<p><strong>In " + esc(state) + ":</strong> " + esc(s["violations"]) + "</p>"
        )
    return (
        "<p><strong>No " + esc(state) + "-specific violation process is "
        "printed in this section</strong> &mdash; the official sources "
        "checked do not lay out this state&rsquo;s hearing steps in plain "
        "terms. The general pattern above still applies: your officer "
        "files a report with the sentencing court, the court holds a "
        "hearing, and the judge decides. Ask your officer or the court "
        "clerk for the local violation-hearing procedure before your "
        "hearing date.</p>"
    )


def early_block(s):
    state = s["state"]
    if s.get("early"):
        return (
            "<p><strong>In " + esc(state) + ":</strong> " + esc(s["early"]) + "</p>"
        )
    return (
        "<p><strong>No " + esc(state) + "-specific early-termination rule "
        "is printed in this section</strong> &mdash; the official sources "
        "checked do not describe a published early-termination or "
        "earned-discharge process for " + esc(state) + ". That does not "
        "mean the court cannot end probation early: in many states the "
        "sentencing court can do so on request. Ask your officer how "
        "early-termination requests are made in your court, and finish "
        "treatment, community service, and restitution first &mdash; open "
        "conditions are the most common reason requests stall.</p>"
    )


def fees_block(s):
    state = s["state"]
    if s.get("fees"):
        return (
            "<p><strong>In " + esc(state) + ":</strong> " + esc(s["fees"]) + "</p>"
        )
    return (
        "<p><strong>No " + esc(state) + "-specific fee amount is printed "
        "in this section</strong> &mdash; the official sources checked do "
        "not state this state&rsquo;s supervision-fee amount. Ask your "
        "officer for the exact monthly amount, what it covers, and where "
        "to pay it, and get it in writing. The Bearden rule below still "
        "protects you if you genuinely cannot pay.</p>"
    )


def section_html(s):
    state = s["state"]
    slug = s["slug"]
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(f'<h2 id="probation-in-{slug}">Probation in {esc(state)}</h2>')
    parts.append(
        "<p>Probation is supervision in the community instead of &mdash; or "
        "after &mdash; jail or prison. The judge suspends the sentence and "
        "lets you live at home, work, and see your family, as long as you "
        "follow the conditions in your probation order. Break a condition "
        "and the judge can send you back to serve the sentence that was "
        "hanging over the case. This section is the full picture for "
        + esc(state) + ": what probation is, the conditions, what happens "
        "if you violate, getting off early, moving to another state, the "
        "fees, your rights, and how probation ends. A shorter version of "
        "this lived inside Wrongly Accused on this page; this is the "
        "complete section. Checked <strong>November 14, 2026</strong>. "
        "This is general information, not legal advice.</p>"
    )
    # --- What probation is ---
    parts.append('<div class="card">')
    parts.append("<h3>What probation is</h3>")
    parts.append(
        "<p>When a judge grants probation, the judge usually imposes a "
        "sentence and then <strong>suspends</strong> it &mdash; the "
        "sentence is hanging over the case, not being served, as long as "
        "you stay in compliance. You are assigned a <strong>probation "
        "officer</strong> (sometimes called a probation agent or community "
        "supervision officer) who checks that you are following your "
        "conditions, reports to the court, and can ask the court to act "
        "if you are not. Probation is not the same as parole: parole "
        "follows release from prison, while probation is a sentence the "
        "court imposes instead of sending you to jail or prison in the "
        "first place. How long probation lasts depends on the charge and "
        "the judge &mdash; it can run from months to years.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Read your probation "
        "order the day you get it &mdash; every condition, every date, "
        "every dollar. Keep it somewhere you can find it, and ask your "
        "officer about anything you do not understand before you guess.</p>"
    )
    parts.append("</div>")
    # --- Standard vs special conditions ---
    parts.append('<div class="card">')
    parts.append("<h3>Standard vs. special conditions</h3>")
    parts.append(
        "<p>Almost every probation order has the same <strong>standard "
        "conditions</strong>: report to your probation officer as directed "
        "and keep every appointment, obey all laws, tell your officer "
        "before you change your address or job, and get permission before "
        "leaving the state (often the county). Your order can add "
        "<strong>special conditions</strong> for your case: drug or alcohol "
        "testing, treatment or counseling, community service, a no-contact "
        "order, staying away from certain places or people, and payments "
        "such as fines, fees, and restitution. Your own probation order "
        "controls &mdash; what it says is what you must do.</p>"
    )
    parts.append(
        "<p><strong>What your officer can and cannot do.</strong> Your "
        "officer can set your reporting schedule, visit your home or "
        "workplace, order drug tests your conditions require, require "
        "treatment or classes, and file a violation report with the court. "
        "Your officer cannot change your sentence, revoke your probation, "
        "or waive a condition the court ordered &mdash; only the judge can "
        "do those things. If a condition seems impossible or unfair "
        "&mdash; a treatment program you cannot reach, a curfew that "
        "conflicts with your work shift, a fee you cannot pay &mdash; do "
        "not just break it. Tell your officer first, in writing, explain "
        "the problem, and ask the court to change the condition. Judges "
        "change conditions far more often than people expect, but only "
        "when someone asks before the violation happens.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If a condition clashes "
        "with your job, your housing, or your ability to pay, write to "
        "your officer the same day: what the condition is, why you cannot "
        "meet it as written, and what would work instead. Keep a copy. If "
        "the officer cannot fix it, ask the court &mdash; through your "
        "officer or a lawyer &mdash; to modify the condition.</p>"
    )
    parts.append("</div>")
    # --- Violation hearing ---
    parts.append('<div class="card">')
    parts.append("<h3>If you violate: the violation hearing</h3>")
    parts.append(
        "<p>A violation can be a <strong>new arrest or new charge</strong>, "
        "or a <strong>technical violation</strong>: a missed appointment, "
        "a failed drug test, a missed payment, leaving the state without "
        "permission, or breaking a no-contact order. Either kind can land "
        "you in front of the judge. The usual pattern: your officer files "
        "a violation report or petition with the sentencing court, the "
        "court issues a summons or a warrant, and you get a hearing "
        "before the judge. Under the U.S. Supreme Court&rsquo;s decision "
        "in <em>Gagnon v. Scarpelli</em>, 411 U.S. 778 (1973), you are "
        "entitled to notice of the alleged violation and a hearing where "
        "you can present your side and the evidence that helps you. You "
        "can have a lawyer &mdash; ask the court about a public defender "
        "if you cannot afford one.</p>"
    )
    parts.append(
        "<p><strong>The standard of proof is lower than at trial.</strong> "
        "The state does not have to prove a violation beyond a reasonable "
        "doubt. In most states it only has to show by a "
        "<strong>preponderance of the evidence</strong> &mdash; that it is "
        "more likely than not that you violated a condition. That is why "
        "a violation hearing can go against you even when a new criminal "
        "charge would not. Hearsay and other evidence that would not be "
        "allowed at trial is often allowed at a violation hearing.</p>"
    )
    parts.append(
        "<p><strong>What the judge can do.</strong> The judge can warn you "
        "and continue probation as-is, add or change conditions, extend "
        "the probation term, order a short jail stay as a sanction, or "
        "revoke probation and impose the sentence that was suspended. "
        "Bring proof to the hearing: completion certificates, payment "
        "receipts, pay stubs, treatment letters, and anyone who can speak "
        "for you.</p>"
    )
    parts.append(violations_block(s))
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you miss an "
        "appointment, fail a test, or anything goes wrong, call your "
        "officer before it turns into a violation report, not after. If "
        "you get a summons or a warrant, do not ignore it &mdash; get a "
        "lawyer, gather your proof, and show up to the hearing.</p>"
    )
    parts.append("</div>")
    # --- Early termination ---
    parts.append('<div class="card">')
    parts.append("<h3>Getting off probation early</h3>")
    parts.append(
        "<p>Courts in many states can end probation early for people who "
        "have finished their conditions and stayed in compliance. The "
        "request goes to the sentencing court, and your officer&rsquo;s "
        "compliance report usually carries the most weight. Judges "
        "typically look at how much of the term you have served, whether "
        "every condition is complete, whether fines and restitution are "
        "paid, and whether you have stayed out of trouble. Some states "
        "also let you earn time off the term for compliance, which can "
        "end supervision early without a separate court request.</p>"
    )
    parts.append(early_block(s))
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Finish treatment, "
        "community service, and restitution first &mdash; open conditions "
        "are the most common reason requests stall. Then ask your officer "
        "whether they will recommend early termination, and ask the court "
        "through your officer or a lawyer. Keep proof of everything you "
        "have completed in one folder.</p>"
    )
    parts.append("</div>")
    # --- Interstate Compact ---
    parts.append('<div class="card">')
    parts.append("<h3>Moving to another state: the Interstate Compact</h3>")
    parts.append(
        "<p>All 50 states &mdash; plus the District of Columbia, Puerto "
        "Rico, and the U.S. Virgin Islands &mdash; belong to the "
        "Interstate Compact for Adult Offender Supervision (ICAOS). If "
        "you need to move, you apply through your probation officer: the "
        "state that sentenced you has the final say, the state you want "
        "to move to must accept you, and there is no right to a transfer. "
        "The receiving state will supervise you under its own rules once "
        "you are accepted, but the sentencing state keeps authority over "
        "your case. Do not move first and ask later &mdash; with limited "
        "exceptions you cannot travel to the new state while the "
        "application is pending, and moving without approval can itself "
        "be a violation.</p>"
    )
    parts.append(
        "<p><strong>Fees.</strong> Under ICAOS Rule 4.107, the sending "
        "state may charge a transfer application fee and the receiving "
        "state may charge a supervision fee. The amounts differ by state: "
        "for example, Oregon charges a $50 application fee, Louisiana "
        "charges $150, and Wisconsin charges $150. Ask your officer what "
        + esc(state) + " charges before you apply, and keep the receipt.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Tell your officer as "
        "soon as you know you may need to move &mdash; transfers take "
        "time, and the application goes through your officer, not around "
        "them. Have a real address, a job or family support, and a "
        "treatment plan (if one applies) lined up in the new state before "
        "you apply; the receiving state weighs all of that.</p>"
    )
    parts.append("</div>")
    # --- Fees and costs ---
    parts.append('<div class="card">')
    parts.append("<h3>Fees and costs</h3>")
    parts.append(
        "<p>Probation is rarely free. Most people on probation are charged "
        "a <strong>monthly supervision fee</strong>, plus the cost of drug "
        "tests, treatment or classes the court orders, and any fines and "
        "restitution from the case. The amounts are set by state law or "
        "by the court, and they add up over a long probation term &mdash; "
        "so get the full list in writing and keep every receipt.</p>"
    )
    parts.append(fees_block(s))
    parts.append(
        "<p><strong>If you cannot pay.</strong> A court cannot revoke your "
        "probation solely because you cannot pay a fine or restitution "
        "when you have genuinely tried. In <em>Bearden v. Georgia</em>, "
        "461 U.S. 660 (1983), the U.S. Supreme Court held that the court "
        "must first ask why you did not pay &mdash; if you made bona fide "
        "efforts and still could not pay through no fault of your own, "
        "the court must consider alternatives to jail, such as a payment "
        "plan, a lower amount, or community service. But a court can "
        "revoke if you willfully refused to pay when you had the money, "
        "or never tried. Tell the court early, in writing, that you "
        "cannot pay and why, and bring proof: pay stubs, bills, and a "
        "record of the jobs you applied for.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If money is tight, do "
        "not go silent and miss payments &mdash; ask your officer or the "
        "court for a payment plan, a reduced fee, or a waiver before you "
        "fall behind, and keep proof of every payment you make.</p>"
    )
    parts.append("</div>")
    # --- Your rights ---
    parts.append('<div class="card">')
    parts.append("<h3>Your rights on probation</h3>")
    parts.append(
        "<p>Probation takes away some privacy, but not all of it. Your "
        "probation order itself is a search condition in many states: "
        "your officer may be allowed to search your home, car, or person "
        "without a warrant. The U.S. Supreme Court has upheld that, but "
        "with limits &mdash; in <em>Griffin v. Wisconsin</em>, 483 U.S. "
        "868 (1987), a warrantless probation search was allowed because "
        "the officer had &ldquo;reasonable grounds&rdquo; to believe "
        "contraband was present, and in <em>United States v. Knights</em>, "
        "534 U.S. 112 (2001), the Court required reasonable suspicion for "
        "a search of a probationer. An officer still cannot search for no "
        "reason at all, and police who are not your probation officer do "
        "not get a free pass from your probation status alone.</p>"
    )
    parts.append(
        "<p><strong>If your rights are violated.</strong> Write down what "
        "happened the same day &mdash; who, when, where, what was said, "
        "and any witnesses &mdash; and keep any paperwork. Tell a lawyer "
        "right away: a lawyer can raise an illegal search at your "
        "violation hearing or in court, and can ask the court to change a "
        "condition that is being enforced unfairly. Do not argue with the "
        "officer at the door or refuse in a way that becomes a new "
        "violation; say plainly, &ldquo;I do not consent to this "
        "search,&rdquo; and let the lawyer fight it in court.</p>"
    )
    parts.append(
        "<p><strong>Getting a lawyer.</strong> You can have a lawyer at "
        "your violation hearing and when asking the court to change a "
        "condition or end probation early. If you cannot afford one, ask "
        "the court about a public defender and see the Free Legal Help "
        "section on this page for legal aid in " + esc(state) + ".</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Know your conditions "
        "word for word &mdash; they set the limits on searches and on "
        "your officer. If a search or a demand goes beyond them, say you "
        "do not consent, write it down, and call a lawyer the same day.</p>"
    )
    parts.append("</div>")
    # --- How probation ends ---
    parts.append('<div class="card">')
    parts.append("<h3>How probation ends</h3>")
    parts.append(
        "<p>Probation ends when you complete the full term and the court "
        "discharges you, when the court ends it early, or when you earn "
        "it off through a compliance-credit program where your state has "
        "one. Get the discharge in writing &mdash; a discharge order or "
        "letter from the court or your officer &mdash; and keep it with "
        "your probation order. It is the proof that supervision is over.</p>"
    )
    parts.append(
        "<p><strong>Your record after probation.</strong> Finishing "
        "probation does not erase the conviction. The case stays on your "
        "record unless you get it sealed or expunged under your "
        "state&rsquo;s record-clearing law, and not every case qualifies. "
        "See the record-clearing (expungement and sealing) section of "
        "this page for what can be cleared in " + esc(state) + " and how "
        "to ask. If the conviction is still showing up on background "
        "checks after a discharge or an expungement order, the court "
        "clerk can tell you which agencies hold the record.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> When your term ends, "
        "ask your officer for written proof of discharge, confirm with "
        "the court clerk that the case is closed, and then &mdash; "
        "separately &mdash; look into record clearing on this page.</p>"
    )
    parts.append("</div>")
    # --- Probation in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Probation in {esc(state)}</h3>")
    parts.append(f"<p>{esc(s['delivery'])}</p>")
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Find out which agency "
        "supervises your county &mdash; the official source below lists "
        "it &mdash; and confirm your officer&rsquo;s name, office, and "
        "reporting instructions in writing.</p>"
    )
    parts.append("</div>")
    # --- Official links ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Official links in {esc(state)}</h3>")
    parts.append("<ul>")
    parts.append(
        f"<li><a href=\"{esc(s['link'])}\" target=\"_blank\" "
        f"rel=\"noopener\">{esc(s['link_label'])}</a></li>"
    )
    parts.append("</ul>")
    parts.append("</div>")
    # --- Do this now ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Read your probation "
        "order today and write down every condition, date, and dollar. (2) "
        "If a condition clashes with work, housing, or your ability to pay, "
        "tell your officer in writing and ask the court to change it &mdash; "
        "do not just break it. (3) If anything goes wrong, call your officer "
        "before it becomes a violation report. (4) If you need to move, apply "
        "through your officer before you move. (5) Keep proof of everything "
        "&mdash; completion certificates, payment receipts, pay stubs, "
        "treatment letters &mdash; in one folder, and get your discharge in "
        "writing when probation ends.</p>"
    )
    parts.append(
        "<p><em>Sources: the official " + esc(state) + " source linked "
        "above, checked November 14, 2026, and the probation cards in the "
        "Wrongly Accused section on this page, which were built from "
        "official state sources. U.S. Supreme Court cases cited: "
        "<em>Gagnon v. Scarpelli</em>, 411 U.S. 778 (1973); "
        "<em>Griffin v. Wisconsin</em>, 483 U.S. 868 (1987); "
        "<em>United States v. Knights</em>, 534 U.S. 112 (2001); "
        "<em>Bearden v. Georgia</em>, 461 U.S. 660 (1983). Laws change "
        "&mdash; confirm the current rule in the official source before "
        "you rely on a deadline. This is general information, not legal "
        "advice.</em></p>"
    )
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def build_state_pages(data):
    for s in data:
        slug = s["slug"]
        path = STATES / f"{slug}.html"
        text = path.read_text()
        anchor = f"probation-in-{slug}"
        assert anchor not in text, f"{slug}: anchor already present"
        # --- insert section before Payday / title loans (newest-first) ---
        h2 = text.find(f'<h2 id="payday-title-loans-in-{slug}">')
        assert h2 != -1, f"{slug}: payday-title-loans h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        new_section = section_html(s)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the payday-title-loans <li> ---
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#payday-title-loans-in-'
            + re.escape(slug)
            + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: payday-title-loans contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#probation-in-{slug}">'
            f"Probation in {s['state']}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert "probation" not in helper_part, "index already has helper option"
    assert 'data-topic="probation"' not in text, "index already has card"
    opt_old = (
        '<option value="payday-title-loans" data-anchor="payday-title-loans">'
        "Payday / title loans (cost, caps, payment plans)</option>"
    )
    assert opt_old in text, "payday-title-loans helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="probation" data-anchor="probation">'
        "Probation (conditions, violations, moving, ending early)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="payday-title-loans"'
    idx = text.find(card_anchor)
    assert idx != -1, "payday-title-loans card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="probation">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-probation.jpg" alt="Probation" loading="lazy"></span>
          <h3>Probation</h3>
          <p>Supervision instead of jail: your conditions, what your probation officer can and cannot do, violation hearings, moving to another state, fees, and getting off early.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 35 topics" in text, "show-all label not found"
    text = text.replace("Show all 35 topics", "Show all 36 topics", 1)
    assert '<span class="count-badge">35 topics</span>' in text
    text = text.replace(
        '<span class="count-badge">35 topics</span>',
        '<span class="count-badge">36 topics</span>',
        1,
    )
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 35->36")


def build_about():
    text = ABOUT.read_text()
    assert "80 legal topics" in text, "about count not found"
    ABOUT.write_text(text.replace("80 legal topics", "81 legal topics", 1))
    print("  about.html: 80 -> 81")


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 10498, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith("probation-in-") for e in idx)
    for s in data:
        state = s["state"]
        slug = s["slug"]
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"probation-in-{slug}",
                "h": f"Probation in {state}",
                "t": (
                    f"Probation in {state} "
                    f"\u2014 probation supervision probation officer "
                    f"conditions violation hearing preponderance of the "
                    f"evidence Gagnon early termination Interstate Compact "
                    f"ICAOS transfer move to another state supervision fee "
                    f"Bearden cannot pay drug test travel no-contact "
                    f"treatment search Griffin Knights discharge expungement "
                    f"record {state}"
                ),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Probation",
            "t": (
                "Supervision instead of jail: your conditions, what your "
                "probation officer can and cannot do, violation hearings, "
                "moving to another state, fees, and getting off early."
            ),
        }
    )
    assert len(idx) == 10549, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 10498 -> {len(idx)} (+51)")


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
