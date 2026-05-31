# Pre-publish QA Report - reits-vs-fractional-real-estate

Stage 7. Verified against `checklist/qa-gate.md`.

| Slug | Date | Loop count |
|------|------|------------|
| reits-vs-fractional-real-estate | 2026-05-14 | 0 |

## A. Financial accuracy (sourced)

| Item | Status |
|------|--------|
| Numerical claims in evidence.md | PASS - REIT 90%+ distribution (E1), publicly/non-traded distinction (E2), non-traded REIT risks (E3), Reg A (E4), K-1 (E5), ordinary-income dividend (E6), 4%+ yield 2026 (E8) |
| Regulatory claims in evidence.md | PASS - REIT structures (E1, E2, E3), Reg A (E4), K-1 (E5), 199A reference present in body (medium confidence per E6 note) |
| Return claims paired with risk disclosure same section | PASS - QuickAnswer footer, choose-reit + choose-fractional caveats, FAQ "no guarantees" language, full disclaimer block |
| No "guaranteed return" | PASS - phrase does not appear | <!-- check-rules: allow -->
| Federal references accurate per evidence | PASS - investor.gov language directly quoted in evidence |
| No misleading regulated vs unregulated comparison | PASS - REIT and fractional both correctly framed as SEC-regulated securities under different structures |

## B. SEO & GEO structure

| Item | Status |
|------|--------|
| Frontmatter complete | PASS |
| title 55-60 chars, focus keyword first third | PASS - "Fractional Real Estate vs REIT: Complete 2026 Comparison" = 56 chars; focus keyword chars 1-29 |
| meta_description 150-160 chars | PASS - 152 chars; includes focus keyword + CTA verb ("explained", "Which structure fits") |
| canonical set | PASS - https://psfnetwork.com/blog/reits-vs-fractional-real-estate |
| hero_visual_alt 60-120 chars | PASS - 99 chars |
| H1 unique, contains focus keyword | PASS - "Fractional Real Estate vs REIT: Which Is Right for You?" |
| H2s question format | PASS - all 6 H2s are questions |
| QuickAnswer block at top | PASS, 4 stat cards + risk footer |
| Each capsule 50-75 words | PASS - 61/68/59/65/70/54 |
| FAQ Q/A pairs minimum 5 | PASS - 6 pairs |
| At least 2 internal links to existing posts | PASS - 3 internal links; hub (fractional-real-estate-investing) and how-to-build-passive-income are published; best-fractional-real-estate-platforms exists as brief |
| External links from evidence.md | PASS - 8 Sources, all from evidence |

## C. Brand & content quality

| Item | Status |
|------|--------|
| PSFnetwork lowercase throughout | PASS |
| No em or en dashes | PASS |
| Tone matches `brand/tone-and-voice.md` | PASS - second person, neutral, anti-hype |
| No contradictions | PASS |
| No orphaned sentences | PASS |
| Author + reviewer match `brand/personas.md` | PASS - Maya Reyes, Daniel Cho, CFA |
| Disclaimer matches canonical | PASS - exact match |
| All template components present in order | PASS |

## D. Template completeness

| Item | Status |
|------|--------|
| ArticleHero metadata in frontmatter | PASS - type: Comparison, topic: REITs |
| HeroVisual placeholder | PASS - [VISUAL-HERO-01] |
| QuickAnswer 4 stat cards | PASS - Daily, 5-10 years, Over 4%, $20 |
| Opening 2 paragraphs no headers | PASS |
| Sources numbered references evidence | PASS - 8 entries |
| AuthorCard, Disclaimer, CTABlock, Related | PASS |
| Related exactly 3 internal links | PASS |

---

## Summary

| Section | Total | Pass | Fail |
|---------|-------|------|------|
| A | 6 | 6 | 0 |
| B | 12 | 12 | 0 |
| C | 8 | 8 | 0 |
| D | 7 | 7 | 0 |
| **Total** | **33** | **33** | **0** |

QA_RESULT: PASS
FAILED_ITEMS: []
PASS_ITEMS: 33
RECOMMENDATION: PUBLISH

Loop count: 0. Proceeding to Stage 8.
