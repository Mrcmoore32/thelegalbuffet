#!/usr/bin/env python3
"""Build Topic #102: Data Breach Response — standalone section on
all 50 state pages.

Inserts one new section per state page (before Zoning, Variances &
Land Use, newest-first), a contents-list entry (before the
zoning-variances-land-use <li>), a homepage helper option + topic
card (after Zoning), bumps About 100 -> 101, and appends 50 state
entries + 1 helper entry to assets/search-index.json (11518 -> 11569).

Data: hidden_files/topic-research/data-breach-response/all-states.json
(coordinator-merged 2026-11-20 from 5 research batches; keys lowercased
at merge. AG-coding normalized at merge: "yes" = AG notice for EVERY
breach, "varies" = threshold-based; flipped yes->varies for AL, AZ,
AR, CA, CO, DE, FL. 52 null URLs resolved by the coordinator
2026-11-20: 26 AG homepages + 26 legal-aid homepages, all verified
(42 curl 200, 2 text-fetch confirmed, 9 search-crawl confirmed, 2
superseded by lasco.org after the Ohio Legal Services Association
merged into Legal Aid of Southeast and Central Ohio on Jan 1, 2024).
SD sources filled with a full-text reproduction of SDCL 22-40-19-26.
RI credit_monitoring_note filled from RI Gen. Laws 11-49.3-4(e).
Headline counts: notification deadline "without unreasonable delay"
27 / 45 days 11 / 30 days 6 / 60 days 5 / "as soon as possible" 1
(NH, the statute's own wording); AG notification yes 13 / varies 23
/ no 14; credit monitoring required 5 (CA, CT, DE, MA, PA) / varies 1
(RI) / not-required 44; private right of action yes 4 (HI, LA, TN,
WA) / limited 12 / no 34. No phone numbers in the dataset.
Spot-verifications (all confirmed as researched, Nov 20, 2026):
CA 30-day deadline (SB 446, eff. Jan 1, 2026); NY 30-day deadline
(Ch. 647 of 2024); OK AG duty (SB 626, eff. Jan 1, 2026); TN private
right (47-18-2107(h)); WA private right (RCW 19.255.040); TX SB 768
(AG clock 60 -> 30 days, eff. Sept 1, 2023); CT credit 24 months
(36a-701b(b)(2)(B)); MA credit 18 months (ch. 93H s. 3A); DE credit
1 year (12B-102(e)); PA credit 12 months (Act 33 of 2024); OH no AG
notice at all (1349.19); IN 45-day hard cap (HB 1351); MD AG before
consumers (14-3504); VA private "limited" (18.2-186.6(I)); LA private
"yes" (51:3075); HI private "yes" (HRS 487N-3(b)); RI credit "varies"
(11-49.3-4(e), agencies only); NH "as soon as possible" (RSA
359-C:20(I)(a)); DE private "no" (2017 amendment removed the 2005
private right); SD statute SDCL 22-40-19-26 confirmed.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "data-breach-response" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-data-breach-response.jpg"

SLUG = "data-breach-response"
TITLE = "Data Breach Response"
PREV_SLUG = "zoning-variances-land-use"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def ag_word(v):
    return {
        "yes": "Yes — for every breach",
        "varies": "It depends — only for larger breaches",
        "no": "No — the law does not require it",
    }.get(v, v)


def credit_word(v):
    return {
        "required": "Required — the company must pay for it",
        "varies": "Sometimes — it depends on who was breached",
        "not-required": "Not required by the breach law",
    }.get(v, v)


def private_word(v):
    return {
        "yes": "Yes",
        "limited": "Limited — only in some situations",
        "no": "No",
    }.get(v, v)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="data-breach-response-in-{slug}">Data breach response in {esc(state)}</h2>'
    )
    parts.append(
        "<p>A company loses your personal information — your name with "
        "your Social Security number, your bank account, a password. "
        "Every state has a law that says how fast the company must tell "
        "you, whether it must also tell the state attorney general, and "
        "whether you can sue. The clock is short: in <strong>6 states the "
        "company has 30 days</strong>, in <strong>11 states 45 days</strong>, "
        "in <strong>5 states 60 days</strong> — and in <strong>27 states "
        "there is no fixed number of days, just &ldquo;without unreasonable "
        "delay.&rdquo;</strong> Only <strong>5 states</strong> make the "
        "company pay for credit monitoring. And only <strong>4 states</strong> "
        "clearly let you sue under the breach law itself. The picture here "
        "is as of <strong>November 2026</strong>. This is general "
        "information, not legal advice.</p>"
    )
    # --- Card 1: the deadline ---
    parts.append('<div class="card">')
    parts.append("<h3>How fast must they tell you?</h3>")
    parts.append(
        "<p>In <strong>27 states</strong> the law says the company must "
        "notify you &ldquo;without unreasonable delay&rdquo; — no fixed "
        "number of days. In <strong>6 states</strong> the deadline is "
        "<strong>30 days</strong> (California, Colorado, Florida, Maine, "
        "New York, and Washington), in <strong>11 states</strong> it is "
        "<strong>45 days</strong>, and in <strong>5 states</strong> it is "
        "<strong>60 days</strong> (Connecticut, Delaware, Louisiana, "
        "South Dakota, and Texas). New Hampshire&rsquo;s law uses its own "
        "words: &ldquo;as soon as possible.&rdquo;</p>"
    )
    parts.append(
        "<p>In most states the clock starts when the company discovers "
        "the breach, not the day the breach happened. A company that "
        "finds a breach late can still be within the law — which is why "
        "the letter can arrive months after your information was taken. "
        "Some states let the company delay notice while law enforcement "
        "investigates. Check your state&rsquo;s card below for the exact "
        "deadline and what starts the clock.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> The day the letter "
        "arrives, start the clock on your own protection: freeze your "
        "credit (see the card below) and change the password on any "
        "account that used the same one.</p>"
    )
    parts.append("</div>")
    # --- Card 2: the attorney general ---
    parts.append('<div class="card">')
    parts.append("<h3>Does the attorney general get told?</h3>")
    parts.append(
        "<p>In <strong>13 states</strong> the company must tell the "
        "attorney general about every breach. In <strong>23 states</strong> "
        "it only has to tell the attorney general about bigger breaches — "
        "usually when 250, 500, or 1,000 residents are affected, "
        "depending on the state. In <strong>14 states</strong> (Alaska, "
        "Georgia, Kansas, Kentucky, Michigan, Minnesota, Mississippi, "
        "Nevada, New Jersey, Ohio, Tennessee, West Virginia, Wisconsin, "
        "and Wyoming) the breach law does not require the company to tell "
        "the attorney general at all.</p>"
    )
    parts.append(
        "<p>Attorney general notice does not make your letter arrive "
        "faster — it is the state&rsquo;s enforcement hook. It is also "
        "how the attorney general learns about breaches and, in some "
        "states, posts them publicly. If you never got a letter but think "
        "your information was exposed, your attorney general&rsquo;s "
        "consumer-protection office (linked in your state&rsquo;s card "
        "below) is the place to report it.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If the company never "
        "told you and you learn about the breach another way, report it "
        "to your attorney general&rsquo;s office. Keep the letter if you "
        "got one — it is your proof of when you were told.</p>"
    )
    parts.append("</div>")
    # --- Card 3: credit monitoring and freezes ---
    parts.append('<div class="card">')
    parts.append("<h3>Credit monitoring and freezes</h3>")
    parts.append(
        "<p>Only <strong>5 states</strong> make the company pay for "
        "credit monitoring when your information is exposed: "
        "California, Connecticut, Delaware, Massachusetts, and "
        "Pennsylvania. Rhode Island requires it only when a state or "
        "city agency is breached — private companies are not required to "
        "provide it. In the other <strong>44 states</strong> the company "
        "may offer monitoring, but the law does not make it.</p>"
    )
    parts.append(
        "<p>The protection that does not depend on the company is a "
        "credit freeze. In every state you can freeze your credit with "
        "each of the three credit bureaus for free — that right comes "
        "from federal law. A freeze stops anyone from opening a new "
        "account in your name. You can lift it temporarily when you need "
        "credit yourself. A fraud alert is the lighter option: it tells "
        "lenders to check your identity before opening an account, and "
        "it lasts one year (or seven years for an extended alert).</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Freeze your credit "
        "at all three bureaus — it is free, and it is the single "
        "strongest step you can take. Your state&rsquo;s card below has "
        "the details for your state.</p>"
    )
    parts.append("</div>")
    # --- Card 4: can you sue? ---
    parts.append('<div class="card">')
    parts.append("<h3>Can you sue the company?</h3>")
    parts.append(
        "<p>In only <strong>4 states</strong> does the breach law clearly "
        "let you sue the company yourself: Hawaii, Louisiana, Tennessee, "
        "and Washington. In <strong>12 states</strong> the right is "
        "limited — for example, California lets you sue only under its "
        "separate privacy law, and only for certain kinds of breaches. "
        "In <strong>34 states</strong> there is no private right under "
        "the breach law at all: only the attorney general can enforce "
        "it.</p>"
    )
    parts.append(
        "<p>No private right under the breach law does not always mean no "
        "lawsuit. You may still have a claim under a different law — a "
        "consumer-protection law, or a negligence claim — but that is "
        "harder to prove and depends on your state&rsquo;s courts. If "
        "you lost money because of a breach, that is the question to "
        "take to a lawyer, not to guess at yourself.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you lost money, "
        "save every document — the breach letter, bank statements "
        "showing the loss, anything you spent fixing it. Then talk to "
        "the legal aid linked in your state&rsquo;s card, or a consumer "
        "lawyer, before any deadline passes.</p>"
    )
    parts.append("</div>")
    # --- Card 5: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Data breach response in {esc(state)}</h3>")
    parts.append(
        f"<p><strong>How fast must they tell you:</strong> {esc(e['notification_deadline'])}. {esc(e['notification_deadline_note'])}</p>"
    )
    parts.append(
        f"<p><strong>Does the attorney general get told:</strong> {ag_word(e['ag_notification'])}. {esc(e['ag_notification_note'])}</p>"
    )
    credit_note = e.get("credit_monitoring_note") or ""
    credit_suffix = f" {esc(credit_note)}" if credit_note else ""
    parts.append(
        f"<p><strong>Credit monitoring:</strong> {credit_word(e['credit_monitoring'])}.{credit_suffix}</p>"
    )
    private_note = e.get("private_right_of_action_note") or ""
    private_suffix = f" {esc(private_note)}" if private_note else ""
    parts.append(
        f"<p><strong>Can you sue:</strong> {private_word(e['private_right_of_action'])}.{private_suffix}</p>"
    )
    parts.append(
        f"<p><strong>Freezing your credit:</strong> {esc(e['freeze_rights_note'])}</p>"
    )
    parts.append(
        f"<p><strong>The law:</strong> {esc(e['statute_name'])} — {esc(e['statute_cite'])}</p>"
    )
    parts.append(
        f"<p><strong>Where to report a breach:</strong> "
        f'<a href="{esc(e["agency_url"])}" target="_blank" rel="noopener">{esc(e["agency_name"])}</a>.</p>'
    )
    if e["state_note"]:
        parts.append(f"<p>{esc(e['state_note'])}</p>")
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Start with the "
        "attorney general&rsquo;s office linked above if you were never "
        "told about a breach or the company is not answering. Freeze "
        "your credit, change reused passwords, and keep the breach "
        "letter. If you lost money, talk to the legal aid above before "
        "any deadline passes.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Freeze your "
        "credit at all three bureaus — it is free. (2) Change the "
        "password on any account that used the same password as the "
        "breached one. (3) Read the breach letter carefully for what "
        "was exposed and what the company is offering. (4) If the "
        "company never told you, report the breach to your attorney "
        "general&rsquo;s office. (5) If you lost money, save every "
        "document and talk to legal aid before any deadline passes.</p>"
    )
    parts.append(
        "<p><em>Sources: the official state breach-notification statutes, "
        "attorneys general, and legal aid organizations linked in the "
        "research for this section, checked November 20, 2026. Breach "
        "laws change — confirm the current law with your attorney "
        "general&rsquo;s office before you rely on it. This is general "
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
            f"Data breach response in {state}</a></li>\n"
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
        '<option value="zoning-variances-land-use" data-anchor="zoning-variances-land-use">'
        "Zoning, variances &amp; land use (variances, nonconforming uses, appeals, deadlines)</option>"
    )
    assert opt_old in text, "zoning helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="data-breach-response" data-anchor="data-breach-response">'
        "Data breach response (notice deadlines, attorney general notice, credit monitoring, can you sue)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="zoning-variances-land-use"'
    idx = text.find(card_anchor)
    assert idx != -1, "zoning card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="data-breach-response">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-data-breach-response.jpg" alt="Data breach response" loading="lazy"></span>
          <h3>Data Breach Response</h3>
          <p>Your personal information was exposed in a data breach. How fast the company must tell you, whether the attorney general gets told, whether you get free credit monitoring, and whether you can sue &mdash; state by state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 55 topics" in text, "show-all label not found"
    text = text.replace("Show all 55 topics", "Show all 56 topics", 1)
    show_pos = text.find("Show all 56 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">55 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("55 topics", "56 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 55->56")


def build_about():
    text = ABOUT.read_text()
    assert text.count("100 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("100 legal topics", "101 legal topics", 1))
    print("  about.html: 100 -> 101")


def state_index_t(state, slug, e):
    bits = [
        "data breach response breach notification identity theft credit freeze",
        f"Data breach response in {state}",
        f"notification deadline {e['notification_deadline']} {e['notification_deadline_note']}",
        f"attorney general notice {ag_word(e['ag_notification']).lower()} {e['ag_notification_note']}",
        f"credit monitoring {credit_word(e['credit_monitoring']).lower()} {e.get('credit_monitoring_note') or ''}",
        f"can you sue {private_word(e['private_right_of_action']).lower()} {e.get('private_right_of_action_note') or ''}",
        f"freeze your credit {e['freeze_rights_note']}",
        f"{e['statute_name']} {e['statute_cite']}",
        f"{e['agency_name']}",
        f"{e['state_note'] or ''}",
        f"{e['legal_aid_name']}",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11518, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Data breach response in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Data Breach Response",
            "t": (
                "data-breach-response Data Breach Response? "
                "Your personal information was exposed in a data breach. How fast the company must tell you, "
                "whether the attorney general gets told, whether you get free credit monitoring, "
                "and whether you can sue — state by state. "
                "breach notification deadline attorney general credit monitoring credit freeze identity theft can you sue."
            ),
        }
    )
    assert len(idx) == 11569, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11518 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    assert len(d) == 50, len(d)
    data = [(k, d[k]) for k in sorted(d)]  # keys already lowercase
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "notification_deadline", "notification_deadline_note", "ag_notification",
        "ag_notification_note", "credit_monitoring", "private_right_of_action",
        "freeze_rights_note", "statute_name", "statute_cite", "agency_name",
        "agency_url", "legal_aid_name", "legal_aid_url", "state_note", "sources",
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
        assert e["ag_notification"] in ("yes", "varies", "no"), f"{k}: bad ag_notification"
        assert e["credit_monitoring"] in ("required", "varies", "not-required"), f"{k}: bad credit_monitoring"
        assert e["private_right_of_action"] in ("yes", "limited", "no"), f"{k}: bad private_right_of_action"
        assert e["notification_deadline"] and e["notification_deadline_note"] and e["ag_notification_note"] and e["freeze_rights_note"] and e["statute_name"] and e["statute_cite"] and e["agency_name"] and e["agency_url"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"], f"{k}: empty required field"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before zoning-variances-land-use section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
