# Patch archive

A running history of significant changes, kept as `git format-patch` files so
the team has a durable, reviewable record and a continuous checking point even
when a change has not yet reached the remote (for example, while a session is
waiting on push permissions).

## Convention

* One file per significant change set.
* Name: `YYYY-MM-DD-short-description.patch`.
* Generate with: `git format-patch -1 <sha> --stdout > patches/<name>.patch`
  (or `-N` for a range).
* Each patch records its source commit SHA in the header, so it stays traceable
  back to the commit it came from.

## Applying a patch

```bash
git checkout -b <branch> main
git am < patches/<name>.patch
```

## Checking a patch without applying

```bash
git apply --check patches/<name>.patch   # verifies it applies cleanly
git apply --stat  patches/<name>.patch    # shows the files and line counts
```

## Index

| Date | Patch | Source commit | Summary |
|------|-------|---------------|---------|
| 2026-05-30 | `2026-05-30-rebrand-to-PSFnetwork-and-add-editorial-agent.patch` | `bba15b9` | Rebrand all prose to PSFnetwork, flip the `check-rules.py` casing rule and its tests, and add `brand/editorial-agent.md` (the editor charter with the punctuation ban, mandatory disclosure, Human Anchors, and reconciled sentence-rhythm guidance). 135 files. |
