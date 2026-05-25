# talk-to-chapter

A Claude Code skill that transforms a Claude Academy talk corpus into a technical-reference book chapter.

## What it does

Reads the full chapter corpus from `chapters/<slug>/` (transcript, summary, entities, enrichment notes, overlap report) and produces a Markdown chapter of roughly 4000 to 6000 words. The skill runs in six phases with one explicit checkpoint (outline approval) before drafting begins.

The skill is opinionated about three things:
1. It never invents technical content. Uncertainty becomes inline editor queries, not guesses.
2. It does not mirror the talk's order. A chapter is concept-organised, not talk-chronological.
3. It writes in technical-reference voice (like `docs.claude.com`), not the speaker's conversational style.

## Inputs

The skill expects a corpus in `chapters/<slug>/` assembled by earlier pipeline steps:

- `source/transcript.txt` (required, from step 1)
- `metadata.yaml` (required, from step 1)
- `summary.md` (from step 2, if available)
- `entities.json` (from step 2, if available)
- `quotes.md` (from step 2, if available)
- `enrichment.md` (from step 3, if available)
- `overlap_report.md` (from step 5, if available)

Not all files will exist for every chapter. The skill works with what is available.

## How to invoke

Point Claude at a chapter slug:

- "Draft chapter for beyond-the-basics-with-claude-code."
- "Write the chapter from the corpus in chapters/beyond-the-basics/."
- "Convert the Beyond the Basics talk into a chapter, target 5000 words."

Optional arguments worth specifying upfront:
- Target word count (default 4000 to 6000)
- Book context (other chapters already drafted)

## What you will get back

Six phases in sequence:

1. **Triage memo** (Phase 1): thesis, claims, enrichment deltas, overlap notes, garbled passages, stage artefacts.
2. **Outline** (Phase 2, CHECKPOINT): proposed chapter structure with word budgets and overlap decisions. **The skill stops here and waits for your approval.**
3. **Draft chapter** (Phase 3): full Markdown chapter with inline editor queries and cross-references.
4. **Fidelity audit** (Phase 4): table mapping every chapter claim to its corpus source.
5. **Polished final** (Phase 5): em-dashes removed, intensifiers cut, oral artefacts hunted, cross-references verified.
6. **Book index update** (Phase 6): `book_index.json` updated with this chapter's entry.

Output: `chapters/<slug>/chapter.md` with editor queries and fidelity audit appended. Audit also written separately to `chapters/<slug>/audit.md`.

## Customising

- Edit `house_style.md` to change standing style preferences (the no-em-dash rule, intensifier list, tone, etc.)
- Add example transformations to `examples/` to improve consistency across chapters
- Adjust the default word target by editing the relevant line in `SKILL.md`

## When not to use this skill

- Short summaries or blog posts under 1500 words: write them directly.
- Verbatim cleanup that preserves oral form: this skill rewrites, it does not preserve.
- Meeting minutes or operational reports: different genre.

## Files

- `SKILL.md`: the procedure Claude follows
- `house_style.md`: standing style preferences
- `README.md`: this file
- `examples/`: before-and-after pairs (add your own to improve future runs)
