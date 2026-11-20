#!/usr/bin/env python3
"""Build Topic #106: Digital Assets After Death — standalone section on
all 50 state pages.

Inserts one new section per state page (before Service Animals &
Disability Access, newest-first), a contents-list entry (before the
service-animals <li>), a homepage helper option + topic card (after
Service Animals), bumps About 104 -> 105, and appends 50 state
entries + 1 helper entry to assets/search-index.json (11722 -> 11773).

Data: hidden_files/topic-research/digital-assets-after-death/all-states.json
(coordinator-merged 2026-11-20 from 5 research batches; 4 batches
recovered from the researchers' session files, NM-SC saved from the
handoff text).
URL verification 2026-11-20: 86/100 curl 200; 13 confirmed alive by
text fetch or search-result verification (CA agency, CA legal aid,
OK legal aid, ID legal aid, SD agency, TN agency, MA agency, NH
agency, MT agency, KS agency, NM agency, PA agency, RI agency);
1 replaced with a verified same-org page — AR legal aid:
arkansaslegal.org 404s (curl and fetcher) -> Legal Aid of Arkansas,
https://arlegalaid.org/ (live, crawled <1 min before the swap).
Dataset corrections by the coordinator (all verified Nov 20):
- WEST VIRGINIA legal aid lawv.net is defunct (verified in #105)
  -> legalaidwv.org.
- MASSACHUSETTS bill numbers conflicted inside the payload
  (H.4639/S.1110 in the status text vs H.1968/S.1048 in the sources);
  unsourced numbers dropped, pending-bill fact kept.
Headline counts (computed from the merged dataset): 46 states have
adopted RUFADAA (in some form); 4 have not — Delaware (own 2014 act,
12 Del. C. 5001-5007) and Louisiana (own 2014 law, La. Code Civ. P.
art. 3191) have their own earlier laws; Massachusetts has no digital-
assets act at all; Oklahoma has only a narrow 2010 law (Okla. Stat.
tit. 58, 269) covering social media and email. Custodian compliance
deadline: 60 days in 45 states, 30 days in 3 (AR, DE, LA), no
statutory deadline in 2 (MA, OK).
Spot-verifications (coordinator, Nov 20, 2026, official sources):
- OKLAHOMA non-adoption confirmed against Law Commentary citing
  NCSL: LA, OK, MA are the lone holdouts; OK's RUFADAA bill has sat
  in the House Rules Committee since Feb 4, 2020. A fourth worker's
  note claiming OK "has since adopted" was wrong and was rejected.
- MINNESOTA ch. 521A confirmed live on the Revisor site: "CHAPTER
  521A. UNIFORM FIDUCIARY ACCESS TO DIGITAL ASSETS ACT",
  521A.01-521A.19, 521A.16 custodian compliance.
- ARKANSAS 30-day deadline confirmed in the enacted act text:
  28-75-116(a), "Not later than 30 days after receipt of the
  information required under 28-75-107 - 28-75-115, a custodian
  shall comply..."
No phone numbers in the dataset.
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "digital-assets-after-death" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-digital-assets-after-death.jpg"

SLUG = "digital-assets-after-death"
TITLE = "Digital Assets After Death"
PREV_SLUG = "service-animals-disability-access"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="digital-assets-after-death-in-{slug}">Digital assets after death in {esc(state)}</h2>'
    )
    parts.append(
        "<p>When someone dies, their email, photos, cloud files, social "
        "media, and online accounts do not just open up for the family. "
        "Federal privacy law and each company&rsquo;s terms of service "
        "usually block access — even for the executor named in the will. "
        "Most states have fixed this with a law called the Revised "
        "Uniform Fiduciary Access to Digital Assets Act (RUFADAA): "
        "<strong>46 states have adopted it</strong> in some form. "
        "<strong>Delaware and Louisiana</strong> have their own earlier "
        "laws instead, and <strong>Massachusetts and Oklahoma have no "
        "RUFADAA law at all</strong>. The law draws one line that matters "
        "more than any other: a family member can usually get a "
        "<strong>catalogue</strong> of an account — who emailed whom, "
        "when — but not the <strong>content</strong> of the messages "
        "unless the person consented while alive or a court orders it. "
        "And the person who plans ahead decides everything: what you "
        "set up in an online tool beats your will, and your will beats "
        "the company&rsquo;s terms of service. The picture here is as of "
        "<strong>November 2026</strong>. This is general information, "
        "not legal advice.</p>"
    )
    # --- Card 1: catalogue vs content ---
    parts.append('<div class="card">')
    parts.append("<h3>What the family can actually get: catalogue vs. content</h3>")
    parts.append(
        "<p>Under RUFADAA, a fiduciary — the executor, trustee, agent "
        "under a power of attorney, or conservator — can get two kinds "
        "of things. First, the <strong>catalogue of electronic "
        "communications</strong>: who the person communicated with, when, "
        "and at what address — the envelope, not the letter. Second, "
        "<strong>other digital assets</strong>: photos, files, documents, "
        "and online accounts. The <strong>content</strong> of emails and "
        "private messages is different: it is disclosed only if the user "
        "consented while alive — through an online tool or in a will, "
        "trust, or power of attorney — or if a court orders it. That "
        "split comes from the federal Stored Communications Act, which "
        "bars a provider from handing over message content without the "
        "user&rsquo;s consent or a court order.</p>"
    )
    parts.append(
        "<p>To get anything, the fiduciary usually has to send the "
        "custodian — the company holding the account — a written request "
        "with a certified death certificate, proof of appointment as "
        "executor or administrator, the account identifier, and evidence "
        "linking the account to the person. The custodian then has to "
        "comply within <strong>60 days</strong> in most states — "
        "<strong>30 days in Arkansas, Delaware, and Louisiana</strong> — "
        "and may grant full access, partial access, or a copy of the "
        "assets, and may charge a reasonable administrative fee. "
        "Massachusetts and Oklahoma have no statutory deadline at all.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you are the "
        "executor, start by making an inventory of the person&rsquo;s "
        "accounts, devices, and passwords — including crypto wallets and "
        "seed phrases — then check whether they set up any online tool "
        "below before you write to a single company. A written request "
        "with the death certificate and your appointment papers is the "
        "key that opens the door; a phone call alone usually is not.</p>"
    )
    parts.append("</div>")
    # --- Card 2: the priority ladder ---
    parts.append('<div class="card">')
    parts.append("<h3>Who wins: the priority ladder</h3>")
    parts.append(
        "<p>RUFADAA fixes a clear order for who decides what happens to "
        "an account. <strong>First, the user&rsquo;s direction through "
        "the custodian&rsquo;s online tool</strong> — a setting the user "
        "can change or delete at any time. <strong>Second, a direction in "
        "the user&rsquo;s will, trust, or power of attorney.</strong> "
        "<strong>Third, the custodian&rsquo;s terms of service.</strong> "
        "An online-tool direction beats a contrary direction in a will; a "
        "will beats a contrary term of service. If the user left no "
        "direction at all, the terms of service govern, and the "
        "fiduciary gets only what the law allows by default — the "
        "catalogue and other assets, not message content.</p>"
    )
    parts.append(
        "<p>That order is exactly why the tools in the next card matter "
        "so much: they sit at the top of the ladder. A will that says "
        "&ldquo;give my daughter my email&rdquo; loses to a Google "
        "setting that says something else — so the setting and the will "
        "should agree with each other. In Delaware, Louisiana, "
        "Massachusetts, and Oklahoma there is no RUFADAA ladder at all, "
        "so the platform&rsquo;s own tools and the estate documents do "
        "even more of the work — see your state&rsquo;s card below.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> If you are planning "
        "for yourself, set the online tools first and then write matching "
        "language into your will or power of attorney — do not rely on "
        "either one alone. If you are settling someone else&rsquo;s "
        "estate, look for an online-tool direction before you assume the "
        "will controls.</p>"
    )
    parts.append("</div>")
    # --- Card 3: the platform tools ---
    parts.append('<div class="card">')
    parts.append("<h3>The three tools to set up while you are alive</h3>")
    parts.append(
        "<p><strong>Google Inactive Account Manager</strong> lets you name "
        "trusted contacts and choose what happens after a period of "
        "inactivity — who gets which data, or whether the account is "
        "deleted. <strong>Apple Legacy Contact</strong> lets a named "
        "person request access to your Apple data with an access key and "
        "a death certificate. <strong>Meta legacy contact</strong> lets a "
        "Facebook user name someone to manage a memorialized account, and "
        "Instagram memorializes accounts on request with proof of death. "
        "These are the most reliable way to arrange access in advance — "
        "especially in the four states without RUFADAA, where they are "
        "often the only route that works without a court order.</p>"
    )
    parts.append(
        "<p>No tool hands over your passwords, and no tool lets the named "
        "person log in as you or read your private "
        "messages without your consent. They are a controlled handover, "
        "not a spare key. Each platform has its own request form and "
        "proof requirements, and each will still ask for a death "
        "certificate.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Set all three up "
        "today if you use the services — it takes a few minutes each, "
        "and it is the single most useful thing on this page. Tell the "
        "person you named, and tell them where your access key or "
        "instructions are kept. Then put the same authority in your will "
        "or power of attorney so the documents agree.</p>"
    )
    parts.append("</div>")
    # --- Card 4: set it up now ---
    parts.append('<div class="card">')
    parts.append("<h3>If you are planning for yourself: do it now, on paper too</h3>")
    parts.append(
        "<p>A password manager shared with a trusted person, a written "
        "inventory of accounts kept with your will, and express "
        "digital-asset authority in your will, trust, and durable power "
        "of attorney will do more than any law can. Some states require "
        "the power of attorney to <em>expressly</em> grant digital-asset "
        "authority — a general grant may not be enough — and Wisconsin "
        "even recognizes a separate written notarized consent instrument "
        "for message content. Crypto is the sharpest edge: if nobody has "
        "the seed phrase or private key, the coins are gone for good, and "
        "no court order can recover them.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Make the "
        "inventory — every account, device, password manager, and crypto "
        "wallet, with seed phrases stored somewhere safe at home. (2) Set "
        "up the three platform tools above. (3) Put express digital-asset "
        "authority in your will, trust, and power of attorney, naming who "
        "may access which accounts. (4) Tell that person where the "
        "inventory is. Do not put passwords in the will itself — a will "
        "becomes a public court record.</p>"
    )
    parts.append("</div>")
    # --- Card 5: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Digital assets in {esc(state)}</h3>")
    parts.append(f"<p><strong>The law:</strong> {esc(e['rufada_status'])}</p>")
    parts.append(f"<p><strong>What a fiduciary can get:</strong> {esc(e['custodian_access'])}</p>")
    parts.append(f"<p><strong>Who decides:</strong> {esc(e['user_direction'])}</p>")
    parts.append(f"<p><strong>Terms of service:</strong> {esc(e['terms_of_service'])}</p>")
    parts.append(f"<p><strong>The statute:</strong> {esc(e['state_statute'])}</p>")
    if e["state_note"]:
        parts.append(f"<p>{esc(e['state_note'])}</p>")
    parts.append(
        f"<p><strong>Who to contact:</strong> "
        f'<a href="{esc(e["agency_url"])}" target="_blank" rel="noopener">{esc(e["agency_name"])}</a>.</p>'
    )
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>.</p>'
    )
    parts.append(
        f"<p><strong>What to do:</strong> {esc(e['what_to_do'])}</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) If you are the "
        "executor, inventory the accounts and devices first, then check "
        "for an online-tool or legacy-contact designation before writing "
        "to any company. (2) Send each custodian a written request with a "
        "certified death certificate and proof of appointment — and note "
        "the deadline: 60 days in most states, 30 days in Arkansas, "
        "Delaware, and Louisiana. (3) If a custodian refuses or the "
        "content of messages is needed, ask the court in your state&rsquo;s "
        "card above for an order. (4) If you are planning for yourself, "
        "set up the three platform tools and put express digital-asset "
        "authority in your will and power of attorney today.</p>"
    )
    parts.append(
        "<p><em>Sources: the official state digital-assets statutes, "
        "state attorneys general and legal aid organizations linked in "
        "the research for this section, checked November 20, 2026. "
        "Forty-six states have adopted the Revised Uniform Fiduciary "
        "Access to Digital Assets Act; Delaware and Louisiana have their "
        "own earlier laws, and Massachusetts and Oklahoma have no "
        "RUFADAA law. Confirm the current law with a local attorney "
        "before you rely on it. This is general information, not legal "
        "advice.</em></p>"
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
            f"Digital assets in {state}</a></li>\n"
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
        '<option value="service-animals-disability-access" data-anchor="service-animals-disability-access">'
        "Service animals &amp; disability access (ADA) — what counts as a service animal, the two questions a business may ask, emotional support animals, and faking one</option>"
    )
    assert opt_old in text, "service-animals helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="digital-assets-after-death" data-anchor="digital-assets-after-death">'
        "Digital assets after death — who can get into your email, photos, and accounts when you die, and how to leave access behind</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    card_anchor = 'data-topic="service-animals-disability-access"'
    idx = text.find(card_anchor)
    assert idx != -1, "service-animals card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="digital-assets-after-death">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-digital-assets-after-death.jpg" alt="Digital Assets After Death" loading="lazy"></span>
          <h3>Digital Assets After Death</h3>
          <p>When someone dies, their email, photos, and online accounts don&rsquo;t just open for the family. Most states have a law — RUFADAA — that decides who can get in, what they can see, and what a will or an online setting can change. Here&rsquo;s how it works in your state.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 59 topics" in text, "show-all label not found"
    text = text.replace("Show all 59 topics", "Show all 60 topics", 1)
    show_pos = text.find("Show all 60 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">59 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("59 topics", "60 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 59->60")


def build_about():
    text = ABOUT.read_text()
    assert text.count("104 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("104 legal topics", "105 legal topics", 1))
    print("  about.html: 104 -> 105")


def state_index_t(state, slug, e):
    bits = [
        "digital assets after death RUFADAA fiduciary access email photos accounts",
        f"Digital assets after death in {state}",
        f"the law {e['rufada_status']}",
        f"what a fiduciary can get {e['custodian_access']}",
        f"who decides {e['user_direction']}",
        f"terms of service {e['terms_of_service']}",
        f"{e['state_statute']}",
        f"{e['agency_name']}",
        f"{e['state_note'] or ''}",
        f"{e['legal_aid_name']}",
        "Google Inactive Account Manager Apple Legacy Contact Meta legacy contact catalogue content of electronic communications 60 days",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11722, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Digital assets after death in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Digital Assets After Death",
            "t": (
                "digital-assets-after-death Digital Assets After Death? "
                "When someone dies, their email, photos, and online accounts don't just open for the family. "
                "Most states have a law — RUFADAA — that decides who can get in, what they can see, and what a "
                "will or an online setting can change. Here's how it works in your state. "
                "RUFADAA fiduciary access digital assets catalogue content of electronic communications "
                "Google Inactive Account Manager Apple Legacy Contact Meta legacy contact online tool will trust "
                "power of attorney terms of service 60 days."
            ),
        }
    )
    assert len(idx) == 11773, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11722 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    assert len(d) == 50, len(d)
    data = [(k, d[k]) for k in sorted(d)]  # keys already lowercase
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "rufada_status", "custodian_access", "user_direction",
        "terms_of_service", "platform_tools", "what_to_do",
        "state_statute", "agency_name", "agency_url", "legal_aid_name",
        "legal_aid_url", "state_note", "sources",
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
        assert e["rufada_status"] and e["custodian_access"] and e["user_direction"] and e["terms_of_service"] and e["what_to_do"] and e["state_statute"] and e["agency_name"] and e["agency_url"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"], f"{k}: empty required field"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before service-animals-disability-access section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
