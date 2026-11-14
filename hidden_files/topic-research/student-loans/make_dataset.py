#!/usr/bin/env python3
"""Build the Topic #79 (Student loans) dataset from already-published
on-site material plus one fresh official directory check.

Sources (coordinator, Nov 14, 2026):
- State servicer-law / ombudsman paragraphs and the official state link:
  extracted verbatim from the "Student loans: repayment, default, and
  the way out" buried block inside Credit Card & Debt on each state page
  (Batch 6, commit 9906033). Those paragraphs were built from official
  state sources when that block shipped; the link sweep re-run for this
  build (Nov 14, 2026) found all 50 links live: 200/202, or 403 from
  official .gov bot filters (kept per precedent), and the two curl-000
  links (CT portal.CT.gov, TN tn.gov) confirmed live by a text fetch
  the same day.
- State Loan Repayment Program (SLRP) office: the HRSA / National
  Health Service Corps "State Loan Repayment Program Contacts" page
  (nhsc.hrsa.gov/loan-repayment/state-loan-repayment-program/contacts),
  read Nov 14, 2026. It lists a funded program office for 42 states in
  the 2026 cycle; the other 8 states (AL, FL, IA, NH, NJ, NC, SC, SD)
  have no office on that list, so their SLRP field is null and the
  section says so plainly instead of inventing a program.
- Federal figures (RAP/IDR, 270-day default, 15% garnishment, 30-day
  hearing / 65-day offset windows, 9-payment rehabilitation, PSLF 120
  payments, Teacher Loan Forgiveness $17,500/$5,000, Fresh Start ended
  Oct 2, 2024, Jan 16, 2026 collections pause, Defaulted Loans Support
  Center launched Sept 30, 2026): checked Nov 14, 2026 against
  studentaid.gov's IDR FAQ, Federal Student Aid default/rehabilitation
  guidance, and current reporting; see the build script header.
- No other state program is named: where a state publishes no official
  source found in this build, the field stays claim-free.

Output: all-states.json next to this script.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
STATES = ROOT / "states"

# SLRP program office per state, transcribed from the HRSA NHSC
# "State Loan Repayment Program Contacts" page, read Nov 14, 2026.
# States absent from that list get None (no funded office listed).
SLRP = {
    "alaska": "Alaska Department of Health",
    "arizona": "Arizona Department of Health Services",
    "arkansas": "University of Arkansas for Medical Sciences",
    "california": "California Department of Health Care Access and Information",
    "colorado": "Colorado Health Services Corps",
    "connecticut": "Connecticut Student Loan Repayment Program (UConn AHEC)",
    "delaware": "Delaware State Loan Repayment Program, Department of Health and Social Services",
    "georgia": "Georgia Board of Health Care Workforce",
    "hawaii": "Hawaii Department of Health, Office of Primary Care and Rural Health",
    "idaho": "Idaho Department of Health and Welfare",
    "illinois": "Illinois Department of Public Health",
    "indiana": "Indiana Department of Health",
    "kansas": "Kansas Department of Health and Environment",
    "kentucky": "University of Kentucky Center of Excellence in Rural Health",
    "louisiana": "Well-Ahead Louisiana (State Loan Repayment Program)",
    "maine": "Maine Center for Disease Control and Prevention",
    "maryland": "Maryland Department of Health",
    "massachusetts": "Massachusetts Department of Public Health",
    "michigan": "Michigan Department of Health and Human Services",
    "minnesota": "Minnesota Department of Health, Office of Rural Health and Primary Care",
    "mississippi": "Mississippi State Department of Health",
    "missouri": "Missouri Department of Health and Senior Services",
    "montana": "Montana Department of Public Health and Human Services",
    "nebraska": "Nebraska Department of Health and Human Services",
    "nevada": "Nevada Health Service Corps (University of Nevada, Reno School of Medicine)",
    "new-mexico": "New Mexico Higher Education Department",
    "new-york": "Doctors Across New York (New York Department of Health)",
    "north-dakota": "North Dakota Department of Health and Human Services, Primary Care Office",
    "ohio": "Ohio Department of Health",
    "oklahoma": "Oklahoma State Department of Health",
    "oregon": "Oregon Office of Rural Health (Oregon Health & Science University)",
    "pennsylvania": "Pennsylvania Department of Health",
    "rhode-island": "Rhode Island Department of Health",
    "tennessee": "Tennessee Department of Health",
    "texas": "Texas Higher Education Coordinating Board",
    "utah": "Utah Department of Health and Human Services",
    "vermont": "Vermont Department of Health",
    "virginia": "Virginia Department of Health",
    "washington": "Washington Student Achievement Council (Washington Health Corps)",
    "west-virginia": "West Virginia Department of Health",
    "wisconsin": "Wisconsin Office of Rural Health",
    "wyoming": "Wyoming Department of Health",
}

STATES_WITHOUT_SLRP = [
    "alabama", "florida", "iowa", "new-hampshire",
    "new-jersey", "north-carolina", "south-carolina", "south-dakota",
]


def clean(text):
    return htmlmod.unescape(re.sub(r"<[^>]+>", "", text)).strip()


def extract(slug):
    text = (STATES / f"{slug}.html").read_text()
    m = re.search(r"<title>([^<]+?) Legal Resources", text)
    assert m, f"{slug}: title not found"
    state = m.group(1)
    i = text.find("Student loans: repayment")
    assert i != -1, f"{slug}: buried student-loan block not found"
    # State-specific paragraphs live under the "Extra borrower
    # protections in {state}" h4, if the state has one.
    extra = []
    em = re.search(
        r"Extra borrower protections in " + re.escape(state) + r"</h3>(.*?)"
        r"(?=<h3|Do this now)",
        text[i:], re.S,
    )
    if em:
        extra = [clean(p) for p in re.findall(r"<p>(.*?)</p>", em.group(1), re.S)]
        # Drop the generic "official source" line if it leaked in.
        extra = [p for p in extra if not p.startswith("The official ")]
    # State card heading + official link: the link labelled
    # "Go to the official {state} page".
    lm = re.search(
        r'<h3[^>]*>([^<]+)</h3>\s*<p>The official '
        + re.escape(state)
        + r" source for student loans.*?"
        r'<a class="r-link" href="([^"]+)"',
        text[i:], re.S,
    )
    assert lm, f"{slug}: state card/link not found"
    return {
        "state": state,
        "slug": slug,
        "state_law": extra,
        "link_label": clean(lm.group(1)),
        "link": lm.group(2),
        "slrp_office": SLRP.get(slug),
    }


def main():
    slugs = sorted(p.name[:-5] for p in STATES.glob("*.html"))
    assert len(slugs) == 50, len(slugs)
    out = {"states": {}}
    for slug in slugs:
        rec = extract(slug)
        if slug in STATES_WITHOUT_SLRP:
            assert rec["slrp_office"] is None, slug
        out["states"][slug] = rec
    with_slrp = sum(1 for s in out["states"].values() if s["slrp_office"])
    with_law = sum(1 for s in out["states"].values() if s["state_law"])
    print(f"states: 50, with SLRP office: {with_slrp}, with state-law paras: {with_law}")
    dest = Path(__file__).resolve().parent / "all-states.json"
    dest.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {dest}")


if __name__ == "__main__":
    main()
