#!/usr/bin/env python3
"""Merge the 5 research batches for Topic #112: Protecting Kids Online
into hidden_files/topic-research/protecting-kids-online/all-states.json.

Fixes applied at merge (all spot-verified against official/second sources
2026-11-23, see header notes in the builder):
- CA age_design: Ninth Circuit Mar 12, 2026 ruling NARROWED the CAADCA
  injunction (coverage definition + age estimation may now be enforced;
  only data-use restrictions and the dark-patterns ban remain blocked).
  Researcher text said "most substantive provisions remain blocked" — wrong.
- UT age_design: drop the unverified "stayed pending a decision by the
  U.S. Court of Appeals for the 10th Circuit" — no such appeal confirmed.
- AR age_design: add the state's Eighth Circuit appeal + the two 2025
  follow-up laws (Acts 900 and 901), both preliminarily enjoined in 2026.
- AL age_design: add signing date Feb 17, 2026 (Act 2026-59) + CCIA suit
  filed Oct 28, 2026 with no blocking order yet.
- IN age_design: fix the Free Speech Coalition v. Paxton phrasing (the 2024
  preliminary injunction was vacated on appeal in Aug 2024; Paxton was the
  June 2025 SCOTUS decision upholding Texas's similar law) + add HEA 1408
  (2026), the new social-media age-verification/parental-consent law
  (Ind. Code 24-16, eff. Jan 1, 2027; NetChoice sued Nov 18, 2026).
- CO report_url: http -> https (https returns 200).
- Sexting fields: reframe "no separate teen-sexting law" leads as positive
  statements about the applicable general statute (AL, AK, CA, DE, GA, KY,
  MI, MN, MO, MT, NV, NH). Several of those absence claims were NOT
  confirmed by two official sources, so the lead is dropped and the
  statute speaks for itself.
- Empty fields stay empty (claim-free per the gap rule): age_design empty
  in 27 states, sexting empty in HI/ME/MS, grooming empty in WY,
  report_name/report_url empty in NV/NH. The builder omits those lines.
"""
import json
import re
from pathlib import Path

DIR = Path(__file__).resolve().parent
BATCHES = [
    "batch-al-ga.json",
    "batch-hi-md.json",
    "batch-ma-nj.json",
    "batch-nm-sc.json",
    "batch-sd-wy.json",
]
OUT = DIR / "all-states.json"

FIXES = {
    ("california", "age_design"): (
        "California Age-Appropriate Design Code Act (AB 2273, 2022; "
        "Cal. Civ. Code §§ 1798.99.28–1798.99.40) — partially enjoined — "
        "after a March 12, 2026 Ninth Circuit ruling, the coverage "
        "definition and age-estimation requirement may be enforced, while "
        "data-use restrictions and the dark-patterns ban remain blocked; "
        "the case continues on remand."
    ),
    ("utah", "age_design"): (
        "Utah Minor Protection in Social Media Act, SB 194 (2024), Utah "
        "Code §§ 13-71-101 to -401, which replaced the 2023 Social Media "
        "Regulation Act (HB 311/SB 152) — requires age assurance and "
        "default privacy protections for minor accounts; enjoined: a "
        "federal court issued a preliminary injunction in September 2024 "
        "(NetChoice v. Reyes), and enforcement remains blocked while the "
        "case continues."
    ),
    ("arkansas", "age_design"): (
        "Social Media Safety Act (Act 689 of 2023) — permanently enjoined "
        "and held unconstitutional by a federal court on March 31, 2025 "
        "(NetChoice v. Griffin); the law is struck down and not in effect; "
        "the state has appealed to the Eighth Circuit. Arkansas later "
        "passed two follow-up laws (Acts 900 and 901 of 2025); a federal "
        "court has preliminarily blocked both while those cases continue."
    ),
    ("alabama", "age_design"): (
        "App Store Accountability Act (HB 161, Act 2026-59; signed "
        "February 17, 2026) — takes effect January 1, 2027; requires app "
        "stores to verify users' age categories and get verifiable "
        "parental consent before minors download apps or make purchases. "
        "A trade group sued to block it in October 2026; no court has "
        "blocked it yet."
    ),
    ("indiana", "age_design"): (
        "Senate Enrolled Act 17 (2024), codified at Ind. Code §24-4-23 — "
        "requires adult-oriented website operators displaying material "
        "harmful to minors to use a reasonable age-verification method; "
        "in effect since July 1, 2024 (a 2024 preliminary injunction was "
        "vacated on appeal, and the U.S. Supreme Court's June 2025 "
        "decision in Free Speech Coalition v. Paxton upheld a similar "
        "Texas law). Separately, HEA 1408 (2026) creates new social-media "
        "age-verification and parental-consent rules (Ind. Code § 24-16) "
        "taking effect January 1, 2027; NetChoice sued to block it on "
        "November 18, 2026, and no court has ruled yet."
    ),
    ("colorado", "report_url"): "https://coloradoicac.com/",
    ("alabama", "sexting"): (
        "Under Ala. Code § 13A-12-192, a minor who possesses or shares a "
        "sexual image of another minor can be charged under the state's "
        "general child sexual abuse material law."
    ),
    ("alaska", "sexting"): (
        "Under Alaska Stat. § 11.61.116, it is a crime to send an "
        "explicit image of a minor under 16 to another person or post it "
        "publicly with intent to annoy or humiliate."
    ),
    ("california", "sexting"): (
        "Under Cal. Penal Code § 311.11, a minor who possesses matter "
        "depicting another minor in sexual conduct can be charged under "
        "the general law against possessing such material."
    ),
    ("delaware", "sexting"): (
        "Under 11 Del. C. § 1109, a minor who deals in child sexual abuse "
        "material can be charged under the same felony statute as an "
        "adult, except that under § 1110A a minor cannot be convicted "
        "when the image depicts only partial nudity."
    ),
    ("georgia", "sexting"): (
        "Under O.C.G.A. § 16-12-100, a minor who produces or shares a "
        "visual depiction of another minor in sexually explicit conduct "
        "can face felony sexual exploitation of a child charges, though "
        "§ 16-12-100(f)(3) allows a misdemeanor when the image was "
        "consensual, the depicted minor was at least 14, and the "
        "defendant was 18 or younger."
    ),
    ("kentucky", "sexting"): (
        "Under Ky. Rev. Stat. § 531.335, possessing explicit material "
        "depicting a minor is a crime."
    ),
    ("michigan", "sexting"): (
        "Minors are charged under MCL 750.145c, the child sexually "
        "abusive material law, which has no exception for minors; "
        "prosecutors often handle cases in juvenile court or through "
        "diversion."
    ),
    ("minnesota", "sexting"): (
        "Minors are charged under Minn. Stat. § 617.247, the law against "
        "possessing or disseminating pornographic works involving minors, "
        "with no exception for teens."
    ),
    ("missouri", "sexting"): (
        "Minors face the same child sexual abuse material statutes as "
        "adults, including Mo. Rev. Stat. § 573.035 (promoting child "
        "sexual abuse material, class D felony) and § 573.037 "
        "(possession, class D felony)."
    ),
    ("montana", "sexting"): (
        "Minors are prosecuted under MCA § 45-5-625 (sexual abuse of "
        "children), which criminalizes photographing, distributing, or "
        "possessing visual material of a child in sexual conduct, with no "
        "exception for minors."
    ),
    ("nevada", "sexting"): (
        "Minors are prosecuted under Nev. Rev. Stat. §§ 200.725 "
        "(preparing or distributing material depicting a minor in sexual "
        "conduct) and 200.730 (possession of a visual presentation of a "
        "person under 16 in sexual conduct), both category B felonies."
    ),
    ("new-hampshire", "sexting"): (
        "Prosecuted under RSA ch. 649-A (Child Sexual Abuse Images): "
        "possession under § 649-A:3 is a class A felony on a first "
        "offense, with separate felonies for distribution and manufacture."
    ),
    ("iowa", "sexting"): (
        "Iowa Code §728.12 — Sexual exploitation of a minor: it is a "
        "crime to employ, persuade, entice or coerce a minor to engage in "
        "a prohibited sexual act for a visual depiction, or to knowingly "
        "promote or possess such material."
    ),
    ("kansas", "sexting"): (
        "K.S.A. §21-5510 — Sexual exploitation of a child: it is a felony "
        "to possess, promote or distribute sexually exploitative material "
        "depicting a child under 18, which covers explicit images shared "
        "by sexting."
    ),
    ("new-mexico", "sexting"): (
        "Minors are charged under NMSA 1978 § 30-6A-3 (Sexual "
        "Exploitation of Children — possession is a 4th-degree felony, "
        "distribution a 3rd-degree felony), with a narrow exception for "
        "consensual close-in-age possession by minors aged 14–18."
    ),
    ("new-york", "sexting"): (
        "Teens can face felony charges under N.Y. Penal Law Article 263, "
        "but Penal Law § 60.37 (with Soc. Serv. Law § 458-l) lets a court "
        "divert eligible young people (both parties under 20, no more "
        "than 5 years apart) to an education program instead of "
        "prosecution."
    ),
    ("north-carolina", "sexting"): (
        "Prosecuted under felony Sexual Exploitation of a Minor statutes, "
        "N.C.G.S. §§ 14-190.16 (1st degree), 14-190.17 (2nd degree — "
        "recording or distributing, Class E felony), and 14-190.17A (3rd "
        "degree — possession, Class H felony)."
    ),
    ("north-dakota", "sexting"): (
        "Under N.D. Cent. Code § 12.1-27.1-03.3, it is a Class A "
        "misdemeanor to secretly create or possess a sexually expressive "
        "image without written consent, or to share one to cause "
        "emotional harm — but it does not turn on the depicted person's "
        "age. Other conduct falls under felony child sexual abuse "
        "material laws (N.D.C.C. ch. 12.1-27.2)."
    ),
    ("oregon", "sexting"): (
        "Prosecuted under ORS 163.684 (encouraging child sexual abuse, "
        "1st degree, Class B felony — distribution), ORS 163.686 (2nd "
        "degree, Class C felony — possession or viewing), ORS 163.687 "
        "(3rd degree, Class A misdemeanor), and ORS 163.689/163.690 "
        "(possession of materials depicting sexually explicit conduct of "
        "a child), with no age-based exception for minors."
    ),
    ("south-carolina", "sexting"): (
        "Prosecuted under felony Sexual Exploitation of a Minor statutes, "
        "S.C. Code §§ 16-15-395 (1st degree), 16-15-405 (2nd degree), and "
        "16-15-410 (3rd degree), with a first-offense Family Court or "
        "misdemeanor valve under § 16-15-390(D) for the obscenity-based "
        "charge and under §§ 16-15-395(E)/405(E)/410(E) for morphed images."
    ),
}


def norm_slug(key, entry):
    slug = entry.get("slug") or key.replace(" ", "-").replace("_", "-")
    return slug.strip().lower().replace("_", "-").replace(" ", "-")


def main():
    merged = {}
    for fname in BATCHES:
        batch = json.loads((DIR / fname).read_text())
        for key, entry in batch.items():
            slug = norm_slug(key, entry)
            assert slug not in merged, f"duplicate slug {slug}"
            assert re.fullmatch(r"[a-z-]+", slug), f"bad slug {slug!r}"
            entry["slug"] = slug
            merged[slug] = entry
    assert len(merged) == 50, f"expected 50 states, got {len(merged)}"

    for (slug, field), value in FIXES.items():
        assert slug in merged, f"fix target missing: {slug}"
        assert field in merged[slug], f"fix field missing: {slug}.{field}"
        merged[slug][field] = value

    req = [
        "state", "slug", "overview", "cyberbullying", "sexting",
        "grooming", "age_design", "report_name", "report_url",
        "legal_aid_name", "legal_aid_url", "sources",
    ]
    phone_re = re.compile(
        r"\(\d{3}\)\s*\d{3}[-.]\d{4}|\b\d{3}[-.]\d{3}[-.]\d{4}\b|"
        r"1-800-\d{3}-\d{4}|1-866-\d{3}-\d{4}|1-888-\d{3}-\d{4}|1-855-\d{3}-\d{4}|"
        r"877-\d{3}-\d{4}|800-\d{3}-\d{4}|844-\d{3}-\d{4}|866-\d{3}-\d{4}|855-\d{3}-\d{4}|"
        r"1-877-\d{3}-\d{4}|1-833-[A-Z0-9]{7}"
    )
    empty = {}
    for slug, e in sorted(merged.items()):
        for f in req:
            assert f in e, f"{slug}: missing {f}"
        assert e["sources"] and len(e["sources"]) >= 2, f"{slug}: <2 sources"
        assert e["state"] and e["overview"] and e["cyberbullying"], f"{slug}: empty core field"
        assert e["legal_aid_name"] and e["legal_aid_url"], f"{slug}: empty legal aid"
        assert e["slug"] == slug, f"{slug}: slug field mismatch {e['slug']!r}"
        blob = json.dumps({f: e[f] for f in req if f != "sources"})
        assert not phone_re.search(blob), f"{slug}: phone-like string in data"
        for f in ("sexting", "grooming", "age_design", "report_name", "report_url"):
            if not e[f]:
                empty.setdefault(f, []).append(slug)
        # no remaining "no separate/no dedicated" leads in sexting
        s = e["sexting"].lower()
        assert not re.search(r"no (separate|dedicated|specific) teen", s), f"{slug}: unreframed sexting lead"
        assert "no teen safe-harbor" not in s, f"{slug}: unreframed sexting lead"
    for f, slugs in sorted(empty.items()):
        print(f"  empty {f} ({len(slugs)}): {', '.join(slugs)}")

    ordered = {k: merged[k] for k in sorted(merged)}
    OUT.write_text(json.dumps(ordered, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT} ({len(ordered)} states)")


if __name__ == "__main__":
    main()
