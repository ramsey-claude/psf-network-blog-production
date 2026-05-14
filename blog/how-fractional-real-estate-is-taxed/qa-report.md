# QA Report: How Fractional Real Estate Is Taxed

**Stage:** 7 (Pre-publish QA)
**Date:** 2026-05-15
**Verifier:** Stage 7 automated checks + manual cross-reference

## Section A — YAML frontmatter

| Field | Status | Value |
|-------|--------|-------|
| title | PASS | 57 chars (target 55-60) |
| slug | PASS | how-fractional-real-estate-is-taxed |
| type | PASS | Explainer |
| topic | PASS | Tax |
| author | PASS | Maya Reyes, Senior Editor (standing persona) |
| reviewer | PASS | Daniel Cho, CFA (standing persona) |
| read_time | PASS | 9 min |
| published | PASS | 2026-05-15 |
| updated | PASS | 2026-05-15 |
| focus_keyword | PASS | "how is fractional real estate taxed" |
| secondary_keywords | PASS | 4 entries |
| meta_description | PASS | 154 chars (target 150-160), includes focus keyword variant + CTA |
| canonical | PASS | https://psfnetwork.com/blog/how-fractional-real-estate-is-taxed |
| hero_visual_alt | PASS | descriptive, ~140 chars |

## Section B — Component structure

| Component | Present | Notes |
|-----------|---------|-------|
| ArticleHero (H1 + dek) | PASS | H1 matches title; dek 1 sentence, no terminal period |
| HeroVisual placeholder | PASS | `[VISUAL-HERO-01]` present |
| QuickAnswer | PASS | ~110-word summary + 4 stat cards |
| Opening | PASS | 2 paragraphs, no internal headings |
| H2 sections | PASS | 7 question-format H2s, each with answer capsule |
| FAQ | PASS | 6 Q/A pairs (minimum 5) |
| Sources | PASS | 9 numbered sources, all IRS or SEC |
| AuthorCard | PASS | Maya Reyes byline + Daniel Cho review credit |
| Disclaimer | PASS | Standard psfnetwork disclaimer + tax-specific addendum |
| CTA | PASS | Action-oriented, links to offering circular review |
| Related | PASS | 3 internal links to existing slugs |

## Section C — Answer capsule lengths (50-75 words)

| Section | Words | Status |
|---------|-------|--------|
| K-1 or 1099? | 68 | OK |
| What's on a K-1? | 75 | OK |
| Depreciation pass-through | 68 | OK |
| K-1 arrival timing | 73 | OK |
| Multi-state filing | 66 | OK |
| Sale or exit | 70 | OK (initially 77; trimmed in Stage 7 fix) |
| psfnetwork specifically | 73 | OK |

## Section D — Content quality

| Check | Status |
|-------|--------|
| Disclaimer boilerplate ("Past performance...loss of principal") | PASS |
| Standing personas only (no invented bylines) | PASS |
| Sources are primary regulatory (IRS, SEC) | PASS — 8 IRS + 1 SEC; no marketing pages cited for regulatory facts |
| Every claim in claim-inventory.md maps to evidence row | PASS — 24 claims → 15 evidence rows (some rows cover multiple claims) |
| US-only scope (no non-US regulatory references) | PASS |
| "Consult your CPA" framing on actionable items | PASS — present in 7 of 7 H2 sections plus FAQ Q1, Q2 |
| Stage 3 consensus changes applied | PASS — all 7 changelog items reflected in draft |

## Section E — Hub linkage

- Hub: fractional-real-estate-investing — referenced in Related ✓
- Sister spokes: real-estate-crowdfunding-vs-fractional, reits-vs-fractional-real-estate — referenced in Related ✓
- Inbound link from hub (when next hub update is published): TBD, not part of this run

## Failures fixed within Stage 7 (no loop)

| Issue | Original | Fixed value |
|-------|----------|-------------|
| Title length | 63 chars (over) | 57 chars (within) — alternative title from outline used |
| Section 6 capsule length | 77 words (over) | 70 words (within) — trimmed redundant phrasing |

Both fixes are within the "tight tightening" budget of Stage 7 (≤2 micro-edits without invoking a loop back to Stage 4). Loop count remains 0/3.

## Verdict

**PASS → Stage 8 (Publish).**

- HIGH issues: 0
- MED issues open: 0 (all resolved by Stage 4)
- Loop iterations used: 0
- Loop budget remaining: 3
