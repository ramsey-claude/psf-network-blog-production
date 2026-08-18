# Blog cover image spec

Production spec for the `Hero Image` a blog article carries. Written
2026-08-18, after Batch 2's covers shipped with their headlines cut off on
the listing.

One file serves three surfaces, and only one of them shows it whole. That is
the whole reason this spec exists.

| Surface | What it does to the image |
|---------|---------------------------|
| Social preview (`og:image`) | Shows all of it. Wants 1.91:1. |
| Blog listing card | Crops the sides. Container is 1.44928. |
| Article hero | Same 1.44928 container. |

## The numbers

    File            1200 x 630 px   (1.90476, the og:image standard)
    Card container  1.44928
    Visible width   76.1%  =  913 px
    Cut per side    12.0%  =  143 px

The card scales the image to its own height and overflows horizontally, so
`object-fit: cover` with `object-position: center` throws away 143 px from
the left and 143 px from the right. Nothing is lost vertically.

## Safe zone

**Keep every word, logo and face inside x = 200 to x = 1000.**

That is the middle 800 px, 67% of the width, and it leaves 57 px of slack
past the cut line on each side. Do not design to the 143 px line exactly: the
card ratio is a template value that can change, and a headline sitting on the
boundary loses a letter the moment it does.

    0        200                              1000      1200
    |---cut---|--------- SAFE 800 px ----------|---cut---|
    |  143 px | 57 px slack       57 px slack  | 143 px  |

Vertically the full 630 px is visible, but keep 60 px clear top and bottom so
the composition survives a future ratio change.

## What went wrong in Batch 2

The covers set their headline at roughly x = 180, just inside the cut line, so
the listing rendered:

    "You own hundreds of buildings."  ->  "wn hundreds of buildings."
    "Property in your IRA?"           ->  "erty in your IRA?"
    "Signing up is easy."             ->  "gning up is easy."

Batch 1 is unaffected because its covers are charts composed centrally, where
the outer 12% carries nothing readable.

## Format and weight

- **PNG** for flat art, charts and anything with large uniform areas. Batch 1
  is PNG and holds up.
- **WebP** for photographic covers, quality 80 to 85. Batch 2 is WebP, and
  that is not what broke it, but several files were compressed far below what
  a photograph needs: six of the fifteen came in under 30 KB and one at 14 KB
  for a full 1200x630 frame.
- **Target 60 to 150 KB.** Under 60 KB a photographic cover starts banding;
  over 150 KB is wasted on a card that renders at 512 px wide.

## Naming and storage

    cover-<article-slug>-1200x630.<ext>

One per article, in that article's Drive folder. Drive holds the only copy,
so the no-delete rule applies: a replacement moves the old file to
`old version/` rather than overwriting it.

## Before shipping a cover

1. Draw a box from x=200 to x=1000 over the design. Every word inside it?
2. Crop the file to the middle 913 px and look at it. That is the card.
3. Check the weight against the band above.
