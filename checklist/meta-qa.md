# Meta-QA: pipeline artifact QA

Stage 11 sub-step. Runs once per batch retrospective after the per-batch incident-log update is complete. Scope is anything the regular Stage 7 QA does not cover: pipeline specs, checklists, brand docs, README, public-facing wireframes.

This document exists because the v3 humanization rollout (2026-05-26) shipped 101 em-dashes across 7 operational files before anyone noticed, and the existing Stage 7 QA gate only inspected blog drafts. The lesson: brand-voice rules apply to the repo's own documentation as much as to its blog output.

## When to run

After Stage 11's standard sub-steps (run summary, drift check, new incident capture), before committing the updated `incident-log.md`. Also run on-demand whenever a PR touches more than three files under `workflow/`, `checklist/`, `brand/`, or modifies `README.md`.

## Scope

Every file in the following paths:

- `README.md`
- `ROADMAP.md`
- `checklist/**/*.md`
- `workflow/**/*.md` (specs only, not `.py` scripts and not `.sh` push helpers)
- `brand/**/*.md`
- Public-facing visual assets in the operator's working tree (e.g., `psfnetwork_blog_pipeline.html` if delivered to a customer)

Excluded: `blog/**` (covered by Stage 7), `competitors/**`, `workflow/incident-log.md` (self-referential), files under `.git/`, `.venv/`.

## Checks

### Section M-A: Punctuation (BLOCKING)

- [ ] Zero em-dashes (`—`) <!-- check-rules: allow -->
- [ ] Zero en-dashes (`–`) <!-- check-rules: allow -->
- [ ] Zero double-hyphens (`--` outside of CLI flag examples and HTML comments)

### Section M-B: Brand voice (BLOCKING)

- [ ] `PSFnetwork` written with capital PSF, single word, no spaces, no other casing
- [ ] No "guaranteed return," "guaranteed yield," or any guaranteed-X-investment language <!-- check-rules: allow -->
- [ ] No "delve," "leverage" (as verb), "synergy," "robust solution" <!-- check-rules: allow -->

### Section M-C: Cross-document consistency (FAIL on mismatch)

- [ ] Stage numbers consistent between `README.md` Pipeline Stages section and `workflow/pipeline.md` Stage map table
- [ ] Repository structure block in `README.md` lists every file directly referenced from `pipeline.md` and `checklist/*.md`
- [ ] Every `checklist/X.md` referenced from `pipeline.md` exists in the repo
- [ ] Every spec file under `workflow/` referenced from a checklist exists

### Section M-D: AI tell density (WARN)

- [ ] No file in scope exceeds 3 HIGH-tier AI tells per 1000 words (per `checklist/ai-tells.md` Tier 2)
- [ ] No file in scope opens with a Tier 1 stock opener

## Output

`workflow/meta-qa-report-YYYY-MM-DD.md` with per-file PASS/FAIL and aggregate counts. On any BLOCKING failure, the Stage 11 retrospective halts with `meta-qa-failed` until the violations are fixed.

## Failure routing

| Failure type | Route to |
|--------------|----------|
| Punctuation (M-A) | Author of the offending commit fixes in place. Pre-commit hook should have caught this; if it didn't, file an incident for the hook gap. |
| Brand voice (M-B) | Same as M-A. |
| Cross-doc consistency (M-C) | The author of the most recent edit to either side of the mismatch reconciles. |
| AI tell density (M-D) | WARN-only. Open a tracked debt item if any file repeatedly trips this check. |

## Relationship to other guardrails

Meta-QA is the third and last line of defense. Order of catches:

1. **Pre-commit hook (`.githooks/pre-commit`)** catches Tier 0 violations at commit time, before the change reaches the repo. Primary defense.
2. **Stage 7 QA gate** catches blog-content violations before Stage 9 delivery. Secondary defense for blog files specifically.
3. **Stage 11 meta-QA (this document)** catches everything else, retrospectively, once per batch. Last defense for operational files.

If meta-QA finds anything, the pre-commit hook had a gap. Update the hook patterns first, then fix the file.
