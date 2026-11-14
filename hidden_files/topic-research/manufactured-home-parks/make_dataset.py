#!/usr/bin/env python3
"""Build the Topic #80 dataset: Manufactured-home parks.

Source trail (coordinator, Nov 14, 2026):
- State cards (law / rent / closure / eviction / sale) and the official
  source link+label are taken VERBATIM from the buried
  "Manufactured-home parks: your rights on the lot you rent" block inside
  Tenant Rights on each state page. That block was built from official
  state sources in an earlier build; this script re-extracts it
  programmatically so the dataset is reproducible from the repo itself.
- Retaliation: verified Nov 14, 2026 against the official statute text
  (or the official legislature site) for 15 states — see RETALIATION
  below. The other 35 states get null, and the build script prints a
  claim-free fallback for them instead of inventing a rule.
- Link sweep Nov 14, 2026: all 50 official links checked — 43 returned
  HTTP 200, 3 returned 403 from official .gov bot filters (CO, MA, MT;
  kept per precedent), 4 returned curl-000 but were confirmed live by
  text fetch the same day (AK, CA, CT, IL).
- Spot-verification of headline figures against the official source
  before shipping, Nov 14, 2026:
  AK AS 34.03.225 (270-day change-of-use notice, May 1-Oct 15 quit
  window, closed eviction list) — matches the buried card verbatim.
  CA Civ. Code 798.56(g) (60-day permit notice, 6 months after permits,
  12 months if no permits) and 798.30 (90-day rent notice) — match.
  IL 765 ILCS 745/9 (90-day rent-increase notice on renewal) — match.
  OR ORS 90.600/90.645 (90-day notice, rent cap, 365-day closure,
  $6,000/$8,000/$10,000 relocation) and ORS 90.765 (retaliation) —
  match. WA RCW 59.20.070(5)/59.20.075 (retaliation, 120-day
  presumption), 59.20.090(2) (3-month rent notice), 59.20.080(1)(e)
  (12-month closure notice) — match. MN Minn. Stat. 327C.12
  (retaliation, 90-day burden shift), 327C.06 (60-day rent notice, max
  two increases per 12 months), 327C.095 (9-month closure statement) —
  match. FL 723.0615 (retaliation), AZ 33-1491 (retaliation, 6-month
  presumption), CO 38-12-212.5 (retaliation, 120-day presumption),
  NV NRS 118B.210 (retaliation), DE 25 Del. C. 7019 (retaliation,
  90-day presumption), ME 10 M.R.S. 9097(1-A) (retaliation as eviction
  defense) + 14 M.R.S. 6001(3) (6-month presumption), NH RSA 540:13-a
  and 540:13-b (retaliation defense, 6-month presumption), NJ
  N.J.S.A. 2A:42-10.10/10.12 (reprisal, rebuttable presumption),
  MA G.L. c. 186, section 18 (reprisal, 6-month presumption),
  ID Idaho Code 55-2015 (retaliation) — all confirmed.
- No phone numbers are printed anywhere in this topic.
- VT note: 9 V.S.A. 4465 is a general residential retaliation rule; the
  state's own tenant handbook says park-lot residents are covered by
  the Mobile Home Park law (10 V.S.A. ch. 153), not the general rental
  act, so VT is left claim-free on retaliation rather than cited.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
STATES = ROOT / "states"

# Retaliation text verified Nov 14, 2026 against the official statute.
# States not listed here get the claim-free fallback in the build script.
RETALIATION = {
    "arizona": (
        "Arizona's park act bans retaliation: under A.R.S. \u00a7 33-1491, a "
        "landlord may not raise rent, cut services, or bring or threaten an "
        "eviction because you complained in good faith to a housing-code "
        "agency, complained to the landlord about a violation, joined a "
        "tenants' organization, or sued the landlord. If the landlord acts "
        "within six months of your complaint, the law presumes it was "
        "retaliation, and retaliation is a defense to eviction."
    ),
    "california": (
        "The Mobilehome Residency Law has no retaliation section of its own, "
        "but California's general rule, Civil Code \u00a7 1942.5, bars a park "
        "owner from raising rent, cutting services, or seeking possession "
        "within 180 days after your good-faith complaint about habitability, "
        "a complaint to a public agency, or lawful organizing activity \u2014 "
        "and California courts have applied it to park tenancies."
    ),
    "colorado": (
        "Under C.R.S. \u00a7 38-12-212.5, park management may not take "
        "retaliatory action against a home owner who exercises any right "
        "under the Mobile Home Park Act or any other law. If management "
        "acts within 120 days after you complained to an agency or to "
        "management, joined a residents' association, or voted on a "
        "park-purchase opportunity, the action is presumed retaliatory."
    ),
    "delaware": (
        "Delaware's park act bans retaliation: under 25 Del. C. \u00a7 7019, a "
        "community owner may not pursue possession, terminate your "
        "agreement, force you to move, or cut services because you "
        "complained about a code violation, joined a tenants' organization, "
        "or sued. Action within 90 days of the protected act is presumed "
        "retaliatory, and a resident who proves retaliation can recover the "
        "greater of three months' rent or three times actual damages, plus "
        "court costs."
    ),
    "florida": (
        "Under Florida Statutes \u00a7 723.0615, a park owner may not "
        "discriminatorily raise your rent, cut services, or bring or "
        "threaten a possession action primarily to retaliate against you for "
        "complaining in good faith to a code-enforcement agency, organizing "
        "or joining a homeowners' organization, or complaining to the owner "
        "about a violation of the owner's duties. Retaliation is a defense "
        "in a possession action."
    ),
    "idaho": (
        "Under Idaho Code \u00a7 55-2015, a park landlord may not terminate or "
        "refuse to renew your tenancy, raise rent, cut services, or threaten "
        "repossession of your lot because you complained in good faith about "
        "a code violation, complained to the landlord about the park's "
        "condition, rent, or rules, joined a resident association, or hired "
        "a lawyer."
    ),
    "maine": (
        "Under 10 M.R.S. \u00a7 9097(1-A), a court may not order your tenancy "
        "terminated if you prove the eviction is primarily in retaliation "
        "for joining or helping form a landlord-tenant organization or for "
        "asserting any right under the park chapter. Maine's general rule, "
        "14 M.R.S. \u00a7 6001(3), also presumes an eviction filed within six "
        "months of a good-faith code complaint or written repair request "
        "was retaliatory."
    ),
    "massachusetts": (
        "Massachusetts' general reprisal law, G.L. c. 186, \u00a7 18, bars a "
        "landlord from raising rent, ending a tenancy, or substantially "
        "changing its terms as reprisal for reporting a code violation, "
        "complaining in writing to the landlord, joining a tenants' "
        "organization, or going to court to enforce housing law. A notice "
        "served within six months of the protected act is presumed a "
        "reprisal, and the landlord must prove otherwise by clear and "
        "convincing evidence."
    ),
    "minnesota": (
        "Under Minn. Stat. \u00a7 327C.12, a park owner may not raise rent, "
        "cut services, change your rental agreement, or seek possession as "
        "a penalty for a good-faith complaint to the owner or a government "
        "agency, for exercising your rights under state or federal law, or "
        "for joining a resident association. If the owner's action began "
        "within 90 days of the protected act, the owner must prove it was "
        "not retaliation \u2014 and retaliation is a defense in a possession "
        "action."
    ),
    "new-hampshire": (
        "Under RSA 540:13-a, it is a defense to a possessory action that the "
        "action was in retaliation for reporting a violation to the landlord "
        "or an inspection agency, starting a good-faith action under RSA "
        "540-A, or meeting with other tenants for a lawful purpose. Under "
        "RSA 540:13-b, a possessory action, rent increase, or substantial "
        "change in tenancy terms within six months of the protected act is "
        "presumed retaliatory."
    ),
    "new-jersey": (
        "New Jersey's general reprisal law, N.J.S.A. 2A:42-10.10, bars a "
        "landlord from serving a notice to quit or suing for possession as "
        "reprisal for enforcing your rights under the lease or the law, "
        "complaining in good faith to a government authority about a health "
        "or safety violation, or organizing or joining a lawful tenants' "
        "organization \u2014 and a notice that follows such an act raises a "
        "rebuttable presumption of reprisal (N.J.S.A. 2A:42-10.12)."
    ),
    "nevada": (
        "Under NRS 118B.210, a park landlord may not terminate or refuse to "
        "renew your tenancy, raise rent, cut services, or bring or threaten "
        "a possession action because you complained in good faith about a "
        "building, safety, or health code violation, complained to the "
        "landlord about the park's condition or a violation of the park act, "
        "joined a tenants' league, or won a ruling against the landlord. "
        "Willful harassment of a tenant is also prohibited."
    ),
    "oregon": (
        "Under ORS 90.765, a park landlord may not retaliate by raising rent, "
        "cutting services, serving a termination notice, or bringing or "
        "threatening a possession action after you said you would complain "
        "to an agency, made a good-faith complaint to the landlord, filed a "
        "civil-rights complaint, or asserted any right under federal, state, "
        "or local law. Retaliation is a defense to possession, and a "
        "violation can support damages of actual losses or $500, whichever "
        "is greater (ORS 90.710)."
    ),
    "washington": (
        "Under RCW 59.20.070(5), a park landlord may not evict you, refuse "
        "to renew, raise rent or other obligations, cut services, or change "
        "park rules in retaliation for filing a good-faith complaint with a "
        "government authority, asking the landlord to comply with the law, "
        "suing the landlord, or joining a homeowners association. Under RCW "
        "59.20.075, action within 120 days of the protected act is presumed "
        "retaliatory."
    ),
}

CARD_TITLES = {
    "law": "The law that governs your lot in ",
    "rent": "Lot-rent increases in ",
    "closure": "If the park closes or changes use in ",
    "eviction": "Eviction from a park in ",
    "sale": "Selling your home \u2014 and a chance to buy the park \u2014 in ",
}


def clean(text):
    return html.unescape(re.sub(r"<[^>]+>", "", text)).strip()


def main():
    out = {"states": {}}
    for path in sorted(STATES.glob("*.html")):
        slug = path.stem
        text = path.read_text()
        m = re.search(
            r"Manufactured-home parks: your rights on the lot you rent</h3>"
            r"(.*?)<h3>Rent going up",
            text,
            re.S,
        )
        assert m, f"{slug}: buried block not found"
        block = m.group(1)
        cards = re.findall(
            r'<p class="r-tag[^"]*">(.*?)</p>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>'
            r"(?:\s*<a class=\"r-link\" href=\"([^\"]+)\"[^>]*>)?",
            block,
            re.S,
        )
        entry = {"slug": slug, "state": None, "law": None, "rent": None,
                 "closure": None, "eviction": None, "sale": None,
                 "link": None, "link_label": None,
                 "retaliation": RETALIATION.get(slug)}
        for tag, h, body, link in cards:
            tag, h, body = clean(tag), clean(h), clean(body)
            if tag.startswith("In "):
                state = tag[3:]
                entry["state"] = state
                for key, prefix in CARD_TITLES.items():
                    if h == prefix + state:
                        entry[key] = body
            elif tag == "Official source":
                entry["link"] = link
                entry["link_label"] = h
        assert entry["state"], f"{slug}: state name not found"
        for key in ("law", "rent", "closure", "eviction"):
            assert entry[key], f"{slug}: missing {key} card"
        assert entry["link"] and entry["link_label"], f"{slug}: missing official link"
        out["states"][slug] = entry
    assert len(out["states"]) == 50, len(out["states"])
    n_sale = sum(1 for s in out["states"].values() if s["sale"])
    n_retal = sum(1 for s in out["states"].values() if s["retaliation"])
    print(f"50 states; sale card present in {n_sale}; retaliation verified in {n_retal}")
    dest = Path(__file__).resolve().parent / "all-states.json"
    dest.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {dest}")


if __name__ == "__main__":
    main()
