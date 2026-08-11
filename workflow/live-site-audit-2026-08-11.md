# Live Site Audit: psfnetwork.com/blog (follow-up)

Date: 2026-08-11
Method: same as the 2026-07-21 audit: sitemap.xml enumeration, then server-rendered HTML fetched per article with a browser User-Agent. All fetches performed today from this session.
Baseline: `workflow/live-site-audit-2026-07-21.md`. This document records what changed and what did not.
Companion: `workflow/batch1-audit-2026-08-11.md` (repo-side audit of the same 12 articles, run earlier today).

---

## Inventory changes since 2026-07-21

| Change | Detail |
|---|---|
| reits-vs-fractional-real-estate is LIVE | Published since the July audit. All 12 Batch 1 articles are now live. |
| Both live Batch 2 articles UNPUBLISHED | how-to-choose-fractional-real-estate-platform and proptech-future-of-real-estate now return 404 and are gone from the sitemap. On 07-21 they were live carrying un-fixed feedback content. Batch 2 and Batch 3 now have zero live articles. |

Live blog inventory today: 12 Batch 1 articles plus `/blog` and `/blog/getting-started`. All return 200.

---

## Finding 1: Live content has drifted AHEAD of the repo on external links (HIGH, new)

11 of the 12 live articles now carry inline external authority links in the body: irs.gov, investor.gov, sec.gov, federalreserve.gov, census.gov and others, roughly 3 to 10 content links per article. The repo drafts for these same articles contain zero inline links (confirmed this morning in the Batch 1 audit). The link retrofit the Batch 1 audit recommends was already done, directly in Framer, and never synced back.

Two consequences:

- The repo and Drive copies are no longer the source of truth for Batch 1 body content. The same class of divergence that hit Batch 2 in June (fixed by the Drive re-sync) now exists in the opposite direction for Batch 1.
- The live-only links were added outside the pipeline's allowed-domain rule and were never curl-verified by Stage 7. Most are on-policy gov domains, but at least three are not: a link to binaryx.com (a competitor tokenization platform) on the fractional-real-estate-investing pillar, en.wikipedia.org on the K-1 tax article, and finance.yahoo.com on the crowdfunding comparison.

**Action:** pull the live HTML for all 12 articles, diff against repo drafts, and re-sync the repo (same playbook as the June Batch 2 re-sync). Operator should review the binaryx.com link specifically: it sends pillar-page authority to a competitor.

## Finding 2: The newly published REIT article shipped without its production fixes (HIGH, new)

The reits-vs-fractional-real-estate page went live, which closes the 404 that 18 draft links point at. But the paste skipped everything the other 11 articles received:

- Zero inline external links (the only Batch 1 page without them)
- The draft's Author block was pasted into the body verbatim: "Maya Reyes is a Senior Editor... Reviewed by Daniel Cho, CFA" renders as page content while the hero byline and JSON-LD say Youssef Kholeif, CMO. Two conflicting attributions on one page.
- The hero image is the square-foot article's visual (img alt "square-foot-estate"). The REIT-specific visual produced in the repo (`blog/reits-vs-fractional-real-estate/reits-vs-fractional-real-estate-visual-01.webp`, ready since the visuals batch) is not placed. `workflow/visuals-tracker.md` still correctly shows it unplaced.

**Action:** in Framer: remove the pasted persona Author block, place the correct visual, add the article's external links in the same edit.

## Finding 3: Meta descriptions still empty on all 12 (HIGH, unchanged)

`meta name="description"`, `og:description` and `twitter:description` are present but empty on every live article, exactly as on 07-21. Every draft has a ready meta description in frontmatter. This remains the highest-value 30-minute CMS task on the list.

## Finding 4: Zero internal links on all 12 (HIGH, unchanged)

No live article links to any other article. The external-link retrofit (Finding 1) did not include internal links, which supports the July root-cause: links do not survive the Doc-to-Framer paste, and whoever added the external links in Framer did not add internal ones. The 18 Related-block links in drafts still have no live counterpart.

## Finding 5: Three H1 tags per page (MEDIUM, unchanged)

Every article still renders its title plus two "Start from square one" CTA headings as H1. Template-level fix, one edit corrects all pages.

## Finding 6: Title tags over 60 characters: now 11 of 12 (LOW, worse than reported in July)

The " - PSFnetwork" suffix pushes 11 of the 12 live titles past 60 characters (66 to 84 chars). Only best-fractional-real-estate-platforms (58) fits. The July audit listed five; the count grew because the newly live REIT page and the re-measured set all carry the suffix. Fix is unchanged: shorten CMS titles or drop the suffix on long ones.

---

## What is working

- All 12 Batch 1 articles live and returning 200
- Canonical tags correct on all 12 (www host, matching slug)
- JSON-LD present on all 12 (BlogPosting + Organization blocks)
- Sitemap consistent with what actually serves
- External authority links live on 11 of 12 bodies (Finding 1 caveats aside)

## Priority order

1. Fill the 12 empty meta descriptions from draft frontmatter (unchanged from July, still undone)
2. Fix the REIT page in one Framer edit: drop the pasted persona block, place its visual, add its external links
3. Re-sync repo drafts from live HTML so the repo regains source-of-truth status; review the binaryx.com, wikipedia.org and yahoo.com live-only links during the diff
4. Re-apply internal links or move delivery to the Framer CMS API
5. Decide the Batch 2 plan: the two pulled articles plus the 13 never-published ones, and Batch 3's 9, are all sitting corrected in repo and Drive with zero live presence
6. Retag the CTA H1s in the template; trim the title suffix overflow
