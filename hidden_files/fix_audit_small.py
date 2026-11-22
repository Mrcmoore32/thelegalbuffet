#!/usr/bin/env python3
"""Fix small verified audit items (branch fix/audit-small-fixes).

(a) MN fee-waiver statute link 2015 -> current.
(b) MN DNR TIP link contact page -> enforcement/tip.html (single occurrence).
(c) Homepage '65 topics' -> '110 topics' (2 spots).
(d) Homepage URLs: href="index.html" -> href="/" (root), href="../index.html"
    -> href="../" (states), href="index.html#helper" -> href="/#helper"
    (start-here), sitemap homepage loc.
(e) All 50 state pages: og:title aligned to each page's own <title>.
(f) Homepage topic cards: descriptive go-span text from each card's h3.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)
    return cond


# ---------- (a) ----------
mn = ROOT / "states" / "minnesota.html"
text = mn.read_text()
old_a = "https://www.revisor.mn.gov/statutes/2015/cite/563/full"
new_a = "https://www.revisor.mn.gov/statutes/cite/563.01"
check(text.count(old_a) == 1, f"(a) expected 1 occurrence of 2015 revisor URL, got {text.count(old_a)}")
text = text.replace(old_a, new_a)
check("revisor.mn.gov/statutes/2015" not in text, "(a) 2015 revisor URL still present in MN file")
mn.write_text(text)

# ---------- (b) ----------
text = mn.read_text()
old_b = "https://www.dnr.state.mn.us/contact/index.html"
new_b = "https://www.dnr.state.mn.us/enforcement/tip.html"
check(text.count(old_b) == 1, f"(b) expected 1 occurrence of DNR contact URL, got {text.count(old_b)}")
# Scope check: the occurrence must sit inside the TIP section
tip_h = text.find("Minnesota DNR — Turn In Poachers (TIP)")
url_pos = text.find(old_b)
sec_end = text.find("</section>", tip_h)
check(tip_h != -1 and tip_h < url_pos < sec_end, "(b) DNR URL not inside the TIP section")
text = text.replace(old_b, new_b)
mn.write_text(text)

# ---------- (c) ----------
idx = ROOT / "index.html"
text = idx.read_text()
check(text.count("Show all 65 topics") == 1, "(c) 'Show all 65 topics' count != 1")
check(text.count('<span class="count-badge">65 topics</span>') == 1, "(c) count-badge 65 count != 1")
text = text.replace("Show all 65 topics", "Show all 110 topics")
text = text.replace('<span class="count-badge">65 topics</span>', '<span class="count-badge">110 topics</span>')
idx.write_text(text)

# ---------- (d) ----------
root_count = 0
for f in sorted(ROOT.glob("*.html")):
    if f.name == "google729d80b11a08f672.html":
        continue
    t = f.read_text()
    n = t.count('href="index.html"')
    if n:
        t = t.replace('href="index.html"', 'href="/"')
        root_count += n
    if f.name == "start-here.html":
        n2 = t.count('href="index.html#helper"')
        check(n2 == 1, f"(d) start-here #helper link count != 1 (got {n2})")
        t = t.replace('href="index.html#helper"', 'href="/#helper"')
    f.write_text(t)
check(root_count == 43, f"(d) root href=index.html replacements {root_count} != 43")

state_count = 0
for f in sorted((ROOT / "states").glob("*.html")):
    t = f.read_text()
    n = t.count('href="../index.html"')
    if n:
        t = t.replace('href="../index.html"', 'href="../"')
        state_count += n
        f.write_text(t)
check(state_count == 200, f"(d) state href=../index.html replacements {state_count} != 200")

sm = ROOT / "sitemap.xml"
t = sm.read_text()
check(t.count("https://thelegalbuffet.com/index.html") == 1, "(d) sitemap homepage loc count != 1")
t = t.replace("https://thelegalbuffet.com/index.html", "https://thelegalbuffet.com/")
sm.write_text(t)

# ---------- (e) ----------
fixed_e = 0
for f in sorted((ROOT / "states").glob("*.html")):
    t = f.read_text()
    m_title = re.search(r"<title>([^<]*)</title>", t)
    m_og = re.search(r'property="og:title" content="([^"]*)"', t)
    check(m_title is not None, f"(e) no <title> in {f.name}")
    check(m_og is not None, f"(e) no og:title in {f.name}")
    if not m_title or not m_og:
        continue
    title_raw = m_title.group(1)  # preserve &mdash; / literal dash as written
    if m_og.group(1) != title_raw:
        t = t.replace(
            f'property="og:title" content="{m_og.group(1)}"',
            f'property="og:title" content="{title_raw}"',
            1,
        )
        f.write_text(t)
        fixed_e += 1
print(f"(e) og:title aligned on {fixed_e} state pages")

# ---------- (f) ----------
t = idx.read_text()
counts = {"Explore": 0, "Learn more": 0, "Read it": 0, "Get prepared": 0}


def fix_card(m):
    block = m.group(0)
    h3 = re.search(r"<h3>([^<]*)</h3>", block)
    go = re.search(r'<span class="go">([^<]*)</span>', block)
    if not h3 or not go:
        errors.append("(f) card missing h3 or go span")
        return block
    title = h3.group(1)  # raw inner HTML (entities preserved)
    old = go.group(1)
    if old == "Explore &rarr;":
        new = f"Explore {title} &rarr;"
        counts["Explore"] += 1
    elif old == "Learn more &rarr;":
        new = f"Learn more about {title} &rarr;"
        counts["Learn more"] += 1
    elif old == "Read it &rarr;":
        new = f"Read {title} &rarr;"
        counts["Read it"] += 1
    elif old == "Get prepared &rarr;":
        new = f"Get prepared with {title} &rarr;"
        counts["Get prepared"] += 1
    else:
        errors.append(f"(f) unexpected go text: {old!r}")
        return block
    return block.replace(f'<span class="go">{old}</span>', f'<span class="go">{new}</span>')


t = re.sub(r'<a class="topic-card"[^>]*>.*?</a>', fix_card, t, flags=re.DOTALL)
idx.write_text(t)
print(f"(f) card spans fixed: {counts}")
check(counts == {"Explore": 60, "Learn more": 48, "Read it": 1, "Get prepared": 1},
      f"(f) unexpected span counts {counts}")
for bare in ("Explore &rarr;", "Learn more &rarr;", "Read it &rarr;", "Get prepared &rarr;"):
    check(f'<span class="go">{bare}</span>' not in t, f"(f) bare span remains: {bare}")

if errors:
    print("ERRORS:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("All fixes applied, all assertions passed.")
