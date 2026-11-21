#!/usr/bin/env python3
"""Swap the inline header monogram from side-by-side T/L/B to the stacked
(interlocked) arrangement on all 61 site pages, and update tlb-monogram.svg
to match. Run from the site repo root, on branch update/official-logo-stacked.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_RE = re.compile(
    r'<span class="brand-mark"><svg viewBox="0 0 240 240" width="46" height="46" '
    r'aria-hidden="true">.*?</svg></span>',
    re.DOTALL,
)
NEW_INNER = (
    '<span class="brand-mark"><svg viewBox="0 0 240 240" width="46" height="46" '
    'aria-hidden="true"> <circle cx="120" cy="120" r="116" fill="#102744"/>'
    '<circle cx="120" cy="120" r="107" fill="none" stroke="url(#tlbGold)" stroke-width="8"/>'
    '<defs><linearGradient id="tlbGold" gradientUnits="userSpaceOnUse" x1="120" y1="30" '
    'x2="120" y2="210"><stop offset="0" stop-color="#F6E2A0"/>'
    '<stop offset="0.45" stop-color="#D9B45C"/><stop offset="0.75" stop-color="#B58A43"/>'
    '<stop offset="1" stop-color="#8A6526"/></linearGradient></defs>'
    '<text x="120" y="128" text-anchor="middle" font-family="\'Cormorant Garamond\',Georgia,serif" '
    'font-size="125" font-weight="700" fill="url(#tlbGold)">T</text>'
    '<text x="84" y="205" text-anchor="middle" font-family="\'Cormorant Garamond\',Georgia,serif" '
    'font-size="125" font-weight="700" fill="url(#tlbGold)">L</text>'
    '<text x="150" y="205" text-anchor="middle" font-family="\'Cormorant Garamond\',Georgia,serif" '
    'font-size="125" font-weight="700" fill="url(#tlbGold)">B</text> </svg></span>'
)

files = [f for f in sorted(ROOT.glob("*.html")) + sorted((ROOT / "states").glob("*.html"))
         if f.name != "google729d80b11a08f672.html"]  # Search Console verification file: no header, never touch
changed, skipped = [], []
for f in files:
    text = f.read_text()
    matches = OLD_RE.findall(text)
    if len(matches) != 1:
        skipped.append((str(f.relative_to(ROOT)), len(matches)))
        continue
    f.write_text(OLD_RE.sub(lambda _: NEW_INNER, text, count=1))
    changed.append(str(f.relative_to(ROOT)))

print(f"changed: {len(changed)}")
if skipped:
    print("SKIPPED (not exactly 1 match):", skipped)
    sys.exit(1)

# tlb-monogram.svg: replace with the stacked version (same content as the draft)
draft = ROOT / "assets/img/tlb-monogram-stacked-draft.svg"
(ROOT / "assets/img/tlb-monogram.svg").write_text(draft.read_text())
draft.unlink()
print("tlb-monogram.svg updated from draft; draft removed")
