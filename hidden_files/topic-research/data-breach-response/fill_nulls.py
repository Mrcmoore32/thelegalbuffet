#!/usr/bin/env python3
"""Fill the 52 null URLs in the #102 data-breach-response merged dataset.

All URLs verified Nov 20, 2026:
- curl 200 (sequential): 42
- text-fetch confirmed live: ncdoj.gov/protecting-consumers/, mslegalservices.org
- search-crawl confirmed (bot-filtered official sites, #101 precedent):
  mass.gov, dojmt.gov, doj.nh.gov, nmdoj.gov, attorneygeneral.gov (PA),
  riag.ri.gov, atg.sd.gov, lasoregon.org, sclegal.org
- Ohio: OSLSA merged Jan 1, 2024 into Legal Aid of Southeast and Central
  Ohio (LASCO); oslsa.org and seols.org both fail curl -> name + URL updated
  to LASCO / https://www.lasco.org/ (curl 200).
- MS agency: apex https://ago.ms.gov/ curl 200 (www variant empty-reply).
- SD sources: amp.legal full-text PDF of SDCL 22-40-19..26 (curl 200);
  its quoted text matches two independent summaries.
- RI credit_monitoring_note filled from R.I. Gen. Laws 11-49.3-4(d)(5),(e)
  read verbatim Nov 20, 2026.
"""
import json

PATH = "data-breach-response/all-states.json"

AGENCY = {
    "massachusetts": "https://www.mass.gov/orgs/office-of-the-attorney-general",
    "michigan": "https://www.michigan.gov/ag/",
    "minnesota": "https://www.ag.state.mn.us/",
    "mississippi": "https://ago.ms.gov/",
    "missouri": "https://ago.mo.gov/",
    "montana": "https://dojmt.gov/office-of-consumer-protection",
    "nebraska": "https://ago.nebraska.gov/",
    "nevada": "https://ag.nv.gov/",
    "new hampshire": "https://www.doj.nh.gov/",
    "new jersey": "https://www.njoag.gov/",
    "colorado": "https://coag.gov/",
    "delaware": "https://attorneygeneral.delaware.gov/",
    "kentucky": "https://www.ag.ky.gov/",
    "louisiana": "https://ag.louisiana.gov/",
    "maine": "https://www.maine.gov/ag/",
    "maryland": "https://oag.maryland.gov/our-office/Pages/consumer-protection-division.aspx",
    "new mexico": "https://nmdoj.gov/",
    "new york": "https://ag.ny.gov/",
    "north carolina": "https://ncdoj.gov/protecting-consumers/",
    "north dakota": "https://attorneygeneral.nd.gov/",
    "ohio": "https://www.ohioattorneygeneral.gov/",
    "oklahoma": "https://oklahoma.gov/oag.html",
    "pennsylvania": "https://www.attorneygeneral.gov/",
    "rhode island": "https://riag.ri.gov/",
    "south dakota": "https://atg.sd.gov/",
    "virginia": "https://www.oag.state.va.us/",
}

LEGAL_AID = {
    "indiana": "https://www.indianalegalservices.org/applyonline/",
    "kentucky": "https://www.kyjustice.org/about-us",
    "louisiana": "https://slls.org/en/",
    "maine": "https://www.ptla.org/pine-tree-services",
    "maryland": "https://www.mdlab.org/get-help-services/",
    "michigan": "https://www.michiganlegalhelp.org",
    "montana": "https://www.mtlsa.org",
    "nebraska": "https://www.legalaidofnebraska.org",
    "nevada": "https://nevadalegalservices.org",
    "new hampshire": "https://www.nhla.org",
    "new jersey": "https://www.lsnj.org",
    "north dakota": "https://lsnd.org/about/",
    "oklahoma": "https://legalaidok.org/",
    "oregon": "https://lasoregon.org/",
    "pennsylvania": "https://palegalaid.net/",
    "rhode island": "https://www.rils.org/",
    "south carolina": "https://sclegal.org/",
    "washington": "https://www.nwjustice.org/",
    "west virginia": "https://legalaidwv.org/",
    "wisconsin": "https://legalaction.org/",
    "wyoming": "https://www.lawyoming.org/",
    "mississippi": "https://www.mslegalservices.org/",
    "missouri": "https://www.lsmo.org/",
    "new york": "https://legalaidnyc.org/",
    "ohio": "https://www.lasco.org/",
    "south dakota": "https://erlservices.org/",
}

RI_CREDIT_NOTE = (
    "Rhode Island requires state and municipal agencies \u2014 not private "
    "companies \u2014 to provide remediation services: at least 5 years of "
    "coverage for adults, and coverage until age 18 plus at least 2 more "
    "years for minors. A private company's breach notice must describe any "
    "remediation services it offers. R.I. Gen. Laws \u00a7 11-49.3-4(d)(5), (e)."
)

SD_SOURCES = ["https://www.amp.legal/pdf/South_Dakota_Breach_Law.pdf"]

def main():
    d = json.load(open(PATH))
    assert len(d) == 50, len(d)
    filled_ag = filled_la = 0
    for state, url in AGENCY.items():
        v = d[state]
        assert v.get("agency_name"), f"{state}: agency_name missing"
        assert not v.get("agency_url"), f"{state}: agency_url already set"
        v["agency_url"] = url
        filled_ag += 1
    for state, url in LEGAL_AID.items():
        v = d[state]
        assert v.get("legal_aid_name"), f"{state}: legal_aid_name missing"
        assert not v.get("legal_aid_url"), f"{state}: legal_aid_url already set"
        v["legal_aid_url"] = url
        filled_la += 1
    # Ohio org rename: OSLSA merged into LASCO Jan 1, 2024.
    assert d["ohio"]["legal_aid_name"] == "Ohio State Legal Services Association"
    d["ohio"]["legal_aid_name"] = "Legal Aid of Southeast and Central Ohio"
    # SD sources (was empty).
    assert d["south dakota"]["sources"] == []
    d["south dakota"]["sources"] = SD_SOURCES
    # RI credit-monitoring note (was empty).
    assert not d["rhode island"].get("credit_monitoring_note")
    d["rhode island"]["credit_monitoring_note"] = RI_CREDIT_NOTE
    # Final null check.
    null_ag = [k for k, v in d.items() if not v.get("agency_url")]
    null_la = [k for k, v in d.items() if not v.get("legal_aid_url")]
    null_src = [k for k, v in d.items() if not v.get("sources")]
    print(f"filled agency: {filled_ag}, legal aid: {filled_la}")
    print(f"remaining null agency: {null_ag}")
    print(f"remaining null legal aid: {null_la}")
    print(f"remaining empty sources: {null_src}")
    assert not null_ag and not null_la and not null_src
    json.dump(d, open(PATH, "w"), indent=2, ensure_ascii=False)
    print("saved", PATH)

if __name__ == "__main__":
    main()
