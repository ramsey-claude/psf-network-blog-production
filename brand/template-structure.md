# PSFnetwork Blog Template - Component Structure

Canonical component order for every blog post on PSFnetwork. The Stage 2 draft is written to map cleanly onto this order. Stage 7 QA verifies the draft contains every section.

Source: extracted from the PSFnetwork blog template (Railway deployment) in a prior session. The deployment is a React SPA; the template cannot be re-extracted via `WebFetch` alone (server returns the HTML shell, components render client-side). To re-verify, open the deployment in a browser and inspect the rendered DOM.

---

## Component order (top to bottom)

| # | Component | Role | Source in draft.md |
|---|-----------|------|--------------------|
| 1 | ReadingProgress | Sticky reading progress bar at top | (template chrome, not authored) |
| 2 | Nav | Site navigation | (template chrome) |
| 3 | ArticleHero | Type tag, topic tag, H1, dek, author, dates, read time | Frontmatter + H1 + dek line |
| 4 | HeroVisual | 1200x630 illustration | `[VISUAL-HERO-XX]` placeholder line |
| 5 | TOC | Sticky sidebar with section links + reviewer credit | Auto-generated from H2 list |
| 6 | QuickAnswer | 60-second summary + 4 stat cards | `## Quick Answer (60 seconds)` block + 4 stat lines |
| 7 | Opening | 2-paragraph hook, no headers | `## Opening` block, body only |
| 8 | H2 Sections | Each section: question-format H2, 50-75 word answer capsule, body, optional chart/pullquote | One `## [Question]` per section, capsule as first paragraph |
| 9 | FAQ | Accordion, minimum 5 Q/A pairs, schema-ready | `## FAQ` block, Q: / A: pairs |
| 10 | Sources | Numbered, linked | `## Sources` block, numbered list |
| 11 | AuthorCard | Name, credential, bio | `## Author` block |
| 12 | Disclaimer | Standard PSFnetwork disclaimer | `## Disclaimer` block (verbatim from `brand/tone-and-voice.md`) |
| 13 | CTABlock | Full-width call to action | `## CTA` block |
| 14 | Related | 3 related posts | `## Related` block, bulleted with internal links |
| 15 | Footer | Site footer | (template chrome) |

---

## Draft frontmatter (required at top of draft.md)

```yaml
---
title: "[Title tag, 55-60 characters, focus keyword in first third]"
slug: [slug]
type: [Explainer | Comparison | Guide | Listicle]
topic: [Topic tag]
author: Maya Reyes, Senior Editor
reviewer: Daniel Cho, CFA
read_time: [N] min
published: YYYY-MM-DD
updated: YYYY-MM-DD
focus_keyword: [focus keyword]
secondary_keywords: [list]
meta_description: "[150-160 characters, includes focus keyword and CTA]"
canonical: https://psfnetwork.com/blog/[slug]
hero_visual_alt: "[descriptive alt text for HeroVisual, 60-120 characters]"
---
```

Stage 7 QA verifies every field is populated and within length rules. See `checklist/qa-gate.md` section B.

---

## Section-level rules

### ArticleHero (component 3)
- Type tag and Topic tag are single short strings (1-3 words each)
- H1 is unique in the document
- Dek is 1-2 sentences, no period at end if 1 sentence
- Author and reviewer use the standing personas (see `brand/personas.md`)

### HeroVisual (component 4)
- Placeholder line in draft: `[VISUAL-HERO-XX]` with descriptive alt text in frontmatter
- Image production is out of pipeline scope; the draft signals where it goes

### TOC (component 5)
- Auto-generated from H2 list in the rendered page
- Draft does not author the TOC; it is derived

### QuickAnswer (component 6)
- Summary: 60 seconds = roughly 80-110 words
- 4 stat cards: each is a number + a one-line label

### Opening (component 7)
- 2 paragraphs, no internal headings
- First paragraph hooks; second paragraph names what the reader will get

### H2 Sections (component 8)
- Each H2 is a question (Nedir? How? Why? Is it?)
- First paragraph after the H2 is an answer capsule of 50-75 words, self-contained
- Body follows the capsule with detail
- Charts and pullquotes are optional per section

### FAQ (component 9)
- Minimum 5 Q/A pairs
- Q is a real reader question (use SERP People Also Ask from `serp-snapshot.md` when available)
- A is 60-100 words, self-contained

### Sources (component 10)
- Numbered list
- Each entry references a row in `evidence.md`
- Format: `1. Publisher, "Title", URL.` (date in evidence.md, not in inline citation)

### AuthorCard, Disclaimer, CTA, Related (components 11-14)
- Authored as the final blocks of draft.md
- Disclaimer text is verbatim from `brand/tone-and-voice.md`
- CTA is short, action-oriented, links to PSFnetwork product
- Related lists exactly 3 posts, each an internal link to a slug in `blog/`

---

## Out of scope for the pipeline

- ReadingProgress bar (component 1) - template chrome
- Nav (component 2) - template chrome
- TOC rendering (component 5) - derived at render time
- Footer (component 15) - template chrome

These are produced by the Railway template, not by the pipeline.
