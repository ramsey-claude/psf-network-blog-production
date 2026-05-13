# Stage 3 Review - FINRA

| Field | Value |
|-------|-------|
| Reviewer | FINRA |
| Round position | 2 of 4 |
| Prior reviewers seen | SEC |

---

DOMAIN FINDINGS:

Return claims architecture is sound. The 4 to 10% range is labeled "platform-reported" and paired with "These figures are illustrative and not promised. Returns vary..." The stat card carries an inline italic footer with the "past performance" disclosure. The Opening explicitly anti-hypes ("'Passive' is the most oversold word in finance"). This is good practice.

The compounding table is bounded ("at 7% reinvested") and the body text notes "give or take" and references the rule of 72. Not overly precise.

FLAGGED ISSUES:

1. **Income table specificity ("$70 / $350 / $700 / $1,750 / $7,000 annual")** - SEVERITY: MED - FIX: Each row is an arithmetic projection at a specific yield. The body opening of the section already says "Returns vary by platform, vintage..." but the table itself does not carry an inline reminder. Add one sentence directly under the table: "Each row assumes a flat 7% annual yield throughout the year on a constant principal. Actual yields and principal values both vary, often materially."

2. **"Achieving it usually means reinvesting distributions for several years before drawing income"** - SEVERITY: LOW - FIX: Soft suggestion that has a path-dependency. Replace "usually means" with "for most investors means" to avoid implying a guaranteed timeline.

3. **CTA "Want to see the per-square-foot math on a real property?"** - SEVERITY: LOW - FIX: The CTA is hub-anchored, which is good for cross-link strategy. But asking the reader to "see the math" right after a math-heavy post can read as "we have better math here" - this is fine but skirts solicitation if the offering hasn't been qualified for the reader's accreditation. The follow-on language ("offerings are made only under qualified offering documents") covers this. Keep as is.

4. **REITs section table column "Reported yield range: Varies; tied to REIT performance"** - SEVERITY: LOW - FIX: Vague. Suggest a more specific qualifier: "Varies by REIT; publicly traded REITs are subject to daily market price movement that affects effective yield to a new buyer."

RESPONSE TO PREVIOUS REVIEWERS:

I agree with SEC flag #1 (direct rental 8-12% range). MED severity is appropriate; the table-vs-prose disconnect on caveats is the same pattern as the hub draft's stat card issue. Same fix pattern: bring caveats to the visual element, do not rely on adjacent prose.

I agree with SEC flag #3 ($171,000 anchor). Both my flag #1 and that one point to the same root cause: dollar-anchored specificity without inline qualification. The revision should address all three (direct rental table cell, income projection table, $171k figure) together.

VERDICT: APPROVE_WITH_NOTES
