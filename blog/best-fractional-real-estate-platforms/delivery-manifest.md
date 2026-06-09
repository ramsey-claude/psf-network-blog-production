# Drive Delivery Manifest: best-fractional-real-estate-platforms

Folder: https://drive.google.com/drive/folders/1jKP0k2m8tg6QeRKQEtzvx9jRWiuvwWqY

## v1 (original, Stage 3 approved, Stage 7 PASS)
Doc: https://docs.google.com/document/d/1ltEx81E3evOVl9veucPpgvNl4YHVoep4byzD_d_mHDs/edit
Delivered: 2026-05-14
QA report: `qa-report.md`

## v2 (humanized, retroactive Stage 2.5 pass, plus grammar + mobile + link fixes)
Doc: https://docs.google.com/document/d/1Y2VdTijtikhDlivhyh8kubS9Sm1xlNxs0U0QVHHi1BM/edit
Delivered: 2026-05-26 (grammar + mobile + link verification pass on customer feedback)
Source: `draft-v2-humanized.md`
Change log: `draft-v2-humanization-log.md`
QA report: `qa-report-v2.md` (also at `qa-report-v2-humanized.md` for deliver.py naming match)
Note: v1 retained for before/after comparison rather than deleted.

DELIVERY_RESULT: SUCCESS, 2 native gdocs (v1 + v2.1), 3 prior v2 docs deleted and replaced through QA cycles.

## Delivery loop history
| Attempt | Doc ID | Outcome | Reason |
|---------|--------|---------|--------|
| v2-attempt-1 | 1R4NDC6BOiDmQ6yAlaxsJld_DH0G6aATe5yhfdhaWSz0 | DELETED | Em-dashes leaked (no QA run before delivery) |
| v2-attempt-2 | 12oQkthizkKQ8gagKNfmmKkf2mD2h840kiNxcjJfUgbI | DELETED | Em-dashes purged but Stage 7 QA still skipped; B7 + A4 failures surfaced later |
| v2-attempt-3 | 1hpPIG9qNfOdX-3x50gVV7ZJZUwa5DZlgofQpZ9TRWlQ | DELETED | Stage 7 QA ran and passed but customer flagged grammar + mobile issues on review |
| v2-attempt-4 | 1aN9qwvyPU6vpbfVKQ4KYPnguffUMgpH_CU4TMA0QB6k | DELETED | Grammar pass applied, but Source 4 IRS K-1 link was still broken (404) |
| v2-attempt-5 | 1Y2VdTijtikhDlivhyh8kubS9Sm1xlNxs0U0QVHHi1BM | LIVE | All links verified: 3 internal slugs exist, 9 external URLs return 200 (after IRS K-1 URL fix) |

## v2-attempt-4 changes (current LIVE doc)
Grammar fixes applied to 9 locations:
- Awkward sentence "the question of which platform is more about whether" rewritten as two clearer sentences
- Quoted phrase syntax around "I own 14 square feet" smoothed (parenthetical instead of comma-flanked)
- Three comma splices fixed (lines covering $10 caveat, FAQ multi-platform answer, PSFnetwork vs Arrived answer)
- "the bigger split than people realize" rewritten as "matters more than people realize"
- Missing coordinating-conjunction comma added in "Hold positions on three platforms, and your accountant..."
- SEC Regulation A/D explanation restructured from one comma-laden run-on into three short sentences
- "Reviewed by Daniel Cho, CFA - investment strategist" colon-separated instead of hyphen-dash

Mobile readability fix on the comparison table:
- Reduced from 6 columns to 4 (Platform, Minimum, Income, Key trait)
- Liquidity column folded into a follow-up narrative paragraph that calls out the three exceptions (Ark7 secondary, Lofty marketplace, Fundrise quarterly redemption)
- "Structure" and "Notable" columns merged into a single "Key trait" cell per platform
- Table now fits comfortably on a phone screen in landscape and reads cleanly in portrait
