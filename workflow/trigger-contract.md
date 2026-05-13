# Trigger Contract

The psfnetwork blog production pipeline is autonomous once triggered. This document defines exactly what the trigger authorizes.

## Triggers

- `psf network için yeni blog yaz: [slug or topic]` - new post, start at Stage 0
- `psf network [slug] devam et` - resume an in-flight post, start at the stage stored in `pipeline-state.json`

## Pre-authorized actions

Saying "yaz" pre-authorizes every action below for the duration of the run. No per-stage confirmation prompts.

- File writes to the local staging directory
- GitHub API reads against `ramsey-claude/psf-network-blog-production`
- GitHub API writes against `ramsey-claude/psf-network-blog-production` (commits, file PUTs, ref updates) within the slug's directory and `workflow/loop-log.md`
- Anthropic API calls for any reviewer, drafter, moderator, classifier, or QA role
- Internal looping (Stage 3 -> Stage 2, Stage 7 -> earlier) within the shared loop budget of 3
- Web fetches for SERP snapshot and source verification in Stage 1

## Stop conditions

The pipeline halts on any of these without further prompting:

- `loop_count > 3` -> set `stage: "manual-review-required"`, commit state, stop
- Cannibalization conflict in Stage 1 -> write `cannibalization-conflict.md`, stop
- A tool-level permission denial from the harness that this contract does not pre-authorize
- The operator interrupts the run
- A claim cannot be sourced AND there is no acceptable replacement available -> halt with `unsourceable-claim` state

## Actions still requiring explicit operator approval

- Pushes to any repo other than `ramsey-claude/psf-network-blog-production`
- File deletes (the pipeline only writes and overwrites within the slug's directory)
- Force-push, non-fast-forward updates, or any rewrite of `main` history
- Branch creation other than the working branch implicit in the run
- Calls to paid third-party APIs not listed in pre-authorized actions
- Any change to repo settings, collaborators, or webhooks

## Resume semantics

A new "devam et" trigger reads `pipeline-state.json` and resumes at the listed stage. Completed steps are not re-run. A stage interrupted mid-execution is re-run from its start (each stage must be idempotent on its inputs).

## What "published" means

`stage: "published"` in `pipeline-state.json` is the canonical signal that the post is shipped. A subsequent "yaz" or "devam et" trigger on the same slug returns "already published" and exits without action. To revise a published post, use a separate update command (out of scope for v2).
