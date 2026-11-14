#!/usr/bin/env python3
"""Build impound expansion inside Topic #60 (Car Booted or Towed) — all 50 state pages.

Inserts one impound sub-block per state page INSIDE the existing
Car Booted or Towed section (h2 id car-booted-or-towed-in-<slug>), just
before that section's closing </section>. No new topic, no homepage card,
no helper option, no About count change (stays 72). Appends 50 entries to
assets/search-index.json (9740 -> 9790) so "impound"/"impoundment" find
every state's tow section (anchor = the existing tow anchor).

Data: hidden_files/topic-research/impound/all-states.json (final merged
dataset; coordinator-verified: MN fees/phone live on minneapolismn.gov,
NE $500 threshold live in current statute, MT 61-12-401/404 live in MCA,
WA corrected to RCW 46.55.120/130 live text; AL + HI phones nulled for
lack of a second official source; MS SB 2848 vendor sentence removed —
enactment unconfirmed; FL rests on the researcher's loaded 2003-year
statute URL; MA hearing/notice details rest on search crawls after a
429 rate-limit, flagged in the build report).
Fields that are null ship claim-free: the fees card prints the
no-statewide-cap fallback, never an invented figure.
Phones printed only where second-sourced (MN, NJ, NY).
"""
import html as htmlmod
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "impound" / "all-states.json"
STATES = ROOT / "states"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"

MARKER = "<!-- impound-block: car-booted-or-towed expansion, Nov 2026 -->"
FEES_FALLBACK = (
    "No statewide fee cap is published for {state} — tow and storage rates "
    "are set locally or by the lot. Storage charges pile up daily, so call "
    "the lot and ask for the current total before you go."
)


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def tel_href(phone):
    digits = re.sub(r"\D", "", phone or "")
    if len(digits) < 10 or len(digits) > 11:
        return None
    return "tel:+1" + digits[-10:]


def source_links(sources):
    """Up to 4 official-source links; skip bare-homepage URLs."""
    links = []
    for url in sources or []:
        parsed = urlparse(url)
        if parsed.path in ("", "/"):
            continue
        label = parsed.netloc.replace("www.", "")
        links.append(
            f'<a class="r-link" href="{esc(url)}" target="_blank" '
            f'rel="noopener">{esc(label)} &rarr;</a>'
        )
        if len(links) >= 4:
            break
    return links


def card(tag, title, body_html):
    return (
        '            <div class="resource">\n'
        f'              <span class="r-tag">{tag}</span>\n'
        f"              <h3>{title}</h3>\n"
        f"              <p>{body_html}</p>\n"
        "            </div>\n"
    )


def block_html(s):
    state = s["state"]
    slug = s["slug"]
    parts = []
    parts.append(f"          {MARKER}")
    parts.append(
        f'          <h3 class="block-subhead">If your car was impounded in {esc(state)}</h3>'
    )
    parts.append(
        "          <p>Impoundment is the step after a tow: your car sits in a lot, "
        "storage charges pile up daily, and if you wait too long the lot can sell "
        "it. Here is how to find it, what it costs, how to fight the tow, and what "
        "happens if you leave it there.</p>"
    )
    parts.append('          <div class="resource-list">')
    # Find your car
    find_body = esc(s["find_car"])
    if s.get("phone"):
        href = tel_href(s["phone"])
        phone_html = (
            f'<a href="{href}">{esc(s["phone"])}</a>' if href else esc(s["phone"])
        )
        find_body += f"<br><strong>Phone:</strong> {phone_html}"
    parts.append(
        card(
            "Find your car",
            "Where is my car, and how do I get it back?",
            find_body,
        )
    )
    # Fees
    fees_body = esc(s["fees"]) if s.get("fees") else esc(
        FEES_FALLBACK.format(state=state)
    )
    parts.append(card("Fees", "What will it cost?", fees_body))
    # Contest
    parts.append(
        card(
            "Contest the tow",
            "How do I contest the tow or impoundment?",
            esc(s["contest"]),
        )
    )
    # Unclaimed
    parts.append(
        card(
            "If you don't claim it",
            "What happens if I don't claim my car?",
            esc(s["unclaimed"]),
        )
    )
    # Police vs private
    parts.append(
        card(
            "Police vs. private tow",
            "Police-ordered tow vs. private-property tow",
            esc(s["police_vs_private"]),
        )
    )
    # Sources
    links = source_links(s.get("sources"))
    if links:
        src_body = (
            "The rules above come from these official sources. Tow and impound "
            "rules are often local, so read them alongside the notice on your car "
            "and the lot's posted terms.<br>" + "<br>".join(links)
        )
        parts.append(card("Official sources", "Where these rules come from", src_body))
    parts.append("          </div>")
    return "\n".join(parts)


def main():
    data = json.load(open(DATA))
    assert len(data) == 50, f"expected 50 states, got {len(data)}"
    assert len({s["slug"] for s in data}) == 50, "duplicate slugs"
    for s in data:
        for k in ("state", "slug", "find_car", "contest", "unclaimed", "police_vs_private"):
            assert isinstance(s.get(k), str) and s[k].strip(), f"{s['slug']}: bad {k}"

    # --- state pages ---
    changed = []
    for s in data:
        slug = s["slug"]
        path = STATES / f"{slug}.html"
        text = path.read_text()
        assert MARKER not in text, f"{slug}: block already present"
        hid = f'id="car-booted-or-towed-in-{slug}"'
        assert text.count(hid) == 1, f"{slug}: h2 id count {text.count(hid)}"
        h2_idx = text.index(hid)
        close_idx = text.index("</section>", h2_idx)
        block = block_html(s)
        text = text[:close_idx] + block + "\n" + text[close_idx:]
        path.write_text(text)
        changed.append(slug)

    # --- search index: one entry per state, anchor = existing tow anchor ---
    index = json.load(open(SEARCH_INDEX))
    before = len(index)
    assert before == 9740, f"index was {before}, expected 9740"
    for s in data:
        index.append(
            {
                "p": f"{s['state']} Legal Resources — The Legal Buffet",
                "u": f"states/{s['slug']}.html",
                "a": f"car-booted-or-towed-in-{s['slug']}",
                "h": f"Car booted or towed in {s['state']}",
                "t": (
                    f"Impound and impoundment in {s['state']}: where your car "
                    "was taken and how to get it back, tow and storage fees, "
                    "how to contest the tow, and what happens if you don't "
                    "claim it in time."
                ),
            }
        )
    json.dump(index, open(SEARCH_INDEX, "w"), indent=1, ensure_ascii=False)
    with open(SEARCH_INDEX, "a") as f:
        f.write("\n")
    print(f"state pages changed: {len(changed)}")
    print(f"search index: {before} -> {len(index)}")


if __name__ == "__main__":
    main()
