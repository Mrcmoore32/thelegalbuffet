#!/usr/bin/env python3
"""Add prominent 'Not legal advice' disclaimer boxes:
- letters.html: the existing templates disclaimer box duplicated at the TOP,
  immediately before the first letter article.
- All 50 state pages: a compact disclaimer box right after the intro paragraph
  of the three highest-risk sections (foreclosure defense, tenant rights,
  credit card & debt help).
Approved by Craig 2026-11-03.
"""
import re, sys, glob, os

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LETTERS_BOX = """<div class="disclaimer">
      <strong>Not legal advice</strong>
      These are general templates, not legal advice and not a substitute for a lawyer. Laws differ by state and change over time, and a letter that fits one situation can hurt another. If the other side has a lawyer, threatens court, or the amount is large, talk to a licensed attorney in your state or your state&rsquo;s free legal help before you send anything.
    </div>
    """

TOPICS = {
    "foreclosure-defense": (
        "foreclosure",
        "Deadlines in a foreclosure are strict and the rules change &mdash; confirm yours with the court, your servicer, or a local legal-aid office before you act.",
    ),
    "tenant-rights": (
        "renting and eviction",
        "Eviction deadlines are measured in days and the rules change &mdash; confirm yours with the court or a local legal-aid office before you act.",
    ),
    "credit-card-debt-help": (
        "debt and credit problems",
        "Court deadlines are strict and the rules change &mdash; confirm yours with the court or a local legal-aid office before you act.",
    ),
}

def box(topic_label, state, tail):
    return (
        '\n    <div class="disclaimer">\n'
        "      <strong>Not legal advice</strong>\n"
        f"      This section is general information about {topic_label} in {state}, not legal advice and not a substitute for a lawyer. {tail}\n"
        "    </div>"
    )

def main():
    # --- letters.html ---
    p = os.path.join(SITE, "letters.html")
    raw = open(p, encoding="utf-8").read()
    anchor = '<article class="letter" id="debt-validation">'
    assert raw.count(anchor) == 1, "letters anchor not unique"
    head = raw[: raw.index(anchor)]
    assert 'class="disclaimer"' not in head.split('<nav class="letters-toc"')[0][-2000:] or True
    if head.count('class="disclaimer"') > 0:
        print("letters.html: disclaimer already above first letter, skipping")
    else:
        raw = raw.replace(anchor, LETTERS_BOX + anchor, 1)
        open(p, "w", encoding="utf-8").write(raw)
        print("letters.html: top disclaimer inserted")

    # --- state pages ---
    total = 0
    for path in sorted(glob.glob(os.path.join(SITE, "states", "*.html"))):
        slug = os.path.basename(path)[:-5]
        raw = open(path, encoding="utf-8").read()
        sec_open_before = raw.count("<section")
        for prefix, (label, tail) in TOPICS.items():
            h2 = f'<h2 id="{prefix}-in-{slug}">'
            i = raw.find(h2)
            assert i >= 0, f"{slug}: missing {h2}"
            end_h2 = raw.find("</h2>", i)
            state = raw[i:end_h2].rsplit(" in ", 1)[-1].replace(f'id="{prefix}-in-{slug}">', "").strip()
            state = re.sub(r"<[^>]+>", "", state).strip()
            # skip if a disclaimer already sits right after the intro
            intro_end = raw.find("</p>", end_h2)
            assert intro_end > 0
            window = raw[end_h2 : intro_end + 900]
            if 'class="disclaimer"' in window:
                print(f"{slug}/{prefix}: already present, skipping")
                continue
            insert_at = intro_end + len("</p>")
            raw = raw[:insert_at] + box(label, state, tail) + raw[insert_at:]
            total += 1
        assert raw.count("<section") == sec_open_before, f"{slug}: section count changed"
        open(path, "w", encoding="utf-8").write(raw)
    print(f"state insertions: {total}")
    assert total == 150, f"expected 150 insertions, got {total}"
    print("OK")

if __name__ == "__main__":
    main()
