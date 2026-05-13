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

## Stage -1 - Topic selection (conditional)

Runs only when the trigger did not include a slug. See `checklist/topic-selection.md` for the full scoring criteria.

Short version:
1. List every directory under `blog/`. Each is a candidate slug.
2. For each candidate, read `pipeline-state.json` if present. Exclude any candidate where `stage == "published"`.
3. Read `brief.md` metadata (Priority, Type) and cross-reference with `ROADMAP.md` (Step 3 Priority Posts table, Phase 1 Execution Tracker).
4. Apply the scoring rules in `checklist/topic-selection.md`. Hub posts always come before Spoke posts that link back to them.
5. Output the selected slug + a one-paragraph justification. Write the justification to the selected slug's `pipeline-state.json` under `flags.topic_selection_reason` when state is first created in Stage 0.

If no candidate has both `brief.md` and `outline.md` ready, halt with an explanation. Topic selection does not generate briefs or outlines.

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
After GitHub publish, mirror the outputs to the operator's Google Drive for client handoff. See `checklist/delivery.md`.

**Tooling:** Google Drive MCP (`mcp__claude_ai_Google_Drive__*`). Authenticated under the operator's account. No third-party sharing is set by the pipeline.

**Target structure:**

```
My Drive/
└── psfnetwork/
    └── [slug]/
        ├── [Title].gdoc                      (primary draft, converted from markdown)
        ├── [Title] - [market].gdoc           (one per localized variant)
        ├── [slug]-chart.tsx                  (Framer-compatible TypeScript, if applicable)
        └── [additional chart/table].tsx      (one per chart/table component)
```

**Actions:**
1. Ensure the `psfnetwork` folder exists in My Drive root. Create if missing.
2. Ensure subfolder `psfnetwork/[slug]/` exists. Create if missing.
3. Convert `draft.md` to a Google Doc and upload. Document title = the post's H1.
4. Convert each `draft-[market].md` to a Google Doc and upload. Title = "[H1] - [market]".
5. Upload every `.tsx` chart/table file as-is (text/typescript, no conversion).
6. Write a `delivery-manifest.md` in the repo listing each Drive file URL, doc ID, and timestamp.
7. Update `pipeline-state.json` `flags.drive_delivery` with the manifest summary.

**Gate:**
- Drive write failure on any file: retry once. If still failing, halt with `delivery-failed` state. GitHub publish is not rolled back.
- Successful delivery does not require operator confirmation. The operator sees the files in their Drive.

**Output:** `delivery-manifest.md` in the repo.

## Stage 10 - Post-publish QA (live URL)
Runs after the page is live on psfnetwork.com. See `checklist/qa-gate-post-publish.md`. Schema validation, Core Web Vitals, AI citation tests, GSC indexing.

This stage is deferred until the site is actually live. The pipeline does not block on it. When the live URL is available, the operator (or a separate scheduled run) invokes this stage independently.

**Output:** `post-publish-report.md`

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
