# Delivery Manifest: How Fractional Real Estate Is Taxed

**Delivered:** 2026-05-15
**Method:** Drive REST API via `workflow/drive_cli.py` (OAuth, project `my-project-82896`).

## Drive structure

```
My Drive/
└── PSFnetwork/
    └── how-fractional-real-estate-is-taxed/
        └── How Fractional Real Estate Is Taxed: A K-1 Guide for 2026.gdoc
```

## File details

| Item | Value |
|------|-------|
| Drive parent folder | `1saBUbgnW9mb3VC6aokbBhSgo3VCU3ANG` (`PSFnetwork/`) |
| Slug subfolder | `11txAR0kXJBlG11EewoUda7KxbI24Kd8e` (`how-fractional-real-estate-is-taxed/`) |
| Native Google Doc id | `1BcQ6M3l8YScA-KOge7VWvIqSXqiyrpZqZxS4N10wio4` |
| Title | How Fractional Real Estate Is Taxed: A K-1 Guide for 2026 |
| MIME type | `application/vnd.google-apps.document` (native gdoc) |
| View URL | https://docs.google.com/document/d/1BcQ6M3l8YScA-KOge7VWvIqSXqiyrpZqZxS4N10wio4/edit |
| Folder URL | https://drive.google.com/drive/folders/11txAR0kXJBlG11EewoUda7KxbI24Kd8e |

## Source artifact

- Local docx: `/tmp/how-fractional-real-estate-is-taxed.docx` (rendered from `draft.md` via `workflow/render-for-drive.py`)
- After Drive-side conversion to native gdoc on upload, local docx not retained beyond this run.

## Sharing

No sharing changed. File remains in operator's Drive only.

## Idempotency

Folder created fresh (first delivery). On re-delivery, `drive_cli.py list` returns existing files; `drive_cli.py delete` removes them before re-upload. This run is delivery #1 so no deletion needed.
