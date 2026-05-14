# workflow/scripts/

One-shot push helpers and ad-hoc shell scripts go here, NOT in `/tmp/`.

The allowlist pattern `Bash(bash /Users/onur/psfnetwork-pipeline/*.sh)` covers any `.sh` file at the repo root. For per-batch scripts, prefer this subdirectory and reference them as `bash workflow/scripts/<name>.sh` from a working directory at the repo root, OR allowlist `Bash(bash /Users/onur/psfnetwork-pipeline/workflow/scripts/*.sh)` if you keep them here long-term.

Scripts that fire only once for a specific batch (e.g., a one-shot multi-file commit via the Git Data API) can be deleted after use. Long-lived helpers (token rotation, blog push template) belong at the repo root.

See `workflow/incident-log.md` 2026-05-15 entry "/tmp/*.sh ad-hoc push helper triggered prompt" for context.
