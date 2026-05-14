#!/bin/bash
# One-shot: push workflow/incident-log.md + workflow/scripts/README.md (post-run QA artifacts).
set -euo pipefail
cd /Users/onur/psfnetwork-pipeline
TOKEN=$(tr -d '\n' < /Users/onur/.psfnetwork-drive/github-token)
OWNER="ramsey-claude"
REPO="psf-network-blog-production"
BASE="https://api.github.com/repos/${OWNER}/${REPO}"
AUTH="Authorization: Bearer ${TOKEN}"
ACCEPT="Accept: application/vnd.github+json"
CT="Content-Type: application/json"

FILES=(
  "workflow/incident-log.md"
  "workflow/scripts/README.md"
  "workflow/scripts/push-incident-log.sh"
)

MAIN_SHA=$(curl -s -H "$AUTH" -H "$ACCEPT" "${BASE}/git/ref/heads/main" | jq -r '.object.sha')
BASE_TREE=$(curl -s -H "$AUTH" -H "$ACCEPT" "${BASE}/git/commits/${MAIN_SHA}" | jq -r '.tree.sha')

TREE_ITEMS="[]"
for F in "${FILES[@]}"; do
  CONTENT_B64=$(base64 < "$F" | tr -d '\n')
  PAYLOAD=$(jq -nc --arg c "$CONTENT_B64" '{content:$c, encoding:"base64"}')
  BLOB_SHA=$(curl -s -H "$AUTH" -H "$ACCEPT" -H "$CT" -X POST -d "$PAYLOAD" "${BASE}/git/blobs" | jq -r '.sha')
  TREE_ITEMS=$(jq -c --arg p "$F" --arg s "$BLOB_SHA" '. + [{path:$p, mode:"100644", type:"blob", sha:$s}]' <<<"$TREE_ITEMS")
done

TREE_PAYLOAD=$(jq -nc --arg base "$BASE_TREE" --argjson tree "$TREE_ITEMS" '{base_tree:$base, tree:$tree}')
NEW_TREE_SHA=$(curl -s -H "$AUTH" -H "$ACCEPT" -H "$CT" -X POST -d "$TREE_PAYLOAD" "${BASE}/git/trees" | jq -r '.sha')

COMMIT_MSG="chore(workflow): post-run QA for batch ending 2026-05-15 - 1 slug, 3 new incidents

Run summary:
- 1 slug published: how-fractional-real-estate-is-taxed (Stage -2 generation
  from ROADMAP item 16). 0 HIGH / 8 MED / 15 LOW in panel review; 0 loops.
  Stage 7 made 2 micro-fixes (title 63->57, sale capsule 77->70).

New incidents added to log:
- Compound-bash permission prompts mid-run (caught when a multi-line cd+for
  shell command triggered a prompt despite individual commands being
  allowlisted). New active rule: single-command Bash calls only.
- /tmp/*.sh ad-hoc push helpers triggered prompts (allowlist covers
  workflow/*.sh, not /tmp/). New active rule: one-shot push scripts go in
  /Users/onur/psfnetwork-pipeline/workflow/scripts/, not /tmp/.
- Stage 2 over-shoot on title and capsule length (caught and fixed within
  Stage 7's 2-micro-fix budget; rule strengthened).

Also: created workflow/scripts/ subdir with README explaining the path
convention; this push itself uses it as the first example."
COMMIT_PAYLOAD=$(jq -nc --arg msg "$COMMIT_MSG" --arg tree "$NEW_TREE_SHA" --arg parent "$MAIN_SHA" '{message:$msg, tree:$tree, parents:[$parent]}')
NEW_COMMIT_SHA=$(curl -s -H "$AUTH" -H "$ACCEPT" -H "$CT" -X POST -d "$COMMIT_PAYLOAD" "${BASE}/git/commits" | jq -r '.sha')

REF_PAYLOAD=$(jq -nc --arg sha "$NEW_COMMIT_SHA" '{sha:$sha, force:false}')
curl -s -H "$AUTH" -H "$ACCEPT" -H "$CT" -X PATCH -d "$REF_PAYLOAD" "${BASE}/git/refs/heads/main" > /dev/null

echo "Commit: https://github.com/${OWNER}/${REPO}/commit/${NEW_COMMIT_SHA}"
