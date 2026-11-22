#!/usr/bin/env python3
"""Merge the 5 zoning batch files into all-states.json (lowercase keys),
applying the coordinator's verified agency-URL fixes."""
import json, glob, os

BASE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(BASE, "topic-research", "zoning-variances-land-use")

AGENCY_FIXES = {
    # (agency_name, agency_url) — all verified live by coordinator Nov 20, 2026
    "alabama": ("Alabama League of Municipalities", "https://www.almonline.org/"),
    "alaska": (None, "https://www.commerce.alaska.gov/web/dcra/"),
    "arizona": ("League of Arizona Cities and Towns", "https://www.azleague.org/"),
    "arkansas": ("Arkansas Municipal League", "https://www.armunileague.org/"),
    "california": (None, "https://lci.ca.gov/"),
    "idaho": ("Association of Idaho Cities", "https://idahocities.org/"),
    "illinois": ("Illinois Municipal League", "https://iml.org/"),
    "iowa": ("Iowa League of Cities", "https://iowaleague.org/"),
    "kansas": ("League of Kansas Municipalities", "https://www.lkm.org/"),
    "louisiana": ("Louisiana Municipal Association", "https://www.lma.org/"),
    "massachusetts": ("Massachusetts Municipal Association", "https://www.mma.org/"),
    "michigan": ("Michigan Municipal League", "https://mml.org/"),
    "minnesota": ("League of Minnesota Cities", "https://www.lmc.org/resources/land-use-variances/"),
    "mississippi": ("Mississippi Municipal League", "https://www.mmlonline.com/"),
    "missouri": ("Missouri Municipal League", "https://www.mocities.com/"),
    "montana": ("Montana League of Cities and Towns", "https://mtleague.org/"),
    "nebraska": ("League of Nebraska Municipalities", "https://www.lonm.org/"),
    "nevada": ("Nevada League of Cities and Municipalities", "https://nvleague.com/"),
    "new hampshire": ("New Hampshire Municipal Association", "https://www.nhmunicipal.org/"),
    "new jersey": ("New Jersey State League of Municipalities", "https://www.njlm.org/"),
    "oklahoma": ("Oklahoma Municipal League", "https://www.oml.org/"),
    "oregon": ("Oregon Department of Land Conservation and Development", "https://www.oregon.gov/lcd"),
    "pennsylvania": ("Pennsylvania Department of Community and Economic Development", "https://dced.pa.gov/housing-and-development/community-planning/"),
    "rhode island": ("Rhode Island Division of Statewide Planning", "https://planning.ri.gov/"),
    "south carolina": ("Municipal Association of South Carolina", "https://www.masc.sc/"),
    "vermont": (None, "https://www.vlct.org/"),  # was a bylaws PDF link; use org homepage
}

def main():
    merged = {}
    for f in sorted(glob.glob(os.path.join(DIR, "batch-*.json"))):
        d = json.load(open(f))
        for k, v in d.items():
            merged[k.lower()] = v
    assert len(merged) == 50, f"expected 50 states, got {len(merged)}"
    for state, (name, url) in AGENCY_FIXES.items():
        e = merged[state]
        if name:
            e["agency_name"] = name
        e["agency_url"] = url
    # final integrity: no nulls in any field
    FIELDS = ["variance_standard","variance_standard_note","variance_process","appeal_route",
              "appeal_deadline","nonconforming_use","nonconforming_note","statute_name",
              "statute_cite","agency_name","agency_url","legal_aid_name","legal_aid_url",
              "state_note","sources"]
    for k, v in merged.items():
        for fld in FIELDS:
            assert fld in v and v[fld], f"{k}: missing/empty {fld}"
        assert v["variance_standard"] in ("hardship","practical-difficulty","varies"), k
        assert v["nonconforming_use"] in ("protected","limited","varies"), k
    # flag suspicious URLs (PDFs, tracking params)
    for k, v in merged.items():
        for fld in ("agency_url","legal_aid_url"):
            u = v[fld]
            if u.lower().endswith(".pdf") or "?" in u and ("ref=" in u or "sfnsn" in u):
                print("SUSPICIOUS URL:", k, fld, u)
    out = os.path.join(DIR, "all-states.json")
    with open(out, "w") as f:
        json.dump(merged, f, indent=1)
    print(f"merged {len(merged)} states -> {out}")

if __name__ == "__main__":
    main()
