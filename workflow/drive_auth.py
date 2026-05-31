#!/usr/bin/env python3
"""
One-shot OAuth flow to mint a Drive-scoped token for the PSFnetwork pipeline.

Reuses the existing OAuth client at /Users/onur/gsc-mcp/credentials.json
(GCP project: seo-kpi-449217) and adds Drive scope on top of any prior scope.

Stores the resulting token at /Users/onur/.psfnetwork-drive/token.json.

Run once interactively. After that, drive_cli.py uses the saved token
(auto-refreshing as needed) for all Drive operations from the pipeline.

Usage:
    .venv/bin/python3 workflow/drive_auth.py
"""
import json
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS = Path('/Users/onur/gsc-mcp/credentials-ozgurzaman.json')  # project: my-project-82896
TOKEN_PATH = Path('/Users/onur/.psfnetwork-drive/token.json')
SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    if not CLIENT_SECRETS.exists():
        raise SystemExit(f'OAuth client file not found at {CLIENT_SECRETS}')

    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS), SCOPES)
    # run_local_server starts a local HTTP server, opens the browser, and
    # captures the auth code on the localhost redirect.
    creds = flow.run_local_server(port=0, open_browser=True)

    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_PATH.write_text(creds.to_json())
    print(f'Wrote token to {TOKEN_PATH}')
    print('Scopes:', creds.scopes)


if __name__ == '__main__':
    main()
