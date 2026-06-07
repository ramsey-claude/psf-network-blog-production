# Post-Run Workflow QA

Runs once at the end of every batch run, after the last blog publishes (or after the run halts on a stop condition). The output is an updated `workflow/incident-log.md` committed to `main`.

This is a meta-QA on the **pipeline itself**, not on individual blog content. Blog-level QA already happens at Stage 7 and Stage 10.

## When this runs

- After the last slug in a batch reaches `stage: "published"`.
- After the batch halts on any documented stop condition.
- After an operator-initiated interrupt (record what was in flight).

NOT after every individual blog. Only after a batch boundary.

## Inputs

- `workflow/incident-log.md`, the current rules and history.
- `workflow/pipeline.md`, `workflow/trigger-contract.md`, `checklist/*.md`, current spec.
- `blog/*/pipeline-state.json` for every slug touched in this batch.
- Any `loop-log-[N].md` files written during the batch.
- launchd logs at `/Users/onur/.psfnetwork-drive/{stage10,token-check}.{log,err}`.
- Sentinel state at `/Users/onur/.psfnetwork-drive/auth-broken-*` and `token-warning-*`.

## Sub-steps

### 1. Run-summary collection

For each slug touched in this batch, record:
- Final stage (`published`, `manual-review-required`, `delivery-failed`, etc.).
- Loop count if non-zero.
- Stage 7 QA `qa_fail_reasons` if any.
- Whether Stage 9 delivery succeeded.
- Anything in `loop-log-[N].md`.

### 2. Drift check

Diff the following pairs. Any mismatch is a doc-drift incident:
- `workflow/trigger-contract.md` ↔ `workflow/pipeline.md` (pre-authorized actions, stop conditions, tooling references).
- `checklist/delivery.md` ↔ `workflow/pipeline.md` Stage 9 (tooling, target structure).
- `checklist/topic-generation.md` ↔ `workflow/pipeline.md` Stage -2.
- `checklist/topic-discovery-stage-minus-3.md` ↔ `workflow/pipeline.md` Stage -3.
- Active rules in `incident-log.md` ↔ memory entries (`MEMORY.md` index). Memory should not contradict the log.

### 3. New-incident capture

Compare actual run behavior against active rules. For each:
- **New halt** (not in stop-conditions list): write a new incident-history entry. Add a new active rule if the cause is structural.
- **New permission prompt** (allowlist gap): record under "Open issues" with the exact `Bash(...)` pattern needed.
- **New transient failure not covered by retry policy**: add to retry policy in `trigger-contract.md`, log as incident.
- **Content-quality miss caught by Stage 7**: if first-pass error rate exceeds 30% for any rule (capsule length, missing meta, persona drift), flag the Stage 2 prompt as needing refinement.

### 4. Rule retirement

If an active rule didn't fire in the last 3 batches AND its underlying cause is fixed in code (not procedural), demote it from "Active rules" to a one-line note in "Incident history". Keeps the active list scannable.

### 5. Pool & infrastructure health

- ROADMAP Step 2 unused candidate count. If < 5, schedule a Stage -3 run before the next batch.
- GitHub rate limit headroom. If `< 1000 remaining` and reset > 30 min away, defer next batch.
- Drive token: `.venv/bin/python3 workflow/drive_cli.py health` returns ok.
- GitHub token: `.venv/bin/python3 workflow/token_expiry_check.py` returns no expiry warning.
- launchd: both `com.psfnetwork.stage10` and `com.psfnetwork.token-check` listed by `launchctl list | grep PSFnetwork`.

Any failure here is a new incident.

### 6. Commit

Commit message: `chore(workflow): post-run QA for batch ending [date], [N] slugs, [M] new incidents`.

Files always committed:
- `workflow/incident-log.md` (updated).

Files committed if changed during QA:
- `workflow/trigger-contract.md`, `workflow/pipeline.md`, `checklist/*.md` if drift required edits.

## Output

The post-run QA produces:
- An updated `workflow/incident-log.md` on `main`.
- A short summary in the conversation: slugs processed, halts (if any), new incidents (if any), open issues count.

## Halt conditions for the QA itself

- `incident-log-conflict`: the log file diverged on `main` between when the run started and finished (someone else pushed). Rebase manually before running.
- `auth-broken-*` sentinel present: QA cannot push results. Operator must clear before QA can complete.
