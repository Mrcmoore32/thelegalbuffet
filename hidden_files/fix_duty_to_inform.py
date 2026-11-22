#!/usr/bin/env python3
"""Correction pass: duty-to-inform conflicts between Pulled Over (#71) and
Carry Permit Reciprocity (#86). Verdicts from statute-level research (Nov 15, 2026)
against official state legislature/code sites. One commit; targeted git add only.

Rules: every replacement asserts exactly-once occurrence of the old string.
No section ids, anchors, helper, cards, About count, or search index touched.
"""
import re, sys

SITE = "/home/hatch/workspace/goals/50-state-legal-resource-website/site"
EM = "\u2014"  # literal em-dash used in the HTML files

# --- Pulled Over card-line replacements: (state, old_li_text, new_li_text) ---
PO_CARD = [
 ("california",
  "If you are carrying a firearm, you must tell the officer " + EM + " without being asked.",
  "No statewide law makes you tell an officer you are carrying. You must show your license and your firearm if the officer asks to see them."),
 ("oklahoma",
  "If you are carrying a firearm, you must tell the officer " + EM + " without being asked.",
  "You do not have to volunteer it. If the officer asks or demands it during an arrest, detention, or routine traffic stop, you must tell them you are carrying."),
 ("maine",
  "If you are carrying a firearm, you must tell the officer " + EM + " without being asked.",
  "Only if you are carrying a concealed handgun without a permit " + EM + " you must tell the officer right away when you first come into contact during an arrest, detention, or traffic stop. Permit holders do not have to volunteer it, but must show their permit if the officer asks."),
 ("north-dakota",
  "If you are carrying a firearm, you must disclose it when the officer asks " + EM + " including showing your permit on demand.",
  "If you are carrying a concealed firearm without a permit, you must tell the officer you are carrying only if the officer asks about it. If you carry on a license, you do not have to volunteer it " + EM + " just show your license if the officer asks to see it."),
 ("missouri",
  "If you are carrying a firearm, you must disclose it when the officer asks " + EM + " including showing your permit on demand.",
  "No legal duty to tell the officer about a lawfully carried firearm. If you have a concealed carry permit, you must show it and a photo ID if an officer asks for them."),
 ("mississippi",
  "If you are carrying a firearm, you must disclose it when the officer asks " + EM + " including showing your permit on demand.",
  "No legal duty to tell the officer about a lawfully carried firearm. If you have a license to carry, you must show it and valid identification if a law enforcement officer demands them."),
 ("nevada",
  "If you are carrying a firearm, you must disclose it when the officer asks " + EM + " including showing your permit on demand.",
  "No legal duty to tell the officer about a lawfully carried firearm. If you have a concealed firearm permit, you must show it and proper identification if a peace officer asks for them."),
 ("tennessee",
  "If you are carrying a firearm, you must disclose it when the officer asks " + EM + " including showing your permit on demand.",
  "No legal duty to tell the officer about a lawfully carried firearm. You only have to show your permit if an officer asks while you are carrying in a place or way that is legal only because you have the permit."),
 ("virginia",
  "If you are carrying a firearm, you must disclose it when the officer asks " + EM + " including showing your permit on demand.",
  "No legal duty to tell the officer about a lawfully carried firearm. If you have a concealed handgun permit, you must show it and a photo ID if a law-enforcement officer demands them."),
 ("washington",
  "If you are carrying a firearm, you must disclose it when the officer asks " + EM + " including showing your permit on demand.",
  "No legal duty to tell the officer about a lawfully carried firearm. You must show your concealed pistol license if an officer asks for it."),
 ("wisconsin",
  "If you are carrying a firearm, you must disclose it when the officer asks " + EM + " including showing your permit on demand.",
  "No legal duty to tell the officer about a lawfully carried firearm. You must show your license and photo ID if an officer asks for them."),
 ("wyoming",
  "If you are carrying a firearm, you must disclose it when the officer asks " + EM + " including showing your permit on demand.",
  "No legal duty to tell the officer about a lawfully carried firearm. If you carry on a permit, you must show the permit and ID if a peace officer asks."),
]

# --- Pulled Over "Worth knowing" fix (California only) ---
PO_WORTH = [
 ("california",
  "California's duty to inform is a condition of your carry license rather than a separate statute " + EM + " but breaking it can cost the license.",
  "There is no statewide duty-to-inform law in California, but your CCW license itself may add one: some counties require you to disclose when stopped or detained, and breaking a license condition can cost the license."),
]

# --- Pulled Over gap states: add the standard firearm line as first <li> in the card ---
PO_GAP = ["south-dakota", "utah", "vermont", "west-virginia"]
GAP_LI = "<li><strong>Carrying a firearm:</strong> No legal duty to tell the officer about a lawfully carried firearm.</li>\n"

# --- Reciprocity duty_note replacements: (state, old_note, new_note) ---
# Applied to BOTH the state page text and the #86 dataset (same strings).
RECIP_NOTES = [
 ("north-dakota",
  "If you are carrying without a permit, you must inform an officer on any in-person contact (N.D.C.C. \u00a7 62.1-04-04). If you carry on a license, show it when the officer asks.",
  "If you are carrying without a permit, you must tell the officer you are carrying only if the officer asks about it (N.D.C.C. \u00a7 62.1-04-04). If you carry on a license, show it if the officer asks to see it."),
 ("tennessee",
  "No law requires you to volunteer that you are carrying. If the officer asks, answer honestly, and show your permit and ID when asked for them.",
  "No law requires you to volunteer that you are carrying. You only have to show your permit if an officer asks while you are carrying in a place or way that is legal only because you have the permit."),
 ("south-dakota",
  "No law requires you to volunteer that you are carrying. If the officer asks, answer honestly, and show your permit and ID when asked for them.",
  "No law requires you to volunteer that you are carrying. If the officer asks, answer honestly."),
 ("utah",
  "No law requires you to volunteer that you are carrying. If the officer asks, answer honestly, and show your permit and ID when asked for them.",
  "No law requires you to volunteer that you are carrying. If the officer asks, answer honestly."),
 ("west-virginia",
  "No law requires you to volunteer that you are carrying. If the officer asks, answer honestly, and show your permit and ID when asked for them.",
  "No law requires you to volunteer that you are carrying. If the officer asks, answer honestly."),
 ("oregon",
  "No law requires you to volunteer that you are carrying. If the officer asks, answer honestly, and show your permit and ID when asked for them.",
  "No law requires you to volunteer that you are carrying. If the officer asks, answer honestly."),
 ("louisiana",
  "Anyone carrying concealed, licensed or permitless, must inform an officer on contact, and must submit to a pat-down and temporary disarming if the officer asks.",
  "Anyone carrying concealed, licensed or permitless, must inform an officer on contact, and must submit to a pat-down and let the officer temporarily disarm you."),
 ("hawaii",
  "You must immediately disclose that you are carrying when an officer stops or contacts you.",
  "You must immediately disclose that you are carrying when an officer stops you, or stops the vehicle you are riding in."),
 ("minnesota",
  "A permit holder must disclose when an officer asks for ID (Minn. Stat. \u00a7 624.714, subd. 1b(d)). You do not have to volunteer it unasked.",
  "A permit holder must disclose whether they are carrying when a peace officer asks (Minn. Stat. \u00a7 624.714, subd. 1b(d)). You do not have to volunteer it unasked."),
]

def replace_once(text, old, new, where):
    n = text.count(old)
    assert n == 1, f"{where}: expected old string once, found {n}: {old[:80]!r}"
    return text.replace(old, new)

def replace_in_state_entry(ds, slug, old, new, where):
    """Replace the duty_note value inside one state's JSON entry only."""
    pat = re.compile(r'("slug": "' + re.escape(slug) + r'",.*?"duty_note": ")' + re.escape(old) + r'"', re.S)
    m = pat.search(ds)
    assert m, f"{where}: duty_note not found in entry for {slug}"
    return ds[:m.start()] + m.group(1) + new + '"' + ds[m.end():]

def main():
    changed = []
    # 1. Pulled Over card lines
    for st, old, new in PO_CARD:
        p = f"{SITE}/states/{st}.html"
        s = open(p, encoding="utf-8").read()
        old_li = f"<li><strong>Carrying a firearm:</strong> {old}</li>"
        new_li = f"<li><strong>Carrying a firearm:</strong> {new}</li>"
        s = replace_once(s, old_li, new_li, f"{st} PO card")
        open(p, "w", encoding="utf-8").write(s)
        changed.append(f"{st} PO card")
    # 2. California Worth knowing
    for st, old, new in PO_WORTH:
        p = f"{SITE}/states/{st}.html"
        s = open(p, encoding="utf-8").read()
        s = replace_once(s, old, new, f"{st} PO Worth knowing")
        open(p, "w", encoding="utf-8").write(s)
        changed.append(f"{st} PO Worth knowing")
    # 3. Gap states: insert firearm line as first <li> of the traffic-stop card
    for st in PO_GAP:
        p = f"{SITE}/states/{st}.html"
        s = open(p, encoding="utf-8").read()
        state_name = st.replace("-", " ").title().replace("South-dakota", "South Dakota")
        # state display name in the h3: e.g. "At a traffic stop in South Dakota"
        disp = {"south-dakota": "South Dakota", "utah": "Utah",
                "vermont": "Vermont", "west-virginia": "West Virginia"}[st]
        pat = re.compile(r"(<h3>At a traffic stop in " + re.escape(disp) + r"</h3>\s*<ul>\n)")
        m = pat.search(s)
        assert m, f"{st}: traffic-stop card ul not found"
        s = s[:m.end()] + GAP_LI + s[m.end():]
        open(p, "w", encoding="utf-8").write(s)
        changed.append(f"{st} PO gap line added")
    # 4. Reciprocity notes: state pages + dataset
    ds_path = f"{SITE}/hidden_files/topic-research/carry-permit-reciprocity/all-states.json"
    ds = open(ds_path, encoding="utf-8").read()
    for st, old, new in RECIP_NOTES:
        p = f"{SITE}/states/{st}.html"
        s = open(p, encoding="utf-8").read()
        s = replace_once(s, old, new, f"{st} RECIP page")
        open(p, "w", encoding="utf-8").write(s)
        changed.append(f"{st} RECIP page note")
        ds = replace_in_state_entry(ds, st, old, new, f"{st} RECIP dataset")
        changed.append(f"{st} RECIP dataset note")
    open(ds_path, "w", encoding="utf-8").write(ds)
    print(f"OK — {len(changed)} replacements applied:")
    for c in changed:
        print("  -", c)

if __name__ == "__main__":
    main()
