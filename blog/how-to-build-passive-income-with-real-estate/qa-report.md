# Pre-publish QA Report - how-to-build-passive-income-with-real-estate

Stage 7. Verified against `checklist/qa-gate.md`.

| Slug | Date | Loop count |
|------|------|------------|
| how-to-build-passive-income-with-real-estate | 2026-05-14 | 0 |

---

## A. Financial accuracy (sourced)

| Item | Status |
|------|--------|
| Every numerical claim has an entry in `evidence.md` | PASS - C1-C13 covered; arithmetic claims explicitly labeled illustrative |
| Every regulatory claim has an entry in `evidence.md` | PASS - Schedule E (E1), Form 8582 / passive activity (E2), K-1 (E3), REIT 90%+ (E4), non-traded REIT risks (E5), FDIC (E6) |
| All investment return claims include a risk disclosure within the same section | PASS - QuickAnswer carries inline italic footer; how-much body explicitly labels illustrative; risks section is its own H2 |
| No "guaranteed return" language anywhere | PASS - phrase does not appear |
| Federal references factually accurate per evidence | PASS - IRS and investor.gov citations match retrieved content |
| No misleading regulated vs unregulated comparisons | PASS |

## B. SEO & GEO structure

| Item | Status |
|------|--------|
| Frontmatter present with all template-structure.md fields | PASS |
| title 55-60 chars, focus keyword in first third | PASS - "Passive Income Real Estate: A Beginner's Guide for 2026" = 55 chars; focus keyword at chars 1-26 (entire first half) |
| meta_description 150-160 chars, includes focus keyword + CTA verb | PASS - 152 chars; opens with "Passive income real estate"; CTA "How to start" |
| canonical set | PASS - https://psfnetwork.com/blog/how-to-build-passive-income-with-real-estate |
| hero_visual_alt 60-120 chars | PASS - 102 chars |
| H1 unique, contains focus keyword | PASS - "Passive Income Real Estate: How to Build It Without Becoming a Landlord" contains the literal focus keyword |
| H2s in question format | PASS - all 6 H2s are questions |
| QuickAnswer block at top | PASS |
| Every H2 capsule 50-75 words self-contained | PASS - 70 / 63 / 58 / 62 / 60 / 52 |
| FAQ schema-ready Q/A pairs, minimum 5 | PASS - 6 pairs |
| At least 2 internal links to relevant posts that exist in repo | PASS - 3 internal links; hub fractional-real-estate-investing is published, others exist as briefs |
| All external links point to high-authority sources from evidence.md | PASS - 6 Sources, all from E1-E10 |

## C. Brand & content quality

| Item | Status |
|------|--------|
| Brand name written as psfnetwork throughout | PASS |
| No em or en dashes | PASS |
| Tone matches `brand/tone-and-voice.md` | PASS - second person, short sentences, anti-hype |
| No contradictions | PASS |
| No orphaned sentences | PASS |
| Author and reviewer match `brand/personas.md` | PASS - Maya Reyes, Daniel Cho, CFA |
| Disclaimer text matches canonical disclaimer in `brand/tone-and-voice.md` | PASS - exact match |
| Every component listed in `brand/template-structure.md` is present in order | PASS |

## D. Template completeness

| Item | Status |
|------|--------|
| ArticleHero metadata in frontmatter | PASS - type: Guide, topic: Passive Income |
| HeroVisual placeholder present | PASS - [VISUAL-HERO-01] |
| QuickAnswer has exactly 4 stat cards | PASS |
| Opening is 2 paragraphs with no headers | PASS |
| Sources numbered, references evidence.md | PASS - 6 entries |
| AuthorCard, Disclaimer, CTABlock, Related all present | PASS |
| Related lists exactly 3 internal links | PASS |

---

## Summary

| Section | Total items | Pass | Fail |
|---------|-------------|------|------|
| A. Financial accuracy | 6 | 6 | 0 |
| B. SEO & GEO | 12 | 12 | 0 |
| C. Brand & content quality | 8 | 8 | 0 |
| D. Template completeness | 7 | 7 | 0 |
| **Total** | **33** | **33** | **0** |

QA_RESULT: PASS
FAILED_ITEMS: []
PASS_ITEMS: 33
RECOMMENDATION: PUBLISH

Loop count: 0. Proceeding to Stage 8.
