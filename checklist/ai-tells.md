# AI Tells: Ban List

The single biggest reason psfnetwork drafts read as AI-generated is unfiltered language tells. This list is the canonical inventory of those tells, with the required replacement pattern. The humanization reviewer (see `humanization-pass.md`) enforces this list on every draft before the expert panel sees it.

A draft cannot enter Stage 3 (Expert Panel) with any HIGH-tier ban-list match unresolved.

---

## How to use this list

- **HIGH** = automatic block. Reviewer removes or rewrites every occurrence.
- **MED** = remove unless the surrounding sentence is structurally dependent on it. Document the exception in the change log.
- **LOW** = remove if a tighter alternative exists; otherwise leave.

Match is case-insensitive, word-boundary aware. Variants and inflections count (e.g., "leverages", "leveraging", "leveraged").

---

## Tier 0: Hard punctuation bans (BLOCKING)

These are absolute. A draft with any of these does not enter Stage 3, period. No exceptions, no severity downgrade, no "but it reads better here." If you find yourself typing one of these, you have already failed the pass.

| Banned | Replace with |
|--------|--------------|
| Em-dash (, ) | Comma, colon, period, middle dot ( · ), or parentheses depending on context. Never an em-dash, anywhere, for any reason. |
| En-dash ( – ) | Same replacements as em-dash. Use hyphen ( - ) for ranges. | <!-- check-rules: allow -->
| Double-hyphen ( -- ) | Same. This is an em-dash typed in a hurry. Replace. |
| Smart quotes paired with em-dash construction | Cut the entire construction and rewrite the sentence in plain punctuation. |

The em-dash is the single most reliable AI tell in long-form prose. Models default to it. Humans writing on a phone or under deadline do not. Removing every em-dash from a draft does more for the human signal than any other single intervention on this list.

The replacement is almost always a period, sometimes a comma, occasionally a colon. If you cannot rewrite a sentence without an em-dash, the sentence is doing too much. Break it in two.

---

## Tier 1: Stock openers and closers (HIGH)

These give the post away in the first or last sentence.

| Banned | Replace with |
|--------|--------------|
| In today's rapidly evolving [X] landscape | Cut entirely. Start with a number, a question, or a scene. |
| In an ever-changing market | Cut. |
| Now more than ever | Cut. |
| It is important to note that | Cut. State the thing directly. |
| It is worth mentioning | Cut. |
| When it comes to [X] | "For [X]," or just start with the noun. |
| In conclusion | Cut. End with the strongest sentence in the piece. |
| To summarize / To wrap up / In summary | Cut. |
| At the end of the day | Cut. |
| Ultimately | Cut unless it carries actual sequencing weight. |

---

## Tier 2: Hype verbs and adjectives (HIGH)

These are the AI-marketing vocabulary that every model defaults to.

| Banned | Replace with |
|--------|--------------|
| unlock (as in "unlock value", "unlock returns") | Use the literal verb: "earn", "access", "open up to". |
| leverage (as a verb) | "use" |
| utilize | "use" |
| robust | Specific adjective: "tested", "withstood [X]", "fail-safe under [Y]" |
| comprehensive | Cut, or list what is covered |
| seamless | Cut, or describe the actual friction removed |
| streamlined | "shorter by [N] steps", "removes [specific step]" |
| cutting-edge | Name the technology |
| game-changing | Cut |
| revolutionary | Cut |
| disruptive | Cut |
| pivotal | "important" or name the effect |
| navigate (the complexities of) | "work through", "handle" |
| empower | "let", "give you" |
| harness | "use" |
| foster | "build", "create" |
| facilitate | "let", "help" |
| myriad | "many" or a number |
| plethora | "many" or a number |
| paradigm shift | Name the change |
| holistic | Cut or describe what it covers |
| synergy | Cut |
| ecosystem | Cut or name the players |
| innovative | Cut. Show, don't tell. |

---

## Tier 3: Connective tissue tells (MED)

AI overuses these as transition glue. Humans use them rarely.

| Banned at >2 per post | Notes |
|------------------------|-------|
| Furthermore | Use sparingly. Prefer "Also" or a period. |
| Moreover | Same. |
| Additionally | Same. |
| Importantly | Same. |
| Notably | Same. |
| Therefore | Use only when actually deriving a conclusion. |
| Thus | Same. |
| Hence | Same. |
| Consequently | Same. |
| As such | Cut. |

---

## Tier 4: Hedging weasels (HIGH near any factual claim)

These signal the model is unsure. Either source the claim or remove the claim.

| Banned | Action |
|--------|--------|
| may potentially | "may" OR "potentially", not both |
| could possibly | Same. |
| might be able to | "can" or "cannot" |
| is often considered | Source it or cut it |
| is widely regarded as | Source it or cut it |
| many experts believe | Name the experts or cut |
| studies have shown | Name the study or cut |
| it has been suggested | Who suggested? Cite or cut. |
| arguably | Take the position or cut |

Required disclosures (`brand/tone-and-voice.md`) are not hedges and are not in scope here.

---

## Tier 5: Rhetorical scaffolding (MED)

The "tell-them-what-you-told-them" structure of AI essays.

| Pattern | Action |
|---------|--------|
| "In this article, we will explore..." | Cut the entire sentence. The reader is already in the article. |
| "Before we dive in..." | Cut. |
| "Let's take a closer look at..." | Cut and start the closer look. |
| "But what does this mean for you?" | Cut and say what it means. |
| "Here's what you need to know:" | Cut and tell them. |
| "The bottom line is..." | Cut. State the bottom line directly. |
| "There are several factors to consider" | Replace with the number: "Three factors decide this." |

---

## Tier 6: Listicle and structure tells (MED)

| Pattern | Action |
|---------|--------|
| Every H2 is a list | At least 40% of H2s must be narrative paragraphs. |
| Every bullet is a fragment | Bullets that span a topic should be sentences with periods. |
| "Pros and Cons" sections | Allowed once per post max; prefer narrative trade-off paragraph. |
| FAQ section at the end with 8+ Qs | FAQ allowed up to 5 Qs; over that, fold into body. |
| "Key Takeaways" box at top AND bottom | One only. Prefer top, written as a 3-sentence paragraph, not bullets. |

---

## Tier 7: Cadence and rhythm (HIGH)

This is invisible on a scan, audible on a read.

A draft fails the cadence check if any of the following is true:

1. **No sentence under 6 words** in any 500-word stretch
2. **No sentence over 25 words** in the entire post
3. **Paragraph length variance is under 30%** (every paragraph is roughly the same size)
4. **Three consecutive paragraphs start with the same word or part of speech**
5. **Every paragraph has the same internal structure** (claim → evidence → claim → evidence...)

Fix: rewrite at least one sentence to be under 5 words and one sentence to be 25+ words, vary paragraph length, vary openers.

---

## Tier 8: Voice tells (HIGH)

The text refers to itself, hedges its identity, or breaks the second-person frame.

| Banned | Replace with |
|--------|--------------|
| "As an AI..." (any variant) | Block. Should never appear. |
| Third-person discussion of "investors" when the addressee is the investor | Switch to "you". |
| "We at psfnetwork..." opening | Lower-frequency. Allowed once per post max, ideally not in the opener. |
| Switching between "you" / "investors" / "one" within the same paragraph | Pick one and stay there. |

---

## Replacement principle

Most of these phrases exist because the model is filling space without thinking. The default replacement is **deletion**. If the sentence does not survive the deletion, the sentence had nothing to say.

When deletion would create a gap, replace with:
- A specific number
- A real example (see `humanization-pass.md` → Human Anchor requirements)
- A direct claim with a source

---

## Reviewer output

After running the ban-list pass, the humanization reviewer logs:

```
AI TELLS PASS
- HIGH matches found: [count]
- HIGH matches resolved: [count] (must equal found)
- MED matches found: [count]
- MED matches resolved: [count]
- LOW matches found: [count]
- LOW matches resolved: [count]
- Cadence check: PASS / FAIL (if FAIL, list which Tier 7 rule failed)
- Voice check: PASS / FAIL
```

This block is appended to the humanization log for the post.
