# Pipeline Loop Log Template

A loop log is written every time the pipeline backs up to an earlier stage due to a failure. Copy this template per loop event. File name: `blog/[slug]/loop-log-[N].md` where N is the loop ordinal for that slug.

Loop budget is shared across Stage 3 (review rewrites) and Stage 7 (QA failure routing). Combined max: 3. On exceed, set `stage: "manual-review-required"` and halt.

---

## Loop metadata

| Field | Value |
|-------|-------|
| Slug | |
| Loop ordinal | <!-- 1st / 2nd / 3rd (max 3) --> |
| Triggered at stage | <!-- Stage 3 / Stage 7 --> |
| Routed back to stage | <!-- Stage 2 / Stage 4 / Stage 5 / Stage 1 --> |
| Trigger reason | <!-- 3+ HIGH in Stage 3 / Specific Stage 7 QA failure section --> |
| Date | <!-- YYYY-MM-DD --> |

---

## Failure context

### What was the trigger?
<!-- One sentence: e.g. "Stage 3 returned 4 HIGH severity issues from SEC and Editorial" or "Stage 7 QA section A failed because two numerical claims had no evidence.md row" -->

### Which issues drove the loop?
| # | Source (reviewer / QA section) | Description | Severity | Recommended fix |
|---|------------------------------|-------------|----------|----------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

---

## Routing decision

The pipeline routes by failure type. Confirm the route below matches the routing tables in `checklist/qa-gate.md` and `checklist/expert-routing.md`.

| Failure type | Documented route | This loop's route |
|--------------|------------------|-------------------|
| Stage 3: 3+ HIGH issues | Stage 2 (rewrite) | |
| Stage 7 section A: claim unsourceable | Stage 1 (research) | |
| Stage 7 section A: source exists, wording wrong | Stage 4 (revision) | |
| Stage 7 section B: SEO/GEO structure | Stage 4 | |
| Stage 7 section C: brand/content quality | Stage 4 | |
| Stage 7 section D: localization | Stage 5 | |

---

## Actions taken in this loop

| # | Action | Stage where applied | Outcome |
|---|--------|---------------------|---------|
| 1 | | | |
| 2 | | | |

---

## Re-entry checklist

Before re-running the routed stage, confirm:

- [ ] `pipeline-state.json` `loop_count` incremented
- [ ] `pipeline-state.json` `pending_steps` reset for the routed stage onward
- [ ] `flags.qa_fail_reasons` populated (if Stage 7 triggered the loop)
- [ ] `flags.high_severity_issues_count` populated (if Stage 3 triggered the loop)
- [ ] If `loop_count` will exceed 3 after this run, set `stage: "manual-review-required"` and halt instead of re-running

---

## Resolution

| # | Issue | How resolved | Verified at stage | Date |
|---|-------|--------------|-------------------|------|
| 1 | | | | |
| 2 | | | | |

---

## Outcome

- [ ] Loop resolved cleanly, pipeline progressed past the original trigger stage
- [ ] Loop resulted in another failure at the same or later stage (chained loop)
- [ ] Loop budget exhausted (`loop_count = 3`), stage set to `manual-review-required`
