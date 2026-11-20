#!/usr/bin/env python3
"""Build Topic #95: Product Liability & Defective Products — standalone
section on all 50 state pages.

Inserts one new section per state page (before Asylum, DACA & Deportation
Defense, newest-first), a contents-list entry (before the asylum <li>), a
homepage helper option + topic card (after Asylum, DACA & Deportation
Defense), bumps About 93 -> 94, and appends 50 state entries + 1 helper
entry to assets/search-index.json (11161 -> 11212).

Data: hidden_files/topic-research/product-liability-defective-products/all-states.json
(coordinator-merged 2026-11-20 from 5 research batches; all 50 legal-aid URLs
verified alive — 44 curl 200 + 6 via text fetch. Coordinator swaps for
statewide coverage: CA LAFLA -> LawHelpCA, MO LSEM -> Missouri Legal
Services (lsmo.org), NV LACSN -> Nevada Legal Services, NY legalaid.org
(stale splash page) -> The Legal Aid Society (legalaidnyc.org). Headline
facts spot-checked: AL 1-year SOL confirmed against Ala. Code § 6-5-502
text; ND/RI/AZ/AL/NH repose statutes struck down as unconstitutional,
coded null with the case named; WA 12-year rule is a rebuttable
useful-safe-life presumption, not a hard repose period, coded null.
Strict liability is "no" in only 4 states: DE, LA, NC, VA.)
"""
import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hidden_files" / "topic-research" / "product-liability-defective-products" / "all-states.json"
STATES = ROOT / "states"
INDEX = ROOT / "index.html"
ABOUT = ROOT / "about.html"
SEARCH_INDEX = ROOT / "assets" / "search-index.json"
THUMB = ROOT / "assets" / "img" / "topics" / "thumbs" / "legal-buffet-product-liability-defective-products.jpg"

SLUG = "product-liability-defective-products"
TITLE = "Product Liability & Defective Products"
PREV_SLUG = "asylum-daca-deportation-defense"


def esc(s):
    return htmlmod.escape(s or "", quote=True)


def word(v):
    return {"yes": "Yes", "no": "No"}.get(v, v)


def section_html(state, slug, e):
    parts = []
    parts.append('<section class="block" style="padding-block:0 2.5rem">')
    parts.append(
        f'<h2 id="product-liability-defective-products-in-{slug}">Product liability &amp; defective products in {esc(state)}</h2>'
    )
    parts.append(
        "<p>When a product hurts you &mdash; a drug with a hidden side effect, a "
        "car part that fails, a tool that breaks, a children&rsquo;s toy that "
        "chokes &mdash; the maker or seller may have to pay for the harm. "
        "Product liability is the area of law that covers that. This section "
        "explains the three kinds of defects, whether you have to prove the "
        "company was careless, the <strong>two deadlines</strong> that can end "
        "your claim, and what to do right after you are hurt. The picture here "
        "is as of <strong>November 2026</strong>. This is general information, "
        "not legal advice.</p>"
    )
    # --- Card 1: three kinds of defects ---
    parts.append('<div class="card">')
    parts.append("<h3>The three kinds of defects</h3>")
    parts.append(
        "<p>A product-liability claim starts with showing the product was "
        "defective in one of three ways. A <strong>manufacturing defect</strong> "
        "means one unit went wrong on the line &mdash; your bottle had a crack "
        "the others did not, your airbag had a bad part. A <strong>design "
        "defect</strong> means the whole line is unsafe as designed &mdash; every "
        "unit has the same flaw. A <strong>failure to warn</strong> means the "
        "company did not give an adequate warning or instructions about a danger "
        "it knew about, or should have known about.</p>"
    )
    parts.append(
        "<p>In every case you also have to show the defect made the product "
        "<strong>unreasonably dangerous</strong> and that it <strong>caused "
        "your injury</strong>. A product that simply did not work well, or that "
        "you used in a way it was never meant to be used, is usually not enough.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Write down what the product "
        "is, what went wrong, and how you were using it. That is the start of "
        "the defect question a lawyer will ask first.</p>"
    )
    parts.append("</div>")
    # --- Card 2: strict liability vs negligence ---
    parts.append('<div class="card">')
    parts.append("<h3>Strict liability vs. negligence: do you have to prove carelessness?</h3>")
    parts.append(
        "<p>In most states, <strong>strict liability</strong> applies: you do not "
        "have to prove the company was careless. You only have to prove the "
        "product was defective and unreasonably dangerous, and that the defect "
        "caused your injury. That matters, because a careful company can still "
        "sell a dangerous product. Check the state card below for whether "
        + esc(state)
        + " is a strict-liability state.</p>"
    )
    parts.append(
        "<p>A few states never adopted strict liability for products &mdash; "
        "Delaware, Louisiana, North Carolina, and Virginia. There, you must "
        "prove the company was <strong>negligent</strong> or broke a "
        "<strong>warranty</strong>. Louisiana has its own statute that lists "
        "exactly four ways a product can be unreasonably dangerous. Even in "
        "strict-liability states, design-defect and failure-to-warn claims often "
        "turn on a risk-utility test: was the danger greater than the cost of "
        "preventing it?</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Do not assume you have no "
        "case because the company &ldquo;did its best.&rdquo; In most states, "
        "doing its best is not a defense when the product was defective.</p>"
    )
    parts.append("</div>")
    # --- Card 3: two deadlines ---
    parts.append('<div class="card">')
    parts.append("<h3>The two deadlines: limitations and repose</h3>")
    parts.append(
        "<p>Product claims have <strong>two</strong> clocks, and missing either "
        "one ends the claim. The <strong>statute of limitations</strong> is the "
        "deadline to file after the injury &mdash; usually 1 to 6 years "
        "depending on the state, and in most states the clock starts when you "
        "discover, or reasonably should have discovered, the injury and that the "
        "product caused it. The <strong>statute of repose</strong> is an outer "
        "limit measured from when the product was first sold &mdash; 10 to 15 "
        "years in the states that have one. After the repose period runs out, "
        "you cannot sue even if you were only just hurt.</p>"
    )
    parts.append(
        "<p>Some states have no repose period at all, and a few had one that "
        "their courts struck down as unconstitutional. A few states use a "
        "softer rule instead: after a certain number of years, the product is "
        "<em>presumed</em> to be past its useful safe life, but you can still "
        "win if you prove otherwise. The state card below gives both numbers "
        "for " + esc(state) + ".</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Do not wait. The clock can "
        "start before you connect the injury to the product, and the repose "
        "clock runs from the sale date whether you knew about the defect or "
        "not. Talk to a lawyer as soon as you are hurt.</p>"
    )
    parts.append("</div>")
    # --- Card 4: right after you're hurt ---
    parts.append('<div class="card">')
    parts.append("<h3>Right after you are hurt: what to keep</h3>")
    parts.append(
        "<p><strong>Get medical care first.</strong> Then protect the evidence. "
        "<strong>Keep the product.</strong> Do not throw it away, do not repair "
        "it, and do not let anyone alter it &mdash; the product itself is the "
        "most important piece of evidence in the case. Keep the packaging, the "
        "receipt, the instructions, and any warnings that came with it. "
        "Photograph the product, the injury, and where it happened. Write down "
        "what happened while it is fresh: the date, what you were doing, and "
        "who saw it.</p>"
    )
    parts.append(
        "<p>Report the product to the U.S. Consumer Product Safety Commission at "
        '<a href="https://www.saferproducts.gov/" target="_blank" '
        'rel="noopener">SaferProducts.gov</a> &mdash; your report can trigger a '
        "recall that protects other people, and it creates a record of the "
        "problem. For a car or car part, report to the National Highway Traffic "
        "Safety Administration; for a drug or medical device, to the Food and "
        "Drug Administration. Do not sign anything from the maker or its "
        "insurer, and do not give a recorded statement, before you talk to a "
        "lawyer.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Keep the product, keep the "
        "paperwork, take photos, write it down, and report it. Then call a "
        "lawyer &mdash; most product-liability lawyers offer a free first "
        "consultation.</p>"
    )
    parts.append("</div>")
    # --- Card 5: who you can sue ---
    parts.append('<div class="card">')
    parts.append("<h3>Who you can sue</h3>")
    parts.append(
        "<p>Usually you start with the <strong>manufacturer</strong> &mdash; the "
        "company that made the product or the defective part. But the whole "
        "chain of distribution can be liable in many states: the distributor, "
        "the wholesaler, and the store that sold it to you. In some states, a "
        "seller who did not make the product can step out of the case once the "
        "manufacturer is identified and can be sued. In others, the store stays "
        "on the hook. Online marketplaces are a newer question, and the rules "
        "vary by state and court.</p>"
    )
    parts.append(
        "<p>It also matters <em>where</em> you sue. If the product was made in "
        "one state and sold in another, the other state&rsquo;s deadlines can "
        "sometimes apply instead of yours &mdash; that is why a lawyer checks "
        "more than one state&rsquo;s law before filing.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Save the receipt and the "
        "name of the store, and note the maker&rsquo;s name from the product "
        "or packaging. A lawyer can work out who belongs in the case from "
        "there.</p>"
    )
    parts.append("</div>")
    # --- Card 6: what you can recover ---
    parts.append('<div class="card">')
    parts.append("<h3>What you can recover</h3>")
    parts.append(
        "<p>A successful claim can cover your <strong>medical bills</strong>, "
        "<strong>lost wages</strong>, <strong>pain and suffering</strong>, and "
        "damage to your property. If the company&rsquo;s conduct was "
        "especially bad &mdash; it knew about the danger and hid it, for "
        "example &mdash; <strong>punitive damages</strong> may be available, "
        "though many states cap them. If the defective product kills someone, "
        "the family may have a wrongful-death claim.</p>"
    )
    parts.append(
        "<p>Your own fault can matter. Most states reduce your recovery by your "
        "share of fault; a few still bar recovery entirely if you were even "
        "slightly at fault. The state card below notes the rule where it is "
        "unusual.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Keep every bill and every "
        "record of time you missed from work. Those papers are how damages are "
        "proved. If someone died, see the "
        f'<a href="#wrongful-death-in-{slug}">Wrongful Death</a> section on '
        "this page.</p>"
    )
    parts.append("</div>")
    # --- Card 7: in this state ---
    parts.append('<div class="card">')
    parts.append(f"<h3>Product liability &amp; defective products in {esc(state)}</h3>")
    parts.append(
        f"<p><strong>Deadline to file?</strong> {e['sol_years']} year{'s' if e['sol_years'] != 1 else ''}. {esc(e['sol_note'])}</p>"
    )
    if e["repose_years"] is not None:
        parts.append(
            f"<p><strong>Outer limit from sale (statute of repose)?</strong> {e['repose_years']} years. {esc(e['repose_note'])}</p>"
        )
    else:
        parts.append(
            f"<p><strong>Outer limit from sale (statute of repose)?</strong> No limit. {esc(e['repose_note'])}</p>"
        )
    parts.append(
        f"<p><strong>Strict liability?</strong> {word(e['strict_liability'])}. {esc(e['strict_note'])}</p>"
    )
    if e["statute_cite"]:
        parts.append(
            f"<p><strong>The law:</strong> {esc(e['statute_name'])} &mdash; {esc(e['statute_cite'])}.</p>"
        )
    else:
        parts.append(
            "<p><strong>The law:</strong> No single statute &mdash; this state&rsquo;s "
            "product-liability rules come from court decisions, not a statute.</p>"
        )
    if e["state_note"]:
        parts.append(f"<p>{esc(e['state_note'])}</p>")
    parts.append(
        f"<p><strong>Free legal help:</strong> "
        f'<a href="{esc(e["legal_aid_url"])}" target="_blank" rel="noopener">{esc(e["legal_aid_name"])}</a>. '
        "Note: free legal aid rarely takes injury cases. Product-liability "
        "lawyers usually work on contingency &mdash; no fee unless you win "
        "&mdash; and most offer a free first consultation, so that is the usual "
        "route for a defective-product claim.</p>"
    )
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> Check the two deadlines "
        "above for your state, keep the product and all paperwork, report it "
        "to the Consumer Product Safety Commission, and talk to a "
        "product-liability lawyer before either deadline runs out.</p>"
    )
    parts.append("</div>")
    # --- Do this now + sources ---
    parts.append(
        "<p><strong>Okay, so what do I do?</strong> (1) Get medical care. "
        "(2) Keep the product &mdash; do not throw it away or repair it &mdash; "
        "and keep the packaging, receipt, and instructions. (3) Photograph "
        "everything and write down what happened. (4) Report the product at "
        "SaferProducts.gov. (5) Check your state&rsquo;s two deadlines above "
        "&mdash; the filing deadline and the outer limit from the sale date. "
        "(6) Talk to a product-liability lawyer, usually free for a first "
        "consultation and on contingency, before you sign anything from the "
        "maker or its insurer. (7) If someone died, see the "
        f'<a href="#wrongful-death-in-{slug}">Wrongful Death</a> section on '
        "this page.</p>"
    )
    parts.append(
        "<p><em>Sources: the official state statutes and court sources linked in "
        "the research for this section, checked November 20, 2026. Product "
        "liability law is fact-specific and deadlines are strict &mdash; confirm "
        "the current law with a lawyer before you rely on it. This is general "
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
            f"Product liability &amp; defective products in {state}</a></li>\n"
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
        '<option value="asylum-daca-deportation-defense" data-anchor="asylum-daca-deportation-defense">'
        "Asylum, DACA &amp; deportation defense (asylum deadline, DACA renewals, removal hearings, your rights with ICE, detention and bond)</option>"
    )
    assert opt_old in text, "asylum helper option not found"
    opt_new = (
        opt_old
        + '\n<option value="product-liability-defective-products" data-anchor="product-liability-defective-products">'
        "Product liability &amp; defective products (defective drugs, devices, cars, recalls, deadlines to sue, what to keep)</option>"
    )
    text = text.replace(opt_old, opt_new, 1)
    # NOTE: the #94 asylum card was deferred (thumbnail missing), so the
    # newest card actually on the page is self-defense (#93).
    card_anchor = 'data-topic="self-defense-use-of-force"'
    idx = text.find(card_anchor)
    assert idx != -1, "self-defense card not found"
    card_end = text.find("</a>", idx)
    assert card_end != -1
    card_end += len("</a>")
    card = """
        <a class="topic-card" href="#helper" data-topic="product-liability-defective-products">
          <span class="topic-img"><img src="assets/img/topics/thumbs/legal-buffet-product-liability-defective-products.jpg" alt="Product liability and defective products" loading="lazy"></span>
          <h3>Product Liability &amp; Defective Products</h3>
          <p>Hurt by a defective product &mdash; a drug, a device, a car part, a household item. The three kinds of defects, the two deadlines, and what to keep.</p>
          <span class="go">Learn more &rarr;</span>
        </a>"""
    text = text[:card_end] + card + text[card_end:]
    assert "Show all 47 topics" in text, "show-all label not found"
    text = text.replace("Show all 47 topics", "Show all 48 topics", 1)
    show_pos = text.find("Show all 48 topics")
    assert show_pos != -1
    badge = '<span class="count-badge">47 topics</span>'
    badge_pos = text.find(badge, show_pos)
    assert badge_pos != -1, "main-grid badge not found after show-label"
    text = text[:badge_pos] + badge.replace("47 topics", "48 topics") + text[badge_pos + len(badge):]
    assert text.count('<span class="count-badge">42 topics</span>') == 1, "hero badge disturbed"
    INDEX.write_text(text)
    print("  index.html: helper option + card + counts 47->48")


def build_about():
    text = ABOUT.read_text()
    assert text.count("93 legal topics") == 1, "about count not found"
    ABOUT.write_text(text.replace("93 legal topics", "94 legal topics", 1))
    print("  about.html: 93 -> 94")


def state_index_t(state, slug, e):
    repose = (
        f"statute of repose {e['repose_years']} years {e['repose_note']}"
        if e["repose_years"] is not None
        else f"no statute of repose {e['repose_note']}"
    )
    bits = [
        "product liability defective products recalls",
        f"Product liability & defective products in {state}",
        f"statute of limitations {e['sol_years']} years {e['sol_note']}",
        repose,
        f"strict liability {word(e['strict_liability']).lower()} {e['strict_note']}",
        "three kinds of defects manufacturing defect design defect failure to warn unreasonably dangerous",
        "keep the product do not throw it away do not repair it keep packaging receipt instructions photograph report SaferProducts.gov",
        "who to sue manufacturer distributor wholesaler retailer chain of distribution",
        "damages medical bills lost wages pain and suffering punitive damages",
        f"{e['statute_name'] or 'case law'} {e['statute_cite'] or ''}",
        f"{e['state_note'] or ''}",
        f"{e['legal_aid_name']}",
    ]
    return " — ".join(b.strip() for b in bits if b and b.strip())


def build_search_index(data):
    idx = json.loads(SEARCH_INDEX.read_text())
    assert len(idx) == 11161, f"unexpected index size {len(idx)}"
    assert not any(e.get("a", "").startswith(f"{SLUG}-in-") for e in idx)
    for key, e in data:
        state = key.title()
        slug = key.replace(" ", "-")
        idx.append(
            {
                "p": f"{state} Legal Resources \u2014 The Legal Buffet",
                "u": f"states/{slug}.html",
                "a": f"{SLUG}-in-{slug}",
                "h": f"Product liability & defective products in {state}",
                "t": state_index_t(state, slug, e),
            }
        )
    idx.append(
        {
            "p": "The Legal Buffet \u2014 Free Legal Resources for Every State",
            "u": "index.html",
            "a": "helper",
            "h": "Product Liability & Defective Products",
            "t": (
                "product-liability-defective-products product liability defective "
                "products Product Liability & Defective Products? Hurt by a "
                "defective product — a drug, a device, a car part, a household "
                "item. The three kinds of defects, the two deadlines, and what "
                "to keep. Manufacturing defect design defect failure to warn "
                "strict liability statute of limitations statute of repose keep "
                "the product SaferProducts.gov contingency lawyer."
            ),
        }
    )
    assert len(idx) == 11212, f"unexpected new index size {len(idx)}"
    for e in idx[-51:]:
        assert set(e.keys()) == {"p", "u", "a", "h", "t"}, e
    SEARCH_INDEX.write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    print(f"  search-index.json: 11161 -> {len(idx)} (+51)")


def main():
    d = json.loads(DATA.read_text())
    states = d["states"]
    assert len(states) == 50, len(states)
    data = [(k, states[k]) for k in sorted(states)]
    slugs = [k.replace(" ", "-") for k, _ in data]
    assert len(set(slugs)) == 50, "duplicate slugs"
    assert THUMB.exists(), "thumbnail missing"
    req = [
        "sol_years", "sol_note", "repose_years", "repose_note",
        "strict_liability", "strict_note", "statute_name", "statute_cite",
        "legal_aid_name", "legal_aid_url", "state_note", "sources",
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
        assert isinstance(e["sol_years"], int) and 1 <= e["sol_years"] <= 6, f"{k}: bad sol_years"
        assert e["repose_years"] is None or (isinstance(e["repose_years"], int) and 1 <= e["repose_years"] <= 20), f"{k}: bad repose_years"
        assert e["strict_liability"] in ("yes", "no"), f"{k}: bad strict_liability"
        assert e["sol_note"] and e["repose_note"] and e["strict_note"] and e["legal_aid_name"] and e["legal_aid_url"] and e["sources"], f"{k}: empty required field"
        assert (e["statute_name"] is None) == (e["statute_cite"] is None), f"{k}: statute name/cite mismatch"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        assert not phone_re.search(blob), f"{k}: phone-like string in data"
    print("building state pages (insert before asylum-daca-deportation-defense section)...")
    build_state_pages(data)
    print("building index/about/search...")
    build_index()
    build_about()
    build_search_index(data)
    print("DONE")


if __name__ == "__main__":
    main()
