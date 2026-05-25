---
name: talk-to-chapter
description: Transform a Claude Academy talk transcript into a technical-reference book chapter. Use when a chapter corpus exists in chapters/<slug>/ (transcript, summary, entities, enrichment, overlap report) and the user asks to draft or redraft that chapter. Trigger phrases include "draft chapter for <slug>", "turn this talk into a chapter", "write the chapter", or any variation where the input is a talk corpus and the desired output is a technical-reference chapter. Do NOT use for short summaries, blog posts, or executive briefs.
---

# Talk to Chapter

## What this skill does

Transforms a Claude Academy talk corpus into a technical-reference book chapter. The input is not just a transcript; it is the full corpus assembled by the pipeline in `chapters/<slug>/` (transcript, summary, entities, enrichment notes, overlap report). The output is a concept-organised chapter written in dry, precise, reference-manual prose, like `docs.claude.com`. The chapter is a personal technical reference, not a publication under the speaker's name. Your job is to rebuild the talk's content into a structure a reader would look things up in, not to preserve the speaker's voice or the talk's narrative order.

## Hard rules (never violate)

1. **Never invent technical content.** No invented numbers, product behaviours, code examples, or attributions. If the corpus does not say it, you do not write it.
2. **Prefer enrichment over transcript when they conflict.** Speakers describe features as they existed at recording time. `enrichment.md` contains current information from `docs.claude.com`. When the two conflict, use the current info and note the change.
3. **Flag uncertainty inline.** When a passage is too garbled to repair confidently, insert `[EDITOR QUERY: <your specific question>]` rather than guessing. Better to leave ten queries than invent one fact.
4. **No em-dashes.** Use commas, semicolons, parentheses, or sentence breaks. This is a standing house style rule.
5. **No empty intensifiers.** Cut "really", "very", "actually", "just", "literally" unless they carry real meaning. The speaker uses these constantly in oral mode; the reader does not need them.
6. **Keep strong technical metaphors.** If the speaker says "red squigglies", "running NPM on an Arduino", "this is ED, not Vim", keep those phrases when they clarify a concept. They become the chapter's illustrations, not its voice.
7. **Do not mirror the talk's order.** Talks loop, backtrack, and recover. Chapters do not. Reorganise by concept, not by talk chronology.
8. **Respect the overlap report.** If `overlap_report.md` says another chapter owns a concept in depth, do not re-explain it here. Summarise in one sentence and insert a cross-reference ("see Chapter X").

## Procedure

Run these phases in order. Stop at the checkpoint in Phase 2 and wait for user approval before drafting prose.

### Phase 1: Corpus ingestion and triage

Read the full corpus in `chapters/<slug>/` before doing anything else:

- `source/transcript.txt` (the raw Whisper output)
- `metadata.yaml` (video ID, title, duration, URL)
- `summary.md` (abstract + key claims, if available)
- `entities.json` (products, features, concepts, people)
- `quotes.md` (notable verbatim quotes, if available)
- `enrichment.md` (current docs.claude.com info for entities, if available)
- `overlap_report.md` (how this chapter relates to already-drafted chapters, if available)

Not all files will exist for every chapter. Work with what is available; flag what is missing.

Then produce a triage memo (max one page) containing:

- **Speaker, venue, talk title** (from `metadata.yaml` and transcript)
- **One-sentence thesis** as the speaker actually argues it, not as they announce it
- **Three to seven load-bearing claims** that the chapter must preserve
- **Useful metaphors and idioms** worth keeping as illustrations
- **Enrichment deltas**: where the speaker's description of a feature differs from current `docs.claude.com` info
- **Overlap notes**: concepts this chapter shares with existing chapters, and which chapter should own each
- **Garbled passages** that need editorial decisions (give line ranges or distinctive phrases)
- **Stage artefacts inventory** (greetings, time checks, audience polls, slide cues, thanks) which will all be removed

Present this memo to the user. Do not proceed without acknowledgment, but do not require formal approval; the memo is for transparency.

### Phase 2: Structural proposal (CHECKPOINT)

Build a chapter outline. This is the highest-leverage step in the whole skill. The first instinct is to mirror the talk; resist it. Ask: what is the chapter's logical structure if a reader looked something up in it cold?

The chapter structure should be concept-organised, not narrative. A typical structure: Concepts / Customisation primitives / Patterns / Reference, with the talk's evidence populating that structure.

Produce:
- Proposed chapter title (working)
- 4 to 8 section headings with one-line descriptions of what each section covers
- Word budget per section, summing to a target chapter length (default 4000 to 6000 words; ask if unclear)
- **Overlap decisions**: for each concept flagged in the overlap report, state whether this chapter owns it, defers it (with cross-reference), or gives a brief summary with pointer
- Notes on what gets cut entirely (e.g. live audience polls, in-room jokes that do not translate)
- Notes on what gets promoted or demoted relative to the talk (a throwaway aside in the talk may be the strongest point on the page)

**STOP here and present the outline.** Ask the user to approve or revise before any prose is written. Rewriting prose is expensive; rewriting an outline is cheap.

### Phase 3: Drafting

Write the chapter section by section against the approved outline. For each section:

- Open with a claim or definition, not an announcement. Not "In this section I will discuss X." State what X is.
- Write in technical-reference voice: precise, dry, look-up-friendly. Think `docs.claude.com`, not essay, not speaker's conversational style.
- Convert second-person room asides ("who here has used ED?") into declarative prose.
- Where the speaker shows a slide or code, render it as a fenced code block or inline example, but only if the content is recoverable from the corpus.
- When `enrichment.md` provides current information that supersedes what the speaker said, use the current info. Note the update briefly if the difference is significant.
- Preserve technical precision. If the speaker says "ten times as much for uncached tokens", that number stays; do not round or generalise.
- Where the overlap report assigns a concept to another chapter, insert a cross-reference: "see Chapter N: Title" (use the slug and title from `book_index.json`).
- Mark every uncertainty with `[EDITOR QUERY: ...]` inline.

Write in Markdown. Use H2 for section headings, H3 sparingly for sub-points. Code blocks for any config, JSON, or command examples. No bullet lists for narrative content; use prose. Bullets only for genuinely enumerable items (e.g. "the four customisation primitives are...").

### Phase 4: Fidelity audit

After the draft is complete, run a fidelity check. Produce a table with three columns: **Claim in chapter** | **Transcript support (line or phrase)** | **Verdict** (supported / paraphrased / unsupported / inferred).

Any row marked "unsupported" or "inferred" must either be removed from the chapter or converted to an editor query. Do this before showing the user the final draft.

### Phase 5: Polish

Final pass for:
- Em-dash removal (search `---`, `—` and `--` and rewrite)
- Empty intensifier hunt ("really", "very", "actually", "just", "literally", "basically", "kind of", "sort of")
- Passive voice where active is stronger
- Oral artefacts that survived earlier passes ("you know", "right?", "I mean", "so")
- Heading consistency and flow
- One final read for sentences that still sound spoken rather than written
- Verify all cross-references point to valid chapter slugs in `book_index.json`

### Phase 6: Update book index

After the chapter is finalised, update the top-level `book_index.json` with this chapter's entry:

- `slug`, `title`, `source` (speaker, venue, date)
- `covers_in_depth`: concepts this chapter owns
- `mentions_only`: concepts mentioned but not explained
- `entities`: from `entities.json`
- `code_examples`: any fenced code blocks included in the chapter

If `book_index.json` does not exist yet, create it with the schema defined in `docs/pipeline.md`.

## Output structure

Write the chapter to `chapters/<slug>/chapter.md`.

At the top of the file, before the chapter itself, include a brief frontmatter block (HTML comment, not YAML, so it does not render):

```
<!--
Source: <talk title, speaker, venue, date if known>
Corpus: chapters/<slug>/
Target length: <N> words
Editor queries: <count>
Fidelity audit: <pass / N items flagged>
Enrichment deltas applied: <count>
Cross-references inserted: <count>
-->
```

Then the chapter title as H1, then the chapter.

After the chapter, append two sections:

- `## Editor queries` listing every `[EDITOR QUERY: ...]` from the draft with the surrounding context so the user can resolve them
- `## Fidelity audit` containing the table from Phase 4

Additionally, write the audit table separately to `chapters/<slug>/audit.md` for pipeline tracking.

## When the transcript is broken

ASR transcripts often have stretches of pure garble (the speaker said something but the recogniser failed). Signs include: repeated phrases that loop nonsensically, sudden topic jumps with no transition, proper nouns mangled into common words, or sentences that parse grammatically but say nothing.

Rules for handling these:
- If the surrounding context makes the intended meaning clear with high confidence, repair silently and note it in the triage memo.
- If the meaning is recoverable but not certain, repair and add an editor query.
- If the meaning is not recoverable, do not invent a bridge. Either omit the passage entirely (noting the cut in the triage memo) or insert `[EDITOR QUERY: passage at <location> is garbled; please clarify the intended point]`.

## What this skill is not for

- **Short summaries** or executive briefs: just write them directly
- **Verbatim transcripts** cleaned for accuracy but preserving oral form: this skill rewrites; it does not preserve
- **Scientific manuscripts**: different pipeline
- **Meeting minutes or rapporteur reports**: different genre

## Voice

The chapter voice is technical reference: precise, dry, look-up-friendly. Think `docs.claude.com`. Not speaker-faithful (do not preserve the speaker's conversational idiom). Not first-person essay. Not narrative.

The audience is the author (a senior engineer). No need to translate jargon for non-engineers. No need for gentle introductions. Direct technical content throughout.

Strong metaphors from the speaker (e.g. "red squigglies", "USB-C for AI") can be kept when they genuinely clarify a concept, but they serve the reference, not the speaker's personality.
