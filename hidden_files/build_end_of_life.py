#!/usr/bin/env python3
"""Build Topic #73: End of Life & Death with Dignity — all 50 state pages.

Inserts one new section per state page (before the Daycare section,
newest-first), a contents-list entry, a homepage helper option + topic
card (second grid, after Daycare), bumps About 71 -> 72, and appends
50 state entries + 1 helper entry to assets/search-index.json (9689 -> 9740).

Data: hidden_files/topic-research/end-of-life/all-states.json (final merged
dataset; weak links nulled in merge: MA help, MI form, MS bill PDFs,
MO/MN/NV/NH/NE/TN/OH help duplicates, WI POLST opinion, AK/UT/WV/SC/PA
form links, DE DMOST API link; WA state-name transcription error fixed).
Fields that are null ship claim-free: no line is printed for them.
Phones second-sourced and MAID headline facts verified by separate
verification passes before this script runs.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "end-of-life" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"

TOPIC = "end-of-life-and-death-with-dignity"
ANCHOR = "end-of-life-and-death-with-dignity-in-{}"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def tel_href(phone):
    """tel: link only for a single plain number; multi-number strings stay text."""
    digits = re.sub(r"\D", "", phone or "")
    if ";" in (phone or "") or len(digits) < 10 or len(digits) > 11:
        return None
    return "tel:+1" + digits[-10:]


def section_html(s):
    state = s["state"]
    slug = s["slug"]
    parts = []
    parts.append("<section>")
    parts.append(
        f'<h2 id="end-of-life-and-death-with-dignity-in-{slug}">End of Life &amp; '
        f"Death with Dignity in {esc(state)}</h2>"
    )
    parts.append(
        f"<p>This section covers end-of-life law in {esc(state)}: medical aid in "
        "dying, advance directives, naming someone to make health care decisions "
        "for you, POLST medical orders, and refusing treatment or choosing hospice "
        "care. The law differs sharply from state to state on these questions, so "
        "what follows is what "
        f"{esc(state)} law says, in plain language. This is general information, "
        "not legal advice.</p>"
    )
    # --- Medical aid in dying ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Medical aid in dying in {esc(state)}</h3>")
    if s.get("maid_allowed"):
        parts.append(
            f"<p><strong>Allowed.</strong> {esc(s['maid_law'])}</p>"
            if s.get("maid_law")
            else "<p><strong>Allowed.</strong></p>"
        )
        if s.get("maid_eligibility"):
            parts.append(
                f"<p><strong>Who qualifies:</strong> {esc(s['maid_eligibility'])}</p>"
            )
        if s.get("maid_safeguards"):
            parts.append(
                f"<p><strong>Safeguards and steps:</strong> {esc(s['maid_safeguards'])}</p>"
            )
    else:
        if s.get("maid_prohibited_note"):
            parts.append(f"<p>{esc(s['maid_prohibited_note'])}</p>")
        else:
            parts.append(
                f"<p>Medical aid in dying is not authorized in {esc(state)}.</p>"
            )
    parts.append("</div>")
    # --- Advance directives ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Advance directives in {esc(state)}</h3>")
    parts.append("<ul>")
    parts.append(
        f"<li><strong>Form:</strong> {esc(s['advance_directive_name'])}</li>"
    )
    if s.get("advance_directive_url"):
        parts.append(
            f'<li><strong>Get the official form:</strong> <a href="{esc(s["advance_directive_url"])}" '
            f'target="_blank" rel="noopener">official {esc(state)} form</a></li>'
        )
    if s.get("advance_directive_requirements"):
        parts.append(
            f"<li><strong>Signing rules:</strong> "
            f"{esc(s['advance_directive_requirements'])}</li>"
        )
    parts.append(
        f"<li><strong>See also:</strong> Wills &amp; Probate in {esc(state)} on "
        "this page covers wills and estates; this section covers health care "
        "decisions.</li>"
    )
    parts.append("</ul>")
    parts.append("</div>")
    # --- Health care proxy / agent ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Naming someone to decide for you in {esc(state)}</h3>")
    parts.append("<ul>")
    parts.append(
        f"<li><strong>{esc(s['proxy_name'])}:</strong> "
        f"{esc(s['proxy_how'])}</li>"
    )
    parts.append("</ul>")
    parts.append("</div>")
    # --- POLST ---
    if s.get("polst_name") or s.get("polst_note"):
        parts.append('<div class="card">')
        heading = s.get("polst_name") or "Medical orders (POLST)"
        parts.append(f"<h3>{esc(heading)} in {esc(state)}</h3>")
        if s.get("polst_note"):
            parts.append(f"<p>{esc(s['polst_note'])}</p>")
        if s.get("polst_url"):
            parts.append(
                f'<p><a href="{esc(s["polst_url"])}" target="_blank" '
                f'rel="noopener">Official {esc(state)} POLST information</a></p>'
            )
        parts.append("</div>")
    # --- Refusing treatment & hospice ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Refusing treatment and hospice care in {esc(state)}</h3>")
    parts.append(f"<p>{esc(s['hospice_refusal'])}</p>")
    parts.append("</div>")
    # --- Where to get help ---
    if s.get("help_url") or s.get("help_phone"):
        parts.append('<div class="card">')
        parts.append(f"<h3>Where to get help in {esc(state)}</h3>")
        parts.append("<ul>")
        if s.get("help_url"):
            parts.append(
                f'<li><a href="{esc(s["help_url"])}" target="_blank" '
                f'rel="noopener">Find a lawyer or legal help in {esc(state)}</a></li>'
            )
        phone = s.get("help_phone")
        if phone:
            href = tel_href(phone)
            if href:
                parts.append(
                    f'<li><strong>Phone:</strong> <a href="{href}">'
                    f"{esc(phone)}</a></li>"
                )
            else:
                parts.append(f"<li><strong>Phone:</strong> {esc(phone)}</li>")
        parts.append("</ul>")
        parts.append("</div>")
    src = (s.get("sources") or [None])[0]
    if src:
        parts.append(
            f'<p><em>{esc(state)} source: <a href="{esc(src)}" target="_blank" '
            f'rel="noopener">official {esc(state)} page</a>. Checked against official '
            "sources in November 2026. End-of-life laws change &mdash; confirm the "
            "current law on the official source before you rely on it. This is general "
            "information, not legal advice.</em></p>"
        )
    else:
        parts.append(
            "<p><em>Checked against official sources in November 2026. End-of-life "
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
        # --- insert section before Daycare section ---
        h2 = text.find(f'<h2 id="daycare-and-childcare-in-{slug}">')
        assert h2 != -1, f"{slug}: daycare h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        new_section = section_html(s)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the daycare <li> ---
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#daycare-and-childcare-in-'
            + re.escape(slug)
            + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: daycare contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#end-of-life-and-death-with-dignity-in-{slug}">'
            f"End of Life &amp; Death with Dignity in {s['state']}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    assert "end-of-life-and-death-with-dignity" not in text, "index already has topic"
    # helper option after daycare option
    opt_old = (
        '<option value="daycare-and-childcare" data-anchor="daycare-and-childcare">'
        "Daycare &amp; childcare</option>"
    )
    assert opt_old in text, "daycare helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="end-of-life-and-death-with-dignity" '
        'data-anchor="end-of-life-and-death-with-dignity">'
        "End of life &amp; death with dignity</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    # topic card after daycare card (second grid)
    card_anchor = 'data-topic="daycare-and-childcare"'
    idx = text.find(card_anchor)
    assert idx != -1, "daycare card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="end-of-life-and-death-with-dignity">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-end-of-life-and-death-with-dignity.jpg" alt="End of Life &amp; Death with Dignity" loading="lazy"></span>
          <h3>End of Life &amp; Death with Dignity</h3>
          <p>Medical aid in dying, advance directives, naming someone to make health care decisions for you, POLST orders, and refusing treatment or choosing hospice &mdash; what the law says in your state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    # second-grid counts: 26 -> 27 unique topics
    assert "Show all 26 topics" in text, "show-all label not found"
    text = text.replace("Show all 26 topics", "Show all 27 topics", 1)
    assert '<span class="count-badge">26 topics</span>' in text
    text = text.replace(
        '<span class="count-badge">26 topics</span>',
        '<span class="count-badge">27 topics</span>',
        1,
    )
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 26->27")


def build_about():
    text = ABOUT.read_text()
    assert "71 legal topics" in text, "about count not found"
    ABOUT.write_text(text.replace("71 legal topics", "72 legal topics", 1))
    print("  about.html: 71 -> 72")


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 9689, f"unexpected index size {len(idx)}"
    assert not any("end-of-life-and-death-with-dignity" in str(e.get("a", "")) for e in idx)
    for s in data:
        state = s["state"]
        slug = s["slug"]
        idx.append(
            {
                "p": f"{state} Legal Help | The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"end-of-life-and-death-with-dignity-in-{slug}",
                "h": f"End of Life & Death with Dignity in {state}",
                "t": (
                    f"End of Life & Death with Dignity in {state} \u2014 medical aid "
                    f"in dying death with dignity advance directive living will health "
                    f"care proxy POLST hospice refuse treatment end of life {state}"
                ),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "End of Life & Death with Dignity",
            "t": (
                "Medical aid in dying, advance directives, naming someone to make "
                "health care decisions for you, POLST orders, and refusing treatment "
                "or choosing hospice \u2014 what the law says in your state."
            ),
        }
    )
    assert len(idx) == 9740, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 9689 -> {len(idx)} (+51)")


def main():
    data = json.loads(DATA.read_text())
    assert len(data) == 50, len(data)
    slugs = [s["slug"] for s in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert all(s.get("maid_allowed") in (True, False) for s in data), "maid_allowed not bool"
    assert all(s.get("advance_directive_name") for s in data), "missing directive name"
    assert all(s.get("proxy_name") and s.get("proxy_how") for s in data), "missing proxy"
    assert all(s.get("hospice_refusal") for s in data), "missing hospice_refusal"
    print("building state pages...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
