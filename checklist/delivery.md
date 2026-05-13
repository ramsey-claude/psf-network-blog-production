# Stage 9 - Client Delivery (Google Drive)

After GitHub publish (Stage 8), Stage 9 mirrors the post's outputs to the operator's Google Drive as a properly styled native Google Doc. This is the client-facing handoff.

## Tooling stack

The pipeline does NOT use the Drive MCP for this stage. The MCP's `create_file` does not auto-convert docx into a native Google Doc (its conversion list covers only text/plain and text/csv), and it lacks a delete operation. Instead the pipeline uses Google's Drive REST API directly via a thin Python helper.

Three local files implement the stack:

| File | Role |
|------|------|
| `workflow/render-for-drive.py` | Convert `draft.md` (markdown + YAML frontmatter) to a styled `.docx` via pandoc. Prepends a "Production Notes" table with the SEO metadata. Replaces `[VISUAL-HERO-XX]` with a designer note callout. |
| `workflow/drive_auth.py` | One-shot OAuth flow to mint a Drive-scoped token. Run once, interactively. |
| `workflow/drive_cli.py` | Day-to-day Drive operations: `list`, `delete`, `upload-as-gdoc`, `upload-as-is`. Used by Stage 9. |

The token is stored at `/Users/onur/.psfnetwork-drive/token.json` (outside the repo) and auto-refreshes.

## Folder structure (operator's My Drive)

```
My Drive/
└── psfnetwork/                          (created on first run)
    └── [slug]/                          (one per post)
        └── [Title].gdoc                 (native Google Doc, converted from .docx)
```

One native Google Doc per slug. No `.docx` files left in the folder. No localized variants by default (target_markets is `["EN-US"]` only).

## Step by step

For each post in Stage 9:

1. **Render docx.** Run `render-for-drive.py blog/[slug]/draft.md -o /tmp/[slug].docx`. Produces a styled docx with Production Notes block + body.
2. **Ensure parent folders.** Call `drive_cli.py list <psfnetwork_folder_id>`. If `psfnetwork/[slug]/` does not exist, create via Drive API.
3. **Cleanup prior uploads in the slug folder.** Call `drive_cli.py list <slug_folder_id>`. For each existing file, call `drive_cli.py delete <fileId>`. This prevents stale or duplicate docs lingering across re-runs.
4. **Upload native gdoc.** Call `drive_cli.py upload-as-gdoc /tmp/[slug].docx <slug_folder_id> "[H1 of the post]"`. The API converts the docx to a native Google Doc on the fly (target mimeType `application/vnd.google-apps.document`, source mimeType `application/vnd.openxmlformats-officedocument.wordprocessingml.document`).
5. **Capture result.** The API returns `{id, name, mimeType, webViewLink}`. Record in `blog/[slug]/delivery-manifest.md` and `pipeline-state.json` `flags.drive_delivery`.
6. **Commit manifest.** Push `delivery-manifest.md` + updated `pipeline-state.json` to the repo as a follow-up commit: `chore(delivery): drive manifest for [slug]`.

## Why native Google Doc (not docx)

- Opens directly in Drive with no conversion prompt.
- Editable in place by the operator or any shared user.
- Index-friendly for Drive search.
- Avoids the "open with > Google Docs" extra step that docx upload requires.

## Gate

Stage 9 succeeds when:
- The slug subfolder exists and contains exactly one native Google Doc with the H1 as title.
- `delivery-manifest.md` records the Drive file ID, view URL, and timestamp.
- `pipeline-state.json` `flags.drive_delivery` is populated.

Stage 9 fails (`stage: "delivery-failed"`) when:
- Drive REST API returns 4xx/5xx and a single retry also fails.
- The token cannot be refreshed (re-run `drive_auth.py` manually).

A delivery failure does not roll back the GitHub publish. Stage 8 stays final. Operator can re-run Stage 9 once the cause is resolved.

## OAuth setup (one-time)

The token is minted once per machine:

```
.venv/bin/python3 workflow/drive_auth.py
```

This opens a browser, asks the operator to authorize Drive scope, and stores the token at `/Users/onur/.psfnetwork-drive/token.json`. After that, subsequent Stage 9 runs use the saved refresh token automatically.

The OAuth client is reused from `/Users/onur/gsc-mcp/credentials-ozgurzaman.json` (GCP project `my-project-82896`, owned by the operator, with Drive API enabled). Other credentials files in `gsc-mcp/` point to projects the operator does not own (e.g., `seo-kpi-449217`) and cannot enable Drive on; do not switch to those.

## What this stage does NOT do

- Share the Drive folder or doc with any third party.
- Move or delete content outside `My Drive/psfnetwork/`.
- Send notifications.
- Produce `.tsx` chart files (those are handled by the chart-agent step in Stage 4 when needed).
