Stage 7 QA: 33/33 PASS. Loop 0. PUBLISH.

## Re-QA 2026-06-10 (client-feedback revision)
- check-rules.py --diff-base main: 0 BLOCKING, 3 WARNING (grammar-runon).
  - All 3 warnings are pre-existing sentences (lines 32, 56, and the first clause
    of 101), not introduced by this revision.
  - The run-on introduced by the new PSFnetwork positioning line was split and cleared.
- pytest tests/: 37/37 PASS.
- Verdict: PASS, clear to publish. No blocking findings from the tone/positioning edits.

## Brand-casing standard change 2026-06-10
- Brand name standardized to "PSFnetwork" (capital PSF, one word).
- check-rules.py psfnetwork-casing rule inverted: a lowercase brand spelling used as a
  brand name is now BLOCKING; URLs (psfnetwork.com), dotted identifiers
  (com.psfnetwork.stage10), and hyphen/slash/colon identifiers stay exempt.
- brand/tone-and-voice.md terminology table updated to match.
- Swept all 12 blog drafts + governance docs (brand/, checklist/, workflow/, root).
- Left untouched: historical records (qa-report/changelog/post-publish/incident-log)
  and competitor notes, which are point-in-time and out of lint scope.
