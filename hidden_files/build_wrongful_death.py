#!/usr/bin/env python3
"""Build Topic #91: Wrongful Death — standalone section on all 50 state pages.

Inserts one new section per state page (before Sexual Harassment at Work,
newest-first), a contents-list entry (before the harassment <li>), a homepage
helper option + topic card (after Sexual Harassment at Work), bumps About
89 -> 90, and appends 50 state entries + 1 helper entry to
assets/search-index.json (10957 -> 11008).

Data: hidden_files/topic-research/wrongful-death/all-states.json
(coordinator-built 2026-11-20 from 5 research batches).
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "wrongful-death" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-wrongful-death.jpg"

SLUG = "wrongful-death"
TITLE = "Wrongful Death"
PREV_SLUG = "sexual-harassment-at-work"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="wrongful-death-in-{slug}">Wrongful death in {esc(state)}</h2>'
    )
    parts.append(
        "<p>When someone dies because of another person&rsquo;s or company&rsquo;s "
        "negligence or wrongdoing &mdash; a careless driver, a dangerous product, "
        "a doctor&rsquo;s mistake, an unsafe workplace &mdash; the surviving family "
        "may have a civil claim called a <strong>wrongful death</strong> claim. It "
        "is separate from any criminal case: the state can prosecute a killing "
        "whether or not the family sues, and the family can sue whether or not "
        "anyone is charged. The claim is about money &mdash; the income, support, "
        "and companionship the family lost &mdash; not about punishment. This "
        "section is the " + esc(state) + " picture as of "
        "<strong>November 2026</strong> &mdash; who can file, the deadline, what "
        "can be recovered, and what to do first. This is general information, not "
        "legal advice. The deadlines are short, so <strong>do not wait</strong>: in "
        "most states you have one to three years from the death to file.</p>"
    )
    # --- Card 1: what it is ---
    parts.append('<div class="card">')
    parts.append("<h3>What is a wrongful death claim?</h3>")
    parts.append(
        "<p>A wrongful death claim says the death was caused by someone else&rsquo;s "
        "fault &mdash; negligence, recklessness, or an intentional act &mdash; and "
        "that the survivors lost something real because of it: income the person "
        "would have earned, care and guidance for the children, companionship for "
        "a spouse, funeral and medical bills. The claim belongs to the survivors "
        "and the estate, not to the person who died.</p>"
    )
    parts.append(
        "<p>It is <strong>not</strong> the same as a criminal case. A criminal case "
        "is brought by the state and can end in prison. A wrongful death case is "
        "brought by the family and can end in money damages. The two can run at "
        "the same time, and a family can win a civil case even if the criminal "
        "case fails &mdash; the burden of proof is lower in civil court.</p>"
    )
    parts.append(
        "<p>Common causes: car and truck crashes, medical mistakes, dangerous "
        "drugs or products, workplace accidents, nursing-home neglect, and "
        "violence. If the person who died could have sued for their injuries had "
        "they lived, the family usually has a wrongful death claim.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> The next cards are your checklist. "
        "The most important thing to know up front is that the clock is already "
        "running &mdash; see the deadline card below.</p>"
    )
    parts.append("</div>")
    # --- Card 2: who can file ---
    parts.append('<div class="card">')
    parts.append("<h3>Who can file</h3>")
    parts.append(
        "<p>Every state limits who may bring the claim. In most states the claim is "
        "filed by the <strong>personal representative</strong> of the estate "
        "(the executor named in a will, or an administrator appointed by the "
        "probate court) on behalf of the survivors. In some states the surviving "
        "spouse, children, or parents file directly. Who counts as a survivor, "
        "and how the money is divided among them, is set by state law &mdash; your "
        "state&rsquo;s rule is in the state card below.</p>"
    )
    parts.append(
        "<p>If there is no will, a family member can ask the probate court to be "
        "appointed as personal representative. That step is usually quick, and a "
        "probate lawyer or legal-aid office can walk you through it.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Find out who your state allows "
        "to file (state card below). If you are the spouse or a parent and no "
        "estate has been opened, ask the probate court about being appointed "
        "personal representative &mdash; that is usually the first legal step.</p>"
    )
    parts.append("</div>")
    # --- Card 3: deadline ---
    parts.append('<div class="card">')
    parts.append("<h3>The deadline: the clock is short</h3>")
    parts.append(
        "<p>Every state sets a <strong>statute of limitations</strong> for wrongful "
        "death &mdash; usually one to three years from the date of death. Miss it "
        "and the claim is gone, no matter how strong the facts are. A few states "
        "pause the clock for minor children, or start it when the cause of death "
        "is discovered rather than on the date of death. Your state&rsquo;s deadline "
        "is in the state card below.</p>"
    )
    parts.append(
        "<p>Two traps: <strong>(1)</strong> if a government agency is involved "
        "(a city bus, a public hospital, a state road), many states require a "
        "formal notice of claim within months &mdash; far shorter than the lawsuit "
        "deadline. <strong>(2)</strong> A criminal investigation does not pause the "
        "civil deadline. Do not wait for charges or a trial to start the claim.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Find your state&rsquo;s deadline "
        "in the card below and talk to a lawyer or legal-aid office well before "
        "it. Most wrongful-death lawyers work on contingency &mdash; no fee unless "
        "you win &mdash; and the first consultation is usually free.</p>"
    )
    parts.append("</div>")
    # --- Card 4: damages ---
    parts.append('<div class="card">')
    parts.append("<h3>What money can be recovered</h3>")
    parts.append(
        "<p>Damages usually fall into a few buckets: <strong>economic losses</strong> "
        "&mdash; the income and benefits the person would have earned, medical "
        "bills before death, funeral and burial costs; <strong>loss of "
        "companionship and guidance</strong> &mdash; what a spouse, child, or "
        "parent lost in the relationship; and in some states, the person&rsquo;s own "
        "pain and suffering before death (a separate &ldquo;survival&rdquo; claim). "
        "A few states allow <strong>punitive damages</strong> to punish especially "
        "reckless conduct; some cap non-economic damages. What your state allows "
        "is in the state card below.</p>"
    )
    parts.append(
        "<p>There is no fixed formula. Lawyers and courts look at the person&rsquo;s "
        "age, earnings, health, and the family&rsquo;s dependence on them. Keep every "
        "bill and every record of income &mdash; pay stubs, tax returns, benefit "
        "statements.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Start a folder now: the death "
        "certificate, medical and funeral bills, pay stubs and tax returns, and "
        "any insurance letters. Do not throw anything away.</p>"
    )
    parts.append("</div>")
    # --- Card 5: what to do right now ---
    parts.append('<div class="card">')
    parts.append("<h3>What to do right now</h3>")
    parts.append(
        "<p><strong>Preserve evidence.</strong> Photos of the scene or vehicle, "
        "medical records, the police or accident report, names of witnesses. "
        "Evidence disappears fast &mdash; vehicles get repaired, records get "
        "purged, memories fade. Ask a lawyer to send a preservation letter if "
        "a company or hospital holds records.</p>"
    )
    parts.append(
        "<p><strong>Do not give a recorded statement to an insurer.</strong> The other "
        "side&rsquo;s insurance company may call quickly and ask for a statement or "
        "offer a fast settlement. You are not required to give a recorded "
        "statement, and an early offer is almost always less than the claim is "
        "worth. Talk to a lawyer first.</p>"
    )
    parts.append(
        "<p><strong>Do not sign anything.</strong> Releases, settlements, or waivers "
        "from an insurer, an employer, or a hospital can end the claim. Have a "
        "lawyer or legal-aid office read anything before you sign.</p>"
    )
    parts.append(
        "<p><strong>Get the personal representative appointed.</strong> If the claim "
        "must be filed by the estate, open probate and get appointed &mdash; the "
        "court, a probate lawyer, or legal aid can help, and it is usually "
        "straightforward.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Preserve the evidence, say no to "
        "recorded statements and quick settlements, get the estate opened, and "
        "call a wrongful-death lawyer or legal aid &mdash; the first call is "
        "usually free, and most take these cases on contingency.</p>"
    )
    parts.append("</div>")
    # --- Card 6: what NOT to do ---
    parts.append('<div class="card">')
    parts.append("<h3>What NOT to do</h3>")
    parts.append(
        "<p><strong>Do not wait out the deadline.</strong> Grief is real, and the "
        "legal clock does not pause for it. A lawyer can file the claim while "
        "the family grieves &mdash; that is the point of hiring one.</p>"
    )
    parts.append(
        "<p><strong>Do not post about the death or the accident on social media.</strong> "
        "Insurers and defense lawyers read it, and a post can be used against "
        "the claim.</p>"
    )
    parts.append(
        "<p><strong>Do not accept the first settlement offer.</strong> Early offers "
        "come before the full losses are known &mdash; future income, ongoing "
        "care for children, the full medical picture. Once you sign, it is over.</p>"
    )
    parts.append(
        "<p><strong>Do not assume a criminal case covers it.</strong> A conviction "
        "does not pay the family, and an acquittal does not end the civil claim. "
        "They are separate tracks.</p>"
    )
    parts.append("</div>")
    # --- Card 7: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Wrongful death in {esc(state)}</h3>")
    if e["who_can_file"]:
        parts.append(f"<p><strong>Who can file:</strong> {esc(e['who_can_file'])}</p>")
    if e["statute_name"]:
        cite = f" ({esc(e['statute_cite'])})" if e["statute_cite"] else ""
        parts.append(f"<p><strong>The law:</strong> {esc(e['statute_name'])}{cite}.</p>")
    if e["deadline_note"]:
        parts.append(f"<p><strong>Deadline in {esc(state)}:</strong> {esc(e['deadline_note'])}</p>")
    if e["damages_note"]:
        parts.append(f"<p><strong>What can be recovered:</strong> {esc(e['damages_note'])}</p>")
    if e["state_note"]:
        parts.append(f"<p>{esc(e['state_note'])}</p>")
    if e["phone"]:
        parts.append(
            f"<p><strong>{esc(e['phone_label'])} phone:</strong> {esc(e['phone'])}.</p>"
        )
    if e["legal_aid_url"]:
        parts.append(
            f"<p><strong>Free legal help:</strong> "
            f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
        )
    else:
        parts.append(
            f"<p><strong>Free legal help:</strong> {esc(e['legal_aid_name'])} &mdash; no "
            "website link could be verified; search the name to find their intake line.</p>"
        )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Get the estate opened if one is "
        "needed, preserve the evidence, and call a wrongful-death lawyer or the "
        "legal-aid office above well before the deadline. The first consultation "
        "is usually free, and most of these cases are taken on contingency.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Get the death certificate and "
        "start a folder with bills, pay stubs, and tax returns. (2) Preserve "
        "evidence: photos, reports, witness names, medical records. (3) Do not "
        "give a recorded statement or sign anything from an insurer. (4) Get a "
        "personal representative appointed if the estate must file. (5) Call a "
        "wrongful-death lawyer or legal aid well before your state&rsquo;s deadline "
        "&mdash; the first call is usually free. (6) Do not post about the case "
        "on social media.</p>"
    )
    parts.append(
        "<p><em>Sources: the official " + esc(state) +
        " statute, court, and legal-aid sources linked above, checked November 20, "
        "2026. Deadlines and damage rules change &mdash; confirm the current "
        "deadline with a lawyer or the court before you file. This is general "
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
            f"Wrongful death in {state}</a></li>\n"
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
        '<option value="sexual-harassment-at-work" data-anchor="sexual-harassment-at-work">'
        "Sexual harassment at work (what counts, what to do, deadlines, filing a complaint, retaliation)</option>"
    )
    assert opt_old in text, "harassment helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="wrongful-death" data-anchor="wrongful-death">'
        "Wrongful death (who can file, the deadline, what can be recovered, what to do first)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="sexual-harassment-at-work"'
    idx = text.find(card_anchor)
    assert idx != -1, "harassment card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="wrongful-death">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-wrongful-death.jpg" alt="Wrongful death" loading="lazy"></span>
          <h3>Wrongful Death</h3>
          <p>When someone dies because of another person&rsquo;s negligence or wrongdoing. Who can file, the deadline, what can be recovered, and what to do first in your state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 44 topics" in text, "show-all label not found"
    text = text.replace("Show all 44 topics", "Show all 45 topics", 1)
    show_pos = text.find("Show all 45 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">44 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("44 topics", "45 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 44->45")


def build_about():
    text = ABOUT.read_text()
    assert text.count("89 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("89 legal topics", "90 legal topics", 1))
    print("  about.html: 89 -> 90")


def state_index_t(state, slug, e):
    bits = [
        "wrongful-death wrongful death death caused by negligence",
        f"Wrongful death in {state}",
        "who can file personal representative surviving spouse children parents",
        "statute of limitations deadline from date of death",
        "damages economic losses loss of companionship funeral medical bills punitive",
        "what to do preserve evidence no recorded statement do not sign",
        "what not to do wait out deadline social media first settlement criminal case",
        f"{e['who_can_file'] or ''}",
        f"{e['statute_name'] or ''} {e['statute_cite'] or ''}",
        f"deadline in {state}: {e['deadline_note']}",
        f"what can be recovered: {e['damages_note']}",
        f"{e['state_note'] or ''}",
        f"{e['legal_aid_name']}",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 10957, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Wrongful death in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Wrongful Death",
            "t": (
                "wrongful-death wrongful death Wrongful death? When someone dies "
                "because of another person\u2019s negligence or wrongdoing. Who can "
                "file, the deadline, what can be recovered, and what to do first in "
                "your state. Personal representative surviving spouse children "
                "parents statute of limitations deadline damages economic losses "
                "loss of companionship funeral medical bills punitive do not sign "
                "no recorded statement preserve evidence contingency lawyer free "
                "consultation."
            ),
        }
    )
    assert len(idx) == 11008, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 10957 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [(k, states[k]) for k in sorted(states)]
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "who_can_file", "statute_name", "statute_cite",
        "deadline_note", "damages_note", "legal_aid_name", "legal_aid_url",
        "phone", "phone_label", "state_note", "sources",
    ]
    phone_re = re.compile(
        r"\(\d{3}\)\s*\d{3}[-.]\d{4}|\b\d{3}[-.]\d{3}[-.]\d{4}\b|"
        r"1-800-\d{3}-\d{4}|1-866-\d{3}-\d{4}|1-888-\d{3}-\d{4}|"
        r"877-\d{3}-\d{4}|800-\d{3}-\d{4}|844-\d{3}-\d{4}|866-\d{3}-\d{4}|"
        r"1-877-\d{3}-\d{4}|1-833-[A-Z0-9]{7}"
    )
    for k, e in data:
        for f in req:
            assert f in e, f"{k}: missing {f}"
        assert e["deadline_note"] and e["damages_note"] and e["who_can_file"] and e["legal_aid_name"] and e["sources"], f"{k}: empty required field"
        blob = json.dumps({f: e[f] for f in req if f not in ("phone", "phone_label")})
        assert not phone_re.search(blob), f"{k}: phone-like string outside phone field"
        if e["phone"]:
            assert phone_re.search(e["phone"]), f"{k}: phone format {e['phone']!r}"
            assert e["phone_label"] in ("Legal aid",), f"{k}: bad phone_label"
        else:
            assert e["phone_label"] is None, f"{k}: phone_label without phone"
    print("building state pages (insert before harassment section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
