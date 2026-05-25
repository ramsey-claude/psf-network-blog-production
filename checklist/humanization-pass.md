# Humanization Pass — Stage 2.5

A dedicated review stage between the Draft (Stage 2) and the Expert Panel (Stage 3). One reviewer, one job: make the post sound like a person wrote it.

This stage exists because compliance and editorial checks are necessary but not sufficient. A draft can pass every regulator and still read like a model wrote it. The humanization pass is the only stage with the explicit mandate to break AI cadence and inject human signal.

---

## Why this is a separate stage

Editorial review runs inside the Stage 3 expert panel and votes as one of nine voices. Humanization needs more weight than that. By the time the panel sees the draft, the panel is reading for compliance and structure, not voice. If the post still reads as AI after editorial revision, the panel has no leverage to send it back for that reason alone.

Putting humanization before Stage 3 forces the rewrite to happen while the draft is still pliable.

---

## Inputs

- `draft.md` (output of Stage 2)
- `brief.md` (especially the Human Anchors section)
- `brand/tone-and-voice.md`
- `brand/voice-samples/` (3-5 reference pieces from psfnetwork team writing)
- `checklist/ai-tells.md` (ban list)

## Outputs

- `draft.md` (revised in place)
- `humanization-log.md` (what was changed, why, and which checks passed)

---

## The pass — six steps in order

### Step 1 — AI tells sweep

Run the full ban list from `checklist/ai-tells.md`. Resolve every HIGH match. Document MED and LOW resolutions in the log.

**Gate:** zero HIGH matches remaining. Cadence check passes. Voice check passes.

### Step 2 — Human anchor injection

Pull the three Human Anchors from `brief.md`. Each anchor must appear in the body, not as a sidebar or callout:

- **Real story** — one specific scenario with a named (or anonymized but specific) subject, a place, a date, a dollar figure. Woven into the body within the first 60% of the post.
- **POV anchor** — one paragraph or sentence that takes a position. First person plural ("we think", "we've seen") is allowed once per post for this purpose.
- **Contrarian note** — one paragraph that acknowledges the dominant industry view and disagrees with it (or qualifies it). Format: "The standard answer is [X]. Here's where that breaks down."

**Gate:** all three anchors present and integrated. No anchor is a standalone callout box.

### Step 3 — Rhythm and cadence rewrite

Read the draft out loud (or simulate). Apply the Tier 7 rules from the ban list:

- Insert at least one sentence under 5 words
- Insert at least one sentence over 25 words (with multiple clauses, breathing)
- Vary paragraph length — at least one 1-sentence paragraph, at least one 5+ sentence paragraph
- Vary sentence openers — no three consecutive paragraphs starting with the same word or part of speech

**Gate:** cadence check passes per the rules above.

### Step 4 — De-listification

Count H2 sections. At least 40% must be narrative paragraphs, not bullet lists.

For each bullet list:
- If the bullets are fragments, rewrite them as full sentences with periods
- If the list has fewer than 3 items, fold it into a sentence
- If the list is exhaustive (5+ items, all parallel), consider whether a paragraph would read better

Pros/Cons sections: maximum one per post. Prefer a narrative trade-off paragraph.

**Gate:** at least 40% narrative H2s. No fragment bullets. Pros/Cons used at most once.

### Step 5 — Voice consistency

Address the reader as "you" throughout. Do not switch between "you" / "the investor" / "one" within the same paragraph.

If the post needs to refer to a generic third party, name them: "a co-investor", "someone in their first deal", "Lisa, who put $5K into her first share". Generic "investors" is allowed when literally referring to the class, not when the addressee is in that class.

**Gate:** voice check passes. No paragraph switches person.

### Step 6 — Specificity audit

For every claim, the reviewer asks: *would a human writing this know the specific version of this claim?*

- "Many investors" → name a number or remove
- "In recent years" → name the years
- "Real estate has performed well" → which index, which period, what number
- "Some platforms charge fees" → which platforms, what fees

If a specific is not available from `evidence.md`, the claim is generic-tagged. Generic-tagged claims get one of three treatments:
1. Researched and replaced with a specific (preferred — sends back to Stage 1 sub-task)
2. Rewritten as an explicit framing ("There is no industry-standard benchmark for X, but the closest is Y")
3. Cut

**Gate:** zero ungated generic claims. Every generic that survives has a justification in the log.

---

## Reviewer profile

The humanization reviewer is one person (or one model instance with this checklist as its system prompt). They are explicitly not a regulator. Their authority is voice and reader experience. They do not flag compliance issues — those belong to Stage 3.

The reviewer does not negotiate with the writer between revisions. The humanization pass is a single pass with redline output. If the writer disagrees with a specific change, that disagreement is logged and the Stage 3 panel can override.

---

## Output format

The reviewer produces `humanization-log.md` with:

```markdown
# Humanization Pass Log — [slug]

## Pass result
VERDICT: PASS / NEEDS_REWRITE

## Step results
- Step 1 (AI tells): PASS — [N] HIGH matches resolved
- Step 2 (Human anchors): PASS / FAIL — [which anchors present, which missing]
- Step 3 (Rhythm): PASS / FAIL — [which rule failed if any]
- Step 4 (De-listification): PASS / FAIL — [% narrative H2s]
- Step 5 (Voice): PASS / FAIL
- Step 6 (Specificity): PASS / FAIL — [N generic claims, N resolved, N justified]

## Key changes
[List of 5-15 most significant changes, before/after]

## Open items for Stage 3
[Anything the panel should know — e.g., a contrarian claim that needs SEC blessing]
```

---

## Failure mode

If the draft fails NEEDS_REWRITE, it does not go to Stage 3. It goes back to Stage 2 with the humanization log as the rewrite brief. The writer rewrites and re-submits to humanization.

A draft can cycle Stage 2 ↔ Stage 2.5 up to three times before triggering a brief review. If a draft fails humanization three times, the issue is upstream — the brief lacks usable Human Anchors, or the topic is too generic to humanize. Loop back to brief revision.

---

## Why this works

AI-generated content is recognizable not because of any single phrase but because of the absence of friction. Real writing has:

- Sentences of wildly different lengths
- Paragraphs of wildly different sizes
- Specific, idiosyncratic detail that no model would invent
- A position that someone could disagree with
- An admission of trade-off

The humanization pass is the explicit budget for that friction. Without a dedicated stage, friction always gets sanded off by the polish loop.
