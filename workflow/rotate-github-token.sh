#!/usr/bin/env bash
# rotate-github-token.sh
#
# Replaces the GitHub PAT used by the PSFnetwork pipeline.
# Asks the operator for the new token, writes it to the canonical token file
# (/Users/onur/.psfnetwork-drive/github-token), and runs a smoke test against
# the repo to verify the new token works.
#
# Usage:
#   bash workflow/rotate-github-token.sh
#
# The token file is the single source of truth for every script and the
# launchd cron. No script should hardcode the token.

set -euo pipefail

TOKEN_FILE="/Users/onur/.psfnetwork-drive/github-token"
REPO="ramsey-claude/psf-network-blog-production"

echo "Current token file: $TOKEN_FILE"
if [[ -f "$TOKEN_FILE" ]]; then
  OLD_LEN=$(wc -c < "$TOKEN_FILE" | tr -d ' ')
  echo "Current token length: ${OLD_LEN} chars"
else
  echo "No existing token file."
fi

echo ""
echo "Paste new GitHub PAT (it will not be echoed):"
read -rs NEW_TOKEN

if [[ -z "$NEW_TOKEN" ]]; then
  echo "ERROR: empty input." >&2
  exit 1
fi

# Smoke test the new token BEFORE replacing the old one
echo "Smoke testing new token against $REPO ..."
HTTP=$(curl -sS -o /tmp/token-smoke.json -w "%{http_code}" \
  -H "Authorization: Bearer $NEW_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$REPO")

if [[ "$HTTP" != "200" ]]; then
  echo "ERROR: new token failed smoke test (HTTP $HTTP):" >&2
  cat /tmp/token-smoke.json >&2 || true
  echo "" >&2
  echo "Old token file left in place. Aborting rotation." >&2
  exit 2
fi

# Atomic replace
umask 077
TMP_FILE=$(mktemp "${TOKEN_FILE}.XXXX")
printf '%s' "$NEW_TOKEN" > "$TMP_FILE"
chmod 600 "$TMP_FILE"
mv "$TMP_FILE" "$TOKEN_FILE"

echo "OK. New token written to $TOKEN_FILE (chmod 600)."
echo "Subsequent runs (Stage 9, Stage 10 cron, drive_cli.py) pick up the change automatically on next invocation."
