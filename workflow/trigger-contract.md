# Trigger Contract

The psfnetwork blog production pipeline is autonomous once triggered. This document defines exactly what the trigger authorizes.

## Triggers

- `psf network için yeni blog yaz` - new post, system picks the topic (runs Stage -1 first)
- `psf network için yeni blog yaz: [slug or topic]` - new post, operator-specified topic, skip Stage -1
- `psf network [slug] devam et` - resume an in-flight post, start at the stage stored in `pipeline-state.json`

## Mandatory pre-flight (Stage -4)

The first action of every triggered run, before any other read or fetch:

1. Read `workflow/incident-log.md` from current `main`.
2. Internalize the "Active rules" section. These rules govern this run.
3. If the incident log is unreachable, halt with `incident-log-unreachable`. Do not proceed.

This is non-optional. The active rules encode every failure mode the pipeline has previously fixed; skipping the read re-introduces past failures.

## Mandatory post-flight (Stage 11)

The last action of every batch run, after the last slug publishes or the run halts:

1. Run the `checklist/post-run-qa.md` retrospective.
2. Append any new incidents to `workflow/incident-log.md`. Promote new structural causes to "Active rules".
3. Commit the updated log to `main` with message `chore(workflow): post-run QA for batch ending [date], [N] slugs, [M] new incidents`.

Skipping post-run QA breaks the learning loop. The next run's Stage -4 needs current rules.

## Pre-authorized actions

Saying "yaz" pre-authorizes every action below for the duration of the run. No per-stage confirmation prompts.

- File writes to the local staging directory
- GitHub API reads against `ramsey-claude/psf-network-blog-production`
- GitHub API writes against `ramsey-claude/psf-network-blog-production` (commits, file PUTs, ref updates) within the slug's directory and `blog/[slug]/loop-log-[N].md` (per-loop, template in `workflow/loop-log-template.md`)
- Brief.md and outline.md generation in new slug directories under `blog/[new-slug]/` (Stage -2)
- Updates to `ROADMAP.md` Phase 1/2 trackers when Stage -2 generates a new topic
- Anthropic API calls for any reviewer, drafter, moderator, classifier, or QA role
- Internal looping (Stage 3 -> Stage 2, Stage 7 -> earlier) within the shared loop budget of 3
- Web fetches and web searches for SERP snapshot and source verification in Stage 1
- Google Drive REST API calls via `workflow/drive_cli.py` (OAuth, project `my-project-82896`, token at `/Users/onur/.psfnetwork-drive/token.json`) for Stage 9 delivery: folder creation under `psfnetwork/`, file upload, markdown-to-Google-Doc conversion (via `upload-as-gdoc`), file deletion for clean re-runs, all scoped to the operator's own Drive, no third-party sharing. The Drive MCP is NOT used (it cannot auto-convert docx → native gdoc and lacks delete).

## Stop conditions

The pipeline halts on any of these without further prompting:

- `loop_count > 3` -> set `stage: "manual-review-required"`, commit state, stop
- Cannibalization conflict in Stage 1 -> write `cannibalization-conflict.md`, stop
- A tool-level permission denial from the harness for an action this contract does not pre-authorize AND that cannot be auto-recovered via the rewrite/narrow-allowlist protocol (see "Permission prompt self-recovery" below). Recoverable prompts do NOT halt, they re-loop transparently to the operator.
- The operator interrupts the run
- A claim cannot be sourced AND there is no acceptable replacement available -> halt with `unsourceable-claim` state
- An auth sentinel at `/Users/onur/.psfnetwork-drive/auth-broken-{github,drive}` is present at run start -> halt with `auth-broken` state and the sentinel's reason. Do NOT proceed with stages that need the broken credential; operator must run `workflow/rotate-github-token.sh` or `workflow/drive_auth.py` to clear it
- Stage -3 returns `discovery-failed` (no surfaceable gap candidates) -> halt; operator must seed ROADMAP Step 2 manually
- `workflow/incident-log.md` is unreachable at Stage -4 -> halt with `incident-log-unreachable`. Do not run without current rules.

## Permission prompt self-recovery (no halt, no operator approval)

When a tool call gets rejected by the Claude Code permission system, the run does NOT pause for operator approval. Recovery protocol:

1. **Rewrite the command first.** Reshape into an allowlisted form (single-command Bash, repo-scoped paths, `cp` + `rm` instead of `mv`, etc.). Most prompts are caused by compound commands or path scope and resolve cleanly via rewrite.
2. **Narrow-allowlist as fallback.** If the action is safe (read-only, or write-scoped to `/Users/onur/psfnetwork-pipeline/**`, `/tmp/**`, `/Users/onur/.psfnetwork-drive/**`), append the narrowest necessary pattern to `~/.claude/settings.local.json` and retry. Never broad-allow: `Bash(*)`, `sudo *`, interpreter wildcards beyond what is already approved, paths outside the project tree.
3. **Log the incident** to `workflow/incident-log.md` under "Incident history", original pattern, recovery taken, lesson, so Stage 11 can promote recurring fixes to Active rules.
4. **Retry the original action** and continue the run.

This protocol replaces the prior behavior of halting on permission denial for any pattern the contract didn't pre-authorize. Only genuinely unrecoverable denials (the unsafe-pattern list above) halt the run, and they halt with `permission-unrecoverable` rather than pausing for input.

## Transient failure handling (no halt)

These are retried in-stage and do NOT halt the run:

- GitHub API 5xx or 429: retry up to 3 times with exponential backoff (2s, 8s, 30s).
- Drive API 5xx or 403 (transient propagation): retry once after 30s. If still failing, halt with `delivery-failed` for that slug only; other slugs in a batch continue.
- WebFetch / WebSearch transient timeout: retry once with the same query. If still failing, mark the claim/source as `unverified` in `evidence.md` and continue. Stage 1 gate only halts if the unverified-claim count exceeds the brief's tolerance (default: 0 for regulatory claims, 2 for general).
- Federal source 403 (sec.gov main domain): substitute investor.gov / EDGAR / govinfo per `psfnetwork_federal_fetch` policy. Already in memory; do not treat as a halt.

## Actions still requiring explicit operator approval

- Pushes to any repo other than `ramsey-claude/psf-network-blog-production`
- File deletes (the pipeline only writes and overwrites within the slug's directory)
- Force-push, non-fast-forward updates, or any rewrite of `main` history
- Branch creation other than the working branch implicit in the run
- Calls to paid third-party APIs not listed in pre-authorized actions (Semrush is intentionally excluded - see `checklist/research-stage.md`)
- Any change to repo settings, collaborators, or webhooks
- Sharing any Google Drive file or folder with another account (the pipeline writes to the operator's Drive only, never shares)
- Writes to Google Drive locations outside `My Drive/psfnetwork/`

## Resume semantics

A new "devam et" trigger reads `pipeline-state.json` and resumes at the listed stage. Completed steps are not re-run. A stage interrupted mid-execution is re-run from its start (each stage must be idempotent on its inputs).

## What "published" means

`stage: "published"` in `pipeline-state.json` is the canonical signal that the post is shipped. A subsequent "yaz" or "devam et" trigger on the same slug returns "already published" and exits without action. To revise a published post, use a separate update command (out of scope for v2).
