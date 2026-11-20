#!/usr/bin/env python3
"""Build Topic #93: Self-Defense & Use of Force — standalone section on all
50 state pages.

Inserts one new section per state page (before Social Security Retirement &
Survivors Benefits, newest-first), a contents-list entry (before the
retirement-survivors <li>), a homepage helper option + topic card (after
Social Security Retirement & Survivors Benefits), bumps About 91 -> 92, and
appends 50 state entries + 1 helper entry to assets/search-index.json
(11059 -> 11110).

Data: hidden_files/topic-research/self-defense-use-of-force/all-states.json
(coordinator-built 2026-11-20 from 5 research batches; all 50 legal-aid URLs
curl/browser-verified alive; MN § 609.06 and FL § 776.012 spot-verified
against official statute text; MD and VA are case-law only by design, so
their statute fields are null; VT is coded "limited" with the conflict
explained in the notes, per the site's show-the-disagreement rule).
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "self-defense-use-of-force" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-self-defense-use-of-force.jpg"

SLUG = "self-defense-use-of-force"
TITLE = "Self-Defense & Use of Force"
PREV_SLUG = "social-security-retirement-survivors"

# Extra statewide help links for states whose main legal-aid listing is
# regional only (all three verified alive 2026-11-20).
EXTRAS = {
    "new york": ("LawHelpNY", "https://www.lawhelpny.org/",
                 "statewide directory of free legal services in New York"),
    "arizona": ("Southern Arizona Legal Aid", "https://www.sazlegalaid.org/",
                "free legal help in southern and southeastern Arizona"),
    "missouri": ("Missouri Legal Services", "https://lsmo.org/",
                 "statewide portal that routes you to the legal-aid program for your county"),
}


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def word(v):
    return {"yes": "Yes", "no": "No", "limited": "It depends"}.get(v, v)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="self-defense-use-of-force-in-{slug}">Self-defense &amp; use of force in {esc(state)}</h2>'
    )
    parts.append(
        "<p>Every state lets you defend yourself against an attack, but the "
        "rules about <strong>when</strong> you may use force, <strong>how much</strong> "
        "force, and whether you must <strong>retreat first</strong> are very "
        "different from state to state. This section explains the three rules "
        "that matter most &mdash; stand your ground, the castle doctrine, and the "
        "duty to retreat &mdash; and what " + esc(state) + " says about each one. "
        "This is the picture as of <strong>November 2026</strong>. This is general "
        "information, not legal advice. If you have used force, or think you may "
        "have to, talk to a criminal defense lawyer before you talk to police "
        "about what happened.</p>"
    )
    # --- Card 1: stand your ground ---
    parts.append('<div class="card">')
    parts.append("<h3>Stand your ground: what it means</h3>")
    parts.append(
        "<p>In a <strong>stand-your-ground</strong> state, you have no duty to "
        "retreat before using force in self-defense when you are in a place you "
        "have a legal right to be, you did not start the fight, and you are not "
        "breaking the law. You may stand where you are and defend yourself, "
        "including with deadly force if the threat calls for it. In states "
        "without stand your ground, the law may require you to walk away if you "
        "safely can &mdash; that is the duty to retreat, covered below.</p>"
    )
    parts.append(
        "<p>Stand your ground does <strong>not</strong> mean you can use force "
        "whenever you feel threatened. The force must still be reasonable and "
        "necessary against an imminent attack, and the protection is lost if you "
        "provoked the fight or were committing a crime. Some states have "
        "stand-your-ground protection only in limited situations &mdash; for "
        "example, only when the attacker has a weapon &mdash; so read your "
        "state&rsquo;s card below.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check the state card below for "
        "whether " + esc(state) + " is a stand-your-ground state. If it is not, "
        "know that walking away safely is not cowardice &mdash; it is what the "
        "law expects, and it keeps your self-defense claim intact.</p>"
    )
    parts.append("</div>")
    # --- Card 2: castle doctrine ---
    parts.append('<div class="card">')
    parts.append("<h3>The castle doctrine: your home</h3>")
    parts.append(
        "<p>The <strong>castle doctrine</strong> says your home is your castle: "
        "inside it, you have no duty to retreat from an intruder. In most states "
        "the law also <strong>presumes</strong> that you reasonably feared death "
        "or serious injury when someone unlawfully and forcibly enters your home, "
        "which makes a self-defense claim much stronger. The doctrine usually "
        "covers your home and sometimes your occupied vehicle or workplace &mdash; "
        "not your yard, your porch, or a public place.</p>"
    )
    parts.append(
        "<p>Two limits to know: the presumption usually does <strong>not</strong> "
        "apply against someone who also has a right to be there, like a lawful "
        "resident or a co-occupant, and it does not cover chasing someone who is "
        "already leaving. Force must still be reasonable for the threat in front "
        "of you.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If someone breaks in, call 911 "
        "as soon as you safely can, stay inside if you can, and do not go after "
        "a fleeing intruder. The castle doctrine protects you while you defend "
        "your home &mdash; not while you pursue someone outside it.</p>"
    )
    parts.append("</div>")
    # --- Card 3: duty to retreat ---
    parts.append('<div class="card">')
    parts.append("<h3>Duty to retreat: when you must walk away</h3>")
    parts.append(
        "<p>In a <strong>duty-to-retreat</strong> state, you may not use deadly "
        "force in public if you know you can avoid it with complete safety by "
        "retreating &mdash; walking away, leaving the area, or giving up property. "
        "The duty usually does <strong>not</strong> apply inside your own home or "
        "workplace, and it never requires you to retreat into greater danger. "
        "Whether a safe escape existed is judged on the facts at the time, which "
        "is why these cases turn on details.</p>"
    )
    parts.append(
        "<p>Some states sit in the middle: no statute says you must retreat, but a "
        "jury may still weigh whether you could have walked away when deciding if "
        "your force was reasonable. Those states are marked &ldquo;It depends&rdquo; "
        "in the state card below, with the reason in the note.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you can safely walk away "
        "from a confrontation in public, walk away. It is the safest choice "
        "physically and legally, and in a duty-to-retreat state it is what the "
        "law requires.</p>"
    )
    parts.append("</div>")
    # --- Card 4: deadly force limits ---
    parts.append('<div class="card">')
    parts.append("<h3>Deadly force: the limits</h3>")
    parts.append(
        "<p>Deadly force is justified only when you reasonably believe it is "
        "necessary to prevent imminent death, great bodily harm, or a serious "
        "violent felony against you or someone else. That is the rule in every "
        "state, including stand-your-ground states. Deadly force is <strong>never</strong> "
        "justified to protect property alone, against an insult, or against "
        "someone who is already fleeing.</p>"
    )
    parts.append(
        "<p>If you were the <strong>initial aggressor</strong> &mdash; you started "
        "the fight &mdash; you usually lose the self-defense claim unless you "
        "clearly tried to stop and communicated that you wanted to stop. If you "
        "were committing a crime when you used force, the protection is usually "
        "lost too.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Use the least force that will "
        "keep you safe, and stop as soon as the threat stops. The moment the "
        "attacker is down, disarmed, or running away, the legal justification "
        "for force ends.</p>"
    )
    parts.append("</div>")
    # --- Card 5: after you use force ---
    parts.append('<div class="card">')
    parts.append("<h3>After you use force: what to do</h3>")
    parts.append(
        "<p><strong>Call 911.</strong> Report that you were attacked and that you "
        "defended yourself, and ask for medical help if anyone is hurt. Then "
        "<strong>say very little</strong> about the facts until you have a lawyer: "
        "give your name, say you were attacked, say you want a lawyer, and stop "
        "there. Anything you say to police can be used against you, even if you "
        "believe you were fully justified.</p>"
    )
    parts.append(
        "<p>Do <strong>not</strong> leave the scene if it is safe to stay, do not "
        "move or clean up evidence, and do not talk about what happened on social "
        "media. Write down what happened as soon as you can &mdash; who, where, "
        "when, and what the other person did &mdash; and save any photos, video, "
        "or messages. If there were witnesses, get their names.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Call 911, ask for a lawyer, "
        "and say nothing about the facts without one. Then call the free legal "
        "help in the state card below &mdash; they can point you to a criminal "
        "defense lawyer.</p>"
    )
    parts.append("</div>")
    # --- Card 6: what it does not cover ---
    parts.append('<div class="card">')
    parts.append("<h3>What self-defense does not cover</h3>")
    parts.append(
        "<p>Self-defense is not a free pass. It does not cover force used "
        "to <strong>get revenge</strong> after an attack is over, force against "
        "someone who is <strong>fleeing</strong>, force used because you were "
        "insulted or offended, or force to <strong>protect property alone</strong>. "
        "It does not cover a fight you started and then escalated, and it does "
        "not cover using more force than the threat required.</p>"
    )
    parts.append(
        "<p>It also does not automatically protect you from a <strong>civil "
        "lawsuit</strong>: some states give you immunity from being sued when "
        "your force was justified, but many do not, and even in states that do, "
        "you may have to prove the force was justified first.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you are unsure whether your "
        "situation counts as self-defense, treat it as uncertain and get a lawyer "
        "before you say or do anything that assumes you were justified.</p>"
    )
    parts.append("</div>")
    # --- Card 7: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Self-defense &amp; use of force in {esc(state)}</h3>")
    parts.append(
        f"<p><strong>Stand your ground?</strong> {word(e['stand_your_ground'])}. {esc(e['syg_note'])}</p>"
    )
    parts.append(
        f"<p><strong>Castle doctrine?</strong> {word(e['castle_doctrine'])}. {esc(e['castle_note'])}</p>"
    )
    parts.append(
        f"<p><strong>Duty to retreat outside the home?</strong> {word(e['duty_to_retreat'])}. {esc(e['retreat_note'])}</p>"
    )
    if e["statute_cite"]:
        parts.append(
            f"<p><strong>The law:</strong> {esc(e['statute_name'])} &mdash; {esc(e['statute_cite'])}.</p>"
        )
    else:
        parts.append(
            "<p><strong>The law:</strong> No statute &mdash; this state&rsquo;s "
            "self-defense rules come from court decisions, not a statute.</p>"
        )
    if e["state_note"]:
        parts.append(f"<p>{esc(e['state_note'])}</p>")
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
    extra = EXTRAS.get(slug)
    if extra:
        parts.append(
            f"<p><strong>Also:</strong> "
            f'<a href="{esc(extra[1])}" target="_blank" rel="noopener">{esc(extra[0])}</a> '
            f"&mdash; {esc(extra[2])}.</p>"
        )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check the three answers above "
        "for your state, remember that deadly force is only for imminent death or "
        "serious injury, and if you ever use force, call 911 and a lawyer before "
        "you explain what happened.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Learn your state&rsquo;s "
        "three answers above &mdash; stand your ground, castle doctrine, duty to "
        "retreat. (2) Remember the limits: no force for property alone, no force "
        "against a fleeing person, no force if you started it. (3) If you use "
        "force, call 911, say you were attacked, ask for a lawyer, and say nothing "
        "about the facts without one. (4) If you are charged, get a criminal "
        "defense lawyer &mdash; the free legal help above can point you to one. "
        "(5) If you carry a firearm, see the "
        f'<a href="#carry-permit-reciprocity-in-{slug}">Carry permit reciprocity &amp; travel</a> '
        "and "
        f'<a href="#pulled-over-in-{slug}">Pulled Over</a> '
        "sections on this page.</p>"
    )
    parts.append(
        "<p><em>Sources: the official state statutes and court sources linked in "
        "the research for this section, checked November 20, 2026. Self-defense "
        "law is fact-specific and changes &mdash; confirm the current law with a "
        "lawyer before you rely on it. This is general information, not legal "
        "advice.</em></p>"
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
            f"Self-defense &amp; use of force in {state}</a></li>\n"
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
        '<option value="social-security-retirement-survivors" data-anchor="social-security-retirement-survivors">'
        "Social Security retirement &amp; survivors benefits (when to claim, survivors benefits, taxes on benefits, appeals)</option>"
    )
    assert opt_old in text, "retirement-survivors helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="self-defense-use-of-force" data-anchor="self-defense-use-of-force">'
        "Self-defense &amp; use of force (stand your ground, castle doctrine, duty to retreat, what to do after)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="social-security-retirement-survivors"'
    idx = text.find(card_anchor)
    assert idx != -1, "retirement-survivors card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="self-defense-use-of-force">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-self-defense-use-of-force.jpg" alt="Self-defense and use of force" loading="lazy"></span>
          <h3>Self-Defense &amp; Use of Force</h3>
          <p>When you can stand your ground, the castle doctrine at home, when you must retreat, and what to do after you use force.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 46 topics" in text, "show-all label not found"
    text = text.replace("Show all 46 topics", "Show all 47 topics", 1)
    show_pos = text.find("Show all 47 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">46 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("46 topics", "47 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 46->47")


def build_about():
    text = ABOUT.read_text()
    assert text.count("91 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("91 legal topics", "92 legal topics", 1))
    print("  about.html: 91 -> 92")


def state_index_t(state, slug, e):
    bits = [
        "self defense use of force stand your ground castle doctrine duty to retreat",
        f"Self-defense & use of force in {state}",
        f"stand your ground {word(e['stand_your_ground']).lower()} {e['syg_note']}",
        f"castle doctrine {word(e['castle_doctrine']).lower()} {e['castle_note']}",
        f"duty to retreat {word(e['duty_to_retreat']).lower()} {e['retreat_note']}",
        "deadly force only against imminent death great bodily harm serious violent felony never for property alone",
        "after using force call 911 ask for a lawyer say nothing about the facts without one",
        "initial aggressor provocation fleeing attacker no self defense",
        f"{e['statute_name'] or 'case law'} {e['statute_cite'] or ''}",
        f"{e['state_note'] or ''}",
        f"{e['legal_aid_name']}",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11059, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Self-defense & use of force in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Self-Defense & Use of Force",
            "t": (
                "self-defense-use-of-force self defense use of force Self-Defense "
                "& Use of Force? When you can stand your ground, the castle "
                "doctrine at home, when you must retreat, and what to do after "
                "you use force. Stand your ground castle doctrine duty to retreat "
                "deadly force only against imminent death or great bodily harm "
                "never for property alone call 911 ask for a lawyer."
            ),
        }
    )
    assert len(idx) == 11110, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11059 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [(k, states[k]) for k in sorted(states)]
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "stand_your_ground", "syg_note", "castle_doctrine", "castle_note",
        "duty_to_retreat", "retreat_note", "statute_name", "statute_cite",
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
        assert e["stand_your_ground"] in ("yes", "no", "limited"), f"{k}: bad stand_your_ground"
        assert e["castle_doctrine"] in ("yes", "no"), f"{k}: bad castle_doctrine"
        assert e["duty_to_retreat"] in ("yes", "no", "limited"), f"{k}: bad duty_to_retreat"
        assert e["syg_note"] and e["castle_note"] and e["retreat_note"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"], f"{k}: empty required field"
        assert (e["statute_name"] is None) == (e["statute_cite"] is None), f"{k}: statute name/cite mismatch"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before social-security-retirement-survivors section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
