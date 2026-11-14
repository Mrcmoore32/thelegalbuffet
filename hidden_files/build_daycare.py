#!/usr/bin/env python3
"""Build Topic #72: Daycare & Childcare — all 50 state pages.

Inserts one new section per state page (before the Pulled Over section,
newest-first), a contents-list entry, a homepage helper option + topic
card (second grid, after Pulled Over), bumps About 70 -> 71, and appends
50 state entries + 1 helper entry to assets/search-index.json (9638 -> 9689).

Data: hidden_files/topic-research/daycare/all-states.json (final merged
dataset; phones second-sourced, FL/HI abuse-hotline numbers nulled,
KS corrected to the direct licensing line, DE county split noted).
Fields that are null ship claim-free: no line is printed for them.
"""
import html as htmlmod
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "daycare" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"

TOPIC = "daycare-and-childcare"
ANCHOR = "daycare-and-childcare-in-{}"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def tel_href(phone):
    """tel: link only for a single plain number; multi-number strings stay text."""
    digits = re.sub(r"\D", "", phone or "")
    if ";" in (phone or "") or len(digits) < 10 or len(digits) > 11:
        return None
    return "tel:+1" + digits[-10:]


def ratios_html(ratios):
    items = []
    for r in ratios:
        n = r["ratio"].split(":")[1].strip()
        items.append(
            f'<li><strong>{esc(r["group"])}:</strong> 1 adult to {esc(n)} '
            f'{"child" if n == "1" else "children"}</li>'
        )
    return "\n".join(items)


def section_html(s):
    state = s["state"]
    slug = s["slug"]
    parts = []
    parts.append("<section>")
    parts.append(
        f'<h2 id="daycare-and-childcare-in-{slug}">Daycare &amp; Childcare in {esc(state)}</h2>'
    )
    parts.append(
        f"<p>If you run a daycare or you are choosing one for your child, {esc(state)} "
        "has one licensing agency and one set of rules. This page covers both sides "
        "&mdash; what providers must do to stay licensed, and how parents can check a "
        "provider, see its record, and complain if something goes wrong. If you suspect "
        "a child is being abused or neglected, report it right away &mdash; the Childhelp "
        "National Child Abuse Hotline is 1-800-422-4453, also listed under "
        '<a href="#national-resources">National resources</a> at the bottom of this page. '
        "This section is about licensing, inspections, and complaints about the program itself.</p>"
    )
    # --- Providers: licensing at a glance ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Licensing in {esc(state)} &mdash; at a glance</h3>")
    parts.append("<ul>")
    parts.append(
        f'<li><strong>Licensing agency:</strong> <a href="{esc(s["agency_url"])}" '
        f'target="_blank" rel="noopener">{esc(s["agency"])}</a></li>'
    )
    if s.get("license_types"):
        parts.append(f'<li><strong>License types:</strong> {esc(s["license_types"])}</li>')
    if s.get("how_to_get_licensed"):
        parts.append(
            f'<li><strong>How to get licensed:</strong> {esc(s["how_to_get_licensed"])}</li>'
        )
    if s.get("background_checks"):
        parts.append(
            f'<li><strong>Background checks:</strong> {esc(s["background_checks"])}</li>'
        )
    if s.get("insurance"):
        parts.append(
            f'<li><strong>Liability insurance:</strong> {esc(s["insurance"])}</li>'
        )
    parts.append("</ul>")
    parts.append("</div>")
    # --- Ratios (only when verified) ---
    if s.get("ratios"):
        parts.append('<div class="card">')
        parts.append(f"<h3>Staff-to-child ratios in {esc(state)}</h3>")
        parts.append(
            "<p>These are the state&rsquo;s minimum ratios &mdash; the most children "
            "one adult may care for at a time:</p>"
        )
        parts.append("<ul>")
        parts.append(ratios_html(s["ratios"]))
        parts.append("</ul>")
        if s.get("ratios_source_url"):
            parts.append(
                f'<p>Source: <a href="{esc(s["ratios_source_url"])}" target="_blank" '
                f'rel="noopener">official {esc(state)} ratio rules</a></p>'
            )
        parts.append("</div>")
    # --- Parents: check a provider ---
    parts.append('<div class="card">')
    parts.append(f"<h3>For parents: check a provider before you enroll</h3>")
    parts.append("<ul>")
    lookup = s.get("parent_lookup_url")
    inspect = s.get("inspection_history_url")
    if lookup:
        parts.append(
            f'<li><strong>Check the license:</strong> <a href="{esc(lookup)}" '
            f'target="_blank" rel="noopener">look up this provider</a> with the '
            "licensing agency before you enroll.</li>"
        )
    if inspect and inspect != lookup:
        parts.append(
            f'<li><strong>See inspection history:</strong> <a href="{esc(inspect)}" '
            f'target="_blank" rel="noopener">inspection and violation records</a> '
            "for licensed providers.</li>"
        )
    elif inspect and inspect == lookup:
        parts.append(
            "<li><strong>See inspection history:</strong> the same lookup shows "
            "inspection and violation records for licensed providers.</li>"
        )
    if s.get("parent_disclosure"):
        parts.append(
            f'<li><strong>What the provider must tell you:</strong> '
            f'{esc(s["parent_disclosure"])}</li>'
        )
    parts.append(
        "<li><strong>Always ask:</strong> ask for the provider&rsquo;s license number "
        "and the name of the agency that issued it, then check both with the agency above.</li>"
    )
    parts.append("</ul>")
    parts.append("</div>")
    # --- If something goes wrong ---
    parts.append('<div class="card">')
    parts.append("<h3>If something goes wrong with your child</h3>")
    parts.append(
        "<p>Start with the provider &mdash; tell the director what happened, in writing, "
        "and keep a copy. If that does not fix it, or the problem is about safety or "
        "licensing rules:</p>"
    )
    parts.append("<ul>")
    if s.get("complaint_process"):
        parts.append(f"<li>{esc(s['complaint_process'])}</li>")
    phone = s.get("complaint_phone")
    if phone:
        href = tel_href(phone)
        if href:
            parts.append(
                f'<li><strong>Complaint line:</strong> <a href="{href}">{esc(phone)}</a></li>'
            )
        else:
            parts.append(f"<li><strong>Complaint line:</strong> {esc(phone)}</li>")
    if s.get("complaint_url"):
        parts.append(
            f'<li><strong>File a complaint:</strong> <a href="{esc(s["complaint_url"])}" '
            f'target="_blank" rel="noopener">complaint page</a></li>'
        )
    if not s.get("complaint_process") and not phone and not s.get("complaint_url"):
        parts.append(
            "<li>Contact the licensing agency listed above &mdash; it handles complaints "
            "about licensed providers.</li>"
        )
    parts.append(
        "<li><strong>If a child is in immediate danger, call 911.</strong> If you suspect "
        "abuse or neglect, report it right away &mdash; the Childhelp hotline is "
        "1-800-422-4453.</li>"
    )
    parts.append("</ul>")
    parts.append("</div>")
    # --- Contracts (generic guidance; no state publishes a standard form) ---
    parts.append('<div class="card">')
    parts.append("<h3>Contracts, deposits, and withdrawing your child</h3>")
    parts.append(
        "<p>Read the contract before you sign it. Daycare terms vary by provider, so get "
        "these in writing: the weekly rate and what it covers, the deposit and when it is "
        "refunded, how much notice you must give to withdraw, what happens if you pull "
        "your child out mid-month, and late pickup fees. Keep a signed copy. If the "
        "provider changes the terms, ask for the change in writing too.</p>"
    )
    parts.append("</div>")
    parts.append(
        f'<p><em>{esc(state)} source: <a href="{esc(s["agency_url"])}" target="_blank" '
        f'rel="noopener">official {esc(state)} page</a>. Checked against official sources '
        "in November 2026. Child care rules change &mdash; confirm the current requirements "
        "on the agency&rsquo;s page before you rely on them. This is general information, "
        "not legal advice.</em></p>"
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
        # --- insert section before Pulled Over section ---
        h2 = text.find(f'<h2 id="pulled-over-in-{slug}">')
        assert h2 != -1, f"{slug}: pulled-over h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        new_section = section_html(s)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the pulled-over <li> ---
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#pulled-over-in-' + re.escape(slug) + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: pulled-over contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#daycare-and-childcare-in-{slug}">'
            f"Daycare &amp; Childcare in {s['state']}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    assert "daycare-and-childcare" not in text, "index already has daycare"
    # helper option after pulled-over option
    opt_old = (
        '<option value="pulled-over" data-anchor="pulled-over">'
        "Pulled over (traffic stop rights)</option>"
    )
    assert opt_old in text, "pulled-over helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="daycare-and-childcare" data-anchor="daycare-and-childcare">'
        "Daycare &amp; childcare</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    # topic card after pulled-over card (second grid)
    card_anchor = 'data-topic="pulled-over"'
    idx = text.find(card_anchor)
    assert idx != -1, "pulled-over card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="daycare-and-childcare">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-daycare-and-childcare.jpg" alt="Daycare &amp; Childcare" loading="lazy"></span>
          <h3>Daycare &amp; Childcare</h3>
          <p>Running a daycare or choosing one for your child? Licensing, staff-to-child ratios, background checks, how to check a provider&rsquo;s record, and how to file a complaint &mdash; for providers and parents.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    # second-grid counts: 25 -> 26 unique topics
    assert "Show all 25 topics" in text, "show-all label not found"
    text = text.replace("Show all 25 topics", "Show all 26 topics", 1)
    assert '<span class="count-badge">25 topics</span>' in text
    text = text.replace(
        '<span class="count-badge">25 topics</span>',
        '<span class="count-badge">26 topics</span>',
        1,
    )
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 25->26")


def build_about():
    text = ABOUT.read_text()
    assert "70 legal topics" in text, "about count not found"
    ABOUT.write_text(text.replace("70 legal topics", "71 legal topics", 1))
    print("  about.html: 70 -> 71")


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 9638, f"unexpected index size {len(idx)}"
    assert not any("daycare-and-childcare" in str(e.get("a", "")) for e in idx)
    for s in data:
        state = s["state"]
        slug = s["slug"]
        idx.append(
            {
                "p": f"{state} Legal Help | The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"daycare-and-childcare-in-{slug}",
                "h": f"Daycare & Childcare in {state}",
                "t": (
                    f"Daycare & Childcare in {state} \u2014 daycare childcare child care "
                    f"license licensing provider ratios background check complaint inspection "
                    f"lookup parents {state}"
                ),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Daycare & Childcare",
            "t": (
                "Running a daycare or choosing one for your child? Licensing, "
                "staff-to-child ratios, background checks, how to check a provider\u2019s "
                "record, and how to file a complaint \u2014 for providers and parents."
            ),
        }
    )
    assert len(idx) == 9689, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 9638 -> {len(idx)} (+51)")


def main():
    data = json.loads(DATA.read_text())
    assert len(data) == 50, len(data)
    slugs = [s["slug"] for s in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert all(s.get("agency") and s.get("agency_url") for s in data), "missing agency"
    print("building state pages...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
