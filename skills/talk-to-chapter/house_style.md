# House style for chapters

These are standing preferences applied to every chapter produced by this skill.

## Punctuation

- No em-dashes. Use commas, semicolons, parentheses, or sentence breaks.
- No en-dashes in prose. Use "to" for ranges (e.g. "4000 to 6000 words", not "4000-6000").
- Oxford comma in lists of three or more.
- Straight quotes, not curly, unless the publisher specifies otherwise.

## Word-level

Cut on sight unless they carry real meaning:
- really, very, actually, just, literally, basically
- kind of, sort of, somewhat
- I think, I believe, in my opinion (the chapter is by the author; this is assumed)
- "you know", "right?", "I mean" (oral fillers)
- "in order to" (almost always replaceable by "to")

Prefer:
- "because" over "due to the fact that"
- "to" over "in order to"
- active voice over passive, unless the actor is genuinely unknown or unimportant
- one strong verb over a noun phrase ("decided" over "made the decision")

## Sentence-level

- Short sentences are fine. Variation in length is the goal.
- Open paragraphs with claims, not announcements.
- Avoid "There is/are" openings when a stronger subject is available.
- Avoid metadiscourse ("In this section we will discuss") in published prose.

## Technical writing

- Define jargon on first use, then use it freely.
- Numbers under ten in words, ten and above in digits, except in technical contexts (token counts, version numbers, percentages) where digits are clearer.
- Code, file paths, and command names in backticks.
- Code blocks fenced with language identifier when known.

## Tone

- Technical reference: precise, dry, look-up-friendly. Like `docs.claude.com`.
- Not speaker-faithful. Do not preserve conversational idiom, jokes, or personality.
- Not first-person essay. No "I think", no "we found that".
- Direct, not deferential. Confident about established facts.
- Honest about uncertainty: use `[EDITOR QUERY: ...]` rather than hedging.
- No false modesty, no over-promising.

## Audience

- The author: a senior engineer. No need to define standard engineering jargon.
- Define Anthropic-specific or Claude-specific terms on first use, then use freely.
- No gentle introductions or "in this chapter you will learn" framing.
