# Pre-publish QA Report: fractional-real-estate-investing v2-humanized

Stage 7, run against `checklist/qa-gate.md` sections A through E.

| Field | Value |
|-------|-------|
| Slug | fractional-real-estate-investing |
| Version | v2-humanized |
| Source draft | `draft-v2-humanized.md` |
| Loop count | 0, passed first run |
| QA date | 2026-07-21 |
| Live status | v1 is currently published at psfnetwork.com/blog/fractional-real-estate-investing |

## Results

| Section | Item | Result | Detail |
|---------|------|--------|--------|
| A | A3 return claims carry risk disclosure | PASS | Stat card caveat plus canonical disclaimer block |
| A | A4 no guaranteed language | PASS | 3 occurrences in v1, 0 in v2 | <!-- check-rules: allow -->
| A | A1/A2 claims traced to evidence | PASS | No new factual claims introduced; every figure carried over from v1, which cleared Stage 3 |
| A | A5 regulator references accurate | PASS | Reg A Tier 2 $75M cap, Rule 506(b) 35-investor limit, 506(c) accredited-only, all unchanged from v1 |
| A | A6 no misleading regulated comparisons | PASS | REIT and FDIC distinctions intact |
| B | B1 frontmatter complete | PASS | All required fields plus version and v2_changes |
| B | B2 title 55-60 chars | PASS | 56 |
| B | B3 meta description 150-160 | PASS | 150 |
| B | B4 canonical correct | PASS | Corrected to www subdomain to match live site |
| B | B5 hero alt 60-120 | PASS | 117 |
| B | B6 single H1 with focus keyword | PASS | |
| B | B7 substantive H2s in question format | PASS | 6 of 6, unchanged from v1 by design |
| B | B8 QuickAnswer block at top | PASS | Heading intentionally left as "Quick Answer (60 seconds)" |
| B | B9 answer capsules 50-75 words | PASS | Capsule content retained, scaffolding label removed |
| B | B10 FAQ at least 5 entries | PASS | 6 |
| B | B11 at least 2 internal links | PASS | 3 |
| B | B12 external links from evidence | PASS | Sources unchanged except FDIC title corrected to match the live page |
| C | C1 brand casing | PASS | |
| C | C2 no em or en dashes | PASS | |
| C | C3 tone matches brand guide | PASS with note | v2 takes a stronger position than v1; see humanization log open items |
| C | C4 no internal contradictions | PASS | |
| C | C5 no orphaned paragraphs | PASS | |
| C | C6 author and reviewer are standing personas | PASS | Maya Reyes, Daniel Cho |
| C | C7 disclaimer matches canonical text | PASS | |
| C | C8 template components in order | PASS | |
| D | D1 type and topic in frontmatter | PASS | Explainer / Fractional Ownership |
| D | D2 hero placeholder present | PASS | |
| D | D3 four stat cards | PASS | |
| D | D4 opening is 2 paragraphs | PASS | |
| D | D5 sources numbered | PASS | 9 |
| D | D6 Author, Disclaimer, CTA, Related present | PASS | |
| D | D7 Related lists exactly 3 | PASS | |
| E | E1 no BLOCKING from check-rules.py | PASS | |
| E | E2 no comma splices flagged | PASS | |
| E | E3 no hyphen-as-em-dash | PASS | Author line colon-separated |
| E | E4 rhythm variance | PASS | 28 sentences under 6 words, 20 over 24 words |
| E | E5 wide tables fit mobile | PASS | Comparison table is 3 columns |

## Summary

- 34 PASS
- 0 FAIL
- 0 MANUAL

## Recommendation

PUBLISH. Replace the live v1 in Framer.

## Notes for the operator

Three things about this article are true independent of the QA result and need action in Framer:

1. The live page serves an **empty meta description**. The value exists in this draft's frontmatter and needs to be typed into the Framer SEO field.
2. The live page has **zero internal links**. This draft carries 3. They will need to be re-applied after pasting unless the paste method preserves them.
3. One of those 3 links points to `/blog/reits-vs-fractional-real-estate`, which is **not published**. It will 404 until that article ships.
