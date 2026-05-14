#!/bin/bash
set -euo pipefail
cd /Users/onur/psfnetwork-pipeline
TOKEN=$(tr -d '\n' < /Users/onur/.psfnetwork-drive/github-token)
OWNER="ramsey-claude"
REPO="psf-network-blog-production"
BASE="https://api.github.com/repos/${OWNER}/${REPO}"
AUTH="Authorization: Bearer ${TOKEN}"
ACCEPT="Accept: application/vnd.github+json"
CT="Content-Type: application/json"

FILES=("workflow/incident-log.md" "workflow/scripts/push-stage11-active-rules.sh")

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

COMMIT_MSG="chore(incident-log): tighten Active Rules > Content quality

Followup to 79d66cc — the Stage 11 commit added the incident history
entries but the matching Active Rules tightening got lost to an
en-dash mismatch on the first Edit attempt. Applying now:

- Capsule rule: sections with 4+ concrete points -> 3 in capsule, 4th in body
- Title/meta: hard-count BOTH directions; 'shortest viable' is shortest
  WITHIN the range, not absolutely shortest
- Stage 7 micro-fix budget: <=2 normal, 3 boundary (log pattern), 4+ escalate"
COMMIT_PAYLOAD=$(jq -nc --arg msg "$COMMIT_MSG" --arg tree "$NEW_TREE_SHA" --arg parent "$MAIN_SHA" '{message:$msg, tree:$tree, parents:[$parent]}')
NEW_COMMIT_SHA=$(curl -s -H "$AUTH" -H "$ACCEPT" -H "$CT" -X POST -d "$COMMIT_PAYLOAD" "${BASE}/git/commits" | jq -r '.sha')

REF_PAYLOAD=$(jq -nc --arg sha "$NEW_COMMIT_SHA" '{sha:$sha, force:false}')
curl -s -H "$AUTH" -H "$ACCEPT" -H "$CT" -X PATCH -d "$REF_PAYLOAD" "${BASE}/git/refs/heads/main" > /dev/null

echo "Commit: https://github.com/${OWNER}/${REPO}/commit/${NEW_COMMIT_SHA}"
