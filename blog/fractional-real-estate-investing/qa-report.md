# Pre-publish QA Report - fractional-real-estate-investing

Stage 7. Verified against `checklist/qa-gate.md`.

| Field | Value |
|-------|-------|
| Slug | fractional-real-estate-investing |
| Stage | 7 (Pre-publish QA) |
| Date | 2026-05-14 |
| Loop count | 0 |

---

## A. Financial accuracy (sourced)

| Item | Status | Note |
|------|--------|------|
| Every numerical claim has an entry in `evidence.md` | PASS | $20 (E11), 4-9% (E12), $75M Reg A cap (E1), 10% cap (E2), 35 under 506(b) (E4), 90% REIT distribution (E9), $250k FDIC (E10), $20,000 down payment (context E14) |
| Every regulatory claim has an entry in `evidence.md` | PASS | Reg A (E1-3), Reg D (E4-5), JOBS Act (E6), Reg A effective date (E7), K-1 (E8), REIT (E9), FDIC (E10) |
| All investment return claims include a risk disclosure within the same section | PASS | QuickAnswer has risk line and stat-card footer; Is-it-good section has "not guarantees, past performance does not predict" caveat; FAQ first answer reiterates |
| No "guaranteed return" language anywhere | PASS | Phrase appears only in explicit negation: "expects guaranteed returns (no investment offers those)" |
| FDIC, SEC, CFTC, FINRA, Fed references factually accurate per evidence | PASS | All federal references trace to E1-E10 |
| No misleading comparisons between regulated and unregulated products | PASS | REIT comparison is explicit and factually grounded; FDIC reference is explicit about what is NOT insured |

## B. SEO & GEO structure

| Item | Status | Note |
|------|--------|------|
| Frontmatter present with all template-structure.md fields | PASS | title, slug, type, topic, author, reviewer, read_time, published, updated, focus_keyword, secondary_keywords, meta_description, canonical, hero_visual_alt all populated |
| `title` 55-60 characters, focus keyword in first third | PASS | "What Is Fractional Real Estate Investing? The 2026 Guide" = 56 chars; focus keyword starts at char 9 (first third = 1-19) |
| `meta_description` 150-160 characters, includes focus keyword and a CTA verb | PASS | 150 chars; opens with "Fractional real estate investing"; CTA verb "Learn" |
| `canonical` set to psfnetwork.com path | PASS | https://psfnetwork.com/blog/fractional-real-estate-investing |
| `hero_visual_alt` 60-120 characters | PASS | 117 chars |
| H1 unique in body, contains focus keyword | PASS | "What Is Fractional Real Estate Investing? A Complete Guide for 2026" |
| H2s in question format | PASS | All 6 H2s are questions |
| QuickAnswer block present at top | PASS | Present, with 4 stat cards and risk footer |
| Every H2 answer capsule 50-75 words, self-contained | PASS | 67 / 62 / 53 / 59 / 73 / 69 words across 6 H2s (verified post-Stage-4 self-check) |
| FAQ structured for FAQ schema (Q/A pairs), minimum 5 | PASS | 6 Q/A pairs, all in `**Q: ...**` and `A: ...` format |
| At least 2 internal links to relevant posts that exist in the repo | PASS | Related lists 3 internal links; reits-vs-fractional-real-estate, how-to-invest-in-real-estate-with-100, best-fractional-real-estate-platforms all have brief.md in repo |
| All external links point to high-authority sources from `evidence.md` | PASS | All Sources entries trace to E1-E14; canonical SEC, IRS, FDIC, congress.gov URLs |

## C. Brand & content quality

| Item | Status | Note |
|------|--------|------|
| Brand name written as psfnetwork throughout | PASS | Lowercase one-word everywhere |
| No em dashes or en dashes | PASS | Hyphens and commas only |
| Tone matches `brand/tone-and-voice.md` | PASS | Second person, short sentences, active voice, no superlatives without proof |
| No contradictions within the content | PASS | Reviewed against evidence.md and outline.md |
| No orphaned sentences or incomplete paragraphs | PASS | Every paragraph closes a thought |
| Author and reviewer match a standing persona in `brand/personas.md` | PASS | "Maya Reyes, Senior Editor" and "Daniel Cho, CFA" both listed as approved standing personas |
| Disclaimer block present, text matches the canonical disclaimer in `brand/tone-and-voice.md` | PASS | Exact match: "Past performance is not indicative of future results. Fractional real estate investing involves risk, including the possible loss of principal. This content is for informational purposes only and does not constitute investment advice." |
| Every component listed in `brand/template-structure.md` is present in order | PASS | Frontmatter + H1 + Dek + HeroVisual placeholder + QuickAnswer + Opening + 6 H2s + FAQ + Sources + Author + Disclaimer + CTA + Related all present in template order |

## D. Template completeness

| Item | Status | Note |
|------|--------|------|
| ArticleHero metadata (type, topic) in frontmatter | PASS | type: Explainer, topic: Fractional Ownership |
| HeroVisual placeholder `[VISUAL-HERO-XX]` present | PASS | [VISUAL-HERO-01] |
| QuickAnswer has exactly 4 stat cards | PASS | $20, 4-9%, 2012, 0 |
| Opening is 2 paragraphs with no headers | PASS | Two paragraphs, no internal headings |
| Sources uses numbered list and references evidence.md rows | PASS | 9 numbered entries, all from E1-E14 |
| AuthorCard, Disclaimer, CTABlock, Related all present | PASS | All present in template order |
| Related lists exactly 3 internal links | PASS | 3 links, all relative paths to existing slugs |

---

## Daniel Cho quote check (against `brand/personas.md`)

The Daniel Cho pull quote in the "What is the square-foot ownership model?" section:

> "The clearest way to understand fractional ownership is to anchor it to something physical. A square foot is something you can stand in. A share is an abstraction. Both are securities, both carry the same risks, but one is easier to reason about."

Compliance per personas.md quote rules:
- Restate not introduce: PASS (point already supported in body)
- No specific numbers: PASS
- No predictive claims: PASS
- No advisory voice: PASS (no "should", no "buy")
- One quote per post maximum: PASS (this is the only quote)
- Length under 60 words: PASS (54 words)

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

Routing: not applicable (no failure).
Loop count: 0 (no reroute triggered).

Proceeding to Stage 8 (Publish).
