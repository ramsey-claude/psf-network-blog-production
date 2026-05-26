# Stage 3: IRS Specialist Reviewer

**Reviewer scope:** IRS-domain accuracy, form numbers, recovery periods, passive activity rules under IRC §469, Section 1250 mechanics, partnership tax calendar, state-sourcing rules.

Prior reviews considered: SEC, FINRA, CFPB, all M-level findings on language/framing; no IRS-domain corrections raised.

## Findings

### HIGH
None.

### MED

**M1. The K-1 Box 13 / 20 reference is slightly imprecise.**
Section 2 says "Box 13 / 20, Various deductions and credits: depreciation is implicit in Box 2 (it has already been subtracted to arrive at the net figure), but Section 199A qualified business income figures and other deductions appear here."

Box 13 on the K-1 (Form 1065) is "Other deductions" (for items like Section 754 step-up, charitable contributions allocated to partners, etc.). Box 20 carries "Other information," and Section 199A QBI specifically appears in Box 20, Code Z. The current draft conflates the two boxes' contents. For a reader-facing explainer, exact box codes (13 vs 20 Code Z) are appropriate.

Suggested fix: "Box 20, Code Z, Section 199A qualified business income information; this is the box your CPA needs for the QBI deduction calculation."

**M2. The Section 199A reference itself is correct but underexplained for the audience.**
Section 199A (the qualified business income deduction) gives pass-through investors a potential deduction of up to 20% of qualified business income. For rental real estate, this is a complex area with a safe harbor (Revenue Procedure 2019-38) that requires specific documentation. The current draft references "Section 199A qualified business income figures" without explaining what they could mean for the investor.

This is a judgment call, adding a paragraph on §199A is genuinely useful but expands scope. Recommend: keep the reference but add a one-line note in the FAQ pointing readers to a CPA for §199A applicability. Better than expanding the main body and bloating the post.

### LOW

**L1. Form 1065 due date phrasing.**
The draft says "calendar-year partnerships must file Form 1065 by March 15 (March 16, 2026 for tax year 2025, because March 15 falls on a Sunday)." Verbatim accurate per IRS Instructions for Form 1065 (2025). No fix.

**L2. Section 1250 max 25% rate phrasing.**
"Maximum 25% rate" is the IRS-correct phrasing (Pub 544). Some readers will misread this as "always 25%." The current draft mitigates by showing the arithmetic and using "up to 25%" elsewhere. Acceptable.

**L3. Section 1031 exclusion of partnership interests.**
Draft correctly cites IRC §1031(a)(2). Some readers will be aware of pre-2017 rules where partnership interests had limited 1031 access; post-TCJA the exclusion is clearer. Could mention TCJA briefly for completeness, but adds scope. No fix.

**L4. UBTI in SDIRA FAQ.**
The mention of UBTI (unrelated business taxable income) in Q5 is technically correct, debt-financed real estate inside an IRA can trigger UBTI. For a fractional LLC that uses any leverage, this matters. The draft correctly says "specialist territory" and doesn't go deeper, which is right.

## Verdict

Pass with M1 (Box 13 vs 20 Code Z) as a concrete IRS-precision correction. M2 is optional scope expansion.

## Risk score
- High: 0
- Med: 2
- Low: 4
