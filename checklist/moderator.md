# Moderator (Stage 3 and Stage 6)

The moderator runs last in every multi-agent review round. It does not produce new findings - it consolidates the panel.

Output file: `expert-reviews/stage3-moderator-consensus.md` (and `stage6-moderator-consensus.md` if re-check fires).

---

## Inputs

- The current draft
- Every prior reviewer's output (regulators + Editorial) for this round, in order
- The expert panel selection file (`stage3-panel-selection.md`)
- Loop count and history from `pipeline-state.json`

## Job

1. Deduplicate flagged issues across reviewers. Same root cause flagged by multiple reviewers becomes one consolidated entry with all reviewer attributions.
2. Resolve conflicts between reviewers. If SEC says "remove the comparison" and Editorial says "keep but reframe", the moderator picks one and records the reason.
3. Re-rank severity if the panel disagrees. Take the highest severity any reviewer assigned, unless another reviewer explicitly downgraded it with a stronger reason.
4. Verify the count of HIGH issues for the rewrite-loop decision.
5. Decide the next stage.

The moderator must not invent issues that no reviewer raised. If the moderator believes an issue was missed, it notes it under "moderator observation" but does not include it in the consolidated count.

---

## Output format

```
PANEL SUMMARY:
- Reviewers run: [list]
- Total flagged issues (raw): [count]
- Consolidated issues: [count]
- HIGH: [count] | MED: [count] | LOW: [count]

CONSOLIDATED ISSUES:
1. [Issue description] - SEVERITY: HIGH/MED/LOW - RAISED BY: [reviewer list] - RECOMMENDED FIX: [specific action] - SECTION: [where in the draft]
2. ...

CONFLICTS RESOLVED:
1. [Reviewer A] said X, [Reviewer B] said Y. Moderator decision: [Z]. Reason: [why].
2. ...

MODERATOR OBSERVATIONS (informational, not counted):
- [Anything the moderator thinks the panel missed, but does not enter the count]

VERDICT FOR NEXT STAGE:
- If consolidated HIGH count >= 3: REWRITE_REQUIRED -> Stage 2, increment loop_count
- If consolidated HIGH count is 0-2: PROCEED -> Stage 4

DECISION: PROCEED_TO_STAGE_4 | REWRITE_TO_STAGE_2
LOOP_COUNT_AFTER_THIS_DECISION: [number]
```

---

## Decision rules (exact)

| Condition | Decision |
|-----------|----------|
| Consolidated HIGH >= 3 AND loop_count < 3 | REWRITE_TO_STAGE_2, increment loop_count |
| Consolidated HIGH >= 3 AND loop_count >= 3 | Set `stage: "manual-review-required"` in state, halt |
| Consolidated HIGH between 0 and 2 | PROCEED_TO_STAGE_4 |

The moderator does not have discretion outside these rules. The rules are reproducible.

---

## What the moderator does not do

- Generate new flagged issues (only reviewers do)
- Rewrite the draft (that is Stage 4)
- Drop a reviewer's HIGH severity without an explicit conflict resolution
- Move the post to publish on its own - the moderator decides between Stage 4 and Stage 2 only

---

## Quality check

A correctly written moderator output can be diffed against the input reviews and every line should trace back to a specific reviewer's claim, except the MODERATOR OBSERVATIONS block. If a line in CONSOLIDATED ISSUES does not trace back, that is a bug in the moderation, not a finding.
