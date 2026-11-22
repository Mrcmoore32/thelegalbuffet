#!/usr/bin/env python3
"""Step 0 of the Tier 1 program: cheap findability fixes for buried items.

- Add search-index entries for six zero-entry buried items (SCRA, discharge
  upgrade, surprise medical bills, nursing-home resident rights, FEMA
  assistance, disaster contractor scams), 50 states each.
- Fix the 50 extreme-risk protection entries whose anchor is empty so they
  land on the gun-laws section instead of the top of the page.

Source of truth for h/t text: the live state pages themselves. No new facts
are introduced — h is the h3 text, t is the first ~160 chars of the block.
"""
import html
import json
import re
import glob

SITE = "/home/hatch/workspace/goals/50-state-legal-resource-website/site"
INDEX = SITE + "/assets/search-index.json"

ITEMS = [
    # key, h3 fragment, parent topic slug
    ("scra", "On active duty? The SCRA", "veterans-military-help"),
    ("discharge", "Discharge upgrade: DD Form 293", "veterans-military-help"),
    ("surprise", "Surprise bill? The No Surprises Act", "health-insurance-bills"),
    ("nursing", "Nursing-home resident rights", "guardianship-long-term-care"),
    ("fema", "FEMA assistance", "disaster-insurance-recovery"),
    ("contractor", "Contractor and repair scams after a disaster",
     "disaster-insurance-recovery"),
]


def clean(text):
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def state_name(slug):
    return slug.replace("-", " ").title()


def main():
    idx = json.load(open(INDEX))
    before = len(idx)
    existing = {(e["u"], e["a"], e["h"]) for e in idx}

    # 1. Fix empty anchors on extreme-risk entries.
    fixed = 0
    for e in idx:
        if e.get("h", "").lower().startswith("extreme risk") and not e.get("a"):
            slug = e["u"].split("/")[-1].replace(".html", "")
            e["a"] = f"gun-laws-in-{slug}"
            fixed += 1

    # 2. Add entries for the six zero-entry items.
    added = 0
    for key, frag, parent in ITEMS:
        for f in sorted(glob.glob(SITE + "/states/*.html")):
            slug = f.split("/")[-1].replace(".html", "")
            s = open(f).read()
            i = s.find(frag)
            if i < 0:
                print(f"WARN {key}: fragment not found in {slug}")
                continue
            hs = s.rfind("<h3", 0, i)
            he = s.find("</h3>", hs)
            h = clean(s[hs + 3:he].split(">", 1)[-1])
            # text after the h3, up to next h3/h2 or section end
            rest = s[he + 5:]
            nxt = min(
                x for x in (
                    rest.find("<h3"),
                    rest.find("<h2"),
                    rest.find("</section>"),
                ) if x >= 0
            )
            t = clean(rest[:nxt])[:160]
            entry = {
                "p": f"{state_name(slug)} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{parent}-in-{slug}",
                "h": h,
                "t": t,
            }
            if (entry["u"], entry["a"], entry["h"]) in existing:
                continue
            idx.append(entry)
            existing.add((entry["u"], entry["a"], entry["h"]))
            added += 1

    with open(INDEX, "w") as fh:
        json.dump(idx, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"index: {before} -> {len(idx)} entries "
          f"(+{added} new, {fixed} extreme-risk anchors fixed)")


if __name__ == "__main__":
    main()
