#!/bin/bash
set -euo pipefail

TOKEN_FILE="${PSFNETWORK_TOKEN_FILE:-/Users/onur/.psfnetwork-drive/github-token}"
if [[ ! -f "$TOKEN_FILE" ]]; then
  echo "ERROR: token file missing at $TOKEN_FILE" >&2
  exit 1
fi
TOKEN=$(tr -d '\n' < "$TOKEN_FILE")
OWNER="ramsey-claude"
REPO="psf-network-blog-production"
BASE="https://api.github.com/repos/${OWNER}/${REPO}"
AUTH="Authorization: Bearer ${TOKEN}"
ACCEPT="Accept: application/vnd.github+json"
CT="Content-Type: application/json"

FILES=(
  "workflow/pipeline.md"
  "workflow/trigger-contract.md"
  "checklist/research-stage.md"
  "checklist/expert-routing.md"
  "checklist/editorial-review.md"
  "checklist/qa-gate.md"
  "checklist/qa-gate-post-publish.md"
)

cd /Users/onur/psfnetwork-pipeline

echo "==> Get main ref"
MAIN_SHA=$(curl -s -H "$AUTH" -H "$ACCEPT" "${BASE}/git/ref/heads/main" | jq -r '.object.sha')
echo "MAIN_SHA=$MAIN_SHA"

echo "==> Get base tree"
BASE_TREE=$(curl -s -H "$AUTH" -H "$ACCEPT" "${BASE}/git/commits/${MAIN_SHA}" | jq -r '.tree.sha')
echo "BASE_TREE=$BASE_TREE"

echo "==> Create blobs"
TREE_ITEMS="[]"
for F in "${FILES[@]}"; do
  echo "  blob: $F"
  CONTENT_B64=$(base64 < "$F" | tr -d '\n')
  PAYLOAD=$(jq -nc --arg c "$CONTENT_B64" '{content:$c, encoding:"base64"}')
  BLOB_SHA=$(curl -s -H "$AUTH" -H "$ACCEPT" -H "$CT" -X POST -d "$PAYLOAD" "${BASE}/git/blobs" | jq -r '.sha')
  echo "    sha=$BLOB_SHA"
  TREE_ITEMS=$(jq -c --arg p "$F" --arg s "$BLOB_SHA" '. + [{path:$p, mode:"100644", type:"blob", sha:$s}]' <<<"$TREE_ITEMS")
done

echo "==> Create tree"
TREE_PAYLOAD=$(jq -nc --arg base "$BASE_TREE" --argjson tree "$TREE_ITEMS" '{base_tree:$base, tree:$tree}')
NEW_TREE_SHA=$(curl -s -H "$AUTH" -H "$ACCEPT" -H "$CT" -X POST -d "$TREE_PAYLOAD" "${BASE}/git/trees" | jq -r '.sha')
echo "NEW_TREE_SHA=$NEW_TREE_SHA"

echo "==> Create commit"
COMMIT_MSG="refactor(pipeline): v2 - research stage, dynamic expert panel, split QA, autonomous trigger contract

- Add Stage 1 Research & evidence (sourcing every claim before draft)
- Replace fixed 8-expert panel with dynamic regulator selection + always-on Editorial reviewer
- Split QA gate into pre-publish (markdown-verifiable) and post-publish (live URL)
- Route QA failures by type instead of blanket Stage 1 restart
- Add workflow/trigger-contract.md defining what 'yaz' pre-authorizes"
COMMIT_PAYLOAD=$(jq -nc --arg msg "$COMMIT_MSG" --arg tree "$NEW_TREE_SHA" --arg parent "$MAIN_SHA" '{message:$msg, tree:$tree, parents:[$parent]}')
NEW_COMMIT_SHA=$(curl -s -H "$AUTH" -H "$ACCEPT" -H "$CT" -X POST -d "$COMMIT_PAYLOAD" "${BASE}/git/commits" | jq -r '.sha')
echo "NEW_COMMIT_SHA=$NEW_COMMIT_SHA"

echo "==> Update main ref"
REF_PAYLOAD=$(jq -nc --arg sha "$NEW_COMMIT_SHA" '{sha:$sha, force:false}')
RESULT=$(curl -s -H "$AUTH" -H "$ACCEPT" -H "$CT" -X PATCH -d "$REF_PAYLOAD" "${BASE}/git/refs/heads/main")
echo "$RESULT" | jq '.'

echo "==> Done"
echo "Commit: https://github.com/${OWNER}/${REPO}/commit/${NEW_COMMIT_SHA}"
