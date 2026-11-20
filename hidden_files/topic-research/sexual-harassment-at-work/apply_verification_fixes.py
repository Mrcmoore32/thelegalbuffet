#!/usr/bin/env python3
"""Apply coordinator verification fixes to the #90 dataset before building.

URL fixes (from curl + live browser text fetch, Nov 20, 2026):
- AZ agency: https://azag.gov/civil-rights (404) -> https://www.azag.gov/civil-rights/faq (200)
- OH agency: deep filing URL (404) -> https://civ.ohio.gov/ (alive in browser)
- DE agency: dia.delawareworks.com/discrimination/ (000 x2, unresolvable) ->
  https://labor.delaware.gov/antidiscrimination (200; URL the office's own
  intake form cites as its website)

Phone fixes (phone-verification pass + coordinator's own second-source checks):
- 1-800-669-4000 on AL/AR/GA is the EEOC's number, not legal aid's.
  AL -> LSA 1-866-456-4995 (legalservicesalabama.org + alabamalegalhelp.org).
  GA -> GLSP 1-800-498-9469 (glsp.org + georgialegalaid.org + CFPB).
  AR -> null (no second official source for LAA's own number).
- Misattributed-but-real numbers relabeled to their true owner:
  CA 800-884-1684 = CRD (calcivilrights.ca.gov); DE 302-761-8200 = DE Office
  of Anti-Discrimination (official intake PDF); HI (808) 586-8636 = Hawai'i
  Civil Rights Commission; ID (208) 334-2873 = Idaho Human Rights Commission;
  OH 1-888-278-7101 = OCRC (civ.ohio.gov); NE 1-877-250-2016 = Legal Aid of
  Nebraska (legalaidofnebraska.org + hud.gov).
- Added with two official sources: AZ (602) 542-5263 (azag.gov FAQ +
  legal-aid page); NH (603) 271-2767 (humanrights.nh.gov + NH Admin Rules
  Hum 103.01); MA (617) 994-6000 (two mass.gov MCAD pages).
- Dropped to null (no second official source): IN, KY, NY, ND, VT, VA, WV.
- Kept as verified: IL, IA, KS, MN, NV, NJ, MI, MT (agency); WI, WY (legal aid).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "all-states.json"
LOG = HERE / "verification-log-2026-11-20.md"

d = json.loads(DATA.read_text())
states = d["states"]

URL_FIXES = {
    "arizona": ("agency_url", "https://www.azag.gov/civil-rights/faq"),
    "ohio": ("agency_url", "https://civ.ohio.gov/"),
    "delaware": ("agency_url", "https://labor.delaware.gov/antidiscrimination"),
}

# state -> (phone, phone_label) ; label is "State agency" or "Legal aid"
PHONES = {
    "alabama": ("1-866-456-4995", "Legal aid"),
    "arizona": ("(602) 542-5263", "State agency"),
    "arkansas": (None, None),
    "california": ("800-884-1684", "State agency"),
    "delaware": ("302-761-8200", "State agency"),
    "georgia": ("1-800-498-9469", "Legal aid"),
    "hawaii": ("(808) 586-8636", "State agency"),
    "idaho": ("(208) 334-2873", "State agency"),
    "illinois": ("(312) 814-6200", "State agency"),
    "indiana": (None, None),
    "iowa": ("(515) 281-4121", "State agency"),
    "kansas": ("(785) 296-3206", "State agency"),
    "kentucky": (None, None),
    "massachusetts": ("(617) 994-6000", "State agency"),
    "michigan": ("1-800-482-3604", "State agency"),
    "minnesota": ("651-539-1100", "State agency"),
    "montana": ("1-800-542-0807", "State agency"),
    "nebraska": ("1-877-250-2016", "Legal aid"),
    "nevada": ("(702) 486-7161", "State agency"),
    "new hampshire": ("(603) 271-2767", "State agency"),
    "new jersey": ("1-833-NJDCR4U", "State agency"),
    "new york": (None, None),
    "north dakota": (None, None),
    "ohio": ("1-888-278-7101", "State agency"),
    "vermont": (None, None),
    "virginia": (None, None),
    "west virginia": (None, None),
    "wisconsin": ("855-947-2529", "Legal aid"),
    "wyoming": ("877-432-9955", "Legal aid"),
}

assert len(states) == 50
for k, e in states.items():
    # URL fixes
    if k in URL_FIXES:
        f, u = URL_FIXES[k]
        assert e[f] != u, f"{k}: URL already fixed?"
        e[f] = u
    # phones: every state gets an explicit phone + phone_label
    assert k in PHONES or e["phone"] is None, f"{k}: unhandled phone {e['phone']!r}"
    if k in PHONES:
        phone, label = PHONES[k]
        e["phone"] = phone
        e["phone_label"] = label
    else:
        e["phone"] = None
        e["phone_label"] = None

n_phones = sum(1 for e in states.values() if e["phone"])
print(f"phones printing: {n_phones} / 50")
DATA.write_text(json.dumps(d, indent=1, sort_keys=True) + "\n")

LOG.write_text("""# Topic #90 verification log — 2026-11-20

## URLs (90 checked by curl; non-200s confirmed by live browser text fetch)
- Fixed: AZ agency -> https://www.azag.gov/civil-rights/faq (old 404);
  OH agency -> https://civ.ohio.gov/ (old deep URL 404; homepage alive in browser);
  DE agency -> https://labor.delaware.gov/antidiscrimination (old subdomain 000/unresolvable).
- Confirmed alive despite curl 403/406/000 (bot filters): AL, CA x2, CO x2, GA, ID,
  ME, MA x2, MS, NV, NH, NJ, UT, WY x2 legal-aid/agency pages.
- TN agency tn.gov/humanrights.html: curl 403 (bot-filter pattern); one browser fetch
  failed with a network error and was not retried. Kept as the official tn.gov URL.

## Phones (26 in dataset; 10 pass, 16 fail in verification pass)
- 1-800-669-4000 on AL/AR/GA is the EEOC's number, not legal aid's. AL replaced with
  LSA 1-866-456-4995; GA replaced with GLSP 1-800-498-9469; AR dropped to null.
- Relabeled to true owner: CA 800-884-1684 (CRD), DE 302-761-8200 (DE Office of
  Anti-Discrimination), HI (808) 586-8636 (Hawai'i Civil Rights Commission),
  ID (208) 334-2873 (Idaho Human Rights Commission), OH 1-888-278-7101 (OCRC),
  NE 1-877-250-2016 (Legal Aid of Nebraska).
- Added (two official sources each): AZ (602) 542-5263, NH (603) 271-2767,
  MA (617) 994-6000.
- Dropped to null (no second official source): IN, KY, NY, ND, VT, VA, WV.
- Final: 21 phones print (16 state agency, 5 legal aid); 29 states claim-free.

## Federal core (eeoc.gov/time-limits-filing-charge, read Nov 20)
- 180 days baseline, 300 days in deferral states; ongoing-harassment clock runs
  from the last incident; EEOC phone 1-800-669-4000.
""")
print("patched all-states.json + wrote verification log")
