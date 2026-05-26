# Pre-publish QA Gate

Stage 7. Verifies items that can be checked from the markdown file before commit. Post-publish items live in `qa-gate-post-publish.md`.

## How to use

Work through every item. Mark each PASS or FAIL. Use the routing table to decide where a FAIL goes - blanket restart from Stage 1 is not the default.

## Checklist

### A. Financial accuracy (sourced)

- [ ] Every numerical claim has an entry in `evidence.md`
- [ ] Every regulatory claim has an entry in `evidence.md`
- [ ] All investment return claims include a risk disclosure within the same section
- [ ] No "guaranteed return" language anywhere <!-- check-rules: allow -->
- [ ] FDIC, SEC, CFTC, FINRA, Fed references factually accurate per evidence
- [ ] No misleading comparisons between regulated and unregulated products

### B. SEO & GEO structure

- [ ] Frontmatter present with all fields listed in `brand/template-structure.md`
- [ ] `title` field 55-60 characters, focus keyword in the first third
- [ ] `meta_description` field 150-160 characters, includes focus keyword and a CTA verb
- [ ] `canonical` field set to `https://psfnetwork.com/blog/[slug]`
- [ ] `hero_visual_alt` field populated, 60-120 characters
- [ ] H1 unique in body, contains focus keyword
- [ ] H2s in question format
- [ ] QuickAnswer block present at top
- [ ] Every H2 has an answer capsule of 50-75 words (self-contained)
- [ ] FAQ section structured for FAQ schema (Q/A pairs), minimum 5 entries
- [ ] At least 2 internal links to relevant posts that actually exist in the repo
- [ ] All external links point to high-authority sources from `evidence.md`

### C. Brand & content quality

- [ ] Brand name written as psfnetwork throughout
- [ ] No em dashes or en dashes
- [ ] Tone matches `brand/tone-and-voice.md`
- [ ] No contradictions within the content
- [ ] No orphaned sentences or incomplete paragraphs
- [ ] Author and reviewer match a standing persona in `brand/personas.md`. Any other name = FAIL.
- [ ] Disclaimer block present, text matches the canonical disclaimer in `brand/tone-and-voice.md`
- [ ] Every component listed in `brand/template-structure.md` is present in the draft, in order

### D. Template completeness

- [ ] ArticleHero metadata (type, topic) present in frontmatter
- [ ] HeroVisual placeholder line `[VISUAL-HERO-XX]` present
- [ ] QuickAnswer has exactly 4 stat cards
- [ ] Opening is 2 paragraphs with no headers
- [ ] Sources section uses numbered list and references evidence.md rows
- [ ] AuthorCard, Disclaimer, CTABlock, Related blocks all present
- [ ] Related lists exactly 3 internal links

## Routing on FAIL

Do not blindly restart from Stage 1. Route by failure type:

| Failed section | Route to |
|----------------|----------|
| A. Financial accuracy - claim unsourceable | Stage 1 (Research) |
| A. Financial accuracy - source exists but wording wrong | Stage 4 (Revision) |
| B. SEO & GEO structure | Stage 4 (Revision) |
| C. Brand & content quality | Stage 4 (Revision) |
| D. Template completeness | Stage 4 (Revision) |

Loop budget is shared with Stage 3. If `loop_count > 3` at any failure: set `stage: "manual-review-required"` and stop.

## Outputs

`qa-report.md` with PASS/FAIL per item, failure reasons, routing decision, and final recommendation (PUBLISH / ROUTE_TO_STAGE_X / HALT).
