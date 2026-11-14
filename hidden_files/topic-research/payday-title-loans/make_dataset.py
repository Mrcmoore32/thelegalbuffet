#!/usr/bin/env python3
"""Build the Topic #81 (Payday / title loans) dataset.

Coordinator-written, Nov 14, 2026. Per-state payday law, title-loan law,
and the official regulator link are reused VERBATIM from the buried
"Payday loans, title loans, and the safer ways out" cluster inside Credit
Card & Debt on each state page (hidden_files/topic-research/
payday-title-loans/buried-extract.json), which was built from official
state sources. The cap / max-loan / max-term / license cells in the
at-a-glance table are drawn from that same buried text, except Alaska
($500 max outstanding, 14-day minimum — AS 06.50.410/440, verified
against akleg.gov this session) and Delaware ($1,000, under 60 days —
5 Del. C. ch. 22 / DE Reg. 2210, verified this session).

Status map (from the buried text):
- banned (12): AZ, AR, CT, GA, MD, MA, NJ, NY, NC, PA, VT, WV
- capped36 (11): CO, HI, IL, MN, MT, NE, NH, NM, OR, SD, VA
- reformed (2): ME (30% ceiling), OH (28% + 60% total cap, installment)
- allowed (25): AL, AK, CA, DE, FL, ID, IN, IA, KS, KY, LA, MI, MS, MO,
  NV, ND, OK, RI, SC, TN, TX, UT, WA, WI, WY

Extended payment plans (EPP): verified against OFFICIAL statute or
regulator text this session for 16 states (cite in the epp field).
All other states get a claim-free fallback in the build script — NOT
an invented EPP. Two secondary-source claims were REJECTED by that
verification and are deliberately absent:
- Missouri: an EPP appears only in a 2014 bill (SB 694) that was never
  enacted; current Mo. Rev. Stat. 408.500 has no EPP.
- Oklahoma: the old deferred-deposit EPP died with deferred deposit
  lending on Aug 1, 2020; Small Lender Act loans are installment loans.
- California: no verified EPP in the permanent Deferred Deposit
  Transaction Law (the 2020 payment-plan bill was COVID-temporary).

Headline figures spot-verified before shipping:
- $15 per $100 for 14 days = 15% x 365/14 = 391% APR (computed; also
  corroborated by a second source).
- PAL I $200-$1,000 / PAL II up to $2,000, 28% APR cap, $20 max
  application fee, no rollovers (NCUA rule, corroborated by NCUA
  summaries and Experian).
- VA: 36% interest + maintenance fee <= lesser of 8% or $25/mo +
  50%/60% total-charges cap (Va. Code 6.2-1817, 6.2-1818.3, law.lis).
- FL title tiers 30/24/18% (Fla. Stat. 537.011, flsenate.gov).
- OK: 17% per month, $1,500 aggregate principal (adjusted yearly),
  60 days-12 months installment (Small Lenders Act; Hudson Cook +
  ODCC figures).
- OH: 28% interest, $1,000 max, 91 days-1 year, 60% total cap
  (R.C. 1321.40; corroborated by multiple sources).
- RI deferred-deposit law repealed eff. Jan 1, 2027 (buried text;
  corroborated by a second source).
No phone numbers are printed anywhere in this topic.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
SRC = ROOT / "hidden_files" / "topic-research" / "payday-title-loans" / "buried-extract.json"
OUT = ROOT / "hidden_files" / "topic-research" / "payday-title-loans" / "all-states.json"

STATUS = {
    "alabama": "allowed", "alaska": "allowed", "arizona": "banned",
    "arkansas": "banned", "california": "allowed", "colorado": "capped36",
    "connecticut": "banned", "delaware": "allowed", "florida": "allowed",
    "georgia": "banned", "hawaii": "capped36", "idaho": "allowed",
    "illinois": "capped36", "indiana": "allowed", "iowa": "allowed",
    "kansas": "allowed", "kentucky": "allowed", "louisiana": "allowed",
    "maine": "reformed", "maryland": "banned", "massachusetts": "banned",
    "michigan": "allowed", "minnesota": "capped36", "mississippi": "allowed",
    "missouri": "allowed", "montana": "capped36", "nebraska": "capped36",
    "nevada": "allowed", "new-hampshire": "capped36", "new-jersey": "banned",
    "new-mexico": "capped36", "new-york": "banned",
    "north-carolina": "banned", "north-dakota": "allowed",
    "ohio": "reformed", "oklahoma": "allowed", "oregon": "capped36",
    "pennsylvania": "banned", "rhode-island": "allowed",
    "south-carolina": "allowed", "south-dakota": "capped36",
    "tennessee": "allowed", "texas": "allowed", "utah": "allowed",
    "vermont": "banned", "virginia": "capped36", "washington": "allowed",
    "west-virginia": "banned", "wisconsin": "allowed", "wyoming": "allowed",
}

# status label shown in the at-a-glance table
STATUS_LABEL = {
    "banned": "Banned — payday lending is illegal",
    "capped36": "Capped at 36% APR — no classic payday loan",
    "reformed": "Reformed — installment loans only, no classic payday loan",
    "allowed": "Legal and licensed — fee and term limits apply",
}

# (cap, max_loan, max_term, license) — None = not stated in sources checked
TABLE = {
    "alabama": ("Fee no more than 17.5% of the amount advanced",
                "$500", "10 to 31 days",
                "Licensed by the Alabama Banking Department"),
    "alaska": ("No APR cap stated in the sources checked",
               "$500 outstanding with one licensee", "At least 14 days",
               "Licensed by the Division of Banking & Securities"),
    "arizona": ("36% usury cap (A.R.S. 44-1201)",
                None, None, "Not authorized — no payday license"),
    "arkansas": ("17% constitutional cap on consumer loans",
                 None, None, "Illegal — no payday license"),
    "california": ("Fee no more than 15% of the check ($45 maximum on a $300 loan)",
                   "$300 (face amount of the check)", "Up to 31 days",
                   "License required — Department of Financial Protection and Innovation"),
    "colorado": ("36% APR cap, with limits on origination and monthly maintenance charges",
                 None, None, "Supervised-loan framework under the Uniform Consumer Credit Code"),
    "connecticut": ("12% cap on small loans",
                    None, None, "Illegal — no payday license"),
    "delaware": ("No rate cap; database and frequency limits apply",
                 "$1,000", "Under 60 days",
                 "Licensed by the Office of the State Bank Commissioner"),
    "florida": ("Fee no more than 10% plus a verification fee of up to $5",
                "$500", "7 to 31 days",
                "Licensed by the Office of Financial Regulation"),
    "georgia": ("Payday lending illegal under O.C.G.A. 16-17-1 et seq.",
                None, None, "Illegal — unlicensed loans are void"),
    "hawaii": ("36% interest a year, plus a monthly maintenance fee of up to $35; total charges no more than half the amount borrowed",
               "$1,500", "2 to 12 months, in installments",
               "Licensed installment lenders under HRS Chapter 480J"),
    "idaho": ("No fee cap — the fee must be disclosed in dollars and as an APR",
             "$1,000 (no more than 25% of gross monthly income)", None,
             "Licensed by the Department of Finance"),
    "illinois": ("36% all-in APR cap (Predatory Loan Prevention Act)",
                 None, None,
                 "Licensed by IDFPR — a loan over the cap is void"),
    "indiana": ("Tiered fee: 15% of the first $250, 13% of the next $150, 10% above $400",
                "$605", "At least 14 days",
                "Licensed by the Department of Financial Institutions"),
    "iowa": ("Fee capped on a sliding scale ($15 on the first $100, $10 on each additional $100; $55 maximum on a $500 loan)",
             "$500", "No more than 31 days",
             "Licensed by the Division of Banking"),
    "kansas": ("Fee no more than 15% of the cash advance",
               "$500", "7 to 30 days",
               "Licensed by the Office of the State Bank Commissioner"),
    "kentucky": ("Service fee no more than $15 per $100 advanced",
                 "$500", "14 to 60 days",
                 "Licensed by the Department of Financial Institutions (no new deferred deposit licenses since 2019)"),
    "louisiana": ("Fee no more than 16.75% of the face amount of the check, plus a $10 documentation fee",
                  "$350", "No more than 30 days",
                  "Licensed by the Office of Financial Institutions"),
    "maine": ("Rate ceilings, including a 30% ceiling on smaller supervised loans",
              None, None, "Supervised-lender license required"),
    "maryland": ("33% a year on the first $1,000 of a loan of $2,000 or less; 24% above that",
                 None, None, "Illegal — payday lenders are not licensed"),
    "massachusetts": ("23% a year plus a $20 administrative fee on loans of $6,000 or less",
                      None, None, "Not permitted — no payday license"),
    "michigan": ("Service fee on a sliding scale: 15% of the first $100 down to 11% of each $100 above $400",
                 "$600", "No more than 31 days",
                 "Licensed by the Department of Insurance and Financial Services"),
    "minnesota": ("36% APR on consumer short-term loans of $1,000 or less",
                  "$1,000 (short-term loans)", None,
                  "Licensed by the Department of Commerce"),
    "mississippi": ("Fee set by statute (the Department's example: a $20 fee on a $100 advance)",
                    "$500 in check advances outstanding", "Deposit delayed up to 30 days",
                    "Licensed by the Department of Banking and Consumer Finance"),
    "missouri": ("No APR cap; total interest and fees no more than 75% of the original loan amount",
                 "$500", "14 to 31 days",
                 "Licensed under sections 408.500-408.506, RSMo"),
    "montana": ("36% APR cap (Initiative 164, 2010)",
                "$300 (not counting the fee)", "No more than 31 days",
                "Licensed by the Division of Banking and Financial Institutions"),
    "nebraska": ("36% APR cap (Initiative 428, 2020)",
                 "$500 in total, including fees", "Check held no more than 34 days",
                 "Licensed by the Department of Banking and Finance"),
    "nevada": ("No APR cap",
               "25% of expected gross monthly income", "Initial term no more than 35 days",
               "Licensed under NRS Chapter 604A"),
    "new-hampshire": ("36% APR cap on small loans of $10,000 or less (RSA 399-A)",
                      None, None, "Licensed under RSA 399-A"),
    "new-jersey": ("30% for most consumer lending by licensed lenders; above the criminal usury ceiling is a crime",
                   None, None, "Illegal — no payday license"),
    "new-mexico": ("36% APR cap on loans of $10,000 or less",
                   None, None, "Licensed by the Financial Institutions Division"),
    "new-york": ("16% civil usury cap; over 25% is criminal usury",
                 None, None, "Illegal — no payday license"),
    "north-carolina": ("Consumer Finance Act rate caps (about 30%)",
                       None, None, "Illegal — unlicensed loans are void"),
    "north-dakota": ("Fee no more than 20% of the amount advanced",
                     "$500", "No more than 60 days",
                     "Licensed by the Department of Financial Institutions"),
    "ohio": ("28% interest; total fees and interest no more than 60% of the principal",
             "$1,000", "91 days to 1 year, in installments",
             "Licensed by the Division of Financial Institutions"),
    "oklahoma": ("17% interest per month",
                 "$1,500 total principal across all lenders (adjusted yearly)",
                 "60 days to 12 months, in installments",
                 "Licensed by the Department of Consumer Credit"),
    "oregon": ("36% APR; origination fee up to $10 per $100 borrowed, capped at $30",
               None, "Initial term at least 31 days",
               "Licensed by the Division of Financial Regulation"),
    "pennsylvania": ("About 24% for licensed consumer discount companies; 6% for unlicensed lending",
                     None, None, "Illegal — no payday license"),
    "rhode-island": ("Fee no more than 10% of the face amount of the check",
                     "$500", "At least 13 days",
                     "Licensed check cashers — framework repealed January 1, 2027, when a 36% cap takes its place"),
    "south-carolina": ("Fee no more than 15% of the face amount of the check",
                       "$550", "No more than 31 days",
                       "Licensed under the Deferred Presentment Services Act"),
    "south-dakota": ("36% all-in APR cap (Initiated Measure 21, 2016)",
                     "$500 total principal outstanding with one borrower", None,
                     "Money lender license required"),
    "tennessee": ("Service charge no more than 15% of the face amount of the check",
                  "$500 face amount", "No more than 31 days",
                  "Licensed by the Department of Financial Institutions"),
    "texas": ("No cap on the credit services organization (CSO) fee or the rate",
              None, None,
              "CSO registration under Finance Code ch. 393; many cities add local limits"),
    "utah": ("No fee cap stated; no interest may be collected once a loan has been outstanding 10 weeks",
             None, "Repayment no more than 10 weeks from the day the loan was made",
             "Registered with the Department of Financial Institutions"),
    "vermont": ("18-24% licensed-lender rates, depending on loan type and balance",
                None, None, "Not permitted — no payday license"),
    "virginia": ("36% interest a year, plus a monthly maintenance fee of no more than the lesser of 8% of the loan amount or $25; total fees and charges no more than 50% of the amount borrowed on loans of $1,500 or less (60% above that)",
                 None, "4 to 24 months, in installments",
                 "Licensed by the State Corporation Commission, Bureau of Financial Institutions"),
    "washington": ("Tiered fee: $15 per $100 on the first $500, $10 per $100 above $500",
                   "$700 or 30% of gross monthly income (whichever is less)",
                   "Based on the borrower's next pay date",
                   "Licensed by the Department of Financial Institutions"),
    "west-virginia": ("Consumer Credit and Protection Act rate ceilings",
                      None, None, "Illegal — no payday license"),
    "wisconsin": ("No APR cap on payday loans",
                  "$1,500 or 35% of gross monthly income (whichever is less)",
                  "No more than 90 days",
                  "Licensed by the Department of Financial Institutions"),
    "wyoming": ("Finance charge no more than the greater of $30 or 20% of the amount advanced",
                "$1,000", "No more than one calendar month",
                "Licensed postdated check service providers (Division of Banking)"),
}

# Verified extended-payment-plan sentences (official statute/regulator text
# checked Nov 14, 2026). None = no verified EPP right printed for that state.
EPP = {
    "alabama": "After the first loan period and one rollover, if you still cannot pay in full, Alabama law lets the lender offer you four equal monthly installments of what is left (Ala. Code \u00a7 5-18A-12(c)). It is the lender\u2019s choice, not a right \u2014 ask for it in writing, and if the lender says no, complain to the Banking Department.",
    "alaska": "Before sending a defaulted advance to collections or suing, the lender must offer you a payment plan of up to six months, with at least 5% of the balance due when you sign and no added fee (AS 06.50.550).",
    "delaware": "After the maximum rollovers, the lender may enter a \u201cworkout agreement\u201d with you: equal installments over at least 90 days, with no added fee, interest, or charge (5 Del. C. \u00a7\u00a7 2227(8), 2235A). It is the lender\u2019s choice after the rollover limit \u2014 ask for it in writing.",
    "florida": "Florida gives you a 60-day grace period, not a rollover: tell the lender you cannot pay, complete the credit counseling the lender must arrange, and the term extends 60 days with no additional charge (Fla. Stat. \u00a7 560.404).",
    "idaho": "Idaho law requires the lender to let you enter an extended payment plan once in any 12-month period if you ask, with no interest or additional fees (Idaho Code \u00a7 28-46-414). Ask before the due date.",
    "illinois": "If you still owe on one or more payday loans after 35 days, you are entitled to a repayment plan of at least 55 days, in at least four equal installments, with no additional finance charges, interest, or fees (815 ILCS 122/2-40). Ask within 28 days after the loan\u2019s default date.",
    "indiana": "After your third consecutive small loan, the lender must offer you an extended payment plan: at least four equal installments over at least 60 days, with no fee for entering the plan (IC 24-4.5-7-401). Ask during the loan term, before you default.",
    "louisiana": "You may elect an extended payment plan once in any 12-month period \u2014 at least four substantially equal installments \u2014 but you must ask before the due date (La. R.S. 9:3578.4.1). The lender must print this right on the first page of your agreement.",
    "michigan": "If you have taken eight deferred presentment transactions in 12 months, the lender must offer you a written repayment plan: three equal installments tied to your next three paydays, for a small administration fee (MCL 487.2155). Ask within 30 days after the maturity date.",
    "nebraska": "If you cannot pay when the loan is due, you may elect once in any 12-month period to repay it in at least four equal payments on your pay dates, at no additional cost and with no interest or fees during the plan (Neb. Rev. Stat. \u00a7 45-919.01). Ask before the due date.",
    "nevada": "A Nevada deferred deposit licensee must offer you a repayment plan if you cannot repay under the loan agreement, and must tell you the plan exists (NRS 604A.578, 604A.5027). Ask for it in writing before the due date.",
    "south-carolina": "You may elect an extended payment plan once in any 12-month period (S.C. Code \u00a7 34-39-280). Ask before the due date and get the installment schedule in writing.",
    "utah": "Utah law requires the lender to let you enter an extended payment plan at least once in a 12-month period if you ask (Utah Code \u00a7 7-23-403). The lender must give you written notice of this right when you take the loan.",
    "washington": "If you tell the lender you cannot repay when the loan is due, the lender must convert the loan to an installment plan if you ask: at least 90 days to repay (180 days for loans over $400), with no extra fee or interest (RCW 31.45.084).",
    "wisconsin": "If you cannot repay in full at the end of the term, the lender must offer you four equal installments on your pay schedule, at no cost and with no interest while you are on the plan (Wis. Stat. \u00a7 138.14(11g)). You get this offer once in 12 months.",
    "wyoming": "You may elect an extended payment plan once every 12 months \u2014 at least four substantially equal installments over at least 60 days, at no additional cost \u2014 but you must ask before 5:00 p.m. Mountain Time on the last business day before the due date (Wyo. Stat. \u00a7 40-14-366).",
}


# Link overrides (Nov 14, 2026 link sweep): the buried cluster's link for
# these two states is dead (curl 404 + text-fetch 404). The new section
# uses the current official page instead. The buried cluster still links
# the dead URL — flagged for the daily audit, out of this build's scope.
LINK_OVERRIDES = {
    "north-dakota": (
        "https://www.nd.gov/faq/financial-institutions-faq",
        "North Dakota Department of Financial Institutions - Financial "
        "Institutions FAQ (incl. Deferred Presentment / Payday Lenders)",
    ),
    "ohio": (
        "https://com.ohio.gov/",
        "Ohio Department of Commerce - Division of Financial Institutions",
    ),
}

# states whose loans are already installment loans by law (no separate EPP)
INSTALLMENT_STATES = {"hawaii", "ohio", "oklahoma", "virginia"}


def status_line(slug, state):
    st = STATUS[slug]
    if st == "banned":
        return f"Payday lending is illegal in {state}."
    if st == "capped36":
        return (f"In {state}, payday-style loans are capped at 36% APR "
                f"\u2014 the classic two-week loan at triple-digit rates "
                f"cannot legally operate here.")
    if slug == "maine":
        return ("In Maine, small-loan rate ceilings (about 30% a year on "
                "smaller loans) leave no room for the classic triple-digit "
                "payday loan.")
    if slug == "ohio":
        return ("Ohio replaced the classic payday loan with installment "
                "short-term loans: 28% interest, all charges capped at 60% "
                "of the principal, repaid over 91 days to a year.")
    if slug == "texas":
        return ("In Texas, payday and title loans run through the credit "
                "services organization (CSO) model \u2014 there is no state "
                "cap on the CSO fee, though many cities add local limits.")
    if slug == "rhode-island":
        return ("Payday lending is still legal in Rhode Island, but the "
                "framework is repealed January 1, 2027, when a 36% cap "
                "takes its place.")
    return (f"Payday lending is legal and licensed in {state}, within the "
            f"limits in the table below.")


def main():
    buried = json.loads(SRC.read_text())["states"]
    assert len(buried) == 50
    out = {"states": {}}
    for slug in sorted(buried):
        b = buried[slug]
        assert b["payday"] and b["title"] and b["link"], slug
        cap, mx, term, lic = TABLE[slug]
        link, link_label = b["link"], b["link_label"]
        if slug in LINK_OVERRIDES:
            link, link_label = LINK_OVERRIDES[slug]
        out["states"][slug] = {
            "slug": slug,
            "state": b["state"],
            "status": STATUS[slug],
            "status_label": STATUS_LABEL[STATUS[slug]],
            "status_line": status_line(slug, b["state"]),
            "cap": cap,
            "max_loan": mx,
            "max_term": term,
            "license": lic,
            "payday": b["payday"],
            "title": b["title"],
            "epp": EPP.get(slug),
            "epp_installment": slug in INSTALLMENT_STATES,
            "link": link,
            "link_label": link_label,
        }
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {OUT} ({len(out['states'])} states)")
    print("banned:", sum(1 for s in out["states"].values() if s["status"] == "banned"))
    print("capped36:", sum(1 for s in out["states"].values() if s["status"] == "capped36"))
    print("reformed:", sum(1 for s in out["states"].values() if s["status"] == "reformed"))
    print("allowed:", sum(1 for s in out["states"].values() if s["status"] == "allowed"))
    print("epp verified:", sum(1 for s in out["states"].values() if s["epp"]))
    print("installment fallback:", sum(1 for s in out["states"].values() if s["epp_installment"]))


if __name__ == "__main__":
    main()
