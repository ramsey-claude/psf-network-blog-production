# Playbook: delivering to Drive

Mirroring a published article into the operator's Drive as a native Google Doc,
which is Stage 9. Spec in `checklist/delivery.md` and `workflow/pipeline.md`.

## Preconditions

- The article is committed and published (Stage 8 done).
- `blog/[slug]/qa-report-[version].md` exists, recommends PUBLISH, and lists no
  FAILs. `deliver.py` checks this and refuses otherwise, which is the point:
  a delivery once skipped the gate and shipped two rounds of violations (D-007).
- No auth sentinel present. A broken Drive credential halts the stage.

## The call

```bash
python3 workflow/deliver.py --slug [slug] --version [version] \
    --folder-id [drive-folder-id] --title "[H1]"
```

`deliver.py` renders the docx and uploads it as a native Google Doc in one
call. Do not call `drive_cli.py upload-as-gdoc` directly for a delivery; it is
retained for operator cleanup only.

## Around the call

1. Make sure `psfnetwork/[slug]/` exists, creating it if not.
2. Delete whatever is already in that folder, so a re-run leaves one clean
   document instead of a pile of versions. Idempotency is the rule here:
   `R-process-idempotency`.
3. After a successful upload, write `delivery-manifest.md` with the file id,
   the view URL, and the timestamp, and update `flags.drive_delivery` in the
   state file.

## When it fails

- Drive write failure: retry once, then halt that slug with `delivery-failed`.
  Other slugs in the batch keep going. The GitHub publish is not rolled back.
- 403 right after enabling the API: propagation, not a bug. Retry after 30
  seconds.
- `RefreshError`: `drive_cli.py` writes the drive sentinel. The operator clears
  it with `workflow/drive_auth.py`.

Never the Drive MCP. It cannot convert a docx into a native Google Doc and it
cannot delete, which is the whole reason this stack exists (D-001).
