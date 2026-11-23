#!/usr/bin/env python3
"""Build Topic #112: Protecting Kids Online — standalone section on
all 50 state pages.

Inserts one new section per state page (before Gender Marker Changes,
newest-first), a contents-list entry (before the gender-marker-changes
<li>), a homepage helper option + topic card (after Gender Marker
Changes), bumps About 110 -> 111, and appends 50 state entries + 1
helper entry to assets/search-index.json (12028 -> 12079).

Data: hidden_files/topic-research/protecting-kids-online/all-states.json
(coordinator-merged 2026-11-23 from 5 research batches; see
merge_all_states.py for the fixes applied at merge).

Helper decision: the existing "child-safety" option ("Child safety &
abuse reporting", aliased to the footer National-resources anchor) is
LEFT AS-IS — it covers abuse reporting broadly (incl. the Childhelp
hotline), not just online safety. A separate "protecting-kids-online"
option is added for the new section.

Spot verifications 2026-11-23 (second sources, all confirmed unless noted):
- NCMEC CyberTipline report.cybertip.org / 1-800-843-5678 (1-800-THE-LOST),
  24/7; Take It Down takeitdown.ncmec.org (free, under-18 images, launched
  Dec 2022); TAKE IT DOWN Act, Pub. L. 119-12 (S.146), signed May 19, 2025
  — covered platforms must remove flagged intimate images within 48 hours.
- FBI sextortion guidance (tips.fbi.gov, 1-800-CALL-FBI): don't pay, block,
  save evidence; victims typically males 14-17; Oct 2021-Mar 2023: 13,000+
  reports, 12,600+ victims, at least 20 suicides.
- COPPA: under 13, verifiable parental consent, 15 U.S.C. 6501-6506, FTC.
- Apple Screen Time (Family Sharing) and Google Family Link as the
  device-matched parental controls.
- CA CAADCA: Mar 12, 2026 Ninth Circuit NARROWED the injunction (coverage
  definition + age estimation may be enforced; data-use restrictions and
  the dark-patterns ban remain blocked). Researcher text was wrong; fixed.
- FL HB 3: Eleventh Circuit Oct 14, 2026 reversed the preliminary
  injunction; in effect. MS HB 1126: Fifth Circuit Nov 19, 2026 vacated
  the preliminary injunction; in effect since July 1, 2024.
- TN Act: in effect Jan 1, 2025; Sixth Circuit Aug 28, 2026 vacated the
  denial of a preliminary injunction and remanded; no injunction in place.
- TX SCOPE: Fifth Circuit granted rehearing en banc Oct 28, 2026, vacating
  the July 24, 2026 panel opinion; district-court preliminary injunction
  on the content-monitoring/filtering duty stands pending en banc.
- UT SB 194: preliminary injunction Sept 10, 2024 (NetChoice v. Reyes);
  enforcement remains blocked. (Unverified "10th Circuit" claim removed.)
- NE LB 383: preliminary injunction June 27, 2026 (NetChoice v. Hilgers)
  on age-verification + parental-consent provisions; dashboard survives;
  AG appealed to the 8th Circuit.
- AR Act 689: permanently enjoined Mar 31, 2025 (NetChoice v. Griffin);
  state appealed to the 8th Circuit; follow-up Acts 900/901 of 2025 both
  preliminarily enjoined in 2026.
- GA SB 351: Eleventh Circuit vacated the preliminary injunction
  Oct 15, 2026; in effect; litigation continues.
- IL HB 5511 / Public Act 104-0664: signed July 31, 2026; effective
  Jan 1, 2028 (not yet in effect).
- AL HB 161 (Act 2026-59): signed Feb 17, 2026; effective Jan 1, 2027;
  CCIA sued Oct 28, 2026; no blocking order yet.
- IN SEA 17: in effect since July 1, 2024 (2024 preliminary injunction
  vacated on appeal; SCOTUS upheld Texas's similar law in Free Speech
  Coalition v. Paxton, June 2025). HEA 1408 (2026) adds social-media
  age-verification/parental-consent rules (Ind. Code 24-16, eff. Jan 1,
  2027); NetChoice sued Nov 18, 2026; no ruling yet.
- MD Kids Code: in effect Oct 1, 2024; NOT enjoined; NetChoice v. Brown
  pending (motion to dismiss denied Nov 24, 2025).
- MN HF 4138 (Stop Harms from Addictive Social Media Act), Chapter 111,
  2026: effective July 1, 2027; child = 15 or younger.
- NJ Kids Code Act (A4015/S3413): signed Aug 11, 2026; effective
  Sept 1, 2027.
- NY SAFE for Kids Act (S7694A, signed June 20, 2024): final AG rules
  July 28, 2026; takes effect Jan 25, 2027; penalties up to $5,000/violation.
- OH ORC 1349.09: permanently enjoined Apr 16, 2025; Sixth Circuit
  reversed June 18, 2026 (NetChoice v. Yost); mandate stayed Aug 17, 2026
  pending SCOTUS petition (due Dec 3, 2026); NOT in force.
- SC H 3431 (Act No. 96 of 2026): signed Feb 5, 2026, effective
  immediately; S.C. Code Title 39, Chapter 80; annual independent audits.
- ID HB 498, IA HF 864 (ch. 554J, approved June 1, 2026), KS SB 394,
  KY HB 278, LA Act 440 (eff. Jan 1, 2023), MT SB 544 (eff. Jan 1, 2024;
  private lawsuits only since Apr 17, 2025): all confirmed in force.
- UT sexting renumbering (76-10-1206 -> 76-5c-205, May 2025
  recodification) confirmed on the official Utah legislature site.
- ME State Police Major Crimes Unit - Special Victims: the unit "does
  not take direct reports from the public" — report to local law
  enforcement (confirmed live on maine.gov). Maine card says so plainly.
- CO ICAC URL upgraded http -> https (https returns 200).
- KY legal aid (Legal Aid of the Bluegrass) serves 33 counties in
  northern, central, and northeastern Kentucky; LA legal aid (Southeast
  Louisiana Legal Services) serves 22 parishes in southeast Louisiana —
  both noted in the state card.

Claim-free fields (gap rule — line omitted, field never removed):
age_design empty in 26 states; sexting empty in HI/ME/MS; grooming
empty in WY; report_name/report_url empty in NV/NH (shared NCMEC
CyberTipline covers reporting there).

No phone numbers in the state dataset. The two national numbers in the
shared template below (NCMEC 1-800-843-5678, FBI 1-800-CALL-FBI) were
verified against official sources (see above).
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "protecting-kids-online" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-protecting-kids-online.jpg"

SLUG = "protecting-kids-online"
TITLE = "Protecting Kids Online"
PREV_SLUG = "gender-marker-changes"

# States whose legal-aid listing is regional-only (verified, see header).
LEGAL_AID_NOTE = {
    "kentucky": " (serves 33 counties in northern, central, and northeastern Kentucky)",
    "louisiana": " (serves 22 parishes in southeast Louisiana)",
}


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="protecting-kids-online-in-{slug}">Protecting kids online in {esc(state)}</h2>'
    )
    parts.append(
        "<p>Most kids are online every day — school, games, group chats, "
        "video apps — and most of it is fine. But the risks are real: "
        "bullying that follows a child home from school, strangers who "
        "pretend to be friends, and pressure to share photos that can "
        "never be taken back. This section covers what you can set up "
        "today, what to do the moment something happens, and the laws in "
        f"{esc(state)}. The national number to know is the National Center "
        "for Missing &amp; Exploited Children&rsquo;s CyberTipline at "
        '<a href="https://report.cybertip.org" target="_blank" '
        'rel="noopener">report.cybertip.org</a> or 1-800-843-5678 '
        "(1-800-THE-LOST), open 24 hours a day — it takes reports of "
        "online sexual exploitation of children. This is general "
        "information, not legal advice.</p>"
    )
    # --- Card 1: what parents can do right now ---
    parts.append('<div class="card">')
    parts.append("<h3>What parents can do right now</h3>")
    parts.append(
        "<p><strong>Set up the device controls.</strong> On an iPhone, "
        "iPad, or Mac, use Screen Time through Family Sharing: set age "
        "limits, approve app downloads, limit screen time, and block "
        "explicit content. On Android or a Chromebook, use Google Family "
        "Link: approve downloads, set daily limits, and see your "
        "child&rsquo;s location. (The Family Link parent app can run on "
        "an iPhone too.) <strong>Lock down the app store:</strong> "
        "require a password or your approval for every download and "
        "purchase, turn on the age rating for apps and games, and turn "
        "off precise location sharing in the apps your child uses — then "
        "check which apps can still see their location.</p>"
    )
    parts.append(
        "<p><strong>Talk about it, by age.</strong> With younger kids "
        "the rules are simple: never share your name, school, or photos "
        "with strangers online, and tell a grown-up right away if "
        "anything online feels wrong. With tweens and teens, talk about "
        "pressure to send photos, friend requests from strangers, and "
        "what to do if a message makes them uncomfortable — and make the "
        "deal clear: they will not be punished for telling you.</p>"
    )
    parts.append(
        "<p><strong>Know the privacy law in brief.</strong> Under the "
        "federal Children&rsquo;s Online Privacy Protection Act (COPPA), "
        "a website or app must get verifiable parental consent before it "
        "collects personal information from a child under 13. If a site "
        "collected your young child&rsquo;s information without your OK, "
        "complain to the company and to the Federal Trade Commission.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Set up Screen Time "
        "or Family Link tonight — it takes about ten minutes — turn on "
        "purchase approval, and have the short talk: &ldquo;If anything "
        "online ever feels wrong, tell me first. You won&rsquo;t be in "
        "trouble.&rdquo;</p>"
    )
    parts.append("</div>")
    # --- Card 2: cyberbullying ---
    parts.append('<div class="card">')
    parts.append("<h3>Cyberbullying</h3>")
    parts.append(
        "<p><strong>What counts:</strong> repeated mean texts or posts, "
        "spreading rumors or lies, sharing embarrassing photos, leaving "
        "someone out on purpose, threats — by text, social media, or in a "
        "game&rsquo;s chat. <strong>Document it first:</strong> take "
        "screenshots that show the date and the sender&rsquo;s name, "
        "save the messages, and do not delete anything — even if it hurts "
        "to keep it.</p>"
    )
    parts.append(
        "<p><strong>Report it twice:</strong> use the report and block "
        "buttons inside the app, and report it to the school — every "
        "state requires public schools to have a bullying policy, and in "
        "many states that policy covers online bullying that disrupts "
        "learning, even if it happened after school hours. "
        "<strong>When it is a crime:</strong> threats to hurt someone, "
        "stalking, sharing intimate images without consent, and "
        "harassment aimed at a child&rsquo;s race, sex, disability, or "
        "religion can be crimes — call your local police if it crosses "
        "that line.</p>"
    )
    parts.append(
        f"<p><strong>In {esc(state)}:</strong> {esc(e['cyberbullying'])}</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Screenshot "
        "everything first, then report inside the app, then tell the "
        "school in writing (email, so there is a record). If there are "
        "threats or shared images, call the police.</p>"
    )
    parts.append("</div>")
    # --- Card 3: grooming and online predators ---
    parts.append('<div class="card">')
    parts.append("<h3>Grooming and online predators</h3>")
    parts.append(
        "<p><strong>Warning signs:</strong> an adult or older teen who "
        "asks to move to a private chat, asks for photos, offers gifts or "
        "money, asks your child to keep secrets, or asks to meet in "
        "person. A &ldquo;friend&rdquo; your child has never met in real "
        "life who seems to know a lot about them is a red flag.</p>"
    )
    parts.append(
        "<p><strong>The moment you suspect it:</strong> stay calm, do "
        "not confront the person, and do not delete anything — "
        "screenshots and saved messages are evidence. Tell a trusted "
        "adult, then report it to your local police and to the National "
        "Center for Missing &amp; Exploited Children&rsquo;s "
        "CyberTipline at "
        '<a href="https://report.cybertip.org" target="_blank" '
        'rel="noopener">report.cybertip.org</a> or 1-800-843-5678. The '
        "CyberTipline is open 24 hours a day.</p>"
    )
    if e.get("grooming"):
        parts.append(
            f"<p><strong>In {esc(state)}:</strong> {esc(e['grooming'])}</p>"
        )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Save the evidence, "
        "report to the police and the CyberTipline the same day, and do "
        "not let your child keep talking to the person while you wait "
        "for a reply.</p>"
    )
    parts.append("</div>")
    # --- Card 4: sextortion and shared images ---
    parts.append('<div class="card">')
    parts.append("<h3>Sextortion and shared images</h3>")
    parts.append(
        "<p><strong>What sextortion is:</strong> someone threatens to "
        "share intimate photos or videos unless you pay money or send "
        "more images. It happens most often to boys ages 14 to 17. The "
        "FBI counted more than 13,000 reports of online financial "
        "sextortion of minors from October 2021 to March 2023, and at "
        "least 20 suicides.</p>"
    )
    parts.append(
        "<p><strong>Do not pay. Do not send more images. Do not delete "
        "anything</strong> — save the messages, the usernames, and the "
        "payment demands, then block the account. Report the account to "
        "the platform, report to NCMEC&rsquo;s CyberTipline at "
        '<a href="https://report.cybertip.org" target="_blank" '
        'rel="noopener">report.cybertip.org</a> or 1-800-843-5678, and '
        "report to the FBI at "
        '<a href="https://tips.fbi.gov" target="_blank" '
        'rel="noopener">tips.fbi.gov</a> or 1-800-CALL-FBI.</p>'
    )
    parts.append(
        "<p><strong>If an image is already shared:</strong> ask the "
        "platform to take it down, and use NCMEC&rsquo;s Take It Down "
        "service at "
        '<a href="https://takeitdown.ncmec.org" target="_blank" '
        'rel="noopener">takeitdown.ncmec.org</a> — free, for images of '
        "someone under 18. Under the federal TAKE IT DOWN Act of 2025, "
        "covered platforms must remove flagged intimate images within 48 "
        "hours of being notified. This site also covers sextortion in the "
        f'<a href="#stalking-in-{slug}">Stalking section for {esc(state)}</a>.</p>'
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Stop, save, block, "
        "report — in that order. Do not pay, and do not let shame stop "
        "you from reporting: the CyberTipline and the FBI handle these "
        "reports every day.</p>"
    )
    parts.append("</div>")
    # --- Card 5: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Protecting kids online in {esc(state)}</h3>")
    parts.append(f"<p><strong>How it works here:</strong> {esc(e['overview'])}</p>")
    parts.append(
        f"<p><strong>Cyberbullying law:</strong> {esc(e['cyberbullying'])}</p>"
    )
    if e.get("sexting"):
        parts.append(f"<p><strong>Sexting:</strong> {esc(e['sexting'])}</p>")
    if e.get("grooming"):
        parts.append(f"<p><strong>Grooming:</strong> {esc(e['grooming'])}</p>")
    if e.get("age_design"):
        parts.append(
            f"<p><strong>Social media and age checks:</strong> {esc(e['age_design'])}</p>"
        )
    if e.get("report_name") and e.get("report_url"):
        line = (
            f"<p><strong>Where to report in {esc(state)}:</strong> "
            f'<a href="{esc(e["report_url"])}" target="_blank" rel="noopener">{esc(e["report_name"])}</a>.'
        )
        if slug == "maine":
            line += (
                " This unit does not take reports directly from the public "
                "— report to your local police department or the State "
                "Police troop that covers your area, and they can refer "
                "the case."
            )
        else:
            line += " Start here for the state&rsquo;s reporting route."
        line += "</p>"
        parts.append(line)
    aid_note = LEGAL_AID_NOTE.get(slug, "")
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>'
        f"{esc(aid_note)}.</p>"
    )
    parts.append(
        "<p><strong>What to do:</strong> Start with the reporting links "
        "above, and keep copies of everything you send. If a child is in "
        "immediate danger, call 911 or your local police — do not wait "
        "for an online form.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Set up parental "
        "controls and purchase approval tonight. (2) If something "
        "happens, screenshot and save everything before you report or "
        "block. (3) Report to the platform, the school, or the police "
        "depending on what happened — and to NCMEC&rsquo;s CyberTipline "
        "for anything sexual involving a child. (4) If money or photos "
        "are being demanded, do not pay and do not send more — report to "
        "the CyberTipline and the FBI the same day.</p>"
    )
    parts.append(
        "<p><em>Sources: the National Center for Missing &amp; Exploited "
        "Children, the FBI, the Federal Trade Commission, and the official "
        "state statutes and agencies linked in the research for this "
        "section, checked November 23, 2026. State laws on social-media "
        "age checks are changing fast and several are in court — check the "
        "card above for your state&rsquo;s current status. Confirm the "
        "current law with a local attorney before you rely on it. This is "
        "general information, not legal advice.</em></p>"
    )
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def build_state_pages(data):
    for key, e in data:
        state = e["state"]
        slug = e.get("slug") or key.replace(" ", "-")
        path = STATES / f"{slug}.html"
        text = path.read_text()
        anchor = f'id="{SLUG}-in-{slug}"'
        assert anchor not in text, f"{slug}: anchor already present"
        h2 = text.find(f'<h2 id="{PREV_SLUG}-in-{slug}">')
        assert h2 != -1, f"{slug}: {PREV_SLUG} h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        before = text
        new_section = section_html(state, slug, e)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
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
            f"Protecting kids online in {state}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        assert text.count(f'id="{SLUG}-in-{slug}"') == 1, f"{slug}: anchor count"
        assert text.count("<div") - before.count("<div") == 5, f"{slug}: div open delta"
        assert text.count("</div>") - before.count("</div>") == 5, f"{slug}: div close delta"
        assert text.count("<div") == text.count("</div>"), f"{slug}: div imbalance"
        h2s = re.findall(r'<h2 id="([^"]+)">', text)
        assert h2s.index(f"{SLUG}-in-{slug}") == h2s.index(f"{PREV_SLUG}-in-{slug}") - 1, f"{slug}: h2 order"
        assert not re.search(r"\bNone\b", new_section), f"{slug}: leaked None in new section"
        assert "TODO" not in new_section and "FIXME" not in new_section, f"{slug}: leaked marker"
        assert f'href="#stalking-in-{slug}"' in new_section, f"{slug}: stalking cross-link missing"
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert SLUG not in helper_part, "index already has helper option"
    assert f'data-topic="{SLUG}"' not in text, "index already has card"
    assert 'value="child-safety"' in text, "child-safety option missing"
    m = re.search(
        r'<option value="gender-marker-changes" data-anchor="gender-marker-changes">.*?</option>',
        text,
        re.S,
    )
    assert m, "gender-marker helper option not found"
    opt_old = m.group(0)
    opt_new = (
        opt_old
        + '\n<option value="protecting-kids-online" data-anchor="protecting-kids-online">'
        "Protecting kids online — parental controls, cyberbullying, grooming, and sextortion: what to do, how to report it, and your state&rsquo;s laws</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="gender-marker-changes"'
    idx = text.find(card_anchor)
    assert idx != -1, "gender-marker card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="protecting-kids-online">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-protecting-kids-online.jpg" alt="Protecting Kids Online" loading="lazy"></span>
          <h3>Protecting Kids Online</h3>
          <p>Parental controls, cyberbullying, grooming, and sextortion — what to do the moment something happens, how to report it, and your state&rsquo;s laws — state by state.</p>
          <span class="go">Learn more about Protecting Kids Online &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 110 topics" in text, "show-all label not found"
    text = text.replace("Show all 110 topics", "Show all 111 topics", 1)
    show_pos = text.find("Show all 111 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">110 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("110 topics", "111 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 110->111 (child-safety option left as-is)")


def build_about():
    text = ABOUT.read_text()
    assert text.count("110 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("110 legal topics", "111 legal topics", 1))
    print("  about.html: 110 -> 111")


def state_index_t(state, slug, e):
    bits = [
        "protecting kids online parental controls Screen Time Family Link "
        "cyberbullying grooming sextortion NCMEC CyberTipline Take It Down COPPA",
        f"Protecting kids online in {state}",
        f"{e['overview']}",
        f"cyberbullying {e['cyberbullying']}",
        f"sexting {e.get('sexting', '')}",
        f"grooming {e.get('grooming', '')}",
        f"social media age checks {e.get('age_design', '')}",
        f"{e.get('report_name', '')} {e['legal_aid_name']}",
        "report bullying school police sextortion predator take it down remove image",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 12028, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = e["state"]
        slug = e.get("slug") or key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Protecting kids online in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Protecting Kids Online",
            "t": (
                "protecting-kids-online Protecting Kids Online? "
                "Parental controls, cyberbullying, grooming, and sextortion — what to do the moment something "
                "happens, how to report it, and your state's laws — state by state. "
                "Screen Time Family Link cyberbullying grooming sextortion NCMEC CyberTipline Take It Down COPPA "
                "report bullying school police predator remove image."
            ),
        }
    )
    assert len(idx) == 12079, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 12028 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    assert len(d) == 50, len(d)
    data = [(k, d[k]) for k in sorted(d)]  # keys already lowercase slugs
    slugs = [(e.get("slug") or k.replace(" ", "-")) for k, e in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req_core = ["overview", "cyberbullying", "legal_aid_name", "legal_aid_url", "sources", "state"]
    req_maybe_empty = ["sexting", "grooming", "age_design", "report_name", "report_url"]
    phone_re = re.compile(
        r"\(\d{3}\)\s*\d{3}[-.]\d{4}|\b\d{3}[-.]\d{3}[-.]\d{4}\b|"
        r"1-800-\d{3}-\d{4}|1-866-\d{3}-\d{4}|1-888-\d{3}-\d{4}|1-855-\d{3}-\d{4}|"
        r"877-\d{3}-\d{4}|800-\d{3}-\d{4}|844-\d{3}-\d{4}|866-\d{3}-\d{4}|855-\d{3}-\d{4}|"
        r"1-877-\d{3}-\d{4}|1-833-[A-Z0-9]{7}"
    )
    for k, e in data:
        for f in req_core + req_maybe_empty:
            assert f in e, f"{k}: missing {f}"
        assert all(e[f] for f in req_core if f != "sources"), f"{k}: empty core field"
        assert e["sources"] and len(e["sources"]) >= 2, f"{k}: fewer than 2 sources"
        blob = json.dumps({f: e[f] for f in req_core + req_maybe_empty if f != "sources"})
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before gender-marker-changes section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
