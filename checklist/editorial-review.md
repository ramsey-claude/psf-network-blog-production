# Editorial Review

The editorial reviewer runs in every Stage 3 panel. Its job is reader experience and brand voice. Compliance is the regulators' job.

The editorial reviewer is non-removable. Every post passes through this check.

## What editorial checks

### 1. Hook strength

- [ ] The dek and the first paragraph give the reader a reason to keep reading
- [ ] The hook does not waste the first sentence on a definition
- [ ] If the topic is dry, the hook surfaces a number, a contrast, or a specific scenario

### 2. Answer capsules

- [ ] Every H2 has an answer capsule of 50-75 words
- [ ] Each capsule is self-contained - could stand alone if extracted by an AI
- [ ] No capsule depends on a phrase defined earlier in the post

### 3. Narrative flow

- [ ] Sections are in an order a reader would actually follow
- [ ] No section feels bolted on
- [ ] Transitions between sections are not jarring

### 4. Sentence-level clarity

- [ ] Average sentence length under 20 words
- [ ] No sentence longer than 30 words without a clear reason
- [ ] Active voice dominates
- [ ] No filler ("it is important to note", "it should be mentioned", "let us dive in")

### 5. Reader "why do I care"

- [ ] Within the first 200 words, the reader understands what they will get from this post
- [ ] Every section has an implicit "what this means for you"

### 6. Brand voice

- [ ] Second person (you)
- [ ] No corporate hedging language unless legally required
- [ ] Brand terminology consistent with `brand/tone-and-voice.md`

### 7. Banned constructions

- [ ] No em dashes (—) or en dashes (–) anywhere <!-- check-rules: allow -->
- [ ] No "guaranteed return" or synonyms (warranted return, assured return, certain return) <!-- check-rules: allow -->
- [ ] No "PSFnetwork" written with any other casing or spacing
- [ ] No "in conclusion", "in summary", "to wrap up"
- [ ] No "delve", "leverage" (as verb), "synergy", "robust solution" <!-- check-rules: allow -->

## Output format

Same format as regulator reviewers:

```
DOMAIN FINDINGS: [editorial issues identified]
FLAGGED ISSUES: [list with severity HIGH / MED / LOW]
RESPONSE TO PREVIOUS REVIEWERS: [agreements, disagreements, additions on flow or clarity related to their findings]
VERDICT: APPROVE / APPROVE_WITH_NOTES / REVISION_REQUIRED
```

## Severity guide

- **HIGH:** the reader is likely to bounce in the first 200 words; the post buries the answer; the answer capsule is missing or unusable; the brand voice is broken; a banned construction appears
- **MED:** a section is in the wrong order; a paragraph drags; sentence length is consistently high; weak transition
- **LOW:** a single sentence could be tighter; a phrase is mildly cliché

## Why this exists

v1 had 8 regulators and no one checking that the post was actually good to read. Compliance is necessary but not sufficient. Editorial closes the gap.
