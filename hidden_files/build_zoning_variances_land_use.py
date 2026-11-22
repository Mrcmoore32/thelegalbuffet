#!/usr/bin/env python3
"""Build Topic #101: Zoning, Variances & Land Use — standalone section on
all 50 state pages.

Inserts one new section per state page (before Firearm Rights
Restoration, newest-first), a contents-list entry (before the
firearm-rights-restoration <li>), a homepage helper option + topic
card (after Firearm Rights Restoration), bumps About 99 -> 100, and
appends 50 state entries + 1 helper entry to
assets/search-index.json (11467 -> 11518).

Data: hidden_files/topic-research/zoning-variances-land-use/all-states.json
(coordinator-merged 2026-11-20 from 5 research batches; keys lowercased
at merge. All 100 agency + legal-aid URLs checked: 87 curl 200, the
rest resolved via text fetch or researcher live opens; bot-filtered
official sites (AK commerce.alaska.gov, ID idahocities.org, KS lkm.org,
MS mmlonline.com, RI planning.ri.gov) confirmed live via search crawl
or text fetch. Coordinator resolutions: 25 null agency URLs filled
with verified municipal-league / state-agency homepages (MA mma.org,
MI mml.org, MN lmc.org land-use-variances page, MS mmlonline.com,
MO mocities.com, MT mtleague.org, NE lonm.org, NV nvleague.com —
.com not .org, NH nhmunicipal.org, NJ njlm.org, OK oml.org,
OR oregon.gov/lcd, PA dced.pa.gov community-planning page,
RI planning.ri.gov, SC masc.sc, AL almonline.org,
AK commerce.alaska.gov/web/dcra/, AZ azleague.org,
AR armunileague.org — arml.org redirects there, CA lci.ca.gov,
ID idahocities.org, IL iml.org, IA iowaleague.org, KS lkm.org,
LA lma.org); VT agency PDF link replaced with vlct.org homepage;
DE agency PDF replaced with stateplanning.delaware.gov homepage;
KY agency PDF replaced with klc.org homepage.
Headline counts: variance standard hardship 25 / practical-difficulty 2
(CA, MN) / varies 23; nonconforming use protected 27 / limited 4
(CA, LA, OK, SC) / varies 19; appeal deadline 30 days in 28 states,
10 days in MS and TX, 21 days in OR and WA, not stated in the statute
in 5 states (AK, AR, MN, NM, OK). No phone numbers in the dataset.
Key verifications: MN practical-difficulties test under Minn. Stat.
section 462.357 subd. 6, adopted by the 2011 amendment (2011 Minn.
Laws ch. 19) after Krummenacher v. City of Minnetonka; NC Chapter
160D recodification eff. Jan 1, 2021; OR LUBA appeal under ORS
197.830, 21-day deadline; WV 30-day appeal deadline confirmed in
the statute itself, W. Va. Code section 8A-9-1(b) (petition for writ
of certiorari to circuit court within 30 days); WY 30-day deadline
confirmed in W.R.A.P. 12.04(a), quoted verbatim in Chevron U.S.A.
v. Dept. of Revenue, 2007 WY 62 (petition for review within 30 days
after service of the final decision).
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "zoning-variances-land-use" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-zoning-variances-land-use.jpg"

SLUG = "zoning-variances-land-use"
TITLE = "Zoning, Variances & Land Use"
PREV_SLUG = "firearm-rights-restoration"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def standard_word(v):
    return {
        "hardship": "Unnecessary hardship",
        "practical-difficulty": "Practical difficulties",
        "varies": "Varies — no single statewide test",
    }.get(v, v)


def nonconforming_word(v):
    return {
        "protected": "Protected — the use may continue",
        "limited": "Limited — protection has conditions",
        "varies": "Varies — it depends on local law",
    }.get(v, v)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="zoning-variances-land-use-in-{slug}">Zoning, variances &amp; land use in {esc(state)}</h2>'
    )
    parts.append(
        "<p>Zoning decides what you can build on your land and how you can "
        "use it — how close to the lot line, how tall, and whether a home, "
        "a shop, or a rental is allowed there at all. When the rules block "
        "what you need, a <strong>variance</strong> is the way to ask for "
        "an exception. When your use was legal before the rules changed, "
        "that is a <strong>nonconforming use</strong>, and it usually gets "
        "to stay — with limits. And when the board says no, you can "
        "usually appeal, but the deadline is short: <strong>30 days in 28 "
        "states, and as little as 10 days in Mississippi and Texas</strong>. "
        "The picture here is as of <strong>November 2026</strong>. This is "
        "general information, not legal advice.</p>"
    )
    # --- Card 1: what a variance is ---
    parts.append('<div class="card">')
    parts.append("<h3>What a variance is — and what it is not</h3>")
    parts.append(
        "<p>A variance is permission to break one zoning rule for one lot "
        "— usually a <strong>dimensional</strong> rule, like a setback, a "
        "height limit, or a lot-size minimum. It is not a rezoning, and it "
        "is not a permit to use the land for something the zone forbids: "
        "a <strong>use variance</strong> — asking to run a business in a "
        "residential zone, for example — is barred outright in many states, "
        "including Minnesota, where the statute says a city may not permit "
        "by variance any use that is not allowed in the district.</p>"
    )
    parts.append(
        "<p>The test you must meet depends on the state. In <strong>25 "
        "states</strong> you must show <strong>unnecessary hardship</strong> "
        "— that the rule, applied to your lot, causes a hardship because "
        "of something unique about the property, not something you caused. "
        "In <strong>California and Minnesota</strong> the test is the "
        "looser <strong>practical difficulties</strong> standard. In the "
        "other <strong>23 states</strong> there is no single statewide "
        "test: the county or city ordinance sets its own standard, so the "
        "exact words that decide your case are in your local ordinance, "
        "not in a state statute.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Read your state&rsquo;s "
        "test in the card below, then get your local zoning ordinance and "
        "find the variance section — that is the document the board will "
        "actually apply to your lot.</p>"
    )
    parts.append("</div>")
    # --- Card 2: the process ---
    parts.append('<div class="card">')
    parts.append("<h3>How it usually works</h3>")
    parts.append(
        "<p>You apply to the local board of adjustment (sometimes called "
        "the zoning board of appeals), which holds a public hearing and "
        "must make written findings — a reasoned decision, not just a "
        "vote. The board can attach conditions, like a fence or a limit on "
        "hours, to protect neighbors. A variance runs with the land, so it "
        "usually survives when the property is sold, but it can be lost if "
        "you do not use it or do not follow its conditions.</p>"
    )
    parts.append(
        "<p>If the board denies you, appeal fast. The deadline to appeal a "
        "variance decision is <strong>30 days in 28 states</strong>. It is "
        "<strong>21 days in Oregon and Washington</strong> and "
        "<strong>10 days in Mississippi and Texas</strong>. In 5 states "
        "(Alaska, Arkansas, Minnesota, New Mexico, and Oklahoma) no "
        "deadline is stated in the statute itself, so the deadline comes "
        "from the local ordinance or the court rules — check both before "
        "you assume you have time.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Mark the deadline the "
        "day the decision is issued, not the day you read it. Miss it and "
        "the court will not hear you, no matter how good your case is.</p>"
    )
    parts.append("</div>")
    # --- Card 3: nonconforming uses ---
    parts.append('<div class="card">')
    parts.append("<h3>The use that was there first</h3>")
    parts.append(
        "<p>If your home, shop, or building was legal when it was built "
        "and the zoning changed later, it is a <strong>nonconforming "
        "use</strong> — often called grandfathered. In <strong>27 "
        "states</strong> that use is protected and may continue. In "
        "<strong>4 states (California, Louisiana, Oklahoma, and South "
        "Carolina)</strong> protection is limited — for example, the use "
        "may have to end after a set time or may not be expanded. In the "
        "other <strong>19 states</strong> it depends on local law.</p>"
    )
    parts.append(
        "<p>Protection is not forever. In most places a nonconforming use "
        "ends if you abandon it, if you change it to a different use, or "
        "if the building is badly damaged or destroyed and you do not "
        "rebuild within the time the ordinance allows. Expanding a "
        "nonconforming use — a bigger building, more units, longer hours — "
        "usually needs its own approval.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Before you buy a "
        "property with a nonconforming use, or before you stop using it "
        "for a while, ask the zoning office in writing whether the use is "
        "protected and what would end that protection. Get the answer "
        "before you spend money.</p>"
    )
    parts.append("</div>")
    # --- Card 4: traps ---
    parts.append('<div class="card">')
    parts.append("<h3>Traps: do not get caught by these</h3>")
    parts.append(
        "<p><strong>Assuming a variance lets you use the land for a "
        "forbidden purpose.</strong> It almost never does — a variance "
        "bends a dimensional rule, not the allowed-use list. "
        "<strong>Assuming your neighbor&rsquo;s variance means yours is "
        "automatic.</strong> Each lot is decided on its own facts, and a "
        "hardship you created yourself — building first, then asking — "
        "counts against you in most states. <strong>Assuming the city or "
        "county can zone everywhere.</strong> In Texas, a city cannot zone "
        "land in its extraterritorial jurisdiction, and Texas counties have "
        "no general zoning power at all. <strong>Assuming local zoning is "
        "the only approval.</strong> In Vermont, a large project also "
        "needs a separate state Act 250 land-use permit, judged against "
        "ten criteria. <strong>Assuming you have months to appeal.</strong> "
        "Ten days in Mississippi and Texas is less than two weeks.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check three things "
        "before you apply or buy: the local ordinance&rsquo;s variance "
        "test, the appeal deadline, and whether any separate state permit "
        "applies to your project.</p>"
    )
    parts.append("</div>")
    # --- Card 5: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Zoning, variances &amp; land use in {esc(state)}</h3>")
    parts.append(
        f"<p><strong>The variance test:</strong> {standard_word(e['variance_standard'])}. {esc(e['variance_standard_note'])}</p>"
    )
    parts.append(
        f"<p><strong>How to apply:</strong> {esc(e['variance_process'])}</p>"
    )
    parts.append(
        f"<p><strong>If you are denied — appeal:</strong> {esc(e['appeal_route'])} <strong>Deadline:</strong> {esc(e['appeal_deadline'])}</p>"
    )
    parts.append(
        f"<p><strong>Nonconforming use:</strong> {nonconforming_word(e['nonconforming_use'])}. {esc(e['nonconforming_note'])}</p>"
    )
    parts.append(
        f"<p><strong>The law:</strong> {esc(e['statute_name'])} — {esc(e['statute_cite'])}</p>"
    )
    parts.append(
        f"<p><strong>Where to learn more:</strong> "
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
        "linked above for your local ordinance and application forms. If "
        "the board denies you, calendar the appeal deadline the same day. "
        "If the amount at stake is large — a home, a business, a "
        "development — talk to the legal aid above or a land-use lawyer "
        "before the hearing, not after.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Get your local "
        "zoning ordinance and find the variance section — that is the test "
        "the board will apply. (2) Apply to the board of adjustment with "
        "evidence of your lot&rsquo;s unique conditions. (3) If denied, "
        "appeal before the deadline in your state&rsquo;s card above. (4) "
        "Before buying a nonconforming property, confirm in writing that "
        "the use is protected. (5) Check whether a separate state permit "
        "applies to your project.</p>"
    )
    parts.append(
        "<p><em>Sources: the official state statutes, planning agencies, "
        "and municipal leagues linked in the research for this section, "
        "checked November 20, 2026. Zoning rules change — confirm the "
        "current ordinance with your city or county before you rely on "
        "it. This is general information, not legal advice.</em></p>"
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
            f"Zoning, variances &amp; land use in {state}</a></li>\n"
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
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert SLUG not in helper_part, "index already has helper option"
    assert f'data-topic="{SLUG}"' not in text, "index already has card"
    opt_old = (
        '<option value="firearm-rights-restoration" data-anchor="firearm-rights-restoration">'
        "Firearm rights restoration (pardons, court petitions, expungement, waiting periods, the federal warning)</option>"
    )
    assert opt_old in text, "firearm-rights helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="zoning-variances-land-use" data-anchor="zoning-variances-land-use">'
        "Zoning, variances &amp; land use (variances, nonconforming uses, appeals, deadlines)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="firearm-rights-restoration"'
    idx = text.find(card_anchor)
    assert idx != -1, "firearm-rights card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="zoning-variances-land-use">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-zoning-variances-land-use.jpg" alt="Zoning, variances and land use" loading="lazy"></span>
          <h3>Zoning, Variances &amp; Land Use</h3>
          <p>Your city says you can&apos;t build that shed, fence, or addition. How to ask for a variance, what counts as hardship, and how fast you must appeal &mdash; state by state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 54 topics" in text, "show-all label not found"
    text = text.replace("Show all 54 topics", "Show all 55 topics", 1)
    show_pos = text.find("Show all 55 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">54 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("54 topics", "55 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 54->55")


def build_about():
    text = ABOUT.read_text()
    assert text.count("99 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("99 legal topics", "100 legal topics", 1))
    print("  about.html: 99 -> 100")


def state_index_t(state, slug, e):
    bits = [
        "zoning variances land use variance nonconforming use grandfathered",
        f"Zoning, variances & land use in {state}",
        f"variance test {standard_word(e['variance_standard']).lower()} {e['variance_standard_note']}",
        f"how to apply {e['variance_process']}",
        f"appeal {e['appeal_route']} deadline {e['appeal_deadline']}",
        f"nonconforming use {nonconforming_word(e['nonconforming_use']).lower()} {e['nonconforming_note']}",
        f"{e['statute_name']} {e['statute_cite']}",
        f"{e['agency_name']}",
        f"{e['state_note'] or ''}",
        f"{e['legal_aid_name']}",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11467, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Zoning, variances & land use in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Zoning, Variances & Land Use",
            "t": (
                "zoning-variances-land-use Zoning, Variances & Land Use? "
                "Your city says you can't build that shed, fence, or addition. How to ask for a variance, "
                "what counts as hardship, and how fast you must appeal — state by state. "
                "variance unnecessary hardship practical difficulties nonconforming use grandfathered "
                "board of adjustment zoning board of appeals appeal deadline."
            ),
        }
    )
    assert len(idx) == 11518, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11467 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    assert len(d) == 50, len(d)
    data = [(k, d[k]) for k in sorted(d)]  # keys already lowercase
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "variance_standard", "variance_standard_note", "variance_process",
        "appeal_route", "appeal_deadline", "nonconforming_use",
        "nonconforming_note", "statute_name", "statute_cite", "agency_name",
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
        assert e["variance_standard"] in ("hardship", "practical-difficulty", "varies"), f"{k}: bad variance_standard"
        assert e["nonconforming_use"] in ("protected", "limited", "varies"), f"{k}: bad nonconforming_use"
        assert e["variance_standard_note"] and e["variance_process"] and e["appeal_route"] and e["appeal_deadline"] and e["nonconforming_note"] and e["statute_name"] and e["statute_cite"] and e["agency_name"] and e["agency_url"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"], f"{k}: empty required field"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before firearm-rights-restoration section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
