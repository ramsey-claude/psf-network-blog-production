# psfnetwork Blog Production Pipeline (v2)

Autonomous pipeline. Triggered by a single command. No human approval between stages once triggered. State is persisted to `blog/[slug]/pipeline-state.json` so any stage can resume after interruption.

## Trigger

- New post, system picks topic: `psf network için yeni blog yaz`
- New post, operator-specified topic: `psf network için yeni blog yaz: [slug or topic]`
- Resume: `psf network [slug] devam et`

The trigger is a blanket pre-authorization for every stage that follows. Pipeline runs until publish or until it hits a stop condition. See `workflow/trigger-contract.md`.

## Stage map

| Stage | Name | Purpose |
|-------|------|---------|
| -4 | Pre-flight (incident log read) | First action on every trigger — read `workflow/incident-log.md` and apply its active rules to this run |
| -3 | Auto gap discovery (topic pool refresh) | Only runs when Stage -2 exhausts the ROADMAP pool |
| -2 | Topic discovery & brief/outline generation | Only runs when Stage -1 returns no eligible candidate |
| -1 | Topic selection | Only runs when the trigger did not specify a slug |
| 0 | State check | Read `pipeline-state.json`, resume or start |
| 1 | Research & evidence | SERP snapshot, source every claim, cannibalization check |
| 2 | Draft | Write from brief + outline + evidence |
| 3 | Expert + editorial review | Dynamic regulator panel + editorial reviewer, sequential discussion |
| 4 | Revision | Apply consensus fixes |
| 5 | Localization | Per target market |
| 6 | Expert re-check | Conditional, only if Stage 5 changed financial terms |
| 7 | Pre-publish QA | Items checkable from markdown only |
| 8 | Publish | Commit all artifacts to main |
| 9 | Client delivery | Upload outputs to operator Google Drive |
| 10 | Post-publish QA | Live URL: schema, performance, AI citation (deferred until site is live) |
| 11 | Post-run workflow QA | Once-per-batch retrospective; updates `workflow/incident-log.md` |

## Stage -4 - Pre-flight (incident log read)

**Mandatory first action on every trigger.** Before reading any brief, selecting any topic, or fetching any source: read `workflow/incident-log.md` from the current `main`. Internalize the "Active rules" section. The run then proceeds with those rules in force.

If the incident log is unreachable (network error, repo unavailable), halt with `incident-log-unreachable` rather than running blind. The active rules represent every guardrail the pipeline has learned the hard way; running without them re-introduces past failures.

No deliverable for this stage — it is a read-and-internalize step. The fact that it ran is implicit in the run proceeding successfully (errors prevented by the log won't appear).

## Stage -3 - Auto gap discovery (conditional)

Runs only when Stage -2 reports `topic-generation-exhausted` (ROADMAP Step 2 has fewer than 3 unused gap candidates). Scans competitor blogs from ROADMAP Step 1, identifies topics not yet covered by psfnetwork, appends new candidates to Step 2, then loops back to Stage -2.

Spec in `checklist/topic-discovery-stage-minus-3.md`. Halt conditions: `discovery-failed` (no surface-able candidates after a full scan) or `competitor-fetch-failed`.

## Stage -2 - Topic discovery & brief/outline generation (conditional)

Runs only when Stage -1 returns "no ready candidate" — every existing slug under `blog/` is published or in flight. Generates a fresh `brief.md` + `outline.md` for the next-best seed from `ROADMAP.md` Step 2 (gap analysis), then loops back to Stage -1 so the new slug can be picked.

Spec in `checklist/topic-generation.md`. Halt conditions: `topic-generation-exhausted` (no remaining gap-analysis candidates pass filters; falls through to Stage -3) or `topic-generation-validation-failed` (two consecutive generated drafts fail validation).

Stage -2 commits its output as `feat(brief): generate brief + outline for [slug] - Stage -2 auto`.

## Stage -1 - Topic selection (conditional)

Runs only when the trigger did not include a slug. See `checklist/topic-selection.md` for the full scoring criteria.

Short version:
1. List every directory under `blog/`. Each is a candidate slug.
2. For each candidate, read `pipeline-state.json` if present. Exclude any candidate where `stage == "published"`.
3. Read `brief.md` metadata (Priority, Type) and cross-reference with `ROADMAP.md` (Step 3 Priority Posts table, Phase 1 Execution Tracker).
4. Apply the scoring rules in `checklist/topic-selection.md`. Hub posts always come before Spoke posts that link back to them.
5. Output the selected slug + a one-paragraph justification. Write the justification to the selected slug's `pipeline-state.json` under `flags.topic_selection_reason` when state is first created in Stage 0.

If no candidate has both `brief.md` and `outline.md` ready, **fall through to Stage -2** (topic generation) rather than halting. Topic selection itself does not author briefs or outlines.

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

Draft follows the component order in `brand/template-structure.md`. Every claim must trace back to an `evidence.md` entry. Sources section references evidence rows.

**Required output structure:**
1. YAML frontmatter at the top of `draft.md` containing every field listed in `brand/template-structure.md` (title, slug, type, topic, author, reviewer, read_time, published, updated, focus_keyword, secondary_keywords, meta_description, canonical, hero_visual_alt). Length rules:
   - `title`: 55-60 characters, focus keyword in the first third
   - `meta_description`: 150-160 characters, includes focus keyword and a CTA verb
2. H1 in the body matching the post topic (not necessarily identical to `title`, but related)
3. Every component block from `brand/template-structure.md` in order
4. Author and reviewer values use the standing personas in `brand/personas.md`. Any other names are rejected by Stage 7 QA.

The draft is responsible for producing title and meta description on its own. They are not retro-fitted in QA - they must be present and within length rules when Stage 2 ends.

## Stage 2.5 - Humanization pass
**Input:** `draft.md`, `brief.md` (Human Anchors section), `brand/tone-and-voice.md`, `brand/voice-samples/`, `checklist/ai-tells.md`
**Output:** `draft.md` (revised in place), `humanization-log.md`

Single-reviewer stage between draft and expert panel. Mandate is voice and reader experience only — not compliance. Six steps in order, all gated:

1. **AI tells sweep** — run the full ban list from `checklist/ai-tells.md`. Zero HIGH-tier matches may remain. Cadence and voice checks (Tier 7 and Tier 8) must pass.
2. **Human anchor injection** — all three Human Anchors from the brief (Real Story, POV Anchor, Contrarian Note) must appear in the body. No anchor may be relegated to a sidebar or callout.
3. **Rhythm rewrite** — at least one sub-5-word sentence, at least one 25+ word sentence, paragraph length variance ≥ 30%, no three consecutive paragraphs sharing the same opener pattern.
4. **De-listification** — at least 40% of H2 sections must be narrative paragraphs. Bullet fragments rewritten as full sentences. Maximum one Pros/Cons section.
5. **Voice consistency** — second person throughout. No mid-paragraph person switching. Generic "investors" only when literally referring to the class.
6. **Specificity audit** — every claim is checked: would a human writing this know the specific version? Generic claims either researched and replaced, explicitly framed as un-benchmarked, or cut.

Full spec in `checklist/humanization-pass.md`.

**Gate:** `humanization-log.md` exists with `VERDICT: PASS`. All six step results recorded as PASS. If FAIL on any step, draft returns to Stage 2 with the log as rewrite brief. Maximum three Stage 2 ↔ Stage 2.5 cycles before brief revision is triggered.

**Why this stage exists:** the v2 pipeline had editorial review embedded in Stage 3 as one voice among nine. Posts kept reading as AI-generated because editorial got out-voted on voice questions by regulators focused on compliance. Stage 2.5 gives humanization its own pass before the panel.

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

**Default behavior:** psfnetwork operates in the US market only and ships English-only content. With the default `target_markets: ["EN-US"]`, Stage 5 is a no-op: it writes an empty `localization-notes-EN-US.md` recording "no localization required, primary market only", and proceeds. Stage 6 also becomes a no-op.

Multi-market localization (TR, FR, AE) is spec'd in `checklist/localization-guide.md` for future expansion, but is not invoked by the default pipeline. To enable, set `target_markets` in the brief's metadata to include additional markets before running.

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
blog/[slug]/[slug]-chart.tsx        (if applicable, Framer-compatible TypeScript)
blog/[slug]/expert-reviews/         (all stage3 and stage6 files)
```

Commit message: `feat(blog): publish [slug] - passed pre-publish QA on loop [n]`. Update `pipeline-state.json` with `stage: "published"`.

## Stage 9 - Client delivery (Google Drive)
After GitHub publish, mirror the post's body to the operator's Google Drive as a styled native Google Doc. Full spec in `checklist/delivery.md`.

**Tooling:** Google Drive REST API via `workflow/drive_cli.py` (OAuth, project `my-project-82896`, token at `/Users/onur/.psfnetwork-drive/token.json`). NOT the Drive MCP - it cannot convert docx to native gdoc and cannot delete. The pipeline does not set sharing permissions.

**Target structure:**

```
My Drive/
└── psfnetwork/
    └── [slug]/
        └── [Title].gdoc        (native Google Doc, one per slug)
```

**Actions:**
1. `render-for-drive.py blog/[slug]/draft.md -o /tmp/[slug].docx` produces a styled docx with a Production Notes block + body.
2. Ensure `psfnetwork/[slug]/` folder exists via `drive_cli.py list`. Create if missing.
3. Delete any existing files in the slug folder via `drive_cli.py delete <id>` (clean state across re-runs).
4. `drive_cli.py upload-as-gdoc /tmp/[slug].docx <folder_id> "[H1]"`. Drive converts docx to a native Google Doc on upload.
5. Write `delivery-manifest.md` with Drive file id + view URL + timestamp.
6. Update `pipeline-state.json` `flags.drive_delivery`.

**Gate:**
- Drive write failure: retry once. If still failing, halt with `delivery-failed`. GitHub publish is not rolled back.
- Operator does not confirm individual uploads; they see the result in Drive.

**Output:** `delivery-manifest.md` in the repo.

## Stage 11 - Post-run workflow QA

Runs once at the end of every batch (after the last slug publishes or the run halts on a stop condition). Spec in `checklist/post-run-qa.md`.

The output is an updated `workflow/incident-log.md` committed to `main`. This is meta-QA on the pipeline itself — blog-level QA is handled by Stages 7 and 10.

**Triggers:**
- Last slug in a batch reaches `stage: "published"`.
- Batch halts on a documented stop condition.
- Operator-initiated interrupt (record what was in flight).

**Outputs:**
- Updated `workflow/incident-log.md` on `main`.
- One-line summary: slugs processed, halts, new incidents, open issues count.

**Halt conditions:** `incident-log-conflict` (log diverged on `main` mid-run; rebase needed), `auth-broken-*` sentinel present.

The next run's Stage -4 reads this updated log, closing the loop.

## Stage 10 - Post-publish QA (live URL)
Runs automatically once the live URL is available. See `checklist/qa-gate-post-publish.md`.

**Automation:** A launchd cron (`workflow/com.psfnetwork.stage10.plist`, installed at `~/Library/LaunchAgents/com.psfnetwork.stage10.plist`) fires `workflow/stage10_runner.py` every day at 09:13 local. The runner:
1. Lists all `blog/[slug]/pipeline-state.json` with `stage: "published"`.
2. For each, attempts the live URL (default `https://psfnetwork.com/blog/[slug]`).
3. If 404 / not live, defers (next day's cron retries).
4. If 200, runs the automatable Stage 10 checks (canonical, title/meta length, JSON-LD schema presence) and writes `post-publish-report.md` + updates `pipeline-state.json` `flags.post_publish_qa`.
5. Pushes both as a single commit.

The runner is idempotent: it skips slugs where `flags.post_publish_qa.completed_at` is already set.

**Out of scope for the runner (manual / LLM follow-up):**
- AI citation testing in Perplexity / ChatGPT (requires LLM with web).
- Google AI Overview check (live SERP scrape).
- Core Web Vitals via PageSpeed Insights (would need an API key).
- GSC URL inspection / index request.

These appear in the generated `post-publish-report.md` as "Manual follow-up" and are not blockers.

**Output:** `post-publish-report.md` in each slug's directory.

Failures here do not restart the production pipeline. They generate targeted remediation tasks (schema fix, performance ticket, content edit pushed as an update).

## State file

`blog/[slug]/pipeline-state.json` is written after every stage.

```json
{
  "slug": "string",
  "title": "string",
  "stage": "number | 'rewrite-required' | 'manual-review-required' | 'published' | 'delivery-failed' | 'unsourceable-claim' | 'cannibalization-conflict'",
  "stage_name": "string",
  "completed_steps": ["string"],
  "pending_steps": ["string"],
  "loop_count": "number, shared budget across Stage 3 and Stage 7, max 3",
  "last_updated": "YYYY-MM-DD",
  "expert_panel": ["string"],
  "target_markets": ["string, default ['EN-US']"],
  "flags": {
    "high_severity_issues_count": "number",
    "localization_triggered_recheck": "boolean",
    "qa_fail_reasons": ["string"],
    "cannibalization_conflict": "boolean",
    "topic_selection_reason": "string (only set when Stage -1 ran)",
    "drive_delivery": {
      "delivered_at": "YYYY-MM-DD",
      "folder_id": "string",
      "files": [{"name": "string", "id": "string", "url": "string"}]
    }
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
[8] Publish (GitHub commit)
  |
  v
[9] Client delivery (Google Drive)
  |-- delivery failure --> retry once, then HALT (GitHub state remains published)
  |
  v
[10] Post-publish QA (deferred, runs when live URL exists)
  |-- failures --> remediation tasks (not pipeline restart)
```
