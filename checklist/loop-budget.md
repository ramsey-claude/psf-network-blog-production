# Loop Budget

Every stage that can re-run on failure has a budget. When the budget is exhausted, the pipeline halts with `manual-review-required` and stops trying. Added 2026-05-26 because individual stage docs each mention their own loop limit and the overall picture was hard to see.

## Why bounded loops

The autonomous pipeline must terminate. Without a budget, a stuck stage can spin forever (rewriting a draft that fundamentally cannot pass, re-uploading a doc that fails on every attempt). The budget is the autonomous-shutoff.

## Budgets by stage

| Stage | What loops | Budget | What happens when exhausted |
|-------|------------|--------|------------------------------|
| 1 | Source re-verification on unsourceable claim | 2 | Outline reconciliation removes the claim; if removal breaks the post, halt with `evidence-failed` |
| 2 ↔ 2.5 | Humanization re-runs against a stuck draft | 3 | Stage -2 brief revision triggered; the brief lacks usable Human Anchors |
| 3 ↔ 4 | Expert panel disagreement, revision cycles | 3 | Halt with `expert-loop-exhausted`, set `stage: manual-review-required` |
| 5 ↔ 6 | Localization triggers re-check, panel disagrees | 2 | Halt with `localization-stuck` |
| 7 ↔ 4 | QA fail routes back to revision | 3 | Halt with `qa-loop-exhausted` |
| 9 | Drive upload retry on 4xx/5xx | 1 | Halt with `delivery-failed` (per-slug; other slugs in batch continue) |
| 10 | Live URL retry | 3 (daily cron) | Defer indefinitely, log warning each day |

## Counter location

Each loop counter lives in the affected slug's `pipeline-state.json` under `flags.loop_counts.[name]`. Example:

```json
{
  "stage": "stage-7-qa",
  "flags": {
    "loop_counts": {
      "humanization": 1,
      "expert_revision": 0,
      "qa": 2
    }
  }
}
```

The counter increments at the START of a re-run, not at the END. So a re-run that finally succeeds still shows the incremented count.

## Shared vs per-stage

- **Humanization (2 ↔ 2.5):** dedicated counter `humanization`
- **Expert revision (3 ↔ 4):** dedicated counter `expert_revision`
- **QA revision (7 ↔ 4):** dedicated counter `qa`, separate from expert_revision because the routing is different (QA failures are structural; expert failures are compliance)
- **Localization (5 ↔ 6):** dedicated counter `localization`

A draft can hit Stage 4 from two upstream paths (Stage 3 panel and Stage 7 QA) without burning a shared budget; the two counters increment independently.

## Reset rules

- Counters reset on a new pipeline trigger (operator runs `psf network için yeni blog yaz: [slug]` from scratch).
- Counters reset when Stage -2 produces a new brief for the same slug.
- Counters do NOT reset on resume. A resume picks up the existing state, including the existing counts.

## Halt conditions surfacing

When a budget exhausts, the halt condition appears in:

1. `pipeline-state.json` `stage` field: `manual-review-required`
2. A new entry in `loop-log-[N].md` (template at `workflow/loop-log-template.md`) documenting which budget exhausted and the trail of attempts
3. The next Stage 11 retrospective picks it up and writes a summary to `incident-log.md` if the cause is structural (rule needs revision) rather than content-specific
