# Live Site Audit: psfnetwork.com/blog (follow-up)

Date: 2026-08-11
Method: same as the 2026-07-21 audit: sitemap.xml enumeration, then server-rendered HTML fetched per article with a browser User-Agent. All fetches performed today from this session.
Baseline: `workflow/live-site-audit-2026-07-21.md`.
Companions: `workflow/batch1-audit-2026-08-11.md` (repo-side audit, same day) and `workflow/live-sync-2026-08-11.md` (reconciliation pass and captures).

**Revision note:** this file replaces an earlier same-day version that reported zero internal links on live pages. That measurement only looked for absolute `/blog/...` hrefs; the live pages use relative `./slug` hrefs, which the first pass missed. The internal-link findings below are the corrected ones.

---

## Inventory changes since 2026-07-21

| Change | Detail |
|---|---|
| reits-vs-fractional-real-estate is LIVE | Published since the July audit. All 12 Batch 1 articles are now live. |
| Both live Batch 2 articles UNPUBLISHED | how-to-choose-fractional-real-estate-platform and proptech-future-of-real-estate now return 404 and are gone from the sitemap. Batch 2 and Batch 3 have zero live presence. |

Live blog inventory today: 12 Batch 1 articles plus `/blog` and `/blog/getting-started`. All return 200.

---

## Finding 1: The live site carries a full content revision that never reached the repo (HIGH)

Between 2026-07-21 and today, 11 of the 12 live articles received a comprehensive editorial revision done outside the pipeline:

- **Internal links restored:** 5 to 6 inline internal links per article body, all relative `./slug` hrefs, all resolving to live articles. The July audit's zero-internal-links problem has been fixed in Framer.
- **External authority links added:** 3 to 10 per body (irs.gov, investor.gov, sec.gov, federalreserve.gov and others).
- **Body text rewritten:** even articles that kept their section structure carry paragraph-level rewrites with SEO keyword weaving. The revision respects the punctuation rules: zero em or en dashes across all 12 pages.
- **5 articles restructured entirely** (new section sets, statement-style headings): reg-a-vs-reg-d-for-fractional-investors, fractional-real-estate-investing, real-estate-crowdfunding-vs-fractional, best-fractional-real-estate-platforms, how-to-invest-in-real-estate-with-100.
- **2 articles had their question-format H2s renamed to statement form:** how-to-invest-10k-in-real-estate, 90-percent-millionaires-real-estate.
- **5 articles kept the pipeline structure** with lighter text edits: what-is-proptech, square-foot-real-estate-ownership-explained, how-to-build-passive-income-with-real-estate, how-fractional-real-estate-is-taxed, plus the freshly pasted reits article.

The repo drafts are one generation behind the live site. Full details, per-article classification, and faithful markdown captures of all 12 live pages are in `workflow/live-sync-2026-08-11.md` and `workflow/live-captures/2026-08-11/[slug].md`.

**Action:** operator decision on canonicalization: adopt the live revision into the repo as the new baseline (after a Stage 7 style QA on the captures), or reject it and re-push repo content. Also worth recording who produced the revision, since the pipeline has no trace of it.

## Finding 2: The newly published REIT article missed the revision (HIGH)

reits-vs-fractional-real-estate went live, closing the 404 that 18 draft links point at. But it is the un-revised draft pasted as-is:

- Zero inline external links and zero inline internal links in the body (the only such page; its internal links are just the pasted Related list and the template's related-article cards)
- The draft's Author block renders as body content: "Maya Reyes is a Senior Editor... Reviewed by Daniel Cho, CFA" while the hero byline and JSON-LD say Youssef Kholeif, CMO. Two conflicting attributions on one page.
- The hero image is the square-foot article's visual (img alt "square-foot-estate"). The REIT-specific visual in the repo is still unplaced, which `workflow/visuals-tracker.md` correctly shows.

**Action:** one Framer edit: remove the pasted persona block, place the correct visual, bring the article up to the revision standard (internal and external links).

## Finding 3: Meta descriptions still empty on all 12 (HIGH, unchanged)

`meta name="description"`, `og:description` and `twitter:description` are present but empty on every live article, exactly as on 07-21. The revision pass did not touch them either. Every draft has a ready meta description in frontmatter.

## Finding 4: Brand casing violations in live TL;DR blocks (MEDIUM, new)

Three live articles write the brand lowercase in prose, e.g. "Arrived, Ark7, Realbricks, or psfnetwork": <!-- check-rules: allow -->
best-fractional-real-estate-platforms, how-to-invest-10k-in-real-estate, how-to-invest-in-real-estate-with-100 (all in the TL;DR summary block). The brand rule requires "PSFnetwork" in prose. These entered with the Framer-side revision; the pipeline's check-rules would have blocked them.

**Action:** fix the three TL;DR blocks in Framer.

## Finding 5: Off-policy external links went live with the revision (MEDIUM, new)

Three live-only links are outside the allowed-domain policy and absent from every draft and evidence file:

| Article | Link | Problem |
|---|---|---|
| fractional-real-estate-investing | binaryx.com blog post | Competitor tokenization platform, linked from the pillar article |
| how-fractional-real-estate-is-taxed | en.wikipedia.org (like-kind exchange) | Wikipedia as a source; irs.gov has the authoritative page |
| real-estate-crowdfunding-vs-fractional | finance.yahoo.com article | Low-authority aggregator |
| how-to-invest-10k-in-real-estate | irs.gov/forms-pubs/about-schedule-k-1-form-1065 | Known 404. The 2026-05-26 link audit removed this exact URL from the repo and banned it (`tests/test_link_audit.py`); the live revision reintroduced it in the Sources list. The repo test suite caught it in the capture. |

**Action:** replace with authoritative equivalents (or remove) in Framer. The binaryx one matters most: it hands pillar-page authority to a competitor. The dead IRS link should point to irs.gov/instructions/i1065sk1, which the repo draft already uses.

## Finding 6: Three H1 tags per page (MEDIUM, unchanged)

Every article still renders its title plus two "Start from square one" CTA headings as H1. Template-level fix, one edit corrects all pages.

## Finding 7: Title tags over 60 characters: 11 of 12 (LOW)

The " - PSFnetwork" suffix pushes 11 of the 12 live titles past 60 characters (66 to 84 chars). Only best-fractional-real-estate-platforms (58) fits. Fix is unchanged: shorten CMS titles or drop the suffix on long ones.

---

## What is working

- All 12 Batch 1 articles live and returning 200
- Internal linking live and healthy on 11 of 12 (5 to 6 body links each, no dead targets)
- External authority links live on 11 of 12 bodies
- Zero em or en dashes anywhere in the live revision
- Canonical tags correct on all 12 (www host, matching slug)
- JSON-LD present on all 12
- Sitemap consistent with what actually serves

## Priority order

1. Fill the 12 empty meta descriptions from draft frontmatter
2. Fix the REIT page in one Framer edit (drop pasted persona block, place its visual, add its links)
3. Decide canonicalization of the live revision (see `workflow/live-sync-2026-08-11.md`) so repo and site converge on one truth
4. Fix the three lowercase-brand TL;DR blocks in Framer
5. Replace the binaryx, wikipedia and yahoo links
6. Retag the CTA H1s in the template; trim the title suffix overflow
