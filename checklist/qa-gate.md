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

- [ ] Brand name written as PSFnetwork throughout
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

### E. Grammar and readability

Added 2026-05-26 after customer feedback flagged "grammatical errors and mobile formatting issues" on a v2 humanized doc that Stage 7 had previously cleared. Sections A through D do not catch grammar; this section does.

- [ ] `python3 workflow/check-rules.py blog/[slug]/draft-vN.md` returns zero BLOCKING and zero grammar-tier WARNINGs (`grammar-comma-splice`, `grammar-hyphen-as-emdash`, `grammar-bare-comparative`, `grammar-runon`)
- [ ] No comma splices in body prose (heuristic flag: comma followed by independent-clause pronoun starting a new clause)
- [ ] No hyphen-as-em-dash constructions (single hyphen surrounded by spaces between lowercase words)
- [ ] No bare comparatives missing a standard ("the bigger X than Y realize" type)
- [ ] No run-on sentences (heuristic: 40+ words, 3+ commas, no semicolon)
- [ ] Wide tables fit a phone screen. 6+ column tables are restructured to 4 columns max, with non-critical columns folded into a narrative paragraph below. The 6-column comparison table flagged on 2026-05-26 was the failure mode this rule prevents.
- [ ] Optional deeper check: run LanguageTool against the draft if Java is available in the pipeline venv. Recipe: `pip install language-tool-python; python -c "import language_tool_python; t = language_tool_python.LanguageTool('en-US'); print(t.check(open('blog/[slug]/draft-vN.md').read()))"`. Not required for PASS but recommended before any externally visible delivery.

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
