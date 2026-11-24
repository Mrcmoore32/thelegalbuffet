#!/usr/bin/env python3
"""Merge the 5 Forming an LLC research batches into all-states.json.

Source batches (10 states each, researchers' final JSON, saved 2026-11-24):
  batch-al-ga.json, batch-hi-md.json, batch-ma-nj.json, batch-nm-sc.json,
  batch-sd-wy.json  (hidden_files/topic-research/forming-an-llc/)

Adds legal_aid_name / legal_aid_url per state, reused from the #112
dataset (hidden_files/topic-research/protecting-kids-online/all-states.json),
which carries the same per-state legal-aid listing.

Fixes applied at merge (coordinator, 2026-11-24):
1. Wisconsin series_llc citation corrected: the batch cited "Wis. Stat.
   Chapter 183, Subchapter XIII" — Subchapter XIII is Miscellaneous, not
   series law. The series provision is Wis. Stat. sec. 183.0504 ("Series
   of members, managers, or limited liability company interests"),
   confirmed on docs.legis.wisconsin.gov. The weaker-shield caveat is
   kept: Wisconsin's provision lets an operating agreement create series
   of members/interests, but it does not clearly give each series its own
   liability shield the way Delaware-style series laws do.
2. Foreign LLC registration fees added where the batch left the fee out.
   Verified 2026-11-24 against multiple October/November 2026 sources
   tracing to the official Secretary of State pages:
   - Idaho: $100 online / $120 on paper (Foreign Registration Statement;
     $20 manual-processing fee on paper filings).
   - Indiana: $105 online / $125 on paper (Foreign Registration Statement,
     State Form 56369; $75 statutory fee + $30 enhanced-access fee online).
   - Kansas: $115 (Application for Registration, Form FA). (An older $165
     figure in some guides predates the Feb 27, 2026 fee cut.)
   - Tennessee: $300 minimum ($50 per member, $300-$3,000; Form SS-4233).
   - Utah: $59 (foreign registration statement).
   - Vermont: $155 (application for certificate of authority).
   - Wyoming: $150 (Certificate of Authority, FLLC-CertificateAuthority).

Spot verifications 2026-11-24 (all confirmed unless noted):
- Vermont formation $155 / annual report $45 — 11 V.S.A. sec. 4012
  (Act 77 of 2023); the SOS fee page's older $125/$35 figures are stale.
- New Jersey formation $100 — DORES Registry Fee Schedule, P.L. 2026,
  c.24, effective July 1, 2026 (was $125).
- Missouri formation $50 online / $105 on paper — SOS Schedule of Fees
  (RSMo 347.179 $45/$100 + $5 Technology Fund).
- Delaware annual LLC tax $400 for tax year 2026 onward — HB 400
  (85 Del. Laws c. 273), effective Jan 1, 2026; first $400 payment due
  June 1, 2027 (the June 1, 2026 payment covered tax year 2025 at $300).
- West Virginia series LLCs — SB 670 (2026), W. Va. Code sec. 31B-14-101
  et seq., effective June 12, 2026; protected series designated on
  Form LLD-11, $25.
- Utah series LLCs — Utah Code sec. 48-3a-1201 (designated series of
  transferable interests; notice of liability limitation in the
  certificate of organization).
- Florida series LLCs — Fla. Stat. 605.2101-605.2802, Uniform Protected
  Series Provisions, effective July 1, 2026 (SB 316 / CS/HB 403);
  designate a protected series online for $25 per series.
- Kansas formation $85 online / $90 on paper — SOS Form DL (Rev. 2/27/26);
  fee cut from $160/$165 effective Feb 27, 2026.
- Indiana biennial Business Entity Report $32 online / $50 on paper;
  formation $95 online / $100 on paper.
- Montana series LLCs — MCA secs. 35-8-202, 35-8-304 (HB 362, 2013).
  Montana formation $35 (sosmt.gov fee schedule); annual report $20,
  waived for on-time filings in 2026 and 2027.
- Nebraska series LLCs — Neb. Rev. Stat. secs. 21-501 to 21-542,
  Uniform Protected Series Act (LB1121, 2018; effective Jan 1, 2021).
- Ohio series LLCs — Ohio Rev. Code secs. 1706.76-1706.7613 (new LLC act,
  effective Jan 1, 2022).
- Louisiana formation $125 / annual report $35 / foreign $185 — Act 921
  of 2026, SOS fee schedule effective Oct 1, 2026 (was $100/$30).
- Arkansas formation $45 online / $50 on paper (Form LL-01) — SOS LLC
  forms and fees table.

Claim-free fields (gap rule — line omitted, field never removed):
series_llc empty in HI, ID, KY, LA, ME, NM, RI, SC (published lists
conflict; no verified answer). single_member empty in many states —
the builder falls back to the national line "a single person can form
an LLC in every state" (true in all 50; no state requires two members).

No phone numbers in any batch. No phone numbers are printed in the
state sections.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "hidden_files" / "topic-research" / "forming-an-llc"
KIDS = ROOT / "hidden_files" / "topic-research" / "protecting-kids-online" / "all-states.json"
OUT = DIR / "all-states.json"

BATCHES = ["batch-al-ga.json", "batch-hi-md.json", "batch-ma-nj.json",
           "batch-nm-sc.json", "batch-sd-wy.json"]

# Foreign LLC fees the batches left out (see header for verification).
FOREIGN_FEE_ADD = {
    "idaho": " A foreign LLC must file a foreign registration statement with the Idaho Secretary of State before transacting business in Idaho; the fee is $100 online ($120 on paper, which adds a $20 manual-processing fee).",
    "indiana": " A foreign LLC must file a Foreign Registration Statement with the Indiana Secretary of State through INBiz before transacting business in Indiana; the fee is $105 online / $125 on paper (State Form 56369).",
    "kansas": " A foreign LLC must register with the Kansas Secretary of State before transacting business in Kansas; the fee is $115 (Application for Registration, Form FA).",
    "tennessee": " An LLC formed in another state must file an Application for Certificate of Authority with the Tennessee Secretary of State before transacting business in Tennessee and must maintain a Tennessee registered agent; the fee is $300 minimum ($50 per member, $300 to $3,000).",
    "utah": " A foreign LLC must file an Application for Registration with the Division of Corporations and Commercial Code before transacting business in Utah and must maintain a Utah registered agent; the fee is $59.",
    "vermont": " A foreign LLC must obtain a certificate of authority from the Vermont Secretary of State before transacting business in Vermont and must maintain a Vermont agent for service of process; the fee is $155.",
    "wyoming": " A foreign LLC must file a Certificate of Authority with the Wyoming Secretary of State before transacting business in Wyoming and must maintain a Wyoming registered agent; the fee is $150.",
}

WI_SERIES_FIXED = (
    "Yes — Wisconsin law lets an operating agreement create designated "
    "series of members, managers, or LLC interests (Wis. Stat. sec. 183.0504), "
    "but Wisconsin law lacks a clear inter-series liability shield, so the "
    "protection is weaker than in some other series states — get local advice "
    "before relying on a series structure here."
)


def main():
    merged = {}
    for name in BATCHES:
        batch = json.loads((DIR / name).read_text())
        assert isinstance(batch, dict) and len(batch) == 10, f"{name}: bad shape"
        for slug, e in batch.items():
            assert slug not in merged, f"duplicate slug {slug}"
            assert e.get("slug") == slug, f"{slug}: slug field mismatch"
            merged[slug] = e
    assert len(merged) == 50, f"merged {len(merged)} states"

    kids = json.loads(KIDS.read_text())
    assert len(kids) == 50, "kids dataset not 50"
    for slug, e in merged.items():
        assert slug in kids, f"{slug}: no legal-aid entry in #112 dataset"
        e["legal_aid_name"] = kids[slug]["legal_aid_name"]
        e["legal_aid_url"] = kids[slug]["legal_aid_url"]

    # Fix 1: Wisconsin series citation.
    wi = merged["wisconsin"]
    assert "Subchapter XIII" in wi["series_llc"], "WI series text changed?"
    wi["series_llc"] = WI_SERIES_FIXED

    # Fix 2: foreign fees.
    for slug, suffix in FOREIGN_FEE_ADD.items():
        e = merged[slug]
        assert "$" not in e["foreign_llc"], f"{slug}: foreign fee already present?"
        e["foreign_llc"] = e["foreign_llc"].rstrip() + suffix

    # Validation.
    req = ["state", "slug", "overview", "filing_fee", "fee_verified_url",
           "filing_office", "filing_url", "registered_agent",
           "operating_agreement", "annual_report", "series_llc",
           "foreign_llc", "single_member", "sources",
           "legal_aid_name", "legal_aid_url"]
    phone_re = re.compile(
        r"\(\d{3}\)\s*\d{3}[-.]\d{4}|\b\d{3}[-.]\d{3}[-.]\d{4}\b|"
        r"1-800-\d{3}-\d{4}|1-866-\d{3}-\d{4}|1-888-\d{3}-\d{4}|1-855-\d{3}-\d{4}|"
        r"877-\d{3}-\d{4}|800-\d{3}-\d{4}|844-\d{3}-\d{4}|866-\d{3}-\d{4}|855-\d{3}-\d{4}"
    )
    for slug, e in sorted(merged.items()):
        for f in req:
            assert f in e, f"{slug}: missing {f}"
        for f in ["state", "overview", "filing_fee", "filing_office",
                  "filing_url", "registered_agent", "operating_agreement",
                  "annual_report", "foreign_llc", "legal_aid_name",
                  "legal_aid_url"]:
            assert e[f], f"{slug}: empty {f}"
        assert e["sources"] and len(e["sources"]) >= 1, f"{slug}: no sources"
        assert e["filing_url"].startswith("http"), f"{slug}: bad filing_url"
        assert e["legal_aid_url"].startswith("http"), f"{slug}: bad legal_aid_url"
        blob = json.dumps({k: v for k, v in e.items() if k != "sources"})
        assert not phone_re.search(blob), f"{slug}: phone-like string in data"
        assert "TODO" not in blob and "FIXME" not in blob, f"{slug}: marker"
        assert all(v is not None for v in e.values()), f"{slug}: null value"
    empty_series = [s for s, e in sorted(merged.items()) if not e["series_llc"]]
    empty_single = [s for s, e in sorted(merged.items()) if not e["single_member"]]
    print(f"merged 50 states; series_llc claim-free in: {', '.join(empty_series)}")
    print(f"single_member empty (national fallback used) in: {', '.join(empty_single)}")
    OUT.write_text(json.dumps(merged, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
