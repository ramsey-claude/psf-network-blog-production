# Stage -2 - Topic Discovery & Brief/Outline Generation

Runs only when Stage -1 returns "no ready candidate" (every existing slug under `blog/` is already published or in flight, and no brief.md+outline.md pair is available to feed Stage 0). Generates a fresh `brief.md` + `outline.md` for the next-best topic so Stage -1 can pick it up immediately.

This stage exists to make batch runs ("10 blog yaz") self-sustaining without requiring the operator to author briefs by hand.

## Inputs

- `ROADMAP.md`, Step 2 (Content Gap Analysis), Step 3 (Priority Posts), Phase 1 Execution Tracker.
- All existing `blog/*/brief.md` keyword tables (to avoid cannibalization with seeds being considered).
- `brand/tone-and-voice.md`, brand voice for the angle and ICP framing.
- `brand/personas.md`, author + reviewer to use in the new outline's Template Mapping.
- Operating scope: US-only audience, English-only content. Filter all candidates accordingly.

## Sub-steps

### 1. Candidate scan

Source the candidate pool from ROADMAP Step 2 (Content Gap Analysis) plus any topic the operator has explicitly noted but not yet briefed.

Filter rules (apply in order):
1. Drop any candidate that conflicts with US-only scope (International, Gulf/UAE, non-US regulatory frames).
2. Drop any candidate whose focus keyword already appears as the focus of a published or in-flight `brief.md`.
3. Drop any candidate whose entire keyword set overlaps an existing brief by 2+ entries (same as Stage 1 SOFT cannibalization rule applied upstream).

Among the remaining candidates, rank by:
1. Hub-supporting: does this topic naturally link back to the published hub? Spokes preferred.
2. KD/Volume score: `Volume / (KD + 1)`, higher is better.
3. Type weight: Comparison or Definitional Spoke > Listicle.
4. Brand fit: does the topic let psfnetwork's per-square-foot model show up naturally?

Pick the top candidate. Record runner-up for transparency.

### 2. Keyword validation

WebSearch the proposed focus keyword (US locale). Confirm:
- At least 3 distinct organic competitors rank for it (so demand is real).
- No single dominant competitor owns top 3 + answer box (avoid clearly losing battles).
- The keyword phrase makes sense as a standalone Google query.

If any of these fail, fall back to the runner-up. If both fail, halt with `topic-generation-exhausted` and a one-paragraph note recommending the operator add new gap analysis to ROADMAP.

### 3. Brief generation

Write `blog/[new-slug]/brief.md` following the schema used by Phase 1 briefs. Required sections in order:

```markdown
# Brief: [Title]

## Metadata
| Field | Value |
|-------|-------|
| Slug | [new-slug] |
| Type | Spoke / Supporting / Hub (rarely - hubs are authored, not auto-generated) |
| Priority | next available integer after the current Phase max |
| Status | Brief |

## Target Keywords
| Keyword | Volume | KD | Intent |
|---------|--------|-----|--------|
| [focus keyword] | [from WebSearch signal or TBD with note] | [TBD with note] | I / C / N |
| ... 4-5 secondary keywords ... |

## ICP
[US-only audience description, 2-4 sentences, references psfnetwork ICP from existing briefs]

## Content Angle
[2-3 sentences. Position psfnetwork's structural advantages without being promotional.]

## Competitor Gap
- [Specific competitor URL with traffic estimate if from ROADMAP Step 1]
- [Why this gap exists]
- [Why psfnetwork can win it]

## SEO Notes
- Focus keyword placement rules
- FAQ schema requirement
- Internal links to existing slugs
- Featured snippet target (if applicable)

## Regulatory Flags for Expert Review
- [Which regulators are in scope per topic - SEC default, others as needed]
- [Specific phrases or claims that need careful framing]
```

Constraints:
- Never invent a specific Volume / KD number. If WebSearch only gives qualitative signal, use "TBD - WebSearch indicates [signal]" rather than a fabricated integer.
- Internal links must reference existing slugs in `blog/` (typically the published hub).
- Regulatory flags must match the topic. Default SEC + FINRA + CFPB for investment content; add others only when the topic touches their domain.

### 4. Outline generation

Write `blog/[new-slug]/outline.md`. Required sections in order:

```markdown
# Outline: [Title]

## Template Mapping
| Component | Content |
|-----------|---------|
| Type tag | Explainer / Comparison / Guide / Listicle |
| Topic tag | [Single topic tag, e.g. "Fractional Ownership"] |
| H1 | [Working H1, will be finalized in Stage 2] |
| Dek | [One sentence subtitle] |
| Author | Maya Reyes, Senior Editor |
| Reviewer | Daniel Cho, CFA |
| Read time | [Estimated minutes] |

## QuickAnswer (60 sec)
[~80-110 word summary of the full post]

**4 Stat Cards:**
- [Number / unit] - [label]
- [Number / unit] - [label]
- [Number / unit] - [label]
- [Number / unit] - [label]

## Sections

### 1. [Question-format H2] (id: [kebab-id])
**Answer capsule:** [50-75 word placeholder description of what the capsule should say]
Body: [1-2 sentence description of the body content for Stage 2]
Optional: [Chart, pull quote, table reference]

[Repeat for 5-7 sections]

### N. FAQ (id: faq)
1. [Question 1]
2. [Question 2]
3. [Question 3]
4. [Question 4]
5. [Question 5]
6. [Question 6 - optional]

## Charts / Framer Components
- [Chart 1 description if applicable]
- [Chart 2 if applicable]

## Internal Links
- -> [existing-slug-1]
- -> [existing-slug-2]
- -> [existing-slug-3]

## Sources Needed
1. [Federal source 1 - e.g., investor.gov]
2. [Federal source 2]
3. [Industry source]
```

Constraints:
- 4 Stat Cards exact, required by the template.
- 5-7 H2 sections in question format. Last section is always FAQ (not counted in 5-7).
- FAQ has 5-6 Q&A pairs minimum.
- Internal Links reference existing slugs only (not yet-to-be-generated ones).
- Sources Needed names sources, not specific URLs, those come from Stage 1.
- Stat card values: use "TBD - illustrative" if the underlying number requires sourcing in Stage 1.

### 5. Commit and loop back

After writing both files locally and validating their structure (frontmatter-free brief, outline with all required sections), push them to GitHub as a single commit:

```
feat(brief): generate brief + outline for [new-slug] - Stage -2 auto

Brief and outline auto-generated from ROADMAP gap analysis seed:
[seed topic name + rationale]
```

Then loop back to Stage -1. Stage -1 will now see the new slug as eligible and pick it (it is the highest-priority eligible candidate because it was just generated to be the next-best).

## Validation gate

After generation, before commit:
- `brief.md` has all required sections.
- `outline.md` has Template Mapping with all rows, QuickAnswer with 4 stat cards, 5-7 H2 sections in question format, FAQ with 5+ Q&A pairs, Internal Links.
- No keyword in the brief's Target Keywords table appears as the focus keyword of an existing brief.
- No invented dollar figure or percentage; uses "TBD" / "illustrative" where the number is not yet sourced.

If validation fails, retry generation once. If second attempt fails, halt with `topic-generation-validation-failed` and dump the rejected draft to `blog/_failed-generation/[timestamp]/` for operator review.

## Halt conditions

- `topic-generation-exhausted`: every candidate from ROADMAP gap analysis has either been published, is in flight, or fails US-only / cannibalization filters. Operator must add new gap analysis to ROADMAP before another Stage -2 invocation succeeds.

## Soft-fail conditions (do NOT halt the batch)

The following conditions skip the current candidate and immediately try the next-best from the candidate pool, so a batch run does not stall on a single unlucky topic:

- `validation-failed-after-retry`: two consecutive generation attempts produced invalid brief/outline structure. Log the rejected drafts to `blog/_failed-generation/[timestamp]-[slug]/` for later review, then move to the next candidate.
- `keyword-validation-failed-after-retry`: WebSearch on the focus keyword returned no useful signal twice. Move to next candidate.
- `webfetch-permission-prompt-on-validation`: a competitor URL is not in the allowlist and would prompt the operator. Skip the URL, use available WebSearch signal alone, continue.

If the candidate pool is then exhausted by repeated soft-fails, halt with `topic-generation-exhausted` as above.

## Why this exists

For batch runs ("yaz 10 blog"), Stage -1 alone would halt after Phase 1's 6 priority slugs are exhausted. Stage -2 makes the queue self-replenishing within the operator's strategic frame (the ROADMAP gap analysis), without requiring the operator to author briefs by hand mid-batch.

Topic generation is rules-based and seed-bounded, Stage -2 cannot invent topics outside the ROADMAP frame, which keeps psfnetwork's content strategy under operator control.

## What this stage does NOT do

- Invent topics outside the ROADMAP gap analysis.
- Skip US-only / cannibalization filters.
- Author content beyond the brief and outline (that is Stage 2's job, with full sourcing in Stage 1).
- Set Priority to 1 (Hub), hubs are operator-authored decisions.
- Use Maya Reyes or Daniel Cho in any quote or voice (those personas only appear in published content, not in briefs).
