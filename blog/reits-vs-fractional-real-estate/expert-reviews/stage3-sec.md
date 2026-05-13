# Stage 3 Review - SEC

| Field | Value |
|-------|-------|
| Reviewer | SEC |
| Round position | 1 of 4 |
| Prior reviewers seen | N/A - first |

---

DOMAIN FINDINGS:

REIT structural framing is accurate and matches investor.gov source language. Three-form taxonomy (publicly traded, non-traded, private) is correct. The non-traded REIT risk callouts (liquidity, share value transparency at 18 months, distributions from offering proceeds, manager conflicts of interest) match the SEC's public statements on those products. Good.

Fractional framing correctly identifies investors as buying a security (LLC membership interest), not a deed. Reg A and Reg D referenced. K-1 introduced with a complexity flag and tax-advisor consult line, addressing prior-post concerns.

The CTA carries the qualified-offering-documents disclaimer, which is the right pattern.

FLAGGED ISSUES:

1. **REIT minimum cell in differences table: "Price of one share (some brokers offer fractional shares for less)"** - SEVERITY: LOW - FIX: Accurate but the "for less" framing could imply fractional shares are universally cheaper. Suggest: "Price of one share, or smaller if your broker offers fractional shares." Clearer and avoids implying a value judgment.

2. **"Average REIT dividend yield was over 4 percent in early 2026"** - SEVERITY: MED - FIX: The figure is widely cited but the post does not name the underlying source explicitly. Add a clause: "per industry data" or "per Nareit indices" and put the underlying source URL in Sources. Currently traced to NerdWallet (E8 in evidence.md), which is an aggregator rather than the underlying Nareit data. Consider adding the Nareit data page (already 200 OK in research) as a Sources entry.

3. **Non-traded REIT framing might suggest all non-traded REITs use offering proceeds for distributions** - SEVERITY: LOW - FIX: The investor.gov language says "frequently pay distributions in excess of their funds from operations" - I would soften "Non-traded REITs frequently pay distributions in excess of operating cash flow" rather than implying universal practice. Current wording is acceptable but a slight softening reduces overstatement.

4. **199A pass-through deduction reference** - SEVERITY: LOW - FIX: The post mentions "may qualify for a 20 percent pass-through deduction under current US tax rules" in two places. Accurate but the law is subject to sunset/changes. Add: "under current rules, which may change." This is a small future-proofing note.

RESPONSE TO PREVIOUS REVIEWERS:

N/A - first in round.

VERDICT: APPROVE_WITH_NOTES
