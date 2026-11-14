#!/usr/bin/env python3
"""Build Topic #78: Mental-health crisis holds / involuntary commitment.

Inserts one new section per state page (before the Medicare enrollment
section, newest-first), a contents-list entry, a homepage helper option
+ topic card (second grid, after Medicare enrollment), bumps About
76 -> 77, and appends 50 state entries + 1 helper entry to
assets/search-index.json (10294 -> 10345).

Data: hidden_files/topic-research/mental-health-crisis-holds/all-states.json
(coordinator-written; see make_dataset.py for the source trail).

Coordinator verification before the build:
- Hold lengths: ND Legislative Council memo 17.9251.01000 (Mar 2016) x
  Hedman et al., Psychiatric Services 2016, Tables 1-2, x the site's own
  buried Guardianship crisis-hold cards (built from official state
  sources). Where the 2016 sources disagreed with the buried card, the
  buried card's official source was re-checked in-session and won:
  CT 15-day physician's emergency certificate (17a-502, CT DMHAS),
  DE 24h (16 Del. C. 5001/5004), LA 15-day emergency certificate
  (28:53), MT 72h hold (53-21-154), UT 72h (26B-5-331), HI 72h (334-46,
  as amended 2025). Where the two 2016 sources disagreed with each
  other, the current statute text was checked in-session: ID 24h (66-326),
  KY 72h excl. weekends/holidays (202A.031; 18h police phase, 202A.041),
  NH 10 days excl. Sat/Sun (135-C:32), RI 10 days (40.1-5-7), NJ 24h
  screening + 72h to temporary order (30:4-27.5/27.9), NM no fixed hours,
  hearing in 7 days (43-1-10/11), NY 15 days (MHL 9.39), SD 24h hold,
  hearing in 5 days (27A-10), TN judge-ordered hold up to 5 days
  (33-6-401), VT 24h exam + 72h more (18 VSA 7508), WV 72h (27-5-2a),
  NE evaluation within 36h (71-919).
- Hearing deadlines printed for 35 states, each from the statute text or
  an official state source named in make_dataset.py. The other 15 states
  print NO deadline — the card says to ask the facility or court clerk
  for the date in writing.
- Named laws printed for 19 states (Baker Act, 5150, 302, M-1, ECO/TDO,
  Section 12, 9.39, IEA, emergency certification, director's hold, ITA,
  Chapter 51, 24-hour hold, 72-hour hold, emergency certificate,
  emergency protective custody, emergency detention order, physician's
  emergency certificate) — each verified in-session.
- 988 Suicide & Crisis Lifeline confirmed live (browser fetch of
  988lifeline.org, Nov 14, 2026); already printed in the site footer.
  No state-specific crisis line is printed: none was verified against
  two official sources in this build.
- Official links: 44 re-used from the buried Guardianship cards; link
  sweep Nov 14, 2026: 36 returned 200/201, 7 returned 403 (official
  .gov bot filters, kept per the Medicare-build precedent). AK/IL/NY/MI
  links returned 000 and are OMITTED (988 only); AR/GA have no buried
  link (988 only).
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "mental-health-crisis-holds" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"

TOPIC = "mental-health-crisis-holds"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(s):
    state = s["state"]
    slug = s["slug"]
    named = s.get("named")
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="mental-health-crisis-holds-in-{slug}">Mental-Health '
        f"Crisis Holds in {esc(state)}</h2>"
    )
    intro = (
        "A crisis hold is a short emergency detention for evaluation "
        "when someone, because of a mental-health crisis, appears to be "
        "a danger to themselves, a danger to others, or so unable to "
        "care for themselves that they cannot meet basic needs. It is "
        "an evaluation, not a punishment and not a commitment: the "
        "facility has a short window to examine the person, and then "
        "must release them, let them stay voluntarily, or go to court "
        "for longer treatment. "
    )
    if named:
        intro += (
            f"In {esc(state)} this is known as the {esc(named)}. "
        )
    intro += (
        f"The law that sets the rules in {esc(state)} is {esc(s['statute'])}. "
        "This section covers what a hold is, who can start one, how "
        "long it lasts here, the person's rights at a hearing, and "
        "what a hold does not do. The Guardianship section on this "
        "page covers the slower, longer-term court process for someone "
        "who cannot make decisions over months and years \u2014 a hold "
        "is not a guardianship. This is general information, not "
        "legal advice."
    )
    parts.append(f"<p>{intro}</p>")
    # --- What a crisis hold is ---
    parts.append('<div class="card">')
    parts.append("<h3>What a crisis hold is</h3>")
    parts.append(
        "<p>A hold happens in hours, not weeks. Someone in crisis is "
        "taken to a hospital or crisis facility and kept there while "
        "a doctor or other qualified professional examines them and "
        "decides whether they meet the legal test: a mental illness "
        "that makes them a danger to themselves, a danger to others, "
        "or gravely disabled \u2014 unable to provide for their own "
        "food, clothing, shelter, or safety. Being sad, strange, or "
        "difficult is not enough, and a diagnosis alone is not "
        "enough: the law requires recent behavior that shows the "
        "danger. The hold buys time for an evaluation. It does not "
        "decide treatment, and it does not last indefinitely.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you are with "
        "someone in crisis right now, skip the law and go to the "
        "&ldquo;Help right now&rdquo; card below \u2014 call 911 if "
        "anyone is in immediate danger, or call or text 988.</p>"
    )
    parts.append("</div>")
    # --- Who can start one ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Who can start one in {esc(state)} \u2014 and how</h3>")
    parts.append(f"<p>{esc(s['initiators'])}</p>")
    parts.append(
        "<p><strong>How it usually starts:</strong> call 911 and say "
        "plainly that it is a mental-health crisis, where the person "
        "is, and what they have said or done most recently \u2014 "
        "dates, exact words, any threats, any weapons, any medicines "
        "or treatment stopped. Ask for officers trained in crisis "
        "response if your area has them. Or call or text 988 and ask "
        "for the nearest crisis team, or go to an emergency room and "
        "tell the staff the same facts. What helps most is specific, "
        "recent behavior: evaluators and judges act on specifics, "
        "not general worry. Bring a list of the person's medicines, "
        "their doctor or clinic, and any advance directive or crisis "
        "plan they have.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Write down the "
        "specific recent behavior with dates before you call \u2014 "
        "that note is what the officer, the screener, and the judge "
        "will all ask for.</p>"
    )
    parts.append("</div>")
    # --- How long it lasts ---
    parts.append('<div class="card">')
    parts.append(f"<h3>How long the hold lasts in {esc(state)}</h3>")
    parts.append(f"<p><strong>{esc(s['hold'])}</strong></p>")
    if s.get("hold_extra"):
        parts.append(f"<p>{esc(s['hold_extra'])}</p>")
    parts.append(
        "<p><strong>What happens next:</strong> during the hold, a "
        "professional examines the person and decides. Three "
        "outcomes are possible: the person is released because they "
        "no longer meet the test; the person agrees to stay for "
        "treatment voluntarily; or the facility asks a court to "
        "order longer treatment, and a judge decides at a hearing. "
        "The facility cannot simply keep holding the person past "
        "the limit while it waits \u2014 when the clock runs out "
        "without a court order, the person must be released.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Ask the facility, "
        "in writing, when the hold started and when it expires \u2014 "
        "and ask what hearing, if any, has been scheduled.</p>"
    )
    parts.append("</div>")
    # --- Hearing rights ---
    parts.append('<div class="card">')
    parts.append("<h3>Your rights at the hearing</h3>")
    if s.get("hearing"):
        parts.append(f"<p><strong>In {esc(state)}:</strong> {esc(s['hearing'])}</p>")
    else:
        parts.append(
            f"<p>The exact deadline for the hearing is set by "
            f"{esc(state)} law \u2014 ask the facility or the court "
            f"clerk for the date in writing. Do not assume the hold "
            f"can run past it: when the deadline passes without a "
            f"court order, the person must be released.</p>"
        )
    parts.append(
        "<p>At any hearing, the person has the right to be there, to "
        "have a lawyer (appointed free if they cannot pay, in "
        "commitment proceedings), to present evidence and call "
        "witnesses, to question the other side's evidence, and to "
        "argue for a less restrictive option than the hospital. The "
        "state must prove its case by clear and convincing evidence "
        "\u2014 a higher bar than ordinary civil cases. The person "
        "also has the right to be told why they are being held, to "
        "be examined promptly, and to communicate with family and a "
        "lawyer. Nobody can be kept indefinitely on an emergency "
        "hold \u2014 the state must go to court, and the judge "
        "decides.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you are the "
        "person held, ask for a lawyer at once and say you want a "
        "hearing. If you are family, find out which court and which "
        "date \u2014 and show up with the specific facts, not just "
        "your worry.</p>"
    )
    parts.append("</div>")
    # --- What it does NOT do ---
    parts.append('<div class="card">')
    parts.append("<h3>What a hold does NOT do</h3>")
    parts.append(
        "<p><strong>A hold is not a criminal charge.</strong> The "
        "person has not been arrested, has not been charged with a "
        "crime, and a hold by itself is not a criminal record. "
        "Police may be the ones who bring the person in, but the "
        "process is civil, not criminal.</p>"
    )
    parts.append(
        "<p><strong>A hold is not a guardianship.</strong> It does "
        "not appoint anyone to make decisions for the person, and "
        "it does not decide who controls their money, their home, "
        "or their medical care. Guardianship is a separate, slower "
        "court case \u2014 see the Guardianship section on this page.</p>"
    )
    parts.append(
        "<p><strong>A hold does not by itself take away rights.</strong> "
        "Being held for evaluation does not by itself end the "
        "person's right to vote, to make a will, to refuse treatment "
        "outside the emergency, or to make their own decisions once "
        "the hold ends. Longer treatment, and any loss of rights, "
        "requires a separate court order \u2014 and the person can "
        "contest it.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If anyone tells "
        "you the hold means the person is now a criminal, or now "
        "has a guardian, or has now lost their rights \u2014 that is "
        "not what the law says. Ask them to show you the court "
        "order that says so.</p>"
    )
    parts.append("</div>")
    # --- Help right now ---
    parts.append('<div class="card">')
    parts.append("<h3>Help right now</h3>")
    parts.append(
        "<p><strong>Call or text 988</strong> \u2014 the Suicide "
        "&amp; Crisis Lifeline \u2014 free, confidential, and answered "
        "around the clock. Counselors can talk with the person in "
        "crisis, or with you, and can connect you to the nearest "
        "local crisis team. If someone is in immediate danger or "
        "has already hurt themselves, call <strong>911</strong> "
        "first.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> In immediate "
        "danger: 911. In crisis but not immediate danger: call or "
        "text 988 now, and stay with the person until help arrives.</p>"
    )
    parts.append("</div>")
    # --- Official links ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Official links in {esc(state)}</h3>")
    parts.append("<ul>")
    parts.append(
        "<li><a href=\"https://988lifeline.org\" target=\"_blank\" "
        "rel=\"noopener\">988 Suicide &amp; Crisis Lifeline \u2014 "
        "call or text 988, free and 24/7</a></li>"
    )
    if s.get("link"):
        parts.append(
            f"<li><a href=\"{esc(s['link'])}\" target=\"_blank\" "
            f"rel=\"noopener\">{esc(s['link_label'])}</a></li>"
        )
    parts.append("</ul>")
    parts.append("</div>")
    # --- Do this now ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If someone is in "
        "crisis right now, call 911 if there is immediate danger, "
        "or call or text 988. Write down the specific recent "
        "behavior with dates, and take that note to the crisis team "
        "or the emergency room. If the person is already on a hold, "
        "ask the facility in writing when it started, when it "
        "expires, and when the hearing is \u2014 and make sure the "
        "person has a lawyer. A hold is an emergency evaluation, not "
        "a commitment and not a guardianship: longer treatment needs "
        "a judge.</p>"
    )
    parts.append(
        "<p><em>Sources: the emergency-hold statute cited above "
        f"({esc(s['statute'])}); North Dakota Legislative Council "
        "memorandum 17.9251.01000 (March 2016) and Hedman et al., "
        "\u201cState Laws on Emergency Holds for Mental Health "
        "Stabilization,\u201d Psychiatric Services 2016; the "
        "Treatment Advocacy Center emergency-hospitalization chart; "
        "and your state\u2019s official source linked above. Hold "
        "lengths and hearing deadlines change \u2014 confirm the "
        "current law with the facility or the court before you rely "
        "on it. This is general information, not legal advice.</em></p>"
    )
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def build_state_pages(data):
    for s in data:
        slug = s["slug"]
        path = STATES / f"{slug}.html"
        text = path.read_text()
        anchor = f"mental-health-crisis-holds-in-{slug}"
        assert anchor not in text, f"{slug}: anchor already present"
        # --- insert section before Medicare enrollment (newest-first) ---
        h2 = text.find(f'<h2 id="medicare-enrollment-in-{slug}">')
        assert h2 != -1, f"{slug}: medicare-enrollment h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        new_section = section_html(s)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the medicare-enrollment <li> ---
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#medicare-enrollment-in-'
            + re.escape(slug)
            + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: medicare-enrollment contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#mental-health-crisis-holds-in-{slug}">'
            f"Mental-Health Crisis Holds in {s['state']}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert "mental-health-crisis-holds" not in helper_part, "index already has helper option"
    assert 'data-topic="mental-health-crisis-holds"' not in text, "index already has card"
    opt_old = (
        '<option value="medicare-enrollment" data-anchor="medicare-enrollment">'
        "Signing up for Medicare</option>"
    )
    assert opt_old in text, "medicare-enrollment helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="mental-health-crisis-holds" data-anchor="mental-health-crisis-holds">'
        "Mental-health crisis hold (someone in crisis)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="medicare-enrollment"'
    idx = text.find(card_anchor)
    assert idx != -1, "medicare-enrollment card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="mental-health-crisis-holds">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-mental-health-crisis-holds.jpg" alt="Mental-Health Crisis Holds" loading="lazy"></span>
          <h3>Mental-Health Crisis Holds</h3>
          <p>Someone in crisis can be held for emergency evaluation &mdash; but only for a short time, and only a judge can order longer treatment. Your state's hold length, who can start one, and the person's hearing rights.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 31 topics" in text, "show-all label not found"
    text = text.replace("Show all 31 topics", "Show all 32 topics", 1)
    assert '<span class="count-badge">31 topics</span>' in text
    text = text.replace(
        '<span class="count-badge">31 topics</span>',
        '<span class="count-badge">32 topics</span>',
        1,
    )
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 31->32")


def build_about():
    text = ABOUT.read_text()
    assert "76 legal topics" in text, "about count not found"
    ABOUT.write_text(text.replace("76 legal topics", "77 legal topics", 1))
    print("  about.html: 76 -> 77")


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 10294, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith("mental-health-crisis-holds-in-") for e in idx)
    for s in data:
        state = s["state"]
        slug = s["slug"]
        named = f" {s['named']}" if s.get("named") else ""
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"mental-health-crisis-holds-in-{slug}",
                "h": f"Mental-Health Crisis Holds in {state}",
                "t": (
                    f"Mental-Health Crisis Holds in {state} "
                    f"\u2014 mental health crisis hold involuntary commitment "
                    f"emergency detention evaluation danger to self danger to "
                    f"others gravely disabled{named} hearing rights lawyer "
                    f"988 suicide crisis lifeline {s['statute']} {state}"
                ),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Mental-Health Crisis Holds",
            "t": (
                "Someone in crisis can be held for emergency evaluation "
                "\u2014 but only for a short time, and only a judge can "
                "order longer treatment. Your state's hold length, who "
                "can start one, and the person's hearing rights."
            ),
        }
    )
    assert len(idx) == 10345, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 10294 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [states[k] for k in sorted(states)]
    slugs = [s["slug"] for s in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert all(s.get("statute") and s.get("hold") and s.get("initiators") for s in data), "missing core data"
    print("building state pages...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
