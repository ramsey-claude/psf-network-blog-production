# Compliance canon

PSFnetwork writes about securities for retail readers, so the pipeline carries a
regulatory review layer that most content operations do not need. This page is
the map of that layer. The specs it summarises are `checklist/expert-routing.md`,
`checklist/expert-review-template.md`, `checklist/moderator.md`,
`checklist/research-stage.md`, and `checklist/qa-gate.md` Section A.

## The panel

Stage 3 is a sequential multi-agent review. Each reviewer reads every review
before it and responds, then a moderator writes the consensus that Stage 4 has
to apply.

Always present: SEC, FINRA, CFPB, and the Editorial reviewer. Editorial is not
removable and speaks last among reviewers.

Added when the article's subject calls for it:

| Subject in the brief or outline | Reviewer joins |
|---------------------------------|----------------|
| Deposits, savings products | FDIC |
| Bank lending, mortgages, national bank products | OCC |
| Interest rates, monetary policy, inflation | Fed |
| Derivatives, futures, commodities | CFTC |
| Systemic risk, financial stability, contagion | FSOC |
| Tokenization, crypto, digital assets | SEC and CFTC together |

Three or more HIGH findings from any reviewer, editorial included, sends the
draft back to Stage 2 and burns one of the three shared loops.

## Sourcing

Primary sources only for anything regulatory or numerical: SEC, IRS,
investor.gov, EDGAR, FINRA, FDIC, federalreserve.gov, congress.gov. A platform
marketing page is never a source for a regulatory fact.

The main sec.gov domain returns 403 to automated fetches. Route citations to
investor.gov, EDGAR full-text search at efts.sec.gov, or govinfo.gov, and use a
browser user agent when fetching federal pages. Rule:
`R-tooling-federal-sources`.

Every claim gets a row in `evidence.md` at Stage 1 before it can be drafted at
Stage 2. Articles from Batch 3 onward also carry at least two inline external
authority links inside the body, verified live, from that same domain list
(D-012).

## Language that fails the gate

- The word "guaranteed", in any form, including inside a quotation or a <!-- check-rules: allow -->
  negation. The noun form warns rather than blocks, so review it too.
- Any return or performance claim without risk disclosure in the same section.
- Misleading comparisons between regulated and unregulated products.
- Advisory voice from a persona: no "you should", no buy or sell.
- Forecasts from a persona: no "will", "is going to", "expected to rise".
- Positioning PSFnetwork as a traditional structure (D-014).

## Disclaimer

Non-negotiable, verbatim, at the end of every article. Text and rule in
[brand.md](brand.md).

## Where compliance sits in the run

Stage 2.5 is voice only and has no compliance mandate. That separation is
deliberate: the v2 pipeline had editorial embedded in the panel and it kept
losing voice arguments to reviewers focused on compliance, so drafts read as
machine-written. Compliance starts at Stage 3, and Stage 6 re-runs a targeted
version of the panel only when localization changed a financial term, a
disclosure, a number, or a regulatory reference. Under the US-only posture
(D-006) Stage 5 and Stage 6 are no-ops.
