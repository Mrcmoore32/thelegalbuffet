#!/usr/bin/env python3
"""Build Topic #74: Stalking — all 50 state pages.

Inserts one new section per state page (before the End of Life section,
newest-first), a contents-list entry, a homepage helper option + topic
card (second grid, after End of Life), bumps About 72 -> 73, and appends
50 state entries + 1 helper entry to assets/search-index.json (9790 -> 9841).

Data: hidden_files/topic-research/stalking/all-states.json (final merged
dataset from 5 research batches; coordinator-verified: KY stalking rewrite
HB 521 — KRS 508.140/508.150 repealed eff. July 15, 2026, single offense
KRS 508.130 Class D felony (Class C aggravated) — confirmed against
apps.legislature.ky.gov and LegiScan; MN HRO §§ 609.748/609.749 matches
the site's own Domestic Abuse section.
Fields that are null ship claim-free: no line is printed for them, except
the fee line, which falls back to "ask the clerk" wording.
Order-gap notes (AL, AR, DE, IA, MS, NY, PA) print the honest limitation:
no standalone non-family stalking order verified in that state.
Phones: only the National DV Hotline 1-800-799-7233 (already on the site
and in the footer) is printed; no state phone numbers are printed.
Coalition for MN uses Violence Free Minnesota (vfmn.org) to match the
site's Domestic Abuse section, not the researcher's MNCASA pick.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "stalking" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"

TOPIC = "stalking"
ANCHOR = "stalking-in-{}"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(s):
    state = s["state"]
    slug = s["slug"]
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="stalking-in-{slug}">Stalking in {esc(state)}</h2>'
    )
    parts.append(
        f"<p>Stalking is a pattern of unwanted attention that makes you afraid "
        f"&mdash; being followed, watched, threatened, or contacted over and over "
        f"after you have made it clear you want it to stop. It can come from a "
        f"stranger, a neighbor, a coworker, an ex, or someone you barely know. "
        f"This section covers what to do right now, how to document it, how to "
        f"report it, the protective order in {esc(state)}, when stalking is a "
        f"crime, and online stalking. This is general information, not legal "
        f"advice.</p>"
    )
    # --- What to do right now ---
    parts.append('<div class="card">')
    parts.append(f"<h3>What to do right now in {esc(state)}</h3>")
    parts.append(
        "<p><strong>If you are in danger right now, call 911.</strong> "
        "Then: tell someone you trust what is happening and who is doing it. "
        "Vary your routines and routes where you can. Lock your doors and "
        "windows, and tell your workplace or school security if the person "
        "shows up there. Do not agree to meet the person to talk it out, and "
        "do not reply to their messages &mdash; silence is safer than an "
        "argument, and every reply can encourage more contact.</p>"
    )
    parts.append(
        "<p>If someone may be watching what you do on this phone or computer, "
        "use a safer device if you can &mdash; a friend&rsquo;s phone, a work "
        "or library computer. The Quick exit button at the bottom-right of "
        "this page leaves this site fast, but it cannot erase your browsing "
        "history.</p>"
    )
    parts.append(
        "<p>For free confidential help anytime, call the National Domestic "
        'Violence Hotline at <a href="tel:18007997233">1-800-799-7233</a> or '
        "text START to 88788.</p>"
    )
    parts.append("</div>")
    # --- Document it ---
    parts.append('<div class="card">')
    parts.append(f"<h3>How to document stalking in {esc(state)}</h3>")
    parts.append(
        "<p>Start a log now: dates, times, places, what happened, and any "
        "witnesses. Save texts, messages, voicemails, photos, and emails "
        "&mdash; do not delete anything, even if it upsets you to keep it. "
        "Screenshots with visible dates help. Back the log up somewhere the "
        "other person cannot reach, such as a trusted friend&rsquo;s email or "
        "a cloud account they do not know about. A police report helps too, "
        "even if no arrest is made &mdash; bring copies of everything to the "
        "hearing.</p>"
    )
    parts.append("</div>")
    # --- Report to police ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Reporting stalking to the police in {esc(state)}</h3>")
    parts.append(
        "<p>Report it to your local police department or sheriff&rsquo;s "
        "office, in person if you can. Bring your log, your saved messages "
        "and photos, and the names of any witnesses. Tell them the full "
        "pattern, not just the latest incident &mdash; stalking is about "
        "repeated conduct, and a single incident rarely tells the story. Ask "
        "for the report number and keep it with your log. A report does not "
        "force you to press charges, but it creates a record, and it is often "
        "what a judge wants to see before granting a protective order.</p>"
    )
    parts.append("</div>")
    # --- Protective order ---
    parts.append('<div class="card">')
    parts.append(f"<h3>The protective order in {esc(state)}</h3>")
    parts.append("<ul>")
    parts.append(
        f"<li><strong>{esc(s['order_name'])}:</strong> "
        f"{esc(s['order_statute'])}</li>"
    )
    parts.append(f"<li><strong>Where to file:</strong> {esc(s['order_where'])}</li>")
    if s.get("order_free") is True:
        parts.append(
            f"<li><strong>Cost:</strong> No filing fee. "
            + (f"{esc(s['order_free_note'])}" if s.get("order_free_note") else "")
            + "</li>"
        )
    elif s.get("order_free") is False:
        parts.append(
            f"<li><strong>Cost:</strong> {esc(s['order_free_note'])} "
            "Ask the clerk about a fee waiver if you cannot pay.</li>"
            if s.get("order_free_note")
            else "<li><strong>Cost:</strong> A filing fee applies. Ask the "
            "clerk about a fee waiver if you cannot pay.</li>"
        )
    else:
        parts.append(
            "<li><strong>Cost:</strong> Ask the clerk what it costs to file "
            "and whether a fee waiver is available &mdash; the fee was not "
            "published on an official source we could verify.</li>"
        )
    if s.get("order_duration"):
        parts.append(
            f"<li><strong>How long it lasts:</strong> "
            f"{esc(s['order_duration'])}</li>"
        )
    parts.append("</ul>")
    if s.get("order_gap_note"):
        parts.append(f"<p><strong>Important:</strong> {esc(s['order_gap_note'])}</p>")
    parts.append(
        "<p>The Domestic Abuse section on this page has more detail on how "
        "protective orders work &mdash; a judge can often issue a temporary "
        "order the same day you file, with a hearing within a few weeks where "
        "both sides are heard before a longer order is granted. After the "
        "judge signs, law enforcement serves the order on the other person "
        "&mdash; you do not deliver it yourself.</p>"
    )
    parts.append("</div>")
    # --- Criminal stalking law ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Stalking as a crime in {esc(state)}</h3>")
    parts.append(
        f"<p><strong>{esc(s['criminal_statute'])}.</strong> "
        f"{esc(s['criminal_definition'])}</p>"
    )
    if s.get("criminal_penalty"):
        parts.append(f"<p><strong>Penalty:</strong> {esc(s['criminal_penalty'])}</p>")
    parts.append("</div>")
    # --- Cyberstalking ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Online stalking (cyberstalking) in {esc(state)}</h3>")
    if s.get("cyber_statute"):
        parts.append(
            f"<p><strong>{esc(s['cyber_statute'])}.</strong> "
            f"{esc(s['cyber_note'])}</p>"
            if s.get("cyber_note")
            else f"<p><strong>{esc(s['cyber_statute'])}.</strong></p>"
        )
    elif s.get("cyber_note"):
        parts.append(
            f"<p>{esc(state)} has no separate cyberstalking statute. "
            f"{esc(s['cyber_note'])}</p>"
        )
    else:
        parts.append(
            f"<p>{esc(state)} has no separate cyberstalking statute, but "
            "online messages, tracking, and threats can still count as "
            f"stalking under {esc(s['criminal_statute'])} &mdash; save "
            "everything and report it. Report abusive accounts to the platform "
            "as well: every major platform has a report button on profiles, "
            "posts, and messages, and a report creates a record even if the "
            "account is not removed.</p>"
        )
    parts.append(
        "<p>If someone is tracking you, check your phone for unknown apps and "
        "location sharing, change your passwords from a safe device, and turn "
        "off location sharing on apps and photos. Do not delete the messages "
        "&mdash; they are evidence.</p>"
    )
    parts.append("</div>")
    # --- Where to get help ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Where to get help in {esc(state)}</h3>")
    parts.append("<ul>")
    if s.get("coalition_url"):
        parts.append(
            f'<li><a href="{esc(s["coalition_url"])}" target="_blank" '
            f'rel="noopener">{esc(s["coalition_name"])}</a> &mdash; '
            "shelters, legal help, and safety planning across "
            f"{esc(state)}.</li>"
        )
    elif s.get("coalition_name"):
        parts.append(f"<li>{esc(s['coalition_name'])}</li>")
    parts.append(
        "<li>National Domestic Violence Hotline: "
        '<a href="tel:18007997233">1-800-799-7233</a> (24/7) or text START '
        "to 88788.</li>"
    )
    parts.append("</ul>")
    parts.append("</div>")
    src = (s.get("sources") or [None])[0]
    if src:
        parts.append(
            f'<p><em>{esc(state)} source: <a href="{esc(src)}" target="_blank" '
            f'rel="noopener">official {esc(state)} page</a>. Checked against official '
            "sources in November 2026. Stalking laws change &mdash; confirm the "
            "current law on the official source before you rely on it. This is general "
            "information, not legal advice.</em></p>"
        )
    else:
        parts.append(
            "<p><em>Checked against official sources in November 2026. Stalking "
            "laws change &mdash; confirm the current law with the court or a licensed "
            "attorney in your state. This is general information, not legal "
            "advice.</em></p>"
        )
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def build_state_pages(data):
    for s in data:
        slug = s["slug"]
        path = STATES / f"{slug}.html"
        text = path.read_text()
        anchor = ANCHOR.format(slug)
        assert anchor not in text, f"{slug}: anchor already present"
        # --- insert section before End of Life section (newest-first) ---
        h2 = text.find(f'<h2 id="end-of-life-and-death-with-dignity-in-{slug}">')
        assert h2 != -1, f"{slug}: end-of-life h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        new_section = section_html(s)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the end-of-life <li> ---
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#end-of-life-and-death-with-dignity-in-'
            + re.escape(slug)
            + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: end-of-life contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#stalking-in-{slug}">'
            f"Stalking in {s['state']}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    assert "stalking" not in text.split("helper-topic")[1].split("</select>")[0], (
        "index already has stalking helper option"
    )
    assert 'data-topic="stalking"' not in text, "index already has stalking card"
    # helper option after end-of-life option
    opt_old = (
        '<option value="end-of-life-and-death-with-dignity" '
        'data-anchor="end-of-life-and-death-with-dignity">'
        "End of life &amp; death with dignity</option>"
    )
    assert opt_old in text, "end-of-life helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="stalking" data-anchor="stalking">'
        "Stalking</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    # topic card after end-of-life card (second grid)
    card_anchor = 'data-topic="end-of-life-and-death-with-dignity"'
    idx = text.find(card_anchor)
    assert idx != -1, "end-of-life card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="stalking">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-stalking.jpg" alt="Stalking" loading="lazy"></span>
          <h3>Stalking</h3>
          <p>Being followed, watched, or harassed online or in person? What to do right now, how to document it, the protective order in your state, and when it is a crime.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    # second-grid counts: 27 -> 28 unique topics
    assert "Show all 27 topics" in text, "show-all label not found"
    text = text.replace("Show all 27 topics", "Show all 28 topics", 1)
    assert '<span class="count-badge">27 topics</span>' in text
    text = text.replace(
        '<span class="count-badge">27 topics</span>',
        '<span class="count-badge">28 topics</span>',
        1,
    )
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 27->28")


def build_about():
    text = ABOUT.read_text()
    assert "72 legal topics" in text, "about count not found"
    ABOUT.write_text(text.replace("72 legal topics", "73 legal topics", 1))
    print("  about.html: 72 -> 73")


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 9790, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "") == "stalking" for e in idx)
    for s in data:
        state = s["state"]
        slug = s["slug"]
        idx.append(
            {
                "p": f"{state} Legal Help | The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"stalking-in-{slug}",
                "h": f"Stalking in {state}",
                "t": (
                    f"Stalking in {state} \u2014 being followed watched harassed "
                    f"threatened protective order {s['order_name']} "
                    f"{s['criminal_statute']} cyberstalking online stalking "
                    f"document report police safety {state}"
                ),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Stalking",
            "t": (
                "Being followed, watched, or harassed online or in person? What "
                "to do right now, how to document it, the protective order in "
                "your state, and when stalking is a crime."
            ),
        }
    )
    assert len(idx) == 9841, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 9790 -> {len(idx)} (+51)")


def main():
    data = json.loads(DATA.read_text())
    assert len(data) == 50, len(data)
    slugs = [s["slug"] for s in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert all(s.get("order_name") and s.get("order_statute") for s in data), (
        "missing order"
    )
    assert all(
        s.get("criminal_statute") and s.get("criminal_definition")
        for s in data
    ), "missing criminal law"
    assert all(s.get("order_where") for s in data), "missing order_where"
    print("building state pages...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
