# Pre-publish QA Gate

Stage 7. Verifies items that can be checked from the markdown file before commit. Post-publish items live in `qa-gate-post-publish.md`.

## How to use

Work through every item. Mark each PASS or FAIL. Use the routing table to decide where a FAIL goes - blanket restart from Stage 1 is not the default.

## Checklist

### A. Financial accuracy (sourced)

- [ ] Every numerical claim has an entry in `evidence.md`
- [ ] Every regulatory claim has an entry in `evidence.md`
- [ ] All investment return claims include a risk disclosure within the same section
- [ ] No "guaranteed return" language anywhere
- [ ] FDIC, SEC, CFTC, FINRA, Fed references factually accurate per evidence
- [ ] No misleading comparisons between regulated and unregulated products

### B. SEO & GEO structure

- [ ] Title tag 55-60 characters, focus keyword in the first third
- [ ] Meta description 150-160 characters, includes CTA and keyword
- [ ] H1 unique, contains focus keyword
- [ ] H2s in question format
- [ ] TL;DR or summary block present at top
- [ ] Every H2 has an answer capsule of 50-75 words
- [ ] FAQ section structured for FAQ schema (Q/A pairs)
- [ ] At least 2 internal links to relevant posts that actually exist in the repo
- [ ] All external links point to high-authority sources from `evidence.md`

### C. Brand & content quality

- [ ] Brand name written as psfnetwork throughout
- [ ] No em dashes or en dashes
- [ ] Tone matches `brand/tone-and-voice.md`
- [ ] No contradictions within the content
- [ ] No orphaned sentences or incomplete paragraphs
- [ ] Author name and review credit present
- [ ] Disclaimer block present and complete

### D. Localization (if applicable)

- [ ] Financial terms preserved per `checklist/localization-guide.md`
- [ ] Register consistent throughout (siz / vous / formal)
- [ ] Currency formatting correct for the target market
- [ ] Each localized variant has its own `draft-[market].md`

## Routing on FAIL

Do not blindly restart from Stage 1. Route by failure type:

| Failed section | Route to |
|----------------|----------|
| A. Financial accuracy - claim unsourceable | Stage 1 (Research) |
| A. Financial accuracy - source exists but wording wrong | Stage 4 (Revision) |
| B. SEO & GEO structure | Stage 4 (Revision) |
| C. Brand & content quality | Stage 4 (Revision) |
| D. Localization | Stage 5 (Localization) |

Loop budget is shared with Stage 3. If `loop_count > 3` at any failure: set `stage: "manual-review-required"` and stop.

## Outputs

`qa-report.md` with PASS/FAIL per item, failure reasons, routing decision, and final recommendation (PUBLISH / ROUTE_TO_STAGE_X / HALT).
