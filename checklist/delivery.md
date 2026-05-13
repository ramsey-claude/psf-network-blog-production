# Stage 9 - Client Delivery (Google Drive)

After GitHub publish (Stage 8), Stage 9 mirrors the post's outputs to the operator's Google Drive. This is the client-facing handoff.

## Tooling

Google Drive MCP tools (`mcp__claude_ai_Google_Drive__*`). Authenticated under the operator's Google account. The pipeline never sets a sharing permission - the operator shares manually if a client needs access.

Tools used:
- `search_files` - to find the `psfnetwork` folder and the per-slug subfolder
- `create_file` - to create folders, Google Docs (markdown converted), and `.tsx` text files
- `get_file_metadata` - to confirm uploads
- Conversion: markdown is uploaded with target mimeType `application/vnd.google-apps.document` to produce a Google Doc

## Folder structure

```
My Drive/
└── psfnetwork/                          (created if missing)
    └── [slug]/                          (one per post, created if missing)
        ├── [Title].gdoc                 (primary, from draft.md)
        ├── [Title] - TR.gdoc            (per market, if localization ran)
        ├── [Title] - EN.gdoc
        ├── [Title] - FR.gdoc
        ├── [Title] - AE.gdoc
        ├── [slug]-chart.tsx             (if a chart was generated)
        └── [other-component].tsx        (any additional chart or table)
```

## Step-by-step

1. **Ensure root folder.** Search My Drive for `psfnetwork`. If not present, create a folder named `psfnetwork` in My Drive root. Capture its folder ID.
2. **Ensure slug subfolder.** Search the `psfnetwork` folder for a folder named exactly `[slug]`. If not present, create it. Capture its folder ID.
3. **Upload primary Doc.** Convert `blog/[slug]/draft.md` to a Google Doc. Title the doc with the H1 of the post (not the slug). Place in the slug subfolder.
4. **Upload localized Docs.** For each `draft-[market].md`, repeat step 3 with title format `[H1] - [market]`.
5. **Upload .tsx files.** For each Framer component file in the slug's repo directory, upload as-is to the slug subfolder with mimeType `text/typescript` (or `text/plain` if `text/typescript` is not accepted). No conversion.
6. **Write manifest.** Create `blog/[slug]/delivery-manifest.md` in the repo. One row per uploaded file with: file name, Drive file ID, Drive view URL, mimeType, timestamp.
7. **Update state.** Update `pipeline-state.json` `flags.drive_delivery` with `delivered_at`, `folder_id` (slug subfolder), and `files` array.
8. **Commit the manifest** to GitHub as a follow-up commit: `chore(delivery): drive manifest for [slug]`.

## Chart and table components - .tsx convention

All Framer-bound chart and table components produced by the pipeline are TypeScript JSX (`.tsx`), not plain JSX (`.jsx`).

Requirements for each `.tsx`:
- Default export
- Self-contained: no external imports beyond `react`
- SVG-based rendering, no chart library
- Uses psfnetwork tokens inline as CSS variables or constants: `#FF7141`, `#4F8FA3`, `#1C1C1C`, `#F7F5F0`
- Typed props interface even if currently unused (Framer Code Components benefit from props metadata)
- Component name: `[SlugPascalCase][Chart|Table][N]`

## Gate

Stage 9 succeeds when:
- The slug subfolder exists in Drive
- Every expected file has been uploaded
- The manifest has been written to the repo and committed

Stage 9 fails (`stage: "delivery-failed"`) when:
- An upload retry fails twice
- A folder cannot be created (auth or quota)

A delivery failure does not roll back the GitHub publish. Stage 8 stays final. The operator can re-run Stage 9 once the cause is resolved (`psf network [slug] devam et`).

## What this stage does NOT do

- Share the folder with a client or any third party
- Move or delete any existing Drive content
- Send notifications (email, Slack, etc.)
- Write outside `My Drive/psfnetwork/`
