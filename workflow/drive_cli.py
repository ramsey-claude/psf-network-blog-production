#!/usr/bin/env python3
"""
Drive CLI helper for the psfnetwork pipeline.

Uses the token minted by drive_auth.py (Drive scope).

Operations:
    delete <fileId>
        Move a Drive file to trash and then permanently delete.

    upload-as-gdoc <local_path> <parent_folder_id> <title>
        Upload a .docx (or other convertible) file and convert to a native
        Google Doc. Returns {id, webViewLink} as JSON.

    upload-as-is <local_path> <parent_folder_id> <title> <mime_type>
        Upload a file without conversion. Returns {id, webViewLink}.

    list <folder_id>
        List children in a folder. Returns JSON.

Usage:
    .venv/bin/python3 workflow/drive_cli.py <command> [args...]
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

TOKEN_PATH = Path('/Users/onur/.psfnetwork-drive/token.json')
SENTINEL_DIR = Path('/Users/onur/.psfnetwork-drive')
AUTH_BROKEN_SENTINEL = SENTINEL_DIR / 'auth-broken-drive'
SCOPES = ['https://www.googleapis.com/auth/drive']


def _write_broken_sentinel(reason):
    SENTINEL_DIR.mkdir(parents=True, exist_ok=True)
    AUTH_BROKEN_SENTINEL.write_text(json.dumps({
        'reason': reason,
        'checked_at': datetime.now(timezone.utc).isoformat(),
        'remediation': 'Run .venv/bin/python3 workflow/drive_auth.py to re-mint the token.',
    }, indent=2) + '\n')


def _clear_broken_sentinel():
    if AUTH_BROKEN_SENTINEL.exists():
        AUTH_BROKEN_SENTINEL.unlink()


def get_service():
    if not TOKEN_PATH.exists():
        _write_broken_sentinel('token file missing')
        raise SystemExit(f'Token not found at {TOKEN_PATH}. Run drive_auth.py first.')
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                TOKEN_PATH.write_text(creds.to_json())
            except RefreshError as e:
                _write_broken_sentinel(f'refresh failed: {e}')
                raise SystemExit(
                    f'Token refresh failed: {e}. Re-run drive_auth.py to re-mint the token.'
                )
        else:
            _write_broken_sentinel('token invalid; no refresh token available')
            raise SystemExit('Token invalid and cannot refresh. Re-run drive_auth.py.')
    _clear_broken_sentinel()
    return build('drive', 'v3', credentials=creds)


def cmd_health():
    """Verify Drive token works. Outputs ok / broken JSON and exit code."""
    try:
        svc = get_service()
    except SystemExit as e:
        print(json.dumps({
            'status': 'broken',
            'reason': str(e),
            'sentinel': str(AUTH_BROKEN_SENTINEL),
            'checked_at': datetime.now(timezone.utc).isoformat(),
        }), file=sys.stderr)
        sys.exit(1)
    try:
        svc.about().get(fields='user(emailAddress)').execute()
    except HttpError as e:
        _write_broken_sentinel(f'health check HTTP error: {e}')
        print(json.dumps({'status': 'broken', 'error': str(e)}), file=sys.stderr)
        sys.exit(1)
    print(json.dumps({'status': 'ok', 'checked_at': datetime.now(timezone.utc).isoformat()}))


def cmd_delete(file_id):
    svc = get_service()
    svc.files().delete(fileId=file_id, supportsAllDrives=True).execute()
    print(json.dumps({'deleted': file_id}))


def cmd_upload_as_gdoc(local_path, parent_id, title):
    svc = get_service()
    metadata = {
        'name': title,
        'parents': [parent_id],
        'mimeType': 'application/vnd.google-apps.document',
    }
    media = MediaFileUpload(
        local_path,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        resumable=False,
    )
    f = svc.files().create(
        body=metadata,
        media_body=media,
        fields='id,name,mimeType,webViewLink',
        supportsAllDrives=True,
    ).execute()
    print(json.dumps(f))


def cmd_upload_as_is(local_path, parent_id, title, mime_type):
    svc = get_service()
    metadata = {'name': title, 'parents': [parent_id], 'mimeType': mime_type}
    media = MediaFileUpload(local_path, mimetype=mime_type, resumable=False)
    f = svc.files().create(
        body=metadata,
        media_body=media,
        fields='id,name,mimeType,webViewLink',
        supportsAllDrives=True,
    ).execute()
    print(json.dumps(f))


def cmd_list(folder_id):
    svc = get_service()
    q = f"'{folder_id}' in parents and trashed = false"
    result = svc.files().list(
        q=q,
        fields='files(id,name,mimeType,size,webViewLink)',
        supportsAllDrives=True,
    ).execute()
    print(json.dumps(result.get('files', []), indent=2))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    try:
        if cmd == 'delete':
            cmd_delete(*args)
        elif cmd == 'upload-as-gdoc':
            cmd_upload_as_gdoc(*args)
        elif cmd == 'upload-as-is':
            cmd_upload_as_is(*args)
        elif cmd == 'list':
            cmd_list(*args)
        elif cmd == 'health':
            cmd_health()
        else:
            print(f'Unknown command: {cmd}')
            sys.exit(2)
    except HttpError as e:
        print(json.dumps({'error': str(e), 'status': e.resp.status if e.resp else None}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
