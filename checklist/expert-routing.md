# Expert Panel Routing

Stage 3 runs a multi-agent review. The panel is dynamic. This document specifies how to choose which reviewers speak on a given post.

## Default panel

Every post about money, investing, or financial products gets at minimum:

- SEC
- FINRA
- CFPB
- Editorial reviewer (always present, not removable)

## Topic-triggered additions

Add to the panel based on what the post actually discusses:

| Topic signal in brief or outline | Add this reviewer |
|----------------------------------|-------------------|
| Bank accounts, deposits, savings products | FDIC |
| Bank lending, mortgages, national bank products | OCC |
| Interest rates, monetary policy, inflation, Fed actions | Fed |
| Derivatives, futures, commodities, crypto futures | CFTC |
| Systemic risk, financial stability, contagion | FSOC |
| Tokenization, crypto, digital assets | SEC + CFTC (both) |
| Insurance products | State insurance regulator reviewer (placeholder, flag for manual) |
| Tax treatment in depth | IRS specialist (placeholder, flag for manual) |
| Cross-border / non-US investor sections | Add a "cross-border" note to CFPB review scope |

## Removals from default

Drop a default reviewer if the topic clearly does not touch their domain. Examples:

- A post purely about real estate tax depreciation may drop FINRA but keep SEC and CFPB.
- A pure explainer on what a REIT is may drop CFPB if no consumer-facing claims are made (rare).

Removals must be justified in the panel selection output.

## Topic classifier

Before Stage 3 starts, classify the post by reading `brief.md` and `outline.md`. The classifier produces:

- Final panel list (regulators + editorial)
- One-line justification per included reviewer
- One-line justification per excluded default reviewer
- Confidence score (high / medium / low) on the classification

**Output:** `expert-reviews/stage3-panel-selection.md`

## Round order

1. SEC (if on panel)
2. FINRA (if on panel)
3. CFPB (if on panel)
4. Other regulators in alphabetical order
5. Editorial reviewer (always last among reviewers)
6. Moderator (always last)

Each reviewer reads all prior reviews in this round and responds to them in addition to giving their own findings.

## Verdict aggregation

The moderator counts HIGH severity issues across the panel. Editorial HIGH counts equally with regulator HIGH. Decision rule:

- 3+ HIGH from any combination of reviewers: rewrite loop (back to Stage 2)
- 0-2 HIGH: proceed to Stage 4

## Why dynamic

v1 used a fixed 8-reviewer panel. In practice most posts only touch 2-3 regulators meaningfully. Forcing irrelevant reviewers to find issues produced noise, inflated HIGH counts, and triggered false rewrite loops. The dynamic panel keeps every reviewer's findings substantive.
