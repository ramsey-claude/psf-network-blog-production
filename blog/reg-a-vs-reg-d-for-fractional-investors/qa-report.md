# QA Report: Reg A vs Reg D for Fractional Investors

**Stage:** 7 (Pre-publish QA)
**Date:** 2026-05-15

## Section A: YAML frontmatter

| Field | Status | Value |
|-------|--------|-------|
| title | PASS | 58 chars (target 55-60) |
| slug | PASS | reg-a-vs-reg-d-for-fractional-investors |
| type | PASS | Explainer |
| topic | PASS | Regulation |
| author | PASS | Maya Reyes, Senior Editor (standing persona) |
| reviewer | PASS | Daniel Cho, CFA (standing persona) |
| read_time | PASS | 9 min |
| published | PASS | 2026-05-15 |
| updated | PASS | 2026-05-15 |
| focus_keyword | PASS | "reg a vs reg d" |
| secondary_keywords | PASS | 4 entries |
| meta_description | PASS | 155 chars (target 150-160) |
| canonical | PASS | https://psfnetwork.com/blog/reg-a-vs-reg-d-for-fractional-investors |
| hero_visual_alt | PASS | descriptive, ~190 chars |

## Section B: Component structure

| Component | Present |
|-----------|---------|
| ArticleHero (H1 + dek) | PASS |
| HeroVisual placeholder `[VISUAL-HERO-01]` | PASS |
| QuickAnswer + 4 stat cards | PASS |
| Opening (2 paragraphs) | PASS |
| H2 sections (7 question-format) | PASS |
| FAQ (6 Q/A) | PASS (minimum 5) |
| Sources (9 numbered, all SEC/investor.gov/EDGAR) | PASS |
| AuthorCard | PASS |
| Disclaimer | PASS |
| CTA | PASS |
| Related (3 internal links) | PASS |

## Section C: Answer capsule lengths (50-75 words)

| Section | Words | Status |
|---------|-------|--------|
| Reg A + tiers | 60 | OK |
| Reg D + 506(b)/(c) | 56 | OK |
| Accredited investor | 65 | OK |
| Disclosure / protections | 70 | OK |
| Offering caps + timing | 65 | OK (initially 83; trimmed in Stage 7) |
| Which framework do platforms use | 64 | OK |
| PSFnetwork specifically | 66 | OK |

## Section D: Content quality

| Check | Status |
|-------|--------|
| Disclaimer boilerplate ("Past performance...loss of principal") | PASS |
| Standing personas only (no invented bylines) | PASS |
| Sources are primary regulatory (SEC, Investor.gov, EDGAR) | PASS, 9 sources, 0 marketing-page citations for regulatory facts |
| Every claim in claim-inventory.md maps to evidence row | PASS, 25 claims → 20 evidence rows |
| US-only scope (no non-US regulatory references) | PASS |
| Balanced framing (no "Reg A safer than Reg D" claim) | PASS, explicit "neither framework is 'safer'" in FAQ and reinforced at end of Section 4 |
| Stage 3 consensus changes applied | PASS, all 5 changelog items reflected in draft |

## Section E: Hub linkage

- Hub: fractional-real-estate-investing, referenced in Related ✓
- Sister spokes: how-fractional-real-estate-is-taxed (just-published K-1 post, natural complement), real-estate-crowdfunding-vs-fractional ✓

## Failures fixed within Stage 7 (no loop)

| Issue | Original | Fixed value |
|-------|----------|-------------|
| Title length | 53 chars (under floor) | 58 chars |
| Meta description length | 143 chars (under floor) | 155 chars |
| Section 5 capsule length | 83 words (over cap) | 65 words |

All three fixes are within the Stage 7 micro-fix budget. Loop count remains 0/3.

## Verdict

**PASS → Stage 8 (Publish).**

- HIGH issues: 0
- MED issues open: 0 (all resolved by Stage 4)
- Loop iterations used: 0
- Loop budget remaining: 3
