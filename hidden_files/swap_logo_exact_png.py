#!/usr/bin/env python3
"""Swap the header logo from the inline stacked SVG to Craig's exact
transparent PNG (assets/img/tlb-monogram.png, 256px) on all 61 site pages.
Root pages use assets/... paths; states/*.html use ../assets/... paths.
Run from the site repo root, on branch update/header-logo-exact-png.
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

files = [f for f in sorted(ROOT.glob("*.html")) + sorted((ROOT / "states").glob("*.html"))
         if f.name != "google729d80b11a08f672.html"]  # Search Console file: no header, never touch
changed, skipped = [], []
for f in files:
    text = f.read_text()
    matches = OLD_RE.findall(text)
    if len(matches) != 1:
        skipped.append((str(f.relative_to(ROOT)), len(matches)))
        continue
    prefix = "../" if f.parent.name == "states" else ""
    new = (
        f'<span class="brand-mark"><img src="{prefix}assets/img/tlb-monogram.png" '
        f'width="46" height="46" alt=""></span>'
    )
    f.write_text(OLD_RE.sub(lambda _: new, text, count=1))
    changed.append(str(f.relative_to(ROOT)))

print(f"changed: {len(changed)}")
if skipped:
    print("SKIPPED (not exactly 1 match):", skipped)
    sys.exit(1)
