# Expert Review Template

Use this template for each reviewer in Stage 3 (initial multi-agent review) and Stage 6 (post-localization re-check, conditional).

Stage 3 panel is dynamic. See `checklist/expert-routing.md` for which reviewers to invoke for a given post. Default panel for any investment content: SEC, FINRA, CFPB, Editorial. Topic-triggered additions per the routing table.

Each reviewer is a separate file: `expert-reviews/stage3-[reviewer].md` and (if re-check fires) `expert-reviews/stage6-[reviewer].md`.

---

## Review metadata

| Field | Value |
|-------|-------|
| Reviewer | <!-- SEC / FINRA / CFPB / OCC / FDIC / Fed / CFTC / FSOC / Editorial --> |
| Stage | <!-- Stage 3 / Stage 6 --> |
| Content title | |
| Review date | |
| Round position | <!-- 1st reviewer / 2nd / ... / Editorial (last reviewer) / Moderator (final) --> |
| Prior reviewers seen | <!-- list of reviewers whose output this reviewer read before writing --> |

---

## Output format (required)

Every reviewer outputs in this exact format. The moderator depends on it being parseable.

```
DOMAIN FINDINGS:
[Your specific findings within your domain. Concrete. Quote the draft when relevant.]

FLAGGED ISSUES:
1. [Issue description] - SEVERITY: HIGH / MED / LOW - FIX: [specific recommendation]
2. ...

RESPONSE TO PREVIOUS REVIEWERS:
[Agreements, disagreements, additions. Reference reviewers by name. If first reviewer in round, write "N/A - first in round".]

VERDICT: APPROVE / APPROVE_WITH_NOTES / REVISION_REQUIRED
```

---

## Domain prompts

Each reviewer applies the prompt below. Editorial uses its own checklist in `checklist/editorial-review.md`.

### SEC - Securities Markets
Focus on: securities offering language, Regulation A+ / Regulation D references, fund and vehicle descriptions, implied guarantees, disclosure adequacy. Check that "fractional ownership" is framed as ownership of an LLC interest (a security), not deed ownership.

### FINRA - Broker-Dealers
Focus on: investment return claims, risk disclosure placement, broker-dealer activity references, past-performance disclaimers, suitability framing.

### CFPB - Consumer Protection
Focus on: fee disclosures, APR and cost representations, deceptive-claim risk, required consumer disclosures, ease-of-understanding for non-accredited investors.

### CFTC - Futures & Derivatives (invoke only when content touches derivatives, futures, or tokenized assets)
Focus on: derivatives and futures product claims, commodity references, swap or leverage language, crypto asset references against current CFTC guidance.

### Fed - Monetary Policy (invoke only when content touches rates, inflation, or Fed actions)
Focus on: interest rate commentary, monetary policy claims, bank holding references, statements about rate direction.

### OCC - National Banks (invoke only when content touches bank lending, mortgages, national bank products)
Focus on: banking product comparisons, lending rate references, national bank charter references, bank product endorsements.

### FDIC - Deposit Insurance (invoke only when content touches deposits, savings products, or comparisons with bank accounts)
Focus on: FDIC insurance limits ($250,000 per depositor per insured bank), no implication that non-deposit investments are FDIC-insured, deposit vs investment product distinction.

### FSOC - Systemic Risk (invoke only when content touches macro stability, contagion, or systemic risk)
Focus on: proportionality of systemic risk statements, sourcing, too-big-to-fail framing.

### Editorial (always invoked, last among reviewers)
See `checklist/editorial-review.md`. Focus on: hook strength, answer capsule quality, narrative flow, sentence-level clarity, brand voice, banned constructions (em dashes, "guaranteed return", mis-cased brand name (must be PSFnetwork), etc.). <!-- check-rules: allow -->

---

## Severity guide

- **HIGH:** A regulatory or factual violation, or a reader-experience failure that materially harms the post (buries the answer, breaks brand voice, contains a banned construction). Must be fixed.
- **MED:** A meaningful issue that should be fixed but does not block publication on its own. Issue may be partially overridden if it conflicts with the post's core argument.
- **LOW:** A minor refinement. Apply only if it improves the content without adding work disproportionate to the gain.

---

## Multi-agent discussion protocol

Round order is set in `checklist/expert-routing.md`:

1. Regulators in order: SEC, FINRA, CFPB, then any others alphabetically
2. Editorial (always last reviewer)
3. Moderator (always after all reviewers)

Each reviewer reads every prior reviewer's output before writing. The RESPONSE TO PREVIOUS REVIEWERS section must reference at least one prior finding (agree, disagree, or extend) unless this reviewer is first in the round.

The moderator's job is in `checklist/moderator.md`. The moderator does not flag new issues - it consolidates, deduplicates, resolves conflicts, and decides whether the post enters Stage 4 (revision) or loops back to Stage 2 (rewrite) per the 3-HIGH rule.
