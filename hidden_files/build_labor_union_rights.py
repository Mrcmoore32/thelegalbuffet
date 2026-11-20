#!/usr/bin/env python3
"""Build Topic #99: Labor Union Rights — standalone section on all
50 state pages.

Inserts one new section per state page (before Felon Voting Rights,
newest-first), a contents-list entry (before the felon-voting-rights
<li>), a homepage helper option + topic card (after Felon Voting
Rights), bumps About 97 -> 98, and appends 50 state entries + 1
helper entry to assets/search-index.json (11365 -> 11416).

Data: hidden_files/topic-research/labor-union-rights/all-states.json
(coordinator-merged 2026-11-20 from 5 research batches; keys normalized
to lowercase. All 100 agency + legal-aid URLs checked: 83 curl 200,
17 resolved via text fetch (FL PERC, HI HLRB, OH SERB, AZ ICA, CA PERB,
CO CDLE, ID Legal Aid, RI DLT, TN DOL, TN LAS, VT DOL, WY DWS all
confirmed live with real content; KS DOL, KY ELC, ME MLRB, MI MERC
confirmed live earlier; NH PELRB 403s both curl and fetch — bot filter,
researcher opened it and search crawl confirms it). Coordinator
resolutions: OH legal aid is Legal Aid of Southeast and Central Ohio
(lasco.org — LASC merged into LASCO Jan 1, 2024, 36 counties); NY
legal aid is Empire Justice Center (statewide; Legal Aid Society is
NYC-only); ND keeps lsnd.org (legalassist.org redirects to it, per
#98 precedent); MI MERC agency URL swapped to the current landing
page (researcher's URL was a 2011 decisions archive); MI repeal
effective date sharpened to March 2024 per MERC's own page (SB 34,
signed Mar 24, 2023). Headline counts: right-to-work yes 26 / no 24;
public bargaining yes 27 / limited 17 / no 6 (AR, GA, MS, NC, SC, WV);
public strike no 39 / limited 11 (AK, CA, CO, HI, IL, MN, MT, OH, OR,
PA, VT) — no state gives an unrestricted public strike right. No phone
numbers in the dataset. Utah HB 267 note: the 2025 ban was repealed by
the Legislature Dec 9, 2025 (HB 2001, eff. Feb 8, 2026) before it ever
took effect, so Utah public bargaining is "yes" again. Wisconsin Act 10
still in force: Dane County ruling striking it down was reversed by the
Court of Appeals Jul 29, 2026 (Abbotsford Education Assn. v. WERC).
Wyoming public-strike "no" is the weakest cell (no clean statute; a
2024 bill to expressly ban teacher strikes failed introduction) — the
note states only that no Wyoming law gives public workers a strike
right, which is accurate as written.)
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "labor-union-rights" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-labor-union-rights.jpg"

SLUG = "labor-union-rights"
TITLE = "Labor Union Rights"
PREV_SLUG = "felon-voting-rights"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def rtw_word(v):
    return {"yes": "Yes — right-to-work state", "no": "No", "limited": "Limited"}.get(v, v)


def bargaining_word(v):
    return {"yes": "Yes", "limited": "Limited", "no": "No"}.get(v, v)


def strike_word(v):
    return {"yes": "Yes", "limited": "Limited", "no": "No"}.get(v, v)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="labor-union-rights-in-{slug}">Labor union rights in {esc(state)}</h2>'
    )
    parts.append(
        "<p>Can you join a union at your job? Can you be forced to pay union "
        "dues? If you work for the government, can you bargain over pay — or "
        "go on strike? The answers depend on two different sets of law: a "
        "federal law that covers private-sector workers in every state, and "
        "your state&rsquo;s own rules, which decide what happens for public "
        "workers and whether dues can be required. This section explains both, "
        "and what to do in your state. The picture here is as of "
        "<strong>November 2026</strong>. This is general information, not "
        "legal advice.</p>"
    )
    # --- Card 1: federal baseline ---
    parts.append('<div class="card">')
    parts.append("<h3>The federal baseline: private-sector workers</h3>")
    parts.append(
        "<p>Private-sector workers in <strong>every state</strong> are covered "
        "by the federal National Labor Relations Act (NLRA). It gives you the "
        "right to form or join a union, to bargain collectively over pay, "
        "hours, and working conditions, and to act together with coworkers "
        "to improve conditions — even if there is no union at your workplace "
        "yet. Your employer may not fire you, demote you, or punish you for "
        "exercising those rights, and the National Labor Relations Board "
        "(NLRB) is the agency that enforces them. Private-sector strikes are "
        "generally protected too, though there are rules about how and when "
        "you can strike, and some workers — such as supervisors and "
        "independent contractors — are not covered.</p>"
    )
    parts.append(
        "<p>Public-sector workers — teachers, police, firefighters, state and "
        "city employees — are <strong>not</strong> covered by the NLRA. "
        "Their rights come from state law, and that is where the states "
        "differ sharply. Everything in the next two cards is about those "
        "state rules.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you work for a private "
        "company, start with the NLRB: you can file a charge online or at a "
        "regional office if your employer retaliates against union activity. "
        "If you work for the government, read your state&rsquo;s cards below "
        "&mdash; the rules are different.</p>"
    )
    parts.append("</div>")
    # --- Card 2: right-to-work ---
    parts.append('<div class="card">')
    parts.append("<h3>Right-to-work: what it means</h3>")
    parts.append(
        "<p><strong>26 states</strong> have right-to-work laws; <strong>24 "
        "do not</strong>. In a right-to-work state, no worker can be forced "
        "to join a union or pay union dues as a condition of keeping a job. "
        "That does <strong>not</strong> mean unions are banned there — a "
        "union can still form, bargain, and represent workers. It means "
        "paying is voluntary. And even in a right-to-work state, if a union "
        "represents your workplace, it must represent <em>every</em> worker "
        "in the unit fairly, whether or not they pay dues.</p>"
    )
    parts.append(
        "<p>In a state without right-to-work, a union contract can require "
        "workers it covers to pay dues or fees for representation. But there "
        "is one big exception for public workers: the Supreme Court&rsquo;s "
        "<em>Janus</em> decision (2018) says public employees cannot be "
        "forced to pay union fees at all, even in states without "
        "right-to-work laws. So in the public sector, paying is voluntary "
        "everywhere.</p>"
    )
    parts.append(
        "<p>These laws change. Michigan repealed its right-to-work law in "
        "2023, and the repeal took effect in March 2024 — the first state in "
        "nearly 60 years to do so. Illinois went the other way in 2022, when "
        "voters added a constitutional amendment banning any future "
        "right-to-work law in the state.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check your state&rsquo;s "
        "right-to-work line in the card below. If you are being told you "
        "must pay dues to keep your job in a right-to-work state, or you are "
        "being punished for not joining a union, that is worth a complaint "
        "&mdash; see the agency link in your state&rsquo;s card.</p>"
    )
    parts.append("</div>")
    # --- Card 3: public bargaining buckets ---
    parts.append('<div class="card">')
    parts.append("<h3>Public-sector bargaining: the three buckets</h3>")
    parts.append(
        "<p><strong>Yes (27 states):</strong> public workers can form unions "
        "and bargain over pay, hours, and working conditions under a state "
        "law. <strong>Limited (17 states):</strong> only some public workers "
        "can bargain — teachers only, or firefighters only, or workers in "
        "some cities but not others. <strong>No (6 states):</strong> "
        "Arkansas, Georgia, Mississippi, North Carolina, South Carolina, and "
        "West Virginia have no law giving public workers bargaining rights at "
        "all. In North Carolina and South Carolina, the law goes further and "
        "declares public-sector bargaining contracts illegal.</p>"
    )
    parts.append(
        "<p>&ldquo;Limited&rdquo; takes many shapes. Virginia banned "
        "public-sector bargaining for decades, then in 2021 let each city and "
        "county decide for itself whether to allow it. Colorado gave "
        "bargaining rights to state workers in 2020 and county workers in "
        "2022, but most city and school workers still have none. Texas bans "
        "bargaining for most public workers, but police and firefighters in "
        "some cities can bargain under separate laws. Iowa narrowed "
        "bargaining in 2017 so most public workers can bargain only over "
        "base pay.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Find your state&rsquo;s "
        "bucket in the card below. If you are in a &ldquo;limited&rdquo; "
        "state, read the note carefully — the right may cover your job, or "
        "it may cover only a different group of public workers.</p>"
    )
    parts.append("</div>")
    # --- Card 4: strikes ---
    parts.append('<div class="card">')
    parts.append("<h3>Can public workers strike?</h3>")
    parts.append(
        "<p><strong>No state gives public workers an unrestricted right to "
        "strike.</strong> In 39 states the answer is no — public-sector "
        "strikes are banned, and striking can mean being fired or fined. In "
        "11 states the answer is &ldquo;limited&rdquo;: some public workers "
        "may strike, but only after finishing the full dispute process — "
        "mediation, fact-finding, an expired contract, and advance notice — "
        "and police, firefighters, and other safety workers are barred "
        "everywhere.</p>"
    )
    parts.append(
        "<p>The 11 limited states are Alaska, California, Colorado, Hawaii, "
        "Illinois, Minnesota, Montana, Ohio, Oregon, Pennsylvania, and "
        "Vermont. Even there, the rules are strict: in Oregon, for example, "
        "most public workers may strike only after bargaining, mediation, a "
        "30-day cooling-off period, and 10 days&rsquo; notice. In Minnesota, "
        "only workers who are not essential may strike. In Montana, the "
        "right comes from a 1974 state Supreme Court decision, not a statute."
        "</p>"
    )
    parts.append(
        "<p>Private-sector strikes are different: they are generally "
        "protected by federal law, though there are rules about timing and "
        "notice, and some strikes — such as a strike over a contract that is "
        "still in effect — are not protected.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you work for the "
        "government, do <strong>not</strong> walk out without checking your "
        "state&rsquo;s strike line below first. In most states a public-sector "
        "strike is illegal, and the consequences can include losing your job.</p>"
    )
    parts.append("</div>")
    # --- Card 5: recent changes ---
    parts.append('<div class="card">')
    parts.append("<h3>Recent changes worth knowing</h3>")
    parts.append(
        "<p><strong>Michigan (2023–2024):</strong> repealed its right-to-work "
        "law; the repeal took effect in March 2024. <strong>Utah "
        "(2025):</strong> the Legislature passed a ban on public-sector "
        "bargaining (HB 267), but voters collected over 250,000 signatures "
        "to put it on the ballot, and the Legislature repealed it in "
        "December 2025 before it ever took effect — so Utah public workers "
        "can still bargain. <strong>Wisconsin (Act 10):</strong> the 2011 law "
        "that limits most public workers to bargaining over base wages only, "
        "capped at inflation, is still in force — a court ruling against it "
        "in December 2024 was reversed on appeal in July 2026. "
        "<strong>Florida (2023):</strong> public-sector unions must now keep "
        "at least 60% of workers as dues-paying members or risk losing "
        "certification, and most public-employer dues deductions ended. "
        "<strong>Nevada (2019):</strong> state workers got bargaining rights "
        "for the first time. <strong>Illinois (2022):</strong> voters banned "
        "any future right-to-work law in the state constitution.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If a news story or a "
        "coworker tells you the rules changed, check the date — several of "
        "these changes are from the last few years, and older guides may "
        "still print the old rule.</p>"
    )
    parts.append("</div>")
    # --- Card 6: traps ---
    parts.append('<div class="card">')
    parts.append("<h3>Traps: do not get caught by these</h3>")
    parts.append(
        "<p><strong>Assuming the federal law covers you.</strong> The NLRA "
        "covers private-sector workers only. If you work for the government, "
        "your rights come from state law, and in six states there is no "
        "bargaining right at all. <strong>Assuming dues are optional "
        "everywhere.</strong> In states without right-to-work, a union "
        "contract can require dues — except for public workers, where "
        "<em>Janus</em> makes paying voluntary nationwide. "
        "<strong>Striking without checking.</strong> A public-sector strike "
        "is illegal in most states and can cost you your job. "
        "<strong>Assuming your union must take your case.</strong> A union "
        "must represent everyone in its unit fairly, but it has discretion "
        "about which grievances to take to arbitration. <strong>Trusting old "
        "guides.</strong> Michigan, Utah, Wisconsin, Illinois, Virginia, "
        "Florida, and Nevada have all changed their rules since 2019.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Before you act — join, "
        "refuse to pay, file a complaint, or walk out — confirm your "
        "state&rsquo;s three lines below: right-to-work, bargaining, and "
        "strikes. Then use the agency link in your state&rsquo;s card if you "
        "need help.</p>"
    )
    parts.append("</div>")
    # --- Card 7: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Labor union rights in {esc(state)}</h3>")
    parts.append(
        f"<p><strong>Right-to-work?</strong> {rtw_word(e['right_to_work'])}. {esc(e['right_to_work_note'])}</p>"
    )
    parts.append(
        f"<p><strong>Can public workers bargain?</strong> {bargaining_word(e['public_bargaining'])}. {esc(e['public_bargaining_note'])}</p>"
    )
    parts.append(
        f"<p><strong>Can public workers strike?</strong> {strike_word(e['public_strike'])}. {esc(e['public_strike_note'])}</p>"
    )
    parts.append(
        f"<p><strong>Where to complain:</strong> "
        f'<a href="{esc(e["agency_url"])}" target="_blank" rel="noopener">{esc(e["agency_name"])}</a>.</p>'
    )
    if e["state_note"]:
        parts.append(f"<p>{esc(e['state_note'])}</p>")
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check the three lines "
        "above for your state. If your employer is retaliating against union "
        "activity, contact the agency linked above — and if you work for a "
        "private company, you can also file a charge with the NLRB.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Find your state&rsquo;s "
        "three answers above — right-to-work, public bargaining, and strikes. "
        "(2) If you work for a private company, remember the federal NLRA "
        "protects you in every state. (3) If you work for the government, "
        "your rights come from state law — check before you act. (4) If your "
        "employer punishes you for union activity, contact the agency in your "
        "state&rsquo;s card. (5) Remember the rules change often — confirm "
        "the current law before you rely on it.</p>"
    )
    parts.append(
        "<p><em>Sources: the official state statutes, labor agency, and "
        "labor-relations board pages linked in the research for this section, "
        "checked November 20, 2026. Union and bargaining rules have changed "
        "recently in several states — confirm the current law with your "
        "state&rsquo;s labor agency before you rely on it. This is general "
        "information, not legal advice.</em></p>"
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
            f"Labor union rights in {state}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        assert text.count(f'id="{SLUG}-in-{slug}"') == 1, f"{slug}: anchor count"
        assert text.count("<div") - before.count("<div") == 7, f"{slug}: div open delta"
        assert text.count("</div>") - before.count("</div>") == 7, f"{slug}: div close delta"
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
        '<option value="felon-voting-rights" data-anchor="felon-voting-rights">'
        "Felon voting rights (when the vote comes back, fines and fees, probation and parole, how to re-register)</option>"
    )
    assert opt_old in text, "felon-voting helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="labor-union-rights" data-anchor="labor-union-rights">'
        "Labor union rights (right-to-work, public-sector bargaining, strikes, where to complain)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="felon-voting-rights"'
    idx = text.find(card_anchor)
    assert idx != -1, "felon-voting card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="labor-union-rights">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-labor-union-rights.jpg" alt="Labor union rights" loading="lazy"></span>
          <h3>Labor Union Rights</h3>
          <p>Can you join a union? Can public workers bargain or strike? Right-to-work rules and where to get help in your state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 52 topics" in text, "show-all label not found"
    text = text.replace("Show all 52 topics", "Show all 53 topics", 1)
    show_pos = text.find("Show all 53 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">52 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("52 topics", "53 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 52->53")


def build_about():
    text = ABOUT.read_text()
    assert text.count("97 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("97 legal topics", "98 legal topics", 1))
    print("  about.html: 97 -> 98")


def state_index_t(state, slug, e):
    bits = [
        "labor union rights right-to-work collective bargaining strike",
        f"Labor union rights in {state}",
        f"right-to-work {rtw_word(e['right_to_work']).lower()} {e['right_to_work_note']}",
        f"public workers bargain {bargaining_word(e['public_bargaining']).lower()} {e['public_bargaining_note']}",
        f"public workers strike {strike_word(e['public_strike']).lower()} {e['public_strike_note']}",
        "NLRA National Labor Relations Board NLRB private sector retaliation charge",
        "Janus agency fees dues union security",
        f"{e['agency_name']}",
        f"{e['state_note'] or ''}",
        f"{e['legal_aid_name']}",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11365, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Labor union rights in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Labor Union Rights",
            "t": (
                "labor-union-rights labor union rights Labor Union Rights? "
                "Can you join a union? Can public workers bargain or strike? "
                "Right-to-work rules and where to get help in your state. "
                "NLRA NLRB right-to-work 26 states public bargaining strikes "
                "Janus dues agency fees retaliation."
            ),
        }
    )
    assert len(idx) == 11416, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11365 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d
    assert len(states) == 50, len(states)
    data = [(k.lower(), states[k]) for k in sorted(states)]  # keys are Title Case in JSON; page files are lowercase
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "right_to_work", "right_to_work_note", "public_bargaining",
        "public_bargaining_note", "public_strike", "public_strike_note",
        "agency_name", "agency_url", "legal_aid_name", "legal_aid_url",
        "state_note", "sources",
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
        assert e["right_to_work"] in ("yes", "no", "limited"), f"{k}: bad right_to_work"
        assert e["public_bargaining"] in ("yes", "limited", "no"), f"{k}: bad public_bargaining"
        assert e["public_strike"] in ("yes", "limited", "no"), f"{k}: bad public_strike"
        assert e["right_to_work_note"] and e["public_bargaining_note"] and e["public_strike_note"] and e["agency_name"] and e["agency_url"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"], f"{k}: empty required field"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before felon-voting-rights section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
