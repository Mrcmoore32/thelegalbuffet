#!/usr/bin/env python3
"""Build Topic #98: Felon Voting Rights — standalone section on all
50 state pages.

Inserts one new section per state page (before Applying for Public
Benefits, newest-first), a contents-list entry (before the
public-benefits <li>), a homepage helper option + topic card (after
Applying for Public Benefits), bumps About 96 -> 97, and appends 50
state entries + 1 helper entry to assets/search-index.json
(11314 -> 11365).

Data: hidden_files/topic-research/felon-voting-rights/all-states.json
(coordinator-merged 2026-11-20 from 5 research batches; keys normalized
to lowercase. All 50 legal-aid URLs checked: 41 curl 200, 2 more
confirmed live via text fetch (Legal Aid Services of Oregon, SD Law
Help), 7 more verified live via text fetch during the #95/#97
verification the same day (LawHelpCA, Idaho Legal Aid, Iowa Legal Aid,
MassLegalHelp, Mississippi Legal Services, SC Legal Services, Legal Aid
of West Virginia). Coordinator resolutions: RI keeps rils.org (live
site with current Nov 2026 content; helprilaw.org also live, noted as
an alternate); ND keeps lsnd.org (legalassist.org redirects to it).
Headline counts: never loses the vote 2 (ME, VT); only while in prison
24; after the sentence is complete 12; after sentence plus fines/fees
3 (AZ, AR, SD); permanent for some offenses 8 (AL, DE, FL, IA, KY, MS,
TN, WY); only by pardon 1 (VA — as of November 2026; Virginia voters
approved automatic restoration on release, effective January 1, 2027,
so VA flips to prison-only then — January-sweep item, carried in the
state note). Georgia fines/fees coded "no" — confirmed against the
Georgia Secretary of State's own wording (sentence counts as complete
even with outstanding restitution/fees; probation fines are cancelled
on completion). Missouri H.B. 1871 confirmed effective August 28,
2026 — most felons now vote on release; listed sex/violent offenses
still wait for discharge. Pennsylvania entry cites Mixon v.
Commonwealth (2000), which struck down the five-year bar still printed
in the statute text. No phone numbers in the dataset.)
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "felon-voting-rights" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-felon-voting-rights.jpg"

SLUG = "felon-voting-rights"
TITLE = "Felon Voting Rights"
PREV_SLUG = "applying-for-public-benefits"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def status_word(v):
    return {
        "never-loses": "Never loses the vote",
        "prison-only": "Only while in prison",
        "after-sentence": "After the sentence is complete",
        "after-sentence-and-payment": "After the sentence is complete and fines/fees are paid",
        "pardon-only": "Only by pardon",
        "permanent-some": "Permanent for some offenses",
    }.get(v, v)


def restoration_word(v):
    return {
        "automatic": "Automatic",
        "application": "By application",
        "clemency": "By pardon/clemency",
        "varies": "It depends",
    }.get(v, v)


def fines_word(v):
    return {"yes": "Yes", "no": "No", "na": "Not applicable"}.get(v, v)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="felon-voting-rights-in-{slug}">Felon voting rights in {esc(state)}</h2>'
    )
    parts.append(
        "<p>In most states, a felony conviction takes away the right to vote "
        "&mdash; but for how long, and how you get it back, depends entirely "
        "on your state. In two states you never lose the vote at all. In "
        "about half the states it comes back the day you walk out of prison. "
        "In others you must finish probation and parole first, or pay off "
        "fines and fees, or apply to a court or a governor. This section "
        "explains the rules, the traps, and what to do in your state. The "
        "picture here is as of <strong>November 2026</strong>. This is "
        "general information, not legal advice.</p>"
    )
    # --- Card 1: what disenfranchisement is ---
    parts.append('<div class="card">')
    parts.append("<h3>What losing the vote means</h3>")
    parts.append(
        "<p><strong>Disenfranchisement</strong> means losing the right to vote "
        "because of a criminal conviction. It applies to <strong>felony</strong> "
        "convictions, not misdemeanors &mdash; with one exception: Indiana "
        "also takes the vote away while a person is incarcerated for a "
        "misdemeanor. Being arrested, charged, or held before trial does not "
        "take the vote away, and a conviction that is not final &mdash; for "
        "example, deferred adjudication in Texas, or a First Offender sentence "
        "in Georgia that has not been revoked &mdash; may not take it away "
        "either.</p>"
    )
    parts.append(
        "<p>Losing the vote is separate from losing other rights. A felony "
        "conviction can also affect owning a firearm, serving on a jury, and "
        "holding public office, and those rights often come back on different "
        "schedules &mdash; in Utah, for example, voting comes back on "
        "probation or parole, while holding office takes ten years. Getting "
        "your vote back does not automatically restore the others.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Find your state&rsquo;s "
        "answer in the card below first. Then check your registration status "
        "with your local election office before you assume you can or cannot "
        "vote.</p>"
    )
    parts.append("</div>")
    # --- Card 2: the six buckets ---
    parts.append('<div class="card">')
    parts.append("<h3>The six buckets: when the vote comes back</h3>")
    parts.append(
        "<p><strong>Never loses the vote (2 states):</strong> Maine and "
        "Vermont &mdash; a felony conviction never takes the vote away, even "
        "in prison; people vote by absentee ballot. <strong>Only while in "
        "prison (24 states):</strong> the vote comes back automatically on "
        "release, even while on parole or probation. <strong>After the "
        "sentence is complete (12 states):</strong> the vote returns once "
        "prison, parole, and probation are all finished. "
        "<strong>After the sentence plus fines/fees (3 states):</strong> "
        "Arizona, Arkansas, and South Dakota &mdash; unpaid fines, fees, or "
        "restitution can hold the vote back. <strong>Permanent for some "
        "offenses (8 states):</strong> Alabama, Delaware, Florida, Iowa, "
        "Kentucky, Mississippi, Tennessee, and Wyoming &mdash; most felonies "
        "restore after the sentence, but certain offenses (often murder and "
        "sexual offenses) are barred for life unless pardoned. "
        "<strong>Only by pardon (1 state):</strong> Virginia &mdash; as of "
        "November 2026 the governor must individually restore the right.</p>"
    )
    parts.append(
        "<p>One state is about to change: Virginia voters approved a "
        "constitutional amendment on November 3, 2026 that automatically "
        "restores voting rights on release from incarceration, effective "
        "<strong>January 1, 2027</strong>. And Missouri changed its rule on "
        "August 28, 2026 (H.B. 1871): most people with felony convictions "
        "there can now vote while on probation or parole.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Find your state&rsquo;s "
        "bucket in the card below. If you are in a &ldquo;permanent for "
        "some&rdquo; state, read the note carefully &mdash; the bar usually "
        "applies only to specific offenses, not to every felony.</p>"
    )
    parts.append("</div>")
    # --- Card 3: how restoration works ---
    parts.append('<div class="card">')
    parts.append("<h3>How restoration works</h3>")
    parts.append(
        "<p><strong>Automatic:</strong> in most states the right comes back "
        "by law &mdash; on release, or when the sentence ends. Nothing to "
        "file, no one to ask. But &ldquo;automatic&rdquo; does not mean "
        "&ldquo;already registered&rdquo;: in most states your old "
        "registration was cancelled, so you must <strong>re-register</strong> "
        "to vote. A few states make that easy &mdash; Michigan automatically "
        "registers people on release from prison, and North Dakota has no "
        "voter registration at all. <strong>By application:</strong> some "
        "states require a court petition or an application to a board &mdash; "
        "Tennessee, for example, requires a circuit-court order. "
        "<strong>By pardon/clemency:</strong> in Virginia (until January 1, "
        "2027) and for the permanently barred offenses in several states, "
        "only the governor can restore the right.</p>"
    )
    parts.append(
        "<p>Some states issue a paper that proves the right is back &mdash; a "
        "certificate of discharge, a certificate of restoration, or a court "
        "order. Keep it. An election office may ask for it when you "
        "re-register, and it is the simplest answer if anyone questions your "
        "eligibility.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Once your state&rsquo;s "
        "trigger point has passed, re-register to vote &mdash; online, by "
        "mail, or in person at your local election office &mdash; and keep "
        "any discharge or restoration certificate they gave you.</p>"
    )
    parts.append("</div>")
    # --- Card 4: fines, fees, restitution ---
    parts.append('<div class="card">')
    parts.append("<h3>Fines, fees, and restitution: the money question</h3>")
    parts.append(
        "<p>In most states, unpaid fines, fees, or restitution do <strong>not</strong> "
        "block getting the vote back. But in a few states they do: Arizona, "
        "Arkansas, and South Dakota require the money to be paid (or the "
        "sentence, including its financial conditions, to be complete) before "
        "the vote returns. Florida&rsquo;s rule is similar for most felonies "
        "&mdash; &ldquo;completion of sentence&rdquo; there includes full "
        "payment of fines, fees, and restitution.</p>"
    )
    parts.append(
        "<p>Even where money is not a direct test, it can still delay things "
        "indirectly: if paying is a condition of probation or parole, and "
        "probation gets extended because the money was not paid, you are "
        "still on supervision &mdash; and in an after-sentence state, that "
        "means you still cannot vote. Georgia&rsquo;s rule shows the other "
        "side: fines imposed as a condition of probation are automatically "
        "cancelled when probation ends, and the Secretary of State says a "
        "sentence counts as complete even with outstanding restitution or "
        "fees.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check the money line in "
        "the state card below. If money is the only thing holding your "
        "sentence open, ask the sentencing court or your probation officer "
        "whether the obligation can be converted to community service, put "
        "on a payment plan, or ended &mdash; and get the answer in writing.</p>"
    )
    parts.append("</div>")
    # --- Card 5: probation, parole, jail, pretrial ---
    parts.append('<div class="card">')
    parts.append("<h3>On probation or parole? In jail? Awaiting trial?</h3>")
    parts.append(
        "<p>Whether you can vote while on probation or parole depends on your "
        "state&rsquo;s bucket. In the 24 prison-only states, yes &mdash; "
        "release from prison is enough, and probation or parole does not "
        "matter. In after-sentence states, no &mdash; not until supervision "
        "ends. In Maine and Vermont, the question never arises.</p>"
    )
    parts.append(
        "<p>People in jail <strong>before trial</strong>, and people serving "
        "a <strong>misdemeanor</strong> sentence, can vote in most states "
        "&mdash; usually by absentee ballot. Jails are supposed to help with "
        "that, but in practice many people in jail never get a ballot. If you "
        "or someone you know is in jail and eligible, ask the jail for an "
        "absentee ballot application early, and check the registration "
        "deadline &mdash; it is often weeks before Election Day.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you are not serving a "
        "felony sentence, you can almost certainly vote &mdash; check your "
        "registration and request an absentee ballot if you are in jail. If "
        "you are on felony probation or parole, check your state&rsquo;s "
        "bucket first.</p>"
    )
    parts.append("</div>")
    # --- Card 6: traps ---
    parts.append('<div class="card">')
    parts.append("<h3>Traps: do not get caught by these</h3>")
    parts.append(
        "<p><strong>Assuming you are still registered.</strong> Most states "
        "cancel a registration when a felony conviction is entered. "
        "Re-registering is part of getting the vote back, not an optional "
        "extra. <strong>Assuming the rules are the same everywhere.</strong> "
        "Moving to a new state does not move your old state&rsquo;s rule with "
        "you &mdash; the new state&rsquo;s law decides, and a federal or "
        "out-of-state conviction can be treated differently from an "
        "in-state one. <strong>Voting while ineligible.</strong> In some "
        "states, knowingly voting before your rights are restored is itself a "
        "crime &mdash; North Carolina made it a crime effective January 1, "
        "2024. If you are unsure, check with your local election office "
        "before you cast a ballot, not after. <strong>Trusting old "
        "guides.</strong> These rules change often &mdash; Missouri, "
        "Minnesota, New Jersey, Nevada, and Virginia have all changed theirs "
        "since 2019, and several states have changes taking effect in 2026 "
        "and 2027.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Before an election, "
        "confirm three things: your state&rsquo;s trigger point has passed, "
        "you are registered at your current address, and no money or "
        "supervision condition is still holding your sentence open.</p>"
    )
    parts.append("</div>")
    # --- Card 7: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Felon voting rights in {esc(state)}</h3>")
    parts.append(
        f"<p><strong>When does the vote come back?</strong> {status_word(e['status'])}. {esc(e['status_note'])}</p>"
    )
    parts.append(
        f"<p><strong>How is it restored?</strong> {restoration_word(e['restoration'])}. {esc(e['restoration_note'])}</p>"
    )
    parts.append(
        f"<p><strong>Do fines, fees, or restitution block it?</strong> {fines_word(e['fines_fees_required'])}. {esc(e['fines_fees_note'])}</p>"
    )
    if e["statute_cite"]:
        parts.append(
            f"<p><strong>The law:</strong> {esc(e['statute_name'])} &mdash; {esc(e['statute_cite'])}.</p>"
        )
    else:
        parts.append(
            "<p><strong>The law:</strong> No statute &mdash; this state&rsquo;s "
            "voting rule comes from its constitution or court decisions, not a statute.</p>"
        )
    if e["state_note"]:
        parts.append(f"<p>{esc(e['state_note'])}</p>")
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check the answers above "
        "for your state, re-register to vote once the trigger point has "
        "passed, and if you are unsure whether you are eligible, ask your "
        "local election office before Election Day &mdash; not after.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Find your state&rsquo;s "
        "answer above &mdash; when the vote comes back, and whether money "
        "blocks it. (2) Once the trigger point has passed, re-register to "
        "vote at your current address. (3) Keep any discharge or restoration "
        "certificate. (4) If you are on probation or parole, in jail, or "
        "unsure about fines, check with your local election office before "
        "you vote. (5) Remember the rules change often &mdash; confirm the "
        "current law before each election.</p>"
    )
    parts.append(
        "<p><em>Sources: the official state constitutions, statutes, and "
        "Secretary of State / elections office pages linked in the research "
        "for this section, checked November 20, 2026. Felon voting rules "
        "have changed recently in several states and more changes take "
        "effect in 2027 &mdash; confirm the current law with your local "
        "election office before you rely on it. This is general information, "
        "not legal advice.</em></p>"
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
            f"Felon voting rights in {state}</a></li>\n"
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


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert SLUG not in helper_part, "index already has helper option"
    assert f'data-topic="{SLUG}"' not in text, "index already has card"
    opt_old = (
        '<option value="applying-for-public-benefits" data-anchor="applying-for-public-benefits">'
        "Applying for public benefits (Medicaid, SNAP food help — who qualifies, where to apply online, appeals, renewals)</option>"
    )
    assert opt_old in text, "public-benefits helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="felon-voting-rights" data-anchor="felon-voting-rights">'
        "Felon voting rights (when the vote comes back, fines and fees, probation and parole, how to re-register)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="applying-for-public-benefits"'
    idx = text.find(card_anchor)
    assert idx != -1, "public-benefits card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="felon-voting-rights">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-felon-voting-rights.jpg" alt="Felon voting rights" loading="lazy"></span>
          <h3>Felon Voting Rights</h3>
          <p>When does the vote come back after a felony conviction? The six rules, the fines-and-fees trap, and how to re-register in your state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 51 topics" in text, "show-all label not found"
    text = text.replace("Show all 51 topics", "Show all 52 topics", 1)
    show_pos = text.find("Show all 52 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">51 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("51 topics", "52 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 51->52")


def build_about():
    text = ABOUT.read_text()
    assert text.count("96 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("96 legal topics", "97 legal topics", 1))
    print("  about.html: 96 -> 97")


def state_index_t(state, slug, e):
    bits = [
        "felon voting rights disenfranchisement restoration",
        f"Felon voting rights in {state}",
        f"vote comes back {status_word(e['status']).lower()} {e['status_note']}",
        f"restoration {restoration_word(e['restoration']).lower()} {e['restoration_note']}",
        f"fines fees restitution block {fines_word(e['fines_fees_required']).lower()} {e['fines_fees_note']}",
        "probation parole jail pretrial misdemeanor absentee ballot re-register",
        "voting while ineligible crime check registration election office",
        f"{e['statute_name'] or 'constitution'} {e['statute_cite'] or ''}",
        f"{e['state_note'] or ''}",
        f"{e['legal_aid_name']}",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11314, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Felon voting rights in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Felon Voting Rights",
            "t": (
                "felon-voting-rights felon voting rights Felon Voting Rights? "
                "When does the vote come back after a felony conviction? The "
                "six rules, the fines-and-fees trap, and how to re-register in "
                "your state. Never loses prison-only after sentence fines fees "
                "restitution pardon clemency probation parole re-register."
            ),
        }
    )
    assert len(idx) == 11365, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11314 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d
    assert len(states) == 50, len(states)
    data = [(k, states[k]) for k in sorted(states)]
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "status", "status_note", "restoration", "restoration_note",
        "fines_fees_required", "fines_fees_note", "statute_name",
        "statute_cite", "legal_aid_name", "legal_aid_url", "state_note",
        "sources",
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
        assert e["status"] in ("never-loses", "prison-only", "after-sentence", "after-sentence-and-payment", "pardon-only", "permanent-some"), f"{k}: bad status"
        assert e["restoration"] in ("automatic", "application", "clemency", "varies"), f"{k}: bad restoration"
        assert e["fines_fees_required"] in ("yes", "no", "na"), f"{k}: bad fines_fees_required"
        assert e["status_note"] and e["restoration_note"] and e["fines_fees_note"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"], f"{k}: empty required field"
        assert (e["statute_name"] is None) == (e["statute_cite"] is None), f"{k}: statute name/cite mismatch"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before applying-for-public-benefits section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
