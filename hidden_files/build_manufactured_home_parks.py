#!/usr/bin/env python3
"""Build Topic #80: Manufactured-home parks — standalone section on all 50
state pages.

Inserts one new section per state page (before the Student loans section,
newest-first), a contents-list entry, a homepage helper option + topic
card (second grid, after Student loans), bumps About 78 -> 79, and
appends 50 state entries + 1 helper entry to assets/search-index.json
(10396 -> 10447).

Data: hidden_files/topic-research/manufactured-home-parks/all-states.json
(coordinator-written; see make_dataset.py for the source trail).

Coordinator verification before the build (Nov 14, 2026):
- State cards (park act, rent, closure, eviction, sale) and the official
  source link are reused verbatim from the buried "Manufactured-home
  parks" block inside Tenant Rights on each state page, which was built
  from official state sources. The buried block stays where it is; this
  section goes further (park rules, retaliation, sale/closure clocks,
  help) and cross-references Tenant Rights instead of duplicating it.
- Link sweep Nov 14, 2026: all 50 official links checked — 43 HTTP 200,
  3 HTTP 403 from official .gov bot filters (CO, MA, MT — kept per
  precedent), 4 curl-000 confirmed live by text fetch the same day
  (AK, CA, CT, IL).
- Headline figures spot-verified against the official source before
  shipping: AK AS 34.03.225 (270-day change-of-use notice, May 1-Oct 15
  quit window, closed eviction list); CA Civ. Code 798.30 (90-day rent
  notice) and 798.56(g) (60-day permit notice, 6 months after permits,
  12 months if no permits); IL 765 ILCS 745/9 (90-day rent notice on
  renewal); OR ORS 90.600/90.645 (90-day notice, rent cap, 365-day
  closure, $6,000/$8,000/$10,000 relocation); WA RCW 59.20.090(2)
  (3-month rent notice), 59.20.080(1)(e) (12-month closure notice); MN
  327C.06 (60-day rent notice, max two increases per 12 months),
  327C.095 (9-month closure statement).
- Retaliation verified against the official statute for 14 states: AZ
  A.R.S. 33-1491 (6-month presumption), CA Civ. Code 1942.5 (180 days),
  CO C.R.S. 38-12-212.5 (120-day presumption), DE 25 Del. C. 7019
  (90-day presumption), FL 723.0615, ID Idaho Code 55-2015, ME 10 M.R.S.
  9097(1-A) + 14 M.R.S. 6001(3) (6-month presumption), MA G.L. c. 186
  section 18 (6-month presumption), MN 327C.12 (90-day burden shift),
  NH RSA 540:13-a/13-b (6-month presumption), NJ N.J.S.A. 2A:42-10.10
  and 2A:42-10.12, NV NRS 118B.210, OR ORS 90.765, WA RCW 59.20.070(5)
  and 59.20.075 (120-day presumption). The other 36 states get a
  claim-free fallback, not an invented rule. VT is deliberately
  claim-free: its general retaliation rule (9 V.S.A. 4465) sits in the
  general rental act, and the state's own handbook says park-lot
  residents are covered by the park law (10 V.S.A. ch. 153) instead.
- No phone numbers are printed anywhere in this topic. No state
  manufactured-housing association is named: none was verified against
  an official source for any state in this build, and the section says
  so instead of inventing one.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "manufactured-home-parks" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"

TOPIC = "manufactured-home-parks"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(s):
    state = s["state"]
    slug = s["slug"]
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="manufactured-home-parks-in-{slug}">Manufactured-Home Parks in {esc(state)}</h2>'
    )
    parts.append(
        "<p>If you own a manufactured or mobile home but rent the lot under "
        "it, you live under two rulebooks at once \u2014 and the park "
        "rulebook is the one that decides whether you can stay. Your home "
        "is expensive to move \u2014 often $5,000 to $15,000 or more, and "
        "some homes cannot survive a move at all \u2014 so losing the lot "
        "can mean losing the home. This section is the park rulebook for "
        + esc(state) + ": the state park act, lot-rent increases, park "
        "rules and evictions, what happens if the park is sold or closes, "
        "and what to do if the park retaliates for a complaint. The general "
        "rules for renters \u2014 deposits, repairs, and the eviction "
        "process for a rented home \u2014 are in the Tenant Rights section "
        "on this page; this section is about the lot under a home you own. "
        "Checked <strong>November 14, 2026</strong>. This is general "
        "information, not legal advice.</p>"
    )
    # --- Own the home, rent the lot ---
    parts.append('<div class="card">')
    parts.append("<h3>Own the home, rent the lot</h3>")
    parts.append(
        "<p>Your home is expensive to move \u2014 often $5,000 to $15,000 "
        "or more, and some homes cannot survive a move at all \u2014 so "
        "losing the lot can mean losing the home. That is why your "
        "<strong>lot lease and the park rules are the most important papers "
        "you own</strong> after the title. Read them before you buy a home "
        "in a park, get every promise about rent and rules in writing, and "
        "keep copies of every notice the park sends you. The protections in "
        "the " + esc(state) + " cards below come from state law; where your "
        "lease promises more, the lease promise counts too.</p>"
    )
    parts.append(
        "<p>Before you buy a home in a park, ask for the lot lease, the "
        "park rules, and the last two rent-increase notices, and check them "
        "against the " + esc(state) + " cards below \u2014 especially the "
        "rent notice period, the eviction grounds, and the closure rules. "
        "If the seller or the park will not show you the papers, walk away: "
        "the lot, not the home, is what you are really buying into.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Find your lot lease "
        "and park rules today and keep them with your title. If you are "
        "buying, get the lease, the rules, and the recent rent history in "
        "writing before you sign anything.</p>"
    )
    parts.append("</div>")
    # --- The four fights ---
    parts.append('<div class="card">')
    parts.append("<h3>The four fights that matter</h3>")
    parts.append(
        "<p><strong>(1) Lot-rent increases</strong> \u2014 most park laws "
        "require long written notice, and a few states now cap the amount. "
        "<strong>(2) Eviction</strong> \u2014 in most park acts the owner "
        "may evict only for a short list of reasons (\u201cgood "
        "cause\u201d), not for any reason or no reason. <strong>(3) "
        "Closure or conversion</strong> \u2014 closing a park usually "
        "requires many months of notice, and some states make the owner "
        "help pay to move your home. <strong>(4) Selling</strong> \u2014 you "
        "generally may sell your home in place, and in a growing number of "
        "states residents get a chance to buy the park itself when it is "
        "sold. Each fight has its own " + esc(state) + " card below.</p>"
    )
    parts.append("</div>")
    # --- Rent increases ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Lot-rent increases in {esc(state)}</h3>")
    parts.append(f"<p>{esc(s['rent'])}</p>")
    parts.append(
        "<p>Where no cap applies, the amount of an increase is set by your "
        "lease and the local market \u2014 which makes the notice period "
        "the thing to watch. An increase that arrives with too little "
        "notice, or only by word of mouth, is not valid under the notice "
        "rules above: say so in writing, keep a copy, and keep paying the "
        "old rent while you dispute it. A rent increase that lands right "
        "after you complained may be retaliation instead \u2014 see the "
        "retaliation card below.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> When a rent-increase "
        "notice arrives, check the date on it against the notice period in "
        "the card above. If the notice was short, late, or only verbal, "
        "object in writing the same week and keep a copy.</p>"
    )
    parts.append("</div>")
    # --- Park rules and evictions ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Park rules and evictions in {esc(state)}</h3>")
    parts.append(
        "<p>Park rules must be in writing \u2014 in your rental agreement "
        "or given to you in writing \u2014 and they must be reasonable and "
        "applied the same way to everyone in the park. A rule that "
        "contradicts " + esc(state) + "'s park law is usually "
        "unenforceable, and the park cannot use a rule to take away a right "
        "the act gives you, such as selling your home in place. What a park "
        "commonly may require: keeping your home and lot maintained, "
        "following reasonable appearance and safety rules, and paying the "
        "charges your agreement lists. What it commonly may not do: change "
        "the rules to punish one resident, charge a fee the act forbids, or "
        "require you to buy goods or services from the park or its chosen "
        "seller.</p>"
    )
    parts.append(f"<p>{esc(s['eviction'])}</p>")
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you get a rule-"
        "violation or termination notice, read it against the grounds "
        "above and check whether the park gave you the notice and the "
        "chance to fix it that the law requires. Get legal aid involved "
        "before the deadline in the notice runs out \u2014 eviction "
        "deadlines are short, and missing one is hard to undo.</p>"
    )
    parts.append("</div>")
    # --- Sale or closure ---
    parts.append('<div class="card">')
    parts.append(f"<h3>If the park is sold or closing in {esc(state)}</h3>")
    parts.append(f"<p>{esc(s['closure'])}</p>")
    if s.get("sale"):
        parts.append(f"<p>{esc(s['sale'])}</p>")
    else:
        parts.append(
            f"<p>No resident-purchase right is printed for {esc(state)} in "
            f"this section \u2014 in the sources checked, no verified right "
            f"for residents to match a buyer's offer and buy the park when "
            f"it is sold was found for {esc(state)}. You can still sell "
            f"your own home in place under the general rules in the Tenant "
            f"Rights section on this page, and the closure notice rules in "
            f"the card above still apply. If a sale notice arrives, ask "
            f"legal aid whether a purchase right exists that this section "
            f"missed.</p>"
        )
    parts.append(
        "<p>Resident purchase windows are measured in <strong>days, not "
        "months</strong> \u2014 commonly 45 to 120 days from the "
        "owner\u2019s notice \u2014 and relocation help usually has to be "
        "claimed, not waited for. If a sale or closure notice arrives: "
        "<strong>(1)</strong> note the date you received it and keep the "
        "envelope; <strong>(2)</strong> contact your homeowners\u2019 "
        "association the same week \u2014 purchase rights usually run "
        "through an association, and if none exists, the notice itself "
        "often explains how to form one; <strong>(3)</strong> call the "
        "official source below and your state Attorney General\u2019s "
        "office and ask what deadlines apply to you; "
        "<strong>(4)</strong> do not sign a buyout, waiver, or new lease "
        "at the door without advice \u2014 legal aid (see the Free Legal "
        "Help section) reviews these free.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Calendar every deadline "
        "in any sale or closure notice the day it arrives \u2014 in park "
        "law, missing a short window (a purchase offer, a relocation "
        "claim, an objection) usually cannot be undone.</p>"
    )
    parts.append("</div>")
    # --- Retaliation ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Retaliation in {esc(state)}</h3>")
    parts.append(
        "<p>Retaliation is when the park punishes you for standing up for "
        "your rights: raising your lot rent, cutting services, changing the "
        "rules against you, refusing to renew, or starting an eviction "
        "\u2014 right after you complained about the park, reported a code "
        "violation, joined a residents\u2019 association, or went to "
        "court. The timing is the evidence: the closer the park\u2019s move "
        "follows your complaint, the harder it is for the park to call it a "
        "coincidence.</p>"
    )
    if s.get("retaliation"):
        parts.append(f"<p>{esc(s['retaliation'])}</p>")
    else:
        parts.append(
            f"<p>No park-specific retaliation rule is printed for "
            f"{esc(state)} in this section. That does not mean the park can "
            f"punish you for complaining \u2014 {esc(state)}\u2019s general "
            f"landlord-tenant law may still protect you, and in many states "
            f"retaliation is a defense to eviction. If a rent increase, "
            f"service cut, or eviction notice follows a complaint, write "
            f"down the date of the complaint and the date of the park\u2019s "
            f"action, keep copies of both, and ask legal aid (see the Free "
            f"Legal Help section on this page) whether {esc(state)}\u2019s "
            f"general retaliation rule covers park tenancies.</p>"
        )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Complain in writing, "
        "not just in person, and keep a dated copy of every complaint. If "
        "the park moves against you within weeks of a complaint, write down "
        "both dates, keep the notice, and take the paper trail to legal aid "
        "before you answer the notice.</p>"
    )
    parts.append("</div>")
    # --- State park act ---
    parts.append('<div class="card">')
    parts.append(f"<h3>The law that governs your lot in {esc(state)}</h3>")
    parts.append(f"<p>{esc(s['law'])}</p>")
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Read the official "
        "source linked below before you act on a deadline \u2014 statutes "
        "change, and the official text is what a court will read.</p>"
    )
    parts.append("</div>")
    # --- Help ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Help in {esc(state)}</h3>")
    parts.append(
        "<p>If the park breaks the rules above: <strong>(1)</strong> "
        "complain in writing to the park owner or manager, keep a copy, and "
        "keep every notice the park sends you. <strong>(2)</strong> Take "
        "the paper trail to the official source linked below \u2014 park "
        "complaints in many states go to the attorney general\u2019s office, "
        "the housing agency, or the courts, and the official page is where "
        "to start. <strong>(3)</strong> Get free help from legal aid "
        "\u2014 see the Free Legal Help section on this page; legal aid "
        "reviews sale and closure notices free, and the clocks on those are "
        "short. <strong>(4)</strong> Do not sign a buyout, waiver, or new "
        "lease at the door without advice. No state manufactured-housing "
        "association is named here because none was verified against an "
        "official source for " + esc(state) + " in this build \u2014 the "
        "official source below is the verified starting point.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> One call solves most "
        "problems: the park owner in writing first, then the official "
        "source below, then legal aid if the park will not fix it.</p>"
    )
    parts.append("</div>")
    # --- Official links ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Official links in {esc(state)}</h3>")
    parts.append("<ul>")
    parts.append(
        f"<li><a href=\"{esc(s['link'])}\" target=\"_blank\" "
        f"rel=\"noopener\">{esc(s['link_label'])}</a></li>"
    )
    parts.append("</ul>")
    parts.append("</div>")
    # --- Do this now ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Find your lot lease "
        "and park rules and check them against the " + esc(state) + " cards "
        "above \u2014 a rule that contradicts state law is usually "
        "unenforceable. (2) Join your park\u2019s homeowners\u2019 "
        "association, or keep its contact information with your lease; it is "
        "the vehicle for purchase rights and the fastest warning system for "
        "sales and closures. (3) Calendar every deadline in any notice you "
        "receive the day it arrives \u2014 in park law, missing a short "
        "window (a purchase offer, a relocation claim, an objection) usually "
        "cannot be undone. (4) If the park breaks the rules above, complain "
        "in writing to the official source on this page and keep a copy; a "
        "paper trail is what enforcement runs on.</p>"
    )
    parts.append(
        "<p><em>Sources: the official " + esc(state) + " source linked "
        "above, checked November 14, 2026, and the manufactured-home park "
        "cards in the Tenant Rights section on this page, which were built "
        "from official state sources. Laws change \u2014 confirm the current "
        "rule in the official source before you rely on a deadline. This is "
        "general information, not legal advice.</em></p>"
    )
    parts.append("</section>")
    return "\n".join(parts) + "\n"


def build_state_pages(data):
    for s in data:
        slug = s["slug"]
        path = STATES / f"{slug}.html"
        text = path.read_text()
        anchor = f"manufactured-home-parks-in-{slug}"
        assert anchor not in text, f"{slug}: anchor already present"
        # --- insert section before Student loans (newest-first) ---
        h2 = text.find(f'<h2 id="student-loans-in-{slug}">')
        assert h2 != -1, f"{slug}: student-loans h2 not found"
        sec_start = text.rfind("<section", 0, h2)
        assert sec_start != -1, f"{slug}: section start not found"
        new_section = section_html(s)
        text = text[:sec_start] + new_section + "\n" + text[sec_start:]
        # --- contents-list entry before the student-loans <li> ---
        li_pat = re.compile(
            r'(^[ \t]*<li><a href="#student-loans-in-'
            + re.escape(slug)
            + r'">.*$)',
            re.M,
        )
        m = li_pat.search(text)
        assert m, f"{slug}: student-loans contents <li> not found"
        indent = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
        new_li = (
            f'{indent}<li><a href="#manufactured-home-parks-in-{slug}">'
            f"Manufactured-Home Parks in {s['state']}</a></li>\n"
        )
        text = text[: m.start()] + new_li + text[m.start():]
        path.write_text(text)
        print(f"  {slug}: section + contents entry inserted")


def build_index():
    text = INDEX.read_text()
    helper_part = text.split("helper-topic")[1].split("</select>")[0]
    assert "manufactured-home-parks" not in helper_part, "index already has helper option"
    assert 'data-topic="manufactured-home-parks"' not in text, "index already has card"
    opt_old = (
        '<option value="student-loans" data-anchor="student-loans">'
        "Student loans (repayment, default, forgiveness)</option>"
    )
    assert opt_old in text, "student-loans helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="manufactured-home-parks" data-anchor="manufactured-home-parks">'
        "Manufactured-home parks (own the home, rent the lot)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="student-loans"'
    idx = text.find(card_anchor)
    assert idx != -1, "student-loans card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="manufactured-home-parks">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-manufactured-home-parks.jpg" alt="Manufactured-Home Parks" loading="lazy"></span>
          <h3>Manufactured-Home Parks</h3>
          <p>Own the home, rent the lot: lot-rent increases, park rules and evictions, sale and closure of the park, retaliation, and your state's park act.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 33 topics" in text, "show-all label not found"
    text = text.replace("Show all 33 topics", "Show all 34 topics", 1)
    assert '<span class="count-badge">33 topics</span>' in text
    text = text.replace(
        '<span class="count-badge">33 topics</span>',
        '<span class="count-badge">34 topics</span>',
        1,
    )
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 33->34")


def build_about():
    text = ABOUT.read_text()
    assert "78 legal topics" in text, "about count not found"
    ABOUT.write_text(text.replace("78 legal topics", "79 legal topics", 1))
    print("  about.html: 78 -> 79")


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 10396, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith("manufactured-home-parks-in-") for e in idx)
    for s in data:
        state = s["state"]
        slug = s["slug"]
        law_kw = " ".join(s["law"].split()[:25])
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"manufactured-home-parks-in-{slug}",
                "h": f"Manufactured-Home Parks in {state}",
                "t": (
                    f"Manufactured-Home Parks in {state} "
                    f"\u2014 manufactured home park mobile home park lot "
                    f"rent lot lease rent increase eviction good cause park "
                    f"rules closure conversion relocation sale in place "
                    f"resident purchase retaliation park act {law_kw} "
                    f"{state}"
                ),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Manufactured-Home Parks",
            "t": (
                "Own the home, rent the lot: lot-rent increases, park "
                "rules and evictions, sale and closure of the park, "
                "retaliation, and your state's park act."
            ),
        }
    )
    assert len(idx) == 10447, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 10396 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [states[k] for k in sorted(states)]
    slugs = [s["slug"] for s in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert all(s.get("link") and s.get("link_label") for s in data), "missing link data"
    print("building state pages...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
