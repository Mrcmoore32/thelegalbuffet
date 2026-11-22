#!/usr/bin/env python3
"""Merge Topic #102: Data Breach Response — 5 research batches into
hidden_files/topic-research/data-breach-response/all-states.json.

Normalizations (coordinator, 2026-11-20):
- Keys lowercased at merge (same lesson as #99: page files are lowercase).
- AG-notification coding normalized: the AL-GA researcher coded
  threshold-based AG notice as "yes", while the other four batches coded
  the same pattern as "varies". Uniform rule applied: "yes" = AG notice
  for EVERY breach (no minimum); "varies" = threshold-based; "no" = none.
  States flipped yes -> varies: AL (1,000+), AZ (1,000+), AR (1,000+),
  CA (500+), CO (500+), DE (500+), FL (500+). True every-breach "yes"
  states kept: CT, IN, LA, MA, MD, ME, MT, NC, NE, NH, NY, VT, VA.
  Post-normalization counts: yes 13 / varies 23 / no 14.
- perfectlyparalegal.com/legal-aid-resources/ stripped from sources
  (weak roundup in all 10 MA-NJ states; statute links are the real
  verification sources).
- NH notification_deadline kept verbatim as "as soon as possible"
  (the statute's own wording, RSA 359-C:20); counted with the
  no-fixed-days states in headline counts.

Headline counts (post-normalization): notification deadline
"without unreasonable delay" 27 / "as soon as possible" 1 (NH) /
45 days 11 / 30 days 6 / 60 days 5; credit monitoring required 5
(CA, CT, DE, MA, PA) / varies 1 (RI) / not-required 44; private
right of action yes 4 (HI, LA, TN, WA) / limited 12 / no 34.
No phone numbers in the dataset.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "hidden_files" / "topic-research" / "data-breach-response"

BATCHES = ["batch-al-ga.json", "batch-hi-md.json", "batch-ma-nj.json",
           "batch-nm-sc.json", "batch-sd-wy.json"]

# Threshold-based AG notice miscoded as "yes" by the AL-GA researcher.
AG_YES_TO_VARIES = {"alabama", "arizona", "arkansas", "california",
                    "colorado", "delaware", "florida"}

merged = {}
for f in BATCHES:
    batch = json.loads((DIR / f).read_text())
    for state, entry in batch.items():
        key = state.lower()
        assert key not in merged, f"duplicate state {state}"
        merged[key] = entry

assert len(merged) == 50, f"expected 50 states, got {len(merged)}"

for key, entry in merged.items():
    if key in AG_YES_TO_VARIES:
        assert entry["ag_notification"] == "yes", key
        entry["ag_notification"] = "varies"
    # strip weak roundup from sources
    entry["sources"] = [u for u in entry.get("sources", [])
                        if "perfectlyparalegal.com" not in u]

from collections import Counter
print("states:", len(merged))
print("deadlines:", Counter(v["notification_deadline"] for v in merged.values()))
print("ag:", Counter(v["ag_notification"] for v in merged.values()))
print("credit:", Counter(v["credit_monitoring"] for v in merged.values()))
print("private right:", Counter(v["private_right_of_action"] for v in merged.values()))
print("null agency_url:", sorted(k for k, v in merged.items() if not v.get("agency_url")))
print("null legal_aid_url:", sorted(k for k, v in merged.items() if not v.get("legal_aid_url")))
print("empty sources:", sorted(k for k, v in merged.items() if not v.get("sources")))

(DIR / "all-states.json").write_text(json.dumps(merged, indent=2, sort_keys=True) + "\n")
print("wrote all-states.json")
