#!/usr/bin/env python3
"""Build Topic #100: Firearm Rights Restoration — standalone section on
all 50 state pages.

Inserts one new section per state page (before Labor Union Rights,
newest-first), a contents-list entry (before the labor-union-rights
<li>), a homepage helper option + topic card (after Labor Union
Rights), bumps About 98 -> 99, and appends 50 state entries + 1
helper entry to assets/search-index.json (11416 -> 11467).

Data: hidden_files/topic-research/firearm-rights-restoration/all-states.json
(coordinator-merged 2026-11-20 from 5 research batches; keys are
Title Case in JSON, normalized to lowercase before building. All 100
agency + legal-aid URLs checked: 87 curl 200, 13 resolved via text
fetch or researcher live opens (AZ CLS, ID Legal Aid, KS governor
clemency, MA mass.gov pardons, MA GBLS, MN mncourts.gov, MO courts.mo.gov
500 was transient, MS Legal Services, NH courts, NJ courts, RI governor,
SD DOC pardon FAQ, TN clemency FAQ PDF). Coordinator resolutions:
HI agency null -> https://dcr.hawaii.gov/hpa/ (Hawaii Paroling
Authority); IN null -> https://www.in.gov/idoc/parole-board; KY PDF ->
https://governor.ky.gov/services/application-for-pardons-and-commutations;
LA PDF -> https://doc.la.gov/imprisoned-person-programs-resources/pardons-parole/;
ME PDF -> https://www1.maine.gov/corrections/pardonboard; VA PDF ->
https://www.restore.virginia.gov/ and VA legal aid null ->
https://www.vlas.org/; WA null -> https://www.courts.wa.gov/; NC null ->
https://www.nccourts.gov/; RI null -> https://governor.ri.gov/; AR null ->
https://doc.arkansas.gov/parole-board/executive-clemency/; CA legal aid
null -> https://www.rootandrebound.org/; TX PDF ->
https://www.tdcj.texas.gov/bpp/; WY contact page ->
https://corrections.wyo.gov/; TN clemency FAQ PDF kept (verified live
via fetch; tn.gov bot-filters curl); IL agency URL de-tracked
(?sfnsn=mo stripped); KS note typo fixed ("a person felony or drug
crime" -> "a felony or drug crime") and KS legal-aid URL de-tracked to
https://www.kansaslegalservices.org/; ME legal-aid URL corrected to
https://www.ptla.org/; ?ref= params stripped from OH/KY sources.
Headline counts: restoration possible yes 14 / limited 36 / no 0
(yes: AK, AZ, ID, IN, MI, MN, MS, MT, ND, OH, OR, SD, VA, WY);
process pardon 22 / court-petition 10 / varies 10 / automatic 4
(AK, LA, ND, SD) / expungement 4 (IN, MO, NH, NJ). No phone numbers
in the dataset. Key verifications: MN Minn. Stat. 609.165 subd. 1d is
current — crime-of-violence felons may petition the sentencing court
on good cause after release from confinement, no fixed wait for a
first petition, 3-year refiling bar after denial (the 2015 HF 3779
10-year proposal was never enacted); NC N.C.G.S. 14-415.4 wait still
20 years (2017 bill to cut it to 10 never passed), read on ncleg.gov
2026-11-20; UT restricted-persons statute recodified 2025 from
76-10-503 to 76-11-303; WI pardon applications after Oct 5, 2026 held
for the next administration; CO clemency applications after Apr 3,
2026 held for the next administration; VT route unsettled in official
sources (ban keys to violent crime only, 13 V.S.A. 4017).
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "firearm-rights-restoration" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-firearm-rights-restoration.jpg"

SLUG = "firearm-rights-restoration"
TITLE = "Firearm Rights Restoration"
PREV_SLUG = "labor-union-rights"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def possible_word(v):
    return {"yes": "Yes", "limited": "Limited — only some people qualify", "no": "No"}.get(v, v)


def process_word(v):
    return {
        "automatic": "Automatic — rights come back on their own when the waiting period ends",
        "court-petition": "Court petition",
        "pardon": "Governor\u2019s pardon",
        "varies": "Varies — it depends on the conviction",
        "expungement": "Expungement",
    }.get(v, v)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="firearm-rights-restoration-in-{slug}">Firearm rights restoration in {esc(state)}</h2>'
    )
    parts.append(
        "<p>A felony conviction usually takes away the right to possess a "
        "firearm. In many states there is a way to get that right back — "
        "a pardon, a court petition, an expungement, or simply waiting out "
        "the ban. The route, the wait, and who qualifies are different in "
        "every state, and there is one warning that applies everywhere: "
        "getting your rights back under <strong>state</strong> law does not "
        "always lift the separate <strong>federal</strong> ban. Read the "
        "federal warning below first, then your state&rsquo;s card. The "
        "picture here is as of <strong>November 2026</strong>. This is "
        "general information, not legal advice.</p>"
    )
    # --- Card 1: federal warning ---
    parts.append('<div class="card">')
    parts.append("<h3>The federal warning first</h3>")
    parts.append(
        "<p>Federal law (18 U.S.C. &sect; 922(g)) makes it a federal crime "
        "for a person convicted of a felony punishable by more than a year "
        "in prison to possess a firearm. That ban is <strong>separate</strong> "
        "from your state&rsquo;s ban, and a state pardon, court order, or "
        "expungement does not always lift it. Whether it does depends on "
        "the exact kind of relief you got and how federal law treats it — "
        "for example, a pardon that expressly restores firearm rights is "
        "treated differently from a pardon that says nothing about "
        "firearms, and an expungement that fully erases the conviction is "
        "treated differently from a record-sealing that leaves the "
        "conviction in place.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Do <strong>not</strong> "
        "buy, borrow, or handle a firearm until you are sure both the "
        "state ban and the federal ban are lifted for you. If you are not "
        "sure, ask a criminal-defense lawyer or the legal aid listed in "
        "your state&rsquo;s card below before you touch one — possessing a "
        "firearm while still banned can mean a new felony charge, even if "
        "you believed your rights were restored.</p>"
    )
    parts.append("</div>")
    # --- Card 2: five routes ---
    parts.append('<div class="card">')
    parts.append("<h3>The five routes back</h3>")
    parts.append(
        "<p>Across the 50 states, restoration happens in five ways. "
        "<strong>Governor&rsquo;s pardon (22 states):</strong> you apply "
        "to the governor (or a pardons board that recommends to the "
        "governor), and only a pardon that expressly restores firearm "
        "rights counts. <strong>Court petition (10 states):</strong> you "
        "ask a judge to lift the ban, usually by showing good cause and a "
        "clean record since the sentence ended. <strong>Varies (10 "
        "states):</strong> the route depends on the conviction — one kind "
        "of felony may be restored automatically, another only by pardon. "
        "<strong>Automatic (4 states — Alaska, Louisiana, North Dakota, "
        "South Dakota):</strong> the ban ends on its own when the waiting "
        "period runs out, with no application needed. "
        "<strong>Expungement (4 states — Indiana, Missouri, New "
        "Hampshire, New Jersey):</strong> clearing the conviction in court "
        "restores the right along with it.</p>"
    )
    parts.append(
        "<p>In <strong>14 states</strong> most people with a felony "
        "conviction have a real route back; in <strong>36 states</strong> "
        "the route is limited — only some convictions qualify, or only a "
        "pardon will do. No state has a route for everyone: violent "
        "felonies, crimes with a firearm, and repeat felonies are excluded "
        "in most states.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Find your state&rsquo;s "
        "route in the card below. The route decides who you apply to — a "
        "governor, a board, or a judge — and the waiting period decides "
        "when you can apply.</p>"
    )
    parts.append("</div>")
    # --- Card 3: traps ---
    parts.append('<div class="card">')
    parts.append("<h3>Traps: do not get caught by these</h3>")
    parts.append(
        "<p><strong>Assuming getting your vote back restores your gun "
        "rights.</strong> It does not. In Florida, restoring voting rights "
        "under Amendment 4 does not restore firearm rights — that takes a "
        "separate clemency decision. In Kentucky, automatic restoration of "
        "voting rights does not restore firearm rights either. "
        "<strong>Assuming sealing or expunging the record is enough.</strong> "
        "In Arkansas, sealing a record alone does not restore firearm "
        "rights, and in California a dismissal under Penal Code 1203.4 "
        "does not either. <strong>Assuming time alone does it.</strong> In "
        "Oregon, the state Supreme Court has held that the 15-year "
        "provision does not lift the ban — you still need a court order, "
        "a set-aside, or a pardon. <strong>Assuming any pardon works.</strong> "
        "In Alabama, Arkansas, and Georgia, a pardon that does not "
        "expressly mention firearm rights does not restore them. "
        "<strong>Assuming the state ban is the only ban.</strong> The "
        "federal ban under 18 U.S.C. &sect; 922(g) can still apply after a "
        "state restoration — see the warning at the top.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check the exact words "
        "of whatever relief you get — a pardon, a court order, or an "
        "expungement — and make sure it says firearm rights are restored. "
        "If it does not say so, assume they are not.</p>"
    )
    parts.append("</div>")
    # --- Card 4: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Firearm rights restoration in {esc(state)}</h3>")
    parts.append(
        f"<p><strong>Can rights be restored?</strong> {possible_word(e['restoration_possible'])}. {esc(e['restoration_note'])}</p>"
    )
    parts.append(
        f"<p><strong>How it works:</strong> {process_word(e['process'])}. {esc(e['process_note'])}</p>"
    )
    parts.append(
        f"<p><strong>Waiting period:</strong> {esc(e['waiting_period'])}</p>"
    )
    parts.append(
        f"<p><strong>The law:</strong> {esc(e['statute_name'])} — {esc(e['statute_cite'])}</p>"
    )
    parts.append(
        f"<p><strong>Where to apply:</strong> "
        f'<a href="{esc(e["agency_url"])}" target="_blank" rel="noopener">{esc(e["agency_name"])}</a>.</p>'
    )
    if e["state_note"]:
        parts.append(f"<p>{esc(e['state_note'])}</p>")
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Start with the agency "
        "linked above — it has the application or the court forms. If "
        "your case is complicated, or you are not sure the federal ban is "
        "lifted too, talk to the legal aid above or a criminal-defense "
        "lawyer before you apply, and do not possess a firearm in the "
        "meantime.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Read the federal "
        "warning at the top — state restoration does not always lift the "
        "federal ban. (2) Find your state&rsquo;s route and waiting period "
        "in the card above. (3) Apply to the agency linked there — a "
        "governor, a pardons board, or a court. (4) Make sure whatever you "
        "receive expressly restores firearm rights. (5) Do not possess a "
        "firearm until you are sure both bans are lifted.</p>"
    )
    parts.append(
        "<p><em>Sources: the official state statutes, pardons boards, "
        "governors&rsquo; offices, and courts linked in the research for "
        "this section, checked November 20, 2026. Restoration rules change "
        "— confirm the current law with your state&rsquo;s agency before "
        "you rely on it. This is general information, not legal advice.</em></p>"
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
            f"Firearm rights restoration in {state}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        assert text.count(f'id="{SLUG}-in-{slug}"') == 1, f"{slug}: anchor count"
        assert text.count("<div") - before.count("<div") == 4, f"{slug}: div open delta"
        assert text.count("</div>") - before.count("</div>") == 4, f"{slug}: div close delta"
        assert text.count("<div") == text.count("</div>"), f"{slug}: div imbalance"
        h2s = re.findall(r'<h2 id="([^"]+)">', text)
        assert h2s.index(f"{SLUG}-in-{slug}") == h2s.index(f"{PREV_SLUG}-in-{slug}") - 1, f"{slug}: h2 order"
        assert not re.search(r"\bNone\b", new_section), f"{slug}: leaked None in new section"
        assert "TODO" not in new_section and "FIXME" not in new_section, f"{slug}: leaked marker"
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert SLUG not in helper_part, "index already has helper option"
    assert f'data-topic="{SLUG}"' not in text, "index already has card"
    opt_old = (
        '<option value="labor-union-rights" data-anchor="labor-union-rights">'
        "Labor union rights (right-to-work, public-sector bargaining, strikes, where to complain)</option>"
    )
    assert opt_old in text, "labor-union helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="firearm-rights-restoration" data-anchor="firearm-rights-restoration">'
        "Firearm rights restoration (pardons, court petitions, expungement, waiting periods, the federal warning)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="labor-union-rights"'
    idx = text.find(card_anchor)
    assert idx != -1, "labor-union card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="firearm-rights-restoration">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-firearm-rights-restoration.jpg" alt="Firearm rights restoration" loading="lazy"></span>
          <h3>Firearm Rights Restoration</h3>
          <p>Can you get your gun rights back after a felony conviction? Pardons, court petitions, waiting periods, and the federal warning — state by state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 53 topics" in text, "show-all label not found"
    text = text.replace("Show all 53 topics", "Show all 54 topics", 1)
    show_pos = text.find("Show all 54 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">53 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("53 topics", "54 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 53->54")


def build_about():
    text = ABOUT.read_text()
    assert text.count("98 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("98 legal topics", "99 legal topics", 1))
    print("  about.html: 98 -> 99")


def state_index_t(state, slug, e):
    bits = [
        "firearm rights restoration gun rights after felony conviction",
        f"Firearm rights restoration in {state}",
        f"can rights be restored {possible_word(e['restoration_possible']).lower()} {e['restoration_note']}",
        f"how it works {process_word(e['process']).lower()} {e['process_note']}",
        f"waiting period {e['waiting_period']}",
        f"{e['statute_name']} {e['statute_cite']}",
        "federal ban 18 U.S.C. 922(g) federal warning",
        f"{e['agency_name']}",
        f"{e['state_note'] or ''}",
        f"{e['legal_aid_name']}",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11416, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Firearm rights restoration in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Firearm Rights Restoration",
            "t": (
                "firearm-rights-restoration firearm rights restoration Firearm Rights Restoration? "
                "Can you get your gun rights back after a felony conviction? Pardons, court petitions, "
                "waiting periods, and the federal warning — state by state. "
                "18 U.S.C. 922(g) pardon court petition expungement automatic restoration waiting period."
            ),
        }
    )
    assert len(idx) == 11467, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11416 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d
    assert len(states) == 50, len(states)
    data = [(k.lower(), states[k]) for k in sorted(states)]  # keys are Title Case in JSON; page files are lowercase
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "restoration_possible", "restoration_note", "process", "process_note",
        "waiting_period", "statute_name", "statute_cite", "agency_name",
        "agency_url", "legal_aid_name", "legal_aid_url", "state_note", "sources",
    ]
    phone_re = re.compile(
        r"\(\d{3}\)\s*\d{3}[-.]\d{4}|\b\d{3}[-.]\d{3}[-.]\d{4}\b|"
        r"1-800-\d{3}-\d{4}|1-866-\d{3}-\d{4}|1-888-\d{3}-\d{4}|1-855-\d{3}-\d{4}|"
        r"877-\d{3}-\d{4}|800-\d{3}-\d{4}|844-\d{3}-\d{4}|866-\d{3}-\d{4}|855-\d{3}-\d{4}|"
        r"1-877-\d{3}-\d{4}|1-833-[A-Z0-9]{7}"
    )
    for k, e in data:
        for f in req:
            assert f in e, f"{k}: missing {f}"
        assert e["restoration_possible"] in ("yes", "limited", "no"), f"{k}: bad restoration_possible"
        assert e["process"] in ("automatic", "court-petition", "pardon", "varies", "expungement"), f"{k}: bad process"
        assert e["restoration_note"] and e["process_note"] and e["waiting_period"] and e["statute_name"] and e["statute_cite"] and e["agency_name"] and e["agency_url"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"], f"{k}: empty required field"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before labor-union-rights section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
