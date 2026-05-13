# Stage -1 - Topic Selection

Runs only when the trigger did not specify a slug. Picks the next post to produce from the queue of candidates already in `blog/`.

Topic selection does not invent new topics. It picks among slugs that already have at minimum `brief.md` and `outline.md`. Generating new briefs and outlines is a separate task, out of scope for this pipeline.

## Inputs

- All directories under `blog/`
- `pipeline-state.json` in each candidate directory (if present)
- `brief.md` metadata of each candidate (Type, Priority, Status, target keyword)
- `ROADMAP.md` - Step 3 Priority Posts table and Phase 1 Execution Tracker

## Eligibility filter

A slug is eligible only if all of the following hold:

- `brief.md` exists
- `outline.md` exists
- `pipeline-state.json` either does not exist or its `stage` is not `published`
- `pipeline-state.json` `stage` is not `manual-review-required` (those need operator review first)

Ineligible slugs are excluded before scoring.

## Scoring criteria

Sort eligible candidates by these rules, in order. Higher in this list = stronger tiebreaker:

1. **Hub-before-spoke dependency.** If a Hub post links back from any Spoke post, the Hub must be picked before that Spoke. Check each candidate's `brief.md` "Internal Links" or "Type" field. If a candidate is a Spoke and its Hub is not yet `published`, the candidate is bumped after the Hub.
2. **Explicit Priority** in `brief.md` metadata or in ROADMAP Step 3 table. Lower number = higher priority. Priority 1 wins over Priority 2.
3. **Type weight.** Hub > Spoke > Supporting. Within the same Priority, Hub still wins.
4. **Search opportunity.** Compute `score = Volume / (KD + 1)`. Higher score wins as a tiebreaker among Spokes of the same Priority.
5. **Readiness signal.** If `brief.md` has Status = `Brief` and `outline.md` exists, the slug is ready. If outline still says "skeleton", deprioritize.

## Output

The selection produces:

- A single chosen slug
- A justification paragraph - at least: why this slug, which competitors it counters, what dependencies are satisfied
- A runner-up slug (recorded for transparency, not used)

Justification is recorded in the chosen slug's `pipeline-state.json` under `flags.topic_selection_reason` when state is initialized in Stage 0.

## Halt conditions

- No candidate has both `brief.md` and `outline.md` -> halt, report "no ready candidate"
- All candidates are `published` -> halt, report "Phase 1 complete, no next post in queue"
- A clear Hub dependency cannot be resolved -> halt, ask operator to confirm priority override

## Why this exists

Earlier triggers required the operator to name a slug. The operator wanted the pipeline to also pick what to write next, given the queue and the cluster strategy. Selection is rules-based, not discretionary, so the choice is reproducible and auditable. Operator can still override by naming a slug in the trigger.
