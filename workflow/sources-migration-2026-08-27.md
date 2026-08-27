# Clickable sources migration, 2026-08-27

Operator request: every source link at the end of every live article must
be clickable. Done for all 21 articles that use the CMS sources box
(15 Batch 2 + 6 Batch 1). Verified live: numbered, clickable entries on
every one.

## Final architecture (do not simplify without re-testing)

- **`Sources` (Plain Text, legacy):** still exists and still matters. The
  article template's Sources SECTION visibility is effectively tied to
  this field being non-empty; leave plain-text content in it. Emptying it
  hides the whole box even when Sources Rich has content (proven on the
  six Batch 1 articles).
- **`Sources Rich` (Formatted Text, new):** holds the rendered content.
  The template's Sources text layer is bound to this field (rebinding
  done in the canvas on 2026-08-27). Content format: numbered PARAGRAPHS,
  `<p>N. <a href="url">Publisher, Title</a></p>` - NOT an `<ol>`.
- Generator: `framer_batch_csv.py --sources-style linked --fields
  "Slug,Sources"`; plain style feeds the legacy field.

## What failed on the way (recorded so nobody retries them)

1. Markdown in the CSV prints literally, into plain and formatted fields
   alike. CSV import parses HTML for formatted fields, not markdown.
2. HTML into a Plain Text field gets escaped and shows as code. The
   original Sources field could not be converted in place; Framer offers
   no type change on an existing field, hence the new field + rebind.
3. An imported `<ol>` renders its links but NOT its numbers on the live
   site: the runtime draws list numbers as absolutely positioned CSS
   counters and the published page lacks the positioning they need. The
   editor canvas renders them fine, which misleads. Hence numbered
   paragraphs.
4. Import-mapping trap: Framer preselects the last-used target field, so
   a file meant for the legacy field can land in Sources Rich and
   overwrite it (happened once; re-import restored).

## Per-article state

- 15 Batch 2 + 6 Batch 1 (square-foot, passive-income, best-platforms,
  10k, 90-percent, what-is-proptech): sources box live, numbered + linked.
- 4 Batch 1 articles have their sources inline in Content and already
  clickable (investing, with-100, crowdfunding, reg-a-vs-reg-d): left
  untouched, no box needed.
- `how-fractional-real-estate-is-taxed`: 8 in-body source URLs are still
  plain text; needs a hand edit in the CMS Content editor (select URL,
  add link). Importing the box for it would duplicate its inline list.
