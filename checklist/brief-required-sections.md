# Brief: Required Sections

Every blog brief (`blog/[slug]/brief.md`) must contain the sections listed here before the pipeline triggers. Stage -2 (topic generation) is responsible for filling them. Stage 2 (Draft) refuses to start if any required section is missing or marked TODO.

This document defines the new required `Human Anchors` section that addresses the AI-generated feel of earlier posts. The other sections preserve the existing brief format.

---

## Section order

1. Title
2. Metadata
3. Target Keywords
4. ICP
5. Content Angle
6. **Human Anchors** *(NEW, required as of v3)*
7. Competitor Gap
8. SEO Notes
9. Regulatory Flags for Expert Review

---

## Human Anchors: required content

This is the most important addition to the brief. It is the raw material that the writer and humanization reviewer use to break AI cadence.

The section must contain three sub-fields. Each is a 2-4 sentence input from a real human source (founder, ops lead, investor relations, or a documented investor conversation).

### A. Real Story

A specific scenario from psfnetwork's actual operations or investor base. Anonymize if needed, but keep the specifics: city, profession, dollar figure, date, outcome.

Bad: "Many investors have had positive experiences."
Good: "Marcus, a 38-year-old physical therapist in Austin, put $7,200 into three fractional shares of a duplex in Q3 2024. His first quarterly distribution was $94. He told us he didn't believe it would actually arrive until it did."

### B. POV Anchor

A position psfnetwork holds that not every competitor would agree with. One paragraph. First person plural ("we") is allowed and encouraged for this field.

Bad: "We think fractional real estate is important."
Good: "We think the per-square-foot model is the only fractional structure that lets a first-time investor understand exactly what they own. Crowdfunding gives you a slice of a fund. We give you a number of square feet, in a specific building, at a specific address."

### C. Contrarian Note

The standard industry narrative on this topic, followed by where psfnetwork breaks with it. Two short paragraphs.

Bad: "Some people disagree about fractional real estate."
Good: "The standard pitch from REITs is that they offer real estate exposure with stock-like liquidity. The catch they don't lead with: REIT pricing tracks the stock market, not the underlying property. A REIT can fall 30% in a quarter even if every property in its portfolio is fully occupied and rent-paying. Our fractional model isolates the investor from market sentiment by construction, the share is tied to the asset, not to a ticker."

---

## Source authority

The brief author is whoever runs Stage -2 (topic generation). For autonomous runs, that is Claude. For operator-initiated runs, that is Onur.

Neither role has authority to invent Human Anchor content. Anchors come from:

- **Real Story:** investor relations call notes, support transcripts, founder anecdotes. Requires an operator-attested source line.
- **POV Anchor:** the operator's written record of what psfnetwork stands for on this topic. Lives in `brand/voice-samples/` (founder essays, public statements) or the operator's interview notes.
- **Contrarian Note:** the operator's written critique of the industry's default framing for this topic. Same source as POV Anchor.

If none of the above are available for a topic, Stage -2 halts with `human-anchor-source-missing` and produces no brief. The operator provides the source material via a Slack DM, an interview transcript, or a curated set of investor stories. Brief generation does not proceed otherwise.

## How to source Human Anchors

If the brief author does not have direct input from a real psfnetwork source, they must request one before submitting the brief. Acceptable sources:

- Slack message or transcript from a psfnetwork team member (with permission to use)
- Investor relations call notes (anonymized)
- Founder/exec interview snippets
- Direct customer support transcripts (anonymized)
- Logged conversations from `brand/voice-samples/` if relevant

Brief author cannot invent the anchors. If invented anchors slip through, Stage 2.5 (humanization) will flag and Stage -2 cycles for a new brief.

---

## Format example

```markdown
## Human Anchors

### A. Real Story
[2-4 sentences with named/anonymized subject, city, dollar figure, date, outcome]

### B. POV Anchor
[1 paragraph stating a position psfnetwork holds; "we" allowed]

### C. Contrarian Note
[2 short paragraphs: standard industry view, then where psfnetwork breaks with it]

### Source
[Where the anchors came from, Slack thread, IR call, founder interview, etc. Permission/approval status.]
```

---

## Validation

Stage 2 (Draft) runs a pre-flight check on the brief:

- All three Human Anchor sub-fields present
- Each sub-field at least 40 words
- "Source" field populated
- No placeholder text ("TODO", "TBD", "[insert here]")

If any check fails, Stage 2 does not start. The brief returns to Stage -2 for completion.

---

## Migration note for existing briefs

Briefs created before this template version do not have Human Anchors. They can be migrated in place at any time. Migration does not require re-running earlier stages, it adds the required input for any future pipeline run on that slug.

For existing published posts, no retroactive change is required. The humanization pass applies to new and re-published posts only.
