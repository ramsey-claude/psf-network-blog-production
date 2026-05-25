# Voice Samples

Reference library of real psfnetwork team writing. Used by:

- Stage 2 (Draft generation) as voice anchor input to the model
- Stage 2.5 (Humanization pass) as the reference for "what does a human at psfnetwork actually sound like"

## What belongs here

- Founder essays, blog posts, or LinkedIn pieces written by named psfnetwork team members
- Internal Slack threads or memos with permission to use
- Transcripts of investor relations calls, podcasts, or panel appearances
- Customer support replies that exemplify the voice
- Newsletter copy with named authorship

## What does not belong here

- Anything previously generated through this pipeline (circular reference)
- Marketing copy from agencies or contractors who do not write in the psfnetwork voice
- Generic industry writing (REIT analyst reports, etc.)

## File naming

```
[YYYY-MM-DD]-[author-firstname]-[short-topic].md
```

Example: `2026-03-14-marcus-why-square-foot.md`

## Recommended minimum

- 5 samples from at least 2 distinct authors
- Mix of long-form (800+ words) and short-form (Slack thread length)
- At least one piece that takes a contrarian position on a sector topic

## How writers reference these

When generating a new draft, the model is prompted with 2-3 samples from this library as "write in this voice" reference. The humanization reviewer uses the full set as the comparison baseline when judging voice consistency.

---

**Status:** Library is currently empty. Populate before the next pipeline run that relies on humanization Stage 2.5 voice anchors.
