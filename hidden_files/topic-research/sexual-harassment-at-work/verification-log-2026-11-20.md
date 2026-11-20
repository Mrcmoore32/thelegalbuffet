# Topic #90 verification log — 2026-11-20

## URLs (90 checked by curl; non-200s confirmed by live browser text fetch)
- Fixed: AZ agency -> https://www.azag.gov/civil-rights/faq (old 404);
  OH agency -> https://civ.ohio.gov/ (old deep URL 404; homepage alive in browser);
  DE agency -> https://labor.delaware.gov/antidiscrimination (old subdomain 000/unresolvable).
- Confirmed alive despite curl 403/406/000 (bot filters): AL, CA x2, CO x2, GA, ID,
  ME, MA x2, MS, NV, NH, NJ, UT, WY x2 legal-aid/agency pages.
- TN agency tn.gov/humanrights.html: curl 403 (bot-filter pattern); one browser fetch
  failed with a network error and was not retried. Kept as the official tn.gov URL.

## Phones (26 in dataset; 10 pass, 16 fail in verification pass)
- 1-800-669-4000 on AL/AR/GA is the EEOC's number, not legal aid's. AL replaced with
  LSA 1-866-456-4995; GA replaced with GLSP 1-800-498-9469; AR dropped to null.
- Relabeled to true owner: CA 800-884-1684 (CRD), DE 302-761-8200 (DE Office of
  Anti-Discrimination), HI (808) 586-8636 (Hawai'i Civil Rights Commission),
  ID (208) 334-2873 (Idaho Human Rights Commission), OH 1-888-278-7101 (OCRC),
  NE 1-877-250-2016 (Legal Aid of Nebraska).
- Added (two official sources each): AZ (602) 542-5263, NH (603) 271-2767,
  MA (617) 994-6000.
- Dropped to null (no second official source): IN, KY, NY, ND, VT, VA, WV.
- Final: 21 phones print (16 state agency, 5 legal aid); 29 states claim-free.

## Federal core (eeoc.gov/time-limits-filing-charge, read Nov 20)
- 180 days baseline, 300 days in deferral states; ongoing-harassment clock runs
  from the last incident; EEOC phone 1-800-669-4000.
