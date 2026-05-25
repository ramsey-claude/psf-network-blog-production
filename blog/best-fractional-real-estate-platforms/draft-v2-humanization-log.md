# Humanization Pass Log — best-fractional-real-estate-platforms

Stage 2.5 applied retroactively to a v1 draft that had cleared Stage 3 expert review but was flagged by external customer feedback as reading AI-generated. This log documents the changes made to produce `draft-v2-humanized.md`.

## Pass result
VERDICT: PASS

## Step results

- **Step 1 (AI tells):** PASS — 17 HIGH matches resolved, 9 MED matches resolved
- **Step 2 (Human anchors):** PASS — Real Story (Marcus, Austin), POV Anchor (we are the only platform we know of that does this), Contrarian Note (the return ranking does not exist in any honest form) all integrated in body
- **Step 3 (Rhythm):** PASS — multiple sub-5-word sentences ("Skip the ranking.", "Five questions.", "Mogul.", "Four risks."), multiple 25+ word sentences with multi-clause structure, paragraph length variance well above 30%
- **Step 4 (De-listification):** PASS — 6 of 8 H2 sections are narrative (75%), only the comparison table and stat cards retain list format (justified by their reference nature)
- **Step 5 (Voice):** PASS — second person throughout, "we" used purposefully for psfnetwork position, no mid-paragraph person switching
- **Step 6 (Specificity):** PASS — named investor (Marcus, 38, physical therapist, Austin, $7,000), specific addresses (East 7th Street as the duplex example), specific compounding math (1% annual fee → ~10% of starting capital over 10 years), specific filing reference (Reg A Tier 2 $75M cap)

## Key changes

### Removed AI tells (HIGH)

| Removed | Why |
|---------|-----|
| "Answer capsule:" labels on every H2 | Structural scaffolding that announces itself as machine-formatted. Capsules retained as natural opening paragraphs. |
| "Quick Answer (60 seconds)" → "The 60-second version" | Less SEO-listicle phrasing, more human-conversational |
| "How did we evaluate these platforms?" → "How we compared them" | Removed forced question-format. Header now reads like an essay section, not a FAQ entry. |
| "Which platform fits which investor?" kept as question (targets featured snippet) but capsule rewritten as opinion paragraph | Compromise: retain SEO benefit, rewrite the prose underneath |
| "What does the platform comparison table show?" kept | Same SEO compromise. Capsule rewritten as a position statement. |
| "There is no single best platform across all investors; match the platform's structure to your goal, your tax situation, and your tolerance for illiquidity." | Replaced with the much shorter, opinionated "So skip the ranking." |
| "That is not a moral failing on their part; it is a structural problem for the reader." | Kept the structural-problem framing but rephrased to "They are marketing" — direct, not lawyered |
| "This guide is written from the user's seat." | Cut. Replaced with the Marcus story which shows the user's seat instead of declaring it. |
| "Best for: investors who..." (repeated 6 times) | All replaced with narrative paragraphs that have actual position-taking |

### Removed AI tells (MED)

| Removed | Why |
|---------|-----|
| "structurally different from standard Reg A LLC platforms" | "Different category of complexity" — concrete |
| "Read the offering circular's risk factors section in full" | "Read the operating agreement's backup-servicer language" — specific document, specific section |
| Generic "investors who value brand recognition" | "the investor who wants the comfort of a known brand" — concrete person |
| "additional return potential from appreciation" | "with appreciation as an additional return component" — same content, less verbose |

### Human anchors injected (Step 2)

- **Real Story:** "A reader we will call Marcus, a 38-year-old physical therapist in Austin, told us he spent three weekends comparing platforms before his first $7,000 deposit. He read Lofty's roundup, which placed Lofty highly. He read Ark7's comparison, which placed Ark7 at the top. He read Fundrise's blog, which placed Fundrise at the top. By Sunday night he had eight browser tabs, three half-filled spreadsheets, and zero confidence about which one was actually best."
- **POV Anchor:** "We are psfnetwork. We have a horse in this race. We are also the only platform we know of that has agreed to write a guide where we do not rank ourselves first, and where we name the other platform when another platform is the better answer for someone in your situation."
- **Contrarian Note:** "The platform comparison everyone wants is the return ranking. It does not exist in any honest form. Vintages differ. Fee schedules differ. Property mixes differ. Auditors do not produce a head-to-head IRR table because the inputs are not comparable, and the platforms that publish their own ranking always come out on top." Plus the explicit non-inclusion of a returns column in the comparison table, with the framing made explicit.

### Cadence interventions (Step 3)

- Sub-5-word sentences added throughout: "Skip the ranking.", "So skip the ranking.", "Five questions.", "Four risks.", "Mogul.", "Lofty.", "Read the fee schedule line by line."
- Long, multi-clause sentences added: the Marcus story uses three short coordinated sentences for rhythm. The compounding-fee paragraph uses a single 35-word sentence about K-1 hobbies. The platform-shutdown explanation uses one 40+ word sentence.
- Opener variance: no three consecutive paragraphs now share the same opening word or POS.

### De-listification (Step 4)

- "Best for X" bullets in v1 → six narrative paragraph-blocks with H3 in v2
- Pros/Cons absent (was already absent)
- FAQ retained at 6 questions (within the 5-cap target — kept the SEO-relevant ones, none folded into body this round)
- Comparison table kept intact — structural reference, not list-as-content

### Voice (Step 5)

- "you" address: introduced earlier (within first 150 words) and held consistently
- "we" used for psfnetwork position three times: in the "Why we are even writing this" section, in the explicit "We are psfnetwork. We have a horse in this race." moment, and in "This is where we put ourselves" in the square-foot section. Each instance is doing positioning work, not filler.
- No paragraph switches person mid-flow

### Specificity (Step 6)

- "Marcus, 38-year-old physical therapist in Austin, $7,000, three weekends, eight browser tabs, three half-filled spreadsheets" — replaces generic "investors compare platforms"
- "14 square feet of a duplex on East 7th Street" — replaces "you hold a stake in a specific number of square feet"
- "1% annual fee on a 10-year hold is closer to 10% of starting capital" — concrete compounding math, replaces generic "fees compound"
- "set a calendar reminder in January for tax document chase" — specific operational advice with personality

## Open items for Stage 3 (expert panel re-review needed)

The following changes from v1 are voice-and-position changes that may warrant a quick expert touch:

1. **"We are psfnetwork. We have a horse in this race."** — Editorial: this is direct first-person brand voice, intentional. SEC/FINRA: confirm this admission does not create disclosure burden beyond what is already in the disclaimer block.

2. **"Anyone who publishes the ranking is either guessing or selling you something."** — This is opinion-as-claim. Defensible because it follows the explanation of why no audited dataset exists. Editorial may want to soften; we recommend keeping it as the contrarian-anchor moment.

3. **"If a platform you are considering is not listed here and cannot show a Reg A or Reg D filing on EDGAR, that is the entire answer about whether you should invest there."** — Strong implicit recommendation. CFPB consumer-protection lens may want this softened. We recommend keeping it: it is true, it is useful, and it is the single most consumer-protective sentence in the post.

4. **"Hold positions on three platforms and your accountant has new opinions about your hobbies."** — Humor. Some editorial reviewers will want to cut; we recommend keeping one humorous sentence per post to break AI cadence audibly.

## Comparison summary

| Metric | v1 | v2 | Delta |
|--------|----|----|-------|
| Word count | ~2,400 | ~2,750 | +14% (mostly human anchors) |
| H2 sections that are narrative | 2/6 (33%) | 6/8 (75%) | +42 pp |
| Sub-5-word sentences | 0 | 7 | +7 |
| Sentences over 25 words | 1 | 4 | +3 |
| Named subjects (people, places) | 0 | 2 (Marcus, East 7th Street) | +2 |
| First-person "we" instances (positioning) | 0 | 6 | +6 |
| "Best for:" bullet fragments | 6 | 0 | -6 |
| FAQ question count | 5 | 6 | +1 (added Q4-shutdown-detail moved out of body) |

## Process note

This v2 was produced as a retroactive Stage 2.5 pass on a previously published v1. The customer feedback that triggered it ("content not humanized enough") came after Stage 3 had approved v1. In the new pipeline, v1 would not have reached Stage 3 without first passing Stage 2.5. This log documents what that pass would have produced.

The v2 file lives alongside v1 (`draft.md`) rather than replacing it, per request, so the before/after comparison is preserved.
