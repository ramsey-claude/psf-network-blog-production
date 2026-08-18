# Client Decisions

Dated log of decisions received from the client. Each entry keeps the
client's own words (quoted) and states what the pipeline does with them.
These are standing policy until a later entry supersedes them; nothing
here is deleted, only superseded.

## 2026-08-18: disclaimer, CTAs and link targets pre-launch

Received by email through the operator, answering the three questions sent
with the Batch 2 delivery.

### 1. Disclaimer ("legend") language

> "I think we can carry the same language as its complaint, I don't see why
> it would change materially pre or post launch"

The compliance disclaimer block keeps its current wording, before and after
launch. No article edits follow from launch day. ("as its complaint" read as
"as is, compliant" - the sentence's intent is unambiguous either way: no
material change pre or post launch.)

### 2. CTAs: waitlist only until the offering is qualified

> "Our plan is to point readers to the waitlist only, and to avoid any
> 'invest now' language until the offering is qualified. Until we launch, we
> should continue driving traffic to waitlist and homepage as normal. We can
> always adjust down the line"

Pipeline consequences:
- No draft may carry "invest now" style direct-response language until the
  client says the offering is qualified. Enforced as qa_battery W10 (WARN),
  which greps the imperative phrasings only; the word "invest" in editorial
  prose stays untouched.
- CTA destinations are the waitlist and the homepage. As of this entry no
  published or drafted article contains such CTA language (checked across
  all 36 drafts), so this is policy for new content, not a cleanup.

### 3. Link targets from blog articles

> "Preference is for Waitlist, but yes these are acceptable links
> [/how-it-works and /investors], any link that is most relevant to the
> topic of the article should be used. Blog is not a direct response
> channel, so I would not enforce an 'Invest Now' if it does not make sense
> pre or post launch"

Pipeline consequences:
- /how-it-works and /investors are allowed link destinations when they fit
  the article's topic; the waitlist is preferred where a nudge fits.
- The blog is not a direct-response channel: relevance beats conversion.
  No forced CTA blocks.
- Current state: Batch 1-3 drafts link only to blog articles and the
  homepage. Batch 3's internal-link pass (the 47 relative links) may now
  also use /how-it-works and /investors where topical, absolute form as
  always (https://www.psfnetwork.com/...).
