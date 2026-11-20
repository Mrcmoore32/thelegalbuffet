#!/usr/bin/env python3
"""Build Topic #90: Sexual Harassment at Work — standalone section on all
50 state pages.

Inserts one new section per state page (before What to Do If You're
Arrested, newest-first), a contents-list entry (before the arrested <li>), a
homepage helper option + topic card (after What to Do If You're Arrested),
bumps About 88 -> 89, and appends 50 state entries + 1 helper entry to
assets/search-index.json (10906 -> 10957).

Data: hidden_files/topic-research/sexual-harassment-at-work/all-states.json
(coordinator-built 2026-11-20 from 5 research batches; verification notes in
this docstring).

Coordinator verification before the build (Nov 20, 2026):
- Federal core vs official sources: Title VII of the Civil Rights Act of 1964
  covers employers with 15 or more employees; EEOC charge deadline 180 days,
  extended to 300 days where a state/local agency enforces a matching law;
  for ongoing harassment the clock runs from the last incident; EEOC phone
  1-800-669-4000 — all confirmed on eeoc.gov/time-limits-filing-charge,
  read Nov 20, 2026.
- URLs: all 90 non-null agency + legal-aid URLs curl-checked Nov 20. 3 real
  problems fixed: AZ agency https://azag.gov/civil-rights 404 ->
  https://www.azag.gov/civil-rights/faq (200, and it prints the Division's
  Phoenix phone (602) 542-5263); OH agency deep filing URL 404 ->
  https://civ.ohio.gov/ (alive in browser; prints OCRC toll-free
  1-888-278-7101); DE agency dia.delawareworks.com/discrimination/ 000 x2
  and unresolvable in the browser -> https://labor.delaware.gov/antidiscrimination
  (200; the URL the office's own intake form cites as its website). All other
  403/406/000s confirmed alive via live browser text fetch (AL/CA/CO/GA/ID/
  MA/ME/MS/NV/NH/NJ/UT/WY agency and legal-aid pages). TN agency
  tn.gov/humanrights.html curls 403 (bot filter pattern) and one browser
  fetch failed with a network error; kept as the official tn.gov URL.
- Phones: the dataset's 1-800-669-4000 on AL/AR/GA is the EEOC's own number
  (confirmed on eeoc.gov and in EEOC field-office listings), NOT the legal-aid
  orgs' number — replaced with each org's real number, second-sourced:
  AL Legal Services Alabama 1-866-456-4995 (legalservicesalabama.org +
  alabamalegalhelp.org); GA Georgia Legal Services Program 1-800-498-9469
  (glsp.org + georgialegalaid.org + CFPB); AR phone dropped to null (no
  second official source for Legal Aid of Arkansas's own number). CA
  800-884-1684 is the CRD contact center, not Legal Aid at Work's number
  (confirmed on calcivilrights.ca.gov) — labeled as the agency phone. OH
  1-888-278-7101 is OCRC's toll-free number (confirmed on civ.ohio.gov) —
  labeled as the agency phone. DE 302-761-8200 is the DE Office of
  Anti-Discrimination (confirmed in the office's own intake-form PDF on
  industrialaffairs.delaware.gov) — labeled as the agency phone. AZ
  (602) 542-5263 added (azag.gov FAQ + legal-aid page). NH (603) 271-2767
  added (humanrights.nh.gov + NH Admin Rules Hum 103.01). MA (617) 994-6000
  added (two mass.gov MCAD pages). NV (702) 486-7161 confirmed on
  detr.nv.gov. WY 877-432-9955 confirmed on lawyoming.org. All other printed
  phones verified against a second official source by the phone-verification
  pass (see verification log); any phone that failed that pass is null.
  The EEOC number 1-800-669-4000 is printed once in the federal intro.
- Structural notes in the data: 4 states have no state fair-employment agency
  for private-sector workers (AL, AR, MS, NC) — the section says so plainly
  and routes readers to the EEOC. GA's agency covers state-government
  employees only — the agency name carries that qualifier. 3 states have no
  verifiable agency URL (NM, OK, OR) and 3 have no verifiable legal-aid URL
  (MD, OK, WV) — name printed without a link, never a guessed URL.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "sexual-harassment-at-work" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-sexual-harassment-at-work.jpg"

SLUG = "sexual-harassment-at-work"
TITLE = "Sexual Harassment at Work"
PREV_SLUG = "what-to-do-if-youre-arrested"

NO_AGENCY_STATES = {"alabama", "arkansas", "mississippi", "north carolina"}


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="sexual-harassment-at-work-in-{slug}">Sexual harassment at work in {esc(state)}</h2>'
    )
    parts.append(
        "<p>Sexual harassment at work is illegal. Under federal law (Title VII of the "
        "Civil Rights Act of 1964), your employer may not allow sexual harassment "
        "that affects your job &mdash; and most states have their own law that covers "
        "smaller employers the federal law does not reach. You do not have to prove "
        "you were fired or demoted: harassment that creates a hostile work environment "
        "is enough. This section is the " + esc(state) + " picture as of "
        "<strong>November 2026</strong> &mdash; what counts, what to do right now, the "
        "deadlines, and where to file a complaint. This is general information, not "
        "legal advice. The deadlines are short, so <strong>do not wait</strong>: in "
        "most states you have months, not years, to file. If you are in immediate "
        "danger, call 911. To file a federal complaint, call the Equal Employment "
        "Opportunity Commission (EEOC) at <strong>1-800-669-4000</strong>.</p>"
    )
    # --- Card 1: what counts ---
    parts.append('<div class="card">')
    parts.append("<h3>What counts as sexual harassment</h3>")
    parts.append(
        "<p><strong>Quid pro quo</strong> (&ldquo;this for that&rdquo;): a boss or supervisor "
        "conditions a job benefit &mdash; a hire, a promotion, a raise, keeping your "
        "job &mdash; on sexual favors, or punishes you for refusing. One incident can "
        "be enough.</p>"
    )
    parts.append(
        "<p><strong>Hostile work environment:</strong> unwelcome sexual conduct so severe "
        "or repeated that it makes your workplace abusive &mdash; sexual comments or "
        "jokes, leering, unwanted touching, sexual pictures or messages, repeated "
        "unwanted invitations, or sexual rumors about you. It does not have to come "
        "from your boss: a coworker, a client, or a customer can create it, and your "
        "employer is responsible if it knew or should have known and did nothing.</p>"
    )
    parts.append(
        "<p>It counts even if the harasser is the same sex as you, even if it happens "
        "outside the office (a work trip, a work party, a text message after hours), "
        "and even if nobody else saw it. What matters is that the conduct was unwelcome "
        "and based on sex. A single very serious incident (like an assault) can qualify "
        "on its own; lesser conduct usually has to be repeated.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If it happened to you, the next card "
        "is your checklist. If you are not sure it &ldquo;counts,&rdquo; write down what "
        "happened anyway &mdash; investigators and lawyers decide that question, and "
        "they need the facts.</p>"
    )
    parts.append("</div>")
    # --- Card 2: what to do right now ---
    parts.append('<div class="card">')
    parts.append("<h3>What to do right now</h3>")
    parts.append(
        "<p><strong>Write it down, today.</strong> For each incident: the date, time, "
        "place, exactly what was said or done, who was there, and how it affected your "
        "work. Keep adding to the list. Memory fades; a written log is evidence.</p>"
    )
    parts.append(
        "<p><strong>Save everything.</strong> Texts, emails, messages, photos, schedules, "
        "performance reviews, pay stubs. Screenshot messages before they can be "
        "deleted, and keep copies outside of work &mdash; not only on a work computer "
        "or phone you could lose access to.</p>"
    )
    parts.append(
        "<p><strong>Tell the harasser to stop, if you safely can.</strong> A clear "
        "&ldquo;stop, that is not okay&rdquo; helps show the conduct was unwelcome. If "
        "saying it in person is unsafe or could cost you your job, skip this step "
        "&mdash; it is not required.</p>"
    )
    parts.append(
        "<p><strong>Report it in writing.</strong> Tell your supervisor, HR, or whoever "
        "your employer&rsquo;s policy names &mdash; in writing (email counts), keeping a "
        "copy for yourself. Say what happened, when, and what you want: for it to stop. "
        "If the harasser <em>is</em> your supervisor, report to HR or to their boss. "
        "Your employer&rsquo;s duty to act usually starts when it knows.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Start the written log today, save "
        "copies off your work devices, and put the complaint in writing. Then watch "
        "the deadlines in the next card &mdash; reporting to your employer does not "
        "pause the filing clock.</p>"
    )
    parts.append("</div>")
    # --- Card 3: deadlines ---
    parts.append('<div class="card">')
    parts.append("<h3>The deadlines: the clock is short</h3>")
    parts.append(
        "<p>Federal law gives you <strong>180 days</strong> from the harassment to file "
        "a charge with the EEOC &mdash; <strong>300 days</strong> if your state has its "
        "own fair-employment agency. For ongoing harassment, the clock runs from the "
        "<em>last</em> incident, but earlier incidents still count as evidence. State "
        "deadlines are all over the map: some are 180 days, some are a year, a few "
        "are two or three years. Your state&rsquo;s deadline is in the state card below.</p>"
    )
    parts.append(
        "<p>Two traps: <strong>(1)</strong> trying to resolve it inside the company does "
        "not pause the clock &mdash; the EEOC says so plainly. <strong>(2)</strong> The "
        "state deadline and the federal deadline are different clocks. File with "
        "whichever agency has the shorter deadline first, and ask about dual-filing "
        "&mdash; in many states one filing counts for both.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Find your state&rsquo;s deadline in "
        "the card below, and file well before it. If you are anywhere near the limit, "
        "call the agency or the EEOC (1-800-669-4000) today and ask how much time you "
        "have left.</p>"
    )
    parts.append("</div>")
    # --- Card 4: how to file ---
    parts.append('<div class="card">')
    parts.append("<h3>How to file a complaint</h3>")
    parts.append(
        "<p><strong>Step 1: pick the agency.</strong> If your state has a fair-employment "
        "agency (most do &mdash; see the state card below), file there; it usually "
        "dual-files with the EEOC, so one filing protects both claims. If your state "
        "has no agency, or your employer is big enough for federal law (15 or more "
        "employees), file with the EEOC directly &mdash; online, by phone at "
        "1-800-669-4000, or at a field office.</p>"
    )
    parts.append(
        "<p><strong>Step 2: the charge.</strong> You describe what happened, when, and "
        "who did it. The agency may interview you, ask for your log and saved messages, "
        "and contact your employer. Filing is free, and you do not need a lawyer to file.</p>"
    )
    parts.append(
        "<p><strong>Step 3: investigation, then a decision.</strong> The agency investigates "
        "and either finds cause (and tries to settle it or sues on your behalf) or closes "
        "the case. If it closes, you get a &ldquo;right-to-sue&rdquo; letter &mdash; usually "
        "90 days from that letter to file a lawsuit in court. You can also ask for a "
        "right-to-sue letter earlier in many states.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> File with the agency in the state card "
        "below (or the EEOC if there is none). Bring your written log and your saved "
        "messages. Do not sign anything from your employer about the harassment "
        "without reading the next card first.</p>"
    )
    parts.append("</div>")
    # --- Card 5: retaliation ---
    parts.append('<div class="card">')
    parts.append("<h3>Retaliation is illegal too</h3>")
    parts.append(
        "<p>It is illegal for your employer to punish you for complaining about "
        "harassment, filing a charge, or helping a coworker&rsquo;s complaint &mdash; "
        "firing you, demoting you, cutting your hours, giving you worse shifts, or "
        "suddenly writing you up. This is called <strong>retaliation</strong>, and it "
        "is a separate violation even if the harassment claim itself is hard to prove.</p>"
    )
    parts.append(
        "<p>Write down any change in how you are treated after you complain, with dates. "
        "If you are fired or punished after complaining, tell the agency right away "
        "&mdash; a retaliation claim has its own deadline, and it usually starts on the "
        "day of the retaliatory act.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Keep logging. If anything about your "
        "job gets worse after you report, that goes in the log too, and you tell the "
        "agency.</p>"
    )
    parts.append("</div>")
    # --- Card 6: what NOT to do ---
    parts.append('<div class="card">')
    parts.append("<h3>What NOT to do</h3>")
    parts.append(
        "<p><strong>Do not delete evidence.</strong> Do not delete texts, emails, or "
        "photos, and do not &ldquo;clean up&rdquo; your side of a message thread.</p>"
    )
    parts.append(
        "<p><strong>Do not sign a severance, settlement, or release without reading it "
        "closely.</strong> These papers often include a clause giving up your right to "
        "sue or to talk about what happened. Ask a lawyer or a legal-aid office to read "
        "it first &mdash; many will do that for free.</p>"
    )
    parts.append(
        "<p><strong>Do not wait out the deadline.</strong> Hoping HR fixes it, waiting "
        "for a transfer, or waiting until you find a new job can all run out the "
        "filing clock. You can keep working with HR <em>and</em> file on time.</p>"
    )
    parts.append(
        "<p><strong>Do not quit in anger without a plan, if you can avoid it.</strong> "
        "Quitting can make a claim harder (and can affect unemployment benefits), "
        "though staying in an abusive workplace is not required either. If you are "
        "thinking of quitting, talk to a lawyer or legal aid first &mdash; it is a "
        "free call in most states.</p>"
    )
    parts.append(
        "<p><strong>Do not confront the harasser alone if it feels unsafe.</strong> Report "
        "through HR, the agency, or the police if there was an assault. Your safety "
        "comes before any procedure.</p>"
    )
    parts.append("</div>")
    # --- Card 7: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Where to file in {esc(state)}</h3>")
    if e["agency_name"]:
        if e["agency_url"]:
            parts.append(
                f"<p><strong>State agency:</strong> "
                f'<a href="{esc(e["agency_url"])}" target="_blank" rel="noopener">{esc(e["agency_name"])}</a>.</p>'
            )
        else:
            parts.append(
                f"<p><strong>State agency:</strong> {esc(e['agency_name'])} &mdash; no "
                "agency complaint-page link could be verified; search the agency name "
                "or call the EEOC at 1-800-669-4000 to be pointed to the right place.</p>"
            )
    else:
        parts.append(
            f"<p><strong>State agency:</strong> {esc(state)} has no state "
            "fair-employment agency that takes private-sector sexual-harassment "
            "complaints. Your route is the federal EEOC &mdash; call "
            "<strong>1-800-669-4000</strong>.</p>"
        )
    if e["statute_name"]:
        cite = f" ({esc(e['statute_cite'])})" if e["statute_cite"] else ""
        parts.append(f"<p><strong>The law:</strong> {esc(e['statute_name'])}{cite}.</p>")
    if e["deadline_note"]:
        parts.append(f"<p><strong>Deadline in {esc(state)}:</strong> {esc(e['deadline_note'])}</p>")
    if e["state_note"]:
        parts.append(f"<p>{esc(e['state_note'])}</p>")
    if e["phone"]:
        parts.append(
            f"<p><strong>{esc(e['phone_label'])} phone:</strong> {esc(e['phone'])}.</p>"
        )
    if e["legal_aid_url"]:
        parts.append(
            f"<p><strong>Free legal help:</strong> "
            f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
        )
    else:
        parts.append(
            f"<p><strong>Free legal help:</strong> {esc(e['legal_aid_name'])} &mdash; no "
            "website link could be verified; search the name to find their intake line.</p>"
        )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Start your written log today, "
        "report the harassment in writing at work, and file with the agency above "
        "(or the EEOC at 1-800-669-4000) well before the deadline. Bring your log "
        "and your saved messages.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Start a written log today: dates, "
        "exact words, witnesses. (2) Save texts, emails, and photos off your work "
        "devices. (3) Report it in writing at work and keep a copy. (4) File with "
        "your state agency &mdash; or the EEOC at 1-800-669-4000 &mdash; well before "
        "the deadline in the card above. (5) If you are punished for complaining, "
        "log that too and tell the agency. (6) Do not sign a release or severance "
        "without a free legal-aid review first.</p>"
    )
    parts.append(
        "<p><em>Sources: U.S. Equal Employment Opportunity Commission (Title VII; time "
        "limits for filing a charge; 1-800-669-4000), and the official " + esc(state) +
        " agency, statute, and legal-aid sources linked above, checked November 20, "
        "2026. Deadlines and agency procedures change &mdash; confirm the current "
        "deadline with the agency before you file. This is general information, not "
        "legal advice.</em></p>"
    )
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def build_state_pages(data):
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        path = STATES / f"{slug}.html"
        text = path.read_text()
        anchor = f"{SLUG}-in-{slug}"
        assert anchor not in text, f"{slug}: anchor already present"
        # --- insert section before What to Do If You're Arrested ---
        h2 = text.find(f'<h2 id="{PREV_SLUG}-in-{slug}">')
        assert h2 != -1, f"{slug}: {PREV_SLUG} h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        before = text
        new_section = section_html(state, slug, e)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the arrested <li> ---
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#' + re.escape(PREV_SLUG) + r'-in-'
            + re.escape(slug)
            + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: {PREV_SLUG} contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#{SLUG}-in-{slug}">'
            f"Sexual harassment at work in {state}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        # --- structural assertions ---
        assert text.count(f'id="{SLUG}-in-{slug}"') == 1, f"{slug}: anchor count"
        assert text.count("<div") - before.count("<div") == 7, f"{slug}: div open delta"
        assert text.count("</div>") - before.count("</div>") == 7, f"{slug}: div close delta"
        assert text.count("<div") == text.count("</div>"), f"{slug}: div imbalance"
        h2s = re.findall(r'<h2 id="([^"]+)">', text)
        assert h2s.index(f"{SLUG}-in-{slug}") == h2s.index(f"{PREV_SLUG}-in-{slug}") - 1, f"{slug}: h2 order"
        assert "None" not in new_section, f"{slug}: leaked None in new section"
        assert "TODO" not in new_section and "FIXME" not in new_section, f"{slug}: leaked marker"
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert SLUG not in helper_part, "index already has helper option"
    assert f'data-topic="{SLUG}"' not in text, "index already has card"
    opt_old = (
        '<option value="what-to-do-if-youre-arrested" data-anchor="what-to-do-if-youre-arrested">'
        "What to do if you&rsquo;re arrested (stay silent, ask for a lawyer, bail, arraignment, diversion, public defender)</option>"
    )
    assert opt_old in text, "arrested helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="sexual-harassment-at-work" data-anchor="sexual-harassment-at-work">'
        "Sexual harassment at work (what counts, what to do, deadlines, filing a complaint, retaliation)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="what-to-do-if-youre-arrested"'
    idx = text.find(card_anchor)
    assert idx != -1, "arrested card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="sexual-harassment-at-work">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-sexual-harassment-at-work.jpg" alt="Sexual harassment at work" loading="lazy"></span>
          <h3>Sexual Harassment at Work</h3>
          <p>What counts as harassment, what to do right now, the filing deadlines, and where to complain in your state. Quid pro quo, hostile work environment, and retaliation.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 43 topics" in text, "show-all label not found"
    text = text.replace("Show all 43 topics", "Show all 44 topics", 1)
    # Two badges: hero grid reads "42 topics", main grid reads "43 topics". The
    # main-grid badge is the one AFTER the show-label line; the hero badge
    # stays untouched (badge-collision lesson from #89).
    show_pos = text.find("Show all 44 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">43 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("43 topics", "44 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 43->44")


def build_about():
    text = ABOUT.read_text()
    assert text.count("88 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("88 legal topics", "89 legal topics", 1))
    print("  about.html: 88 -> 89")


def state_index_t(state, slug, e):
    bits = [
        "sexual-harassment-at-work sexual harassment at work quid pro quo hostile work environment",
        f"Sexual harassment at work in {state}",
        "quid pro quo hostile work environment unwelcome sexual conduct",
        "what to do write it down save texts emails report in writing HR",
        "deadline EEOC 180 days 300 days file a charge dual filing",
        "how to file a complaint state agency EEOC right to sue",
        "retaliation illegal fired demoted hours cut after complaining",
        "what not to do delete evidence sign severance release wait out deadline quit",
        f"{e['agency_name'] or ''}",
        f"{e['statute_name'] or ''} {e['statute_cite'] or ''}",
        f"deadline in {state}: {e['deadline_note']}",
        f"{e['state_note'] or ''}",
        f"{e['legal_aid_name']}",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 10906, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Sexual harassment at work in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Sexual Harassment at Work",
            "t": (
                "sexual-harassment-at-work sexual harassment at work quid pro quo "
                "hostile work environment Sexual harassment at work? What counts as "
                "harassment, what to do right now, the filing deadlines, and where to "
                "complain in your state. EEOC 1-800-669-4000 180 days 300 days file a "
                "charge dual filing retaliation illegal write it down save evidence "
                "report in writing do not sign severance release."
            ),
        }
    )
    assert len(idx) == 10957, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 10906 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [(k, states[k]) for k in sorted(states)]
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "agency_name", "agency_url", "statute_name", "statute_cite",
        "deadline_note", "legal_aid_name", "legal_aid_url", "phone",
        "phone_label", "state_note", "sources",
    ]
    phone_re = re.compile(
        r"\(\d{3}\)\s*\d{3}[-.]\d{4}|\b\d{3}[-.]\d{3}[-.]\d{4}\b|"
        r"1-800-\d{3}-\d{4}|1-866-\d{3}-\d{4}|1-888-\d{3}-\d{4}|"
        r"877-\d{3}-\d{4}|800-\d{3}-\d{4}|844-\d{3}-\d{4}|866-\d{3}-\d{4}|"
        r"1-877-\d{3}-\d{4}|1-833-[A-Z0-9]{7}"
    )
    for k, e in data:
        for f in req:
            assert f in e, f"{k}: missing {f}"
        assert e["deadline_note"] and e["legal_aid_name"] and e["sources"], f"{k}: empty required field"
        assert (e["agency_name"] is None) == (k in NO_AGENCY_STATES), f"{k}: agency null mismatch"
        # phones appear only in the phone field (plus the federal EEOC number in the template)
        blob = json.dumps({f: e[f] for f in req if f not in ("phone", "phone_label")})
        assert not phone_re.search(blob), f"{k}: phone-like string outside phone field"
        if e["phone"]:
            assert phone_re.search(e["phone"]), f"{k}: phone format {e['phone']!r}"
            assert e["phone_label"] in ("State agency", "Legal aid"), f"{k}: bad phone_label"
        else:
            assert e["phone_label"] is None, f"{k}: phone_label without phone"
    print("building state pages (insert before arrested section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
