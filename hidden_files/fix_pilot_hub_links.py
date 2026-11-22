"""One-off repair 2026-11-22: pilot hub links used the bare relative
'timeshare-exit/', which from states/<state>.html resolves to
/states/timeshare-exit/ and 404s. Rewrite all three hub references per
state to the absolute /states/<state>/timeshare-exit/ path, and make
404.html's asset paths root-relative (it can be served at any depth).
Also fixes the generator's source strings in build_pilot_timeshare_exit_split.py
— that file was edited separately; this script patches the live hub files.
Run from the site repo root. Idempotent: refuses to run twice.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATES = ROOT / "states"

slugs = sorted(p.stem for p in STATES.glob("*.html"))
assert len(slugs) == 50, f"expected 50 state hubs, got {len(slugs)}"

for slug in slugs:
    path = STATES / f"{slug}.html"
    text = path.read_text()
    abs_url = f"/states/{slug}/timeshare-exit/"
    # Preconditions: the broken relative forms are present exactly as built.
    assert text.count('href="timeshare-exit/"') == 2, f"{slug}: href count"
    assert text.count("'timeshare-exit/'") == 1, f"{slug}: catch dest count"
    assert abs_url not in text, f"{slug}: already patched?"
    text = text.replace('href="timeshare-exit/"', f'href="{abs_url}"')
    text = text.replace("'timeshare-exit/'", f"'{abs_url}'")
    assert 'href="timeshare-exit/"' not in text, f"{slug}: bare href left"
    assert "'timeshare-exit/'" not in text, f"{slug}: bare dest left"
    assert text.count(f'href="{abs_url}"') == 2, f"{slug}: abs href count"
    assert text.count(f"'{abs_url}'") == 1, f"{slug}: abs dest count"
    path.write_text(text)
    print(f"patched {slug}")

# 404.html: it can be served at any depth, so EVERY relative href/src
# (assets, nav links) must be root-relative, not just the assets.
p404 = ROOT / "404.html"
t = p404.read_text()
def _root_rel(m):
    attr, val = m.group(1), m.group(2)
    if val.startswith(("/", "#", "http:", "https:", "data:", "tel:", "mailto:")):
        return m.group(0)
    return f'{attr}="/{val}"'
t = re.sub(r'(href|src)="([^"]*)"', _root_rel, t)
left = re.findall(r'(?:href|src)="(?!/|#|https?:|data:|tel:|mailto:)([^"]*)"', t)
assert not left, f"404 still has relative refs: {left}"
p404.write_text(t)
print("patched 404.html refs to root-relative")
print(f"OK: {len(slugs)} hubs + 404.html")
