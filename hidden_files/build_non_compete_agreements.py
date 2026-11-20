#!/usr/bin/env python3
"""Build Topic #96: Non-Compete Agreements — standalone section on all
50 state pages.

Inserts one new section per state page (before Product Liability &
Defective Products, newest-first), a contents-list entry (before the
product-liability <li>), a homepage helper option + topic card (after
Product Liability & Defective Products), bumps About 94 -> 95, and
appends 50 state entries + 1 helper entry to assets/search-index.json
(11212 -> 11263).

Data: hidden_files/topic-research/non-compete-agreements/all-states.json
(coordinator-merged 2026-11-20 from 5 research batches; all 50 legal-aid
URLs verified alive — 44 curl 200 + 6 via text fetch during the #95
verification, same URLs, same day. Coordinator swaps for statewide
coverage: CA LAFLA -> LawHelpCA, KY klaid.org -> Kentucky Justice Online
(kyjustice.org), MI Lakeshore -> Michigan Legal Help, MN Mid-Minnesota ->
LawHelp Minnesota, MO LSEM -> Missouri Legal Services (lsmo.org), MS
Mississippi Center -> Mississippi Legal Services, NJ lsnjlawhotline.org ->
LSNJ (lsnj.org). MA wage_threshold normalized null (no dollar threshold;
note explains the nonexempt-worker rule). Headline counts: 5 states ban
non-competes outright (CA, MN, ND, OK, WY), 23 restricted, 22 allowed.
WA is coded "restricted" as of Nov 2026 — its near-total ban takes effect
June 30, 2027 and is prominent in the notes.)
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "non-compete-agreements" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-non-compete-agreements.jpg"

SLUG = "non-compete-agreements"
TITLE = "Non-Compete Agreements"
PREV_SLUG = "product-liability-defective-products"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def enforce_word(v):
    return {"banned": "Banned", "restricted": "Restricted", "allowed": "Allowed"}.get(v, v)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="non-compete-agreements-in-{slug}">Non-compete agreements in {esc(state)}</h2>'
    )
    parts.append(
        "<p>A <strong>non-compete agreement</strong> is a promise not to work "
        "for a competitor, or start a competing business, after you leave a "
        "job. It can lock you out of your own profession for months or years, "
        "so whether it is enforceable matters a lot &mdash; and the answer "
        "depends almost entirely on your state. Five states ban employee "
        "non-competes outright, most others allow them only with limits, and a "
        "few still enforce them broadly. This section explains what a "
        "non-compete can and cannot do, the tests courts use, and what "
        + esc(state)
        + " says. The picture here is as of <strong>November 2026</strong>. "
        "This is general information, not legal advice.</p>"
    )
    # --- Card 1: what a non-compete is ---
    parts.append('<div class="card">')
    parts.append("<h3>What a non-compete is</h3>")
    parts.append(
        "<p>A non-compete usually says that after you leave, you cannot work "
        "for a competing business, or start one yourself, for a set time (often "
        "six months to two years) and within a set area (a city, a state, a "
        "radius around the office). It is often buried in an offer letter, an "
        "employment agreement, or a handbook you sign on your first day. It is "
        "different from a <strong>non-solicitation</strong> clause (do not "
        "poach the company&rsquo;s customers or co-workers) and a "
        "<strong>confidentiality</strong> clause (do not share trade secrets) "
        "&mdash; those are usually enforceable even where non-competes are "
        "banned.</p>"
    )
    parts.append(
        "<p>Non-competes are not enforceable just because you signed one. In "
        "most states a court will only enforce a non-compete that is "
        "<strong>reasonable</strong> in time, area, and scope, and that protects "
        "a real business interest like trade secrets or customer relationships "
        "&mdash; not one whose only purpose is to stop ordinary competition. "
        "Some courts will narrow an overbroad clause and enforce the trimmed "
        "version; others throw the whole clause out if any part is "
        "unreasonable.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Before you sign, read the "
        "clause and note the time, the area, and what work it covers. If you "
        "are asked to sign one after you already started the job, check the "
        "state card below &mdash; in some states your employer must give you "
        "something new in return, like a raise or a promotion, for it to count.</p>"
    )
    parts.append("</div>")
    # --- Card 2: banned vs restricted vs allowed ---
    parts.append('<div class="card">')
    parts.append("<h3>Banned, restricted, or allowed: the three buckets</h3>")
    parts.append(
        "<p><strong>Banned:</strong> California, Minnesota, North Dakota, "
        "Oklahoma, and Wyoming void employee non-competes by statute. In those "
        "states an employer generally cannot stop you from taking a competing "
        "job at all, though sale-of-business and trade-secret rules still "
        "apply. <strong>Restricted:</strong> most states allow non-competes "
        "only with limits &mdash; an earnings threshold below which the clause "
        "is void, a notice period, a time cap, or protection for certain "
        "professions like doctors. <strong>Allowed:</strong> the rest enforce "
        "non-competes under a court reasonableness test, with no statute "
        "setting a pay threshold.</p>"
    )
    parts.append(
        "<p>The trend is one way: bans and thresholds are spreading, and several "
        "states have new laws that took effect in 2025 and 2026. A clause that "
        "was enforceable when you signed it may not be enforceable now, and "
        "the reverse is also true for older agreements in states that "
        "tightened the rules only for new contracts.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Find your state&rsquo;s "
        "bucket in the state card below first. If your state bans non-competes "
        "or you earn under its threshold, the clause may already be void.</p>"
    )
    parts.append("</div>")
    # --- Card 3: earnings thresholds ---
    parts.append('<div class="card">')
    parts.append("<h3>Earnings thresholds: the pay line</h3>")
    parts.append(
        "<p>Many restricted states draw a <strong>pay line</strong>: earn under "
        "it and a non-compete is void; earn over it and the clause can still "
        "bind you if it is reasonable. The lines vary widely &mdash; some are "
        "tied to the federal poverty level, some to the state minimum wage, "
        "some are fixed dollar amounts that rise on a schedule, and some "
        "adjust every year for inflation. A few states draw the line by "
        "hourly pay or by job type instead of salary.</p>"
    )
    parts.append(
        "<p>Watch the dates: thresholds that adjust annually change every "
        "January, and a few states have new thresholds that only started in "
        "2026. The figure in the state card below is the 2026 figure where one "
        "could be verified.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Compare your pay to your "
        "state&rsquo;s threshold in the card below. If you are under it, the "
        "non-compete is likely void &mdash; but keep a copy of the agreement "
        "and your pay records anyway.</p>"
    )
    parts.append("</div>")
    # --- Card 4: what makes one unenforceable ---
    parts.append('<div class="card">')
    parts.append("<h3>What makes a non-compete unenforceable</h3>")
    parts.append(
        "<p>Even in states that allow non-competes, a clause can fail for "
        "several reasons: it lasts too long or covers too much territory; it "
        "bars work the employer has no legitimate interest in stopping; you "
        "were given no advance notice or no copy before you accepted the job; "
        "you received nothing new in exchange for signing mid-employment; or "
        "you were fired without cause or laid off, which in several states "
        "ends the employer&rsquo;s right to enforce it. A clause that bans "
        "all work in your field, anywhere, is almost never reasonable.</p>"
    )
    parts.append(
        "<p>Some states add teeth: an employer that presents or tries to "
        "enforce a void non-compete can owe the worker damages, a penalty per "
        "affected worker, and the worker&rsquo;s attorney fees.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If any of those problems "
        "fits your situation, do not assume the clause binds you &mdash; but "
        "do not ignore it either. Get advice before you take the competing job, "
        "so you are not the one sued first.</p>"
    )
    parts.append("</div>")
    # --- Card 5: if you're asked to sign / if you're leaving ---
    parts.append('<div class="card">')
    parts.append("<h3>Asked to sign one? Leaving a job with one?</h3>")
    parts.append(
        "<p><strong>Before you sign:</strong> ask for the full agreement in "
        "writing and time to read it. Negotiate the time and area down, ask "
        "what counts as a competitor, and ask what happens if you are laid "
        "off. In several states the employer must give you the agreement days "
        "or weeks before you start, and must tell you in writing to talk to a "
        "lawyer. <strong>After you leave:</strong> do not take customer lists, "
        "pricing, or trade secrets with you, even if the non-compete itself is "
        "void &mdash; those are separate obligations. Tell your new employer "
        "about the clause; a new employer that knowingly hires you into a "
        "breach can be sued too.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Keep a copy of everything "
        "you signed, note the dates, and get advice before you accept the "
        "competing job &mdash; not after the old employer&rsquo;s lawyer "
        "writes to you.</p>"
    )
    parts.append("</div>")
    # --- Card 6: what it does not cover ---
    parts.append('<div class="card">')
    parts.append("<h3>What a non-compete ban does not cover</h3>")
    parts.append(
        "<p>Even in states that ban non-competes, an employer can usually still "
        "enforce a <strong>confidentiality</strong> clause, a "
        "<strong>non-solicitation</strong> clause for customers and co-workers, "
        "a requirement to repay <strong>training costs</strong>, and a "
        "non-compete tied to <strong>selling a business</strong>. Trade-secret "
        "law applies in all 50 states regardless of what you signed. And a "
        "non-compete in a contract signed before a state&rsquo;s ban took "
        "effect may still be judged under the old rules.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Do not treat a ban as a "
        "free pass to take the client list with you. The non-compete may be "
        "dead while the trade-secret and non-solicitation rules are very much "
        "alive.</p>"
    )
    parts.append("</div>")
    # --- Card 7: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Non-compete agreements in {esc(state)}</h3>")
    parts.append(
        f"<p><strong>Enforceable?</strong> {enforce_word(e['enforceability'])}. {esc(e['enforce_note'])}</p>"
    )
    if e["wage_threshold"] is not None:
        parts.append(
            f"<p><strong>Earnings threshold?</strong> {esc(e['wage_threshold'])}. {esc(e['threshold_note'])}</p>"
        )
    else:
        parts.append(
            f"<p><strong>Earnings threshold?</strong> No threshold. {esc(e['threshold_note'])}</p>"
        )
    if e["statute_cite"]:
        parts.append(
            f"<p><strong>The law:</strong> {esc(e['statute_name'])} &mdash; {esc(e['statute_cite'])}.</p>"
        )
    else:
        parts.append(
            "<p><strong>The law:</strong> No statute &mdash; this state&rsquo;s "
            "non-compete rules come from court decisions, not a statute.</p>"
        )
    if e["state_note"]:
        parts.append(f"<p>{esc(e['state_note'])}</p>")
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check the two answers "
        "above for your state, keep a copy of anything you signed, and if the "
        "clause looks void or overbroad, talk to an employment lawyer before "
        "you take the competing job &mdash; many offer a free first "
        "consultation.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Find your state&rsquo;s "
        "answer above &mdash; banned, restricted, or allowed &mdash; and its "
        "pay threshold. (2) Read the clause for its time, area, and scope, and "
        "keep a copy of everything you signed. (3) If you are under the "
        "threshold or your state bans non-competes, the clause may already be "
        "void. (4) Do not take customer lists or trade secrets with you, even "
        "if the non-compete is dead. (5) Get advice from an employment lawyer "
        "before you accept the competing job, not after your old employer "
        "writes to you.</p>"
    )
    parts.append(
        "<p><em>Sources: the official state statutes and court sources linked in "
        "the research for this section, checked November 20, 2026. "
        "Non-compete law is changing fast and thresholds adjust yearly &mdash; "
        "confirm the current law with a lawyer before you rely on it. This is "
        "general information, not legal advice.</em></p>"
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
            f"Non-compete agreements in {state}</a></li>\n"
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
        '<option value="product-liability-defective-products" data-anchor="product-liability-defective-products">'
        "Product liability &amp; defective products (defective drugs, devices, cars, recalls, deadlines to sue, what to keep)</option>"
    )
    assert opt_old in text, "product-liability helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="non-compete-agreements" data-anchor="non-compete-agreements">'
        "Non-compete agreements (is yours enforceable, pay thresholds, bans, what to do before you sign or leave)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="product-liability-defective-products"'
    idx = text.find(card_anchor)
    assert idx != -1, "product-liability card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="non-compete-agreements">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-non-compete-agreements.jpg" alt="Non-compete agreements" loading="lazy"></span>
          <h3>Non-Compete Agreements</h3>
          <p>Can your employer stop you from taking a competing job? The five ban states, the pay thresholds, and what to do before you sign or leave.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 48 topics" in text, "show-all label not found"
    text = text.replace("Show all 48 topics", "Show all 49 topics", 1)
    show_pos = text.find("Show all 49 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">48 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("48 topics", "49 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 48->49")


def build_about():
    text = ABOUT.read_text()
    assert text.count("94 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("94 legal topics", "95 legal topics", 1))
    print("  about.html: 94 -> 95")


def state_index_t(state, slug, e):
    threshold = (
        f"earnings threshold {e['wage_threshold']} {e['threshold_note']}"
        if e["wage_threshold"] is not None
        else f"no earnings threshold {e['threshold_note']}"
    )
    bits = [
        "non-compete agreements restrictive covenants",
        f"Non-compete agreements in {state}",
        f"enforceability {enforce_word(e['enforceability']).lower()} {e['enforce_note']}",
        threshold,
        "reasonableness time area scope legitimate business interest blue pencil narrow overbroad clause",
        "before you sign read time area scope ask what counts as competitor notice period consideration",
        "confidentiality non-solicitation trade secrets still apply even where non-competes banned sale of business",
        f"{e['statute_name'] or 'case law'} {e['statute_cite'] or ''}",
        f"{e['state_note'] or ''}",
        f"{e['legal_aid_name']}",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11212, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Non-compete agreements in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Non-Compete Agreements",
            "t": (
                "non-compete-agreements non-compete agreements Non-Compete "
                "Agreements? Can your employer stop you from taking a competing "
                "job? The five ban states, the pay thresholds, and what to do "
                "before you sign or leave. Banned restricted allowed earnings "
                "threshold reasonableness garden leave blue pencil "
                "confidentiality non-solicitation trade secrets."
            ),
        }
    )
    assert len(idx) == 11263, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11212 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [(k, states[k]) for k in sorted(states)]
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "enforceability", "enforce_note", "wage_threshold", "threshold_note",
        "statute_name", "statute_cite",
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
        assert e["enforceability"] in ("banned", "restricted", "allowed"), f"{k}: bad enforceability"
        assert e["enforce_note"] and e["threshold_note"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"], f"{k}: empty required field"
        assert (e["statute_name"] is None) == (e["statute_cite"] is None), f"{k}: statute name/cite mismatch"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before product-liability-defective-products section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
