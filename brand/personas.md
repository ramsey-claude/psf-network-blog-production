# PSFnetwork Standing Personas

PSFnetwork uses standing author and reviewer personas for blog content. The reviewer persona is a brand-approved byline, not a real individual; the author byline is a real member of the PSFnetwork team. Operator has authorized their automated use across the pipeline. No per-post operator approval is required.

This file is the source of truth for who appears in the byline and credit on every post.

---

## Author byline (operator directive, 2026-08-16)

**Every post is bylined to a real PSFnetwork person: either Youssef or Omar. No other name goes in the `author` field.**

The invented editor persona that previously held this slot is retired. It was corrected in Framer on the live articles, and the pipeline must not reintroduce it, on any batch, at any stage.

### Youssef Kholeif - CMO

- **Byline string:** `Youssef Kholeif`. The title is NOT part of it. The CMS
  Author collection stores the name and the role in separate fields, Author
  and Position, and Youssef's Position already reads `CMO, PSFnetwork`. A
  combined "Youssef Kholeif, CMO" string matches no Author item, which is one
  of the two reasons the byline failed to import on 2026-08-17.
- **CMS slug:** `youssef-kholeif`. A reference resolves by slug, not by the
  displayed name; sending the name left the byline unrendered on all 15
  Batch 2 pages.
- **Short Bio:** empty in the CMS as of 2026-08-17, for Youssef and for every
  other Author item. The AuthorCard therefore has no bio to show on any
  article, Batch 1 included. Operator decision whether to write one.
- **Role on post:** Author byline
- **Appears in:** `author` field (YAML frontmatter or Production Notes), ArticleHero component, AuthorCard component
- **Bio (canonical):** Youssef Kholeif is the CMO of PSFnetwork, writing on fractional real estate, real-asset investing, and consumer finance.
- **Quotable:** No. The byline is the article's voice; quotes attributed to Youssef are not placed in body content.
- **Status:** Confirmed. Already carried by `real-estate-as-an-asset-class`, applied by Youssef himself in the round-2 Drive doc, and the default byline for the rest of Batch 2.

### Omar Elghazaly

- **Byline string:** `Omar Elghazaly`. Spelling confirmed against the CMS
  Author collection on 2026-08-17, exactly as recorded here.
- **CMS slug:** not read yet. Read it off the Author collection before using
  this byline; do not assume it mirrors the name.
- **Role on post:** Author byline
- **Appears in:** `author` field (YAML frontmatter or Production Notes), ArticleHero component, AuthorCard component
- **Bio (canonical):** pending. Needs one sentence from the operator, in the shape of Youssef's above.
- **Quotable:** No, same rule as the Youssef byline.
- **Title:** the question is moot in the CMS, which keeps the role in its own
  Position field rather than in the byline. Omar's Position is whatever the
  Author collection holds; nothing needs inventing here.
- **Status:** Usable. No article is assigned to this byline yet; all 15 Batch 2 articles carry the Youssef byline. Reassignment is a per-article operator decision, not a default.
- **Spelling:** supplied as `omar-elghazaly`, which is handle form. Rendered here as `Omar Elghazaly`. Correct this line if the capitalisation differs.

### Retired: the previous editor persona

- **Status:** Retired 2026-08-16. Not a valid byline on any new or revised draft.
- **Published Batch 1 content:** the live articles carry the corrected byline in Framer. Batch 1's repo drafts still show the old persona because published batches are frozen (see `workflow/incident-log.md`, 2026-08-13). That gap is recorded debt, not something to sweep-fix in place.
- **Automation:** `qa_battery.py` W8 flags any draft whose author is not an approved byline.

---

## Standing personas

### Daniel Cho, CFA - Reviewer

- **Role on post:** Editorial reviewer credit
- **Appears in:** Frontmatter `reviewer` field, TOC reviewer credit line, AuthorCard "Reviewed by"
- **Bio (canonical):** Daniel Cho, CFA, is an investment strategist and former real estate analyst.
- **Voice:** Analytical, concise, factually anchored.
- **Quotable:** Yes, within rules below.

---

## Quote rules (Daniel Cho, CFA)

Pull quotes attributed to Daniel Cho appear in some posts to add analytical authority. Rules:

1. **Restate, do not introduce.** A Daniel Cho quote may only restate or sharpen a point that is already supported by `evidence.md` and present in the post's own analysis. Never use a quote to introduce a new factual claim that does not appear elsewhere in the post with a source.
2. **No specific numbers in the quote.** Numbers belong in the body with citations, not in the persona's mouth. Quotes are interpretive ("The clearest way to understand X is..."), not factual ("4.7% of portfolios...").
3. **No predictive claims.** No "will", "is going to", "expected to rise". Persona does not forecast.
4. **No advisory voice.** No "you should", no "buy", no "sell". Persona explains; it does not recommend.
5. **One quote per post maximum.** Quote is a flavor element, not a recurring device.
6. **Length:** 1 to 3 sentences, under 60 words total.

If a quote candidate violates any rule above, the pipeline does not produce the quote and the section runs without one.

---

## Disclosure

PSFnetwork's About page is responsible for disclosing the production model (AI-assisted content under standing editorial personas). The blog post itself does not need to repeat that disclosure - the Disclaimer block already covers the content's nature.

This separation is by operator decision. The pipeline does not author or modify the About page.

---

## Adding or rotating personas

To add a new standing persona, update this file and `brand/tone-and-voice.md`. Any persona used in a post byline or reviewer credit must appear here first. The pipeline rejects any author/reviewer name not present in this file.

---

## What the pipeline does NOT do

- Generate quotes from Maya Reyes
- Generate forecasting or advisory quotes from Daniel Cho
- Use any author or reviewer name not listed here
- Mark content as written by a non-persona without operator instruction
