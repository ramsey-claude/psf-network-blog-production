# Out-of-band Humanization

How to re-humanize an article that already shipped through the pipeline as v1 (pre-humanization-pass). Added 2026-05-26 after the first such re-run, which we did ad-hoc and surfaced two structural gaps in the process.

## When this applies

- A v1 article exists on `main` and (usually) in the operator's Drive
- The article needs the humanization treatment retroactively
- The customer has signed off on the topic itself (no new brief generation)

If the topic itself is in question, do not run out-of-band humanization. Run Stage -2 (brief regeneration) instead.

## Numbering convention

The original draft is `blog/[slug]/draft.md`. Re-humanized versions are `blog/[slug]/draft-vN-humanized.md` where N starts at 2. Each version gets:

- `draft-vN-humanized.md` (the rewritten content)
- `draft-vN-humanization-log.md` (six-step humanization log per `checklist/humanization-pass.md`)
- `qa-report-vN-humanized.md` (Stage 7 output for this version)

The unversioned files (`draft.md`, `qa-report.md`) refer to v1 and remain untouched.

## Procedure

### 1. Brief check

Run `python3 workflow/brief_preflight.py blog/[slug]/brief.md`. If the brief lacks Human Anchors (most v1 briefs do), backfill the Human Anchors section before continuing. The humanization will be mechanical without them.

### 2. Humanization (Stage 2.5)

Apply all six steps from `checklist/humanization-pass.md` to a copy of `draft.md`, writing to `draft-v2-humanized.md`. Write the change log to `draft-v2-humanization-log.md`.

### 3. Expert re-touch (selective)

Out-of-band humanization does NOT trigger a full Stage 3 panel by default, because the underlying claims and structure are unchanged from a Stage-3-cleared v1. BUT: any voice-and-position change that crosses a regulator domain DOES need a single-reviewer touch. The humanization-log "Open items" section lists these candidates.

Decision rule: if a humanization change introduces a new claim, a new opinion the platform stands behind, or modifies a previously approved disclaimer, route to:

| Change type | Reviewer | Output file |
|-------------|----------|-------------|
| New SEC-domain claim or disclaimer | SEC | `expert-reviews/stage3-sec-v2.md` |
| New FINRA-domain claim or comparison | FINRA | `expert-reviews/stage3-finra-v2.md` |
| New consumer-facing fee or risk language | CFPB | `expert-reviews/stage3-cfpb-v2.md` |
| Pure voice/cadence change, no claim change | Editorial only | `expert-reviews/stage3-editorial-v2.md` |
| Multiple of the above | Full Stage 3 panel | full `stage3-*-v2.md` set |

### 4. QA gate (Stage 7)

Run `qa-gate.md` Sections A through E against `draft-v2-humanized.md`. Write to `qa-report-v2-humanized.md`. Note the naming: deliver.py looks for `qa-report-<version>.md`, so the file name must include the version slug.

### 5. Delivery (Stage 9)

```bash
.venv/bin/python workflow/deliver.py \
  --slug [slug] \
  --version v2-humanized \
  --folder-id [drive-folder-id] \
  --title "[v2 Humanized] [original H1]"
```

deliver.py refuses if `qa-report-v2-humanized.md` is missing or has a non-PUBLISH verdict.

### 6. v1 retention

By default, KEEP the v1 Drive doc alongside the new v2 doc so the customer can compare. The delivery-manifest captures both links and the prior-version-deleted history.

If the operator decides v1 should be deleted (e.g., customer signs off on v2 as the canonical version), delete the v1 doc via `drive_cli.py delete <fileId>` and add a "DELETED" row to the delivery-manifest history table.

### 7. Customer communication

Per `checklist/customer-feedback-intake.md` Step 5: send the new Drive doc link, a one-line summary, and a pointer to the audit trail.

## What goes in pipeline-state.json

After an out-of-band humanization, append to the slug's `pipeline-state.json`:

```json
{
  "out_of_band_humanization_history": [
    {
      "version": "v2-humanized",
      "started_at": "2026-05-26T15:00:00Z",
      "completed_at": "2026-05-26T16:30:00Z",
      "drive_doc_id": "1Y2VdTijtikhDlivhyh8kubS9Sm1xlNxs0U0QVHHi1BM",
      "qa_report": "blog/[slug]/qa-report-v2-humanized.md",
      "loops": 4
    }
  ]
}
```

This is in addition to the normal `stage` field, which remains at "published" for the underlying v1. v2 is not a new pipeline run; it is a re-render of an already-published article.

## Loop tracking

Each delivery attempt counts toward a per-slug `humanization_redo` loop counter. Budget is 3. If three attempts fail to land a working v2 doc, halt with `humanization-out-of-band-exhausted` and route to manual review. Loop history in `delivery-manifest.md` "Delivery loop history" table.
