#!/usr/bin/env python3
"""Eviction-timeline strip generator (Phase B B2-3).

One reusable component: for every state page, reads the ALREADY VERIFIED
"Notice before eviction" card text from that page's own Tenant Rights
section and reuses it verbatim as step 1 of a 4-step visual strip
(notice -> court filing -> hearing -> lockout), inserted inside the
Tenant Rights section just before its "What to do next" block.

No day count is ever invented: steps 2-4 are generic process steps with
no state-specific numbers (step 4 restates the page's own line that
only a court can order an eviction), and step 1 is the page's own
verified wording — including for states whose wording states there is
no statutory notice period or no cure period, where the strip shows
that wording as-is plus the "confirm with your local court" caveat.

Idempotent: pages that already contain an evict-timeline block are
left untouched.
"""
import glob
import html
import re

MARKER = "evict-timeline"
TIMELINE_CSS = """
/* Eviction timeline strip (added 2026-10-29, Phase B B2-3). */
.evict-timeline { margin: 1.5rem 0; background: var(--gold-soft); border: 1px solid var(--gold); border-radius: var(--radius-sm); padding: 1.1rem 1.25rem; }
.evict-timeline h3 { margin: 0 0 .8rem; }
.evict-steps { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(4, 1fr); gap: .75rem; }
.evict-steps li { background: var(--card); border-radius: 12px; padding: .8rem; box-shadow: var(--shadow); }
.evict-steps li strong { display: block; color: var(--ink); margin-bottom: .25rem; }
.evict-steps li span { color: var(--ink-soft); font-size: .92rem; }
.evict-note { margin: .9rem 0 0; font-size: .9rem; color: var(--muted); }
@media (max-width: 700px) { .evict-steps { grid-template-columns: 1fr; } }
"""


def strip_html(text):
    return html.unescape(re.sub(r"<[^>]+>", "", text)).strip()


def build_strip(state, notice_text):
    notice = html.escape(notice_text)
    return (
        f'<div class="evict-timeline">\n'
        f'  <h3>How an eviction usually moves, step by step, in {html.escape(state)}</h3>\n'
        f'  <ol class="evict-steps">\n'
        f'    <li><strong>1. Notice</strong><span>{notice}</span></li>\n'
        f'    <li><strong>2. Court filing</strong><span>If the problem is not fixed, '
        f'the landlord files an eviction case in court.</span></li>\n'
        f'    <li><strong>3. Hearing</strong><span>A hearing is held in court. '
        f'Go to it, and bring your lease, notices, and payment records.</span></li>\n'
        f'    <li><strong>4. Lockout — only after a court order</strong><span>Only a '
        f'court can order an eviction. A lockout happens only after a court '
        f'order, not on the landlord&rsquo;s say-so alone.</span></li>\n'
        f'  </ol>\n'
        f'  <p class="evict-note">Steps and deadlines vary by case and by city. '
        f'Confirm the exact deadlines with your local court. This is general '
        f'information, not legal advice.</p>\n'
        f'</div>\n'
    )


def build_timeline():
    changed, skipped = [], []
    for path in sorted(glob.glob("states/*.html")):
        txt = open(path).read()
        if MARKER in txt:
            skipped.append(path)
            continue
        h2 = re.search(r'<h2 id="tenant-rights-in-[^"]+">Tenant rights in ([^<]+)</h2>', txt)
        notice = re.search(r"<h3>Notice before eviction</h3>\s*<p>(.*?)</p>", txt, re.S)
        if not h2 or not notice:
            print(f"  SKIP (no tenant notice card): {path}")
            skipped.append(path)
            continue
        state = h2.group(1).strip()
        # Tenant section slice, so the anchor is that section's own
        # "What to do next" block, not a later section's.
        sec_end = txt.find("</section>", h2.start())
        seg = txt[h2.start():sec_end]
        anchor = seg.find('<div class="next-steps">')
        if anchor < 0 or "What to do next" not in seg[anchor:anchor + 200]:
            print(f"  SKIP (anchor not found): {path}")
            skipped.append(path)
            continue
        insert_at = h2.start() + anchor
        strip = build_strip(state, strip_html(notice.group(1)))
        txt = txt[:insert_at] + strip + txt[insert_at:]
        open(path, "w").write(txt)
        changed.append((path, state, strip_html(notice.group(1))))
    print(f"Timeline: added to {len(changed)} state pages, skipped {len(skipped)}")
    for path, state, notice in changed:
        print(f"  {path}: {state} — notice: {notice}")
    return changed


if __name__ == "__main__":
    build_timeline()
