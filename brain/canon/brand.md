# Brand canon

The rules that make a PSFnetwork article recognisably PSFnetwork's. Sources are
`brand/tone-and-voice.md`, `brand/personas.md`, `brand/template-structure.md`,
and the ban list at `checklist/ai-tells.md`. When this page and those files
disagree, they win and this page is the bug.

## The name

PSFnetwork. Capital PSF, lowercase network, one word, no space. Every other
form is a blocking lint failure, including in headings, alt text, and file
prose. The lowercase form is exempt only inside a URL, path, or identifier such
as psfnetwork.com or the Drive folder psfnetwork/.

## Personality

Confident without shouting. Clear over clever. Optimistic and honest about
risk. Modern and direct, with no filler.

## Voice rules

1. Second person throughout. You, your. No first person in body content.
2. Short sentences, under 20 words where the sentence allows it.
3. Active voice. "Investors earn returns", not "Returns are earned by investors".
4. No superlative without proof.
5. No hype vocabulary. Nothing is revolutionary, game-changing, or disrupting.
6. Numbers beat adjectives. "12% annual return" says more than "strong returns".
7. Any return or performance claim carries risk disclosure in the same section.

## Terminology

| Use | Not |
|-----|-----|
| fractional ownership | fractional shares, which carries a securities connotation |
| PSFnetwork | psfnetwork, PSF Network, PSFNETWORK, Psfnetwork | <!-- check-rules: allow -->
| co-investors | shareholders, which is legally imprecise here |
| property | asset, too generic |
| exit | sell or liquidate, too transactional for the voice |
| target return | the word "guaranteed", which is banned in every form | <!-- check-rules: allow -->

## Punctuation

No em dash. No en dash. No double hyphen standing in for one. This is Tier 0 of
the ban list. The linter enforces it on every push, and it stays the single most
reliable signal that a machine wrote the sentence. Replace with a
period, sometimes a comma, occasionally a colon, or a middle dot in a list of
production fields. A sentence that cannot survive without one is a sentence
doing too much work; break it in two.

Hyphens are fine for ranges and compounds. A lone hyphen between two lowercase
words, surrounded by spaces, is an em dash in disguise and the linter says so.

## The disclaimer

Every piece that mentions returns, performance, or outcomes ends with the
canonical block from `brand/tone-and-voice.md`:

> Past performance is not indicative of future results. Fractional real estate
> investing involves risk, including the possible loss of principal. This
> content is for informational purposes only and does not constitute investment
> advice.

Rule: `R-content-quality-disclaimer`.

## Bylines

Two standing personas, and no others. Any third name fails the gate.

| Persona | Role | Quotable |
|---------|------|----------|
| Maya Reyes, Senior Editor | Author byline, ArticleHero, AuthorCard | No. The author voice is the article's voice. |
| Daniel Cho, CFA | Reviewer credit, TOC, AuthorCard | Yes, under the six quote rules below. |

A Daniel Cho quote may only restate a point the article already makes and
sources. No numbers inside the quote, no forecasts, no advice, one per article
at most, one to three sentences, under 60 words. If a candidate quote breaks
any of those, the section runs without a quote.

See D-015 for why these are standing bylines and where the production
disclosure lives.

## Colors and type

| Token | Hex | Use |
|-------|-----|-----|
| C01 Cream | #F7F5F0 | Background |
| C02 Matte Black | #1C1C1C | Primary text |
| C03 Orange | #FF7141 | CTA and accent |
| C04 Blue | #4F8FA3 | Secondary accent, links |

Typeface is Söhne (Kräftig, Halbfett, Buch). Visual and video assets are
produced by Superclasico. Shared visual styling for article graphics lives in
`workflow/visual-base.css`, and every rendered visual picks up a change there
on the next render.

## Article shape

Fifteen components in a fixed order, from ReadingProgress through Footer, of
which the draft authors ten: hero metadata, hero visual placeholder, quick
answer with exactly four stat cards, a two-paragraph opening with no headers,
question-format H2 sections each opening with a 50 to 75 word answer capsule,
an FAQ of at least five pairs, numbered sources, author card, disclaimer, CTA,
and exactly three related links. Full table in `brand/template-structure.md`.

## What the pipeline never does

- Put words in Maya Reyes's mouth as a quote.
- Let Daniel Cho forecast or advise.
- Use a byline that is not in `brand/personas.md`.
- Touch the About page.
