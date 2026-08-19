# PSFnetwork blog production

[![Content rules](https://github.com/ramsey-claude/psf-network-blog-production/actions/workflows/lint-content.yml/badge.svg)](https://github.com/ramsey-claude/psf-network-blog-production/actions/workflows/lint-content.yml)

End-to-end blog production pipeline for PSFnetwork, from draft to published, with humanization, multi-expert regulatory review, localization, and QA gates.

## Quick start

```bash
make setup       # create venv, install pinned deps
make lint        # run brand-voice and grammar checks
make test        # run pytest suite
make brain       # rebuild the operation's knowledge index
make status      # repo health snapshot
```

Start a session at `CLAUDE.md`, then `brain/README.md`. See `CONTRIBUTING.md`
for contributor protocol and `SECURITY.md` for the security policy.

## The brain

`brain/` is the operation's memory: one indexed place for what is decided, what
is in force, what has gone wrong, what has shipped, and what is left to write.

```bash
python3 workflow/brain.py search "drive delivery gate"   # ranked recall with file:line
python3 workflow/brain.py rules --category tooling        # rules in force, and what checks them
python3 workflow/brain.py stats                           # what the brain holds
```

Curated pages (`brain/decisions.md`, `brain/canon/`, `brain/playbooks/`) hold
knowledge with no other home. Generated registries (`brain/rules.md`,
`incidents.md`, `articles.md`, `topics.md`, `index.md`) are rebuilt from the
files that own those facts, and `brain.py check` runs in CI so an index that
drifts from its sources fails the build. Full explanation in
`brain/README.md`.

## The clone

`mind/` is a person's own knowledge rather than this project's: beliefs,
decision heuristics, preferences, judgment. It is not about PSFnetwork or any
other single job, and it does not depend on the rest of this repo. The engine
is one self-contained file in git; the clone itself lives in `~/.mind`, outside
version control.

```bash
python3 workflow/mind.py init          # create the store (empty, it fills from answers)
python3 workflow/mind.py interview     # the next questions worth answering
python3 workflow/mind.py ask "..."     # what the clone holds on a subject
python3 workflow/mind.py fidelity      # how often it predicts its owner correctly
```

`MIND_HOME` moves the store, `export` moves the whole thing to a private repo.
Guide in `mind/README.md`, agent protocol in `mind/AGENT.md`.

## Overview

Every blog post goes through a structured pipeline before publication. The pipeline combines the SEO & GEO blog checklist with a humanization pass and a financial regulatory review layer specific to PSFnetwork's fractional real estate content.

```
Draft → Humanization Pass → Expert Panel Review → Revision → Localization → Expert Re-check → QA → Publish
           ↑                                                                                       ↓ (fail)
           └──── rewrite ──── Back to Draft ──────────────────────────────────────────────────────┘
```

## Pipeline Stages

The pipeline uses one authoritative stage numbering. See `workflow/pipeline.md` Stage map for the full table. The short version below is the production path a brief follows from input to delivery.

| Stage | Name | Output |
|-------|------|--------|
| 1 | Research and evidence | `evidence.md`, `serp-snapshot.md` |
| 2 | Draft generation | `draft.md` |
| 2.5 | Humanization pass | revised `draft.md`, `humanization-log.md` |
| 3 | Expert and editorial review | `expert-reviews/stage3-*.md` |
| 4 | Revision | revised `draft.md`, `changelog.md` |
| 5 | Localization | `localization-notes-EN-US.md` |
| 6 | Expert re-check (conditional) | `expert-reviews/stage6-*.md` |
| 7 | Pre-publish QA | `qa-report.md` (or `qa-report-vN.md`) |
| 8 | Publish | commit on `main` |
| 9 | Client delivery | `delivery-manifest.md` + Drive doc |
| 10 | Post-publish QA | `post-publish-report.md` |
| 11 | Post-run workflow QA | updated `workflow/incident-log.md` |

Optional pre-stages (-4 to -1) handle incident-log readout, gap discovery, brief generation, and topic selection when the trigger does not specify a slug. Full spec in `workflow/pipeline.md`.

### Stage 2.5: Humanization Pass (the new gate)
A dedicated reviewer rewrites the draft to sound like a person wrote it. This is the only stage with the explicit mandate to break AI cadence and inject human signal. Six steps:

1. AI tells sweep (per `checklist/ai-tells.md` ban list)
2. Human anchor injection (real story, POV, contrarian note, sourced from the brief)
3. Rhythm and cadence rewrite (sentence and paragraph length variance)
4. De-listification (at least 40% narrative H2s)
5. Voice consistency (second person throughout)
6. Specificity audit (named subjects, dollar figures, dates, no generic claims)

The draft cannot enter Stage 3 with any HIGH-tier AI tell unresolved, all three Human Anchors missing, or a failed cadence/voice check. See `checklist/humanization-pass.md`.

### Stage 3: Expert Panel Discussion
Eight US financial regulatory experts plus an editorial reviewer read the humanized draft, each from their own domain:

| Expert | Domain | Focus in PSFnetwork content |
|--------|--------|----------------------------|
| SEC | Securities Markets | Investment offering language, securities disclaimers |
| CFTC | Futures & Derivatives | Derivative product references, commodity language |
| Fed | Monetary Policy | Interest rate commentary, monetary policy claims |
| OCC | National Banks | Banking product comparisons, lending references |
| FDIC | Deposit Insurance | Deposit product language, insurance claim accuracy |
| CFPB | Consumer Protection | Consumer-facing claims, fee disclosures |
| FINRA | Broker-Dealers | Brokerage comparisons, investment return claims |
| FSOC | Systemic Risk | Macro-financial risk statements |
| Editorial | Reader experience and brand voice | Hook, capsule, flow, structure (see `checklist/editorial-review.md`) |

Each reviewer flags issues in their domain. The moderator (`checklist/moderator.md`) reaches consensus on required revisions before content advances to Stage 4.

### Stages 4 to 6: Revision, Localization, Re-check
Stage 4 applies consensus fixes from Stage 3, documented in `changelog.md`. Stage 5 localizes to US English (`target_markets: ["EN-US"]`, see `checklist/localization-guide.md`). Stage 6 runs the expert panel again ONLY if Stage 5 changed financial terms or disclosures, per `checklist/expert-routing.md`.

### Stage 7: Pre-publish QA Gate
Final pre-publication checklist (see `checklist/qa-gate.md`, Sections A through E). If any BLOCKING item fails, content routes back per the routing table; no blanket Stage 1 restart. Section E grammar checks added 2026-05-26 after customer feedback.

### Stages 8 to 11: Publish, Deliver, Monitor, Retrospect
Stage 8 commits all artifacts to `main`. Stage 9 delivers a native Google Doc to the operator's Drive folder via `workflow/deliver.py` (which enforces a QA-report check before upload). Stage 10 verifies the live URL once published. Stage 11 runs a once-per-batch retrospective plus meta-QA on pipeline artifacts (see `checklist/meta-qa.md`).

## Repository Structure

```
psf-network-blog-production/
├── README.md                              This file
├── CLAUDE.md                              Entry point for a session, human or agent
├── brain/
│   ├── README.md                          How the knowledge index works
│   ├── decisions.md                       Standing decisions with their evidence
│   ├── rules.md                           Generated: every rule in force, and what enforces it
│   ├── incidents.md                       Generated: the incident timeline and open issues
│   ├── articles.md                        Generated: every article folder and its state
│   ├── topics.md                          Generated: the gap pool matched against what shipped
│   ├── canon/                             Brand, product, compliance, systems, glossary
│   └── playbooks/                         Runbooks for the jobs that recur
├── checklist/
│   ├── ai-tells.md                        Ban list of AI-generated language tells
│   ├── humanization-pass.md               Stage 1 humanization spec
│   ├── brief-required-sections.md         Brief format including Human Anchors
│   ├── seo-geo-blog-checklist.md          Full SEO & GEO production checklist
│   ├── expert-review-template.md          Per-expert review form
│   ├── editorial-review.md                Editorial reviewer checklist (Stage 2)
│   ├── localization-guide.md              Localization rules and scope (US/EN only)
│   └── qa-gate.md                         QA gate criteria and failure protocol
├── workflow/
│   ├── pipeline.md                        Detailed pipeline steps and decision trees
│   ├── brain.py                           Knowledge index and recall (build, check, search)
│   └── loop-log-template.md               Template for logging pipeline restarts
└── brand/
    ├── tone-and-voice.md                  PSFnetwork brand voice for content producers
    ├── personas.md                        Target audience personas
    └── voice-samples/                     Reference writing samples from PSFnetwork team
```

## Brand Notes

- Brand name is always written as **PSFnetwork**: capital PSF, lowercase "network", one word, no spaces
- Brand colors: Cream #F7F5F0 | Matte Black #1C1C1C | Orange #FF7141 | Blue #4F8FA3
- Font: Söhne (Kräftig, Halbfett, Buch)
- Visual/video assets: produced by Superclasico
- Written content: AI-drafted, humanization-reviewed, regulator-cleared

## Related Repositories

- [psfnetwork-blog-template](https://github.com/ramsey-claude/psfnetwork-blog-template), Blog template, brand guidelines, Framer components
- [GEO-SEO-Blog-Writing-](https://github.com/ramsey-claude/GEO-SEO-Blog-Writing-), SEO & GEO blog checklist (source)
