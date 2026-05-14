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
SLUG="reg-a-vs-reg-d-for-fractional-investors"

FILES=(
  "blog/${SLUG}/brief.md"
  "blog/${SLUG}/outline.md"
  "blog/${SLUG}/serp-snapshot.md"
  "blog/${SLUG}/claim-inventory.md"
  "blog/${SLUG}/evidence.md"
  "blog/${SLUG}/draft.md"
  "blog/${SLUG}/changelog.md"
  "blog/${SLUG}/localization-notes-EN-US.md"
  "blog/${SLUG}/qa-report.md"
  "blog/${SLUG}/pipeline-state.json"
  "blog/${SLUG}/expert-reviews/stage3-panel-selection.md"
  "blog/${SLUG}/expert-reviews/stage3-sec.md"
  "blog/${SLUG}/expert-reviews/stage3-finra.md"
  "blog/${SLUG}/expert-reviews/stage3-cfpb.md"
  "blog/${SLUG}/expert-reviews/stage3-editorial.md"
  "blog/${SLUG}/expert-reviews/stage3-moderator-consensus.md"
  "workflow/scripts/push-blog-reg-a-vs-reg-d.sh"
)

MAIN_SHA=$(curl -s -H "$AUTH" -H "$ACCEPT" "${BASE}/git/ref/heads/main" | jq -r '.object.sha')
BASE_TREE=$(curl -s -H "$AUTH" -H "$ACCEPT" "${BASE}/git/commits/${MAIN_SHA}" | jq -r '.tree.sha')

TREE_ITEMS="[]"
for F in "${FILES[@]}"; do
  if [[ ! -f "$F" ]]; then
    echo "MISSING: $F" >&2
    exit 1
  fi
  CONTENT_B64=$(base64 < "$F" | tr -d '\n')
  PAYLOAD=$(jq -nc --arg c "$CONTENT_B64" '{content:$c, encoding:"base64"}')
  BLOB_SHA=$(curl -s -H "$AUTH" -H "$ACCEPT" -H "$CT" -X POST -d "$PAYLOAD" "${BASE}/git/blobs" | jq -r '.sha')
  echo "  $F  ->  $BLOB_SHA"
  TREE_ITEMS=$(jq -c --arg p "$F" --arg s "$BLOB_SHA" '. + [{path:$p, mode:"100644", type:"blob", sha:$s}]' <<<"$TREE_ITEMS")
done

TREE_PAYLOAD=$(jq -nc --arg base "$BASE_TREE" --argjson tree "$TREE_ITEMS" '{base_tree:$base, tree:$tree}')
NEW_TREE_SHA=$(curl -s -H "$AUTH" -H "$ACCEPT" -H "$CT" -X POST -d "$TREE_PAYLOAD" "${BASE}/git/trees" | jq -r '.sha')

COMMIT_MSG="feat(blog): publish reg-a-vs-reg-d-for-fractional-investors

Stage -2 generation from ROADMAP Step 2 item 13. Spoke of the
fractional-real-estate-investing hub; natural complement to the
just-shipped K-1 tax post (explains the regulatory framework that
produces the K-1).

Panel: SEC + FINRA + CFPB + Editorial. 0 HIGH, 5 MED (all resolved
at Stage 4), 14 LOW. Loop count 0/3. Stage 7 made three micro-fixes
within budget (title 53->58, meta 143->155, section-5 capsule 83->65).

9 sources, all SEC primary (via investor.gov + SEC.gov resource pages
+ EDGAR per the federal-fetch substitution rule). 25 claims across 20
evidence rows; no marketing-page citations for regulatory facts."
COMMIT_PAYLOAD=$(jq -nc --arg msg "$COMMIT_MSG" --arg tree "$NEW_TREE_SHA" --arg parent "$MAIN_SHA" '{message:$msg, tree:$tree, parents:[$parent]}')
NEW_COMMIT_SHA=$(curl -s -H "$AUTH" -H "$ACCEPT" -H "$CT" -X POST -d "$COMMIT_PAYLOAD" "${BASE}/git/commits" | jq -r '.sha')

REF_PAYLOAD=$(jq -nc --arg sha "$NEW_COMMIT_SHA" '{sha:$sha, force:false}')
curl -s -H "$AUTH" -H "$ACCEPT" -H "$CT" -X PATCH -d "$REF_PAYLOAD" "${BASE}/git/refs/heads/main" > /dev/null

echo ""
echo "Commit: https://github.com/${OWNER}/${REPO}/commit/${NEW_COMMIT_SHA}"
