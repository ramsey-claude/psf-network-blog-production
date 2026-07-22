# Pre-publish QA Report: how-to-verify-fractional-real-estate-platform

Stage 7, run against `checklist/qa-gate.md` sections A through E.

| Field | Value |
|-------|-------|
| Slug | how-to-verify-fractional-real-estate-platform |
| Batch | 3 (pilot article) |
| Source draft | `draft.md` |
| Loop count | 1 (hero alt was 126 chars, trimmed to 105, re-run PASS) |
| QA date | 2026-07-22 |

## Results

| Section | Item | Result | Detail |
|---------|------|--------|--------|
| A | A3 risk disclosure with return references | PASS | No yield figures beyond category context; disclaimer block canonical |
| A | A4 no guaranteed language | PASS | 0 occurrences |
| A | A5 regulator references | PASS | Reg A Form 1-A/1-K, Reg D Form D, EDGAR full-text search, BrokerCheck described as broker-dealer lookup only |
| A | A6 no misleading comparisons | PASS | FINRA FAQ explicitly states platforms are issuers, not broker-dealers |
| B | B2 title 55-60 | PASS | 56 |
| B | B3 meta 150-160 | PASS | 159 |
| B | B5 hero alt 60-120 | PASS | 105 after fix |
| B | B6 single H1 with keyword | PASS | |
| B | B7 substantive H2s in question format | PASS | 5 of 5 ("What this routine does not do" is a closing admin section) |
| B | B10 FAQ >= 5 | PASS | 6 |
| B | B11 internal links | PASS | 3, all verified live on psfnetwork.com |
| C | C1 brand casing | PASS | |
| C | C2 no em or en dashes | PASS | |
| C | C7 canonical disclaimer | PASS | |
| C | scaffolding | PASS | No "Answer capsule" labels; capsules are natural openers |
| C | persona rules | PASS | Carla, unique across all 28 drafts, scenario framing with no testimonial claim; test_persona_uniqueness green |
| D | D2 hero placeholder | PASS | |
| D | D3 four stat cards | PASS | |
| D | D4 opening 2 paragraphs | PASS | |
| D | D5 sources numbered, all curl-verified live | PASS | 5 sources |
| D | D6/D7 blocks present, related = 3 | PASS | |
| E | check-rules.py | PASS | 0 BLOCKING, 0 WARNING |
| E | rhythm | PASS | 18 sentences under 6 words, 16 over 24 |
| E | tables fit mobile | PASS | No wide tables in this article |

## Word count

1,696 body words. Within cluster norms for a focused how-to (cluster range 1,683 to 2,821).

## Humanization

Produced humanized-first per the Batch 3 process; no separate v2 needed.
- Scenario anchor: Carla, claims adjuster, Cleveland, two-tabs image. No "told us" framing.
- POV anchor: "Run them on us. A platform that flinches at verification is answering your question for you."
- Contrarian anchor: scams are the rare case; the common loss is a legal offering unread. Stated in "What this routine does not do".

## Recommendation

PUBLISH. Deliver to the 07-July Drive folder as the Batch 3 pilot for operator review.
