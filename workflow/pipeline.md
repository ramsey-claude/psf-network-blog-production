# psfnetwork Blog Production Pipeline (v2)

Autonomous pipeline. Triggered by a single command. No human approval between stages once triggered. State is persisted to `blog/[slug]/pipeline-state.json` so any stage can resume after interruption.

## Trigger

- New post: `psf network için yeni blog yaz: [slug or topic]`
- Resume: `psf network [slug] devam et`

The trigger is a blanket pre-authorization for every stage that follows. Pipeline runs until publish or until it hits a stop condition. See `workflow/trigger-contract.md`.

## Stage map

| Stage | Name | Purpose |
|-------|------|---------|
| 0 | State check | Read `pipeline-state.json`, resume or start |
| 1 | Research & evidence | SERP snapshot, source every claim, cannibalization check |
| 2 | Draft | Write from brief + outline + evidence |
| 3 | Expert + editorial review | Dynamic regulator panel + editorial reviewer, sequential discussion |
| 4 | Revision | Apply consensus fixes |
| 5 | Localization | Per target market |
| 6 | Expert re-check | Conditional, only if Stage 5 changed financial terms |
| 7 | Pre-publish QA | Items checkable from markdown only |
| 8 | Publish | Commit all artifacts to main |
| 9 | Post-publish QA | Live URL: schema, performance, AI citation |

## Stage 0 - State check
Read `blog/[slug]/pipeline-state.json` from the repo.
- File missing: new post, start at Stage 1.
- `stage == "published"`: stop, report already published.
- Otherwise: resume at the listed stage. Do not redo completed steps.

## Stage 1 - Research & evidence gathering
**Input:** `brief.md`, `outline.md`
**Output:** `evidence.md`, `serp-snapshot.md`, possibly updated `outline.md`

Sub-steps:
1. SERP snapshot. Top 10 organic, People Also Ask, AI Overview, featured snippet, related searches for the focus keyword. Save to `serp-snapshot.md`.
2. Cannibalization check. Search `blog/` for existing posts on same keyword. If conflict: write `cannibalization-conflict.md`, halt.
3. Claim inventory. Extract every numerical, regulatory, comparative, historical, and named-entity claim from outline.
4. Source verification. Each claim gets a row in `evidence.md` with primary source. See `checklist/research-stage.md` for acceptable sources.
5. Outline reconciliation. Unsourceable claims are removed or replaced. Outline updated if changed.

**Gate:** No claim enters Stage 2 without a row in `evidence.md`.

## Stage 2 - Draft generation
**Input:** `brief.md`, `outline.md`, `evidence.md`
**Output:** `draft.md`

Draft follows the psfnetwork template (component order in the Railway blog-post.jsx). Every claim must trace back to an `evidence.md` entry. Sources section references evidence rows.

## Stage 3 - Expert + editorial review
Multi-agent sequential discussion. Two changes from v1:
- Panel is dynamic. Default minimum: SEC, FINRA, CFPB. Topic-triggered additions per `checklist/expert-routing.md`.
- Editorial reviewer always runs. Responsible for reader experience (hook, flow, clarity, brand voice). See `checklist/editorial-review.md`.

Round order: SEC, FINRA, CFPB, other regulators alphabetically, Editorial last among reviewers, Moderator final. Each reviewer reads all prior reviews and responds.

**Outputs:** `expert-reviews/stage3-panel-selection.md`, `expert-reviews/stage3-[reviewer].md` per reviewer, `expert-reviews/stage3-moderator-consensus.md`.

**Decision:**
- 3+ HIGH issues (any reviewer, including editorial): set `stage: "rewrite-required"`, loop back to Stage 2 with consensus notes. Increment `loop_count`. Max 3.
- 0-2 HIGH: proceed to Stage 4.

## Stage 4 - Revision
**Input:** `draft.md`, `stage3-moderator-consensus.md`
**Output:** updated `draft.md`, `changelog.md`

Apply every HIGH, most MED, judgment on LOW. Never delete sections - revise. Maintain brand voice. Output a numbered changelog with each change and its source reviewer.

## Stage 5 - Localization
**Input:** `draft.md`, `checklist/localization-guide.md`
**Output:** `localization-notes-[market].md` and `draft-[market].md` per target market; primary market keeps base `draft.md`.

If more than one target market is requested, localization runs once per market. Each pass reports whether financial terms were modified.

## Stage 6 - Expert re-check (conditional)
Runs only if any localized version modified financial terms, disclosures, numerical claims, or regulatory references. Same panel as Stage 3 but targeted to changed sections only.

**Decision:**
- New issues: loop to Stage 4 with localization notes.
- No new issues: proceed to Stage 7.

## Stage 7 - Pre-publish QA
See `checklist/qa-gate.md`. Items in this gate are only those verifiable from markdown before publish. Failures route by failure type (per qa-gate routing table). Blanket Stage 1 restart is removed.

**Output:** `qa-report.md`

**Decision:** PASS → Stage 8. FAIL → route to the stage indicated by failure type. Loop budget shared with Stage 3 (max 3 total).

## Stage 8 - Publish
Commit all artifacts to `main`:

```
blog/[slug]/brief.md
blog/[slug]/outline.md
blog/[slug]/evidence.md
blog/[slug]/serp-snapshot.md
blog/[slug]/draft.md
blog/[slug]/draft-[market].md       (per market)
blog/[slug]/changelog.md
blog/[slug]/localization-notes-[market].md
blog/[slug]/qa-report.md
blog/[slug]/pipeline-state.json
blog/[slug]/[slug]-chart.jsx        (if applicable)
blog/[slug]/expert-reviews/         (all stage3 and stage6 files)
```

Commit message: `feat(blog): publish [slug] - passed pre-publish QA on loop [n]`. Update `pipeline-state.json` with `stage: "published"`.

## Stage 9 - Post-publish QA
Runs after the page is live. See `checklist/qa-gate-post-publish.md`. Schema validation, Core Web Vitals, AI citation tests, GSC indexing.

**Output:** `post-publish-report.md`

Failures here do not restart the production pipeline. They generate targeted remediation tasks (schema fix, performance ticket, content edit pushed as an update).

## State file

`blog/[slug]/pipeline-state.json` is written after every stage.

```json
{
  "slug": "string",
  "title": "string",
  "stage": "number | 'rewrite-required' | 'manual-review-required' | 'published'",
  "stage_name": "string",
  "completed_steps": ["string"],
  "pending_steps": ["string"],
  "loop_count": "number, shared budget across Stage 3 and Stage 7, max 3",
  "last_updated": "YYYY-MM-DD",
  "expert_panel": ["string"],
  "target_markets": ["string"],
  "flags": {
    "high_severity_issues_count": "number",
    "localization_triggered_recheck": "boolean",
    "qa_fail_reasons": ["string"],
    "cannibalization_conflict": "boolean"
  },
  "evidence_summary": {
    "claims_total": "number",
    "claims_sourced": "number",
    "claims_dropped": "number"
  }
}
```

## Loop budget

Combined budget across Stage 3 and Stage 7: max 3. On exceed, set `stage: "manual-review-required"`, commit state, stop.

## Diagram

```
[0] State check
  |
  v
[1] Research & evidence
  |-- cannibalization conflict --> HALT
  |
  v
[2] Draft
  |
  v
[3] Expert + editorial review
  |-- 3+ HIGH --> [2] (loop, max 3)
  |
  v
[4] Revision
  |
  v
[5] Localization
  |
  v
[6] Expert re-check (conditional)
  |-- new issues --> [4]
  |
  v
[7] Pre-publish QA
  |-- FAIL routed by type --> [1] / [4] / [5] (max 3 total loops)
  |
  v
[8] Publish
  |
  v
[9] Post-publish QA
  |-- failures --> remediation tasks (not pipeline restart)
```
